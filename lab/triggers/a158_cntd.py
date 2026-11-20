"""Many more up-bars than down-bars (Qlib Alpha158: CNTD).

Source factor: CNTD(n) is the share of the last n bars that closed up minus the share that closed down.
It counts bars and ignores their size, so it is not an RSI. Kept: the factor and the 20 and 60 bar windows.
Changed: the event fires when CNTD first moves above the 95% quantile (+1) or below the 5% quantile (-1)
of its own previous 500 bars.
Note: the source page could not be opened in the session that wrote this file, so the formula is written from the published definition as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="a158_cntd",
    source="Microsoft Qlib, Alpha158 factor set (github.com/microsoft/qlib, qlib/contrib/data/loader.py), factor CNTD",
    summary="+1 when up-closes outnumber down-closes over n bars by an unusual margin, -1 when down-closes do.",
    variants=[{"n": 20}, {"n": 60}],
    timed=False,
)


def event(df, p):
    n = int(p["n"]); c = df["close"]; pc = c.shift(1)
    x = (c > pc).astype(float).rolling(n).mean() - (c < pc).astype(float).rolling(n).mean()
    hi = x.rolling(500).quantile(0.95).shift(1); lo = x.rolling(500).quantile(0.05).shift(1)
    up = x > hi; dn = x < lo
    return np.where(up & ~up.shift(1, fill_value=False), 1, np.where(dn & ~dn.shift(1, fill_value=False), -1, 0))
