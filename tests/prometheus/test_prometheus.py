import unittest
from unittest.mock import Mock, patch

from requests import RequestException

from metricheq.connectors.prometheus import (
    PrometheusClient,
    PrometheusConfig,
    PrometheusConnector,
    PrometheusUserPasswordConfig,
)
from metricheq.exceptions.exceptions import UnsupportedConfigurationError


class TestPrometheusClient(unittest.TestCase):
    def test_init_with_base_config(self):
        config = PrometheusConfig(host_url="http://example.com")
        client = PrometheusClient(config)
        self.assertIsNone(client.authenticator)

    def test_init_with_user_password_config(self):
        user_password_config = PrometheusUserPasswordConfig(
            host_url="http://example.com", username="younes", password="1234"
        )
        client = PrometheusClient(user_password_config)
        self.assertIsNotNone(client.authenticator)

    def test_with_unsupported_config(self):
        with self.assertRaises(UnsupportedConfigurationError):
            PrometheusClient({})

    @patch("requests.Session.send")
    def test_make_request_success(self, mock_send):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_send.return_value = mock_response

        config = PrometheusConfig(host_url="http://example.com")
        client = PrometheusClient(config)
        response = client.make_request("query")

        self.assertEqual(response.status_code, 200)


class TestPrometheusConnector(unittest.TestCase):
    @patch("metricheq.connectors.prometheus.PrometheusClient")
    def test_connector_initialization(self, mock_client):
        connector = PrometheusConnector.from_config({})
        self.assertIsInstance(connector, PrometheusConnector)

    @patch("metricheq.connectors.prometheus.PrometheusClient")
    def test_ensure_connectivity(self, mock_client):
        mock_client_instance = mock_client.return_value
        mock_response = Mock()
        mock_response.status_code = 200
        mock_client_instance.make_request.return_value = mock_response

        connector = PrometheusConnector(mock_client_instance)
        self.assertTrue(connector.ensure_connectivity())

    @patch("metricheq.connectors.prometheus.PrometheusClient")
    def test_connectivity_with_failure_response(self, mock_client):
        mock_client_instance = mock_client.return_value
        mock_response = Mock()
        mock_response.status_code = 500
        mock_client_instance.make_request.return_value = mock_response

        connector = PrometheusConnector(mock_client_instance)
        with self.assertRaises(ConnectionError):
            connector.ensure_connectivity()

    @patch("metricheq.connectors.prometheus.PrometheusClient")
    def test_connectivity_with_request_exception(self, mock_client):
        mock_client_instance = mock_client.return_value
        mock_client_instance.make_request.side_effect = RequestException

        connector = PrometheusConnector(mock_client_instance)
        with self.assertRaises(ConnectionError):
            connector.ensure_connectivity()
