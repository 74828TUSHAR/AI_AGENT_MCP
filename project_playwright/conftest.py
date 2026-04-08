# conftest.py
import pytest
import yaml
import logging
import os
import re
import shutil
from functools import lru_cache
from pathlib import Path
from playwright.async_api import async_playwright
from utils.data_loader import load_json
from core.api_client import AutomationExerciseApiClient


def _get_int_env(name, default_value):
    value = os.getenv(name)
    return int(value) if value else default_value


def _get_window_settings(env):
    window_config = env.get("window", {})
    window_mode = os.getenv("WINDOW_MODE", window_config.get("mode", "maximized")).lower()
    width = _get_int_env("WINDOW_WIDTH", window_config.get("width", 1280))
    height = _get_int_env("WINDOW_HEIGHT", window_config.get("height", 720))
    return window_mode, width, height


async def _apply_window_state(page, window_mode, width, height, headless):
    if headless:
        return

    session = await page.context.new_cdp_session(page)
    window_info = await session.send("Browser.getWindowForTarget")

    if window_mode == "fullscreen":
        await session.send(
            "Browser.setWindowBounds",
            {
                "windowId": window_info["windowId"],
                "bounds": {"windowState": "fullscreen"},
            },
        )
        return

    if window_mode == "maximized":
        await session.send(
            "Browser.setWindowBounds",
            {
                "windowId": window_info["windowId"],
                "bounds": {"windowState": "maximized"},
            },
        )
        return

    if window_mode == "minimized":
        await session.send(
            "Browser.setWindowBounds",
            {
                "windowId": window_info["windowId"],
                "bounds": {"windowState": "minimized"},
            },
        )
        return

    await session.send(
        "Browser.setWindowBounds",
        {
            "windowId": window_info["windowId"],
            "bounds": {
                "left": 0,
                "top": 0,
                "width": width,
                "height": height,
                "windowState": "normal",
            },
        },
    )


@pytest.fixture(scope="function")
async def page(env, request):
    async with async_playwright() as p:
        p.selectors.set_test_id_attribute("data-qa")
        headless = os.getenv("HEADLESS", "false").lower() == "true"
        test_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", request.node.name)
        video_dir = Path("video")
        temp_video_dir = video_dir / "_temp" / test_name
        temp_video_dir.mkdir(parents=True, exist_ok=True)

        window_mode, width, height = _get_window_settings(env)

        args = []
        viewport = None

        # ===============================
        # WINDOW MODE HANDLING
        # ===============================
        if window_mode in ["maximized", "fullscreen"]:
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

        context = await browser.new_context(
            viewport=viewport,
            record_video_dir=str(temp_video_dir)
        )
        page = await context.new_page()

        await _apply_window_state(page, window_mode, width, height, headless)

        yield page

        await context.close()
        test_failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
        final_video_path = video_dir / f"{test_name}.webm"
        recorded_videos = list(temp_video_dir.glob("*.webm"))

        if test_failed and recorded_videos:
            video_dir.mkdir(exist_ok=True)
            if final_video_path.exists():
                final_video_path.unlink()
            shutil.move(str(recorded_videos[0]), str(final_video_path))

        if temp_video_dir.exists():
            shutil.rmtree(temp_video_dir, ignore_errors=True)

        temp_root = video_dir / "_temp"
        if temp_root.exists() and not any(temp_root.iterdir()):
            temp_root.rmdir()

        await browser.close()


@pytest.fixture(scope="session")
def env_name():
    return os.getenv("ENV", "qa")


@pytest.fixture(scope="session")
def env(env_name):
    with open("config/env.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config[env_name]


@pytest.fixture(scope="session")
def api_base_url(env):
    return env.get("api_base_url", env["base_url"])


@pytest.fixture(scope="function")
async def api_context(api_base_url):
    async with async_playwright() as p:
        request_context = await p.request.new_context(base_url=api_base_url)
        yield request_context
        await request_context.dispose()


@pytest.fixture(scope="function")
def api_client(api_context):
    return AutomationExerciseApiClient(api_context)


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
    # Extract a stable module name from the file name so nested folders stay readable.
    test_module_name = Path(str(item.fspath)).stem

    # Create log file path
    logs_dir = os.getenv("LOG_DIR", "logs")
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


def pytest_collection_modifyitems(items):
    """
    Auto-tag collected tests based on their folder so Jenkins can run UI and API
    suites separately without editing every individual test file.
    """
    for item in items:
        test_path = Path(str(item.fspath)).as_posix()
        if "/tests/UI/" in test_path:
            item.add_marker(pytest.mark.ui)
        elif "/tests/API/" in test_path:
            item.add_marker(pytest.mark.api)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
