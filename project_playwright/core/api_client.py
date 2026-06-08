from core.api_models import ApiResponse as ApiResult
from core.base_api import BaseAPI
from core.resources import CustomerAPI, OrderAPI, ProductAPI, UserAPI


class AutomationExerciseApiClient(BaseAPI):
    def __init__(self, request_context, **kwargs):
        super().__init__(request_context, **kwargs)
        self.users = UserAPI(
            request_context,
            base_url=self.base_url,
            auth_manager=self.auth_manager,
            default_headers=self.default_headers,
            timeout_ms=self.timeout_ms,
            max_retries=self.max_retries,
            retry_delay_ms=self.retry_delay_ms,
            retryable_statuses=self.retryable_statuses,
            log_response_body=self.log_response_body,
            attach_to_report=self.attach_to_report,
            logger=self.logger,
        )
        self.products = ProductAPI(
            request_context,
            base_url=self.base_url,
            auth_manager=self.auth_manager,
            default_headers=self.default_headers,
            timeout_ms=self.timeout_ms,
            max_retries=self.max_retries,
            retry_delay_ms=self.retry_delay_ms,
            retryable_statuses=self.retryable_statuses,
            log_response_body=self.log_response_body,
            attach_to_report=self.attach_to_report,
            logger=self.logger,
        )
        self.orders = OrderAPI(
            request_context,
            base_url=self.base_url,
            auth_manager=self.auth_manager,
            default_headers=self.default_headers,
            timeout_ms=self.timeout_ms,
            max_retries=self.max_retries,
            retry_delay_ms=self.retry_delay_ms,
            retryable_statuses=self.retryable_statuses,
            log_response_body=self.log_response_body,
            attach_to_report=self.attach_to_report,
            logger=self.logger,
        )
        self.customers = CustomerAPI(
            request_context,
            base_url=self.base_url,
            auth_manager=self.auth_manager,
            default_headers=self.default_headers,
            timeout_ms=self.timeout_ms,
            max_retries=self.max_retries,
            retry_delay_ms=self.retry_delay_ms,
            retryable_statuses=self.retryable_statuses,
            log_response_body=self.log_response_body,
            attach_to_report=self.attach_to_report,
            logger=self.logger,
        )
