from pydantic import BaseModel
import requests

from metricheq.connectors.base import BearerTokenAuthenticator, Client, Connector


class GitHubConfig(BaseModel):
    api_key: str
    base_url: str = "https://api.github.com"


class GitHubClient(Client):
    def __init__(self, config: GitHubConfig):
        super().__init__(config)
        self.authenticator = BearerTokenAuthenticator(config.api_key)
        self.base_url = config.base_url

    def make_request(self, endpoint: str, method: str = "GET", **kwargs):
        full_url = f"{self.base_url}{endpoint}"
        request = requests.Request(method, full_url, **kwargs)
        prepared_request = self.authenticator.apply(request)
        with requests.Session() as session:
            response = session.send(prepared_request.prepare())

        return response


class GitHubConnector(Connector):
    def __init__(self, client):
        super().__init__(client)

    @staticmethod
    def from_config(config):
        return GitHubConnector(client=GitHubClient(config))

    def ensure_connectivity(self):
        try:
            self.client.make_request("/")
        except requests.RequestException as e:
            raise ConnectionError("Failed to connect to GitHub") from e
