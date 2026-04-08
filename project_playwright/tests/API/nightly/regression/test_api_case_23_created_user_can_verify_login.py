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
@allure.story("Account Lifecycle")
@allure.title("API Case 23 - Created user can verify login")
async def test_api_case_23_created_user_can_verify_login(api_client, test_record):
    scenarios = {
        "scenario_1": "Create a new account",
        "scenario_2": "Verify created user login through verify login API",
        "scenario_3": "Delete created account as cleanup"
    }
    log_api_header(logger, "test_api_case_23_created_user_can_verify_login", scenarios)

    test_name = "test_api_case_23_created_user_can_verify_login"
    created_payload = {}

    # ============================================================
    # SCENARIO 1: Create a new account
    # ============================================================
    with allure.step("Scenario 1: Create account"):
        async def scenario():
            nonlocal created_payload
            created_payload, response = await create_user(api_client, test_record["user_template"])
            assert_api_field_equal(logger, field_name="create_response_code", actual=response.response_code, expected=201, response=response)

        await run_api_scenario(logger, test_name, "scenario_1", scenario)

    # ============================================================
    # SCENARIO 2: Verify created user login through verify login API
    # ============================================================
    with allure.step("Scenario 2: Verify created user login"):
        async def scenario():
            response = await api_client.post(VERIFY_LOGIN, form={"email": created_payload["email"], "password": created_payload["password"]})
            assert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=200, response=response)
            assert_api_field_equal(logger, field_name="message", actual=response.message, expected="User exists!", response=response)

        await run_api_scenario(logger, test_name, "scenario_2", scenario)

    # ============================================================
    # SCENARIO 3: Delete created account as cleanup
    # ============================================================
    with allure.step("Scenario 3: Cleanup created account"):
        async def scenario():
            response = await delete_user(api_client, created_payload["email"], created_payload["password"])
            assert_api_field_equal(logger, field_name="cleanup_response_code", actual=response.response_code, expected=200, response=response)

        await run_api_scenario(logger, test_name, "scenario_3", scenario)


