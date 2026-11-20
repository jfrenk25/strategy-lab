"""Price moving with volume (Qlib Alpha158: CORR).

Source factor: CORR(n) is the correlation between the close and the log of volume over the last n bars.
Kept: the factor and the 20 and 60 bar windows. Changed: the event fires when CORR first moves above the 95%
quantile (+1) or below the 5% quantile (-1) of its own previous 500 bars.
Note: the source page could not be opened in the session that wrote this file, so the formula is written from the published definition as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="a158_corr",
    source="Microsoft Qlib, Alpha158 factor set (github.com/microsoft/qlib, qlib/contrib/data/loader.py), factor CORR",
    summary="+1 when price and volume have risen and fallen together unusually closely over n bars, -1 when unusually oppositely.",
    variants=[{"n": 20}, {"n": 60}],
    timed=False,
)


def event(df, p):
    n = int(p["n"])
    x = df["close"].rolling(n).corr(np.log(df["volume"] + 1.0)).replace([np.inf, -np.inf], np.nan)
    hi = x.rolling(500).quantile(0.95).shift(1); lo = x.rolling(500).quantile(0.05).shift(1)
    up = x > hi; dn = x < lo
    return np.where(up & ~up.shift(1, fill_value=False), 1, np.where(dn & ~dn.shift(1, fill_value=False), -1, 0))
