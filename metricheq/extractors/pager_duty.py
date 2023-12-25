from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel
from dateutil.parser import parse
from metricheq.connectors.base import Connector
from metricheq.connectors.pager_duty import PagerDutyConnector

from metricheq.extractors.base import Extractor
from metricheq.extractors.utils import DurationFormat, convert_seconds


class IncidentUrgencyEnum(str, Enum):
    """
    Enum for defining incident urgency levels in PagerDuty.
    """

    high = "high"
    low = "low"


class PagerDutyAverageIncidentResolutionTimeParams(BaseModel):
    """
    Parameter model for configuring the PagerDutyAverageIncidentResolutionTimeExtractor.

    Attributes:
        service_id (str): The ID of the PagerDuty service to query.
        incident_urgency (IncidentUrgencyEnum): The urgency level of the incidents to consider.
        format (DurationFormat): The format for representing time duration (seconds, minutes, etc.).
        since (Optional[datetime]): The start time for the incident query window.
        until (Optional[datetime]): The end time for the incident query window.
    """

    service_id: str
    incident_urgency: IncidentUrgencyEnum
    format: DurationFormat = DurationFormat.SECONDS

    since: Optional[datetime] = None
    until: Optional[datetime] = None


class PagerDutyAverageIncidentResolutionTimeExtractor(Extractor):
    """
    Extractor for calculating the average time to resolution of incidents in PagerDuty.

    This extractor fetches incident data from PagerDuty and calculates the average time taken from when incidents are reported until they are resolved.

    Attributes:
        connector (Connector): A connector instance for making API requests to PagerDuty.
        params_model (PagerDutyAverageIncidentResolutionTimeParams): Parameters for incident data extraction.
    """

    def __init__(self, connector: Connector, params: dict):
        if not isinstance(connector, PagerDutyConnector):
            raise TypeError(
                "The provided connector is not a valid pager duty connector"
            )
        self.params_model = PagerDutyAverageIncidentResolutionTimeParams(**params)
        super().__init__(connector, params)

    def fetch_data(self):
        endpoint = f"/incidents?service_ids[]={self.params_model.service_id}&urgencies[]={self.params_model.incident_urgency.value}"

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
        total_time_to_resolution = 0
        count = 0
        for incident in incidents:
            if incident["status"] == "resolved":
                created_at = parse(incident["created_at"])
                resolved_at = parse(incident["last_status_change_at"])
                time_to_resolution = (resolved_at - created_at).total_seconds()
                total_time_to_resolution += time_to_resolution
                count += 1

        if count == 0:
            return None

        average_time_to_resolution = total_time_to_resolution / count
        return average_time_to_resolution

    def finalize(self, processed_data):
        if processed_data is not None:
            return convert_seconds(processed_data, format=self.params_model.format)
        return None
