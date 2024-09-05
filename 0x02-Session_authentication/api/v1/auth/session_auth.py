#!/usr/bin/env python3
"""class SessionAuth that inherits from Auth"""

from models.user import User
from api.v1.auth.auth import Auth
from typing import TypeVar, List
import uuid


class SessionAuth(Auth):
    """class SessionAuth that inherits from Auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """method creates a Session ID for a user_id"""
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if session_id is None or type(session_id) is not str:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ returns a User instance based on a cookie value"""
        cookiebased = self.session_cookie(request)
        return User.get(
            self.user_id_for_session_id(cookiebased))

    def destroy_session(self, request=None):
        """deletes the user session / logout"""
        if request is None:
            return False
        else:
            cookiebased = self.session_cookie(request)
            if not cookiebased or not self.user_id_by_session_id(cookiebased):
                return False
            else:
                self.user_id_by_session_id.pop(cookiebased)
                return True
