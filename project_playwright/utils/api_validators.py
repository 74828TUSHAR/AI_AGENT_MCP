import json
from typing import Any

import allure

from core.api_exceptions import ApiValidationError


def _payload_from_response(response_or_payload):
    if hasattr(response_or_payload, "body_json"):
        return response_or_payload.body_json
    return response_or_payload


def _text_from_response(response_or_payload):
    if hasattr(response_or_payload, "body_text"):
        return response_or_payload.body_text
    if isinstance(response_or_payload, (dict, list)):
        return json.dumps(response_or_payload, default=str)
    return str(response_or_payload)


def _attach_validation(name: str, payload: Any):
    try:
        allure.attach(
            json.dumps(payload, indent=2, default=str),
            name=name,
            attachment_type=allure.attachment_type.JSON,
        )
    except Exception:
        return


def validate_status_code(logger, response, expected_status: int):
    actual_status = getattr(response, "http_status", getattr(response, "status_code", None))
    if actual_status != expected_status:
        _attach_validation(
            "status_code_failure",
            {"expected": expected_status, "actual": actual_status, "response": _payload_from_response(response)},
        )
        logger.error("Status code validation failed | expected=%s | actual=%s", expected_status, actual_status)
        raise ApiValidationError(f"Expected status code {expected_status}, got {actual_status}")

    logger.info("Status code validation passed | expected=%s | actual=%s", expected_status, actual_status)


def validate_response_time(logger, response, max_ms: int):
    actual_ms = getattr(response, "duration_ms", None)
    if actual_ms is None or actual_ms > max_ms:
        _attach_validation(
            "response_time_failure",
            {"max_ms": max_ms, "actual_ms": actual_ms, "response": _payload_from_response(response)},
        )
        logger.error("Response time validation failed | max_ms=%s | actual_ms=%s", max_ms, actual_ms)
        raise ApiValidationError(f"Expected response time <= {max_ms}ms, got {actual_ms}ms")

    logger.info("Response time validation passed | max_ms=%s | actual_ms=%s", max_ms, actual_ms)


def validate_schema(logger, response_or_payload, expected_schema):
    payload = _payload_from_response(response_or_payload)

    def _validate(actual, expected, path="root"):
        if isinstance(expected, type):
            if not isinstance(actual, expected):
                raise ApiValidationError(f"Schema mismatch at {path}: expected {expected.__name__}, got {type(actual).__name__}")
            return

        if isinstance(expected, dict):
            if not isinstance(actual, dict):
                raise ApiValidationError(f"Schema mismatch at {path}: expected dict, got {type(actual).__name__}")
            for key, nested in expected.items():
                if key not in actual:
                    raise ApiValidationError(f"Schema mismatch at {path}: missing key '{key}'")
                _validate(actual[key], nested, f"{path}.{key}")
            return

        if isinstance(expected, list):
            if not isinstance(actual, list):
                raise ApiValidationError(f"Schema mismatch at {path}: expected list, got {type(actual).__name__}")
            if expected:
                sample = expected[0]
                for index, item in enumerate(actual):
                    _validate(item, sample, f"{path}[{index}]")
            return

        if callable(expected):
            if not expected(actual):
                raise ApiValidationError(f"Schema predicate failed at {path}")
            return

        if actual != expected:
            raise ApiValidationError(f"Schema mismatch at {path}: expected {expected}, got {actual}")

    try:
        _validate(payload, expected_schema)
    except ApiValidationError as exc:
        _attach_validation(
            "schema_validation_failure",
            {"expected_schema": str(expected_schema), "response": payload, "error": str(exc)},
        )
        logger.error("Schema validation failed | error=%s", exc)
        raise

    logger.info("Schema validation passed")


def validate_response_contains(logger, response_or_payload, expected_value, *, path: str | None = None):
    payload = _payload_from_response(response_or_payload)
    haystack = payload
    if path:
        for segment in path.split("."):
            if isinstance(haystack, dict):
                haystack = haystack.get(segment)
            else:
                haystack = None
                break

    text = _text_from_response(haystack if path else payload)
    if str(expected_value) not in text:
        _attach_validation(
            "response_contains_failure",
            {"expected_value": expected_value, "path": path, "response": payload},
        )
        logger.error("Response contains validation failed | expected=%s | path=%s", expected_value, path)
        raise ApiValidationError(f"Response did not contain '{expected_value}'")

    logger.info("Response contains validation passed | expected=%s | path=%s", expected_value, path)
