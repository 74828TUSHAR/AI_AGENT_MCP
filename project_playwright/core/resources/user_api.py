from constants.api_routes import CREATE_ACCOUNT, DELETE_ACCOUNT, GET_USER_DETAIL_BY_EMAIL, UPDATE_ACCOUNT, VERIFY_LOGIN
from core.base_api import BaseAPI


class UserAPI(BaseAPI):
    async def create_user(self, payload, *, headers=None, timeout=None):
        return await self.post(CREATE_ACCOUNT, form=payload, headers=headers, timeout=timeout)

    async def get_user(self, email: str, *, headers=None, timeout=None):
        return await self.get(GET_USER_DETAIL_BY_EMAIL, params={"email": email}, headers=headers, timeout=timeout)

    async def update_user(self, payload, *, headers=None, timeout=None):
        return await self.put(UPDATE_ACCOUNT, form=payload, headers=headers, timeout=timeout)

    async def delete_user(self, email: str, password: str, *, headers=None, timeout=None):
        return await self.delete(
            DELETE_ACCOUNT,
            form={"email": email, "password": password},
            headers=headers,
            timeout=timeout,
        )

    async def verify_login(self, email: str, password: str, *, headers=None, timeout=None):
        return await self.post(
            VERIFY_LOGIN,
            form={"email": email, "password": password},
            headers=headers,
            timeout=timeout,
        )
