from locators.registration.registration_locator import RegistrationLocator
from playwright.async_api import Page

from pages.base_page import BasePage


class RegistrationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = RegistrationLocator()

    async def navigate(self, url: str):
        await super().navigate(url)

    async def navigate_to_signup_login(self):
        await self.click(
            self.page.get_by_role(
                self.locators.SIGNUP_LOGIN_ROLE, name=self.locators.SIGNUP_LOGIN_NAME
            )
        )

    async def new_user_signup(self, username: str, useremail: str):
        await self.enter_text(self.page.get_by_test_id(self.locators.REGISTER_NAME_TEXTBOX), username)
        await self.enter_text(self.page.get_by_test_id(self.locators.REGISTER_EMAIL_TEXTBOX), useremail)
        await self.click(
            self.page.get_by_role(
                self.locators.SIGNUP_BUTTON_ROLE, name=self.locators.SIGNUP_BUTTON_NAME
            )
        )

    async def information_page_visible(self) -> bool:
        return await self.is_visible(self.page.get_by_text(self.locators.ENTER_ACCOUNT_INFORMATION_TEXT))

    async def enter_account_information(self, password: str, day: str, month: str, year: str):
        await self.check(self.page.get_by_label(self.locators.TITLE_NAME))
        await self.enter_text(self.page.get_by_test_id(self.locators.PASSWORD_TEXTBOX), password)
        await self.select_dropdown(self.page.get_by_role("combobox").nth(0), day)
        await self.select_dropdown(self.page.get_by_role("combobox").nth(1), month)
        await self.select_dropdown(self.page.get_by_role("combobox").nth(2), year)
        await self.check(self.page.get_by_label(self.locators.NEWSLETTER_CHECKBOX_LABEL))
        await self.check(self.page.get_by_label(self.locators.SPECIAL_OFFER_CHECKBOX_LABEL))

    async def enter_address_information(
        self,
        first_name: str,
        last_name: str,
        company: str,
        address: str,
        address_2: str,
        country: str,
        city: str,
        state: str,
        zipcode: int,
        mobile_number: int,
    ):
        await self.enter_text(self.page.get_by_test_id(self.locators.FIRST_NAME_TEXTBOX), first_name)
        await self.enter_text(self.page.get_by_test_id(self.locators.LAST_NAME_TEXTBOX), last_name)
        await self.enter_text(self.page.get_by_test_id(self.locators.COMPANY_TEXTBOX), company)
        await self.enter_text(self.page.get_by_test_id(self.locators.ADDRESS_TEXTBOX), address)
        await self.enter_text(self.page.get_by_test_id(self.locators.ADDRESS_2_TEXTBOX), address_2)
        await self.select_dropdown(self.page.get_by_role("combobox").nth(3), country)
        await self.enter_text(self.page.get_by_test_id(self.locators.STATE_TEXTBOX), state)
        await self.enter_text(self.page.get_by_test_id(self.locators.CITY_TEXTBOX), city)
        await self.enter_text(self.page.get_by_test_id(self.locators.ZIPCODE_TEXTBOX), str(zipcode))
        await self.enter_text(self.page.get_by_test_id(self.locators.MOBILE_NUMBER_TEXTBOX), str(mobile_number))
        await self.click(
            self.page.get_by_role(
                self.locators.CREATE_ACCOUNT_BUTTOM_ROLE,
                name=self.locators.CREATE_ACCOUNT_BUTTOM_NAME,
            )
        )
        await self.wait_for_page_load_state("domcontentloaded")

    async def account_created_text_visible(self) -> bool:
        return await self.is_visible(self.page.get_by_text(self.locators.ACCOUNT_CREATED_MESSAGE))

    async def click_on_continue_button(self):
        await self.click(
            self.page.get_by_role(
                self.locators.CONTINUE_BUTTON_ROLE, name=self.locators.CONTINUE_BUTTON_NAME
            )
        )
        await self.wait_for_page_load_state("domcontentloaded")

    async def is_logged_in(self) -> bool:
        return self.locators.LOG_IN_TEXT in await self.page.evaluate("document.body.innerText")

    async def delete_account_process(self):
        await self.click(
            self.page.get_by_role(
                self.locators.DELETE_ACCOUNT_ROLE, name=self.locators.DELETE_ACCOUNT_NAME
            )
        )
        await self.wait_for_page_load_state("domcontentloaded")

    async def account_deleted_text_visible(self) -> bool:
        return await self.is_visible(self.page.get_by_text(self.locators.ACCOUNT_DELETED_MESSAGE))

    async def click_delete_continue_button(self):
        await self.click(
            self.page.get_by_role(
                self.locators.DELETE_ACCOUNT_CONTINUE_BUTTON_ROLE,
                name=self.locators.DELETE_ACCOUNT_CONTINUE_BUTTON_NAME,
            )
        )
        await self.wait_for_page_load_state("domcontentloaded")

    async def signup_error_message(self) -> str:
        return await self.get_text(self.page.get_by_text(self.locators.SIGNUP_ERROR_MESSAGE))

    async def is_new_user_signup_visible(self) -> bool:
        return await self.is_visible(self.page.get_by_text(self.locators.NEW_USER_SIGNUP_TEXT))
