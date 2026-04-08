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
@allure.title("API Case 16 - Validate products payload structure")
async def test_api_case_16_validate_products_payload_structure(api_client, test_record):
    scenarios = {
        "scenario_1": "Verify products list response contains top-level contract keys"
    }
    log_api_header(logger, "test_api_case_16_validate_products_payload_structure", scenarios)

    test_name = "test_api_case_16_validate_products_payload_structure"

    # ============================================================
    # SCENARIO 1: Verify products list response contains top-level contract keys
    # ============================================================
    with allure.step("Scenario 1: Validate products payload structure"):
        async def scenario():
            response = await api_client.get(PRODUCTS_LIST)
            body = response.body_json
            assert_api_field_equal(logger, field_name="response_code", actual=body.get("responseCode"), expected=200, response=response)
            assert_api_truthy(logger, field_name="has_products_key", actual="products" in body, response=response)
            assert_api_truthy(logger, field_name="products_is_list", actual=isinstance(body.get("products"), list), response=response)

        await run_api_scenario(logger, test_name, "scenario_1", scenario)


