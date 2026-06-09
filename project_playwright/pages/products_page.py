import re

from locators.products.products_locators import ProductsLocators
from playwright.async_api import Page

from pages.base_page import BasePage


class ProductsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = ProductsLocators()

    async def is_all_products_visible(self) -> bool:
        return await self.is_visible(self.page.get_by_text(self.locators.PRODUCTS_HEADING))

    async def all_product_cards(self):
        return self.page.get_by_role("link", name=self.locators.VIEW_PRODUCT_LINK_NAME)

    async def open_first_product_details(self):
        await self.click(self.page.get_by_role("link", name=self.locators.VIEW_PRODUCT_LINK_NAME).first)
        await self.wait_for_page_load_state("domcontentloaded")

    async def product_detail_text(self) -> str:
        return await self.page.evaluate("document.body.innerText")

    async def search_product(self, product_name: str):
        await self.enter_text(self.page.get_by_placeholder(self.locators.SEARCH_INPUT_PLACEHOLDER), product_name)
        await self.click(self.page.get_by_role("button").first)
        await self.page.wait_for_timeout(1000)

    async def is_searched_products_visible(self) -> bool:
        return await self.is_visible(self.page.get_by_text(self.locators.SEARCHED_PRODUCTS_TEXT))

    async def search_results_text(self) -> str:
        return await self.page.evaluate("document.body.innerText")

    async def add_product_to_cart(self, index: int):
        # Wait for networkidle so ads and lazy-loaded product cards have fully rendered
        try:
            await self.page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass  # networkidle may time out on ad-heavy pages — proceed anyway

        # Dismiss any ad overlay/iframe that may be blocking the products
        try:
            await self.page.keyboard.press("Escape")
            await self.page.wait_for_timeout(500)
        except Exception:
            pass

        add_to_cart_locator = self.page.get_by_text(self.locators.ADD_TO_CART_TEXT).nth(index)

        # Scroll the target button into view so it is visible before clicking
        await add_to_cart_locator.scroll_into_view_if_needed(timeout=60000)
        await self.click(add_to_cart_locator, force=True)
        await self.page.wait_for_timeout(500)

    async def continue_shopping(self):
        await self.click(self.page.get_by_role("button", name=self.locators.CONTINUE_SHOPPING_BUTTON_NAME))

    async def view_cart_from_modal(self):
        await self.click(self.page.get_by_role("link", name=self.locators.VIEW_CART_LINK_NAME))
        await self.wait_for_page_load_state("domcontentloaded")

    async def set_product_quantity(self, quantity: str):
        await self.enter_text(self.page.get_by_role("spinbutton"), quantity)

    async def first_product_name(self) -> str:
        heading = self.page.get_by_role("heading").nth(5)
        return (await heading.inner_text()).strip()

    async def add_review(self, name: str, email: str, review: str):
        await self.enter_text(self.page.get_by_placeholder(self.locators.NAME_PLACEHOLDER), name)
        await self.enter_text(self.page.get_by_placeholder(self.locators.EMAIL_PLACEHOLDER).first, email)
        await self.enter_text(self.page.get_by_placeholder(self.locators.REVIEW_PLACEHOLDER), review)
        await self.click(self.page.get_by_role("button", name="Submit"))

    async def get_review_success_message(self) -> str:
        return await self.get_text(self.page.get_by_text(self.locators.REVIEW_SUCCESS_MESSAGE))

    async def open_category(self, category_name: str, sub_category_name: str):
        await self.click(
            self.page.get_by_role("link", name=re.compile(category_name, re.IGNORECASE)).first,
            force=True,
        )
        await self.page.wait_for_timeout(500)
        sub_category_link = self.page.get_by_text(sub_category_name, exact=False).first
        href = await sub_category_link.get_attribute("href")
        if href:
            await self.navigate(f"https://automationexercise.com{href}")
        else:
            await self.click(sub_category_link, force=True)
            await self.wait_for_page_load_state("domcontentloaded")

    async def open_brand(self, brand_name: str):
        await self.click(self.page.get_by_role("link", name=re.compile(brand_name, re.IGNORECASE)).first)
        await self.wait_for_page_load_state("domcontentloaded")
