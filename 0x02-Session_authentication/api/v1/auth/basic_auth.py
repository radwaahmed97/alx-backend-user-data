#!/usr/bin/env python3
"""basic_authentication module"""

from api.v1.auth.auth import Auth
from typing import TypeVar, Tuple, Optional
from flask import request
from models.user import User
import base64
import re


class BasicAuth(Auth):
    """BasicAuth class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract base64 authorization header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """returns the decoded value of a Base64 string"""
        if base64_authorization_header is None or\
           type(base64_authorization_header) is not str:
            return None
        try:
            base64_code = base64_authorization_header.encode('utf-8')
            reversed_base64 = base64.b64decode(base64_code)
            return reversed_base64.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str,
            ) -> Tuple[str, str]:
        """Extracts user credentials from a base64-decoded authorization
        header that uses the Basic authentication flow.
        """
        if isinstance(decoded_base64_authorization_header, str):
            patt = r'(?P<user>[^:]+):(?P<password>.+)'
            f_match = re.fullmatch(
                patt,
                decoded_base64_authorization_header.strip(),
            )
            if f_match is not None:
                user_name = f_match.group('user')
                pword = f_match.group('password')
                return user_name, pword
        return None, None

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """Returns the User instance based on his email and password"""
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Overload current_user"""
        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(base64_header)
        user_credentials = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(user_credentials[0],
                                                 user_credentials[1])
