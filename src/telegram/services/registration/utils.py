import re


def valid_name(name: str) -> bool:
    if not name:
        return False
    return not name.isnumeric()


def valid_email(email: str) -> bool:
    return bool(re.match("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$", email))
