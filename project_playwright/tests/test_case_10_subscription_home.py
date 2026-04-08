import logging

import allure
import pytest

from pages.home_page import HomePage
from utils.test_case_helpers import get_exception_line, log_test_header

TEST_DATA_FILE = "common/common.json"
logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.test_data(index=0)
@allure.feature("Subscription")
@allure.story("Home Page")
@allure.title("Verify subscription in home page")
async def test_case_10_subscription_home(page, env, test_record):
    scenarios = {
        "scenario_1": "Navigate to base URL and load homepage",
        "scenario_2": "Scroll to footer and verify subscription text",
        "scenario_3": "Subscribe with email and verify success message",
    }
    log_test_header(logger, "test_case_10_subscription_home", scenarios)
    home_page = HomePage(page)

    # ============================================================
    # SCENARIO 1: Navigate to base URL and load homepage
    # ============================================================
    with allure.step("Scenario 1: Navigate to homepage"):
        try:
            await home_page.navigate(env["base_url"])
            assert await home_page.is_home_page_visible()
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_10_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Scroll to footer and verify subscription text
    # ============================================================
    with allure.step("Scenario 2: Verify subscription section"):
        try:
            await home_page.scroll_to_footer()
            assert await home_page.is_subscription_visible()
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_10_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Subscribe with email and verify success message
    # ============================================================
    with allure.step("Scenario 3: Subscribe and verify success"):
        try:
            await home_page.subscribe(test_record["subscription_email"])
            assert test_record["expected_subscription_message"] in await home_page.get_subscription_success_message()
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_10_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e


