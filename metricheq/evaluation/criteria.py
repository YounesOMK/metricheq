from typing import Union
from metricheq.evaluation.models import Criterion, Metric


class BooleanTrue(Criterion):
    def is_satisfied_by(self, metric: Metric) -> bool:
        return metric.value is True


class BooleanFalse(Criterion):
    def is_satisfied_by(self, metric: Metric) -> bool:
        return metric.value is False


class NumericGreaterThan(Criterion):
    def __init__(self, threshold: Union[float, int]):
        self.threshold = threshold

    def is_satisfied_by(self, metric: Metric) -> bool:
        if isinstance(metric.value, bool):
            return False
        elif isinstance(metric.value, (float, int)):
            return metric.value > self.threshold
        return False

    def __str__(self):
        return f"> {self.threshold}"


class NumericLessThan(Criterion):
    def __init__(self, threshold: Union[float, int]):
        self.threshold = threshold

    def is_satisfied_by(self, metric: Metric) -> bool:
        if isinstance(metric.value, bool):
            return False
        elif isinstance(metric.value, (float, int)):
            return metric.value < self.threshold
        return False


class NumericEqualTo(Criterion):
    def __init__(self, value: float):
        self.value = value

    def is_satisfied_by(self, metric: Metric) -> bool:
        if isinstance(metric.value, (float, int)):
            return metric.value == self.value
        return False
