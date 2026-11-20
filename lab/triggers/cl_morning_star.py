"""Morning Star and Evening Star, as defined by Caginalp and Laurent.

Source: Caginalp and Laurent, "The Predictive Power of Price Patterns", Applied Mathematical Finance 5 (1998), 181-205. The definitions were read from the paper in the session that wrote this file.
Kept: the pattern (bar 1 is a down bar in a downtrend; bar 2 opens and closes below bar 1's close; bar 3 is an up bar
closing above the middle of bar 1's body; mirror image for the down side) and the paper's trend rule (see below).
Changed: 1-hour bars instead of days. The event is on bar 3. The pattern needs a gap between bars, so it is rare on
markets that trade around the clock.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="cl_morning_star",
    source='Caginalp and Laurent, "The Predictive Power of Price Patterns", Applied Mathematical Finance 5 (1998), 181-205 (Morning Star / Evening Star)',
    summary="+1 when, after a downtrend, a down bar is followed by a bar that opens and closes below its close and then an up bar closing above the middle of the first bar's body; -1 for the mirror image after an uptrend.",
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
    mid = (o1 + c1) / 2
    bull = down & (o1 > c1) & (c1 > c2) & (c1 > o2) & (c > o) & (c > mid)
    bear = up & (c1 > o1) & (c2 > c1) & (o2 > c1) & (o2 != c2) & (o > c) & (c < mid)
    return np.where(bull, 1, np.where(bear, -1, 0))
