"""Three Outside Up and Three Outside Down, as defined by Caginalp and Laurent.

Source: Caginalp and Laurent, "The Predictive Power of Price Patterns", Applied Mathematical Finance 5 (1998), 181-205. The definitions were read from the paper in the session that wrote this file.
Kept: the pattern (bar 1 is a down bar in a downtrend, bar 2 is an up bar whose body swallows bar 1's body, bar 3 is
an up bar closing above bar 2's close; mirror image for the down side) and the paper's trend rule (see below).
Changed: 1-hour bars instead of days. The event is on bar 3. On markets that trade around the clock a bar usually
opens at the previous close, so the strict "opens beyond the previous close" part makes this pattern rare there.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="cl_three_outside",
    source='Caginalp and Laurent, "The Predictive Power of Price Patterns", Applied Mathematical Finance 5 (1998), 181-205 (Three Outside Up / Three Outside Down)',
    summary="+1 when, after a downtrend, a down bar is swallowed by an up bar and the next bar is an up bar closing higher still; -1 for the mirror image after an uptrend.",
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
    bigger = (c2 - o2).abs() >= (c1 - o1).abs()
    bull = down & (o1 > c1) & (c2 > o1) & (c1 > o2) & bigger & (c > o) & (c > c2)
    bear = up & (c1 > o1) & (o2 > c1) & (o1 > c2) & bigger & (o > c) & (c < c2)
    return np.where(bull, 1, np.where(bear, -1, 0))
