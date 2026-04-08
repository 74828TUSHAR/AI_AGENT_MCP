import logging

import allure
import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.test_case_helpers import get_exception_line, log_test_header

TEST_DATA_FILE = "login/login_valid.json"

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.test_data(index=0)
@allure.feature("Authentication")
@allure.story("Logout User")
@allure.title("Logout user after successful login")
async def test_case_04_logout_user(page, env, test_record):
    scenarios = {
        "scenario_1": "Navigate to base URL and open login page",
        "scenario_2": "Login with valid credentials",
        "scenario_3": "Logout from the application",
        "scenario_4": "Verify user is navigated back to login page",
    }
    log_test_header(logger, "test_case_04_logout_user", scenarios)
    home_page = HomePage(page)
    login_page = LoginPage(page)

    # ============================================================
    # SCENARIO 1: Navigate to base URL and open login page
    # ============================================================
    with allure.step("Scenario 1: Open login page"):
        try:
            await home_page.navigate(env["base_url"])
            await home_page.go_to_signup_login()
            assert await login_page.is_login_form_visible()
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_04_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Login with valid credentials
    # ============================================================
    with allure.step("Scenario 2: Login with valid credentials"):
        try:
            await login_page.login(test_record["username"], test_record["password"])
            assert await login_page.is_logged_in()
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_04_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Logout from the application
    # ============================================================
    with allure.step("Scenario 3: Logout from application"):
        try:
            await login_page.logout()
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_04_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e

    # ============================================================
    # SCENARIO 4: Verify user is navigated back to login page
    # ============================================================
    with allure.step("Scenario 4: Verify login page navigation"):
        try:
            assert "/login" in page.url
            logger.info("Scenario 4 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 4 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_04_scenario_4.png")
            raise AssertionError(f"Scenario 4 failed: {e}") from e


