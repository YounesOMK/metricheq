from pydantic import BaseModel, validator

from metricheq.core.connectors.base import Connector
from metricheq.core.connectors.sonar import SonarConnector
from metricheq.core.deducers.base import Deducer


ALLOWED_METRIC_KEYS = {"coverage", "bugs", "vulnerabilities", "code_smells"}


class SonarMeasureParams(BaseModel):
    component: str
    metric_key: str

    @validator("metric_key")
    def validate_metric_key(cls, v):
        if v not in ALLOWED_METRIC_KEYS:
            raise ValueError(
                f"Invalid metric_key: {v}. Must be one of {ALLOWED_METRIC_KEYS}"
            )
        return v


class SonarMeasureDeducer(Deducer):
    def __init__(self, connector: Connector, params: dict):
        if not isinstance(connector, SonarConnector):
            raise TypeError("The provided connector is not a valid sonar connector")
        self.params_model = SonarMeasureParams(**params)
        super().__init__(connector, params)

    def retrieve_data(self):
        endpoint = f"/api/measures/component?component={self.params_model.component}&metricKeys={self.params_model.metric_key}"
        response = self.client.make_request(endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def process_data(self, data):
        measures = data.get("component", {}).get("measures", [])
        for measure in measures:
            if measure["metric"] == self.params_model.metric_key:
                return measure["value"]

    def finalize(self, processed_data):
        return processed_data
