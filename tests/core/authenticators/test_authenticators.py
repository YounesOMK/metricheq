import unittest
from requests import Request

import base64

from metricheq.core.authenticators import (
    BearerTokenAuthenticator,
    NoAuthAuthenticator,
    TokenAuthenticator,
    UserPasswordBasicAuthenticator,
)


class TestAuthenticators(unittest.TestCase):
    def test_bearer_token_authenticator(self):
        token = "test_token"
        authenticator = BearerTokenAuthenticator(token)
        request = Request()
        modified_request = authenticator.apply(request)
        self.assertEqual(modified_request.headers["Authorization"], f"Bearer {token}")

    def test_token_authenticator(self):
        token = "test_token"
        authenticator = TokenAuthenticator(token)
        request = Request()
        modified_request = authenticator.apply(request)
        self.assertEqual(
            modified_request.headers["Authorization"], f"Token token={token}"
        )

    def test_user_password_basic_authenticator(self):
        username = "user"
        password = "pass"
        authenticator = UserPasswordBasicAuthenticator(username, password)
        request = Request()
        modified_request = authenticator.apply(request)
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.assertEqual(
            modified_request.headers["Authorization"], f"Basic {encoded_credentials}"
        )

    def test_no_auth_authenticator(self):
        authenticator = NoAuthAuthenticator()
        request = Request()
        modified_request = authenticator.apply(request)
        self.assertNotIn("Authorization", modified_request.headers)
