"""Bulk-volume order imbalance (Easley, Lopez de Prado and O'Hara).

Source: Easley, Lopez de Prado and O'Hara, "Flow Toxicity and Liquidity in a High-frequency World", Review of
Financial Studies 25(5), 2012, 1457-1493 (bulk volume classification and VPIN). The formulas were read from the
February 2012 working-paper version in the session that wrote this file.
The paper splits each bar's volume into buys and sells from the price change alone:
buy volume = V x Z(dP / sigma), sell volume = V - buy volume, where Z is the standard normal distribution function
and sigma is the standard deviation of price changes between bars. VPIN is the sum of |sell - buy| over the last
n = 50 volume buckets divided by the total volume in them.
Kept: the split, and n = 50.
Changed: 1-hour time bars stand in for the paper's equal-volume buckets built from 1-minute bars. The paper's
measure is unsigned (it gauges how one-sided the flow is, not which side). Here the sign is kept:
imbalance = sum(buy - sell) / sum(volume) over the last n bars, so the event has a direction. sigma is the standard
deviation of the last 500 close-to-close changes. The event fires when the imbalance first moves above the q
quantile (+1) or below the 1 - q quantile (-1) of its own previous 500 bars. Bars with no volume add nothing.
"""
import numpy as np
import pandas as pd
from math import erf, sqrt

TRIGGER = dict(
    name="bvc_imbalance",
    source='Easley, Lopez de Prado and O\'Hara, "Flow Toxicity and Liquidity in a High-frequency World", Review of Financial Studies 25(5), 2012, 1457-1493 (bulk volume classification)',
    summary="+1 when estimated buying, as a share of volume over the last 50 bars, first becomes unusually high for this market; -1 when estimated selling does.",
    variants=[{"n": 50, "q": 0.95}],
    timed=False,
)


def event(df, p):
    c, v = df["close"], df["volume"]; n = int(p["n"])
    d = c.diff()
    z = (d / d.rolling(500).std()).to_numpy(dtype=float)
    buy_share = pd.Series([0.5 * (1.0 + erf(x / sqrt(2.0))) if x == x else np.nan for x in z], index=c.index)
    net = v * (2.0 * buy_share - 1.0)                       # buy volume minus sell volume
    tot = v.rolling(n).sum()
    x = net.rolling(n).sum() / tot.where(tot > 0)
    hi = x.rolling(500).quantile(p["q"]).shift(1); lo = x.rolling(500).quantile(1 - p["q"]).shift(1)
    up = x > hi; dn = x < lo
    return np.where(up & ~up.shift(1, fill_value=False), 1, np.where(dn & ~dn.shift(1, fill_value=False), -1, 0))
