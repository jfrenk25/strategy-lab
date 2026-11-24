"""TD Line break: a close through the trendline drawn across the last two swing highs (or lows).

Source: T. DeMark, "The New Science of Technical Analysis" (1994), TD Points and TD Lines. Written from the published
definition as recalled; no page was opened for it in the session that wrote this file.
Rule: a TD Point high is a high with lower highs on both sides. The supply line joins the two most recent TD Point
highs when the later one is the lower, and is extended to the right. A close above it is a break upward. The demand
line joins the two most recent TD Point lows when the later one is the higher; a close below it is a break downward.
Kept: the points, the two-point line, and the break by a close.
Changed: 1-hour bars. A point needs k bars on each side (DeMark's basic point uses 1; 3 is his higher-level point).
A point is only used once the k bars after it have closed. The bar before the break must have closed on the other
side of the line, each line gives one signal, and DeMark's breakout qualifiers and price projections are left out.
Not the built-in breakout (a flat level: the highest high of n bars) and not dow_swing (a close beyond the last swing
high itself): the level here slopes, so a falling market can break upward well below its last swing high.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="td_line_break",
    source='T. DeMark, "The New Science of Technical Analysis" (1994), TD Points and TD Lines',
    summary="+1 when the close crosses above the falling line through the last two swing highs, -1 when it crosses below the rising line through the last two swing lows.",
    variants=[{"k": 1}, {"k": 3}],
    timed=False,
)


def event(df, p):
    k = int(p["k"]); h = df["high"].to_numpy(); l = df["low"].to_numpy(); c = df["close"].to_numpy(); n = len(c)
    out = np.zeros(n, dtype=int)
    hi = []; lo = []                    # confirmed points as (bar, price), newest last
    up_done = dn_done = True            # one signal per line
    for i in range(2 * k, n):
        j = i - k                       # the bar that may now be confirmed as a point
        win_h = h[j - k:i + 1]; win_l = l[j - k:i + 1]
        if h[j] == win_h.max() and (win_h == h[j]).sum() == 1:
            hi.append((j, h[j])); hi = hi[-2:]; up_done = False
        if l[j] == win_l.min() and (win_l == l[j]).sum() == 1:
            lo.append((j, l[j])); lo = lo[-2:]; dn_done = False
        up = dn = False
        if not up_done and len(hi) == 2 and hi[1][1] < hi[0][1]:
            (a, pa), (b, pb) = hi; slope = (pb - pa) / (b - a)
            if c[i] > pb + slope * (i - b) and c[i - 1] <= pb + slope * (i - 1 - b):
                up = True; up_done = True
        if not dn_done and len(lo) == 2 and lo[1][1] > lo[0][1]:
            (a, pa), (b, pb) = lo; slope = (pb - pa) / (b - a)
            if c[i] < pb + slope * (i - b) and c[i - 1] >= pb + slope * (i - 1 - b):
                dn = True; dn_done = True
        out[i] = 1 if (up and not dn) else (-1 if (dn and not up) else 0)
    return out
