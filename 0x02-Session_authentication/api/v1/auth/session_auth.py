#!/usr/bin/env python3
"""class SessionAuth that inherits from Auth"""

from models.user import User
from api.v1.auth.auth import Auth
from typing import TypeVar, List
import uuid


class SessionAuth(Auth):
    """class SessionAuth that inherits from Auth"""
    def __init__(self):
        """attributes"""
        self.user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """method creates a Session ID for a user_id"""
        if user_id is None or type(user_id) is not str:
            return None
        session_id = uuid.uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id
