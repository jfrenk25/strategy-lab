"""Ease of movement reaches an extreme (Guotai Junan Alpha191: Alpha#9 and Alpha#68).

Source factors, read on 2026-11-23 from a public listing of the 191 formulas (bigquant.com/wiki/doc/Pyf0TYya6H):
    Alpha9  = SMA( ((HIGH+LOW)/2 - (DELAY(HIGH,1)+DELAY(LOW,1))/2) * (HIGH-LOW) / VOLUME, 7, 2 )
    Alpha68 = the same with SMA(., 15, 2).
The move of the bar's midpoint is multiplied by the bar's range and divided by its volume: a large value means price
travelled far on little volume. This is Arms' ease-of-movement measure.
SMA(A, n, m) is taken as Y = (m x A + (n - m) x Y_before) / n. The listing does not define it; that meaning is from recall.
Kept: the formula and the two smoothings (7 and 15). Changed: nothing in the factor; a bar with zero volume is left
out. The event fires when the factor first moves above the 95% quantile of its own previous 500 bars (+1) or below
the 5% quantile (-1). Comparing with its own past removes the price and volume scale.
Not a repeat: vol_spike fires on high volume, big_bar on a large bar; this fires on distance travelled per unit of volume.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="gtja009_ease_of_movement",
    source="Guotai Junan Securities, 191 short-horizon price-volume alpha factors (2017), Alpha#9 and Alpha#68, as listed at https://bigquant.com/wiki/doc/Pyf0TYya6H",
    summary="+1 when smoothed ease of movement (midpoint move x range / volume) first reaches a high extreme of its own past, -1 at a low extreme.",
    variants=[{"n": 7}, {"n": 15}],
    timed=False,
)


def event(df, p):
    n = int(p["n"]); h, l, v = df["high"], df["low"], df["volume"]
    mid = (h + l) / 2.0
    a = ((mid - mid.shift(1)) * (h - l) / v.where(v > 0)).replace([np.inf, -np.inf], np.nan)
    x = a.ewm(alpha=2.0 / n, adjust=False, ignore_na=True).mean()      # SMA(A, n, 2)
    hi = x.rolling(500).quantile(0.95).shift(1); lo = x.rolling(500).quantile(0.05).shift(1)
    up = x > hi; dn = x < lo
    return np.where(up & ~up.shift(1, fill_value=False), 1, np.where(dn & ~dn.shift(1, fill_value=False), -1, 0))
