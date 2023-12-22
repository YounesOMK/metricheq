import unittest
from unittest.mock import Mock, patch

from metricheq.connectors.sonar import SonarConnector
from metricheq.extractors.sonar import SonarMeasuresExtractor, SonarMetricType


class TestSonarMeasuresExtractor(unittest.TestCase):
    def setUp(self):
        self.mock_connector = Mock(spec=SonarConnector)
        self.mock_client = Mock()
        self.mock_connector.client = self.mock_client
        self.mock_client.make_request = Mock()
        self.params = {
            "component": "test_component",
            "metric_key": SonarMetricType.COVERAGE,
        }

    def test_init_valid_connector(self):
        extractor = SonarMeasuresExtractor(self.mock_connector, self.params)
        self.assertIsInstance(extractor, SonarMeasuresExtractor)

    def test_init_invalid_connector(self):
        with self.assertRaises(TypeError):
            SonarMeasuresExtractor(Mock(), self.params)

    def test_fetch_data_exception_handling(self):
        self.mock_client.make_request.side_effect = Exception("Request failed")
        extractor = SonarMeasuresExtractor(self.mock_connector, self.params)
        with self.assertRaises(Exception):
            extractor.fetch_data()

    def test_fetch_data(self):
        extractor = SonarMeasuresExtractor(self.mock_connector, self.params)
        extractor.fetch_data()
        self.mock_connector.client.make_request.assert_called_with(
            "/api/measures/component?component=test_component&metricKeys=coverage"
        )

    def test_process_data_valid_response(self):
        mock_response = Mock()
        mock_response.json.return_value = {
            "component": {"measures": [{"metric": "coverage", "value": 80}]}
        }
        extractor = SonarMeasuresExtractor(self.mock_connector, self.params)
        result = extractor.process_data(mock_response)
        self.assertEqual(result, 80)

    @patch("metricheq.extractors.sonar.SonarMeasuresExtractor.process_data")
    def test_perform(self, mock_process_data):
        mock_process_data.return_value = 10
        extractor = SonarMeasuresExtractor(self.mock_connector, self.params)
        result = extractor.perform()
        self.assertEqual(result, 10)

    def test_finalize_method(self):
        extractor = SonarMeasuresExtractor(self.mock_connector, self.params)
        processed_data = "Some data"
        result = extractor.finalize(processed_data)
        self.assertEqual(result, processed_data)

    def test_ensure_connectivity_called(self):
        mock_response = Mock()
        mock_response.json.return_value = {
            "component": {"measures": [{"metric": "coverage", "value": "80"}]}
        }
        self.mock_client.make_request.return_value = mock_response

        with patch.object(
            self.mock_connector, "ensure_connectivity"
        ) as mock_ensure_connectivity:
            extractor = SonarMeasuresExtractor(self.mock_connector, self.params)
            extractor.perform()
            mock_ensure_connectivity.assert_called_once()
