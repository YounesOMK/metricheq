from datetime import datetime, timezone
import requests
from metricheq.fetchers.git_providers.base import (
    GitProviderFileExistsFetcher,
    GitProviderLastCommitFreshnessFetcher,
    GitProviderLastWorkFlowDurationFetcher,
)
from metricheq.fetchers.utils import DurationFormat


class GitHubFileExistsFetcher(GitProviderFileExistsFetcher):
    def fetch_data(self):
        endpoint = f"/repos/{self.params_model.repo_name}/contents/{self.params_model.file_path}"
        return self.client.make_request(endpoint)

    def process_data(self, response):
        return response.status_code == 200

    def finalize(self, file_exists) -> bool:
        return file_exists


class GitHubLastWorkFlowDurationFetcher(GitProviderLastWorkFlowDurationFetcher):
    def fetch_data(self):
        endpoint = f"/repos/{self.params_model.repo_name}/actions/runs"
        return self.client.make_request(endpoint)

    def process_data(self, response):
        if response.status_code == 200:
            runs = response.json().get("workflow_runs", [])
            if runs:
                latest_run = runs[0]
                start_time_str = latest_run["run_started_at"].replace("Z", "+00:00")
                end_time_str = latest_run["updated_at"].replace("Z", "+00:00")

                start_time = datetime.fromisoformat(start_time_str)
                end_time = datetime.fromisoformat(end_time_str)

                return (end_time - start_time).total_seconds()
            return None
        else:
            response.raise_for_status()

    def finalize(self, duration_in_seconds: float):
        if self.params_model.format == DurationFormat.SECONDS:
            return duration_in_seconds
        elif self.params_model.format == DurationFormat.MINUTES:
            return duration_in_seconds / 60
        elif self.params_model.format == DurationFormat.HOURS:
            return duration_in_seconds / 3600
        else:
            raise ValueError("Invalid duration format")


class GitHubLastCommitFreshnessFetcher(GitProviderLastCommitFreshnessFetcher):
    def fetch_data(self):
        endpoint = f"/repos/{self.params_model.repo_name}/commits/{self.params_model.branch_name}"
        return self.client.make_request(endpoint)

    def process_data(self, response):
        if response.status_code == 200:
            commit_data = response.json()
            commit_time_str = commit_data["commit"]["committer"]["date"]
            commit_time_str = commit_time_str.replace("Z", "+00:00")
            commit_time = datetime.fromisoformat(commit_time_str)
            return commit_time
        else:
            response.raise_for_status()

    def finalize(self, commit_time: datetime):
        current_time = datetime.now(timezone.utc)
        time_elapsed = current_time - commit_time
        return time_elapsed.total_seconds()
