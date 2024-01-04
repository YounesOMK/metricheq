# Welcome to Metricheq

A tool that simplifies gathering SRE metrics from various services.

## Incident frequency Example

```python
def is_above_threshold(metric: Metric):
    threshold = 10  
    return metric.value >= threshold

config = PagerDutyConfig(api_key="somekey")
pagerduty_connector = PagerDutyConnector.from_config(config)

params = {
    "service_id": "P8WTODX",
    "incident_urgency": "high",
    "since": datetime.utcnow() - timedelta(days=7),
    "until": datetime.utcnow(),
}

deducer = PagerDutyIncidentFrequencyDeducer(pagerduty_connector, params)
result = deducer.metric.satisfies(is_above_threshold)
```