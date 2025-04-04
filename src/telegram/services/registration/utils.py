import re


def valid_name(name: str) -> bool:
    if not name:
        return False
    return not name.isnumeric()


def valid_email(email: str) -> bool:
    return bool(re.match("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$", email))


def valid_number(number: str) -> bool:
    return bool(re.match(r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$", number))
