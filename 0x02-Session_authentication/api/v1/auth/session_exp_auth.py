#!/usr/bin/env python3
"""
Module of expiration Class
"""
from datetime import datetime, timedelta
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Session Exp Auth class"""

    def __init__(self):
        """
        It initializes the class by setting the session duration to
        the value of the environment variable
        `SESSION_DURATION` if it exists, or to 0 if it doesn't
        """
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        It creates a session for a user, and returns the session ID

        :param user_id: The user_id of the user who is logging in
        :type user_id: str
        :return: session_id
        """
        if not user_id:
            return None
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        If the session ID is valid, return the user ID

        :param session_id: The session ID of the user
        :return: The user_id for the session_id
        """
        if not session_id:
            return None
        user_dictionary = self.user_id_by_session_id.get(session_id)
        if user_dictionary is None:
            return None
        user = user_dictionary.get('user_id')
        if user is None:
            return None
        if self.session_duration <= 0:
            return user

        created_at = user_dictionary.get('created_at')
        if not created_at:
            return None
        duration_in_seconds = timedelta(seconds=self.session_duration)
        if created_at + duration_in_seconds < datetime.now():
            return None
        return user
