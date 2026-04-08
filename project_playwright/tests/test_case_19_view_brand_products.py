import logging

import allure
import pytest

from pages.home_page import HomePage
from pages.products_page import ProductsPage
from utils.test_case_helpers import get_exception_line, log_test_header

TEST_DATA_FILE = "products/products.json"
logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.test_data(index=0)
@allure.feature("Products")
@allure.story("Brand Products")
@allure.title("View and verify brand products")
async def test_case_19_view_brand_products(page, env, test_record):
    scenarios = {
        "scenario_1": "Navigate to products page",
        "scenario_2": "Open first brand page",
        "scenario_3": "Open second brand page",
    }
    log_test_header(logger, "test_case_19_view_brand_products", scenarios)
    home_page = HomePage(page)
    products_page = ProductsPage(page)

    # ============================================================
    # SCENARIO 1: Navigate to products page
    # ============================================================
    with allure.step("Scenario 1: Navigate to products page"):
        try:
            await home_page.navigate(env["base_url"])
            await home_page.go_to_products()
            logger.info("Scenario 1 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 1 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_19_scenario_1.png")
            raise AssertionError(f"Scenario 1 failed: {e}") from e

    # ============================================================
    # SCENARIO 2: Open first brand page
    # ============================================================
    with allure.step("Scenario 2: Open first brand page"):
        try:
            await products_page.open_brand(test_record["brand_one"])
            assert test_record["brand_one"] in (await page.evaluate("document.body.innerText")).upper()
            logger.info("Scenario 2 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 2 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_19_scenario_2.png")
            raise AssertionError(f"Scenario 2 failed: {e}") from e

    # ============================================================
    # SCENARIO 3: Open second brand page
    # ============================================================
    with allure.step("Scenario 3: Open second brand page"):
        try:
            await home_page.go_to_products()
            await products_page.open_brand(test_record["brand_two"])
            assert "H&M" in await page.evaluate("document.body.innerText")
            logger.info("Scenario 3 passed")
        except Exception as e:
            line_num = get_exception_line()
            logger.error(f"Scenario 3 failed at line {line_num}: {e}")
            await page.screenshot(path="screenshots/case_19_scenario_3.png")
            raise AssertionError(f"Scenario 3 failed: {e}") from e


