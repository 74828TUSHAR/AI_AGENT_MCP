import logging

import allure
import pytest

from pages.cart_page import CartPage
from pages.home_page import HomePage
from utils.test_case_helpers import get_exception_line, log_test_header

TEST_DATA_FILE = "common/common.json"
logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.test_data(index=0)
@allure.feature("Subscription")
@allure.story("Cart Page")
@allure.title("Verify subscription in cart page")
async def test_case_11_subscription_cart(page, env, test_record):
    scenarios = {
        "scenario_1": "Navigate to homepage and open cart page",
        "scenario_2": "Scroll to footer and verify subscription text",
        "scenario_3": "Subscribe from cart and verify success message",
    }
    log_test_header(logger, "test_case_11_subscription_cart", scenarios)
    home_page = HomePage(page)
    cart_page = CartPage(page)

    # ============================================================
    # SCENARIO 1: Navigate to homepage and open cart page
    # ============================================================
    with allure.step("Scenario 1: Open cart page"):
        try:
            await home_page.navigate(env["base_url"])
            await home_page.go_to_cart()
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_11_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Scroll to footer and verify subscription text
    # ============================================================
    with allure.step("Scenario 2: Verify cart subscription section"):
        try:
            await cart_page.scroll_to_footer()
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_11_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Subscribe from cart and verify success message
    # ============================================================
    with allure.step("Scenario 3: Subscribe from cart"):
        try:
            await cart_page.subscribe(test_record["subscription_email"])
            assert test_record["expected_subscription_message"] in await cart_page.get_subscription_success_message()
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_11_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e


