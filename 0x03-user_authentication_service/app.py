#!/usr/bin/env python3

"""
    Our flask app
"""

from auth import Auth
from flask import Flask, jsonify, request


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


if __name__ == ('__main__'):
    app.run(host='0.0.0.0', port='5000')
