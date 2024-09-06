#!/usr/bin/env python3
"""
new authentication system, based on Session ID stored in database
(for us, it will be in a file, like User)
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from os import getenv
from datetime import datetime, timedelta
from flask import request


class SessionDBAuth(SessionExpAuth):
    """SessionExpAuth class to manage API authentication
    """

    def create_session(self, user_id=None) -> str:
        """Create session
        """
        session_id = super().create_session(user_id)
        if type(session_id) == str:
            kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get user ID from session
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        current_time = datetime.now()
        time_delta = timedelta(seconds=self.session_duration)
        expiration_time = sessions[0].created_at + time_delta
        if expiration_time < current_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None):
        """Delete the user session / log out
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
