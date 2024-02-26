# idgen_alpha.py

import random
import string
import secrets
import uuid
from ._utils import luhn_checksum
import bson
import datetime
from typing import Union


def generate_password(length: int = 6) -> str:
    """
    Generate a password of at least 6 characters with at least one uppercase,
    one lowercase letter, one number, and one symbol.

    :param length: Length of the password (default is 6).
    :return: Generated password.
    """
    assert length >= 6, f"Password length can't be less than 6, {length} given!"
    while True:
        pwd = ""
        for i in range(length):
            pwd += "".join(
                secrets.choice(
                    string.ascii_letters + string.digits + string.punctuation
                )
            )
        if (
                (any(char.isupper() for char in pwd))
                and (any(char.islower() for char in pwd))
                and (any(char in string.punctuation for char in pwd))
                and (any(char in string.digits for char in pwd))
        ):
            break

    return pwd


def generate_guid() -> str:
    """
    Generate a GUID.

    :return: Generated GUID.
    """
    guid = str(uuid.uuid4())
    guid = guid.upper()
    return guid


def generate_credit_card_number(length: int = 8) -> str:
    """
    Generate a credit card number using the Luhn checksum test.

    :param length: Length of the credit card number (default is 8).
    :return: Generated credit card number.
    """
    number = "".join(random.choices(string.digits, k=length))
    while not luhn_checksum(number):
        number = "".join(random.choices(string.digits, k=length))
    return number


def generate_pin_number(length: int = 4) -> str:
    """
    Generate a credit/debit card pin number. The pin number can only contain digits.

    :param length: Length of the pin number (default is 4).
    :return: Generated pin number.
    """
    return "".join(random.choices(string.digits, k=length))


def generate_object_id() -> str:
    """
    Generate a MongoDB-like ObjectID.

    :return: Generated ObjectID.
    """
    return str(bson.ObjectId())


def generate_unix_timestamp() -> int:
    """
    Generate a Unix timestamp representing the current time.

    :return: Generated Unix timestamp.
    """
    return int(datetime.datetime.now(datetime.UTC).timestamp())


def generate_random_string(length: int = 8) -> str:
    """
    Generate a random string of the specified length.

    :param length: Length of the random string (default is 8).
    :return: Generated random string.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_secure_token(length: int = 16) -> str:
    """
    Generate a secure token using the secrets module.

    :param length: Length of the secure token (default is 16).
    :return: Generated secure token.
    """
    return secrets.token_hex(length)


def generate_random_uuid() -> str:
    """
    Generate a random UUID.

    :return: Generated random UUID.
    """
    return str(uuid.uuid4())


def generate_email_address() -> str:
    """
    Generate a random email address.

    :return: Generated random email address.
    """
    username = generate_random_string(8)
    domain = generate_random_string(5) + ".com"
    return f"{username}@{domain}"


def generate_phone_number() -> str:
    """
    Generate a random phone number.

    :return: Generated random phone number.
    """
    return ''.join(random.choices(string.digits, k=10))


def generate_boolean() -> bool:
    """
    Generate a random boolean value.

    :return: Generated random boolean value.
    """
    return random.choice([True, False])


def generate_choice(choices: list) -> Union[str, int, bool]:
    """
    Generate a random choice from the given list of options.

    :param choices: List of options.
    :return: Randomly selected item from the list.
    """
    return random.choice(choices)
