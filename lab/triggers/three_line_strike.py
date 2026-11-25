"""Three-line strike: three bars in a row one way, then one bar that wipes out all three.

Source: the TA-Lib function CDL3LINESTRIKE (open-source library; the rule was read on its documentation page,
https://ta-lib.org/functions/cdl3linestrike.html, on 2026-11-25, through a helper that summarised it).
As read: four bars. Bars 1 to 3 have the same colour and closes that step the same way; bars 2 and 3 each open inside
or near the body of the bar before. Bar 4 has the other colour, opens beyond bar 3's close and closes past bar 1's
open. The output takes the colour of the first three bars (up for white), so the library reads it as the old move
carrying on; the page notes that Bulkowski found it turns more often than it carries on. The trend before the pattern
is not checked.
Kept: the four-bar shape and the library's sign (+1 when the first three bars are up bars). The screen tries the
follow and the fade side, which covers both readings.
Changed: "opens inside or near the previous body" and "opens beyond bar 3's close" allow a slack of a tenth of the
24-bar average bar range, because a round-the-clock market opens each bar at about the last close and almost never
beyond it. 1-hour bars, not days. The event is on bar 4.
Not the built-in streak (which stops at the run) nor big_bar (one large bar, whatever came before): the fourth bar
has to undo exactly the three-bar run before it.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="three_line_strike",
    source="TA-Lib, CDL3LINESTRIKE, https://ta-lib.org/functions/cdl3linestrike.html",
    summary="+1 when three up bars with rising closes are followed by a down bar that closes below the first bar's open; -1 for three down bars and an up bar closing above the first bar's open.",
    variants=[{"slack": 0.1}],
    timed=False,
)


def event(df, p):
    o, h, l, c = df["open"], df["high"], df["low"], df["close"]
    tol = float(p["slack"]) * (h - l).rolling(24).mean().shift(1)
    up, dn = c > o, c < o
    top, bot = np.maximum(o, c), np.minimum(o, c)

    def inside_prev(j):                      # bar j bars back opens inside or near the body of the bar before it
        return (o.shift(j) <= top.shift(j + 1) + tol) & (o.shift(j) >= bot.shift(j + 1) - tol)

    three_up = up.shift(3, fill_value=False) & up.shift(2, fill_value=False) & up.shift(1, fill_value=False) \
        & (c.shift(2) > c.shift(3)) & (c.shift(1) > c.shift(2)) & inside_prev(2) & inside_prev(1)
    three_dn = dn.shift(3, fill_value=False) & dn.shift(2, fill_value=False) & dn.shift(1, fill_value=False) \
        & (c.shift(2) < c.shift(3)) & (c.shift(1) < c.shift(2)) & inside_prev(2) & inside_prev(1)
    bull = three_up & dn & (o >= c.shift(1) - tol) & (c < o.shift(3))
    bear = three_dn & up & (o <= c.shift(1) + tol) & (c > o.shift(3))
    return np.where(bull, 1, np.where(bear, -1, 0))
