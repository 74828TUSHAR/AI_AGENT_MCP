from constants.api_routes import BRANDS_LIST, PRODUCTS_LIST, SEARCH_PRODUCT
from core.base_api import BaseAPI


class ProductAPI(BaseAPI):
    async def list_products(self, *, headers=None, timeout=None):
        return await self.get(PRODUCTS_LIST, headers=headers, timeout=timeout)

    async def list_brands(self, *, headers=None, timeout=None):
        return await self.get(BRANDS_LIST, headers=headers, timeout=timeout)

    async def search_products(self, search_term: str, *, headers=None, timeout=None):
        return await self.post(
            SEARCH_PRODUCT,
            form={"search_product": search_term},
            headers=headers,
            timeout=timeout,
        )
