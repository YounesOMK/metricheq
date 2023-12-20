from pydantic import BaseModel
from metricheq.fetchers.base import Fetcher
from metricheq.fetchers.utils import DurationFormat
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


class GitProviderFileExistsFetcher(Fetcher):
    def __init__(self, connector: Connector, params: dict):
        self.params_model = GitProviderFileExistsParams(**params)
        super().__init__(connector, params)

    @property
    def friendly_name(self):
        return "existence of file in git repository"



class GitProviderLastWorkFlowDurationFetcher(Fetcher):
    def __init__(self, connector: Connector, params: dict):
        self.params_model = GitProviderLastWorkflowDurationParams(**params)
        super().__init__(connector, params)

    @property
    def friendly_name(self):
        return "last Git workflow duration"


class GitProviderLastCommitFreshnessFetcher(Fetcher):
    def __init__(self, connector: Connector, params: dict):
        self.params_model = GitProviderLastCommitFreshnessParams(**params)
        super().__init__(connector, params)

    @property
    def friendly_name(self):
        return "freshness of last Git commit"
