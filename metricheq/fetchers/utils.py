from enum import Enum

fetcher_registry = {}


class DurationFormat(str, Enum):
    SECONDS = "seconds"
    MINUTES = "minutes"
    HOURS = "hours"


def register_fetcher(file_name):
    def decorator(fetcher_class):
        fetcher_registry[fetcher_class.__name__] = file_name
        return fetcher_class

    return decorator
