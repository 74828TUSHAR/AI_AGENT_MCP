class ApiError(Exception):
    """Base exception for API framework failures."""


class ApiRequestError(ApiError):
    """Raised when a request cannot be completed."""


class ApiTimeoutError(ApiRequestError):
    """Raised when a request exceeds the configured timeout."""


class ApiRetryError(ApiRequestError):
    """Raised when retry attempts are exhausted."""


class ApiValidationError(ApiError):
    """Raised when response validation fails."""
