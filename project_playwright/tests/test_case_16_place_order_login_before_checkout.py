import logging

import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from utils.ecommerce_flows import add_first_product_to_cart, login_existing_user
from utils.test_case_helpers import get_exception_line, log_test_header

TEST_DATA_FILE = "order/order.json"
logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.test_data(index=0)
@allure.feature("Checkout")
@allure.story("Login Before Checkout")
@allure.title("Place order after login before checkout")
async def test_case_16_place_order_login_before_checkout(page, env, test_record):
    scenarios = {
        "scenario_1": "Login with existing user",
        "scenario_2": "Add product to cart and proceed to checkout",
        "scenario_3": "Place order and verify confirmation",
    }
    log_test_header(logger, "test_case_16_place_order_login_before_checkout", scenarios)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)
    login_page = LoginPage(page)

    # ============================================================
    # SCENARIO 1: Login with existing user
    # ============================================================
    with allure.step("Scenario 1: Login with existing user"):
        try:
            await login_existing_user(page, env)
            assert await login_page.is_logged_in()
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_16_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Add product to cart and proceed to checkout
    # ============================================================
    with allure.step("Scenario 2: Add product and checkout"):
        try:
            await add_first_product_to_cart(page, env)
            await cart_page.proceed_to_checkout()
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_16_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Place order and verify confirmation
    # ============================================================
    with allure.step("Scenario 3: Place order and verify confirmation"):
        try:
            await checkout_page.enter_comment(test_record["comment"])
            await checkout_page.place_order()
            await checkout_page.fill_payment_details(
                test_record["name_on_card"], test_record["card_number"], test_record["cvc"],
                test_record["expiry_month"], test_record["expiry_year"]
            )
            await checkout_page.pay_and_confirm_order()
            assert await checkout_page.is_order_placed_visible()
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_16_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e


