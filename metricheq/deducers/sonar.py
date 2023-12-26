from enum import Enum
from pydantic import BaseModel
from metricheq.connectors.base import Connector
from metricheq.connectors.sonar import SonarConnector

from metricheq.deducers.base import Deducer


class SonarMetricType(str, Enum):
    COVERAGE = "coverage"
    BUGS = "bugs"
    VULNERABILITIES = "vulnerabilities"
    CODE_SMELLS = "code_smells"


class SonarMeasureParams(BaseModel):
    component: str
    metric_key: SonarMetricType


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
