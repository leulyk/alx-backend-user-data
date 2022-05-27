#!/usr/bin/env python3

"""
    Our flask app
"""

from auth import Auth
from flask import abort, Flask, jsonify, redirect, request


AUTH = Auth()
app = Flask(__name__)

app.url_map.strict_slashes = False


@app.route('/')
def index():
    """ a GET route that returns a message """
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'])
def register_user():
    """ endpoint that registers a user to our database """
    email = request.form['email']
    password = request.form['password']
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": "{}".format(email),
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """ implements the login functionality """
    email = request.form['email']
    password = request.form['password']
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        resp = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie("session_id", session_id)
        return resp
    abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """ implements the logout functionality """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


@app.route("/profile")
def profile():
    """ finds a user based on session id """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email})
    abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token() -> str:
    """ password reset endpoint """
    email = request.form.get("email")
    reset_token = None
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        reset_token = None
    if reset_token:
        return jsonify({"email": email, "reset_token": reset_token})
    abort(403)


if __name__ == ('__main__'):
    app.run(host='0.0.0.0', port='5000')
