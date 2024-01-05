from pydantic import BaseModel
import requests
from requests import RequestException
from metricheq.core.authenticators import UserPasswordBasicAuthenticator

from metricheq.core.connectors.base import (
    Client,
    Connector,
)
from metricheq.exceptions.core.exceptions import UnsupportedConfigurationError


class PrometheusConfig(BaseModel):
    host_url: str


class PrometheusUserPasswordConfig(PrometheusConfig):
    username: str
    password: str


class PrometheusClient(Client):
    def __init__(self, config) -> None:
        if not isinstance(config, PrometheusConfig):
            raise UnsupportedConfigurationError("Unsupported configuration type.")

        super().__init__(config)
        self.base_url = config.host_url
        self.authenticator = None

        if isinstance(config, PrometheusUserPasswordConfig):
            self.authenticator = UserPasswordBasicAuthenticator(
                config.username, config.password
            )

    def make_request(self, endpoint: str, method: str = "GET", **kwargs):
        full_url = f"{self.base_url}/api/v1/{endpoint}"
        request = requests.Request(method, full_url, **kwargs)

        if self.authenticator:
            prepared_request = self.authenticator.apply(request)
        else:
            prepared_request = request

        with requests.Session() as session:
            response = session.send(prepared_request.prepare())

        return response


class PrometheusConnector(Connector):
    def __init__(self, client):
        super().__init__(client)

    @staticmethod
    def from_config(config):
        return PrometheusConnector(client=PrometheusClient(config))

    def ensure_connectivity(self):
        try:
            response = self.client.make_request("status/runtimeinfo")
            if response.status_code == 200:
                return True
            else:
                raise ConnectionError(
                    f"Failed to connect to Prometheus API. Status Code: {response.status_code}"
                )
        except RequestException as e:
            raise ConnectionError(f"Failed to connect to Prometheus: {e}")
