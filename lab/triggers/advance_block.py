"""Advance block: three up bars in a row that are running out of push.

Source: the TA-Lib function CDLADVANCEBLOCK (open-source library; the rule was read on its documentation page,
https://ta-lib.org/functions/cdladvanceblock.html, on 2026-11-25, through a helper that summarised it). The pattern is
from S. Nison, "Japanese Candlestick Charting Techniques", 1991 (not opened).
As read: three white bars with rising closes, where the advance weakens: the bodies get smaller and/or the upper
shadows get longer. The output is always bearish. The page gives no numbers, does not check the trend before the
pattern, and notes that Bulkowski found the pattern carries on upward more often than it turns.
Kept: three up bars, rising closes, shrinking bodies, a growing upper shadow, and the bearish sign (-1).
Changed or added: both signs of weakening are required (each body smaller than the one before, and the third bar's
upper shadow longer than the first bar's and at least `shadow` times its own body), so the event is not just any
three up bars. The mirror image (three down bars with shrinking bodies and a growing lower shadow, +1) is the lab's
addition, so the trigger has both signs. 1-hour bars, not days. The event is on bar 3.
The related "stalled pattern" (CDLSTALLEDPATTERN, also read) was left out as a near-copy of this one.
Not the built-in streak or cl_three_soldiers (three strong bars): this asks for three bars that weaken.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="advance_block",
    source="TA-Lib, CDLADVANCEBLOCK, https://ta-lib.org/functions/cdladvanceblock.html; pattern from S. Nison, Japanese Candlestick Charting Techniques, 1991",
    summary="-1 when three up bars with rising closes have shrinking bodies and a growing upper shadow; +1 for three down bars with shrinking bodies and a growing lower shadow.",
    variants=[{"shadow": 0.5}, {"shadow": 1.0}],
    timed=False,
)


def event(df, p):
    s = float(p["shadow"])
    o, h, l, c = df["open"], df["high"], df["low"], df["close"]
    body = (c - o).abs()
    us = h - np.maximum(o, c)
    ls = np.minimum(o, c) - l
    up, dn = c > o, c < o
    shrink = (body < body.shift(1)) & (body.shift(1) < body.shift(2))
    block = up & up.shift(1, fill_value=False) & up.shift(2, fill_value=False) & (c > c.shift(1)) & (c.shift(1) > c.shift(2)) \
        & shrink & (us > us.shift(2)) & (us >= s * body)
    mirror = dn & dn.shift(1, fill_value=False) & dn.shift(2, fill_value=False) & (c < c.shift(1)) & (c.shift(1) < c.shift(2)) \
        & shrink & (ls > ls.shift(2)) & (ls >= s * body)
    return np.where(block, -1, np.where(mirror, 1, 0))
