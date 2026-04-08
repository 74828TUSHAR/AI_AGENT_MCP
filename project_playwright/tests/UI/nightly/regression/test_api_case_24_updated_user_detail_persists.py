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
@allure.title("API Case 24 - Updated user details persist")
async def test_api_case_24_updated_user_detail_persists(api_client, test_record):
    scenarios = {
        "scenario_1": "Create a new account",
        "scenario_2": "Update created account",
        "scenario_3": "Get user details and verify updated fields",
        "scenario_4": "Delete updated account as cleanup"
    }
    log_api_header(logger, "test_api_case_24_updated_user_detail_persists", scenarios)

    test_name = "test_api_case_24_updated_user_detail_persists"
    created_payload = {}
    updated_payload = {}

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
    # SCENARIO 2: Update created account
    # ============================================================
    with allure.step("Scenario 2: Update account"):
        async def scenario():
            nonlocal updated_payload
            updated_payload, response = await update_user(api_client, created_payload, test_record["updated_user_template"])
            assert_api_field_equal(logger, field_name="update_response_code", actual=response.response_code, expected=200, response=response)

        await run_api_scenario(logger, test_name, "scenario_2", scenario)

    # ============================================================
    # SCENARIO 3: Get user details and verify updated fields
    # ============================================================
    with allure.step("Scenario 3: Verify updated fields"):
        async def scenario():
            response = await get_user_by_email(api_client, updated_payload["email"])
            user = response.body_json.get("user", {})
            assert_api_field_equal(logger, field_name="updated_name", actual=user.get("name"), expected=updated_payload["name"], response=response)
            assert_api_field_equal(logger, field_name="updated_city", actual=user.get("city"), expected=updated_payload["city"], response=response)

        await run_api_scenario(logger, test_name, "scenario_3", scenario)

    # ============================================================
    # SCENARIO 4: Delete updated account as cleanup
    # ============================================================
    with allure.step("Scenario 4: Cleanup updated account"):
        async def scenario():
            response = await delete_user(api_client, updated_payload["email"], updated_payload["password"])
            assert_api_field_equal(logger, field_name="cleanup_response_code", actual=response.response_code, expected=200, response=response)

        await run_api_scenario(logger, test_name, "scenario_4", scenario)


