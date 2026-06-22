import inspect
import logging
import os
import re
from pathlib import Path

from playwright.async_api import Locator, Page

from utils.logger import get_execution_context, get_logger

DEFAULT_TIMEOUT = 120000  # 120s — accommodates slow ad-heavy pages like automationexercise.com


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = self._resolve_logger()
        self.screenshot_dir = Path(os.getenv("SCREENSHOT_DIR", "screenshots"))

    def _resolve_logger(self) -> logging.Logger:
        frame = inspect.currentframe()
        try:
            frame = frame.f_back
            while frame:
                module_name = frame.f_globals.get("__name__", "")
                file_name = frame.f_code.co_filename.replace("\\", "/")
                if "/tests/" in file_name or module_name.startswith("test_") or ".tests." in module_name:
                    return logging.getLogger(module_name)
                frame = frame.f_back
        finally:
            del frame

        return get_logger(self.__class__.__module__)

    def _resolve_locator(self, locator):
        if isinstance(locator, str):
            return self.page.locator(locator)
        return locator

    def _locator_label(self, locator, description: str | None = None) -> str:
        if description:
            return description
        if isinstance(locator, str):
            return locator
        return str(locator)

    def _sanitize(self, value: str) -> str:
        return re.sub(r"[^A-Za-z0-9_.-]+", "_", str(value)).strip("_") or "artifact"

    def _screenshot_name(self, action: str, locator_label: str | None = None) -> str:
        context = get_execution_context()
        parts = [
            context.get("test_name") or "test",
            self.__class__.__name__,
            action,
        ]
        if locator_label:
            parts.append(locator_label)

        safe_name = "_".join(self._sanitize(part) for part in parts if part)
        return f"{safe_name}.png"

    async def _capture_failure_screenshot(self, action: str, locator_label: str | None = None):
        if self.page.is_closed():
            self.logger.error("Screenshot skipped because the page is already closed")
            return None

        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = self.screenshot_dir / self._screenshot_name(action, locator_label)

        try:
            await self.page.screenshot(path=str(screenshot_path), full_page=True)
            self.logger.error("Failure screenshot saved to: %s", screenshot_path)
            return screenshot_path
        except Exception as exc:
            self.logger.error("Failed to capture screenshot for %s: %s", action, exc)
            return None

    async def _wait_for_locator(self, locator, *, state: str = "visible", timeout: int | None = None):
        target = self._resolve_locator(locator)
        await target.wait_for(state=state, timeout=timeout or DEFAULT_TIMEOUT)
        return target

    async def navigate(self, url: str, *, wait_until: str = "domcontentloaded"):
        self.logger.info("Navigating to url: %s", url)
        try:
            await self.page.goto(url, wait_until=wait_until, timeout=DEFAULT_TIMEOUT)
            self.logger.info("Successfully navigated to url: %s", url)
        except Exception as exc:
            self.logger.error("Failed navigating to url: %s | error=%s", url, exc)
            await self._capture_failure_screenshot("navigate", url)
            raise

    async def wait_for_page_load_state(self, state: str = "domcontentloaded"):
        self.logger.info("Waiting for page load state: %s", state)
        try:
            await self.page.wait_for_load_state(state)
            self.logger.info("Page load state reached: %s", state)
        except Exception as exc:
            self.logger.error("Failed waiting for page load state: %s | error=%s", state, exc)
            await self._capture_failure_screenshot("wait_for_page_load_state", state)
            raise

    async def wait_for_element(self, locator, *, state: str = "visible", timeout: int | None = None):
        label = self._locator_label(locator)
        self.logger.info("Waiting for locator: %s | state=%s", label, state)
        try:
            target = await self._wait_for_locator(locator, state=state, timeout=timeout or DEFAULT_TIMEOUT)
            self.logger.info("Locator is ready: %s", label)
            return target
        except Exception as exc:
            self.logger.error("Failed waiting for locator: %s | state=%s | error=%s", label, state, exc)
            await self._capture_failure_screenshot("wait_for_element", label)
            raise

    async def click(self, locator, *, force: bool = False, timeout: int | None = None):
        target = self._resolve_locator(locator)
        label = self._locator_label(locator)
        self.logger.info("Clicking on locator: %s", label)
        try:
            await target.wait_for(state="visible", timeout=timeout or DEFAULT_TIMEOUT)
            await target.click(force=force, timeout=timeout or DEFAULT_TIMEOUT)
            self.logger.info("Successfully clicked locator: %s", label)
        except Exception as exc:
            self.logger.error("Failed clicking locator: %s | error=%s", label, exc)
            await self._capture_failure_screenshot("click", label)
            raise

    async def enter_text(self, locator, text: str, *, timeout: int | None = None):
        target = self._resolve_locator(locator)
        label = self._locator_label(locator)
        self.logger.info("Entering text into locator: %s", label)
        try:
            await target.wait_for(state="visible", timeout=timeout or DEFAULT_TIMEOUT)
            await target.fill(text, timeout=timeout or DEFAULT_TIMEOUT)
            self.logger.info("Successfully entered text into locator: %s", label)
        except Exception as exc:
            self.logger.error("Failed entering text into locator: %s | error=%s", label, exc)
            await self._capture_failure_screenshot("enter_text", label)
            raise

    async def select_dropdown(self, locator, value: str, *, timeout: int | None = None):
        target = self._resolve_locator(locator)
        label = self._locator_label(locator)
        self.logger.info("Selecting dropdown value on locator: %s | value=%s", label, value)
        try:
            await target.wait_for(state="visible", timeout=timeout or DEFAULT_TIMEOUT)
            await target.select_option(value=value, timeout=timeout or DEFAULT_TIMEOUT)
            self.logger.info("Successfully selected dropdown value on locator: %s | value=%s", label, value)
        except Exception as exc:
            self.logger.error("Failed selecting dropdown value on locator: %s | value=%s | error=%s", label, value, exc)
            await self._capture_failure_screenshot("select_dropdown", label)
            raise

    async def get_text(self, locator, *, timeout: int | None = None) -> str:
        target = self._resolve_locator(locator)
        label = self._locator_label(locator)
        self.logger.info("Reading text from locator: %s", label)
        try:
            await target.wait_for(state="visible", timeout=timeout or DEFAULT_TIMEOUT)
            text = await target.inner_text(timeout=timeout or DEFAULT_TIMEOUT)
            self.logger.info("Successfully read text from locator: %s", label)
            return text
        except Exception as exc:
            self.logger.error("Failed reading text from locator: %s | error=%s", label, exc)
            await self._capture_failure_screenshot("get_text", label)
            raise

    async def is_visible(self, locator, *, timeout: int | None = None) -> bool:
        target = self._resolve_locator(locator)
        label = self._locator_label(locator)
        self.logger.info("Checking visibility for locator: %s", label)
        try:
            await target.wait_for(state="visible", timeout=timeout or DEFAULT_TIMEOUT)
            visible = await target.is_visible()
            self.logger.info("Visibility check completed for locator: %s | visible=%s", label, visible)
            return visible
        except Exception as exc:
            self.logger.error("Failed checking visibility for locator: %s | error=%s", label, exc)
            await self._capture_failure_screenshot("is_visible", label)
            raise

    async def scroll_to_element(self, locator, *, timeout: int | None = None):
        target = self._resolve_locator(locator)
        label = self._locator_label(locator)
        self.logger.info("Scrolling to locator: %s", label)
        try:
            await target.scroll_into_view_if_needed(timeout=timeout or DEFAULT_TIMEOUT)
            self.logger.info("Successfully scrolled to locator: %s", label)
        except Exception as exc:
            self.logger.error("Failed scrolling to locator: %s | error=%s", label, exc)
            await self._capture_failure_screenshot("scroll_to_element", label)
            raise

    async def upload_file(self, locator, file_path: str, *, timeout: int | None = None):
        target = self._resolve_locator(locator)
        label = self._locator_label(locator)
        resolved_path = str(Path(file_path))
        self.logger.info("Uploading file via locator: %s | file_path=%s", label, resolved_path)
        try:
            await target.wait_for(state="visible", timeout=timeout or DEFAULT_TIMEOUT)
            await target.set_input_files(resolved_path, timeout=timeout or DEFAULT_TIMEOUT)
            self.logger.info("Successfully uploaded file via locator: %s", label)
        except Exception as exc:
            self.logger.error("Failed uploading file via locator: %s | file_path=%s | error=%s", label, resolved_path, exc)
            await self._capture_failure_screenshot("upload_file", label)
            raise

    async def hover(self, locator, *, timeout: int | None = None):
        target = self._resolve_locator(locator)
        label = self._locator_label(locator)
        self.logger.info("Hovering over locator: %s", label)
        try:
            await target.wait_for(state="visible", timeout=timeout or DEFAULT_TIMEOUT)
            await target.hover(timeout=timeout or DEFAULT_TIMEOUT)
            self.logger.info("Successfully hovered over locator: %s", label)
        except Exception as exc:
            self.logger.error("Failed hovering over locator: %s | error=%s", label, exc)
            await self._capture_failure_screenshot("hover", label)
            raise

    async def check(self, locator, *, timeout: int | None = None):
        target = self._resolve_locator(locator)
        label = self._locator_label(locator)
        self.logger.info("Checking locator: %s", label)
        try:
            await target.wait_for(state="visible", timeout=timeout or DEFAULT_TIMEOUT)
            await target.check(timeout=timeout or DEFAULT_TIMEOUT)
            self.logger.info("Successfully checked locator: %s", label)
        except Exception as exc:
            self.logger.error("Failed checking locator: %s | error=%s", label, exc)
            await self._capture_failure_screenshot("check", label)
            raise

    async def press_key(self, key: str):
        self.logger.info("Pressing keyboard key: %s", key)
        try:
            await self.page.keyboard.press(key)
            self.logger.info("Successfully pressed keyboard key: %s", key)
        except Exception as exc:
            self.logger.error("Failed pressing keyboard key: %s | error=%s", key, exc)
            await self._capture_failure_screenshot("press_key", key)
            raise
