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
@allure.story("Category Products")
@allure.title("View category products")
async def test_case_18_view_category_products(page, env, test_record):
    scenarios = {
        "scenario_1": "Navigate to homepage and verify category area",
        "scenario_2": "Open women dress category page",
        "scenario_3": "Open men tshirts category page",
    }
    log_test_header(logger, "test_case_18_view_category_products", scenarios)
    home_page = HomePage(page)
    products_page = ProductsPage(page)

    # ============================================================
    # SCENARIO 1: Navigate to homepage and verify category area
    # ============================================================
    with allure.step("Scenario 1: Verify category area"):
        try:
            await home_page.navigate(env["base_url"])
            assert await home_page.is_home_page_visible()
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_18_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Open women dress category page
    # ============================================================
    with allure.step("Scenario 2: Open women dress page"):
        try:
            await products_page.open_category(test_record["women_category"], test_record["women_sub_category"])
            assert "WOMEN - DRESS PRODUCTS" in (await page.evaluate("document.body.innerText")).upper()
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_18_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Open men tshirts category page
    # ============================================================
    with allure.step("Scenario 3: Open men tshirts page"):
        try:
            await home_page.navigate(env["base_url"])
            await products_page.open_category(test_record["men_category"], test_record["men_sub_category"])
            assert "MEN - TSHIRTS PRODUCTS" in (await page.evaluate("document.body.innerText")).upper()
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_18_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e


