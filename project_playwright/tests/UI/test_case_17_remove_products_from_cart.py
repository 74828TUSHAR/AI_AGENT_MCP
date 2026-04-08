import logging

import allure
import pytest

from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.products_page import ProductsPage
from utils.test_case_helpers import get_exception_line, log_test_header

TEST_DATA_FILE = "products/products.json"
logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.test_data(index=0)
@allure.feature("Cart")
@allure.story("Remove Product")
@allure.title("Remove products from cart")
async def test_case_17_remove_products_from_cart(page, env, test_record):
    scenarios = {
        "scenario_1": "Navigate to products page and add product to cart",
        "scenario_2": "Open cart page",
        "scenario_3": "Remove product and verify cart is empty",
    }
    log_test_header(logger, "test_case_17_remove_products_from_cart", scenarios)
    home_page = HomePage(page)
    products_page = ProductsPage(page)
    cart_page = CartPage(page)

    # ============================================================
    # SCENARIO 1: Navigate to products page and add product to cart
    # ============================================================
    with allure.step("Scenario 1: Add product to cart"):
        try:
            await home_page.navigate(env["base_url"])
            await home_page.go_to_products()
            await products_page.add_product_to_cart(0)
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_17_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Open cart page
    # ============================================================
    with allure.step("Scenario 2: Open cart page"):
        try:
            await products_page.view_cart_from_modal()
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_17_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Remove product and verify cart is empty
    # ============================================================
    with allure.step("Scenario 3: Remove product and verify empty cart"):
        try:
            await cart_page.remove_first_product()
            assert await cart_page.is_empty()
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_17_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e


