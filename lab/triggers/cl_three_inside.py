"""Three Inside Up and Three Inside Down, as defined by Caginalp and Laurent.

Source: Caginalp and Laurent, "The Predictive Power of Price Patterns", Applied Mathematical Finance 5 (1998), 181-205. The paper tests eight three-day candlestick reversal patterns, defined by inequalities on opens and
closes only, each needing a prior trend: the 3-day average close must have moved one way over six days with at most
one exception. The definitions were read from the paper in the session that wrote this file.
Kept: the pattern (bar 1 is a down bar in a downtrend, bar 2's body sits inside bar 1's body, bar 3 is an up bar that
closes above bar 1's open; mirror image for the down side) and the paper's trend rule.
Changed: 1-hour bars instead of days. The event is on bar 3.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="cl_three_inside",
    source='Caginalp and Laurent, "The Predictive Power of Price Patterns", Applied Mathematical Finance 5 (1998), 181-205 (Three Inside Up / Three Inside Down)',
    summary="+1 when, after a downtrend, a down bar is followed by a bar whose body sits inside it and then an up bar closing above the first bar's open; -1 for the mirror image after an uptrend.",
    variants=[{"trend": 6}],
    timed=False,
)

def _trends(c):
    """The paper's trend: the 3-bar average close fell (rose) on at least 5 of the last 6 bars."""
    ma = c.rolling(3).mean()
    down = (ma < ma.shift(1)).astype(float).rolling(6).sum() >= 5
    up = (ma > ma.shift(1)).astype(float).rolling(6).sum() >= 5
    return down.shift(3, fill_value=False), up.shift(3, fill_value=False)       # judged on the bar before the pattern starts


def event(df, p):
    o, c = df["open"], df["close"]
    o1, c1, o2, c2 = o.shift(2), c.shift(2), o.shift(1), c.shift(1)
    down, up = _trends(c)
    same = (o2 == c1) & (c2 == o1)
    bull = down & (o1 > c1) & (o1 > o2) & (o2 >= c1) & (o1 >= c2) & (c2 > c1) & ~same & (c > o) & (c > o1)
    same = (o2 == c1) & (c2 == o1)
    bear = up & (c1 > o1) & (c1 >= o2) & (o2 > o1) & (c1 > c2) & (c2 >= o1) & ~same & (o > c) & (c < o1)
    return np.where(bull, 1, np.where(bear, -1, 0))
