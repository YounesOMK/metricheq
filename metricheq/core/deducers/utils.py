from datetime import timedelta


def convert_seconds(duration_in_seconds, format: str):
    if format == "seconds":
        return duration_in_seconds
    elif format == "minutes":
        return duration_in_seconds / 60
    elif format == "hours":
        return duration_in_seconds / 3600
    else:
        raise ValueError("Invalid duration format")


def calculate_frequency(total_events: int, time_delta: timedelta, time_unit: str):
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
    if time_unit == "daily":
        days = time_delta.days or 1
        return total_events / days
    elif time_unit == "weekly":
        weeks = max(time_delta.days / 7, 1)
        return total_events / weeks
    elif time_unit == "monthly":
        # approximation
        months = max(time_delta.days / 30, 1)
        return total_events / months
    else:
        raise ValueError("Invalid time unit format")
