from datetime import datetime, timezone
from metricheq.extractors.git_providers.base import (
    GitProviderFileExistsExtractor,
    GitProviderLastCommitFreshnessExtractor,
    GitProviderLastWorkFlowDurationExtractor,
)
from metricheq.extractors.utils import convert_seconds


class GitHubFileExistsExtractor(GitProviderFileExistsExtractor):
    def fetch_data(self):
        endpoint = f"/repos/{self.params_model.repo_name}/contents/{self.params_model.file_path}"
        return self.client.make_request(endpoint)

    def process_data(self, response):
        return response.status_code == 200

    def finalize(self, file_exists) -> bool:
        return file_exists


class GitHubLastWorkFlowDurationExtractor(GitProviderLastWorkFlowDurationExtractor):
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
        return convert_seconds(duration_in_seconds, self.params_model.format)


class GitHubLastCommitFreshnessExtractor(GitProviderLastCommitFreshnessExtractor):
    def fetch_data(self):
        endpoint = f"/repos/{self.params_model.repo_name}/commits/{self.params_model.branch_name}"
        return self.client.make_request(endpoint)

    def process_data(self, response):
        if response.status_code == 200:
            commit_data = response.json()
            commit_time_str = commit_data["commit"]["committer"]["date"]
            commit_time_str = commit_time_str.replace("Z", "+00:00")
            commit_time = datetime.fromisoformat(commit_time_str)
            time_elapsed_in_seconds = (
                datetime.now(timezone.utc) - commit_time
            ).total_seconds()
            return time_elapsed_in_seconds
        else:
            response.raise_for_status()

    def finalize(self, time_elapsed_in_seconds):
        return convert_seconds(time_elapsed_in_seconds, self.params_model.format)
