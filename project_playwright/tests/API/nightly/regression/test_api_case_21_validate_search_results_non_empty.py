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
@allure.story("Search Product Contract")
@allure.title("API Case 21 - Validate search results are non-empty")
async def test_api_case_21_validate_search_results_non_empty(api_client, test_record):
    scenarios = {
        "scenario_1": "Verify valid search term returns at least one product"
    }
    log_api_header(logger, "test_api_case_21_validate_search_results_non_empty", scenarios)

    test_name = "test_api_case_21_validate_search_results_non_empty"

    # ============================================================
    # SCENARIO 1: Verify valid search term returns at least one product
    # ============================================================
    with allure.step("Scenario 1: Validate search results are non-empty"):
        async def scenario():
            response = await api_client.post(SEARCH_PRODUCT, form={"search_product": test_record["search_product_secondary"]})
            products = response.body_json.get("products", [])
            assert_api_truthy(logger, field_name="non_empty_search_results", actual=len(products) > 0, response=response)

        await run_api_scenario(logger, test_name, "scenario_1", scenario)


