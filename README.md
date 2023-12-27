## metricheq
[![codecov](https://codecov.io/gh/YounesOMK/metricheq/graph/badge.svg?token=UCFOOO5F69)](https://codecov.io/gh/YounesOMK/metricheq)
[![ci](https://github.com/YounesOMK/metricheq/actions/workflows/ci.yml/badge.svg)](https://github.com/YounesOMK/metricheq/actions/workflows/ci.yml)

This project currently offers 4 connectors:

✅ Completed \
🚧 In progress
    
| Connector  | Deducer                                         | Description                                       | Status |
|------------|-------------------------------------------------|---------------------------------------------------|:------:|
| Sonar      | SonarMeasureDeducer                             | Deduces metrics for coverage, bugs, vulnerabilities, code smells | ✅ |
| GitHub     | GitHubFileExistenceDeducer                      | Determines if a file exists in the repo           | ✅ |
|            | GitHubLastWorkFlowDurationDeducer               | Calculates duration of the last workflow          | ✅ |
|            | GitHubLastCommitAgeDeducer                      | Measures time since the last commit               | ✅ |
|            | GitHubPRTimeToMergeDeducer                      | Measures avg pr time to merge                      | 🚧 |
|            | GitHubIssueTimeToCloseDeducer                   | Measures  time taken to close issues                | 🚧 |
| GitLab     |                                                 |                                                     | 🚧 |
| BitBucket  |                                                 |                                                     | 🚧 |
| PagerDuty  | PagerDutyIncidentFrequencyDeducer               | Deducer for frequency of incidents                | ✅ |
|            | PagerDutyAverageIncidentResolutionTimeDeducer   | Calculates average resolution time of incidents   | ✅ |
|            | PagerDutyIncidentTimeToAcknowledgeDeducer       | Calculates average time to acknowldge incidents   | 🚧 |
| Prometheus | PrometheusServiceAvailabilityDeducer            | Determines the service uptime ratio over a specified period of time | ✅ |
| Jenkins    |                                                 |                                                    | 🚧 |

