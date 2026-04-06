# hooks/pytest_hooks.py
import pytest
import os
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.hookimpl(hookwrapper=True)
async def pytest_runtest_makereport(item, call):
    """
    Hook to take screenshot whenever a test fails.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        logger.error(f"Test Failed: {item.name}")

        page = item.funcargs.get("page", None)

        if page:
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)
            path = f"{screenshots_dir}/{item.name}.png"
            # <--- await is required
            await page.screenshot(path=path, full_page=True)
            logger.error(f"Screenshot saved: {path}")

        logger.error(f"Error:\n{report.longreprtext}")
