"""Time-series momentum across markets: hold each market in the direction of its own past return."""
import numpy as np

IDEA = dict(
    name="ts_momentum",
    mode="position",
    source="Kakushadze and Serur, 151 Trading Strategies, section 10.4 (after Moskowitz, Ooi and Pedersen, 2012)",
    reason="Trends persist for months because information spreads slowly and investors adjust positions gradually.",
    loser="Hedgers and slow movers who trade against a move that has not finished.",
    grid=[{"lookback": 21}, {"lookback": 63}, {"lookback": 252}],
)


def positions(data, p):
    close = data["close"]
    filled = close.ffill()
    past = filled / filled.shift(p["lookback"]) - 1
    vol = filled.pct_change().rolling(60, min_periods=40).std()
    w = (np.sign(past) / vol).where(close.notna())
    w = w.div(w.abs().sum(axis=1), axis=0)
    monday = close.index.dayofweek == 0          # decide once a week, hold in between
    return w.loc[monday].reindex(w.index).ffill()
