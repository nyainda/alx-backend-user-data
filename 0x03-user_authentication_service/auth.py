#!/usr/bin/env python3
""" module to hash a password """

import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """
    It takes a password as a string, generates a salt, and then hashes the
    password using the salt

    :param password: The password to hash
    :type password: str
    :return: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """
    "Generate a new UUID."

    :return: str
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        "Register a new user with the given email and password."

        The first thing we do is check that the email and password are not
        empty. If they are, we raise a ValueError

        :param email: str
        :type email: str
        :param password: str
        :type password: str
        :return: User object
        """
        try:
            self._db.find_user_by(email=email)
            raise(ValueError)
        except NoResultFound:
            hashed_password = _hash_password(password)
            created_user = self._db.add_user(email, hashed_password)
            return created_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        "Check if the given email and password are valid."

        :param email: str
        :type email: str
        :param password: str
        :type password: str
        :return: True if the email and password are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ Create a new session for the user with the given email."""

        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str):
        """ Get the user from the session id."""
        try:
            if session_id is None:
                return None
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception as e:
            return None

    def destroy_session(self, user_id: str):
        """ Destroy the session for the user with the given id."""
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        > It takes an email address, finds the user with that email address,
        generates a reset token, and updates the user with that reset token

        :param email: The email address of the user who wants to reset their
        password
        :type email: str
        :return: A reset token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except Exception as err:
            raise(ValueError)

    def update_password(self, reset_token: str, password: str) -> None:
        """
        > It takes a reset token and a new password, finds the user with that
        reset token, hashes the password, and updates the user with the new
        password

        :param reset_token: The reset token
        :type reset_token: str
        :param password: The new password
        :type password: str
        :return: None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password,
                                 reset_token=None)
        except Exception as err:
            raise(ValueError)
