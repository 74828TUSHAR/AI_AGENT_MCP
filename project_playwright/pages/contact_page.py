from pathlib import Path

from playwright.async_api import Page

from locators.contact.contact_locators import ContactLocators
from pages.base_page import BasePage


class ContactPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = ContactLocators()

    async def is_get_in_touch_visible(self) -> bool:
        return await self.is_visible(self.page.get_by_text(self.locators.GET_IN_TOUCH_TEXT))

    async def submit_contact_form(
        self, name: str, email: str, subject: str, message: str, upload_file: str | None = None
    ):
        await self.enter_text(self.page.get_by_test_id(self.locators.NAME_TEST_ID), name)
        await self.enter_text(self.page.get_by_test_id(self.locators.EMAIL_TEST_ID), email)
        await self.enter_text(self.page.get_by_test_id(self.locators.SUBJECT_TEST_ID), subject)
        await self.enter_text(self.page.get_by_test_id(self.locators.MESSAGE_TEST_ID), message)
        if upload_file:
            await self.upload_file(self.page.locator("input[type='file']"), str(Path(upload_file)))
        self.page.once("dialog", lambda dialog: dialog.accept())
        await self.click(self.page.get_by_test_id(self.locators.SUBMIT_BUTTON_TEST_ID))
        await self.wait_for_page_load_state("domcontentloaded")

    async def get_success_message(self) -> str:
        return await self.get_text(self.page.get_by_text(self.locators.SUCCESS_MESSAGE).first)

    async def click_home(self):
        await self.click(self.page.get_by_role("link", name=self.locators.HOME_LINK_NAME).last)
        await self.wait_for_page_load_state("domcontentloaded")
