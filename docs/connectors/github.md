## Configuration

```python
from metricheq.core.connectors.github import GitHubConfig
from metricheq.core.connectors.github import GitHubConnector

config = GitHubConfig(api_key="your_api_key_here")
```

## Creating a Connector Instance

With the configuration ready, you can create a GitHubConnector instance:

```python
connector = GitHubConnector.from_config(config)
```

## Available Deducers

- [GitHubFileExistenceDeducer](../deducers/github/github_file_existence_deducer.md)
- [GitHubLastWorkFlowDurationDeducer](../deducers/github/github_last_workflow_duration_deducer.md)
- [GitHubLastCommitAgeDeducer](../deducers/github/github_last_commit_age_deducer.md)