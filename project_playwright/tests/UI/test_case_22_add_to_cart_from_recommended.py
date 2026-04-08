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
@allure.story("Recommended Items")
@allure.title("Add to cart from recommended items")
async def test_case_22_add_to_cart_from_recommended(page, env, test_record):
    scenarios = {
        "scenario_1": "Navigate to homepage and verify recommended items section",
        "scenario_2": "Add recommended item to cart",
        "scenario_3": "Open cart and verify recommended item is present",
    }
    log_test_header(logger, "test_case_22_add_to_cart_from_recommended", scenarios)
    home_page = HomePage(page)
    products_page = ProductsPage(page)

    # ============================================================
    # SCENARIO 1: Navigate to homepage and verify recommended items section
    # ============================================================
    with allure.step("Scenario 1: Verify recommended items section"):
        try:
            await home_page.navigate(env["base_url"])
            assert await home_page.is_recommended_items_visible()
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_22_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Add recommended item to cart
    # ============================================================
    with allure.step("Scenario 2: Add recommended item to cart"):
        try:
            await home_page.add_recommended_item_to_cart()
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_22_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Open cart and verify recommended item is present
    # ============================================================
    with allure.step("Scenario 3: Verify recommended item in cart"):
        try:
            await products_page.view_cart_from_modal()
            cart_text = await page.evaluate("document.body.innerText")
            assert "Stylish Dress" in cart_text or "Winter Top" in cart_text or "Summer White Top" in cart_text
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_22_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e


