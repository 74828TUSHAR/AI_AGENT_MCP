import logging

import allure
import pytest

from pages.home_page import HomePage
from pages.products_page import ProductsPage
from utils.test_case_helpers import get_exception_line, log_test_header

TEST_DATA_FILE = "products/products.json"
logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.test_data(index=0)
@allure.feature("Products")
@allure.story("Search Product")
@allure.title("Search product and verify searched results")
async def test_case_09_search_product(page, env, test_record):
    scenarios = {
        "scenario_1": "Navigate to products page",
        "scenario_2": "Enter product name in search input and search",
        "scenario_3": "Verify searched products are visible",
    }
    log_test_header(logger, "test_case_09_search_product", scenarios)
    home_page = HomePage(page)
    products_page = ProductsPage(page)

    # ============================================================
    # SCENARIO 1: Navigate to products page
    # ============================================================
    with allure.step("Scenario 1: Navigate to products page"):
        try:
            await home_page.navigate(env["base_url"])
            await home_page.go_to_products()
            assert await products_page.is_all_products_visible()
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_09_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Enter product name in search input and search
    # ============================================================
    with allure.step("Scenario 2: Search product"):
        try:
            await products_page.search_product(test_record["search_product"])
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_09_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Verify searched products are visible
    # ============================================================
    with allure.step("Scenario 3: Verify searched products"):
        try:
            assert await products_page.is_searched_products_visible()
            assert test_record["search_product"] in await products_page.search_results_text()
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_09_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e


