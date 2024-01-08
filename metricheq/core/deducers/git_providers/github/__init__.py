from .github_file_existence import GitHubFileExistenceDeducer
from .github_last_commit_age import GitHubLastCommitAgeDeducer
from .github_last_work_flow_duration import GitHubLastWorkFlowDurationDeducer

__all__ = [
    "GitHubFileExistenceDeducer",
    "GitHubLastCommitAgeDeducer",
    "GitHubLastWorkFlowDurationDeducer",
]
