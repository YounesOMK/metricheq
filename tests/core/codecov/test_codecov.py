import unittest
from unittest.mock import Mock, patch

from requests import RequestException
from metricheq.core.authenticators import BearerTokenAuthenticator

from metricheq.core.connectors.codecov import (
    CodecovClient,
    CodecovConfig,
    CodecovConnector,
)


class TestCodecovClient(unittest.TestCase):
    def setUp(self):
        self.config = CodecovConfig(api_token="test_api_token")

    def test_init(self):
        client = CodecovClient(self.config)
        self.assertIsInstance(client.authenticator, BearerTokenAuthenticator)

    @patch("requests.Session.send")
    def test_make_request_success(self, mock_send):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_send.return_value = mock_response

        client = CodecovClient(self.config)
        response = client.make_request("/test_endpoint")

        self.assertEqual(response.status_code, 200)

    @patch("requests.Session.send")
    def test_make_request_failure(self, mock_send):
        mock_send.side_effect = RequestException("Connection error")

        client = CodecovClient(self.config)

        with self.assertRaises(RequestException):
            client.make_request("/test_endpoint")


class TestCodecovConnector(unittest.TestCase):
    def setUp(self):
        self.config = CodecovConfig(api_token="test_api_token")

    @patch("metricheq.core.connectors.codecov.CodecovClient")
    def test_connector_initialization(self, mock_client):
        connector = CodecovConnector.from_config(self.config)
        self.assertIsInstance(connector, CodecovConnector)

    @patch("metricheq.core.connectors.codecov.CodecovClient")
    def test_ensure_connectivity_success(self, mock_client):
        mock_client_instance = mock_client.return_value
        mock_response = Mock()
        mock_response.status_code = 200
        mock_client_instance.make_request.return_value = mock_response

        connector = CodecovConnector(mock_client_instance)
        self.assertTrue(connector.ensure_connectivity())

    @patch("metricheq.core.connectors.codecov.CodecovClient")
    def test_ensure_connectivity_failure(self, mock_client):
        mock_client_instance = mock_client.return_value
        mock_response = Mock()
        mock_response.status_code = 404
        mock_client_instance.make_request.return_value = mock_response

        connector = CodecovConnector(mock_client_instance)
        with self.assertRaises(ConnectionError):
            connector.ensure_connectivity()

    @patch("metricheq.core.connectors.codecov.CodecovClient")
    def test_ensure_connectivity_request_exception(self, mock_client):
        mock_client_instance = mock_client.return_value
        mock_client_instance.make_request.side_effect = RequestException

        connector = CodecovConnector(mock_client_instance)
        with self.assertRaises(ConnectionError):
            connector.ensure_connectivity()
