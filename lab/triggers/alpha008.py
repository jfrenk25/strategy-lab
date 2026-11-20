"""Change in (summed opens times summed returns) (101 Formulaic Alphas: Alpha#8).

Source formula: -1 * rank(sum(open, 5) * sum(returns, 5) - delay(sum(open, 5) * sum(returns, 5), 10)).
The formula was read from the paper (arXiv:1601.00991v1, Appendix A) in the session that wrote this file.
Kept: the inner quantity, its windows and its sign (a large rise points down). Changed: the rank across stocks is
replaced by the market's own past. The quantity is divided by the close to remove the price scale, and the event fires
when it first moves above the 95% quantile (-1) or below the 5% quantile (+1) of its own previous 500 bars.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="alpha008",
    source='Z. Kakushadze, "101 Formulaic Alphas" (2016), arXiv:1601.00991, Alpha#8',
    summary="-1 when the 5-bar return, weighted by price, has risen unusually much against its value 10 bars ago; +1 when it has fallen unusually much.",
    variants=[{"q": 0.95}],
    timed=False,
)


def event(df, p):
    o, c = df["open"], df["close"]
    y = o.rolling(5).sum() * (c / c.shift(1) - 1).rolling(5).sum()
    x = (y - y.shift(10)) / c.shift(10)
    hi = x.rolling(500).quantile(p["q"]).shift(1); lo = x.rolling(500).quantile(1 - p["q"]).shift(1)
    up = x > hi; dn = x < lo
    return np.where(dn & ~dn.shift(1, fill_value=False), 1, np.where(up & ~up.shift(1, fill_value=False), -1, 0))
