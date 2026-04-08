from pathlib import Path

from playwright.async_api import Download, Page

from locators.checkout.checkout_locators import CheckoutLocators


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = CheckoutLocators()

    async def body_text(self) -> str:
        return await self.page.evaluate("document.body.innerText")

    async def enter_comment(self, comment: str):
        await self.page.get_by_role("textbox").last.fill(comment)

    async def place_order(self):
        await self.page.get_by_text(self.locators.PLACE_ORDER_TEXT).click()
        await self.page.wait_for_load_state("domcontentloaded")

    async def fill_payment_details(
        self, name_on_card: str, card_number: str, cvc: str, expiry_month: str, expiry_year: str
    ):
        await self.page.get_by_test_id(self.locators.NAME_ON_CARD_TEST_ID).fill(name_on_card)
        await self.page.get_by_test_id(self.locators.CARD_NUMBER_TEST_ID).fill(card_number)
        await self.page.get_by_test_id(self.locators.CVC_TEST_ID).fill(cvc)
        await self.page.get_by_test_id(self.locators.EXPIRY_MONTH_TEST_ID).fill(expiry_month)
        await self.page.get_by_test_id(self.locators.EXPIRY_YEAR_TEST_ID).fill(expiry_year)

    async def pay_and_confirm_order(self):
        await self.page.get_by_text(self.locators.PAY_CONFIRM_TEXT).click()
        await self.page.wait_for_load_state("domcontentloaded")

    async def is_order_placed_visible(self) -> bool:
        order_placed_text = self.page.get_by_text(self.locators.ORDER_PLACED_TEXT)
        await order_placed_text.wait_for(state="visible")
        return await order_placed_text.is_visible()

    async def get_order_success_message(self) -> str:
        success_text = self.page.get_by_text(self.locators.ORDER_SUCCESS_TEXT)
        await success_text.wait_for(state="visible")
        return await success_text.inner_text()

    async def download_invoice(self, download_path: str) -> str:
        async with self.page.expect_download() as download_info:
            await self.page.get_by_text(self.locators.DOWNLOAD_INVOICE_TEXT).click()
        download: Download = await download_info.value
        target = Path(download_path)
        await download.save_as(str(target))
        return str(target)

    async def click_continue(self):
        await self.page.get_by_test_id("continue-button").click()
        await self.page.wait_for_load_state("domcontentloaded")
