from abc import ABC, abstractmethod


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
