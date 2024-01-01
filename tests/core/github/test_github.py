import unittest
from unittest.mock import Mock, patch

import requests

from metricheq.core.connectors.git_providers.github import (
    GitHubClient,
    GitHubConfig,
    GitHubConnector,
)


class TestGitHubClient(unittest.TestCase):
    def setUp(self):
        self.config = GitHubConfig(api_key="test_api_key")

    def test_initialization(self):
        client = GitHubClient(self.config)
        self.assertEqual(client.base_url, "https://api.github.com")
        self.assertIsNotNone(client.authenticator)

    @patch("requests.Session.send")
    def test_make_request(self, mock_send):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_send.return_value = mock_response

        client = GitHubClient(self.config)
        response = client.make_request("/test")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"data": "test"})


class TestGitHubConnector(unittest.TestCase):
    def setUp(self):
        self.config = GitHubConfig(api_key="test_api_key")

    @patch("metricheq.core.connectors.git_providers.github.GitHubClient")
    def test_connector_initialization(self, mock_client):
        connector = GitHubConnector.from_config(self.config)
        self.assertIsInstance(connector, GitHubConnector)

    @patch("metricheq.core.connectors.git_providers.github.GitHubClient.make_request")
    def test_ensure_connectivity(self, mock_make_request):
        mock_make_request.return_value.status_code = 200
        connector = GitHubConnector.from_config(self.config)

        connector.ensure_connectivity()

    @patch("metricheq.core.connectors.git_providers.github.GitHubClient.make_request")
    def test_ensure_connectivity_failure(self, mock_make_request):
        mock_make_request.side_effect = requests.RequestException

        connector = GitHubConnector.from_config(self.config)

        with self.assertRaises(ConnectionError):
            connector.ensure_connectivity()
