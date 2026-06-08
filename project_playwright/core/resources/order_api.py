from core.base_api import BaseAPI


class OrderAPI(BaseAPI):
    async def create_order(self, endpoint: str, payload, *, headers=None, timeout=None):
        return await self.post(endpoint, form=payload, headers=headers, timeout=timeout)

    async def get_order(self, endpoint: str, *, params=None, headers=None, timeout=None):
        return await self.get(endpoint, params=params, headers=headers, timeout=timeout)

    async def update_order(self, endpoint: str, payload, *, headers=None, timeout=None):
        return await self.put(endpoint, form=payload, headers=headers, timeout=timeout)

    async def delete_order(self, endpoint: str, payload=None, *, headers=None, timeout=None):
        return await self.delete(endpoint, form=payload, headers=headers, timeout=timeout)
