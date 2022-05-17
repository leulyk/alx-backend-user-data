#!/usr/bin/env python3

"""
    Demonstrating Basic Auth
"""


from api.v1.auth.auth import Auth
from base64 import b64encode, b64decode


class BasicAuth(Auth):
    """ class that implements the Basic Auth system """
    def extract_base64_authorization_header(self, authorization_header: str) \
            -> str:
        """ returns Base64 part of the Authorization header """
        if not authorization_header or \
                not isinstance(authorization_header, str) or \
                not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, authorization_header: str) \
            -> str:
        """ decodes the base64 string in the Authorization header """
        if not authorization_header or \
                not isinstance(authorization_header, str):
            return None
        try:
            if b64encode(b64decode(authorization_header)) \
                    == authorization_header.encode('utf-8'):
                return b64decode(authorization_header).decode('utf-8')
        except Exception:
            return None
