"""Far from the fitted trend line (Qlib Alpha158: RESI).

Source factor: RESI(n) is the last close minus the value of a straight line fitted to the last n closes, over the close.
Kept: the factor and the 20 and 60 bar windows. Changed: the event fires when RESI first moves more than 2 of its own
standard deviations (previous 500 bars) away from zero.
Note: the source page could not be opened in the session that wrote this file, so the formula is written from the published definition as recalled.
"""
import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view

TRIGGER = dict(
    name="a158_resi",
    source="Microsoft Qlib, Alpha158 factor set (github.com/microsoft/qlib, qlib/contrib/data/loader.py), factor RESI",
    summary="+1 when the close first stands unusually far above the line fitted to the last n closes, -1 when unusually far below.",
    variants=[{"n": 20}, {"n": 60}],
    timed=False,
)


def event(df, p):
    n = int(p["n"]); c = df["close"].to_numpy(np.float64); N = len(c)
    resi = np.full(N, np.nan)
    if N >= n:
        w = sliding_window_view(c, n)
        t = np.arange(n) - (n - 1) / 2.0
        m = w.mean(axis=1)
        b = ((w - m[:, None]) * t).sum(axis=1) / (t * t).sum()
        fitted_last = m + b * t[-1]
        resi[n - 1:] = (w[:, -1] - fitted_last) / w[:, -1]
    resi = pd.Series(resi, index=df.index)
    z = resi / resi.rolling(500).std().shift(1)
    zp = z.shift(1)
    return np.where((z > 2) & (zp <= 2), 1, np.where((z < -2) & (zp >= -2), -1, 0))
