"""Highs running up fast above their average (101 Formulaic Alphas: Alpha#23).

Source formula, in words: if the high is above the 20-bar average high, the alpha is minus the 2-bar change in the
high; otherwise zero.
Kept: the condition, the windows and the sign (a fast rise in highs points down). Changed: the 2-bar change is taken
as a fraction of the close and must be above the q-quantile of its own previous 500 bars. A mirror image on the lows
is added for the +1 side, which the source does not have.
Note: the source page could not be opened in the session that wrote this file, so the formula is written from the published definition as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="alpha023",
    source='Z. Kakushadze, "101 Formulaic Alphas" (2016), arXiv:1601.00991, Alpha#23',
    summary="-1 when the high is above its 20-bar average and has risen unusually fast over 2 bars; +1 for the mirror image on the lows.",
    variants=[{"q": 0.95}],
    timed=False,
)


def event(df, p):
    h, l, c = df["high"], df["low"], df["close"]
    dh = h.diff(2) / c.shift(2); dl = -l.diff(2) / c.shift(2)
    dh_lim = dh.rolling(500).quantile(p["q"]).shift(1); dl_lim = dl.rolling(500).quantile(p["q"]).shift(1)
    top = (h > h.rolling(20).mean()) & (dh > dh_lim)
    bot = (l < l.rolling(20).mean()) & (dl > dl_lim)
    return np.where(bot & ~top, 1, np.where(top & ~bot, -1, 0))
