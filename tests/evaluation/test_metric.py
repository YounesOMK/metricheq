import unittest

from metricheq.evaluation.metric import Metric


class TestMetric(unittest.TestCase):
    @staticmethod
    def criterion_greater_than_five(m):
        return m.value > 5

    @staticmethod
    def criterion_less_than_four(m):
        return m.value < 4

    @staticmethod
    def criterion_is_true(m):
        return m.value is True

    @staticmethod
    def criterion_is_not_none(m):
        return m.value is not None

    def test_satisfies_with_int(self):
        metric = Metric(value=10)
        self.assertTrue(metric.satisfies(self.criterion_greater_than_five))

    def test_satisfies_with_float(self):
        metric = Metric(value=3.14)
        self.assertTrue(metric.satisfies(self.criterion_less_than_four))

    def test_satisfies_with_bool(self):
        metric = Metric(value=True)
        self.assertTrue(metric.satisfies(self.criterion_is_true))

    def test_satisfies_with_none(self):
        metric = Metric(value=None)
        self.assertFalse(metric.satisfies(self.criterion_is_not_none))

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
