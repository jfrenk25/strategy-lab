"""Long candle shadows (Qlib Alpha158: KUP and KLOW).

Source factors: KUP = (high - max(open, close)) / open, KLOW = (min(open, close) - low) / open.
Kept: the two factors as defined. Changed: a factor is turned into an event by firing when it is above
the q-quantile of its own previous 500 bars and is the longer of the two shadows.
Note: the source page could not be opened in the session that wrote this file, so the formula is written from the published definition as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="a158_shadow",
    source="Microsoft Qlib, Alpha158 factor set (github.com/microsoft/qlib, qlib/contrib/data/loader.py), factors KUP and KLOW",
    summary="+1 when the lower shadow is unusually long against the last 500 bars, -1 when the upper shadow is.",
    variants=[{"q": 0.95}, {"q": 0.99}],
    timed=False,
)


def event(df, p):
    o, h, l, c = df["open"], df["high"], df["low"], df["close"]
    kup = (h - np.maximum(o, c)) / o
    klow = (np.minimum(o, c) - l) / o
    up_lim = kup.rolling(500).quantile(p["q"]).shift(1)
    lo_lim = klow.rolling(500).quantile(p["q"]).shift(1)
    return np.where((klow > lo_lim) & (klow > kup), 1, np.where((kup > up_lim) & (kup > klow), -1, 0))
