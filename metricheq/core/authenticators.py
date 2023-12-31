from abc import ABC, abstractmethod
import base64

from requests import Request


class Authenticator(ABC):
    @abstractmethod
    def apply(self, request) -> Request:
        pass


class BearerTokenAuthenticator(Authenticator):
    def __init__(self, token) -> None:
        self.token = token

    def apply(self, request):
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request


class TokenAuthenticator(Authenticator):
    def __init__(self, token) -> None:
        self.token = token

    def apply(self, request):
        request.headers["Authorization"] = f"Token token={self.token}"
        return request


class UserPasswordBasicAuthenticator(Authenticator):
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def apply(self, request):
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        request.headers["Authorization"] = f"Basic {encoded_credentials}"
        return request


class NoAuthAuthenticator(Authenticator):
    def apply(self, request) -> Request:
        return request
