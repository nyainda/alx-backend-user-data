#!/usr/bin/env python3
"""
Encrypt and validate passwords with bcrypt
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    It takes a string, encodes it as UTF-8, and then hashes it using bcrypt

    :param password: The password to hash
    :type password: str
    :return: A byte string
    """
    return bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    )


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    It takes a hashed password and a password, and returns
    True if the password matches the hashed
    password, and False otherwise

    :param hashed_password: The hashed password that was
    returned from the hash_password function
    :type hashed_password: bytes
    :param password: The password to be hashed
    :type password: str
    :return: A boolean value.
    """
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed_password
    )
