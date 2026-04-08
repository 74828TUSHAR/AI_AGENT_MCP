import logging

import allure
import pytest

from constants.api_routes import *
from utils.api_assertions import assert_api_field_equal, assert_api_truthy
from utils.api_flows import create_user, delete_user, get_user_by_email, update_user
from utils.api_test_runner import log_api_header, run_api_scenario

TEST_DATA_FILE = "api/api_regression.json"

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.regression
@pytest.mark.test_data(index=0)
@allure.feature("API")
@allure.story("Verify Login API")
@allure.title("API Case 09 - DELETE to verify login is not supported")
async def test_api_case_09_verify_login_delete_not_supported(api_client, test_record):
    scenarios = {
        "scenario_1": "Send DELETE request to verify login API and verify method not supported response"
    }
    log_api_header(logger, "test_api_case_09_verify_login_delete_not_supported", scenarios)

    test_name = "test_api_case_09_verify_login_delete_not_supported"

    # ============================================================
    # SCENARIO 1: Send DELETE request to verify login API and verify method not supported response
    # ============================================================
    with allure.step("Scenario 1: DELETE verify login"):
        async def scenario():
            response = await api_client.delete(VERIFY_LOGIN)
            assert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=405, response=response)
            assert_api_field_equal(logger, field_name="message", actual=response.message, expected="This request method is not supported.", response=response)

        await run_api_scenario(logger, test_name, "scenario_1", scenario)


