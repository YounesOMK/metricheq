import unittest
from unittest.mock import Mock

from metricheq.connectors.sonar import SonarConnector
from metricheq.extractors.sonar import SonarMeasuresExtractor, SonarMetricType


class TestSonarMeasuresExtractor(unittest.TestCase):
    def setUp(self):
        self.mock_connector = Mock(spec=SonarConnector)
        self.mock_connector.client = Mock()
        self.params = {"component": "my_component", "metric_key": SonarMetricType.BUGS}

    def test_initialization(self):
        extractor = SonarMeasuresExtractor(self.mock_connector, self.params)
        self.assertIsInstance(extractor, SonarMeasuresExtractor)

    # TODO: MORE TESTS
