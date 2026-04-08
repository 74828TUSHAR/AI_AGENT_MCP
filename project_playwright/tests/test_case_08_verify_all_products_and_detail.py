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
@allure.story("All Products")
@allure.title("Verify all products and product detail page")
async def test_case_08_verify_all_products_and_detail(page, env, test_record):
    scenarios = {
        "scenario_1": "Navigate to base URL and open products page",
        "scenario_2": "Verify all products list page is visible",
        "scenario_3": "Open first product details page",
        "scenario_4": "Verify product details are visible",
    }
    log_test_header(logger, "test_case_08_verify_all_products_and_detail", scenarios)
    home_page = HomePage(page)
    products_page = ProductsPage(page)

    # ============================================================
    # SCENARIO 1: Navigate to base URL and open products page
    # ============================================================
    with allure.step("Scenario 1: Open products page"):
        try:
            await home_page.navigate(env["base_url"])
            await home_page.go_to_products()
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_08_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Verify all products list page is visible
    # ============================================================
    with allure.step("Scenario 2: Verify products list page"):
        try:
            assert await products_page.is_all_products_visible()
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_08_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Open first product details page
    # ============================================================
    with allure.step("Scenario 3: Open first product details"):
        try:
            await products_page.open_first_product_details()
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_08_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e

    # ============================================================
    # SCENARIO 4: Verify product details are visible
    # ============================================================
    with allure.step("Scenario 4: Verify product details"):
        try:
            detail_text = await products_page.product_detail_text()
            assert test_record["expected_product_name"] in detail_text
            assert test_record["expected_category_text"] in detail_text
            assert test_record["expected_brand_text"] in detail_text
            assert "Availability:" in detail_text
            assert "Condition:" in detail_text
            logger.info("Scenario 4 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 4 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_08_scenario_4.png")
            raise AssertionError(f"Scenario 4 failed: {e}") from e


