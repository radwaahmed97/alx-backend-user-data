#!/usr/bin/env python3
"""new Flask view that handles all routes for the Session authentication"""

from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models.user import User
from api.v1.auth.session_auth import SessionAuth
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /auth_session/login
    Return:
      - User object JSON represented
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400
    search = User.search({'email': email})
    if not search:
        return jsonify({"error": "no user found for this email"}), 404
    for user in search:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
        _my_session_id = SessionAuth().create_session(user.id)
        response = jsonify(user.to_json())
        response.set_cookie(getenv('SESSION_NAME'), _my_session_id)
        return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """ DELETE /auth_session/logout
    Return:
      - Empty dictionary
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
