import unittest
from unittest.mock import Mock

from metricheq.connectors.sonar import SonarClient, SonarConnector
from metricheq.extractors.sonar import (
    SonarMeasuresExtractor,
    SonarMeasuresParams,
    SonarMetricType,
)


class TestSonarMeasuresExtractor(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock(spec=SonarClient)
        self.mock_connector = Mock(spec=SonarConnector, client=self.mock_client)

        self.params = {
            "component": "example_component",
            "metric_key": SonarMetricType.COVERAGE,
        }
        self.params_model = SonarMeasuresParams(**self.params)

        self.extractor = SonarMeasuresExtractor(self.mock_connector, self.params)

    def test_fetch_data_successful(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "component": {"measures": [{"metric": "coverage", "value": "85.2"}]}
        }
        self.mock_client.make_request.return_value = mock_response

        result = self.extractor.fetch_data()
        if result is None:
            self.fail("fetch_data returned None")
        else:
            self.assertIn("component", result)

    def test_fetch_data_failure(self):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("404 Client Error")
        self.mock_client.make_request.return_value = mock_response

        with self.assertRaises(Exception):
            self.extractor.fetch_data()

    def test_process_data(self):
        mock_data = {
            "component": {"measures": [{"metric": "coverage", "value": "85.2"}]}
        }

        # Call process_data and verify the result
        result = self.extractor.process_data(mock_data)
        self.assertEqual(result, "85.2")

    def test_finalize(self):
        # Test finalize method
        processed_data = "85.2"
        result = self.extractor.finalize(processed_data)
        self.assertEqual(result, "85.2")
