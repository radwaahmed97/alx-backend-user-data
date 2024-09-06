#!/usr/bin/env python3
"""class SessionExpAuth that inherits from SessionAuth"""

from api.v1.auth.session_auth import SessionAuth
from flask import request
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """class implementation to add expiration date to a Session ID"""
    def __init__(self) -> None:
        """constructor"""
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create a session"""
        session_id = super().create_session(user_id)
        if not isinstance(session_id, str):
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """return a User ID based on a Session ID"""
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dict['user_id']
            if 'created_at' not in session_dict:
                return None
            current_time = datetime.now()
            time_delta = timedelta(seconds=self.session_duration)
            expiration_time = session_dict['created_at'] + time_delta
            if expiration_time < current_time:
                return None
            return session_dict['user_id']
