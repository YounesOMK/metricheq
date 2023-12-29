from datetime import datetime, timedelta, timezone
import unittest
from unittest.mock import Mock

from requests import HTTPError

from metricheq.connectors.pager_duty import PagerDutyConnector
from metricheq.deducers.pager_duty import (
    IncidentUrgencyEnum,
    PagerDutyIncidentFrequencyDeducer,
)
from metricheq.deducers.utils import FrequencyTimeUnit


class TestPagerDutyIncidentFrequencyDeducer(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.mock_connector = Mock(spec=PagerDutyConnector, client=self.mock_client)

        self.params = {
            "service_id": "example_service_id",
            "incident_urgency": IncidentUrgencyEnum.high,
            "since": datetime.now(timezone.utc) - timedelta(days=7),
            "until": datetime.now(timezone.utc),
            "time_unit": FrequencyTimeUnit.DAILY,
        }

        self.deducer = PagerDutyIncidentFrequencyDeducer(
            self.mock_connector, self.params
        )

    def test_init_with_invalid_connector(self):
        with self.assertRaises(TypeError):
            invalid_connector = Mock()
            PagerDutyIncidentFrequencyDeducer(invalid_connector, self.params)

    def test_retrieve_data_successful(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"incidents": [{"id": "1"}, {"id": "2"}]}
        self.mock_client.make_request.return_value = mock_response

        result = self.deducer.retrieve_data()
        self.assertIsNotNone(result)
        if result is not None:
            self.assertIn("incidents", result)
            self.assertEqual(len(result["incidents"]), 2)

    def test_retrieve_data_failure(self):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = HTTPError("404 Client Error")
        self.mock_client.make_request.return_value = mock_response

        with self.assertRaises(HTTPError):
            self.deducer.retrieve_data()

    def test_process_data(self):
        mock_data = {"incidents": [{"id": "1"}, {"id": "2"}]}
        result = self.deducer.process_data(mock_data)
        self.assertEqual(result, 2)

    def test_finalize_with_data(self):
        processed_data = 2
        result = self.deducer.finalize(processed_data)
        self.assertAlmostEqual(result, 2 / 7)

    def test_finalize_with_no_data(self):
        processed_data = 0
        result = self.deducer.finalize(processed_data)
        self.assertEqual(result, 0)
