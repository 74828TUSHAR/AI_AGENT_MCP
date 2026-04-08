import logging

import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.registration_page import RegistrationPage
from utils.ecommerce_flows import add_first_product_to_cart, register_new_user
from utils.test_case_helpers import get_exception_line, log_test_header

TEST_DATA_FILE = "order/order.json"
logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.test_data(index=0)
@allure.feature("Checkout")
@allure.story("Register Before Checkout")
@allure.title("Place order after registering before checkout")
async def test_case_15_place_order_register_before_checkout(page, env, test_record):
    scenarios = {
        "scenario_1": "Register user before checkout",
        "scenario_2": "Add product to cart and proceed to checkout",
        "scenario_3": "Place order and verify confirmation",
        "scenario_4": "Delete account after order completion",
    }
    log_test_header(logger, "test_case_15_place_order_register_before_checkout", scenarios)
    cart_page = CartPage(page)
    registration_page = RegistrationPage(page)
    checkout_page = CheckoutPage(page)

    # ============================================================
    # SCENARIO 1: Register user before checkout
    # ============================================================
    with allure.step("Scenario 1: Register user"):
        try:
            await register_new_user(page, env, test_record)
            assert await registration_page.account_created_text_visible()
            await registration_page.click_on_continue_button()
            assert await registration_page.is_logged_in()
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_15_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Add product to cart and proceed to checkout
    # ============================================================
    with allure.step("Scenario 2: Add product and proceed to checkout"):
        try:
            await add_first_product_to_cart(page, env)
            await cart_page.proceed_to_checkout()
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_15_scenario_2.png")
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
            await page.screenshot(path="screenshots/case_15_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e

    # ============================================================
    # SCENARIO 4: Delete account after order completion
    # ============================================================
    with allure.step("Scenario 4: Delete account"):
        try:
            await registration_page.delete_account_process()
            assert await registration_page.account_deleted_text_visible()
            await registration_page.click_delete_continue_button()
            logger.info("Scenario 4 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 4 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_15_scenario_4.png")
            raise AssertionError(f"Scenario 4 failed: {e}") from e


