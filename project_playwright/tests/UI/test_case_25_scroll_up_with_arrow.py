import logging

import allure
import pytest

from pages.home_page import HomePage
from utils.test_case_helpers import get_exception_line, log_test_header

TEST_DATA_FILE = "common/common.json"
logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.test_data(index=0)
@allure.feature("Scroll")
@allure.story("Arrow Scroll Up")
@allure.title("Verify scroll up using arrow button")
async def test_case_25_scroll_up_with_arrow(page, env, test_record):
    scenarios = {
        "scenario_1": "Navigate to homepage and scroll to footer",
        "scenario_2": "Verify subscription section at footer",
        "scenario_3": "Click arrow button and verify hero text at top",
    }
    log_test_header(logger, "test_case_25_scroll_up_with_arrow", scenarios)
    home_page = HomePage(page)

    # ============================================================
    # SCENARIO 1: Navigate to homepage and scroll to footer
    # ============================================================
    with allure.step("Scenario 1: Scroll to footer"):
        try:
            await home_page.navigate(env["base_url"])
            await home_page.scroll_to_footer()
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_25_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Verify subscription section at footer
    # ============================================================
    with allure.step("Scenario 2: Verify subscription at footer"):
        try:
            assert await home_page.is_subscription_visible()
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_25_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Click arrow button and verify hero text at top
    # ============================================================
    with allure.step("Scenario 3: Scroll to top using arrow"):
        try:
            await home_page.scroll_to_top_using_arrow()
            assert await home_page.hero_text_visible()
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_25_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e


