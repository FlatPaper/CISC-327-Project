import re
from datetime import datetime

EMAIL_REGEX = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.["
                         r"-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t "
                         r"-~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.["
                         r"-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

POSTAL_REGEX = re.compile(r"^[A-Z]\d[A-Z]\d[A-Z]\d$")


def validate_email(email: str):
    # Check for empty email field
    if len(email) == 0:
        return False, "Email cannot be empty."

    # Check that email matches RFC 5322 constraints with a very long regex
    if not EMAIL_REGEX.match(email):
        return False, "Email does not follow addr-spec defined in RFC 5322."

    return True, "Email is in the correct format."


def validate_password(password: str):
    # Check for empty email and password fields
    if len(password) == 0:
        return False, "Password cannot be empty."

    # Check for password complexity constraints
    if len(password) < 6:
        return False, "Password is too short."
    if not any(ch.isupper() for ch in password):
        return False, "The password does not contain any uppercase characters."
    if not any(ch.islower() for ch in password):
        return False, "The password does not contain any lowercase characters."
    if not any(not ch.isalnum() for ch in password):
        return False, "The password does not contain any special characters."

    return True, "Password meets the constraints."


def validate_postal_code(postal_code: str):
    # Check if postal code field is empty
    if len(postal_code) == 0:
        return False, "Postal code cannot be empty."

    # Check that postal code is a valid Canadian postal code
    if not POSTAL_REGEX.match(postal_code):
        return False, "Postal code is not a valid Canadian postal code."

    return True, "Valid Canadian postal code given."


def validate_username(username: str):
    # Check for username constraints
    if len(username) == 0:
        return False, "The username is empty."
    if len(username) <= 2 or len(username) >= 20:
        error_info = "The username must be longer than 2 characters and " \
                     "shorter than 20 characters. "
        return False, error_info
    if not all(ch.isalnum() or ch.isspace() for ch in username):
        error_info = "The username contains characters that are not " \
                     "alphanumeric or a space. "
        return False, error_info
    if username[0] == ' ':
        return False, "The username cannot contain a space as its prefix."
    if username[len(username) - 1] == ' ':
        return False, "The username cannot contain a space as its suffix."

    return True, "Username meets the constraints."


def validate_title(title: str):
    if not all(ch.isalnum() or ch.isspace() for ch in title):
        return False, "Title of the product must be alphanumeric."

    if len(title) > 80:
        return False, "Title of the product must be 80 characters or less."

    if title.strip() != title:
        return False, "Spaces as prefixes and suffixes are not allowed."

    return True, "Title meets constraints."


def validate_description(description: str, title: str):
    if len(description) < 20 or len(description) > 2000:
        return False, "Description length must be between 20-2000 characters."

    if len(description) <= len(title):
        return False, "Description must be longer than the title."

    return True, "Description meets constraints."


def validate_price(price: int, listing_price: int):
    if price < 10 or price > 1000:
        return False, "Price must be between 10 and 1000."

    if price <= listing_price:
        return False, "New price must be greater than the previous price."

    return True, "Price meets constraints."


def validate_date(date: datetime):
    low = datetime(2021, 1, 2)
    high = datetime(2025, 1, 2)
    if low > date > high:
        return False, "New date must be between 2021-01-02 and 2025-01-02."

    return True, "Date was modified."
