from pathlib import Path

from playwright.async_api import Page

from locators.contact.contact_locators import ContactLocators


class ContactPage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = ContactLocators()

    async def is_get_in_touch_visible(self) -> bool:
        return await self.page.get_by_text(self.locators.GET_IN_TOUCH_TEXT).is_visible()

    async def submit_contact_form(
        self, name: str, email: str, subject: str, message: str, upload_file: str | None = None
    ):
        await self.page.get_by_test_id(self.locators.NAME_TEST_ID).fill(name)
        await self.page.get_by_test_id(self.locators.EMAIL_TEST_ID).fill(email)
        await self.page.get_by_test_id(self.locators.SUBJECT_TEST_ID).fill(subject)
        await self.page.get_by_test_id(self.locators.MESSAGE_TEST_ID).fill(message)
        if upload_file:
            await self.page.locator("input[type='file']").set_input_files(str(Path(upload_file)))
        self.page.once("dialog", lambda dialog: dialog.accept())
        await self.page.get_by_test_id(self.locators.SUBMIT_BUTTON_TEST_ID).click()
        await self.page.wait_for_load_state("domcontentloaded")

    async def get_success_message(self) -> str:
        return await self.page.get_by_text(self.locators.SUCCESS_MESSAGE).first.inner_text()

    async def click_home(self):
        await self.page.get_by_role("link", name=self.locators.HOME_LINK_NAME).last.click()
        await self.page.wait_for_load_state("domcontentloaded")
