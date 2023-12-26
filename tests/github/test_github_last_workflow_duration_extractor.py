from datetime import datetime
import unittest
from unittest.mock import Mock

from requests import Response
from requests import HTTPError

from metricheq.connectors.git_providers.github import GitHubClient, GitHubConnector
from metricheq.deducers.git_providers.base import (
    GitProviderLastWorkflowDurationParams,
)
from metricheq.deducers.git_providers.github import (
    GitHubLastWorkFlowDurationDeducer,
)
from metricheq.deducers.utils import DurationFormat


class TestGitHubLastWorkFlowDurationDeducer(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock(spec=GitHubClient)
        self.mock_connector = Mock(spec=GitHubConnector, client=self.mock_client)

        self.params = {"repo_name": "test_repo", "format": DurationFormat.MINUTES}
        self.params_model = GitProviderLastWorkflowDurationParams(**self.params)

        self.extractor = GitHubLastWorkFlowDurationDeducer(
            self.mock_connector, self.params
        )

    def test_fetch_data_successful(self):
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
        self.mock_client.make_request.return_value = mock_response

        result = self.extractor.retrieve_data()
        if result is not None:
            self.assertEqual(len(result), 1)
            self.assertIn("run_started_at", result[0])
        else:
            self.fail("fetch_data returned None")

    def test_fetch_data_failure(self):
        mock_response = Mock(spec=Response)
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = HTTPError("404 Client Error")

        self.mock_client.make_request.return_value = mock_response

        with self.assertRaises(HTTPError):
            self.extractor.retrieve_data()

    def test_process_data(self):
        mock_data = [
            {
                "run_started_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T01:00:00Z",
            }
        ]

        start_time = datetime.fromisoformat("2023-01-01T00:00:00+00:00")
        end_time = datetime.fromisoformat("2023-01-01T01:00:00+00:00")
        expected_duration = (end_time - start_time).total_seconds()

        result = self.extractor.process_data(mock_data)
        self.assertEqual(result, expected_duration)

    def test_finalize(self):
        test_duration_in_seconds = 3600
        result = self.extractor.finalize(test_duration_in_seconds)
        self.assertEqual(result, 60)
