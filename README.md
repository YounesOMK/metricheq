## metricheq
[![codecov](https://codecov.io/gh/YounesOMK/metricheq/graph/badge.svg?token=UCFOOO5F69)](https://codecov.io/gh/YounesOMK/metricheq)
[![ci](https://github.com/YounesOMK/metricheq/actions/workflows/ci.yml/badge.svg)](https://github.com/YounesOMK/metricheq/actions/workflows/ci.yml)

This project currently offers 4 connectors:

| Connector  | Deducer                                         | Description                                       |
|------------|-------------------------------------------------|---------------------------------------------------|
| Sonar      | SonarMeasureDeducer                             | Deduces metrics for coverage, bugs, vulnerabilities, code smells |
| GitHub     | GitHubFileExistenceDeducer                      | Determines if a file exists in the repo           |
|            | GitHubLastWorkFlowDurationDeducer               | Calculates duration of the last workflow          |
|            | GitHubLastCommitAgeDeducer                      | Measures time since the last commit               |
| PagerDuty  | PagerDutyIncidentFrequencyDeducer               | Deducer for frequency of incidents                |
|            | PagerDutyAverageIncidentResolutionTimeDeducer   | Calculates average resolution time of incidents   |
| Prometheus | PrometheusServiceAvailabilityDeducer            | determines the service uptime ratio over a specified period of time|



