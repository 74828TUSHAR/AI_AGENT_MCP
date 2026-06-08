from dataclasses import dataclass, field
from typing import Any


@dataclass
class ApiResponse:
    method: str
    endpoint: str
    url: str
    http_status: int
    body_text: str
    body_json: dict[str, Any] | list[Any] | None
    duration_ms: int
    request_headers: dict[str, Any] = field(default_factory=dict)
    request_payload: Any = None
    request_params: dict[str, Any] | None = None
    retry_count: int = 0

    @property
    def status_code(self):
        return self.http_status

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
