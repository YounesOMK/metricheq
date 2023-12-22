import unittest
from unittest.mock import Mock, patch

from metricheq.connectors.git_providers.github import GitHubConnector
from metricheq.extractors.git_providers.github import (
    GitHubLastWorkFlowDurationExtractor,
)


class TestGitHubLastWorkFlowDurationExtractor(unittest.TestCase):
    def setUp(self):
        self.mock_connector = Mock(spec=GitHubConnector)
        self.mock_client = Mock()
        self.mock_connector.client = self.mock_client
        self.params = {"repo_name": "test_repo", "format": "minutes"}
        self.extractor = GitHubLastWorkFlowDurationExtractor(
            self.mock_connector, self.params
        )

    def test_fetch_data(self):
        self.extractor.fetch_data()
        expected_endpoint = "/repos/test_repo/actions/runs"
        self.mock_client.make_request.assert_called_with(expected_endpoint)

    def test_process_data_valid_response(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "workflow_runs": [
                {
                    "run_started_at": "2023-01-01T00:00:00Z",
                    "updated_at": "2023-01-01T00:30:00Z",
                }
            ]
        }
        result = self.extractor.process_data(mock_response)
        self.assertEqual(result, 1800)

    def test_process_data_no_runs(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"workflow_runs": []}
        result = self.extractor.process_data(mock_response)
        self.assertIsNone(result)

    def test_process_data_non_200(self):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("404 Client Error")

        with self.assertRaises(Exception) as context:
            self.extractor.process_data(mock_response)

        self.assertTrue("404 Client Error" in str(context.exception))

    def test_finalize(self):
        duration_in_seconds = 1800
        result = self.extractor.finalize(duration_in_seconds)
        expected_result = 30
        self.assertEqual(result, expected_result)

    @patch(
        "metricheq.extractors.git_providers.github.GitHubLastWorkFlowDurationExtractor.process_data"
    )
    def test_perform(self, mock_process_data):
        mock_process_data.return_value = 1800
        mock_response = Mock()
        mock_response.status_code = 200
        self.mock_client.make_request.return_value = mock_response
        result = self.extractor.perform()
        self.assertEqual(result, 30)
