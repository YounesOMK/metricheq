from datetime import datetime, timedelta
import unittest
from unittest.mock import Mock, patch
from requests import HTTPError

from metricheq.core.connectors.pagerduty import PagerDutyConnector
from metricheq.core.deducers.pagerduty import (
    PagerDutyAVGIncidentResolutionTimeDeducer,
    PagerDutyAVGIncidentResolutionTimeParams,
)
from metricheq.core.deducers.utils import DurationFormat


class TestPagerDutyAVGIncidentResolutionTimeDeducer(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.mock_connector = Mock(spec=PagerDutyConnector, client=self.mock_client)

        self.params = {
            "service_id": "P8WTODX",
            "incident_urgency": "high",
            "format": DurationFormat.SECONDS,
            "since": datetime.utcnow() - timedelta(days=7),
            "until": datetime.utcnow(),
        }
        self.params_model = PagerDutyAVGIncidentResolutionTimeParams(**self.params)

        self.deducer = PagerDutyAVGIncidentResolutionTimeDeducer(
            self.mock_connector, self.params
        )

    def test_init_with_invalid_connector(self):
        with self.assertRaises(TypeError):
            invalid_connector = Mock()
            PagerDutyAVGIncidentResolutionTimeDeducer(invalid_connector, self.params)

    @patch("dateutil.parser.parse")
    def test_process_data(self, mock_parse):
        mock_data = {
            "incidents": [
                {
                    "status": "resolved",
                    "created_at": "2023-01-01T00:00:00Z",
                    "last_status_change_at": "2023-01-01T01:00:00Z",
                }
            ]
        }

        mock_parse.side_effect = [
            datetime(2023, 1, 1, 0, 0, 0),
            datetime(2023, 1, 1, 1, 0, 0),
        ]

        result = self.deducer.process_data(mock_data)
        self.assertEqual(result, 3600)

    def test_retrieve_data_successful(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "incidents": [
                {
                    "status": "resolved",
                    "created_at": "2023-01-01T00:00:00Z",
                    "last_status_change_at": "2023-01-01T01:00:00Z",
                }
            ]
        }
        self.mock_client.make_request.return_value = mock_response

        result = self.deducer.retrieve_data()
        self.assertIsNotNone(result)
        if result is not None:
            self.assertIn("incidents", result)

    def test_retrieve_data_failure(self):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = HTTPError("404 Client Error")

        self.mock_client.make_request.return_value = mock_response

        with self.assertRaises(HTTPError):
            self.deducer.retrieve_data()

    def test_finalize(self):
        test_duration_in_seconds = 3600
        self.deducer.params_model.format = DurationFormat.MINUTES
        result = self.deducer.finalize(test_duration_in_seconds)
        self.assertEqual(result, 60)

    def test_process_data_no_resolved_incidents(self):
        mock_data = {
            "incidents": [
                {
                    "status": "triggered",
                    "created_at": "2023-01-01T00:00:00Z",
                    "last_status_change_at": "2023-01-01T01:00:00Z",
                }
            ]
        }
        result = self.deducer.process_data(mock_data)
        self.assertIsNone(result)

    def test_finalize_with_none(self):
        result = self.deducer.finalize(None)
        self.assertIsNone(result)
