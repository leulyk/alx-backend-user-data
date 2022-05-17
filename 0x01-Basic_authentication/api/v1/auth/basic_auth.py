#!/usr/bin/env python3

"""
    Demonstrating Basic Auth
"""


from api.v1.auth.auth import Auth


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
