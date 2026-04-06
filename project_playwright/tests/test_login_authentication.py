import pytest
import logging
import allure
import inspect
import traceback
from pages.login_page import LoginPage

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
# TEST METHOD 1: LOGIN WITH VALID CREDENTIALS
# ============================================================================
@pytest.mark.asyncio
@allure.feature("Authentication")
@allure.story("User Login - Valid Credentials")
@allure.title("Login flow with valid credentials")
async def test_login_with_valid_credentials(page, env):
    """
    Test login functionality with VALID credentials

    Test Scenarios Description:
    ===========================
    1 - Navigate to base URL and load homepage
    2 - Click Signup/Login link and navigate to login page
    3 - Enter valid email and password credentials
    4 - Click login button and submit form
    5 - Verify 'Logged in as' message appears
    """

    TEST_SCENARIOS = {
        "scenario_1": "Navigate to base URL and load homepage",
        "scenario_2": "Click Signup/Login link and navigate to login page",
        "scenario_3": "Enter valid email and password credentials",
        "scenario_4": "Click login button and submit form",
        "scenario_5": "Verify 'Logged in as' message appears"
    }

    logger.info("\n" + "="*70)
    logger.info("TEST: test_login_with_valid_credentials")
    logger.info("Scenarios:")
    for scenario_id, description in TEST_SCENARIOS.items():
        logger.info(f"  {scenario_id.split('_')[1]} - {description}")
    logger.info("="*70 + "\n")

    login_page = LoginPage(page)

    # ============================================================
    # SCENARIO 1: Navigate to base URL and load homepage
    # ============================================================
    with allure.step("Scenario 1: Navigate to base URL"):
        try:
            logger.info("\n" + "="*70)
            logger.info("Scenario 1: Navigate to base URL and load homepage")
            logger.info(f"  URL: {env['base_url']}")
            logger.info("="*70)

            await login_page.navigate(env["base_url"])
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
    # SCENARIO 2: Click Signup/Login link and navigate to login page
    # ============================================================
    with allure.step("Scenario 2: Navigate to login page"):
        try:
            logger.info("\n" + "="*70)
            logger.info(
                "Scenario 2: Click Signup/Login link and navigate to login page")
            logger.info("="*70)

            await login_page.navigate_to_signup_login()
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
    # SCENARIO 3: Enter valid email and password credentials
    # ============================================================
    with allure.step("Scenario 3: Enter login credentials"):
        try:
            logger.info("\n" + "="*70)
            logger.info(
                "Scenario 3: Enter valid email and password credentials")
            logger.info(f"  Email: {'*' * len(env['username'])}")
            logger.info(f"  Password: {'*' * len(env['password'])}")
            logger.info("="*70)

            await login_page.login(env["username"], env["password"])
            logger.info(f"✓ Credentials entered successfully")
            logger.info(
                f"  Email field filled with: {'*' * len(env['username'])}")
            logger.info(f"  Password field filled")

        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"✗ FAILED at Scenario 3 (Line {line_num})")
            logger.error(f"  Error: {str(e)}")
            logger.error(f"  Could not fill login form")
            await page.screenshot(path="screenshots/FAILED_scenario_3_valid.png")
            raise AssertionError(f"Scenario 3 failed: {str(e)}") from e

    # ============================================================
    # SCENARIO 4: Click login button and submit form
    # ============================================================
    logger.info("\n" + "="*70)
    logger.info("Scenario 4: Click login button and submit form")
    logger.info("="*70)
    # Note: This happens in scenario 3 when login() is called
    logger.info(f"✓ Login button clicked and form submitted")
    logger.info(f"  Page is loading...")

    # ============================================================
    # SCENARIO 5: Verify 'Logged in as' message appears
    # ============================================================
    with allure.step("Scenario 5: Verify login success"):
        try:
            logger.info("\n" + "="*70)
            logger.info("Scenario 5: Verify 'Logged in as' message appears")
            logger.info("="*70)

            is_logged_in = await login_page.is_logged_in()

            if not is_logged_in:
                line_num = get_exception_line()
                logger.error(f"✗ FAILED at Scenario 5 (Line {line_num})")
                logger.error(
                    f"  Expected: 'Logged in as' message should be visible")
                logger.error(f"  Actual: Message not found on page")
                logger.error(f"  Current URL: {page.url}")
                page_content = await page.content()
                if "Logged in as" in page_content:
                    logger.error(
                        f"  Note: Text exists in HTML but not visible")
                else:
                    logger.error(f"  Note: Text does not exist in HTML at all")
                await page.screenshot(path="screenshots/FAILED_scenario_5_valid.png")
                raise AssertionError(
                    f"Login verification failed at Scenario 5 (Line {line_num})\n"
                    f"  Expected: 'Logged in as' message visible\n"
                    f"  Actual: Message not found\n"
                    f"  URL: {page.url}"
                )

            logger.info(f"✓ Login verification PASSED")
            logger.info(f"  'Logged in as' message found on page")
            logger.info(f"  Current URL: {page.url}")

        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"✗ FAILED at Scenario 5 (Line {line_num})")
            logger.error(f"  Error: {str(e)}")
            await page.screenshot(path="screenshots/FAILED_scenario_5_valid.png")
            raise

    logger.info("\n" + "="*70)
    logger.info("✓✓✓ TEST PASSED ✓✓✓")
    logger.info("All scenarios executed successfully - Valid credentials test")
    logger.info("="*70 + "\n")


