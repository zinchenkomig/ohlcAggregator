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
