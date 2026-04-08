import re

from playwright.async_api import Page

from locators.products.products_locators import ProductsLocators


class ProductsPage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = ProductsLocators()

    async def is_all_products_visible(self) -> bool:
        return await self.page.get_by_text(self.locators.PRODUCTS_HEADING).is_visible()

    async def all_product_cards(self):
        return self.page.get_by_role("link", name=self.locators.VIEW_PRODUCT_LINK_NAME)

    async def open_first_product_details(self):
        await self.page.get_by_role(
            "link", name=self.locators.VIEW_PRODUCT_LINK_NAME
        ).first.click()
        await self.page.wait_for_load_state("domcontentloaded")

    async def product_detail_text(self) -> str:
        return await self.page.evaluate("document.body.innerText")

    async def search_product(self, product_name: str):
        search_input = self.page.get_by_placeholder(self.locators.SEARCH_INPUT_PLACEHOLDER)
        await search_input.fill(product_name)
        await self.page.get_by_role("button").first.click()
        await self.page.wait_for_timeout(1000)

    async def is_searched_products_visible(self) -> bool:
        return await self.page.get_by_text(self.locators.SEARCHED_PRODUCTS_TEXT).is_visible()

    async def search_results_text(self) -> str:
        return await self.page.evaluate("document.body.innerText")

    async def add_product_to_cart(self, index: int):
        await self.page.get_by_text(self.locators.ADD_TO_CART_TEXT).nth(index).click(force=True)
        await self.page.wait_for_timeout(500)

    async def continue_shopping(self):
        await self.page.get_by_role("button", name=self.locators.CONTINUE_SHOPPING_BUTTON_NAME).click()

    async def view_cart_from_modal(self):
        await self.page.get_by_role("link", name=self.locators.VIEW_CART_LINK_NAME).click()
        await self.page.wait_for_load_state("domcontentloaded")

    async def set_product_quantity(self, quantity: str):
        await self.page.get_by_role("spinbutton").fill(quantity)

    async def first_product_name(self) -> str:
        heading = self.page.get_by_role("heading").nth(5)
        return (await heading.inner_text()).strip()

    async def add_review(self, name: str, email: str, review: str):
        await self.page.get_by_placeholder(self.locators.NAME_PLACEHOLDER).fill(name)
        await self.page.get_by_placeholder(self.locators.EMAIL_PLACEHOLDER).first.fill(email)
        await self.page.get_by_placeholder(self.locators.REVIEW_PLACEHOLDER).fill(review)
        await self.page.get_by_role("button", name="Submit").click()

    async def get_review_success_message(self) -> str:
        return await self.page.get_by_text(self.locators.REVIEW_SUCCESS_MESSAGE).inner_text()

    async def open_category(self, category_name: str, sub_category_name: str):
        await self.page.get_by_role(
            "link", name=re.compile(category_name, re.IGNORECASE)
        ).first.click(force=True)
        await self.page.wait_for_timeout(500)
        sub_category_link = self.page.get_by_text(sub_category_name, exact=False).first
        href = await sub_category_link.get_attribute("href")
        if href:
            await self.page.goto(f"https://automationexercise.com{href}", wait_until="domcontentloaded")
        else:
            await sub_category_link.click(force=True)
            await self.page.wait_for_load_state("domcontentloaded")

    async def open_brand(self, brand_name: str):
        await self.page.get_by_role("link", name=re.compile(brand_name, re.IGNORECASE)).first.click()
        await self.page.wait_for_load_state("domcontentloaded")
