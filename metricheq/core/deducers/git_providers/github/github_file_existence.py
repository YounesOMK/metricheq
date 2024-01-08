from metricheq.core.deducers.git_providers.base import GitProviderFileExistenceDeducer


class GitHubFileExistenceDeducer(GitProviderFileExistenceDeducer):
    def retrieve_data(self):
        endpoint = f"/repos/{self.params_model.repo_name}/contents/{self.params_model.file_path}"
        return self.client.make_request(endpoint)

    def process_data(self, response):
        return response.status_code == 200

    def finalize(self, file_exists) -> bool:
        return file_exists
