#!/usr/bin/env python3
"""include auth class and methods regarding hashed passwords"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a new UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user with the provided email and password.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        check the password with bcrypt.checkpw.
        If it matches return True. In any other case, return False
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        find the user corresponding to the email,
        generate a new UUID and store it in database as the user’s session_id,
        then return the session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_ID = _generate_uuid()
            self._db.update_user(user.id, session_id=session_ID)
            return session_ID
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id):
        """get the user corresponding to the session ID."""
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
