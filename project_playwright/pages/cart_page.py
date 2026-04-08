from playwright.async_api import Page

from locators.cart.cart_locators import CartLocators


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = CartLocators()

    async def cart_body_text(self) -> str:
        return await self.page.evaluate("document.body.innerText")

    async def proceed_to_checkout(self):
        await self.page.get_by_text(self.locators.PROCEED_TO_CHECKOUT_TEXT).click()
        await self.page.wait_for_load_state("domcontentloaded")

    async def click_register_login(self):
        await self.page.get_by_role("link", name=self.locators.REGISTER_LOGIN_LINK_NAME).click()
        await self.page.wait_for_load_state("domcontentloaded")

    async def remove_first_product(self):
        await self.page.locator("*").evaluate_all(
            """elements => {
                const deleteLink = elements.find(element =>
                    typeof element.className === 'string' && element.className.includes('cart_quantity_delete')
                );
                if (deleteLink) {
                    deleteLink.click();
                }
            }"""
        )
        await self.page.wait_for_timeout(1500)

    async def is_empty(self) -> bool:
        return await self.page.get_by_text(self.locators.CART_EMPTY_TEXT).is_visible()

    async def scroll_to_footer(self):
        await self.page.keyboard.press("End")
        await self.page.wait_for_timeout(500)

    async def subscribe(self, email: str):
        await self.scroll_to_footer()
        await self.page.get_by_placeholder(
            self.locators.SUBSCRIPTION_EMAIL_PLACEHOLDER
        ).fill(email)
        await self.page.get_by_role("button").last.click()

    async def get_subscription_success_message(self) -> str:
        return await self.page.get_by_text(
            self.locators.SUBSCRIPTION_SUCCESS_MESSAGE
        ).inner_text()
