# conftest.py
import pytest
import yaml
import logging
import os
from playwright.async_api import async_playwright


@pytest.fixture(scope="function")
async def page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        yield page
        await browser.close()


@pytest.fixture(scope="session")
def env():
    with open("config/env.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config["qa"]


def pytest_runtest_setup(item):
    """
    Configure test-specific logging before each test
    Creates separate log files for each test module
    Example: test_login_authentication.py -> logs/login_authentication_test.log
    """
    # Extract test module name (e.g., "test_login_authentication" -> "login_authentication")
    test_module_name = item.module.__name__.replace("tests.test_", "")

    # Create log file path
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    log_file = os.path.join(logs_dir, f"{test_module_name}_test.log")

    # Get the logger for this test module
    logger = logging.getLogger(item.module.__name__)
    logger.setLevel(logging.DEBUG)

    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create file handler with append mode
    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)8s] %(name)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(file_handler)

    # Also add console handler for INFO and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
