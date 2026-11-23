"""Summed buying and selling pressure reaches an extreme (Guotai Junan Alpha191: Alpha#3 and Alpha#59).

Source factors, read on 2026-11-23 from a public listing of the 191 formulas (bigquant.com/wiki/doc/Pyf0TYya6H), which
reproduces the Guotai Junan Securities report on 191 short-horizon price-volume factors (2017):
    Alpha3  = SUM( CLOSE = DELAY(CLOSE,1) ? 0 : CLOSE - (CLOSE > DELAY(CLOSE,1) ? MIN(LOW, DELAY(CLOSE,1)) : MAX(HIGH, DELAY(CLOSE,1))), 6 )
    Alpha59 = the same sum over 20 bars.
On an up bar the term is the close minus the "true low" (the lower of the low and the previous close); on a down bar
it is the close minus the "true high", which is negative. It is the running part of Williams' accumulation/distribution.
Kept: the formula and its two windows (6 and 20). Changed: each bar's term is divided by the close so the value does
not depend on the price level, and the event fires when the sum first moves above the 95% quantile of its own previous
500 bars (+1: buying pressure is extreme) or below the 5% quantile (-1).
Not a repeat: streak counts closes, zmove measures the net move; this adds up how far each close sits from the far
end of its bar, gaps included.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="gtja003_pressure_sum",
    source="Guotai Junan Securities, 191 short-horizon price-volume alpha factors (2017), Alpha#3 and Alpha#59, as listed at https://bigquant.com/wiki/doc/Pyf0TYya6H",
    summary="+1 when the n-bar sum of close-minus-true-low (up bars) and close-minus-true-high (down bars) first reaches a high extreme of its own past, -1 at a low extreme.",
    variants=[{"n": 6}, {"n": 20}],
    timed=False,
)


def event(df, p):
    n = int(p["n"]); c, h, l = df["close"], df["high"], df["low"]
    c1 = c.shift(1)
    term = np.where(c > c1, c - np.minimum(l, c1), np.where(c < c1, c - np.maximum(h, c1), 0.0))
    term = pd.Series(term, index=df.index).where(c1.notna()) / c
    x = term.rolling(n).sum()
    hi = x.rolling(500).quantile(0.95).shift(1); lo = x.rolling(500).quantile(0.05).shift(1)
    up = x > hi; dn = x < lo
    return np.where(up & ~up.shift(1, fill_value=False), 1, np.where(dn & ~dn.shift(1, fill_value=False), -1, 0))
