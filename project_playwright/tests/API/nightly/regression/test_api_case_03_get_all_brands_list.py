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
@allure.story("Brands API")
@allure.title("API Case 03 - Get all brands list")
async def test_api_case_03_get_all_brands_list(api_client, test_record):
    scenarios = {
        "scenario_1": "Send GET request to brands list API and verify successful response"
    }
    log_api_header(logger, "test_api_case_03_get_all_brands_list", scenarios)

    test_name = "test_api_case_03_get_all_brands_list"

    # ============================================================
    # SCENARIO 1: Send GET request to brands list API and verify successful response
    # ============================================================
    with allure.step("Scenario 1: GET brands list"):
        async def scenario():
            response = await api_client.get(BRANDS_LIST)
            assert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=200, response=response)
            assert_api_truthy(logger, field_name="brands_list", actual=response.body_json.get("brands"), response=response)

        await run_api_scenario(logger, test_name, "scenario_1", scenario)


