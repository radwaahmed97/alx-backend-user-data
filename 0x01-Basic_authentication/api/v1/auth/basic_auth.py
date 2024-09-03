#!/usr/bin/env python3
"""basic_authentication module"""

from api.v1.auth.auth import Auth
from typing import List, TypeVar
from flask import request


class BasicAuth(Auth):
    """BasicAuth class"""
