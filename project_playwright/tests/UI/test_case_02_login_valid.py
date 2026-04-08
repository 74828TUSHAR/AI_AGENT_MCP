import logging

import allure
import pytest

from pages.login_page import LoginPage
from utils.test_case_helpers import get_exception_line, log_test_header, mask_value

TEST_DATA_FILE = "login/login_valid.json"

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.test_data(index=0)
@allure.feature("Authentication")
@allure.story("Login Valid")
@allure.title("Login with valid credentials")
async def test_case_02_login_valid(page, env, test_record):
    scenarios = {
        "scenario_1": "Navigate to base URL and load homepage",
        "scenario_2": "Click Signup/Login link and navigate to login page",
        "scenario_3": "Enter valid email and password credentials",
        "scenario_4": "Click login button and submit form",
        "scenario_5": "Verify logged in message appears",
    }
    log_test_header(logger, "test_case_02_login_valid", scenarios)
    login_page = LoginPage(page)

    # ============================================================
    # SCENARIO 1: Navigate to base URL and load homepage
    # ============================================================
    with allure.step("Scenario 1: Navigate to base URL"):
        try:
            await login_page.navigate(env["base_url"])
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_02_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Click Signup/Login link and navigate to login page
    # ============================================================
    with allure.step("Scenario 2: Navigate to login page"):
        try:
            await login_page.navigate_to_signup_login()
            assert await login_page.is_login_form_visible()
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_02_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Enter valid email and password credentials
    # ============================================================
    with allure.step("Scenario 3: Enter valid credentials"):
        try:
            logger.info(f"Email: {mask_value(test_record['username'])}")
            logger.info(f"Password: {mask_value(test_record['password'])}")
            await login_page.login(test_record["username"], test_record["password"])
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_02_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e

    # ============================================================
    # SCENARIO 4: Click login button and submit form
    # ============================================================
    logger.info("Scenario 4 completed during login() method call")

    # ============================================================
    # SCENARIO 5: Verify logged in message appears
    # ============================================================
    with allure.step("Scenario 5: Verify login success"):
        try:
            assert await login_page.is_logged_in() == test_record["expect_logged_in"]
            logger.info("Scenario 5 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 5 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_02_scenario_5.png")
            raise AssertionError(f"Scenario 5 failed: {e}") from e


