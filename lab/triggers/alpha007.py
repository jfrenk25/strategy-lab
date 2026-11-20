"""A large 7-bar move on above-average volume (101 Formulaic Alphas: Alpha#7).

Source formula, in words: when volume is above its 20-bar average, the alpha is minus the 60-bar time-series rank of
the absolute 7-bar change in close, times the sign of that change; otherwise it is a constant.
Kept: the volume condition, the 7, 20 and 60 bar windows. Changed: the event fires only when that rank is in the
top tenth, and it points the way price moved (the source bets against the move; the screen tries both ways).
The constant branch is dropped.
Note: the source page could not be opened in the session that wrote this file, so the formula is written from the published definition as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="alpha007",
    source='Z. Kakushadze, "101 Formulaic Alphas" (2016), arXiv:1601.00991, Alpha#7',
    summary="Volume is above its 20-bar average and the 7-bar price change is among the largest of the last 60 bars: +1 if up, -1 if down.",
    variants=[{"rank": 0.9}],
    timed=False,
)


def event(df, p):
    c, v = df["close"], df["volume"]
    d7 = c.diff(7)
    rk = d7.abs().rolling(60).rank(pct=True)
    busy = v > v.rolling(20).mean()
    on = (busy & (rk >= p["rank"])).to_numpy()
    d = d7.to_numpy()
    return np.where(on & (d > 0), 1, np.where(on & (d < 0), -1, 0))
