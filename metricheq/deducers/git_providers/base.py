from pydantic import BaseModel
from metricheq.connectors.git_providers.github import GitHubConnector
from metricheq.deducers.base import Deducer
from metricheq.deducers.utils import DurationFormat
from metricheq.connectors.base import Connector


class GitProviderFileExistsParams(BaseModel):
    repo_name: str
    file_path: str


class GitProviderLastWorkflowDurationParams(BaseModel):
    repo_name: str
    format: DurationFormat = DurationFormat.SECONDS


class GitProviderLastCommitFreshnessParams(BaseModel):
    repo_name: str
    branch_name: str
    format: DurationFormat = DurationFormat.SECONDS


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
