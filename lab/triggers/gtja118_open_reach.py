"""Reach above the open against reach below it, over 20 bars (Guotai Junan Alpha191: Alpha#118).

Source factor, read on 2026-11-23 from a public listing of the 191 formulas (bigquant.com/wiki/doc/Pyf0TYya6H):
    Alpha118 = SUM(HIGH - OPEN, 20) / SUM(OPEN - LOW, 20) * 100
How far bars travelled above their open, divided by how far they travelled below it. This is the "AR" sentiment
indicator of Chinese technical analysis.
Kept: the formula and its 20. Changed: nothing in the factor (the x100 is dropped, it does not move a quantile). The
event fires when the ratio first moves above the 95% quantile of its own previous 500 bars (+1) or below the 5%
quantile (-1).
Left out as near-copies of this one: Alpha#110 and Alpha#52 (the same ratio measured from the previous close or the
previous typical price, which on 24-hour markets is almost the open), and Alpha#69 with #93 and #187.
Not a repeat: a158_shadow looks at one bar's wick against its body; this adds 20 bars and ignores where they closed.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="gtja118_open_reach",
    source="Guotai Junan Securities, 191 short-horizon price-volume alpha factors (2017), Alpha#118, as listed at https://bigquant.com/wiki/doc/Pyf0TYya6H",
    summary="+1 when the 20-bar ratio of (high - open) to (open - low) first reaches a high extreme of its own past, -1 at a low extreme.",
    variants=[{"n": 20}],
    timed=False,
)


def event(df, p):
    n = int(p["n"]); o, h, l = df["open"], df["high"], df["low"]
    den = (o - l).rolling(n).sum()
    x = ((h - o).rolling(n).sum() / den.where(den > 0)).replace([np.inf, -np.inf], np.nan)
    hi = x.rolling(500).quantile(0.95).shift(1); lo = x.rolling(500).quantile(0.05).shift(1)
    up = x > hi; dn = x < lo
    return np.where(up & ~up.shift(1, fill_value=False), 1, np.where(dn & ~dn.shift(1, fill_value=False), -1, 0))
