"""Volatility carried by falling bars is unusually high or low (Guotai Junan Alpha191: Alpha#160).

Source factor, read on 2026-11-22 from the techfactor package documentation (shrektan.github.io/techfactor), which
reproduces it from the Guotai Junan Securities report on 191 short-horizon price-volume factors (2017):
    Alpha160 = SMA( CLOSE <= DELAY(CLOSE, 1) ? STD(CLOSE, 20) : 0, 20, 1 )
The 20-bar standard deviation of the close is counted only on bars that did not close up, then smoothed.
SMA(A, n, m) is taken as Y = (m x A + (n - m) x Y_before) / n, the usual meaning in that report; the page read does
not define it, so that part is from recall.
Kept: the formula and its two 20s. Changed: the standard deviation is divided by the close so the value does not
depend on the price level, and the event fires when the factor first moves above the 95% quantile of its own previous
500 bars (-1: falling bars have carried a lot of volatility) or below the 5% quantile (+1).
The rest of the Alpha191 list could not be read on 2026-11-22.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="gtja160_down_vol",
    source="Guotai Junan Securities, 191 short-horizon price-volume alpha factors (2017), Alpha#160, as documented at https://shrektan.github.io/techfactor",
    summary="-1 when volatility on non-rising bars (Alpha#160) first reaches a high extreme of its own past, +1 when it first reaches a low extreme.",
    variants=[{"n": 20}],
    timed=False,
)


def event(df, p):
    n = int(p["n"]); c = df["close"]
    a = (c.rolling(n).std(ddof=1) / c).where(c <= c.shift(1), 0.0)
    a = a.where(c.rolling(n).count() == n)                           # undefined until the window is full
    x = a.ewm(alpha=1.0 / n, adjust=False, ignore_na=True).mean()    # SMA(A, n, 1)
    hi = x.rolling(500).quantile(0.95).shift(1); lo = x.rolling(500).quantile(0.05).shift(1)
    up = x > hi; dn = x < lo
    return np.where(up & ~up.shift(1, fill_value=False), -1, np.where(dn & ~dn.shift(1, fill_value=False), 1, 0))
