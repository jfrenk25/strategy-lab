"""A very straight trend (Qlib Alpha158: RSQR, with the sign of BETA).

Source factors: RSQR(n) is the R-squared of a straight line fitted to the last n closes; BETA(n) is its slope.
Kept: both factors and the 20 and 60 bar windows. Changed: the event fires on the bar where RSQR moves above
the 90% quantile of its own previous 500 bars, pointing the way the slope points.
Note: the source page could not be opened in the session that wrote this file, so the formula is written from the published definition as recalled.
"""
import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view

TRIGGER = dict(
    name="a158_rsqr",
    source="Microsoft Qlib, Alpha158 factor set (github.com/microsoft/qlib, qlib/contrib/data/loader.py), factors RSQR and BETA",
    summary="+1 when the last n closes become unusually close to a straight rising line, -1 for a straight falling line.",
    variants=[{"n": 20}, {"n": 60}],
    timed=False,
)


def event(df, p):
    n = int(p["n"]); c = df["close"].to_numpy(np.float64); N = len(c)
    slope = np.full(N, np.nan); r2 = np.full(N, np.nan)
    if N >= n:
        w = sliding_window_view(c, n)
        t = np.arange(n) - (n - 1) / 2.0
        y = w - w.mean(axis=1, keepdims=True)
        b = (y * t).sum(axis=1) / (t * t).sum()
        ss = (y * y).sum(axis=1)
        with np.errstate(divide="ignore", invalid="ignore"):
            r = (b * b * (t * t).sum()) / ss
        slope[n - 1:] = b; r2[n - 1:] = r
    r2 = pd.Series(r2, index=df.index)
    lim = r2.rolling(500).quantile(0.9).shift(1)
    high = (r2 > lim)
    start = (high & ~high.shift(1, fill_value=False)).to_numpy()
    return np.where(start & (slope > 0), 1, np.where(start & (slope < 0), -1, 0))
