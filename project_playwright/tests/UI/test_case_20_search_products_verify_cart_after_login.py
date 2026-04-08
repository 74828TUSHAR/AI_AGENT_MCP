import logging

import allure
import pytest

from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.test_case_helpers import get_exception_line, log_test_header

TEST_DATA_FILE = "products/products.json"
logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.test_data(index=0)
@allure.feature("Cart")
@allure.story("Search Products Cart Persistence")
@allure.title("Search products and verify cart after login")
async def test_case_20_search_products_verify_cart_after_login(page, env, test_record):
    scenarios = {
        "scenario_1": "Open products page and search product",
        "scenario_2": "Add searched product to cart and verify before login",
        "scenario_3": "Login and verify same product remains in cart",
    }
    log_test_header(logger, "test_case_20_search_products_verify_cart_after_login", scenarios)
    home_page = HomePage(page)
    products_page = ProductsPage(page)
    cart_page = CartPage(page)
    login_page = LoginPage(page)

    # ============================================================
    # SCENARIO 1: Open products page and search product
    # ============================================================
    with allure.step("Scenario 1: Search product"):
        try:
            await home_page.navigate(env["base_url"])
            await page.goto(f"{env['base_url']}products", wait_until="domcontentloaded")
            await products_page.search_product(test_record["search_product"])
            assert await products_page.is_searched_products_visible()
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_20_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Add searched product to cart and verify before login
    # ============================================================
    with allure.step("Scenario 2: Add searched product to cart"):
        try:
            await products_page.add_product_to_cart(0)
            await products_page.view_cart_from_modal()
            assert test_record["search_product"] in await cart_page.cart_body_text()
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_20_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Login and verify same product remains in cart
    # ============================================================
    with allure.step("Scenario 3: Login and verify cart persistence"):
        try:
            await home_page.go_to_signup_login()
            await login_page.login(env["username"], env["password"])
            await home_page.go_to_cart()
            assert test_record["search_product"] in await cart_page.cart_body_text()
            await cart_page.remove_first_product()
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_20_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e


