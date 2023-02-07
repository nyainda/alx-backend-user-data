#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


def define_auth():
    """
    It returns an instance of the class that is specified in the environment
    variable `AUTH_TYPE`
    :return: The class that is being returned is the one that is being selected
    """
    auth = None
    selected_class = os.getenv('AUTH_TYPE')
    if selected_class == 'auth':
        from api.v1.auth.auth import Auth
        auth = Auth()
    if selected_class == 'basic_auth':
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    return auth


auth = define_auth()


@app.before_request
def before_request():
    """
    If the request path is not in the list of paths that don't require
    authentication, and the request doesn't have an authorization header,
    or the authorization header doesn't match a user in the database,
    then abort the request with a 401 or 403 status code
    :return: the response object.
    """
    if auth is None:
        return
    paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']

    if not auth.require_auth(request.path, paths):
        return
    if auth.authorization_header(request) is None:
        return abort(401)
    if auth.current_user(request) is None:
        return abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
