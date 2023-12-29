from pydantic import BaseModel
import requests
from requests import RequestException
from metricheq.connectors.base import (
    Client,
    Connector,
    TokenAuthenticator,
)


class PagerDutyConfig(BaseModel):
    base_url: str = "https://api.pagerduty.com"
    api_key: str


class PagerDutyClient(Client):
    def __init__(self, config: PagerDutyConfig) -> None:
        super().__init__(config)
        self.authenticator = TokenAuthenticator(config.api_key)
        self.base_url = config.base_url

    def make_request(self, endpoint: str, method: str = "GET", **kwargs):
        full_url = f"{self.base_url}{endpoint}"
        request = requests.Request(method, full_url, **kwargs)
        prepared_request = self.authenticator.apply(request)
        with requests.Session() as session:
            response = session.send(prepared_request.prepare())

        return response


class PagerDutyConnector(Connector):
    def __init__(self, client):
        super().__init__(client)

    @staticmethod
    def from_config(config):
        return PagerDutyConnector(client=PagerDutyClient(config))

    def ensure_connectivity(self):
        try:
            response = self.client.make_request("/users", params={"limit": 1})
            if response.status_code == 200:
                return True
            else:
                raise ConnectionError(
                    f"Failed to connect to PagerDuty API. Status Code: {response.status_code}"
                )
        except RequestException as e:
            raise ConnectionError(f"Failed to connect to PagerDuty: {e}")
