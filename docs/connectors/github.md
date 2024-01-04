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