## metricheq
[![codecov](https://codecov.io/gh/YounesOMK/metricheq/graph/badge.svg?token=UCFOOO5F69)](https://codecov.io/gh/YounesOMK/metricheq)
[![ci](https://github.com/YounesOMK/metricheq/actions/workflows/ci.yml/badge.svg)](https://github.com/YounesOMK/metricheq/actions/workflows/ci.yml)
![Mypy](https://img.shields.io/badge/mypy-checked-blue)

## Available connectors

| Connector  | Extractors                              | Description                                               |
|------------|-----------------------------------------|-----------------------------------------------------------|
| GitHub     | GitHubFileExistsExtractor               | Checks if a specified file exists in the repository.      |
|            | GitHubLastWorkFlowDurationExtractor     | Retrieves the duration of the last workflow run.          |
|            | GitHubLastCommitFreshnessExtractor      | Determines the freshness of the last commit.              |
| Sonar      | SonarMeasuresExtractor                  | Extracts various code quality metrics from SonarQube.     |

