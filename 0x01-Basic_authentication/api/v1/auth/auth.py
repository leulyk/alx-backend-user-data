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
        if path is None or excluded_paths is None:
            return True
        if path not in excluded_paths:
            for ex_path in excluded_paths:
                if ex_path.endswith('*'):
                    if path.startswith(ex_path[:-1]):
                        return True
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """ checks for the Authorization header key and returns it """
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """ To be implemented soon """
        return None
