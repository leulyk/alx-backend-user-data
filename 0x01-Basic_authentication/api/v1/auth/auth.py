#!/usr/bin/env python3

"""
    Handles the API authentication
"""


from flask import request
from typing import List, TypeVar


class Auth:
    """ Class to act as an authentication template """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ checks for paths that require authentication """
        if path is not None and path[-1] != '/':
            path += '/'
        if path is None or excluded_paths is None or \
                path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """ To be implemented soon """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ To be implemented soon """
        return None
