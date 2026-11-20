"""Hikkake: an inside bar, a false break one way, then a move out the other side.

Source: D. Chesler, "Trading False Moves with the Hikkake Pattern" (Active Trader, 2004), as summarised on
en.wikipedia.org/wiki/Hikkake_pattern, which was read in the session that wrote this file.
Rule: an inside bar (lower high and higher low than the bar before). The next bar has a lower low and a lower high
(a false move down). If price then passes above the inside bar's high within three bars, the pattern points up.
Mirror image for the down side.
Kept: the pattern and the three-bar limit. Changed: 1-hour bars, and the confirmation is the first close beyond the
inside bar's high or low, not a touch.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="hikkake",
    source='D. Chesler, "Trading False Moves with the Hikkake Pattern", Active Trader (2004); summary at en.wikipedia.org/wiki/Hikkake_pattern',
    summary="+1 at the first close above an inside bar's high within three bars of a false break below it, -1 for the mirror image.",
    variants=[{"bars": 3}],
    timed=False,
)


def event(df, p):
    h, l, c = df["high"], df["low"], df["close"]
    inside = (h < h.shift(1)) & (l > l.shift(1))
    fake_dn = inside.shift(1, fill_value=False) & (l < l.shift(1)) & (h < h.shift(1))     # true on the false-break bar
    fake_up = inside.shift(1, fill_value=False) & (h > h.shift(1)) & (l > l.shift(1))
    bull = pd.Series(False, index=df.index); bear = pd.Series(False, index=df.index)
    for k in range(1, int(p["bars"]) + 1):                 # this bar is k bars after the false-break bar
        top = h.shift(k + 1); bot = l.shift(k + 1)         # the inside bar's high and low
        first_up = c > top; first_dn = c < bot
        for j in range(1, k):                              # no earlier close already confirmed it
            first_up &= ~(c.shift(j) > top); first_dn &= ~(c.shift(j) < bot)
        bull |= fake_dn.shift(k, fill_value=False) & first_up
        bear |= fake_up.shift(k, fill_value=False) & first_dn
    return np.where(bull & ~bear, 1, np.where(bear & ~bull, -1, 0))
