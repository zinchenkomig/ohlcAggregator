import typing
from decimal import Decimal
from .ohlc import OHLC


def ema_formula(current_price: Decimal, smoothing: Decimal, length: int, previous_ema: Decimal):
    return current_price * (smoothing / (1 + length)) + previous_ema * (1 - (smoothing / (1 + length)))


def mean(values: list):
    return sum(values) / len(values)


def ema(ohlc_data: typing.Iterator[OHLC], smoothing: float, length: int):
    if length <= 0:
        raise ValueError('length parameter should be greater than zero')

    if smoothing <= 0:
        raise ValueError('smoothing parameter should be greater than zero')

    try:
        start_period_records = [next(ohlc_data) for _ in range(length)]
    except StopIteration:
        return
    start_period_values = list(map(lambda x: x.close, start_period_records))
    start_mean = mean(start_period_values)
    yield start_period_records[-1].ts, start_mean

    previous_ema = start_mean
    for ohlc_record in ohlc_data:
        current_ema = ema_formula(current_price=ohlc_record.close, smoothing=Decimal(smoothing), length=length,
                                  previous_ema=previous_ema)
        yield ohlc_record.ts, current_ema
        previous_ema = current_ema
