"""TD Sequential countdown: thirteen further closes beyond the low (high) two bars earlier, after a completed setup.

Source: T. DeMark, "The New Science of Technical Analysis" (1994); J. Perl, "DeMark Indicators" (2008). Written from
the published definition as recalled; no page was opened for it in the session that wrote this file.
Rule: a buy setup is nine closes in a row each below the close four bars earlier (the lab's td_setup trigger). From the
bar that completes it, count every bar whose close is at or below the low two bars earlier. The bars need not be in a
row. The thirteenth such bar is the buy signal. The sell side is the mirror: nine closes above the close four bars
earlier, then thirteen closes at or above the high two bars earlier.
Kept: the setup of nine, the countdown of thirteen and the comparison two bars back.
Changed: 1-hour bars. A countdown is dropped when a setup the other way completes, and starts again from zero when a
new setup the same way completes; the book's other cancel rules (a close beyond the setup's far extreme) and its extra
demand on the thirteenth bar are left out.
Not td_setup with another number: the setup only arms this event, and the signal comes many bars later, after the
move has gone on.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="td_countdown",
    source='T. DeMark, "The New Science of Technical Analysis" (1994), TD Sequential countdown; J. Perl, "DeMark Indicators" (2008)',
    summary="+1 at the 13th close at or below the low two bars earlier after nine closes in a row below the close four bars earlier; -1 for the mirror image.",
    variants=[{"setup": 9, "count": 13}],
    timed=False,
)


def event(df, p):
    ks, kc = int(p["setup"]), int(p["count"])
    c = df["close"].to_numpy(); h = df["high"].to_numpy(); l = df["low"].to_numpy(); n = len(c)
    out = np.zeros(n, dtype=int); nb = na = 0; side = 0; cnt = 0
    for i in range(4, n):
        nb = nb + 1 if c[i] < c[i - 4] else 0
        na = na + 1 if c[i] > c[i - 4] else 0
        if nb == ks: side, cnt = 1, 0                      # a buy setup arms (or re-arms) the buy countdown
        elif na == ks: side, cnt = -1, 0
        if side == 1 and c[i] <= l[i - 2]:
            cnt += 1
        elif side == -1 and c[i] >= h[i - 2]:
            cnt += 1
        if side != 0 and cnt == kc:
            out[i] = side; side, cnt = 0, 0
    return out
