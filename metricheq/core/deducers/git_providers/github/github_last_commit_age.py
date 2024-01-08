from datetime import datetime, timezone
from metricheq.core.deducers.git_providers.base import GitProviderLastCommitAgeDeducer
from metricheq.core.deducers.utils import convert_seconds


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
