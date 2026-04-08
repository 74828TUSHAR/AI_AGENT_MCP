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
@allure.story("Address Details")
@allure.title("Verify address details in checkout page")
async def test_case_23_verify_address_details_checkout(page, env, test_record):
    scenarios = {
        "scenario_1": "Register user and login successfully",
        "scenario_2": "Add product to cart and proceed to checkout",
        "scenario_3": "Verify delivery and billing address details",
        "scenario_4": "Delete account and verify deletion message",
    }
    log_test_header(logger, "test_case_23_verify_address_details_checkout", scenarios)
    cart_page = CartPage(page)
    registration_page = RegistrationPage(page)

    # ============================================================
    # SCENARIO 1: Register user and login successfully
    # ============================================================
    with allure.step("Scenario 1: Register user"):
        try:
            await register_new_user(page, env, test_record)
            assert await registration_page.account_created_text_visible()
            await registration_page.click_on_continue_button()
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_23_scenario_1.png")
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
            await page.screenshot(path="screenshots/case_23_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Verify delivery and billing address details
    # ============================================================
    with allure.step("Scenario 3: Verify address details"):
        try:
            checkout_text = await CheckoutPage(page).body_text()
            assert test_record["address"] in checkout_text
            assert test_record["city"] in checkout_text
            assert test_record["state"] in checkout_text
            assert test_record["mobile_number"] in checkout_text
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_23_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e

    # ============================================================
    # SCENARIO 4: Delete account and verify deletion message
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
            await page.screenshot(path="screenshots/case_23_scenario_4.png")
            raise AssertionError(f"Scenario 4 failed: {e}") from e


