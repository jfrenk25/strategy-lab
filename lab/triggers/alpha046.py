"""A trend that speeds up (101 Formulaic Alphas: Alpha#46, also the core of Alpha#49 and Alpha#51).

Source quantity: x = (close 20 bars ago - close 10 bars ago) / 10 - (close 10 bars ago - close) / 10, which is the
slope of the last 10 bars minus the slope of the 10 bars before. Alpha#46 goes short when x is above a fixed number
and long when x is below zero.
Kept: x, the 10 and 20 bar lags, and the sign (speeding up points down). Changed: the source's thresholds are fixed
price amounts, so x is taken as a fraction of the close and the event fires when it first moves above the q-quantile
(-1) or below the (1-q)-quantile (+1) of its own previous 500 bars. The source's one-bar fallback is dropped.
Note: the source page could not be opened in the session that wrote this file, so the formula is written from the published definition as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="alpha046",
    source='Z. Kakushadze, "101 Formulaic Alphas" (2016), arXiv:1601.00991, Alpha#46 (same quantity in Alpha#49 and Alpha#51)',
    summary="-1 when the last 10 bars rose unusually much faster than the 10 before, +1 when they fell unusually much faster.",
    variants=[{"q": 0.95}],
    timed=False,
)


def event(df, p):
    c = df["close"]
    x = ((c.shift(20) - c.shift(10)) / 10 - (c.shift(10) - c) / 10) / c.shift(20)
    hi = x.rolling(500).quantile(p["q"]).shift(1); lo = x.rolling(500).quantile(1 - p["q"]).shift(1)
    up = x > hi; dn = x < lo
    return np.where(dn & ~dn.shift(1, fill_value=False), 1, np.where(up & ~up.shift(1, fill_value=False), -1, 0))
