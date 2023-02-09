#!/usr/bin/env python3
""" Session Auth module"""

import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ Session Auth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session for the user with the given user_id,
        and return the session_id.

        :param user_id: The user ID of the user to create a session for
        :type user_id: str
        :return: A session ID
        """
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Return the user ID for the given session ID.

            :param session_id: The session ID to get the user ID for
            :type session_id: str
            :return: The user ID for the given session ID
            :rtype: str
        """
        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Return the user ID for the given session ID.

            :param request: The request to get the user ID for
            :type request: str
            :return: The user ID for the given session ID
            :rtype: str
        """
        session_cookie = self.session_cookie(request)
        session_id = self.user_id_for_session_id(session_cookie)
        return User.get(session_id)

    def destroy_session(self, request=None):
        """
        It deletes the session id from the dictionary
        :param request: The request object
        :return: A boolean value.
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        try:
            del self.user_id_by_session_id[session_id]
        except Exception:
            pass
        return True
