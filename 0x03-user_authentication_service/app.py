#!/usr/bin/env python3

""" app module """

from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def index():
    """
    It returns a JSON object with a key called "message"
    and a value of "Bienvenue"
    :return: A JSON object with a message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    It returns a JSON object with a key called "message"
    and a value of "User created"
    :return: A JSON object with a message
    """

    try:
        new_user = AUTH.register_user(**request.form)
        response = {
            "email": new_user.email,
            "message": "user created"
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": 'email already registered'}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    If the user's email and password are valid, create a session and return
    a response with a cookie containing the session ID
    :return: A response object with a cookie.
    """

    is_valid_login = AUTH.valid_login(**request.form)
    if not request.form['email'] or not\
            request.form['password'] or not\
            is_valid_login:
        abort(401)
    session_id = AUTH.create_session(request.form['email'])
    response = {
        "email": request.form['email'],
        "message": "logged in"
    }
    response = jsonify(response)
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    It deletes the session_id cookie from the browser, and then deletes
    the session from the database
    :return: The user is being returned.
    """

    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('index'))


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    It returns the user's email
    :return: A JSON object with the user's email
    """

    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not session_id or not user:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    It takes an email address as input, and returns a reset token
    :return: A reset token for the user's email.
    """

    email = request.form['email']
    if not email:
        abort(400)
    try:
        reset_token = AUTH.get_reset_password_token(email)
        response = {
            "email": email,
            "reset_token": reset_token
        }
        return jsonify(response)
    except Exception as err:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def reset_password():
    """
    It takes a reset token and a new password, and updates the user's password
    :return: A JSON object with a message
    """
    try:
        email = request.form['email']
        reset_token = request.form['reset_token']
        new_password = request.form['new_password']
        AUTH.update_password(reset_token, new_password)
        response = {"email": email, "message": "Password updated"}
        return jsonify(response)
    except Exception:
        abort(403)


if __name__ == "__main__":
    """ Running the app on port 5000 """
    app.run(host="0.0.0.0", port="5000")
