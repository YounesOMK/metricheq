## metricheq
[![codecov](https://codecov.io/gh/YounesOMK/metricheq/graph/badge.svg?token=UCFOOO5F69)](https://codecov.io/gh/YounesOMK/metricheq)
[![ci](https://github.com/YounesOMK/metricheq/actions/workflows/ci.yml/badge.svg)](https://github.com/YounesOMK/metricheq/actions/workflows/ci.yml)

This project currently offers three connectors:

- [Sonar](https://www.sonarqube.org/)
- [GitHub](https://github.com/)
- [PagerDuty](https://www.pagerduty.com/)


**Sonar Connector Example**

```python
# Import necessary classes and types
from metricheq.connectors.sonar import (
    SonarConnector,
    SonarTokenConfig,
    SonarUserPasswordConfig,
)
from metricheq.extractors.sonar import SonarMeasuresExtractor
from metricheq.evaluation.metric import Metric
from typing import Callable, List

# Define configuration for SonarQube connection using Token-based Authentication
# Note: If your SonarQube is behind a proxy, include the 'proxy' parameter in the configuration.
token_config = SonarTokenConfig(
    host_url="http://your-sonar-host.com",  # Replace with your SonarQube host URL
    user_token="your_token",               # Replace with your SonarQube user token
    # proxy="http://your-proxy-url.com"    # Uncomment and replace with your proxy URL if needed
)

# Alternatively, you can use Username and Password Authentication:
# user_pass_config = SonarUserPasswordConfig(
#     host_url="http://your-sonar-host.com",  # Replace with your SonarQube host URL
#     username="your_username",               # Replace with your SonarQube username
#     password="your_password"                # Replace with your SonarQube password
# )

# Choose the configuration type you want to use
config = token_config
# config = user_pass_config  # Uncomment to use Username and Password Authentication

# Create SonarConnector instance
sonar_connector = SonarConnector.from_config(config)

# Define parameters for fetching measures
params = {"component": "your_project_key", "metric_key": "code_smells"}

# Create an instance to extract SonarQube measures
measures_extractor = SonarMeasuresExtractor(sonar_connector, params)

# Fetch metric data (Example: Code Smells)
metric_data = measures_extractor.perform()

# Define a criterion function
def is_below_threshold(metric: Metric, threshold: int) -> bool:
    return metric.value is not None and metric.value < threshold

# Check if the fetched metric satisfies the given criterion
metric = Metric(value=metric_data)
threshold = 10  # Define your threshold value

if metric.satisfies(lambda x: is_below_threshold(x, threshold)):
    print("The metric satisfies the criterion: below the threshold.")
else:
    print("The metric does not satisfy the criterion.")
```
