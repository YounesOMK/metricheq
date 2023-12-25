import unittest

from metricheq.extractors.utils import DurationFormat, convert_seconds


class TestDurationFormat(unittest.TestCase):
    def test_convert_seconds_from_seconds(self):
        self.assertEqual(convert_seconds(120, DurationFormat.SECONDS), 120)

    def test_convert_seconds_from_minutes(self):
        self.assertEqual(convert_seconds(120, DurationFormat.MINUTES), 2)

    def test_convert_seconds_from_hours(self):
        self.assertEqual(convert_seconds(3600, DurationFormat.HOURS), 1)
