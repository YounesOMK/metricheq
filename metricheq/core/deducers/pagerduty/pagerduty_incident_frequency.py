from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, validator
from metricheq.core.connectors.base import Connector
from metricheq.core.connectors.pagerduty import PagerDutyConnector
from metricheq.core.deducers.base import Deducer

from metricheq.core.deducers.utils import calculate_frequency

from .utils import INCIDENT_URGENCY_ALLOWED_VALUES


class PagerDutyIncidentFrequencyParams(BaseModel):
    service_id: str
    incident_urgency: Optional[str] = None
    since: Optional[datetime] = None
    until: Optional[datetime] = None

    time_unit: str = "daily"

    @validator("incident_urgency")
    def validate_incident_urgency(cls, v):
        if v not in INCIDENT_URGENCY_ALLOWED_VALUES:
            raise ValueError(
                f"Invalid incident_urgency: {v}. Must be one of {INCIDENT_URGENCY_ALLOWED_VALUES}"
            )
        return v


class PagerDutyIncidentFrequencyDeducer(Deducer):
    """
    Deducer class for calculating the frequency of incidents reported in PagerDuty.

    This class extends the Deducer base class and implements methods to fetch, process,
    and finalize data related to incident frequency. It calculates how often incidents occur
    over a given time frame, based on the specified frequency time unit (daily, weekly, monthly).

    Attributes:
        connector (Connector): A connector instance for making API requests to PagerDuty.
        params_model (PagerDutyIncidentFrequencyParams): Parameters for incident frequency extraction.

    Methods:
        retrieve_data: Retrieves incident data from PagerDuty.
        process_data: Processes the fetched data to count the number of incidents.
        finalize: Finalizes the data processing to calculate the incident frequency.
    """

    def __init__(self, connector: Connector, params: dict):
        if not isinstance(connector, PagerDutyConnector):
            raise TypeError("The provided connector is not a valid PagerDuty connector")
        self.params_model = PagerDutyIncidentFrequencyParams(**params)
        super().__init__(connector, params)

    def retrieve_data(self):
        endpoint = f"/incidents?service_ids[]={self.params_model.service_id}"

        if self.params_model.incident_urgency:
            endpoint += f"&urgencies[]={self.params_model.incident_urgency}"

        if self.params_model.since:
            endpoint += f"&since={self.params_model.since.isoformat()}"

        if self.params_model.until:
            endpoint += f"&until={self.params_model.until.isoformat()}"

        response = self.client.make_request(endpoint)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def process_data(self, data):
        incidents = data.get("incidents", [])
        return len(incidents)

    def finalize(self, processed_data):
        total_incidents = processed_data
        default_since = datetime.min.replace(tzinfo=timezone.utc)
        default_until = datetime.now(timezone.utc)

        since = self.params_model.since or default_since
        until = self.params_model.until or default_until

        time_delta = until - since
        return calculate_frequency(
            total_incidents, time_delta, self.params_model.time_unit
        )
