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
@allure.story("Products Contract")
@allure.title("API Case 17 - Validate first product item fields")
async def test_api_case_17_validate_product_item_fields(api_client, test_record):
    scenarios = {
        "scenario_1": "Verify first product item contains required product fields"
    }
    log_api_header(logger, "test_api_case_17_validate_product_item_fields", scenarios)

    test_name = "test_api_case_17_validate_product_item_fields"

    # ============================================================
    # SCENARIO 1: Verify first product item contains required product fields
    # ============================================================
    with allure.step("Scenario 1: Validate first product item"):
        async def scenario():
            response = await api_client.get(PRODUCTS_LIST)
            product = response.body_json.get("products", [])[0]
            for field_name in ["id", "name", "price", "brand", "category"]:
                assert_api_truthy(logger, field_name=f"first_product_{field_name}", actual=field_name in product, response=response)

        await run_api_scenario(logger, test_name, "scenario_1", scenario)


