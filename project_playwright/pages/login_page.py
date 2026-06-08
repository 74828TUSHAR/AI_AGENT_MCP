from playwright.async_api import Page
from locators.login.login_locators import LoginLocators

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = LoginLocators()

    async def navigate(self, url: str):
        await super().navigate(url)

    async def navigate_to_signup_login(self):
        await self.click(
            self.page.get_by_role(
                self.locators.signup_login_role, name=self.locators.signup_login_name
            )
        )

    async def login(self, username: str, password: str):
        await self.enter_text(self.page.get_by_test_id(self.locators.login_email_testid), username)
        await self.enter_text(self.page.get_by_test_id(self.locators.login_password_testid), password)
        await self.click(
            self.page.get_by_role(self.locators.login_button_role, name=self.locators.login_button_name)
        )
        await self.wait_for_page_load_state("domcontentloaded")

    async def is_logged_in(self) -> bool:
        return self.locators.logged_in_text in await self.page.evaluate("document.body.innerText")

    async def get_error_message(self) -> str:
        return await self.get_text(self.page.get_by_text(self.locators.error_message_text))

    async def is_login_form_visible(self) -> bool:
        return await self.is_visible(self.page.get_by_text(self.locators.login_form_heading))

    async def logout(self):
        await self.click(
            self.page.get_by_role(
                self.locators.logout_button_role, name=self.locators.logout_button_name
            )
        )
        await self.wait_for_page_load_state("domcontentloaded")
