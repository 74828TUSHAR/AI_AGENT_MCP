import asyncio
import inspect
import json
import logging
import mimetypes
import os
import time
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import allure
from playwright.async_api import Error as PlaywrightError
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from config.config import get_env
from core.api_exceptions import ApiRequestError, ApiRetryError, ApiTimeoutError
from core.api_models import ApiResponse
from core.auth_manager import AuthManager
from utils.logger import get_logger


class BaseAPI:
    DEFAULT_RETRYABLE_STATUSES = {500, 502, 503, 504}

    def __init__(
        self,
        request_context,
        *,
        base_url: str | None = None,
        auth_manager: AuthManager | None = None,
        default_headers: dict[str, Any] | None = None,
        timeout_ms: int | None = None,
        max_retries: int | None = None,
        retry_delay_ms: int | None = None,
        retryable_statuses: set[int] | None = None,
        log_response_body: bool | None = None,
        attach_to_report: bool = True,
        logger: logging.Logger | None = None,
    ):
        self.request_context = request_context
        self._fallback_logger = logger or get_logger(self.__class__.__name__)
        self.environment = os.getenv("ENV", "qa")
        self.base_url = self._resolve_base_url(base_url)
        self.auth_manager = auth_manager or AuthManager(logger=self.logger)
        self.default_headers = dict(default_headers or {})
        self.timeout_ms = timeout_ms if timeout_ms is not None else int(os.getenv("API_TIMEOUT_MS", "30000"))
        self.max_retries = max_retries if max_retries is not None else int(os.getenv("API_RETRY_COUNT", "2"))
        self.retry_delay_ms = retry_delay_ms if retry_delay_ms is not None else int(os.getenv("API_RETRY_DELAY_MS", "250"))
        self.retryable_statuses = set(retryable_statuses or self.DEFAULT_RETRYABLE_STATUSES)
        self.log_response_body = (
            log_response_body
            if log_response_body is not None
            else os.getenv("API_LOG_RESPONSE_BODY", "false").lower() == "true"
        )
        self.attach_to_report = attach_to_report

    @property
    def logger(self) -> logging.Logger:
        return self._resolve_logger() or self._fallback_logger

    def _resolve_logger(self) -> logging.Logger:
        frame = inspect.currentframe()
        try:
            frame = frame.f_back
            while frame:
                module_name = frame.f_globals.get("__name__", "")
                file_name = frame.f_code.co_filename.replace("\\", "/")
                if "/tests/" in file_name or module_name.startswith("test_") or ".tests." in module_name:
                    return logging.getLogger(module_name)
                frame = frame.f_back
        finally:
            del frame

        return None

    def _resolve_base_url(self, base_url: str | None) -> str:
        if base_url:
            return base_url

        env_config = get_env(self.environment) or {}
        return env_config.get("api_base_url") or env_config.get("base_url") or ""

    def _build_url(self, endpoint: str) -> str:
        if endpoint.startswith(("http://", "https://")):
            return endpoint
        if not self.base_url:
            return endpoint
        return urljoin(self.base_url.rstrip("/") + "/", endpoint.lstrip("/"))

    def _safe_json_loads(self, body_text: str):
        if not body_text:
            return None
        try:
            return json.loads(body_text)
        except json.JSONDecodeError:
            return None

    def _truncate(self, value: Any, limit: int = 2000) -> str:
        text = value if isinstance(value, str) else json.dumps(value, default=str, indent=2)
        return text if len(text) <= limit else f"{text[:limit]}... [truncated]"

    def _log_request(self, method: str, endpoint: str, *, headers=None, params=None, payload=None, multipart=None):
        self.logger.info("API Request Started")
        self.logger.info("Method: %s", method)
        self.logger.info("Endpoint: %s", endpoint)
        if params:
            self.logger.info("Query Params: %s", params)
        if headers:
            self.logger.info("Headers: %s", headers)
        if payload is not None:
            self.logger.info("Payload Sent: %s", self._truncate(payload))
        if multipart is not None:
            self.logger.info("Multipart Payload Sent: %s", self._truncate({k: v for k, v in multipart.items() if k != "buffer"}))

    def _log_response(self, response: ApiResponse):
        self.logger.info("Response Status: %s", response.http_status)
        self.logger.info("Response Time: %sms", response.duration_ms)
        if self.log_response_body or response.http_status >= 400:
            self.logger.info("Response Body: %s", self._truncate(response.body_text))
        self.logger.info("API Request Completed")

    def _attach_report_data(self, *, method: str, endpoint: str, request_payload, request_headers, request_params, response: ApiResponse | None = None, failure: Exception | None = None):
        if not self.attach_to_report:
            return

        def attach_json(name: str, payload: Any):
            allure.attach(
                json.dumps(payload, indent=2, default=str),
                name=name,
                attachment_type=allure.attachment_type.JSON,
            )

        try:
            attach_json(
                "api_request",
                {
                    "method": method,
                    "endpoint": endpoint,
                    "headers": request_headers,
                    "params": request_params,
                    "payload": request_payload,
                },
            )
            if response:
                attach_json(
                    "api_response",
                    {
                        "url": response.url,
                        "http_status": response.http_status,
                        "duration_ms": response.duration_ms,
                        "body_text": response.body_text,
                        "body_json": response.body_json,
                        "retry_count": response.retry_count,
                    },
                )
            if failure:
                attach_json("api_failure", {"type": type(failure).__name__, "message": str(failure)})
        except Exception:
            # Report attachment should never break the request flow.
            return

    async def _send_request(self, method: str, endpoint: str, *, params=None, headers=None, data=None, form=None, multipart=None, timeout=None):
        if data is not None and form is not None:
            raise ValueError("Use either 'data' or 'form' for a single request, not both.")

        request_headers = self.auth_manager.build_headers({**self.default_headers, **(headers or {})})
        resolved_url = self._build_url(endpoint)
        request_payload = multipart if multipart is not None else data if data is not None else form
        request_timeout = timeout if timeout is not None else self.timeout_ms
        request_options = {
            "params": params,
            "headers": request_headers,
            "timeout": request_timeout,
        }
        if data is not None:
            request_options["data"] = data
        if form is not None:
            request_options["form"] = form
        if multipart is not None:
            request_options["multipart"] = multipart

        self._log_request(method, endpoint, headers=request_headers, params=params, payload=request_payload, multipart=multipart)

        last_exception = None
        attempt = 0
        while attempt <= self.max_retries:
            try:
                start = time.perf_counter()
                request_fn = getattr(self.request_context, method.lower())
                response = await request_fn(resolved_url, **request_options)
                duration_ms = round((time.perf_counter() - start) * 1000)
                body_text = await response.text()
                body_json = self._safe_json_loads(body_text)

                result = ApiResponse(
                    method=method,
                    endpoint=endpoint,
                    url=response.url,
                    http_status=response.status,
                    body_text=body_text,
                    body_json=body_json,
                    duration_ms=duration_ms,
                    request_headers=request_headers,
                    request_payload=request_payload,
                    request_params=params,
                    retry_count=attempt,
                )
                self._log_response(result)
                self._attach_report_data(
                    method=method,
                    endpoint=endpoint,
                    request_payload=request_payload,
                    request_headers=request_headers,
                    request_params=params,
                    response=result,
                )

                if result.http_status in self.retryable_statuses and attempt < self.max_retries:
                    self.logger.warning(
                        "Retryable HTTP status encountered | status=%s | attempt=%s/%s",
                        result.http_status,
                        attempt + 1,
                        self.max_retries,
                    )
                    attempt += 1
                    await asyncio.sleep(self.retry_delay_ms / 1000)
                    continue

                return result
            except PlaywrightTimeoutError as exc:
                last_exception = exc
                self.logger.error("Timeout Occurred | method=%s | endpoint=%s | attempt=%s/%s | error=%s", method, endpoint, attempt + 1, self.max_retries, exc)
                self._attach_report_data(
                    method=method,
                    endpoint=endpoint,
                    request_payload=request_payload,
                    request_headers=request_headers,
                    request_params=params,
                    failure=exc,
                )
                if attempt >= self.max_retries:
                    raise ApiTimeoutError(f"Timeout while calling {method} {endpoint}") from exc
            except (PlaywrightError, OSError, ConnectionError) as exc:
                last_exception = exc
                self.logger.error("Request Failed | method=%s | endpoint=%s | attempt=%s/%s | error=%s", method, endpoint, attempt + 1, self.max_retries, exc)
                self._attach_report_data(
                    method=method,
                    endpoint=endpoint,
                    request_payload=request_payload,
                    request_headers=request_headers,
                    request_params=params,
                    failure=exc,
                )
                if attempt >= self.max_retries:
                    raise ApiRequestError(f"Failed to call {method} {endpoint}") from exc

            attempt += 1
            await asyncio.sleep(self.retry_delay_ms / 1000)

        raise ApiRetryError(f"Retry attempts exhausted for {method} {endpoint}") from last_exception

    async def get(self, endpoint, *, params=None, headers=None, timeout=None):
        return await self._send_request("GET", endpoint, params=params, headers=headers, timeout=timeout)

    async def post(self, endpoint, *, data=None, form=None, params=None, headers=None, timeout=None):
        return await self._send_request("POST", endpoint, data=data, form=form, params=params, headers=headers, timeout=timeout)

    async def put(self, endpoint, *, data=None, form=None, params=None, headers=None, timeout=None):
        return await self._send_request("PUT", endpoint, data=data, form=form, params=params, headers=headers, timeout=timeout)

    async def patch(self, endpoint, *, data=None, form=None, params=None, headers=None, timeout=None):
        return await self._send_request("PATCH", endpoint, data=data, form=form, params=params, headers=headers, timeout=timeout)

    async def delete(self, endpoint, *, data=None, form=None, params=None, headers=None, timeout=None):
        return await self._send_request("DELETE", endpoint, data=data, form=form, params=params, headers=headers, timeout=timeout)

    async def upload_file(
        self,
        endpoint,
        *,
        file_path: str,
        field_name: str = "file",
        params=None,
        headers=None,
        form=None,
        timeout=None,
    ):
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Upload file not found: {path}")

        mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        multipart = dict(form or {})
        multipart[field_name] = {
            "name": path.name,
            "mimeType": mime_type,
            "buffer": path.read_bytes(),
        }
        return await self._send_request(
            "POST",
            endpoint,
            params=params,
            headers=headers,
            multipart=multipart,
            timeout=timeout,
        )

    async def close_session(self):
        self.auth_manager.clear_token()
