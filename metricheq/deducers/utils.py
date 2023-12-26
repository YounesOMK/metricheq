from datetime import timedelta
from enum import Enum


class DurationFormat(str, Enum):
    SECONDS = "seconds"
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"


class FrequencyTimeUnit(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


def convert_seconds(duration_in_seconds, format: DurationFormat):
    if format == DurationFormat.SECONDS:
        return duration_in_seconds
    elif format == DurationFormat.MINUTES:
        return duration_in_seconds / 60
    elif format == DurationFormat.HOURS:
        return duration_in_seconds / 3600
    else:
        raise ValueError("Invalid duration format")


def calculate_frequency(
    total_events: int, time_delta: timedelta, time_unit: FrequencyTimeUnit
):
    """
    Calculates the frequency of events based on a given time unit.

    This function computes the frequency of a total number of events over a specified time period.
    The frequency is calculated based on the time unit provided (daily, weekly, monthly).

    Args:
        total_events (int): The total number of events to calculate frequency for.
        time_delta (timedelta): The time span over which the events occurred.
        time_unit (FrequencyTimeUnit): The unit of time to calculate frequency (e.g., daily, weekly, monthly).

    Returns:
        float: The frequency of events per the specified time unit.
    """
    if time_unit == FrequencyTimeUnit.DAILY:
        days = time_delta.days or 1
        return total_events / days
    elif time_unit == FrequencyTimeUnit.WEEKLY:
        weeks = max(time_delta.days / 7, 1)
        return total_events / weeks
    elif time_unit == FrequencyTimeUnit.MONTHLY:
        # approximation
        months = max(time_delta.days / 30, 1)
        return total_events / months
