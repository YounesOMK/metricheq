from datetime import timedelta
import unittest

from metricheq.core.deducers.utils import (
    calculate_frequency,
    convert_seconds,
)


class TestDurationFormat(unittest.TestCase):
    def test_convert_seconds_from_seconds(self):
        self.assertEqual(convert_seconds(120, "seconds"), 120)

    def test_convert_seconds_from_minutes(self):
        self.assertEqual(convert_seconds(120, "minutes"), 2)

    def test_convert_seconds_from_hours(self):
        self.assertEqual(convert_seconds(3600, "hours"), 1)


class TestCalculateFrequency(unittest.TestCase):
    def test_calculate_frequency_daily(self):
        total_events = 14
        time_delta = timedelta(days=7)
        frequency = calculate_frequency(total_events, time_delta, "daily")
        self.assertEqual(frequency, 2)

    def test_calculate_frequency_weekly(self):
        total_events = 8
        time_delta = timedelta(days=28)
        frequency = calculate_frequency(total_events, time_delta, "weekly")
        self.assertEqual(frequency, 2)

    def test_calculate_frequency_monthly(self):
        total_events = 30
        time_delta = timedelta(days=90)
        frequency = calculate_frequency(total_events, time_delta, "monthly")
        self.assertAlmostEqual(frequency, 10)

    def test_calculate_frequency_zero_days(self):
        total_events = 5
        time_delta = timedelta(days=0)
        frequency = calculate_frequency(total_events, time_delta, "daily")
        self.assertEqual(frequency, 5)

    def test_calculate_frequency_large_number_of_events(self):
        total_events = 1000
        time_delta = timedelta(days=100)
        frequency = calculate_frequency(total_events, time_delta, "daily")
        self.assertEqual(frequency, 10)

    def test_calculate_frequency_no_events(self):
        total_events = 0
        time_delta = timedelta(days=30)
        frequency = calculate_frequency(total_events, time_delta, "daily")
        self.assertEqual(frequency, 0)
