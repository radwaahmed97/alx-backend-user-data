#!/usr/bin/env python3
"""include auth class and methods regarding hashed passwords"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
