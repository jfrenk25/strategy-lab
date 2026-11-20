"""Opening range breakout.

Source: T. Crabel, "Day Trading with Short Term Price Patterns and Opening Range Breakout" (1990); tested again in
Zarattini and Aziz, "Can Day Trading Really Be Profitable? Evidence of Sustainable Long-term Profits from Opening Range
Breakout (ORB) Day Trading Strategy vs. Benchmark in the US Stock Market" (2023, SSRN).
Kept: the high and low of the session's first bar form a range, and the first move out of it is the event.
Changed: 1-hour bars, so the range is the first hour. The session starts at a fixed UTC hour (0, 7 or 13: the lab's
Asia, London and New York opens), and only a close outside the range counts, once per side per UTC day. A day with no
bar at that hour gives no event.
Note: the source could not be opened in the session that wrote this file, so the rule is written from the published description as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="opening_range_break",
    source='T. Crabel, "Day Trading with Short Term Price Patterns and Opening Range Breakout" (1990); Zarattini and Aziz, "Can Day Trading Really Be Profitable?" (2023, SSRN)',
    summary="+1 at the first close above the high of the session's first hour, -1 at the first close below its low (same UTC day).",
    variants=[{"hour": 0}, {"hour": 7}, {"hour": 13}],
    timed=False,
)


def event(df, p):
    idx = df.index; day = idx.normalize(); first = idx.hour == int(p["hour"])
    c = df["close"]
    hi = df["high"].where(first).groupby(day).ffill()
    lo = df["low"].where(first).groupby(day).ffill()
    up = (c > hi) & ~first; dn = (c < lo) & ~first
    up1 = up & (up.groupby(day).cumsum() == 1)
    dn1 = dn & (dn.groupby(day).cumsum() == 1)
    return np.where(up1, 1, np.where(dn1, -1, 0))
