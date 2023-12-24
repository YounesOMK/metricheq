from datetime import datetime, timedelta, timezone
import unittest
from unittest.mock import Mock

from metricheq.connectors.git_providers.github import GitHubClient, GitHubConnector
from metricheq.extractors.git_providers.base import GitProviderLastCommitFreshnessParams
from metricheq.extractors.git_providers.github import GitHubLastCommitFreshnessExtractor
from metricheq.extractors.utils import DurationFormat


class TestGitHubLastCommitFreshnessExtractor(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock(spec=GitHubClient)
        self.mock_connector = Mock(spec=GitHubConnector, client=self.mock_client)

        self.params = {
            "repo_name": "test_repo",
            "branch_name": "main",
            "format": DurationFormat.MINUTES,
        }
        self.params_model = GitProviderLastCommitFreshnessParams(**self.params)

        self.extractor = GitHubLastCommitFreshnessExtractor(
            self.mock_connector, self.params
        )

    def test_fetch_data_successful(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "commit": {"committer": {"date": "2023-01-01T00:00:00Z"}}
        }
        self.mock_client.make_request.return_value = mock_response

        result = self.extractor.fetch_data()
        # TODO CHECK this later
        if result is not None:
            self.assertIn("commit", result)
        else:
            self.fail("fetch_data returned None")

    def test_fetch_data_failure(self):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("404 Client Error")
        self.mock_client.make_request.return_value = mock_response

        with self.assertRaises(Exception):
            self.extractor.fetch_data()

    def test_process_data(self):
        commit_time_str = (
            datetime.now(timezone.utc) - timedelta(minutes=30)
        ).isoformat()
        mock_data = {"commit": {"committer": {"date": commit_time_str}}}

        result = self.extractor.process_data(mock_data)
        self.assertAlmostEqual(result, 30 * 60, delta=5)

    def test_finalize(self):
        time_elapsed_in_seconds = 1800
        result = self.extractor.finalize(time_elapsed_in_seconds)
        self.assertEqual(result, 30)
