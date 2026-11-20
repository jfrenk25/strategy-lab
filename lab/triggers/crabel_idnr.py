"""Inside bar with the narrowest range, then a close outside it (Crabel's ID/NR4 pattern).

Source: T. Crabel, "Day Trading with Short Term Price Patterns and Opening Range Breakout" (1990). An inside day that
also has the narrowest range of the last four days marks a contraction, and the move out of it tends to run.
Kept: the pattern (inside bar, narrowest range of the last n bars, n of 4 or 7) and the break of that bar as the event.
Changed: 1-hour bars instead of days, and the break is a close beyond the pattern bar's high or low on the next bar.
This is not the built-in squeeze_break, which looks at the width of a many-bar range.
Note: the source could not be opened in the session that wrote this file, so the rule is written from the published description as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="crabel_idnr",
    source='T. Crabel, "Day Trading with Short Term Price Patterns and Opening Range Breakout" (1990), ID/NR4 and NR7 patterns',
    summary="The previous bar sat inside the bar before it and had the narrowest range of n bars: +1 if this bar closes above its high, -1 if below its low.",
    variants=[{"n": 4}, {"n": 7}],
    timed=False,
)


def event(df, p):
    n = int(p["n"]); h, l, c = df["high"], df["low"], df["close"]
    rng = h - l
    inside = (h.shift(1) <= h.shift(2)) & (l.shift(1) >= l.shift(2))
    narrow = rng.shift(1) <= rng.rolling(n).min().shift(1)
    setup = inside & narrow
    return np.where(setup & (c > h.shift(1)), 1, np.where(setup & (c < l.shift(1)), -1, 0))
