"""TD Clop: a bar that opens beyond the previous bar's open and close and then closes back through both.

Source: J. Perl, "DeMark Indicators" (2008), after Tom DeMark, as set out on the documentation page of the open-source
wickra indicator library (wickra-docs.pages.dev, TdClop), read on 2026-11-24 through a page-reading helper that
summarised the rule section.
Rule as read: buy when the open is below both the previous open and the previous close, and the close is above both.
Sell is the mirror. Highs and lows are not used.
Kept: the four comparisons. Changed: 1-hour bars instead of days. On markets that trade round the clock a bar seldom
opens away from the previous close, so this fires mostly after a pause in trading or a fast market.
Not the built-in gap (the open against the previous range, with no demand on the close) and not an engulfing bar by
range: only the previous bar's open and close matter.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="td_clop",
    source='J. Perl, "DeMark Indicators" (2008), TD Clop, after T. DeMark; rule read at wickra-docs.pages.dev/Indicators/Indicator-TdClop',
    summary="+1 when the bar opens below the previous bar's open and close and closes above both; -1 for the mirror image.",
    variants=[{"back": 1}],
    timed=False,
)


def event(df, p):
    k = int(p["back"]); o, c = df["open"], df["close"]
    po, pc = o.shift(k), c.shift(k)
    buy = (o < po) & (o < pc) & (c > po) & (c > pc)
    sell = (o > po) & (o > pc) & (c < po) & (c < pc)
    return np.where(buy, 1, np.where(sell, -1, 0))
