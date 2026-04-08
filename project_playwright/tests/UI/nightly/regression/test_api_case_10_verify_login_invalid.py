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
@allure.title("API Case 10 - Verify login with invalid details")
async def test_api_case_10_verify_login_invalid(api_client, test_record):
    scenarios = {
        "scenario_1": "Send POST request to verify login API with invalid email and password"
    }
    log_api_header(logger, "test_api_case_10_verify_login_invalid", scenarios)

    test_name = "test_api_case_10_verify_login_invalid"

    # ============================================================
    # SCENARIO 1: Send POST request to verify login API with invalid email and password
    # ============================================================
    with allure.step("Scenario 1: Verify invalid login"):
        async def scenario():
            response = await api_client.post(VERIFY_LOGIN, form={"email": test_record["invalid_login_email"], "password": test_record["invalid_login_password"]})
            assert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=404, response=response)
            assert_api_field_equal(logger, field_name="message", actual=response.message, expected="User not found!", response=response)

        await run_api_scenario(logger, test_name, "scenario_1", scenario)


