"""Double top and double bottom (Lo, Mamaysky and Wang).

Source: Lo, Mamaysky and Wang, "Foundations of Technical Analysis: Computational Algorithms, Statistical Inference, and Empirical Implementation", Journal of Finance 55(4), 2000, 1705-1765.
The paper defines ten chart patterns as conditions on consecutive local highs and lows E1, E2, ... of a smoothed
closing-price series, all inside a 35-day window, and treats a pattern as seen 3 days after its last turning point.
The definitions were read from the paper in the session that wrote this file (a copy of the PDF; some inequality
signs were lost in extraction and were restored from the paper's wording).
Kept: a high E1 and the highest high after it, Ea, close to their average and more than 22 bars apart, both
inside the 35-bar window. Mirror image for the double bottom.
Changed: 1-hour bars instead of days. The paper finds turning points with a kernel regression; here a turning point
is a close that is the highest (lowest) of the w bars on each side, so it is known w bars later, and w = 3 matches
the paper's 3-day wait. Two highs or two lows in a row keep the more extreme one. "Within 1.5 percent of
their average" (a daily-stock scale) becomes "within 0.75 of the market's own typical 1-bar move". The event is on the bar that
confirms the second top or bottom.
The paper gives no direction to any pattern. By the usual convention a top points down (-1) and a bottom points up (+1);
the screen tries both ways anyway.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="lmw_double",
    source='Lo, Mamaysky and Wang, "Foundations of Technical Analysis: Computational Algorithms, Statistical Inference, and Empirical Implementation", Journal of Finance 55(4), 2000, 1705-1765 (Double top and double bottom)',
    summary='-1 when a new high matches an earlier high 23 to 35 bars back with no higher high between them; +1 for two matching lows.',
    variants=[{"w": 3}],
    timed=False,
)

def _pattern(T, E, K, s):
    if len(E) < 3 or not s > 0:
        return 0
    kind, ta, ea = K[-1], T[-1], E[-1]; tol = 0.75 * s
    for j in range(len(E) - 3, -1, -2):                     # earlier turning points of the same kind, newest first
        gap = ta - T[j]
        if gap > 35:
            break
        if (E[j] - ea) * kind > tol * 2:
            break                                           # a clearly more extreme point lies between: Ea is not the extreme after E1
        if gap > 22 and abs(E[j] - ea) / 2 <= tol and all((E[m] - ea) * kind <= 0 for m in range(j + 2, len(E) - 1, 2)):
            return -kind
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
