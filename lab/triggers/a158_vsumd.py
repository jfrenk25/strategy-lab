"""Volume building up (Qlib Alpha158: VSUMD).

Source factor: VSUMD(n) = (sum of volume rises - sum of volume falls) / (sum of all absolute volume changes) over n bars.
Kept: the factor and the 20 and 60 bar windows. Changed: the factor has no direction, so the event fires when VSUMD first
moves above the 95% quantile of its own previous 500 bars and points the way price moved over the same n bars.
Note: the source page could not be opened in the session that wrote this file, so the formula is written from the published definition as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="a158_vsumd",
    source="Microsoft Qlib, Alpha158 factor set (github.com/microsoft/qlib, qlib/contrib/data/loader.py), factor VSUMD",
    summary="Volume has been building unusually strongly over n bars: +1 if price rose over those bars, -1 if it fell.",
    variants=[{"n": 20}, {"n": 60}],
    timed=False,
)


def event(df, p):
    n = int(p["n"]); c = df["close"]; dv = df["volume"].diff()
    tot = dv.abs().rolling(n).sum()
    x = (dv.clip(lower=0).rolling(n).sum() - (-dv.clip(upper=0)).rolling(n).sum()) / tot.where(tot > 0)
    hi = x.rolling(500).quantile(0.95).shift(1)
    up = x > hi
    start = (up & ~up.shift(1, fill_value=False)).to_numpy()
    mv = (c - c.shift(n)).to_numpy()
    return np.where(start & (mv > 0), 1, np.where(start & (mv < 0), -1, 0))