# ============================================================================
# TEST METHOD 2: LOGIN WITH INVALID PASSWORD
# ============================================================================
@pytest.mark.asyncio
@allure.feature("Authentication")
@allure.story("User Login - Invalid Credentials")
@allure.title("Login with invalid password - should show error")
async def test_login_with_invalid_password(page, env):
    """
    Test login functionality with INVALID password

    Test Scenarios Description:
    ===========================
    1 - Navigate to base URL and load homepage
    2 - Click Signup/Login link and navigate to login page
    3 - Enter invalid password credentials
    4 - Click login button and submit form
    5 - Verify error message appears
    """

    TEST_SCENARIOS = {
        "scenario_1": "Navigate to base URL and load homepage",
        "scenario_2": "Click Signup/Login link and navigate to login page",
        "scenario_3": "Enter invalid password credentials",
        "scenario_4": "Click login button and submit form",
        "scenario_5": "Verify error message appears"
    }

    logger.info("\n" + "="*70)
    logger.info("TEST: test_login_with_invalid_password")
    logger.info("Scenarios:")
    for scenario_id, description in TEST_SCENARIOS.items():
        logger.info(f"  {scenario_id.split('_')[1]} - {description}")
    logger.info("="*70 + "\n")

    login_page = LoginPage(page)

    # ============================================================
    # SCENARIO 1: Navigate to base URL and load homepage
    # ============================================================
    with allure.step("Scenario 1: Navigate to base URL"):
        try:
            logger.info("\n" + "="*70)
            logger.info("Scenario 1: Navigate to base URL and load homepage")
            logger.info(f"  URL: {env['base_url']}")
            logger.info("="*70)

            await login_page.navigate(env["base_url"])
            page_title = await page.title()
            logger.info(f"✓ Homepage loaded successfully")
            logger.info(f"  Page Title: {page_title}")
            logger.info(f"  Current URL: {page.url}")

        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"✗ FAILED at Scenario 1 (Line {line_num})")
            logger.error(f"  Error: {str(e)}")
            logger.error(f"  Current URL: {page.url}")
            await page.screenshot(path="screenshots/FAILED_scenario_1_invalid.png")
            raise AssertionError(
                f"Scenario 1 failed at Line {line_num}: {str(e)}") from e

    # ============================================================
    # SCENARIO 2: Click Signup/Login link and navigate to login page
    # ============================================================
    with allure.step("Scenario 2: Navigate to login page"):
        try:
            logger.info("\n" + "="*70)
            logger.info(
                "Scenario 2: Click Signup/Login link and navigate to login page")
            logger.info("="*70)

            await login_page.navigate_to_signup_login()
            logger.info(f"✓ Successfully clicked Signup/Login link")
            logger.info(f"  Current URL: {page.url}")

        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"✗ FAILED at Scenario 2 (Line {line_num})")
            logger.error(f"  Error: {str(e)}")
            logger.error(f"  Current URL: {page.url}")
            await page.screenshot(path="screenshots/FAILED_scenario_2_invalid.png")
            raise AssertionError(
                f"Scenario 2 failed at Line {line_num}: {str(e)}") from e

    # ============================================================
    # SCENARIO 3: Enter INVALID password credentials
    # ============================================================
    with allure.step("Scenario 3: Enter login credentials"):
        try:
            logger.info("\n" + "="*70)
            logger.info("Scenario 3: Enter invalid password credentials")
            logger.info(f"  Email: {'*' * len(env['username'])}")
            logger.info(f"  Password: {'*' * 20} (intentional)")
            logger.info("="*70)

            # Using WRONG password intentionally
            await login_page.login(env["username"], "WRONG_PASSWORD_12345")
            logger.info(f"✓ Credentials entered")
            logger.info(
                f"  Email field filled with: {'*' * len(env['username'])}")
            logger.info(f"  Password field filled with: {'*' * 20}")

        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"✗ FAILED at Scenario 3 (Line {line_num})")
            logger.error(f"  Error: {str(e)}")
            await page.screenshot(path="screenshots/FAILED_scenario_3_invalid.png")
            raise AssertionError(
                f"Scenario 3 failed at Line {line_num}: {str(e)}") from e

    # ============================================================
    # SCENARIO 4: Click login button and submit form
    # ============================================================
    logger.info("\n" + "="*70)
    logger.info("Scenario 4: Click login button and submit form")
    logger.info("="*70)
    logger.info(f"✓ Login button clicked and form submitted")
    logger.info(f"  Waiting for page response...")

    # ============================================================
    # SCENARIO 5: Verify error message appears
    # ============================================================
    with allure.step("Scenario 5: Verify error message"):
        try:
            logger.info("\n" + "="*70)
            logger.info("Scenario 5: Verify error message appears")
            logger.info("="*70)

            error_message = await login_page.get_error_message()

            logger.info(f"✓ Error message captured")
            logger.info(f"  Expected: 'Your email or password is incorrect!'")
            logger.info(f"  Actual: '{error_message}'")
            logger.info(f"  Current URL: {page.url}")

            # Verify the error message
            assert "Your email or password is incorrect!" in error_message, \
                f"Expected error message not found. Got: {error_message}"

            logger.info(
                f"✓ Error message verified successfully (as expected for invalid password)")

        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"✗ FAILED at Scenario 5 (Line {line_num})")
            logger.error(f"  Error: {str(e)}")
            logger.error(
                f"  Expected: 'Your email or password is incorrect!' message")
            logger.error(f"  Current URL: {page.url}")
            page_content = await page.content()
            if "Your email or password is incorrect!" in page_content:
                logger.error(
                    f"  Note: Error message exists in HTML but assertion failed")
            else:
                logger.error(f"  Note: Error message NOT found in HTML")
            await page.screenshot(path="screenshots/FAILED_scenario_5_invalid.png")
            raise AssertionError(
                f"Scenario 5 failed at Line {line_num}: {str(e)}") from e

    logger.info("\n" + "="*70)
    logger.info("✓✓✓ TEST PASSED ✓✓✓")
    logger.info("Invalid password correctly showed error message")
    logger.info("="*70 + "\n")
