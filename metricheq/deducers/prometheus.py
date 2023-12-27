from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from metricheq.connectors.base import Connector
from metricheq.connectors.prometheus import PrometheusConnector
from urllib.parse import quote

from metricheq.deducers.base import Deducer

# TODO: provide default value for step based on start, end date and points


class PrometheusServiceAvailabilityParams(BaseModel):
    labels: dict[str, str]
    start_time: datetime
    end_time: datetime
    step: Optional[int] = None


class PrometheusServiceAvailabilityDeducer(Deducer):
    def __init__(self, connector: Connector, params: dict):
        if not isinstance(connector, PrometheusConnector):
            raise TypeError(
                "The provided connector is not a valid prometheus connector"
            )
        self.params_model = PrometheusServiceAvailabilityParams(**params)
        super().__init__(connector, params)

    def retrieve_data(self):
        label_filters = ",".join(
            [f'{key}="{value}"' for key, value in self.params_model.labels.items()]
        )
        start_date_rfc3339 = self.params_model.start_time.isoformat() + "Z"
        end_date_rfc3339 = self.params_model.end_time.isoformat() + "Z"
        step = self.params.get("step", 60)

        query = f"up{{{label_filters}}}"
        encoded_query = quote(query)
        endpoint = f"query_range?query={encoded_query}&start={start_date_rfc3339}&end={end_date_rfc3339}&step={step}"

        response = self.client.make_request(endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def process_data(self, data):
        results = data.get("data", {}).get("result", [])

        up_times = 0
        total_times = 0

        for result in results:
            for _, status in result.get("values", []):
                total_times += 1
                if status == "1":  # service was up
                    up_times += 1

        availability_percentage = (
            (up_times / total_times) * 100 if total_times > 0 else 0
        )
        return availability_percentage

    def finalize(self, processed_data):
        return processed_data
