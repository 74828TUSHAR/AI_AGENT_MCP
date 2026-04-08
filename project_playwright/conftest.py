# conftest.py
import pytest
import yaml
import logging
import os
from functools import lru_cache
from pathlib import Path
from playwright.async_api import async_playwright
from utils.data_loader import load_json


@pytest.fixture(scope="function")
async def page(env):
    async with async_playwright() as p:
        p.selectors.set_test_id_attribute("data-qa")
        headless = os.getenv("HEADLESS", "false").lower() == "true"

        window_mode = env.get("window", {}).get("mode", "custom")
        width = env.get("window", {}).get("width", 1280)
        height = env.get("window", {}).get("height", 720)

        args = []
        viewport = None

        # ===============================
        # WINDOW MODE HANDLING
        # ===============================
        if window_mode == "maximized":
            args.append("--start-maximized")
            viewport = None  # required

        elif window_mode == "minimized":
            args.append("--start-minimized")
            viewport = {"width": 300, "height": 200}  # fallback

        elif window_mode == "custom":
            viewport = {"width": width, "height": height}

        else:
            raise ValueError(f"Invalid window mode: {window_mode}")

        # ===============================
        # LAUNCH BROWSER
        # ===============================
        browser = await p.chromium.launch(
            headless=headless,
            args=args
        )

        context = await browser.new_context(viewport=viewport)
        page = await context.new_page()

        # ===============================
        # FORCE TRUE MAXIMIZE (IMPORTANT)
        # ===============================
        if window_mode == "maximized":
            dimensions = await page.evaluate("""
                () => ({
                    width: window.screen.width,
                    height: window.screen.height
                })
            """)

            await page.set_viewport_size({
                "width": dimensions["width"],
                "height": dimensions["height"]
            })

        yield page

        await browser.close()


@pytest.fixture(scope="session")
def env_name():
    return os.getenv("ENV", "qa")


@pytest.fixture(scope="session")
def env(env_name):
    with open("config/env.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config[env_name]


@lru_cache(maxsize=None)
def _load_test_data(env_name, relative_path):
    data_path = Path("test_data") / env_name / relative_path
    return load_json(str(data_path))


@pytest.fixture(scope="function")
def test_data(request, env_name):
    data_file = getattr(request.module, "TEST_DATA_FILE", None)
    if not data_file:
        raise ValueError(
            f"{request.module.__name__} must define TEST_DATA_FILE to use test_data fixture"
        )

    return _load_test_data(env_name, data_file)


@pytest.fixture(scope="function")
def test_record(request, test_data):
    marker = request.node.get_closest_marker("test_data")
    data_index = marker.kwargs.get("index", 0) if marker else getattr(
        request.module, "TEST_DATA_INDEX", 0
    )
    if isinstance(test_data, list):
        return test_data[data_index]
    return test_data


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
