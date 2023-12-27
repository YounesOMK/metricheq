from datetime import datetime, timedelta
import unittest
from unittest.mock import Mock

from requests import HTTPError

from metricheq.connectors.prometheus import PrometheusConnector
from metricheq.deducers.prometheus import PrometheusServiceAvailabilityDeducer


class TestPrometheusServiceAvailabilityDeducer(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.mock_connector = Mock(spec=PrometheusConnector, client=self.mock_client)

        start_time = datetime.now() - timedelta(days=1)
        end_time = datetime.now()

        self.params = {
            "labels": {"job": "job_label"},
            "start_time": start_time,
            "end_time": end_time,
            "step": 60,
        }

        self.deducer = PrometheusServiceAvailabilityDeducer(
            self.mock_connector, self.params
        )

    def test_init_with_invalid_connector(self):
        with self.assertRaises(TypeError):
            invalid_connector = Mock()
            PrometheusServiceAvailabilityDeducer(invalid_connector, self.params)

    def test_retrieve_data_successful(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"result": []}}
        self.mock_client.make_request.return_value = mock_response

        result = self.deducer.retrieve_data()
        self.assertIsNotNone(result)

    def test_retrieve_data_failure(self):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = HTTPError("500 Server Error")
        self.mock_client.make_request.return_value = mock_response

        with self.assertRaises(HTTPError):
            self.deducer.retrieve_data()

    def test_process_data(self):
        mock_data = {
            "data": {"result": [{"values": [["timestamp", "1"], ["timestamp", "0"]]}]}
        }
        result = self.deducer.process_data(mock_data)
        expected_availability = (
            50.0  # Assuming one 'up' and one 'down' in the mock data
        )
        self.assertEqual(result, expected_availability)

    def test_finalize(self):
        processed_data = 75.0
        result = self.deducer.finalize(processed_data)
        self.assertEqual(result, processed_data)

    def test_deduce_integration(self):
        mock_retrieve_data = Mock(return_value={"data": {"result": []}})
        mock_process_data = Mock(return_value=100.0)
        mock_finalize = Mock(return_value=100.0)

        self.deducer.retrieve_data = mock_retrieve_data
        self.deducer.process_data = mock_process_data
        self.deducer.finalize = mock_finalize

        result = self.deducer.deduce()
        self.assertEqual(result, 100.0)
