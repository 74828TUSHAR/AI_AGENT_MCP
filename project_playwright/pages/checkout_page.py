from pathlib import Path

from playwright.async_api import Download, Page

from locators.checkout.checkout_locators import CheckoutLocators
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = CheckoutLocators()

    async def body_text(self) -> str:
        return await self.page.evaluate("document.body.innerText")

    async def enter_comment(self, comment: str):
        await self.enter_text(self.page.get_by_role("textbox").last, comment)

    async def place_order(self):
        await self.click(self.page.get_by_text(self.locators.PLACE_ORDER_TEXT))
        await self.wait_for_page_load_state("domcontentloaded")

    async def fill_payment_details(
        self, name_on_card: str, card_number: str, cvc: str, expiry_month: str, expiry_year: str
    ):
        await self.enter_text(self.page.get_by_test_id(self.locators.NAME_ON_CARD_TEST_ID), name_on_card)
        await self.enter_text(self.page.get_by_test_id(self.locators.CARD_NUMBER_TEST_ID), card_number)
        await self.enter_text(self.page.get_by_test_id(self.locators.CVC_TEST_ID), cvc)
        await self.enter_text(self.page.get_by_test_id(self.locators.EXPIRY_MONTH_TEST_ID), expiry_month)
        await self.enter_text(self.page.get_by_test_id(self.locators.EXPIRY_YEAR_TEST_ID), expiry_year)

    async def pay_and_confirm_order(self):
        await self.click(self.page.get_by_text(self.locators.PAY_CONFIRM_TEXT))
        await self.wait_for_page_load_state("domcontentloaded")

    async def is_order_placed_visible(self) -> bool:
        return await self.is_visible(self.page.get_by_text(self.locators.ORDER_PLACED_TEXT))

    async def get_order_success_message(self) -> str:
        return await self.get_text(self.page.get_by_text(self.locators.ORDER_SUCCESS_TEXT))

    async def download_invoice(self, download_path: str) -> str:
        async with self.page.expect_download() as download_info:
            await self.click(self.page.get_by_text(self.locators.DOWNLOAD_INVOICE_TEXT))
        download: Download = await download_info.value
        target = Path(download_path)
        await download.save_as(str(target))
        return str(target)

    async def click_continue(self):
        await self.click(self.page.get_by_test_id("continue-button"))
        await self.wait_for_page_load_state("domcontentloaded")
