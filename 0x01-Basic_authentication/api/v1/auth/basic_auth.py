#!/usr/bin/env python3
""" basic Auth Module """

from typing import TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ class BasicAuth """

    def __init__(self):
        """ __init__ """
        super().__init__()

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """
        It takes a string that looks like this:
        `Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==`
        and returns this:
        `QWxhZGRpbjpvcGVuIHNlc2FtZQ==`

        :param authorization_header: The value of the Authorization header
        :type authorization_header: str
        :return: The base64 encoded string is being returned.
        """
        import re
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        match_pattern = re.compile(r'^Basic (.*)$')
        match = match_pattern.match(authorization_header)
        if match is None:
            return None
        return match.group(1)

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        It takes a base64 encoded string and returns the decoded string

        :param base64_authorization_header: The base64 encoded authorization
        header
        :type base64_authorization_header: str
        :return: The decoded base64 string.
        """
        import base64
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            return base64.b64decode(
                base64_authorization_header
            ).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        It takes a decoded base64 string and returns the user credentials

        :param decoded_base64_authorization_header: The decoded base64 encoded
        authorization header
        :type decoded_base64_authorization_header: str
        :return: The user credentials.
        """
        import re
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) != str:
            return (None, None)
        if decoded_base64_authorization_header.find(':') == -1:
            return (None, None)
        matched_index = re.search(
            ':', decoded_base64_authorization_header).span()[0]
        return (
            decoded_base64_authorization_header[0:matched_index],
            decoded_base64_authorization_header[matched_index+1:]
        )

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """
        It takes a user email and password and returns the user object
        :param user_email: The user email
        :type user_email: str
        :param user_pwd: The user password
        :type user_pwd: str
        :return: The user object.
        """

        from models.user import User

        user = User()
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None
        try:
            dictionary = {"email": user_email, }
            user = user.search(dictionary)[0]
        except Exception:
            return None
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        > It takes an HTTP request object, extracts the user's email and
        password from the request, and
        returns a user object
        :param request: The request object
        :return: The user object is being returned.
        """
        if request is None:
            return None
        authorization_header = request.headers.get('Authorization')
        extracted_base64_authorization_header = \
            self.extract_base64_authorization_header(
                authorization_header)
        decoded_base64_authorization_header = \
            self.decode_base64_authorization_header(
                extracted_base64_authorization_header)
        user_email, user_pwd = self.extract_user_credentials(
            decoded_base64_authorization_header)
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
