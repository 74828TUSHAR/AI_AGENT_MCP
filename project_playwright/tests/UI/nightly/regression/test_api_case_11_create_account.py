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
@allure.story("Account API")
@allure.title("API Case 11 - Create account")
async def test_api_case_11_create_account(api_client, test_record):
    scenarios = {
        "scenario_1": "Create a new account and verify successful account creation response",
        "scenario_2": "Delete created account as cleanup"
    }
    log_api_header(logger, "test_api_case_11_create_account", scenarios)

    test_name = "test_api_case_11_create_account"
    created_payload = {}

    # ============================================================
    # SCENARIO 1: Create a new account and verify successful account creation response
    # ============================================================
    with allure.step("Scenario 1: Create account"):
        async def scenario():
            nonlocal created_payload
            created_payload, response = await create_user(api_client, test_record["user_template"])
            assert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=201, response=response)
            assert_api_field_equal(logger, field_name="message", actual=response.message, expected="User created!", response=response)

        await run_api_scenario(logger, test_name, "scenario_1", scenario)

    # ============================================================
    # SCENARIO 2: Delete created account as cleanup
    # ============================================================
    with allure.step("Scenario 2: Cleanup created account"):
        async def scenario():
            response = await delete_user(api_client, created_payload["email"], created_payload["password"])
            assert_api_field_equal(logger, field_name="cleanup_response_code", actual=response.response_code, expected=200, response=response)

        await run_api_scenario(logger, test_name, "scenario_2", scenario)


