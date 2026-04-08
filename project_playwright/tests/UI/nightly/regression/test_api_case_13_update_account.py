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
@allure.title("API Case 13 - Update account")
async def test_api_case_13_update_account(api_client, test_record):
    scenarios = {
        "scenario_1": "Create a new account for update validation",
        "scenario_2": "Update account and verify successful response",
        "scenario_3": "Delete updated account as cleanup"
    }
    log_api_header(logger, "test_api_case_13_update_account", scenarios)

    test_name = "test_api_case_13_update_account"
    created_payload = {}
    updated_payload = {}

    # ============================================================
    # SCENARIO 1: Create a new account for update validation
    # ============================================================
    with allure.step("Scenario 1: Create account for update"):
        async def scenario():
            nonlocal created_payload
            created_payload, response = await create_user(api_client, test_record["user_template"])
            assert_api_field_equal(logger, field_name="create_response_code", actual=response.response_code, expected=201, response=response)

        await run_api_scenario(logger, test_name, "scenario_1", scenario)

    # ============================================================
    # SCENARIO 2: Update account and verify successful response
    # ============================================================
    with allure.step("Scenario 2: Update account"):
        async def scenario():
            nonlocal updated_payload
            updated_payload, response = await update_user(api_client, created_payload, test_record["updated_user_template"])
            assert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=200, response=response)
            assert_api_field_equal(logger, field_name="message", actual=response.message, expected="User updated!", response=response)

        await run_api_scenario(logger, test_name, "scenario_2", scenario)

    # ============================================================
    # SCENARIO 3: Delete updated account as cleanup
    # ============================================================
    with allure.step("Scenario 3: Cleanup updated account"):
        async def scenario():
            response = await delete_user(api_client, updated_payload["email"], updated_payload["password"])
            assert_api_field_equal(logger, field_name="cleanup_response_code", actual=response.response_code, expected=200, response=response)

        await run_api_scenario(logger, test_name, "scenario_3", scenario)


