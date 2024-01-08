from typing import Optional
import requests
from metricheq.core.authenticators import (
    Authenticator,
    BearerTokenAuthenticator,
    UserPasswordBasicAuthenticator,
)
from metricheq.core.connectors.base import (
    Client,
    Connector,
)
from pydantic import BaseModel

from metricheq.exceptions.core.exceptions import UnsupportedConfigurationError


class SonarBaseConfig(BaseModel):
    host_url: str
    proxy: Optional[str] = None


class SonarTokenConfig(SonarBaseConfig):
    user_token: str


class SonarUserPasswordConfig(SonarBaseConfig):
    username: str
    password: str


class SonarClient(Client):
    def __init__(self, config: SonarBaseConfig):
        self.authenticator: Authenticator
        if isinstance(config, SonarTokenConfig):
            self.authenticator = BearerTokenAuthenticator(config.user_token)
        elif isinstance(config, SonarUserPasswordConfig):
            self.authenticator = UserPasswordBasicAuthenticator(
                config.username, config.password
            )
            self.base_url = config.host_url
        else:
            raise UnsupportedConfigurationError("Unsupported configuration type.")

        self.base_url = config.host_url
        self.proxy = config.proxy

    def make_request(self, endpoint: str, method: str = "GET", **kwargs):
        url = f"{self.base_url}{endpoint}"
        proxies = {"http": self.proxy, "https": self.proxy} if self.proxy else {}
        request = requests.Request(method, url, **kwargs)
        prepared_request = self.authenticator.apply(request)
        with requests.Session() as session:
            response = session.send(prepared_request.prepare(), proxies=proxies)
        return response


class SonarConnector(Connector):
    def __init__(self, client):
        super().__init__(client)

    @staticmethod
    def from_config(config: SonarBaseConfig):
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
