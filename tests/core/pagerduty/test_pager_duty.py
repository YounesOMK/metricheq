import unittest
from unittest.mock import Mock, patch

from requests import RequestException
from metricheq.core.authenticators import TokenAuthenticator

from metricheq.core.connectors.pagerduty import (
    PagerDutyClient,
    PagerDutyConfig,
    PagerDutyConnector,
)


class TestPagerDutyClient(unittest.TestCase):
    def setUp(self):
        self.config = PagerDutyConfig(api_key="test_api_key")

    def test_init(self):
        client = PagerDutyClient(self.config)
        self.assertIsInstance(client.authenticator, TokenAuthenticator)

    @patch("requests.Session.send")
    def test_make_request_success(self, mock_send):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_send.return_value = mock_response

        client = PagerDutyClient(self.config)
        response = client.make_request("/test_endpoint")

        self.assertEqual(response.status_code, 200)

    @patch("requests.Session.send")
    def test_make_request_failure(self, mock_send):
        mock_send.side_effect = RequestException("Connection error")

        client = PagerDutyClient(self.config)

        with self.assertRaises(RequestException):
            client.make_request("/test_endpoint")


class TestPagerDutyConnector(unittest.TestCase):
    def setUp(self):
        self.config = PagerDutyConfig(api_key="test_api_key")

    @patch("metricheq.core.connectors.pagerduty.PagerDutyClient")
    def test_connector_initialization(self, mock_client):
        connector = PagerDutyConnector.from_config(self.config)
        self.assertIsInstance(connector, PagerDutyConnector)

    @patch("metricheq.core.connectors.pagerduty.PagerDutyClient")
    def test_ensure_connectivity_success(self, mock_client):
        mock_client_instance = mock_client.return_value
        mock_response = Mock()
        mock_response.status_code = 200
        mock_client_instance.make_request.return_value = mock_response

        connector = PagerDutyConnector(mock_client_instance)
        self.assertTrue(connector.ensure_connectivity())

    @patch("metricheq.core.connectors.pagerduty.PagerDutyClient")
    def test_ensure_connectivity_failure(self, mock_client):
        mock_client_instance = mock_client.return_value
        mock_response = Mock()
        mock_response.status_code = 404
        mock_client_instance.make_request.return_value = mock_response

        connector = PagerDutyConnector(mock_client_instance)
        with self.assertRaises(ConnectionError):
            connector.ensure_connectivity()

    @patch("metricheq.core.connectors.pagerduty.PagerDutyClient")
    def test_ensure_connectivity_request_exception(self, mock_client):
        mock_client_instance = mock_client.return_value
        mock_client_instance.make_request.side_effect = RequestException

        connector = PagerDutyConnector(mock_client_instance)
        with self.assertRaises(ConnectionError):
            connector.ensure_connectivity()
