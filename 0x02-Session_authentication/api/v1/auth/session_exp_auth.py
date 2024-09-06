#!/usr/bin/env python3
"""class SessionExpAuth that inherits from SessionAuth"""

from api.v1.auth.session_auth import SessionAuth
from flask import Flask, request, abort
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """class implementation to add expiration date to a Session ID"""
    def __init__(self):
        """constructor"""
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create a session"""
        session_id = super().create_session(user_id)
        if session_id:
            session_dict = {'user_id': user_id, 'created_at': datetime.now()}
            SessionAuth.user_id_by_session_id[session_id] = session_dict
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """return a User ID based on a Session ID"""
        if not session_id:
            return None
        session_dict = SessionAuth.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        if 'created_at' not in session_dict:
            return None
        delta_time = timedelta(seconds=self.session_duration)
        if session_dict['created_at'] + delta_time < datetime.now():
            return None
        return session_dict.get('user_id')
