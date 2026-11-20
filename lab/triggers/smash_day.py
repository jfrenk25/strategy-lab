"""Smash-day reversal.

Source: L. Williams, "Long-Term Secrets to Short-Term Trading" (1999). A "smash day" closes below the previous day's
low (or above its high). If the very next day trades back through the smash day's opposite end, the breakout has
failed and the reversal is the trade.
Kept: the two-bar pattern and its direction. Changed: 1-hour bars instead of days, and the reversal must be a close
beyond the smash bar's high or low, not just a touch.
Note: the source could not be opened in the session that wrote this file, so the rule is written from the published description as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="smash_day",
    source='L. Williams, "Long-Term Secrets to Short-Term Trading" (1999), smash day reversals',
    summary="+1 when the previous bar closed below the low of the bar before it and this bar closes above the previous bar's high; -1 for the mirror image.",
    variants=[{"bars": 1}],
    timed=False,
)


def event(df, p):
    k = int(p["bars"]); h, l, c = df["high"], df["low"], df["close"]
    smash_dn = c.shift(k) < l.shift(k + 1)
    smash_up = c.shift(k) > h.shift(k + 1)
    return np.where(smash_dn & (c > h.shift(k)), 1, np.where(smash_up & (c < l.shift(k)), -1, 0))
