from abc import ABC, abstractmethod
import base64


class Authenticator(ABC):
    @abstractmethod
    def apply(self, request):
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
        request.headers["Authorization"] = f"Token {self.token}"
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


class Client(ABC):
    def __init__(self, config) -> None:
        self.config = config

    @abstractmethod
    def make_request(self, endpoint: str, method: str = "GET", **kwargs):
        pass


class Connector(ABC):
    def __init__(self, client):
        self.client = client

    @abstractmethod
    def ensure_connectivity(self):
        pass
