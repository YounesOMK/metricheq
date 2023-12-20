from enum import Enum
from typing import List
from pydantic import BaseModel
from metricheq.connectors.base import Connector

from metricheq.fetchers.base import Fetcher


class SonarMetricType(str, Enum):
    COVERAGE = "coverage"
    BUGS = "bugs"
    VULNERABILITIES = "vulnerabilities"
    CODE_SMELLS = "code_smells"

class SonarMeasuresParams(BaseModel):
    component: str
    metric_key: SonarMetricType


class SonarMeasuresFetcher(Fetcher):
    def __init__(self, connector: Connector, params: dict):
        self.params_model = SonarMeasuresParams(**params)
        super().__init__(connector, params)
    
    def friendly_name(self):
        return "SonarQube Measures Fetcher" 
    
    def fetch_data(self):
        endpoint = f"/api/measures/component?component={self.params_model.component}&metricKeys={self.params_model.metric_key}"
        return self.client.make_request(endpoint)

    def process_data(self, response):
        data = response.json()
        measures = data.get('component', {}).get('measures', [])
        for measure in measures:
            if measure['metric'] == self.params_model.metric_key:
                return measure['value'] 

    def finalize(self, processed_data):
        return processed_data