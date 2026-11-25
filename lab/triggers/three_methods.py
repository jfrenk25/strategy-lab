"""Rising and falling three methods: a long bar, three small bars against it that stay inside its range, then a long
bar that carries on.

Source: the TA-Lib function CDLRISEFALL3METHODS (open-source library; the rule was read on its documentation page,
https://ta-lib.org/functions/cdlrisefall3methods.html, on 2026-11-25, through a helper that summarised it). The pattern
is from S. Nison, "Japanese Candlestick Charting Techniques", 1991 (not opened).
As read: five bars. Bar 1 has a long body. Bars 2 to 4 are small and of the other colour, and hold within bar 1's
high-low range. Bar 5 is long, of bar 1's colour. The output takes bar 1's colour: up for a white bar, down for black.
The page gives no numbers for "long" and "small" and does not check the trend before the pattern.
Kept: the five-bar shape and the sign.
Changed or added, because the page gives no numbers: "long" is a body larger than `k` times the average body of the
10 bars before it, "small" is a body smaller than that average; the bodies of bars 2 to 4 must lie inside bar 1's
high-low range; bar 5 must close beyond bar 1's close (the classic description, from recall). 1-hour bars, not days.
The event is on bar 5.
Not the built-in big_bar (one bar) or streak (bars in a row the same way), and not cl_three_inside or crabel_idnr
(one inside bar): here a long bar has to survive three bars of pullback and then be repeated.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="three_methods",
    source="TA-Lib, CDLRISEFALL3METHODS, https://ta-lib.org/functions/cdlrisefall3methods.html; pattern from S. Nison, Japanese Candlestick Charting Techniques, 1991",
    summary="+1 when a long up bar, three small down bars inside its range and a long up bar closing above the first follow one another; -1 for the mirror image.",
    variants=[{"k": 1.0}, {"k": 1.5}],
    timed=False,
)


def event(df, p):
    k = float(p["k"])
    o, h, l, c = df["open"], df["high"], df["low"], df["close"]
    body = (c - o).abs()
    avg = body.rolling(10).mean().shift(1)            # average body of the 10 bars before each bar
    long_ = body > k * avg
    small = body < avg
    up, dn = c > o, c < o
    top, bot = np.maximum(o, c), np.minimum(o, c)
    h1, l1, c1 = h.shift(4), l.shift(4), c.shift(4)

    def mids(colour):
        ok = pd.Series(True, index=df.index)
        for j in (1, 2, 3):
            ok &= colour.shift(j, fill_value=False) & small.shift(j, fill_value=False) & (top.shift(j) < h1) & (bot.shift(j) > l1)
        return ok

    rising = up.shift(4, fill_value=False) & long_.shift(4, fill_value=False) & mids(dn) & up & long_ & (c > c1)
    falling = dn.shift(4, fill_value=False) & long_.shift(4, fill_value=False) & mids(up) & dn & long_ & (c < c1)
    return np.where(rising, 1, np.where(falling, -1, 0))
