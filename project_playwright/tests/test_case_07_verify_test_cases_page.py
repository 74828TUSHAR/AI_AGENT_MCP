import logging

import allure
import pytest

from pages.home_page import HomePage
from utils.test_case_helpers import get_exception_line, log_test_header

TEST_DATA_FILE = "contact/contact.json"

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.test_data(index=0)
@allure.feature("Navigation")
@allure.story("Test Cases")
@allure.title("Verify test cases page")
async def test_case_07_verify_test_cases_page(page, env, test_record):
    scenarios = {
        "scenario_1": "Navigate to base URL and load homepage",
        "scenario_2": "Click test cases link",
        "scenario_3": "Verify user is navigated to test cases page",
    }
    log_test_header(logger, "test_case_07_verify_test_cases_page", scenarios)
    home_page = HomePage(page)

    # ============================================================
    # SCENARIO 1: Navigate to base URL and load homepage
    # ============================================================
    with allure.step("Scenario 1: Navigate to base URL"):
        try:
            await home_page.navigate(env["base_url"])
            assert await home_page.is_home_page_visible()
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_07_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Click test cases link
    # ============================================================
    with allure.step("Scenario 2: Click test cases link"):
        try:
            await home_page.go_to_test_cases()
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_07_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Verify user is navigated to test cases page
    # ============================================================
    with allure.step("Scenario 3: Verify test cases page"):
        try:
            assert "/test_cases" in page.url
            assert "TEST CASES" in await page.evaluate("document.body.innerText")
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_07_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e
