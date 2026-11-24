"""TD Clopwin: a bar whose open and close both sit inside the previous bar's body.

Source: J. Perl, "DeMark Indicators" (2008), after Tom DeMark, as set out on the documentation page of the open-source
wickra indicator library (wickra-docs.pages.dev, TdClopwin), read on 2026-11-24 through a page-reading helper that
summarised the rule section.
Rule as read: the current open and close both lie within the span from the previous open to the previous close. The
signal is up if the bar closes at or above its open, down if below.
Kept: the rule. Changed: 1-hour bars instead of days, and a bar that closes exactly at its open gives no signal (the
page counts it as up), so that a flat bar is not a direction.
Not crabel_idnr or hikkake, which use an inside bar by high and low and wait for a break of it: here only the bodies
matter and the bar's own direction is the signal.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="td_clopwin",
    source='J. Perl, "DeMark Indicators" (2008), TD Clopwin, after T. DeMark; rule read at wickra-docs.pages.dev/Indicators/Indicator-TdClopwin',
    summary="The bar's open and close are both inside the previous bar's body: +1 if it closes above its open, -1 if below.",
    variants=[{"back": 1}],
    timed=False,
)


def event(df, p):
    k = int(p["back"]); o, c = df["open"], df["close"]
    lo = np.minimum(o.shift(k), c.shift(k)); hi = np.maximum(o.shift(k), c.shift(k))
    inside = (o >= lo) & (o <= hi) & (c >= lo) & (c <= hi)
    return np.where(inside & (c > o), 1, np.where(inside & (c < o), -1, 0))
