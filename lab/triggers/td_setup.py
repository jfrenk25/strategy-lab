"""TD Sequential setup: nine closes in a row beyond the close four bars earlier.

Source: the TD Sequential strategy in the public freqtrade strategy collection, which acts on Tom DeMark's count of
nine. This is not the built-in streak (close against the previous close): each close is compared with the close four
bars before it.
Kept: the count of nine against the close four bars back, and the direction (nine lower closes point up).
Changed: only the completed setup is used; the countdown phase and the strategy's exits are left out. The event fires
on the bar where the count reaches nine.
Note: the source page could not be opened in the session that wrote this file, so the formula is written from the published definition as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="td_setup",
    source='freqtrade-strategies (github.com/freqtrade/freqtrade-strategies), berlinguyinca/TDSequentialStrategy; count from T. DeMark, "The New Science of Technical Analysis" (1994)',
    summary="+1 when nine closes in a row are each below the close four bars earlier, -1 when nine in a row are each above it.",
    variants=[{"count": 9}],
    timed=False,
)


def event(df, p):
    k = int(p["count"]); c = df["close"]; ref = c.shift(4)
    below = (c < ref).to_numpy(); above = (c > ref).to_numpy()
    out = np.zeros(len(c), dtype=int); nb = na = 0
    for i in range(len(c)):
        nb = nb + 1 if below[i] else 0
        na = na + 1 if above[i] else 0
        if nb == k: out[i] = 1
        elif na == k: out[i] = -1
    return out
