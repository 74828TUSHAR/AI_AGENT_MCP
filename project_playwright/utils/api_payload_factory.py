from utils.test_data_factory import build_unique_email


def build_api_user_payload(template):
    payload = dict(template)
    payload["email"] = build_unique_email(template["email_template"])
    payload.pop("email_template", None)
    return payload
