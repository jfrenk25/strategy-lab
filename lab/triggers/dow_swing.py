"""Dow theory swing signal: a higher low followed by a break of the last swing high (and the mirror image).

Source: the Dow theory as set out by W. P. Hamilton, "The Stock Market Barometer" (1922), and R. Rhea, "The Dow
Theory" (1932); tested in Brown, Goetzmann and Kumar, "The Dow Theory: William Peter Hamilton's Track Record
Reconsidered", Journal of Finance 53(4), 1998. An uptrend is a run of higher swing highs and higher swing lows; the
buy signal comes when, after a higher low, the price moves above the previous swing high. The sell signal is the mirror.
Note: none of these sources was opened in the session that wrote this file, so the rule is written from the
published description as recalled. Dow's rule also asks two indices to confirm each other; that part needs a second
market and is left out.
Kept: swing highs and lows, the higher-low condition, and the signal on the close beyond the last swing high.
Changed: 1-hour bars and one market. Swings come from a zigzag: a turning point is confirmed once the close has moved
k times the market's own typical move away from it (typical move: the standard deviation of the last 500
close-to-close changes). Each swing high or low can give one signal only.
This is not the built-in breakout (highest of a fixed n bars): the level is the last confirmed swing, and the break
only counts after a higher low (lower high).
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="dow_swing",
    source='W. P. Hamilton, "The Stock Market Barometer" (1922); R. Rhea, "The Dow Theory" (1932); Brown, Goetzmann and Kumar, "The Dow Theory: William Peter Hamilton\'s Track Record Reconsidered", Journal of Finance 53(4), 1998',
    summary="+1 when the close moves above the last swing high after a swing low that was higher than the one before; -1 when it moves below the last swing low after a lower swing high.",
    variants=[{"k": 3}, {"k": 6}],
    timed=False,
)


def event(df, p):
    c = df["close"]; cv = c.to_numpy(dtype=float)
    cut = (p["k"] * c.diff().rolling(500).std()).to_numpy(dtype=float)
    out = np.zeros(len(cv), dtype=int)
    highs, lows = [], []                        # confirmed swing highs and lows (prices), oldest first
    leg, ext = 0, np.nan
    up_used = dn_used = True                    # has the latest swing high / low already given its signal?
    for i in range(len(cv)):
        x = cut[i]
        if not x > 0:
            continue
        px = cv[i]
        if leg == 0:
            leg, ext = 1, px
        elif leg == 1:
            if px >= ext:
                ext = px
            elif ext - px >= x:
                highs.append(ext); up_used = False
                leg, ext = -1, px
        else:
            if px <= ext:
                ext = px
            elif px - ext >= x:
                lows.append(ext); dn_used = False
                leg, ext = 1, px
        if not up_used and len(lows) >= 2 and lows[-1] > lows[-2] and px > highs[-1]:
            out[i] = 1; up_used = True
        elif not dn_used and len(highs) >= 2 and highs[-1] < highs[-2] and px < lows[-1]:
            out[i] = -1; dn_used = True
    return out
