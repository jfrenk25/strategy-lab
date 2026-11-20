"""Three White Soldiers and Three Black Crows, as defined by Caginalp and Laurent.

Source: Caginalp and Laurent, "The Predictive Power of Price Patterns", Applied Mathematical Finance 5 (1998), 181-205. The definitions were read from the paper in the session that wrote this file.
Kept: the pattern (three up bars in a row with rising closes, each opening inside the body of the bar before, starting
in a downtrend; mirror image for the down side) and the paper's trend rule (see below).
Changed: 1-hour bars instead of days. The event is on bar 3. This is not the built-in streak: it needs a prior trend
the other way and each bar must open inside the previous body.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="cl_three_soldiers",
    source='Caginalp and Laurent, "The Predictive Power of Price Patterns", Applied Mathematical Finance 5 (1998), 181-205 (Three White Soldiers / Three Black Crows)',
    summary="+1 when, after a downtrend, three up bars in a row each open inside the previous body and close higher; -1 for three down bars after an uptrend.",
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
    bull = down & (c1 > o1) & (c2 > o2) & (c > o) & (c1 < c2) & (c2 < c) & (o1 < o2) & (o2 < c1) & (o2 < o) & (o < c2)
    bear = up & (o1 > c1) & (o2 > c2) & (o > c) & (c1 > c2) & (c2 > c) & (o1 > o2) & (o2 > c1) & (o2 > o) & (o > c2)
    return np.where(bull, 1, np.where(bear, -1, 0))
