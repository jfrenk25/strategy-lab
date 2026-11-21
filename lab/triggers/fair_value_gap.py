"""Fair value gap: a three-bar price gap left by a fast move.

Source: NinjaTrader, "The Ultimate Guide to Trading Fair Value Gaps" (public guide, ninjatrader.com/futures/blogs/fair-value-gaps,
July 2026), read in the session that wrote this file. The same event is one of the building blocks of the "ICT"
method examined in Taylor, "Evaluating the Predictive Validity of ICT's Accumulation-Manipulation-Distribution Model
on CME E-Mini NASDAQ-100 Futures", arXiv:2610.35887, which lists it as future work.
The guide's definition: three bars in a row; a bullish gap when the high of bar 1 is below the low of bar 3, a bearish
gap when the low of bar 1 is above the high of bar 3. The middle bar is the fast move. The guide says price often
comes back to the gap before carrying on, and gives no statistics.
Kept: the three-bar definition. The event is on bar 3, the first bar on which the gap is known.
Changed: the gap must be at least k times the market's own average bar range of the 24 bars before the pattern, so
that gaps of a tick or two do not count. The guide's "wait for price to return to the gap" entry is not coded: the
event is the gap itself, and the screen tries both following and fading it.
This is not the built-in gap trigger (open against the previous close) and not big_bar (one bar's size and close position).
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="fair_value_gap",
    source='NinjaTrader, "The Ultimate Guide to Trading Fair Value Gaps", ninjatrader.com/futures/blogs/fair-value-gaps (2026); see also Taylor, arXiv:2610.35887',
    summary="+1 when a bar's low is above the high of the bar two bars back by at least k average ranges; -1 when its high is below that bar's low by as much.",
    variants=[{"k": 0.25}, {"k": 1.0}],
    timed=False,
)


def event(df, p):
    h, l = df["high"], df["low"]
    avg_range = (h - l).rolling(24).mean().shift(3)         # the 24 bars before the three-bar pattern
    up = (l - h.shift(2)) >= p["k"] * avg_range
    dn = (l.shift(2) - h) >= p["k"] * avg_range
    ok = avg_range > 0
    return np.where(up & ok, 1, np.where(dn & ok, -1, 0))
