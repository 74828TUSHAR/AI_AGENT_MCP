from locators.home.home_locators import HomeLocators
from playwright.async_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = HomeLocators()

    async def navigate(self, url: str):
        await super().navigate(url)

    async def is_home_page_visible(self) -> bool:
        hero = self.page.get_by_role("heading", name="Full-Fledged practice website").first
        return await self.is_visible(hero)

    async def go_to_products(self):
        await self.click(
            self.page.get_by_role(
                self.locators.HOME_LINK_ROLE, name=self.locators.PRODUCTS_LINK_NAME
            ).first
        )
        await self.wait_for_page_load_state("domcontentloaded")

    async def go_to_cart(self):
        await self.click(
            self.page.get_by_role(
                self.locators.HOME_LINK_ROLE, name=self.locators.CART_LINK_NAME
            ).first
        )
        await self.wait_for_page_load_state("domcontentloaded")

    async def go_to_signup_login(self):
        await self.click(
            self.page.get_by_role(
                self.locators.HOME_LINK_ROLE, name=self.locators.SIGNUP_LOGIN_LINK_NAME
            ).first
        )
        await self.wait_for_page_load_state("domcontentloaded")

    async def go_to_test_cases(self):
        await self.click(
            self.page.get_by_role(
                self.locators.HOME_LINK_ROLE, name=self.locators.TEST_CASES_LINK_NAME
            ).first
        )
        await self.wait_for_page_load_state("domcontentloaded")

    async def go_to_contact_us(self):
        await self.click(
            self.page.get_by_role(
                self.locators.HOME_LINK_ROLE, name=self.locators.CONTACT_US_LINK_NAME
            )
        )
        await self.wait_for_page_load_state("domcontentloaded")

    async def scroll_to_footer(self):
        await self.press_key("End")
        await self.page.wait_for_timeout(500)

    async def is_subscription_visible(self) -> bool:
        return await self.is_visible(self.page.get_by_text(self.locators.SUBSCRIPTION_TEXT))

    async def subscribe(self, email: str):
        await self.enter_text(
            self.page.get_by_placeholder(self.locators.SUBSCRIPTION_EMAIL_PLACEHOLDER),
            email,
        )
        await self.click(self.page.get_by_role("button").last)

    async def get_subscription_success_message(self) -> str:
        return await self.get_text(self.page.get_by_text(self.locators.SUBSCRIPTION_SUCCESS_MESSAGE))

    async def is_recommended_items_visible(self) -> bool:
        await self.scroll_to_footer()
        return await self.is_visible(self.page.get_by_text(self.locators.RECOMMENDED_ITEMS_TEXT))

    async def add_recommended_item_to_cart(self):
        await self.scroll_to_footer()
        await self.click(self.page.get_by_text("Add to cart").last, force=True)

    async def scroll_to_top_using_arrow(self):
        await self.click(self.page.get_by_role("link").last)
        await self.page.wait_for_timeout(1000)

    async def scroll_to_top(self):
        await self.press_key("Home")
        await self.page.wait_for_timeout(1000)

    async def hero_text_visible(self) -> bool:
        return await self.is_visible(self.page.get_by_role("heading", name="Full-Fledged practice website").first)
