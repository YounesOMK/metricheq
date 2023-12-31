from pydantic import BaseModel
from metricheq.core.connectors.git_providers.github import GitHubConnector
from metricheq.core.deducers.base import Deducer
from metricheq.core.connectors.base import Connector


class GitProviderFileExistsParams(BaseModel):
    repo_name: str
    file_path: str


class GitProviderLastWorkflowDurationParams(BaseModel):
    repo_name: str
    format: str = "seconds"


class GitProviderLastCommitFreshnessParams(BaseModel):
    repo_name: str
    branch_name: str
    format: str = "seconds"


class GitProviderFileExistenceDeducer(Deducer):
    def __init__(self, connector: Connector, params: dict):
        if not isinstance(connector, GitHubConnector):
            raise TypeError("The provided connector is not a valid github connector")

        self.params_model = GitProviderFileExistsParams(**params)
        super().__init__(connector, params)


class GitProviderLastWorkFlowDurationDeducer(Deducer):
    def __init__(self, connector: Connector, params: dict):
        if not isinstance(connector, GitHubConnector):
            raise TypeError("The provided connector is not a valid github connector")
        self.params_model = GitProviderLastWorkflowDurationParams(**params)
        super().__init__(connector, params)


class GitProviderLastCommitAgeDeducer(Deducer):
    def __init__(self, connector: Connector, params: dict):
        if not isinstance(connector, GitHubConnector):
            raise TypeError("The provided connector is not a valid github connector")
        self.params_model = GitProviderLastCommitFreshnessParams(**params)
        super().__init__(connector, params)
