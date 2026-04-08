import logging
from pathlib import Path

import allure
import pytest

from pages.contact_page import ContactPage
from pages.home_page import HomePage
from utils.test_case_helpers import get_exception_line, log_test_header

TEST_DATA_FILE = "contact/contact.json"

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.test_data(index=0)
@allure.feature("Navigation")
@allure.story("Contact Us")
@allure.title("Submit contact us form")
async def test_case_06_contact_us_form(page, env, test_record):
    scenarios = {
        "scenario_1": "Navigate to base URL and open contact us page",
        "scenario_2": "Enter contact form details and submit",
        "scenario_3": "Verify success message and navigate back home",
    }
    log_test_header(logger, "test_case_06_contact_us_form", scenarios)
    home_page = HomePage(page)
    contact_page = ContactPage(page)
    upload_path = Path(test_record["upload_file"]).resolve()

    # ============================================================
    # SCENARIO 1: Navigate to base URL and open contact us page
    # ============================================================
    with allure.step("Scenario 1: Open contact us page"):
        try:
            await home_page.navigate(env["base_url"])
            await home_page.go_to_contact_us()
            assert await contact_page.is_get_in_touch_visible()
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_06_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Enter contact form details and submit
    # ============================================================
    with allure.step("Scenario 2: Submit contact form"):
        try:
            await contact_page.submit_contact_form(
                name=test_record["name"],
                email=test_record["email"],
                subject=test_record["subject"],
                message=test_record["message"],
                upload_file=str(upload_path),
            )
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_06_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Verify success message and navigate back home
    # ============================================================
    with allure.step("Scenario 3: Verify contact success"):
        try:
            assert test_record["expect_success_message"] in await contact_page.get_success_message()
            await contact_page.click_home()
            assert await home_page.is_home_page_visible()
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_06_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e


