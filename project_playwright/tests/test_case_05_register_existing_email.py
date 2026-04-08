import logging

import allure
import pytest

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utils.test_case_helpers import get_exception_line, log_test_header

TEST_DATA_FILE = "login/login_valid.json"

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.test_data(index=0)
@allure.feature("Authentication")
@allure.story("Register Existing Email")
@allure.title("Register user with existing email")
async def test_case_05_register_existing_email(page, env, test_record):
    scenarios = {
        "scenario_1": "Navigate to base URL and open signup page",
        "scenario_2": "Enter existing email in signup form",
        "scenario_3": "Verify already exists error message",
    }
    log_test_header(logger, "test_case_05_register_existing_email", scenarios)
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    # ============================================================
    # SCENARIO 1: Navigate to base URL and open signup page
    # ============================================================
    with allure.step("Scenario 1: Open signup page"):
        try:
            await home_page.navigate(env["base_url"])
            await home_page.go_to_signup_login()
            assert await registration_page.is_new_user_signup_visible()
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_05_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Enter existing email in signup form
    # ============================================================
    with allure.step("Scenario 2: Enter existing email"):
        try:
            await registration_page.new_user_signup("Existing User", test_record["username"])
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_05_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Verify already exists error message
    # ============================================================
    with allure.step("Scenario 3: Verify already exists error"):
        try:
            assert "already exist" in (await registration_page.signup_error_message()).lower()
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_05_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e


