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
@allure.story("Add Products")
@allure.title("Add products in cart")
async def test_case_12_add_products_in_cart(page, env, test_record):
    scenarios = {
        "scenario_1": "Navigate to products page",
        "scenario_2": "Add first and second products to cart",
        "scenario_3": "Verify both products and cart details",
    }
    log_test_header(logger, "test_case_12_add_products_in_cart", scenarios)
    home_page = HomePage(page)
    products_page = ProductsPage(page)
    cart_page = CartPage(page)

    # ============================================================
    # SCENARIO 1: Navigate to products page
    # ============================================================
    with allure.step("Scenario 1: Navigate to products page"):
        try:
            await home_page.navigate(env["base_url"])
            await home_page.go_to_products()
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_12_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Add first and second products to cart
    # ============================================================
    with allure.step("Scenario 2: Add two products to cart"):
        try:
            await products_page.add_product_to_cart(0)
            await products_page.continue_shopping()
            await products_page.add_product_to_cart(2)
            await products_page.view_cart_from_modal()
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_12_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Verify both products and cart details
    # ============================================================
    with allure.step("Scenario 3: Verify cart details"):
        try:
            cart_text = await cart_page.cart_body_text()
            assert "Blue Top" in cart_text
            assert "Men Tshirt" in cart_text
            assert "Rs. 500" in cart_text
            assert "Rs. 400" in cart_text
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_12_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e


