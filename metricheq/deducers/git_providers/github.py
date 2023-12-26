from datetime import datetime, timezone
from metricheq.deducers.git_providers.base import (
    GitProviderFileExistenceDeducer,
    GitProviderLastCommitAgeDeducer,
    GitProviderLastWorkFlowDurationDeducer,
)
from metricheq.deducers.utils import convert_seconds


class GitHubFileExistenceDeducer(GitProviderFileExistenceDeducer):
    def retrieve_data(self):
        endpoint = f"/repos/{self.params_model.repo_name}/contents/{self.params_model.file_path}"
        return self.client.make_request(endpoint)

    def process_data(self, response):
        return response.status_code == 200

    def finalize(self, file_exists) -> bool:
        return file_exists


class GitHubLastWorkFlowDurationDeducer(GitProviderLastWorkFlowDurationDeducer):
    def retrieve_data(self):
        endpoint = f"/repos/{self.params_model.repo_name}/actions/runs"
        response = self.client.make_request(endpoint)
        if response.status_code == 200:
            runs = response.json().get("workflow_runs", [])
            return runs
        else:
            response.raise_for_status()

    def process_data(self, data):
        runs = data
        if runs:
            latest_run = runs[0]
            start_time_str = latest_run["run_started_at"].replace("Z", "+00:00")
            end_time_str = latest_run["updated_at"].replace("Z", "+00:00")

            start_time = datetime.fromisoformat(start_time_str)
            end_time = datetime.fromisoformat(end_time_str)

            return (end_time - start_time).total_seconds()
        return None

    def finalize(self, duration_in_seconds: float):
        return convert_seconds(duration_in_seconds, self.params_model.format)


class GitHubLastCommitAgeDeducer(GitProviderLastCommitAgeDeducer):
    def retrieve_data(self):
        endpoint = f"/repos/{self.params_model.repo_name}/commits/{self.params_model.branch_name}"
        response = self.client.make_request(endpoint)
        if response.status_code == 200:
            commit_data = response.json()
            return commit_data
        else:
            response.raise_for_status()

    def process_data(self, data):
        commit_data = data
        commit_time_str = commit_data["commit"]["committer"]["date"]
        commit_time_str = commit_time_str.replace("Z", "+00:00")
        commit_time = datetime.fromisoformat(commit_time_str)
        time_elapsed_in_seconds = (
            datetime.now(timezone.utc) - commit_time
        ).total_seconds()
        return time_elapsed_in_seconds

    def finalize(self, time_elapsed_in_seconds):
        return convert_seconds(time_elapsed_in_seconds, self.params_model.format)
