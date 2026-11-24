"""TD Camouflage: a bar that closes down on the day but up from its own open, after dipping under the bar before.

Source: T. DeMark, "The New Science of Technical Analysis" (1994) and J. Perl, "DeMark Indicators" (2008), as set out on
the documentation page of the open-source wickra indicator library (wickra-docs.pages.dev, TdCamouflage), read on
2026-11-24 through a page-reading helper that summarised the rule section.
Rule as read: buy when the close is below the previous close, above the bar's own open, and the low is below the
previous low. Sell is the mirror: close above the previous close, below the bar's own open, high above the previous high.
Kept: the three comparisons, on two bars. Changed: 1-hour bars instead of days. Some descriptions add a comparison with
the close two bars back; the page read does not, and neither does this file.
Not the built-in sweep (a break of a many-bar extreme that closes back) nor a158_shadow (the size of a wick): this is
the hidden strength of a bar that looks weak against the previous close.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="td_camouflage",
    source='T. DeMark, "The New Science of Technical Analysis" (1994); J. Perl, "DeMark Indicators" (2008); rule read at wickra-docs.pages.dev/Indicators/Indicator-TdCamouflage',
    summary="+1 when the close is below the previous close but above the open and the low is under the previous low; -1 for the mirror image.",
    variants=[{"back": 1}],
    timed=False,
)


def event(df, p):
    k = int(p["back"]); o, h, l, c = df["open"], df["high"], df["low"], df["close"]
    buy = (c < c.shift(k)) & (c > o) & (l < l.shift(k))
    sell = (c > c.shift(k)) & (c < o) & (h > h.shift(k))
    return np.where(buy, 1, np.where(sell, -1, 0))
