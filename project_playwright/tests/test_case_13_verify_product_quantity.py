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
@allure.story("Quantity")
@allure.title("Verify product quantity in cart")
async def test_case_13_verify_product_quantity(page, env, test_record):
    scenarios = {
        "scenario_1": "Navigate to homepage and open first product detail page",
        "scenario_2": "Increase quantity and add product to cart",
        "scenario_3": "Verify exact quantity in cart page",
    }
    log_test_header(logger, "test_case_13_verify_product_quantity", scenarios)
    home_page = HomePage(page)
    products_page = ProductsPage(page)
    cart_page = CartPage(page)

    # ============================================================
    # SCENARIO 1: Navigate to homepage and open first product detail page
    # ============================================================
    with allure.step("Scenario 1: Open first product details"):
        try:
            await home_page.navigate(env["base_url"])
            await products_page.open_first_product_details()
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_13_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Increase quantity and add product to cart
    # ============================================================
    with allure.step("Scenario 2: Add product with quantity four"):
        try:
            await products_page.set_product_quantity("4")
            await page.get_by_role("button", name="Add to cart").click()
            await products_page.view_cart_from_modal()
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_13_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Verify exact quantity in cart page
    # ============================================================
    with allure.step("Scenario 3: Verify quantity in cart"):
        try:
            assert "4" in await cart_page.cart_body_text()
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_13_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e


