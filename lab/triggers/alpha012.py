"""Price change against the volume change (101 Formulaic Alphas: Alpha#12).

Source formula: sign(change in volume) times minus the one-bar change in close.
Kept: the formula, with the price change taken as a fraction of the close so that it has no price scale.
Changed: the event fires when the value is above the q-quantile (+1) or below the (1-q)-quantile (-1) of its own
previous 500 bars. So +1 is a large fall on rising volume or a large rise on falling volume.
Note: the source page could not be opened in the session that wrote this file, so the formula is written from the published definition as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="alpha012",
    source='Z. Kakushadze, "101 Formulaic Alphas" (2016), arXiv:1601.00991, Alpha#12',
    summary="+1 after an unusually large fall on rising volume (or rise on falling volume), -1 after an unusually large rise on rising volume (or fall on falling volume).",
    variants=[{"q": 0.95}, {"q": 0.99}],
    timed=False,
)


def event(df, p):
    c, v = df["close"], df["volume"]
    a = np.sign(v.diff()) * (-(c.diff() / c.shift(1)))
    hi = a.rolling(500).quantile(p["q"]).shift(1); lo = a.rolling(500).quantile(1 - p["q"]).shift(1)
    return np.where(a > hi, 1, np.where(a < lo, -1, 0))
