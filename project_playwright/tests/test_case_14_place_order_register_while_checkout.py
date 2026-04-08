import logging

import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utils.ecommerce_flows import add_first_product_to_cart
from utils.test_case_helpers import get_exception_line, log_test_header
from utils.test_data_factory import build_unique_email

TEST_DATA_FILE = "order/order.json"
logger = logging.getLogger(__name__)


async def _complete_payment(page, record):
    checkout_page = CheckoutPage(page)
    await checkout_page.enter_comment(record["comment"])
    await checkout_page.place_order()
    await checkout_page.fill_payment_details(
        record["name_on_card"],
        record["card_number"],
        record["cvc"],
        record["expiry_month"],
        record["expiry_year"],
    )
    await checkout_page.pay_and_confirm_order()
    return checkout_page


@pytest.mark.asyncio
@pytest.mark.test_data(index=0)
@allure.feature("Checkout")
@allure.story("Register While Checkout")
@allure.title("Place order while registering at checkout")
async def test_case_14_place_order_register_while_checkout(page, env, test_record):
    scenarios = {
        "scenario_1": "Add product to cart and proceed to checkout",
        "scenario_2": "Register new user from checkout flow",
        "scenario_3": "Place order and verify confirmation",
        "scenario_4": "Delete account after order completion",
    }
    log_test_header(logger, "test_case_14_place_order_register_while_checkout", scenarios)
    home_page = HomePage(page)
    cart_page = CartPage(page)
    registration_page = RegistrationPage(page)

    # ============================================================
    # SCENARIO 1: Add product to cart and proceed to checkout
    # ============================================================
    with allure.step("Scenario 1: Add product and proceed to checkout"):
        try:
            await add_first_product_to_cart(page, env)
            await cart_page.proceed_to_checkout()
            await cart_page.click_register_login()
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_14_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Register new user from checkout flow
    # ============================================================
    with allure.step("Scenario 2: Register new user from checkout"):
        try:
            email = build_unique_email(test_record["email_template"])
            await registration_page.new_user_signup(test_record["name"], email)
            await registration_page.enter_account_information(
                test_record["password"], test_record["day"], test_record["month"], test_record["year"]
            )
            await registration_page.enter_address_information(
                test_record["first_name"], test_record["last_name"], test_record["company"],
                test_record["address"], test_record["address_2"], test_record["country"],
                test_record["city"], test_record["state"], test_record["zipcode"],
                test_record["mobile_number"]
            )
            assert await registration_page.account_created_text_visible()
            await registration_page.click_on_continue_button()
            assert await registration_page.is_logged_in()
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_14_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Place order and verify confirmation
    # ============================================================
    with allure.step("Scenario 3: Place order and verify confirmation"):
        try:
            await home_page.go_to_cart()
            await cart_page.proceed_to_checkout()
            checkout_page = await _complete_payment(page, test_record)
            assert await checkout_page.is_order_placed_visible()
            assert test_record["expected_order_message"] in await checkout_page.get_order_success_message()
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_14_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e

    # ============================================================
    # SCENARIO 4: Delete account after order completion
    # ============================================================
    with allure.step("Scenario 4: Delete account after order"):
        try:
            await registration_page.delete_account_process()
            assert await registration_page.account_deleted_text_visible()
            await registration_page.click_delete_continue_button()
            logger.info("Scenario 4 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 4 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_14_scenario_4.png")
            raise AssertionError(f"Scenario 4 failed: {e}") from e
