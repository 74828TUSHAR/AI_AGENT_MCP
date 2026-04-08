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
@allure.story("Search Product API")
@allure.title("API Case 06 - Search product without parameter")
async def test_api_case_06_search_product_without_parameter(api_client, test_record):
    scenarios = {
        "scenario_1": "Send POST request to search product API without parameter and verify bad request response"
    }
    log_api_header(logger, "test_api_case_06_search_product_without_parameter", scenarios)

    test_name = "test_api_case_06_search_product_without_parameter"

    # ============================================================
    # SCENARIO 1: Send POST request to search product API without parameter and verify bad request response
    # ============================================================
    with allure.step("Scenario 1: Search product without parameter"):
        async def scenario():
            response = await api_client.post(SEARCH_PRODUCT)
            assert_api_field_equal(logger, field_name="response_code", actual=response.response_code, expected=400, response=response)
            assert_api_field_equal(logger, field_name="message", actual=response.message, expected="Bad request, search_product parameter is missing in POST request.", response=response)

        await run_api_scenario(logger, test_name, "scenario_1", scenario)


