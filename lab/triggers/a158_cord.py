"""Price changes moving with volume changes (Qlib Alpha158: CORD).

Source factor: CORD(n) is the correlation over n bars between the close's one-bar ratio and the log of volume's one-bar ratio.
Kept: the factor and the 20 and 60 bar windows. Changed: the event fires when CORD first moves above the 95%
quantile (+1) or below the 5% quantile (-1) of its own previous 500 bars.
Note: the source page could not be opened in the session that wrote this file, so the formula is written from the published definition as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="a158_cord",
    source="Microsoft Qlib, Alpha158 factor set (github.com/microsoft/qlib, qlib/contrib/data/loader.py), factor CORD",
    summary="+1 when up-bars have come with rising volume and down-bars with falling volume unusually often over n bars, -1 for the opposite.",
    variants=[{"n": 20}, {"n": 60}],
    timed=False,
)


def event(df, p):
    n = int(p["n"]); c, v = df["close"], df["volume"]
    pr = c / c.shift(1)
    vr = np.log(v / v.shift(1).where(v.shift(1) > 0) + 1.0)
    x = pr.rolling(n).corr(vr).replace([np.inf, -np.inf], np.nan)
    hi = x.rolling(500).quantile(0.95).shift(1); lo = x.rolling(500).quantile(0.05).shift(1)
    up = x > hi; dn = x < lo
    return np.where(up & ~up.shift(1, fill_value=False), 1, np.where(dn & ~dn.shift(1, fill_value=False), -1, 0))
