#!/usr/bin/env python3

""" end to end tests module"""

import requests

URL = 'http://0.0.0.0:5000'


def register_user(email: str, password: str) -> None:
    """
    Validating user registration
    """
    response = requests.post(f'{URL}/users',
                             {'email': email, 'password': password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Validating user login with wrong password
    """
    response = requests.post(f'{URL}/sessions',
                             {'email': email, 'password': password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Validating user login
    """
    response = requests.post(
        f'{URL}/sessions', {'email': email, 'password': password})
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies['session_id']


def profile_unlogged() -> None:
    """
    Profile unlogged validation
    """
    response = requests.get(f'{URL}/profile')
    assert response.status_code == 403


def profile_logged(session_id) -> None:
    """ Validating user profile """
    response = requests.get(
        f'{URL}/profile', cookies={'session_id': session_id})
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def log_out(session_id):
    """ Validating user logout """
    response = requests.delete(
        f'{URL}/sessions', cookies={'session_id': session_id})
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """ Validating user password reset token """
    response = requests.post(
        f'{URL}/reset_password', {'email': email})
    assert response.status_code == 200
    assert response.json() == {
        "email": email, "reset_token": response.json()['reset_token']}
    return response.json()['reset_token']


def update_password(email: str, reset_token: str, new_password: str):
    """ Validating user password update """
    response = requests.put(f"{URL}/reset_password",
                            {'email': email, 'reset_token': reset_token,
                             'new_password': new_password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    """ A way to execute code only if the file was
    executed directly, and not imported."""

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    profile_unlogged()
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
