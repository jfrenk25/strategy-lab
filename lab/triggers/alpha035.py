"""High volume with price and returns at the bottom of their recent ranks (101 Formulaic Alphas: Alpha#35).

Source formula: ts_rank(volume, 32) * (1 - ts_rank(close + high - low, 16)) * (1 - ts_rank(returns, 32)).
All three parts rank a bar against the market's own recent bars, so no price or volume scale is assumed.
Kept: the formula and its windows for the +1 side. Changed: the event fires when the value is above the q-quantile of
its own previous 500 bars. The -1 side is the same formula on the price series turned upside down, which the source
does not have.
Note: the source page could not be opened in the session that wrote this file, so the formula is written from the published definition as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="alpha035",
    source='Z. Kakushadze, "101 Formulaic Alphas" (2016), arXiv:1601.00991, Alpha#35',
    summary="+1 when volume ranks high while price and the last return rank low against recent bars to an unusual degree; -1 for the mirror image.",
    variants=[{"q": 0.95}, {"q": 0.99}],
    timed=False,
)


def event(df, p):
    h, l, c, v = df["high"], df["low"], df["close"], df["volume"]
    ret = c / c.shift(1) - 1
    rv = v.rolling(32).rank(pct=True)
    up = rv * (1 - (c + h - l).rolling(16).rank(pct=True)) * (1 - ret.rolling(32).rank(pct=True))
    dn = rv * (1 - (-c + h - l).rolling(16).rank(pct=True)) * (1 - (-ret).rolling(32).rank(pct=True))
    up_lim = up.rolling(500).quantile(p["q"]).shift(1); dn_lim = dn.rolling(500).quantile(p["q"]).shift(1)
    a, b = (up > up_lim), (dn > dn_lim)
    return np.where(a & ~b, 1, np.where(b & ~a, -1, 0))
