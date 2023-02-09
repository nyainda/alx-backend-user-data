#!/usr/bin/env python3
""" Session db Auth module"""

from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ It's a session manager that uses the
    database to store session information"""

    def create_session(self, user_id=None):
        """
        It creates a session for a user.

        :param user_id: The user_id of the user to create a session for
        :return: The session_id is being returned.
        """

        if user_id is None:
            return None
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        new_session = UserSession(user_id=user_id, session_id=session_id)
        new_session.save()
        UserSession.save_to_file()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        If the session_id is valid, return the user_id associated with it

        :param session_id: The session ID that you want to look up
        :return: The user_id for the session_id
        """

        if session_id is None:
            return None
        UserSession.load_from_file()
        matches = UserSession.search({'session_id': session_id})
        if not matches:
            return None
        user_session = matches[0]
        created_at = user_session.created_at
        if created_at + timedelta(seconds=self.session_duration) <\
                datetime.now():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """
        It deletes the session id from the dictionary

        :param request: The request object
        :return: A boolean value.
        """

        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        user_session = UserSession.search({
            'session_id': session_cookie
        })
        if user_session is None:
            return False
        try:
            user_session[0].remove()
            UserSession.save_to_file()
            return True
        except Exception as e:
            return False
