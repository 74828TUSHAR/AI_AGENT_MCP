import json
import time
from dataclasses import dataclass
from typing import Any

from utils.logger import get_logger


@dataclass
class ApiResult:
    method: str
    endpoint: str
    url: str
    http_status: int
    body_text: str
    body_json: dict[str, Any] | list[Any] | None
    duration_ms: int

    @property
    def response_code(self):
        if isinstance(self.body_json, dict):
            return self.body_json.get("responseCode")
        return None

    @property
    def message(self):
        if isinstance(self.body_json, dict):
            return self.body_json.get("message")
        return None


class AutomationExerciseApiClient:
    def __init__(self, request_context):
        self.request_context = request_context
        self.logger = get_logger(self.__class__.__name__)

    async def get(self, endpoint, *, params=None, headers=None):
        return await self._request("GET", endpoint, params=params, headers=headers)

    async def post(self, endpoint, *, form=None, params=None, headers=None):
        return await self._request("POST", endpoint, form=form, params=params, headers=headers)

    async def put(self, endpoint, *, form=None, params=None, headers=None):
        return await self._request("PUT", endpoint, form=form, params=params, headers=headers)

    async def delete(self, endpoint, *, form=None, params=None, headers=None):
        return await self._request("DELETE", endpoint, form=form, params=params, headers=headers)

    async def _request(self, method, endpoint, *, form=None, params=None, headers=None):
        request_fn = getattr(self.request_context, method.lower())
        self._log_request(method, endpoint, params=params, form=form, headers=headers)

        start = time.perf_counter()
        response = await request_fn(endpoint, params=params, form=form, headers=headers)
        duration_ms = round((time.perf_counter() - start) * 1000)

        body_text = await response.text()
        body_json = self._safe_json_loads(body_text)
        result = ApiResult(
            method=method,
            endpoint=endpoint,
            url=response.url,
            http_status=response.status,
            body_text=body_text,
            body_json=body_json,
            duration_ms=duration_ms,
        )
        self._log_response(result)
        return result

    def _safe_json_loads(self, body_text):
        if not body_text:
            return None
        try:
            return json.loads(body_text)
        except json.JSONDecodeError:
            return None

    def _log_request(self, method, endpoint, *, params=None, form=None, headers=None):
        self.logger.info(
            "API REQUEST | method=%s | endpoint=%s | params=%s | form=%s | headers=%s",
            method,
            endpoint,
            params,
            form,
            headers,
        )

    def _log_response(self, result):
        self.logger.info(
            "API RESPONSE | method=%s | endpoint=%s | http_status=%s | response_code=%s | message=%s | duration_ms=%s",
            result.method,
            result.endpoint,
            result.http_status,
            result.response_code,
            result.message,
            result.duration_ms,
        )
