"""TD Differential and TD Reverse Differential (Thomas DeMark).

Source: DeMark, "New Market Timing Techniques" (Wiley, 1997). The conditions were read on 2026-11-23 from a public
description of the pattern (litefinance.org, "A set of differential tools by Thomas DeMark"), not from the book.
    true low  = the lower of the bar's low and the previous close;  true high = the higher of the high and the previous close
    buying pressure = close - true low;  selling pressure = true high - close
TD Differential (variant reverse = 0), a reversal signal:
    +1: two closes in a row each below the one before, buying pressure above the previous bar's, selling pressure below it.
    -1: two closes in a row each above the one before, selling pressure above the previous bar's, buying pressure below it.
TD Reverse Differential (variant reverse = 1), described as a continuation signal:
    -1: two lower closes, buying pressure below the previous bar's, selling pressure above it.
    +1: two higher closes, buying pressure above the previous bar's, selling pressure below it.
Kept: every condition as described. Changed: nothing. The description says the pattern suits 4-hour bars and longer;
the lab has 1-hour bars. TD Anti-Differential was left out: the description read contradicts itself.
Not a repeat: streak needs three or more closes and nothing else; td_setup compares closes four bars apart.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="td_differential",
    source="Thomas DeMark, New Market Timing Techniques (Wiley, 1997), TD Differential and TD Reverse Differential, as described at https://www.litefinance.org/blog/for-professionals/a-set-of-differential-tools-by-thomas-demark-td-differential-td-anti-differential-td-reverse-differential/",
    summary="reverse=0: +1 after two lower closes with buying pressure rising and selling pressure falling, -1 for the mirror. reverse=1: the continuation version, with the pressure conditions swapped.",
    variants=[{"reverse": 0}, {"reverse": 1}],
    timed=False,
)


def event(df, p):
    c, h, l = df["close"], df["high"], df["low"]
    c1 = c.shift(1)
    bp = c - np.minimum(l, c1); sp = np.maximum(h, c1) - c
    two_down = (c < c1) & (c1 < c.shift(2)); two_up = (c > c1) & (c1 > c.shift(2))
    bp_up = bp > bp.shift(1); bp_dn = bp < bp.shift(1); sp_up = sp > sp.shift(1); sp_dn = sp < sp.shift(1)
    if int(p["reverse"]) == 0:
        return np.where(two_down & bp_up & sp_dn, 1, np.where(two_up & sp_up & bp_dn, -1, 0))
    return np.where(two_down & bp_dn & sp_up, -1, np.where(two_up & bp_up & sp_dn, 1, 0))
