from enum import Enum


class DurationFormat(str, Enum):
    SECONDS = "seconds"
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"


def convert_to_seconds(duration_in_seconds, format: DurationFormat):
    if format == DurationFormat.SECONDS:
        return duration_in_seconds
    elif format == DurationFormat.MINUTES:
        return duration_in_seconds / 60
    elif format == DurationFormat.HOURS:
        return duration_in_seconds / 3600
    else:
        raise ValueError("Invalid duration format")
