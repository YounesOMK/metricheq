import unittest
from unittest.mock import Mock, patch

import requests
from metricheq.core.connectors.base import (
    BearerTokenAuthenticator,
    UserPasswordBasicAuthenticator,
)
from metricheq.core.connectors.sonar import (
    SonarClient,
    SonarConnector,
    SonarTokenConfig,
    SonarUserPasswordConfig,
)
from metricheq.exceptions.exceptions import UnsupportedConfigurationError


class TestSonarClient(unittest.TestCase):
    def test_init_with_token_config(self):
        token_config = SonarTokenConfig(
            host_url="http://example.com", user_token="abcd1234"
        )

        client = SonarClient(token_config)

        self.assertIsInstance(client.authenticator, BearerTokenAuthenticator)

    def test_init_with_user_password_config(self):
        user_password_config = SonarUserPasswordConfig(
            host_url="http://example.com", username="younes", password="1234"
        )

        client = SonarClient(user_password_config)
        self.assertIsInstance(client.authenticator, UserPasswordBasicAuthenticator)

    def test_with_unsupported_config(self):
        with self.assertRaises(UnsupportedConfigurationError):
            SonarClient({})

    @patch("requests.Session.send")
    def test_make_request_success(self, mock_send):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_send.return_value = mock_response

        config = SonarTokenConfig(host_url="http://example.com", user_token="token123")
        client = SonarClient(config)
        response = client.make_request("/api/test")

        self.assertEqual(response.status_code, 200)


class TestSonarConnector(unittest.TestCase):
    @patch("metricheq.core.connectors.sonar.SonarClient")
    def test_connector_initialization(self, mock_client):
        connector = SonarConnector.from_config({})
        self.assertIsInstance(connector, SonarConnector)

    @patch("metricheq.core.connectors.sonar.SonarClient")
    def test_ensure_connectivity(self, mock_client):
        mock_client_instance = mock_client.return_value
        mock_client_instance.make_request.return_value.json.return_value = {
            "health": "GREEN"
        }

        connector = SonarConnector(mock_client_instance)
        self.assertTrue(connector.ensure_connectivity())

    @patch("metricheq.core.connectors.sonar.SonarClient")
    def test_connectivity_with_unhealthy_response(self, mock_client):
        mock_client_instance = mock_client.return_value
        mock_client_instance.make_request.return_value.json.return_value = {
            "health": "RED"
        }

        connector = SonarConnector(mock_client_instance)
        with self.assertRaises(Exception):
            connector.ensure_connectivity()

    @patch("metricheq.core.connectors.sonar.SonarClient")
    def test_connectivity_with_request_exception(self, mock_client):
        mock_client_instance = mock_client.return_value
        mock_client_instance.make_request.side_effect = requests.RequestException

        connector = SonarConnector(mock_client_instance)
        with self.assertRaises(ConnectionError):
            connector.ensure_connectivity()

    @patch("metricheq.core.connectors.sonar.SonarClient")
    def test_method_calls_with_mocks(self, mock_client):
        mock_client_instance = mock_client.return_value
        mock_client_instance.make_request.return_value.json.return_value = {
            "health": "GREEN"
        }

        connector = SonarConnector(mock_client_instance)
        connector.ensure_connectivity()

        mock_client_instance.make_request.assert_called_once_with("/api/system/health")
