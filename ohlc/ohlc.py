import collections.abc
import dataclasses
from datetime import datetime
from decimal import Decimal

from .time_utils import trunc_start_time, ns2datetime


@dataclasses.dataclass
class OHLC:
    ts: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal


def from_trades(trades: collections.abc.Iterator[(int, Decimal)],
                interval_seconds: int) -> collections.abc.Iterator[OHLC]:
    """

    :param trades: Iterator object that yields tuples with ns int timestamp and Decimal price
    :param interval_seconds: interval in seconds
    """
    ns_interval = interval_seconds * 10 ** 9
    interval_start_ns_ts, interval_start_price = next(trades)  # Initialization
    interval_start_ns_ts = trunc_start_time(interval_start_ns_ts, interval_seconds)
    interval_high = interval_low = close_price = interval_start_price

    for current_ns_ts, current_price in trades:
        if ns_interval <= current_ns_ts - interval_start_ns_ts < ns_interval * 2:
            yield OHLC(ts=ns2datetime(interval_start_ns_ts),
                       open=interval_start_price,
                       high=interval_high,
                       low=interval_low,
                       close=close_price)
            interval_start_ns_ts += ns_interval
            interval_high = interval_low = interval_start_price = close_price = current_price

        # In case there are lost intervals in data
        elif current_ns_ts - interval_start_ns_ts >= ns_interval * 2:
            yield OHLC(ts=ns2datetime(interval_start_ns_ts),
                       open=interval_start_price,
                       high=interval_high,
                       low=interval_low,
                       close=close_price)
            lost_intervals_amount = (current_ns_ts - interval_start_ns_ts) // ns_interval
            for i in range(1, lost_intervals_amount):
                yield OHLC(
                    ts=ns2datetime(interval_start_ns_ts + i * ns_interval),
                    open=close_price,
                    high=close_price,
                    low=close_price,
                    close=close_price
                )
            interval_start_ns_ts += lost_intervals_amount * ns_interval
            interval_high = interval_low = interval_start_price = close_price = current_price
        else:
            if current_price > interval_high:
                interval_high = current_price
            if current_price < interval_low:
                interval_low = current_price
            close_price = current_price
    yield OHLC(ts=ns2datetime(interval_start_ns_ts),
               open=interval_start_price,
               high=interval_high,
               low=interval_low,
               close=close_price)
