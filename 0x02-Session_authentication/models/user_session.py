#!/usr/bin/env python3
""" Session user  module"""

from models.base import Base


class UserSession(Base):
    """ > The UserSession class is a child of the Base
    class and it has two attributes: user_id and
    session_id"""

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a UserSession instance """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id', None)
        self.session_id = kwargs.get('session_id', None)
