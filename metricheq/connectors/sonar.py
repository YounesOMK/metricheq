from typing import Optional
import requests
from metricheq.connectors.base import (
    ApiTokenAuthenticator,
    BasicAuthenticator,
    Client,
    Connector,
)
from pydantic import BaseModel


class SonarConnectorBaseConfig(BaseModel):
    host_url: str
    proxy: Optional[str] = None


class SonarConnectorApiTokenConfig(SonarConnectorBaseConfig):
    user_token: str


class SonarConnectorBasicConfig(SonarConnectorBaseConfig):
    username: str
    password: str


class SonarClient(Client):
    def __init__(self, config):
        self.base_url = config.host_url
        self.proxy = config.proxy

        if isinstance(config, SonarConnectorApiTokenConfig):
            self.authenticator = ApiTokenAuthenticator(config.user_token)
        if isinstance(config, SonarConnectorBasicConfig):
            self.authenticator = BasicAuthenticator(config.username, config.password)
            self.base_url = config.host_url
        else:
            return TypeError("Unsupported configuration type.")

    def make_request(self, endpoint: str, method: str = "GET", **kwargs):
        url = f"{self.base_url}{endpoint}"
        proxies = {"http": self.proxy, "https": self.proxy} if self.proxy else {}
        request = requests.Request(method, url, **kwargs)
        prepared_request = self.authenticator.apply(request)
        with requests.Session() as session:
            response = session.send(prepared_request.prepare(), proxies=proxies)
        response.raise_for_status()
        return response


class SonarConnector(Connector):
    def __init__(self, client):
        super().__init__(client)

    @staticmethod
    def from_config(config):
        return SonarConnector(client=SonarClient(config))

    def ensure_connectivity(self):
        try:
            response = self.client.make_request("/api/system/health")
            data = response.json()
            health_status = data.get("health")
            if health_status == "GREEN":
                return True
            else:
                raise Exception(
                    f"SonarQube health check returned status: {health_status}"
                )
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to Sonar service: {e}")
