# pages/login_page.py
from playwright.async_api import Page
from locators.login.login_locators import LoginLocators


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = LoginLocators()

    async def navigate(self, url: str):
        await self.page.goto(url)

    async def navigate_to_signup_login(self):
        element = self.page.get_by_role(
            self.locators.signup_login_role, name=self.locators.signup_login_name)
        if await element.is_visible():
            await element.click()

    async def login(self, username: str, password: str):
        await self.page.get_by_test_id(self.locators.login_email_testid).fill(username)
        await self.page.get_by_test_id(self.locators.login_password_testid).fill(password)
        await self.page.get_by_role(self.locators.login_button_role, name=self.locators.login_button_name).click()
        # Wait for page to load after button click
        await self.page.wait_for_load_state("domcontentloaded")

    async def is_logged_in(self) -> bool:
        return self.locators.logged_in_text in await self.page.evaluate("document.body.innerText")

    async def get_error_message(self) -> str:
        error_element = self.page.get_by_text(self.locators.error_message_text)
        return await error_element.inner_text()

    async def is_login_form_visible(self) -> bool:
        login_form_text = self.page.get_by_text(self.locators.login_form_heading)
        return await login_form_text.is_visible()

    async def logout(self):
        await self.page.get_by_role(
            self.locators.logout_button_role, name=self.locators.logout_button_name
        ).click()
        await self.page.wait_for_load_state("domcontentloaded")
