"""Cross-market contrarian: buy what lagged the group last week, sell what led it."""
import numpy as np

IDEA = dict(
    name="xs_contrarian",
    mode="position",
    source="Kakushadze and Serur, 151 Trading Strategies, section 10.3",
    reason="Short-term moves away from the group partly reverse as temporary buying or selling pressure fades.",
    loser="Traders who chase last week's leaders, and those forced to trade into a temporary imbalance.",
    grid=[{"lookback": 5}, {"lookback": 10}, {"lookback": 21}],
)


def positions(data, p):
    close = data["close"]
    filled = close.ffill()
    r = (filled / filled.shift(p["lookback"]) - 1).where(close.notna())
    vol = filled.pct_change().rolling(60, min_periods=40).std()
    w = (-(r.sub(r.mean(axis=1), axis=0)) / vol).where(close.notna())
    w = w.div(w.abs().sum(axis=1), axis=0)
    monday = close.index.dayofweek == 0
    return w.loc[monday].reindex(w.index).ffill()
