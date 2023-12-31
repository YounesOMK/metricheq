from datetime import datetime, timedelta, timezone
import unittest
from unittest.mock import Mock

from metricheq.core.connectors.git_providers.github import GitHubClient, GitHubConnector
from metricheq.core.deducers.git_providers.base import (
    GitProviderLastCommitFreshnessParams,
)
from metricheq.core.deducers.git_providers.github import GitHubLastCommitAgeDeducer


class TestGitHubLastCommitAgeDeducer(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock(spec=GitHubClient)
        self.mock_connector = Mock(spec=GitHubConnector, client=self.mock_client)

        self.params = {
            "repo_name": "test_repo",
            "branch_name": "main",
            "format": "minutes",
        }
        self.params_model = GitProviderLastCommitFreshnessParams(**self.params)

        self.deducer = GitHubLastCommitAgeDeducer(self.mock_connector, self.params)

    def test_retrieve_data_successful(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "commit": {"committer": {"date": "2023-01-01T00:00:00Z"}}
        }
        self.mock_client.make_request.return_value = mock_response

        result = self.deducer.retrieve_data()
        # TODO CHECK this later
        if result is not None:
            self.assertIn("commit", result)
        else:
            self.fail("retrieve_data returned None")

    def test_retrieve_data_failure(self):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("404 Client Error")
        self.mock_client.make_request.return_value = mock_response

        with self.assertRaises(Exception):
            self.deducer.retrieve_data()

    def test_process_data(self):
        commit_time_str = (
            datetime.now(timezone.utc) - timedelta(minutes=30)
        ).isoformat()
        mock_data = {"commit": {"committer": {"date": commit_time_str}}}

        result = self.deducer.process_data(mock_data)
        self.assertAlmostEqual(result, 30 * 60, delta=5)

    def test_finalize(self):
        time_elapsed_in_seconds = 1800
        result = self.deducer.finalize(time_elapsed_in_seconds)
        self.assertEqual(result, 30)
