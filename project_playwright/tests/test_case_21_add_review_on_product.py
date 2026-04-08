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
@allure.story("Product Review")
@allure.title("Add review on product")
async def test_case_21_add_review_on_product(page, env, test_record):
    scenarios = {
        "scenario_1": "Navigate to products page and open first product",
        "scenario_2": "Enter review details and submit",
        "scenario_3": "Verify review success message",
    }
    log_test_header(logger, "test_case_21_add_review_on_product", scenarios)
    home_page = HomePage(page)
    products_page = ProductsPage(page)

    # ============================================================
    # SCENARIO 1: Navigate to products page and open first product
    # ============================================================
    with allure.step("Scenario 1: Open product detail page"):
        try:
            await home_page.navigate(env["base_url"])
            await home_page.go_to_products()
            await products_page.open_first_product_details()
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_21_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Enter review details and submit
    # ============================================================
    with allure.step("Scenario 2: Submit product review"):
        try:
            await products_page.add_review(
                test_record["review_name"],
                test_record["review_email"],
                test_record["review_text"],
            )
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_21_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Verify review success message
    # ============================================================
    with allure.step("Scenario 3: Verify review success"):
        try:
            assert test_record["expected_review_success"] in await products_page.get_review_success_message()
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_21_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e
