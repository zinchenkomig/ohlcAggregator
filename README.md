# Docs

Runs on `Python 3.10`
## Set Up
```
git clone
python -m venv ohlc_venv 
source ohlc_venv/bin/activate

pip install -r requirements.txt
python usage_example.py

```

## Getting started

Here is an example on how to use this package to plot OHLC Candlestick with its EMA indicator.

```python
import pandas as pd
import plotly.graph_objects as go

import ohlc


if __name__ == '__main__':
    trades = ohlc.readers.csv_reader("prices.csv")
    ohlc_data = list(ohlc.from_trades(trades=trades, interval_seconds=3600 * 24))

    ohlc_df = pd.DataFrame(ohlc_data)
    ema_graph = pd.DataFrame(ohlc.indicators.ema(iter(ohlc_data), smoothing=2, length=7), columns=['ts', 'ema'])

    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=ohlc_df['ts'],
                                 open=ohlc_df['open'],
                                 high=ohlc_df['high'],
                                 low=ohlc_df['low'],
                                 close=ohlc_df['close']))
    fig.add_trace(go.Scatter(x=ema_graph['ts'], y=ema_graph['ema']))

    fig.show()
```

Here is what you get:


## OHLC
OHLC object is represented as dataclass:
```python
@dataclasses.dataclass
class OHLC:
    ts: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
```

## OHLC Aggregation
`ohlc.from_trades()` function accepts trades as an `Iterator[(ns_timestamp int, price Decimal)]` 
and the interval length for one ohlc record in seconds. It returns an `Iterator[ohlc.OHLC]` for provided trades.
```python
import ohlc

...

ohlc_iterator = ohlc.from_trades(trades=trades, interval_seconds=3600 * 24)

print(list(ohlc_iterator))

# Return format:
# [OHLC(ts=datetime.datetime(2023, 5, 4, 0, 0),
#       open=Decimal('1875.979748793'),
#       high=Decimal('1877.9007182547'),
#       low=Decimal('1869.0165488903'),
#       close=Decimal('1875.8833246727')),
#  OHLC(ts=datetime.datetime(2023, 5, 5, 0, 0),
#       open=Decimal('1876.5328126135'),
#       high=Decimal('2005.2157656006'),
#       low=Decimal('1875.8820238586'),
#       close=Decimal('1993.9739093948')),
#  OHLC(ts=datetime.datetime(2023, 5, 6, 0, 0),
#       open=Decimal('1994.1272438815'),
#       high=Decimal('2013.9876735985'),
#       low=Decimal('1866.590305501'),
#       close=Decimal('1898.5453245012')),
#  ...
#  ]
```



## Readers
This package has reader adapters 
to convert csv files or text strs to the `ohlc.from_trades` function readable iterators
### CSV file
`csv_reader` accepts a file with a header string of a format:
```
TS,PRICE
2023-05-04 18:21:18.340000000,1875.979748793
2023-05-04 18:21:18.341000192,1876.7313482702
2023-05-04 18:22:48.342000128,1876.7311357534
```
Usage:
```python
import ohlc

trades_iterator = ohlc.readers.csv_reader("filepath.csv")
```
### STR Reader
Usage example:
```python
import ohlc

data = """2023-05-04 18:21:18.340000000,1875.979748793
          2023-05-04 18:21:18.341000192,1876.7313482702
          2023-05-04 18:22:48.342000128,1876.7311357534"""

trades_iterator = ohlc.readers.str_reader(data)
```

## EMA
This function accepts an `Iterator[OHLC]`, smoothing and length parameters 
and returns Exponential Moving Average for provided data.

Returns an `Iterator[(ts: datetime, ema: Decimal)]`
```python
import ohlc

ohlc.indicators.ema(ohlc_data=ohlc_data, smoothing=2, length=14)

```

## Tests

You can run tests located in the `tests` folder by running `pytest tests` in your terminal