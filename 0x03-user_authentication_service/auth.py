#!/usr/bin/env python3

"""
    Module to excercise on authorization
"""

import bcrypt
import uuid

from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from typing import Union


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

    def valid_login(self, email: str, password: str) -> bool:
        """ validates a user """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode(), user.hashed_password)

    def create_session(self, email: str) -> Union[str, None]:
        """
            creates a session, stores the id in a database and returns the id
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """
            Returns the user of a specified session id
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: str) -> None:
        """ destroys a session """
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return
        self._db.update_user(user.id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ resets a password """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError()
        reset_token = uuid.UUID(_generate_uuid())
        self._db.update_user(reset_token=reset_token)
        return reset_token


def _hash_password(password: str) -> bytes:
    """
        Takes a password and returns a salted hash of the password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ generates a unique string """
    return str(uuid.uuid4())
