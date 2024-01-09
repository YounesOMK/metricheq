from pydantic import BaseModel
import requests
from requests import RequestException
from metricheq.core.authenticators import BearerTokenAuthenticator, TokenAuthenticator

from metricheq.core.connectors.base import Client, Connector


class CodecovConfig(BaseModel):
    base_url: str = "https://api.codecov.io/api/v2"
    api_token: str


class CodecovClient(Client):
    def __init__(self, config: CodecovConfig) -> None:
        super().__init__(config)
        self.authenticator = BearerTokenAuthenticator(config.api_token)
        self.base_url = config.base_url

    def make_request(self, endpoint: str, method: str = "GET", **kwargs):
        full_url = f"{self.base_url}{endpoint}"
        request = requests.Request(method, full_url, **kwargs)
        prepared_request = self.authenticator.apply(request)
        with requests.Session() as session:
            response = session.send(prepared_request.prepare())

        return response


class CodecovConnector(Connector):
    def __init__(self, client):
        super().__init__(client)

    @staticmethod
    def from_config(config):
        return CodecovConnector(client=CodecovClient(config))

    def ensure_connectivity(self):
        try:
            response = self.client.make_request("/github")
            if response.status_code == 200:
                return True
            else:
                raise ConnectionError(
                    f"Failed to connect to Codecov API. Status Code: {response.status_code}"
                )
        except RequestException as e:
            raise ConnectionError(f"Failed to connect to Codecov: {e}")
