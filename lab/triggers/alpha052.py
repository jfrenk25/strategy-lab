"""Falling 5-bar low, weighted by the longer-run return and by volume (101 Formulaic Alphas: Alpha#52).

Source formula: ((-1 * ts_min(low, 5)) + delay(ts_min(low, 5), 5)) * rank((sum(returns, 240) - sum(returns, 20)) / 220)
* ts_rank(volume, 5). The formula was read from the paper (arXiv:1601.00991, Appendix A) in the session that wrote this file.
Kept: the three factors and their windows. The first is positive when the 5-bar low has dropped below the 5-bar low
of five bars ago; the second is high when the return from 240 to 20 bars ago was strong; the third is high when the
latest bar's volume is the largest of the last five. The paper's sign is kept: a large positive value points up.
Changed: 1-hour bars instead of days. The rank across stocks is replaced by the rank of the return term within the
market's own previous 500 bars (0 to 1). The change in the low is divided by the close to remove the price scale.
The event fires when the product first moves above the q quantile of its own previous 500 bars (+1) or below the
1 - q quantile (-1, a rising low under the same weights).
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="alpha052",
    source='Z. Kakushadze, "101 Formulaic Alphas" (2016), arXiv:1601.00991, Alpha#52',
    summary="+1 when the 5-bar low has fallen unusually far on high volume after a strong longer-run return; -1 when it has risen unusually far under the same weights.",
    variants=[{"q": 0.95}],
    timed=False,
)


def event(df, p):
    c, l, v = df["close"], df["low"], df["volume"]
    r = c / c.shift(1) - 1
    low5 = l.rolling(5).min()
    drop = (low5.shift(5) - low5) / c.shift(5)
    slow = (r.rolling(240).sum() - r.rolling(20).sum()) / 220
    slow_rank = slow.rolling(500).rank(pct=True)
    vol_rank = v.rolling(5).rank(pct=True)
    x = drop * slow_rank * vol_rank
    hi = x.rolling(500).quantile(p["q"]).shift(1); lo = x.rolling(500).quantile(1 - p["q"]).shift(1)
    up = x > hi; dn = x < lo
    return np.where(up & ~up.shift(1, fill_value=False), 1, np.where(dn & ~dn.shift(1, fill_value=False), -1, 0))
