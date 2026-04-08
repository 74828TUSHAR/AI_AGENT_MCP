from datetime import datetime


def build_unique_email(email_template: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return email_template.format(timestamp=timestamp)
