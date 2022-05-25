#!/usr/bin/env python3

"""
    Module to excercise on authorization
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """
        Takes a password and returns a salted hash of the password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
