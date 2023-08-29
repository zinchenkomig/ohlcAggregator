from datetime import datetime


def ns2datetime(ns_ts: int) -> datetime:
    return datetime.fromtimestamp(ns_ts / 10 ** 9)


def trunc_start_time(start_ts_ns: int, interval_seconds: int) -> int:
    """
    Depending on the interval length truncates timestamp

    In case we have interval of 1 hour,
    we want to truncate the timestamp so the interval would start from zero minutes of the hour

    :param start_ts_ns: ns timestamp
    :param interval_seconds: interval in seconds
    :return:
    """
    interval_start_dt = ns2datetime(start_ts_ns)
    if interval_seconds < 60:
        interval_start_dt = interval_start_dt.replace(microsecond=0)
    elif 60 <= interval_seconds < 3600:
        interval_start_dt = interval_start_dt.replace(second=0, microsecond=0)
    elif 3600 <= interval_seconds < 3600 * 24:
        interval_start_dt = interval_start_dt.replace(minute=0, second=0, microsecond=0)
    else:
        interval_start_dt = interval_start_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return int(interval_start_dt.timestamp() * 10 ** 9)


def parse_timestamp(date_string: str) -> int:
    """

    :param date_string: example '2023-05-04 18:21:18.340000000'
    :return: integer nanoseconds timestamp
    """
    # Datetime fromisoformat function gets only microseconds precision
    # whereas in the input string we have nanoseconds precision.
    # So we cut the last three digits when parsing datetime
    return int(datetime.fromisoformat(date_string[:-3]).timestamp() * 10 ** 9) + int(date_string[-3:])
