import logging

import allure
import pytest

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utils.test_case_helpers import get_exception_line, log_test_header, mask_value
from utils.test_data_factory import build_unique_email

TEST_DATA_FILE = "registration/registration.json"

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.test_data(index=0)
@allure.feature("Authentication")
@allure.story("Register User")
@allure.title("Register user successfully")
async def test_case_01_register_user(page, env, test_record):
    test_scenarios = {
        "scenario_1": "Navigate to base URL and load homepage",
        "scenario_2": "Click Signup/Login link and navigate to signup page",
        "scenario_3": "Enter valid signup name and email",
        "scenario_4": "Enter account and address information",
        "scenario_5": "Verify account created and logged in state",
        "scenario_6": "Delete account and verify deletion message",
    }
    log_test_header(logger, "test_case_01_register_user", test_scenarios)

    home_page = HomePage(page)
    registration_page = RegistrationPage(page)
    email = build_unique_email(test_record["email_template"])

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
            await page.screenshot(path="screenshots/case_01_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Click Signup/Login link and navigate to signup page
    # ============================================================
    with allure.step("Scenario 2: Navigate to signup page"):
        try:
            await home_page.go_to_signup_login()
            assert await registration_page.is_new_user_signup_visible()
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_01_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Enter valid signup name and email
    # ============================================================
    with allure.step("Scenario 3: Enter signup name and email"):
        try:
            logger.info(f"Name: {mask_value(test_record['name'])}")
            logger.info(f"Email: {mask_value(email)}")
            await registration_page.new_user_signup(test_record["name"], email)
            assert await registration_page.information_page_visible()
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_01_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e

    # ============================================================
    # SCENARIO 4: Enter account and address information
    # ============================================================
    with allure.step("Scenario 4: Enter account and address information"):
        try:
            await registration_page.enter_account_information(
                password=test_record["password"],
                day=test_record["day"],
                month=test_record["month"],
                year=test_record["year"],
            )
            await registration_page.enter_address_information(
                first_name=test_record["first_name"],
                last_name=test_record["last_name"],
                company=test_record["company"],
                address=test_record["address"],
                address_2=test_record["address_2"],
                country=test_record["country"],
                city=test_record["city"],
                state=test_record["state"],
                zipcode=test_record["zipcode"],
                mobile_number=test_record["mobile_number"],
            )
            logger.info("Scenario 4 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 4 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_01_scenario_4.png")
            raise AssertionError(f"Scenario 4 failed: {e}") from e

    # ============================================================
    # SCENARIO 5: Verify account created and logged in state
    # ============================================================
    with allure.step("Scenario 5: Verify account created and logged in state"):
        try:
            assert await registration_page.account_created_text_visible()
            await registration_page.click_on_continue_button()
            assert await registration_page.is_logged_in()
            logger.info("Scenario 5 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 5 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_01_scenario_5.png")
            raise AssertionError(f"Scenario 5 failed: {e}") from e

    # ============================================================
    # SCENARIO 6: Delete account and verify deletion message
    # ============================================================
    with allure.step("Scenario 6: Delete account and verify deletion message"):
        try:
            await registration_page.delete_account_process()
            assert await registration_page.account_deleted_text_visible()
            await registration_page.click_delete_continue_button()
            logger.info("Scenario 6 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 6 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_01_scenario_6.png")
            raise AssertionError(f"Scenario 6 failed: {e}") from e


    


