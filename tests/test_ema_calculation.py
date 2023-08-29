import pytest
import ohlc
from decimal import Decimal
import datetime


@pytest.mark.parametrize("ohlc_data, result",
                         [
                             # Just testing calculations
                             (
                                     [
                                         ohlc.OHLC(ts=datetime.datetime(2023, 5, 4, 18, 21),
                                                   open=Decimal('1875'),
                                                   high=Decimal('1875'),
                                                   low=Decimal('1875'),
                                                   close=Decimal('1875')),
                                         ohlc.OHLC(ts=datetime.datetime(2023, 5, 4, 18, 22),
                                                   open=Decimal('1879'),
                                                   high=Decimal('1879'),
                                                   low=Decimal('1879'),
                                                   close=Decimal('1879')),
                                         ohlc.OHLC(ts=datetime.datetime(2023, 5, 4, 18, 23),
                                                   open=Decimal('1885'),
                                                   high=Decimal('1890'),
                                                   low=Decimal('1790'),
                                                   close=Decimal('1790')),
                                         ohlc.OHLC(ts=datetime.datetime(2023, 5, 4, 18, 24),
                                                   open=Decimal('1790'),
                                                   high=Decimal('1790'),
                                                   low=Decimal('1790'),
                                                   close=Decimal('1790')),
                                         ohlc.OHLC(ts=datetime.datetime(2023, 5, 4, 18, 25),
                                                   open=Decimal('1830'),
                                                   high=Decimal('1830'),
                                                   low=Decimal('1830'),
                                                   close=Decimal('1830'))

                                     ],
                                     [
                                         (datetime.datetime(2023, 5, 4, 18, 23), Decimal('1848')),
                                         (datetime.datetime(2023, 5, 4, 18, 24), Decimal('1819')),
                                         (datetime.datetime(2023, 5, 4, 18, 25), Decimal('1824.5'))
                                     ]
                             ),

                             #  Case when the length for the ema calculation is greater than the amount of intervals
                             #  The expected result is an empty list because we cannot calculate a single ema value
                             (
                                     [
                                         ohlc.OHLC(ts=datetime.datetime(2023, 5, 4, 18, 21),
                                                   open=Decimal('1875'),
                                                   high=Decimal('1875'),
                                                   low=Decimal('1875'),
                                                   close=Decimal('1875')),
                                         ohlc.OHLC(ts=datetime.datetime(2023, 5, 4, 18, 22),
                                                   open=Decimal('1879'),
                                                   high=Decimal('1879'),
                                                   low=Decimal('1879'),
                                                   close=Decimal('1879'))
                                     ],
                                     []
                             )
                         ]
                         )
def test_ema(ohlc_data: list[ohlc.OHLC], result: list[(datetime.datetime, Decimal)]):
    assert list(ohlc.indicators.ema(iter(ohlc_data), smoothing=2, length=3)) == result


def test_ema_bad_smoothing():
    ohlc_data = [
        ohlc.OHLC(ts=datetime.datetime(2023, 5, 4, 18, 21),
                  open=Decimal('1875'),
                  high=Decimal('1875'),
                  low=Decimal('1875'),
                  close=Decimal('1875')),
        ohlc.OHLC(ts=datetime.datetime(2023, 5, 4, 18, 22),
                  open=Decimal('1879'),
                  high=Decimal('1879'),
                  low=Decimal('1879'),
                  close=Decimal('1879'))
    ]
    with pytest.raises(ValueError):
        list(ohlc.indicators.ema(iter(ohlc_data), smoothing=-1, length=5))


def test_ema_bad_length():
    ohlc_data = [
        ohlc.OHLC(ts=datetime.datetime(2023, 5, 4, 18, 21),
                  open=Decimal('1875'),
                  high=Decimal('1875'),
                  low=Decimal('1875'),
                  close=Decimal('1875')),
        ohlc.OHLC(ts=datetime.datetime(2023, 5, 4, 18, 22),
                  open=Decimal('1879'),
                  high=Decimal('1879'),
                  low=Decimal('1879'),
                  close=Decimal('1879'))
    ]
    with pytest.raises(ValueError):
        list(ohlc.indicators.ema(iter(ohlc_data), smoothing=1, length=-1))
