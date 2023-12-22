import unittest

from metricheq.evaluation.metric import Metric


class TestMetric(unittest.TestCase):
    def test_satisfies_with_int(self):
        metric = Metric(value=10)
        criterion = lambda m: m.value > 5
        self.assertTrue(metric.satisfies(criterion))

    def test_satisfies_with_float(self):
        metric = Metric(value=3.14)
        criterion = lambda m: m.value < 4
        self.assertTrue(metric.satisfies(criterion))

    def test_satisfies_with_bool(self):
        metric = Metric(value=True)
        criterion = lambda m: m.value is True
        self.assertTrue(metric.satisfies(criterion))

    def test_satisfies_with_none(self):
        metric = Metric(value=None)
        criterion = lambda m: m.value is not None
        self.assertFalse(metric.satisfies(criterion))

    def test_satisfies_all_with_multiple_criteria(self):
        metric = Metric(value=7)
        criteria = [lambda m: m.value > 5, lambda m: m.value < 10]
        self.assertTrue(metric.satisfies_all(criteria))

    def test_satisfies_all_with_failing_criteria(self):
        metric = Metric(value=2)
        criteria = [lambda m: m.value > 1, lambda m: m.value < 2]
        self.assertFalse(metric.satisfies_all(criteria))

    def test_satisfies_all_with_no_value(self):
        metric = Metric(value=None)
        criteria = [lambda m: m.value > 0]
        self.assertFalse(metric.satisfies_all(criteria))

    def test_satisfies_all_with_empty_criteria(self):
        metric = Metric(value=10)
        self.assertTrue(metric.satisfies_all([]))

    def test_satisfies_all_no_side_effects(self):
        metric = Metric(value=5)
        original_value = metric.value
        criteria = [lambda m: m.value > 0]
        metric.satisfies_all(criteria)
        self.assertEqual(metric.value, original_value)
