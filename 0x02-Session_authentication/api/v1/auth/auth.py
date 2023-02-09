#!/usr/bin/env python3
""" Module of Auth Class """

import os
from typing import List, TypeVar


class Auth():
    """ class Auth """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        If the path is not in the list of excluded paths, then require
        authentication

        :param path: The path of the request
        :type path: str
        :param excluded_paths: A list of paths that do not require
        authentication
        :type excluded_paths: List[str]
        :return: A boolean value.
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        path = path + '/' if path[-1] != '/' else path

        for wildcard_pattern in excluded_paths:
            if wildcard_pattern[-1] == "*" and\
                    path.startswith(wildcard_pattern[:-1]):
                return False
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        If the request has an authorization header, return it, otherwise
        return None

        :param request: The request object
        :return: The authorization header from the request.
        """
        if request is None:
            return None
        return request.headers.get('Authorization') if \
            request.headers.get('Authorization') is not None else None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Return the user object from the request """
        return None

    def session_cookie(self, request=None):
        """
        It returns the session cookie from the request object

        :param request: The request object
        :return: The session cookie is being returned.
        """
        if request is None:
            return None
        cookies = request.cookies.get(os.environ.get('SESSION_NAME'))
        return cookies if cookies is not None else None
