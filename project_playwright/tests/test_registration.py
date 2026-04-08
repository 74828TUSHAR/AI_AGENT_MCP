import pytest
import logging
import allure
import inspect
import traceback
from pages.registration_page import RegistrationPage

# Configure logger for detailed output
logger = logging.getLogger(__name__)

# Helper function to get current line number


def get_line_number():
    """Get the current line number in the code"""
    return inspect.currentframe().f_back.f_lineno

# Helper function to get exception line number


def get_exception_line():
    """Get the line number where exception occurred"""
    return traceback.extract_tb(traceback.sys.exc_info()[2])[-1].lineno
 
# ============================================================================
# TEST METHOD 1: Sigh-up WITH VALID CREDENTIALS
# ============================================================================


@pytest.mark.asyncio
@allure.feature("Authentication")
@allure.story("User Signup - Valid Credentials")
@allure.title("Signup flow with valid credentials")
async def test_signup_with_valid_credentials(page,env):
    """
    Test Sign-Up functionality with VALID credentials

    Test Scenarios Description:
    ===========================
    1 - Navigate to base URL and load homepage
    2 - Click Signup/Login link and navigate to login page
    3 - Enter valid Name and Email credentials
    4 - Click Signup button and submit form
    5 - Verify 'Enter Account Informatino' text appears

    """
    TEST_SCENARIOS = {
        "scenario_1": "Navigate to base URL and load homepage",
        "scenario_2": "Click Signup/Login link and navigate to login page",
        "scenario_3": "Enter valid Name and Email credentials",
        "scenario_4": "Click Signup button and submit form",
        "scenario_5": "Verify 'Enter Account Informatino' text appears"
    }

    logger.info("\n" + "="*70)
    logger.info("Test: test_signup_with_valid_credentials")
    logger.info("Scenarios:")
    for scenario_id, description in TEST_SCENARIOS.items():
        logger.info(f"  {scenario_id.split('_')[1]} - {description}")
    logger.info("="*70 + "\n")

    register_page = RegistrationPage(page)

    with allure.step("Scenario 1: Navigate to base URL"):
        try:
            logger.info("\n" + "="*70)
            logger.info("Scenario 1: Navigate to base URL and load homepage")
            logger.info(f"  URL: {env['base_url']}")
            logger.info("="*70)

            await register_page.navigate(env["base_url"])
            page_title = await page.title()
            logger.info(f"✓ Homepage loaded successfully")
            logger.info(f"  Page Title: {page_title}")
            logger.info(f"  Current URL: {page.url}")

        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"✗ FAILED at Scenario 1 (Line {line_num})")
            logger.error(f"  Error: {str(e)}")
            logger.error(f"  Current URL: {page.url}")
            logger.error(f"  Page Title: {await page.title()}")
            await page.screenshot(path="screenshots/FAILED_scenario_1_valid.png")
            raise AssertionError(f"Scenario 1 failed: {str(e)}") from e

    # ============================================================
    # SCENARIO 2: Click Signup/Login link and navigate to Sign-up/Login page
    # ============================================================
    with allure.step("Scenario 2: Navigate to Sign-up page"):
        try:
            logger.info("\n" + "="*70)
            logger.info(
                "Scenario 2: Click Signup/Login link and navigate to Signup page")
            logger.info("="*70)

            await register_page.navigate_to_signup_login()
            logger.info(f"✓ Successfully clicked Signup/Login link")
            logger.info(f"  Current URL: {page.url}")

        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"✗ FAILED at Scenario 2 (Line {line_num})")
            logger.error(f"  Error: {str(e)}")
            logger.error(f"  Current URL: {page.url}")
            await page.screenshot(path="screenshots/FAILED_scenario_2_valid.png")
            raise AssertionError(
                f"Scenario 2 failed at Line {line_num}: {str(e)}") from e

    # ============================================================
    # SCENARIO 3: Enter valid Name and Email credentials
    # ============================================================
    with allure.step("Scenario 3: Enter SignUp credentials"):
        try:
            logger.info("\n" + "="*70)
            logger.info(
                "Scenario 3: Enter valid Name and Email credentials")
            logger.info(f"  Email: {'*' * len(env['username'])}")
            logger.info(f"  Password: {'*' * len(env['email'])}")
            logger.info("="*70)

            await register_page.new_user_signup(env["username"], env["email"])
            logger.info(f"✓ Credentials entered successfully")
            logger.info(
                f"  Name field filled with: {'*' * len(env['username'])}")
            logger.info(f"  Password field filled")

        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"✗ FAILED at Scenario 3 (Line {line_num})")
            logger.error(f"  Error: {str(e)}")
            logger.error(f"  Could not fill signup form")
            await page.screenshot(path="screenshots/FAILED_scenario_3_valid.png")
            raise AssertionError(f"Scenario 3 failed: {str(e)}") from e
