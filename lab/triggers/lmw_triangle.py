"""Triangle top and bottom (Lo, Mamaysky and Wang).

Source: Lo, Mamaysky and Wang, "Foundations of Technical Analysis: Computational Algorithms, Statistical Inference, and Empirical Implementation", Journal of Finance 55(4), 2000, 1705-1765.
The paper defines ten chart patterns as conditions on consecutive local highs and lows E1, E2, ... of a smoothed
closing-price series, all inside a 35-day window, and treats a pattern as seen 3 days after its last turning point.
The definitions were read from the paper in the session that wrote this file (a copy of the PDF; some inequality
signs were lost in extraction and were restored from the paper's wording).
Kept: five turning points in a row inside 35 bars. Top: E1 a high, E1 > E3 > E5 and E2 < E4 (lower highs, higher lows).
Bottom: E1 a low, E1 < E3 < E5 and E2 > E4.
Changed: 1-hour bars instead of days. The paper finds turning points with a kernel regression; here a turning point
is a close that is the highest (lowest) of the w bars on each side, so it is known w bars later, and w = 3 matches
the paper's 3-day wait. Two highs or two lows in a row keep the more extreme one. This pattern has no tolerance, so nothing depends on the price scale.
The paper gives no direction to any pattern. By the usual convention a top points down (-1) and a bottom points up (+1);
the screen tries both ways anyway.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="lmw_triangle",
    source='Lo, Mamaysky and Wang, "Foundations of Technical Analysis: Computational Algorithms, Statistical Inference, and Empirical Implementation", Journal of Finance 55(4), 2000, 1705-1765 (Triangle top and bottom)',
    summary='-1 when five turning points starting with a high make lower highs and higher lows; +1 when five starting with a low make higher lows and lower highs.',
    variants=[{"w": 3}],
    timed=False,
)

def _pattern(T, E, K, s):
    if len(E) < 5 or T[-1] - T[-5] > 35:
        return 0
    e1, e2, e3, e4, e5 = E[-5:]
    if K[-5] == 1 and e1 > e3 > e5 and e2 < e4:
        return -1
    if K[-5] == -1 and e1 < e3 < e5 and e2 > e4:
        return 1
    return 0


def _turning_points(c, w):
    """Positions where a turning point becomes known: bar i confirms that bar i - w was a local high or low of the close."""
    span = 2 * w + 1
    mid = c.shift(w)
    is_max = (mid == c.rolling(span).max()).to_numpy()
    is_min = (mid == c.rolling(span).min()).to_numpy()
    return is_max, is_min


def event(df, p):
    c = df["close"]; w = int(p["w"]); cv = c.to_numpy(dtype=float)
    sigma = c.diff().rolling(500).std().to_numpy()          # the market's own typical 1-bar move, up to this bar
    is_max, is_min = _turning_points(c, w)
    out = np.zeros(len(c), dtype=int)
    T, E, K = [], [], []                                    # position, price and kind (+1 high, -1 low) of each turning point
    for i in np.flatnonzero(is_max ^ is_min):
        kind = 1 if is_max[i] else -1; price = cv[i - w]
        if K and K[-1] == kind:
            if (price - E[-1]) * kind <= 0:
                continue                                    # not more extreme than the last one of the same kind
            T[-1], E[-1] = i - w, price
        else:
            T.append(i - w); E.append(price); K.append(kind)
        out[i] = _pattern(T, E, K, sigma[i])
    return out
