"""Close at the edge of the bar, tilted by the bar's direction (101 Formulaic Alphas: Alpha#54).

Source formula: -((low - close) * open^5) / ((low - high) * close^5), which equals minus the close's position in the
bar's range times (open / close)^5. It is highest when the bar closes on its low and lowest when it closes on its
high after falling from the open.
Kept: the formula and its sign. Changed: the event fires when the value first reaches the q-quantile (+1) or the
(1-q)-quantile (-1) of its own previous 500 bars. No bar-size condition is used.
Note: the source page could not be opened in the session that wrote this file, so the formula is written from the published definition as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="alpha054",
    source='Z. Kakushadze, "101 Formulaic Alphas" (2016), arXiv:1601.00991, Alpha#54',
    summary="+1 when a bar closes unusually near its low (by the Alpha#54 score), -1 when unusually near its high.",
    variants=[{"q": 0.95}],
    timed=False,
)


def event(df, p):
    o, h, l, c = df["open"], df["high"], df["low"], df["close"]
    rng = (h - l).where(h > l)
    a = -((c - l) / rng) * (o / c) ** 5
    hi = a.rolling(500).quantile(p["q"]).shift(1); lo = a.rolling(500).quantile(1 - p["q"]).shift(1)
    up = a >= hi; dn = a <= lo
    return np.where(up & ~up.shift(1, fill_value=False), 1, np.where(dn & ~dn.shift(1, fill_value=False), -1, 0))
