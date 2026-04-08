import inspect
import json
from pathlib import Path

import allure

def _attach_payload(name, payload):
    allure.attach(
        json.dumps(payload, indent=2, default=str),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )


def assert_api_field_equal(logger, *, field_name, actual, expected, response=None):
    if response:
        _attach_payload("api_response", _serialize_response(response))

    if actual != expected:
        line_num = inspect.currentframe().f_back.f_lineno
        logger.error(
            "API ASSERTION FAILED | line=%s | field=%s | expected=%s | actual=%s",
            line_num,
            field_name,
            expected,
            actual,
        )
        if response:
            logger.error(
                "API RESPONSE DETAILS | http_status=%s | response_code=%s | message=%s",
                response.http_status,
                response.response_code,
                response.message,
            )
        error = AssertionError(
            f"{field_name} mismatch at line {line_num}. Expected: {expected} | Actual: {actual}"
        )
        error.api_response = response
        raise error

    logger.info(
        "API ASSERTION PASSED | field=%s | expected=%s | actual=%s",
        field_name,
        expected,
        actual,
    )


def assert_api_truthy(logger, *, field_name, actual, response=None):
    if response:
        _attach_payload("api_response", _serialize_response(response))

    if not actual:
        line_num = inspect.currentframe().f_back.f_lineno
        logger.error(
            "API ASSERTION FAILED | line=%s | field=%s | expected_truthy=True | actual=%s",
            line_num,
            field_name,
            actual,
        )
        error = AssertionError(
            f"{field_name} expected truthy at line {line_num}. Actual: {actual}"
        )
        error.api_response = response
        raise error

    logger.info("API ASSERTION PASSED | field=%s | actual=%s", field_name, actual)


def write_api_failure_artifact(test_case_name, scenario_name, response):
    screenshots_dir = Path("screenshots")
    screenshots_dir.mkdir(exist_ok=True)
    artifact_path = screenshots_dir / f"{test_case_name}_{scenario_name}_api_failure.json"
    artifact_path.write_text(json.dumps(_serialize_response(response), indent=2), encoding="utf-8")
    return artifact_path


def _serialize_response(response):
    return {
        "method": response.method,
        "endpoint": response.endpoint,
        "url": response.url,
        "http_status": response.http_status,
        "response_code": response.response_code,
        "message": response.message,
        "duration_ms": response.duration_ms,
        "body_json": response.body_json,
        "body_text": response.body_text,
    }
