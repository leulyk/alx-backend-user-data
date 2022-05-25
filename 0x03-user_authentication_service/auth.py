#!/usr/bin/env python3

"""
    Module to excercise on authorization
"""

import bcrypt

from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


class Auth:
    """
        Auth class to interact with the authentication database
    """
    def __init__(self):
        """ constructor of Auth class """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ registers a user to our database """
        try:
            self._db.find_user_by(email=email)
            raise ValueError('User {} already exists.'.format(email))
        except NoResultFound:
            pass
        hashed_passwd = _hash_password(password)
        user = User(email=email, hashed_password=hashed_passwd)
        self._db.add_user(email, hashed_passwd)
        return user


def _hash_password(password: str) -> bytes:
    """
        Takes a password and returns a salted hash of the password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
