from datetime import datetime
from metricheq.core.deducers.git_providers.base import (
    GitProviderLastWorkFlowDurationDeducer,
)
from metricheq.core.deducers.utils import convert_seconds


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
