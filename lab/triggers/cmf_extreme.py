"""Chaikin Money Flow at an extreme.

Source: the technical-indicator example strategy in the public freqtrade strategy collection, which trades on the sign
of Chaikin Money Flow. CMF(n) = sum over n bars of ((close - low) - (high - close)) / (high - low) * volume, divided by
the sum of volume.
Kept: the indicator. Changed: a zero cross is an indicator crossover, which the lab has stopped adding, so the event
fires when CMF first moves above the 95% quantile (+1) or below the 5% quantile (-1) of its own previous 500 bars.
Note: the source page could not be opened in the session that wrote this file, so the formula is written from the published definition as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="cmf_extreme",
    source='freqtrade-strategies (github.com/freqtrade/freqtrade-strategies), berlinguyinca/TechnicalExampleStrategy (Chaikin Money Flow)',
    summary="+1 when volume-weighted closes have been unusually near the bar highs over n bars, -1 when unusually near the lows.",
    variants=[{"n": 20}],
    timed=False,
)


def event(df, p):
    n = int(p["n"]); h, l, c, v = df["high"], df["low"], df["close"], df["volume"]
    rng = (h - l).where(h > l)
    mfv = (((c - l) - (h - c)) / rng).fillna(0.0) * v
    vs = v.rolling(n).sum()
    x = mfv.rolling(n).sum() / vs.where(vs > 0)
    hi = x.rolling(500).quantile(0.95).shift(1); lo = x.rolling(500).quantile(0.05).shift(1)
    up = x > hi; dn = x < lo
    return np.where(up & ~up.shift(1, fill_value=False), 1, np.where(dn & ~dn.shift(1, fill_value=False), -1, 0))
