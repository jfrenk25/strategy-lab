"""Tweezer top and tweezer bottom: two bars in a row stop at the same price at the edge of the recent range.

Source: S. Nison, "Japanese Candlestick Charting Techniques", 1991 (tweezer tops and bottoms). The pattern is among
those tested by Marshall, Young and Rose, "Candlestick technical trading strategies: Can they create value for
investors?", Journal of Banking and Finance 30(8), 2006. Written from the published description as recalled; neither
source was opened.
Tweezer top: after a rise, a bar that closes up is followed by a bar that closes down, and the two highs match.
Tweezer bottom is the mirror image with matching lows.
Kept: the two-bar shape and the matching extremes. Changed: "matching" is made exact as within a tenth of the 24-bar
average bar range, and "after a rise" as the shared high being the highest high of the last n bars (the lowest low
for a bottom). The event is -1 for a top and +1 for a bottom.
Not the built-in sweep (a bar that pokes through an old extreme and closes back), nor cl_three_inside or
a158_shadow: here two bars test one price and nothing needs a long shadow or an inside bar.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="tweezer",
    source='S. Nison, "Japanese Candlestick Charting Techniques", 1991; Marshall, Young and Rose, Journal of Banking and Finance 30(8), 2006',
    summary="-1 when an up bar and then a down bar share the same high at an n-bar high, +1 when a down bar and then an up bar share the same low at an n-bar low.",
    variants=[{"n": 12}, {"n": 48}],
    timed=False,
)


def event(df, p):
    n = int(p["n"]); o, h, l, c = df["open"], df["high"], df["low"], df["close"]
    tol = 0.1 * (h - l).rolling(24).mean().shift(1)
    up, dn = c > o, c < o
    top = up.shift(1, fill_value=False) & dn & ((h - h.shift(1)).abs() <= tol) & (np.maximum(h, h.shift(1)) >= h.rolling(n).max())
    bot = dn.shift(1, fill_value=False) & up & ((l - l.shift(1)).abs() <= tol) & (np.minimum(l, l.shift(1)) <= l.rolling(n).min())
    return np.where(top, -1, np.where(bot, 1, 0))
