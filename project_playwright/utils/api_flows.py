from constants.api_routes import CREATE_ACCOUNT, DELETE_ACCOUNT, GET_USER_DETAIL_BY_EMAIL, UPDATE_ACCOUNT
from utils.api_payload_factory import build_api_user_payload


async def create_user(api_client, template):
    payload = build_api_user_payload(template)
    response = await api_client.post(CREATE_ACCOUNT, form=payload)
    return payload, response


async def get_user_by_email(api_client, email):
    return await api_client.get(GET_USER_DETAIL_BY_EMAIL, params={"email": email})


async def update_user(api_client, original_payload, updated_fields):
    payload = dict(original_payload)
    payload.update(updated_fields)
    response = await api_client.put(UPDATE_ACCOUNT, form=payload)
    return payload, response


async def delete_user(api_client, email, password):
    return await api_client.delete(
        DELETE_ACCOUNT,
        form={"email": email, "password": password},
    )
