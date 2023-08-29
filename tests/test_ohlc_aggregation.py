import pytest

import ohlc
import datetime
from decimal import Decimal


@pytest.mark.parametrize("data,result",
                         [("""2023-05-04 18:21:18.340000000,1875.979748793
                            2023-05-04 18:21:18.341000192,1876.7313482702
                            2023-05-04 18:22:48.342000128,1876.7311357534
                            2023-05-04 18:22:48.342999808,1876.5195508966
                            2023-05-04 18:22:48.344000000,1876.1535273193
                            2023-05-04 18:23:03.344999936,1875.9899474618
                            2023-05-04 18:23:03.345999872,1875.806175391
                            2023-05-04 18:23:03.346999808,1875.42707394
                            2023-05-04 18:23:03.348000000,1875.42707394""",
                           [ohlc.OHLC(ts=datetime.datetime(2023, 5, 4, 18, 21),
                                      open=Decimal('1875.979748793'),
                                      high=Decimal('1876.7313482702'),
                                      low=Decimal('1875.979748793'),
                                      close=Decimal('1876.7313482702')),
                            ohlc.OHLC(ts=datetime.datetime(2023, 5, 4, 18, 22),
                                      open=Decimal('1876.7311357534'),
                                      high=Decimal('1876.7311357534'),
                                      low=Decimal('1876.1535273193'),
                                      close=Decimal('1876.1535273193')),
                            ohlc.OHLC(ts=datetime.datetime(2023, 5, 4, 18, 23),
                                      open=Decimal('1875.9899474618'),
                                      high=Decimal('1875.9899474618'),
                                      low=Decimal('1875.42707394'),
                                      close=Decimal('1875.42707394'))]
                           ),

                          #  Gap case. There is no data for 18:24 in the input.
                          #  We expect the result to interpolate ohlc of 18:24 with previous (18:23) ohlc close value.
                          #  Also checking for last element to make an ohlc successfully
                          #  even with initially truncated time
                          ("""2023-05-04 18:21:00.000000000,1875
                            2023-05-04 18:22:00.000000000,1879
                            2023-05-04 18:23:00.000000000,1885
                            2023-05-04 18:23:01.000000000,1800
                            2023-05-04 18:23:05.000000000,1890
                            2023-05-04 18:23:59.999999999,1790
                            2023-05-04 18:25:00.000000000,1830""",
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

                           ]

                           ),

                          (
                                  """2023-05-04 18:21:01.123000000,1875""",
                                  [ohlc.OHLC(ts=datetime.datetime(2023, 5, 4, 18, 21),
                                             open=Decimal('1875'),
                                             high=Decimal('1875'),
                                             low=Decimal('1875'),
                                             close=Decimal('1875'))]
                          ),

                          ])
def test_minute_ohlc(data, result):
    assert list(ohlc.from_trades(ohlc.readers.str_reader(data), interval_seconds=60)) == result
