import unittest
from unittest.mock import Mock, patch
from metricheq.connectors.git_providers.github import GitHubConnector

from metricheq.deducers.git_providers.github import (
    GitHubFileExistenceDeducer,
)


class TestGitHubFileExistenceDeducer(unittest.TestCase):
    def setUp(self):
        self.mock_connector = Mock(spec=GitHubConnector)
        self.mock_client = Mock()
        self.mock_connector.client = self.mock_client
        self.params = {"repo_name": "test_repo", "file_path": "test_file.py"}
        self.extractor = GitHubFileExistenceDeducer(self.mock_connector, self.params)

    def test_fetch_data(self):
        self.extractor.retrieve_data()
        expected_endpoint = "/repos/test_repo/contents/test_file.py"
        self.mock_client.make_request.assert_called_with(expected_endpoint)

    def test_process_data_valid_response(self):
        mock_response = Mock()
        mock_response.status_code = 200
        result = self.extractor.process_data(mock_response)
        self.assertTrue(result)

    def test_process_data_non_200(self):
        mock_response = Mock()
        mock_response.status_code = 404
        result = self.extractor.process_data(mock_response)
        self.assertFalse(result)

    def test_finalize(self):
        self.assertTrue(self.extractor.finalize(True))
        self.assertFalse(self.extractor.finalize(False))

    @patch(
        "metricheq.extractors.git_providers.github.GitHubFileExistsExtractor.process_data"
    )
    def test_perform(self, mock_process_data):
        mock_process_data.return_value = True
        mock_response = Mock()
        mock_response.status_code = 200
        self.mock_client.make_request.return_value = mock_response
        result = self.extractor.deduce()
        self.assertTrue(result)

        mock_process_data.return_value = False
        mock_response.status_code = 404
        self.mock_client.make_request.return_value = mock_response
        result = self.extractor.deduce()
        self.assertFalse(result)
