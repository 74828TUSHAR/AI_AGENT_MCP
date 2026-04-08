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
@allure.story("Brands Contract")
@allure.title("API Case 19 - Validate first brand item fields")
async def test_api_case_19_validate_brand_item_fields(api_client, test_record):
    scenarios = {
        "scenario_1": "Verify first brand item contains required fields"
    }
    log_api_header(logger, "test_api_case_19_validate_brand_item_fields", scenarios)

    test_name = "test_api_case_19_validate_brand_item_fields"

    # ============================================================
    # SCENARIO 1: Verify first brand item contains required fields
    # ============================================================
    with allure.step("Scenario 1: Validate first brand item"):
        async def scenario():
            response = await api_client.get(BRANDS_LIST)
            brand = response.body_json.get("brands", [])[0]
            for field_name in ["id", "brand"]:
                assert_api_truthy(logger, field_name=f"first_brand_{field_name}", actual=field_name in brand, response=response)

        await run_api_scenario(logger, test_name, "scenario_1", scenario)


