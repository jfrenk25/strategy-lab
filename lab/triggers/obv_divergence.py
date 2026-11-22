"""A new closing high that on-balance volume does not confirm, or a new closing low it does not confirm.

Source: J. Granville, "Granville's New Key to Stock Market Profits", 1963 (on-balance volume and its non-confirmation
of new price highs and lows). Sullivan, Timmermann and White, "Data-Snooping, Technical Trading Rule Performance, and
the Bootstrap", Journal of Finance 54(5), 1999, include on-balance volume rules in their universe, but only as
moving averages of it. Written from the published idea as recalled; neither source was opened.
On-balance volume adds a bar's volume when the close rises and subtracts it when the close falls.
Kept: the divergence itself. Changed: Granville gives no fixed window, so "new high" means a close above every close
of the previous n bars, and "not confirmed" means on-balance volume is still below its own highest value of those n
bars. The event points against the unconfirmed move: -1 at an unconfirmed high, +1 at an unconfirmed low.
Not the built-in breakout (which fires on every new extreme and ignores volume) and not an on-balance-volume
crossover. Only differences of on-balance volume over the window matter, so the volume scale drops out.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="obv_divergence",
    source='J. Granville, "Granville\'s New Key to Stock Market Profits", 1963 (on-balance volume non-confirmation)',
    summary="-1 when the close makes a new n-bar high but on-balance volume does not, +1 when the close makes a new n-bar low but on-balance volume does not.",
    variants=[{"n": 24}, {"n": 72}],
    timed=False,
)


def event(df, p):
    n = int(p["n"]); c = df["close"]
    obv = (np.sign(c.diff()).fillna(0.0) * df["volume"]).cumsum()
    new_hi = c > c.rolling(n).max().shift(1); new_lo = c < c.rolling(n).min().shift(1)
    obv_hi = obv.rolling(n).max().shift(1); obv_lo = obv.rolling(n).min().shift(1)
    return np.where(new_hi & (obv < obv_hi), -1, np.where(new_lo & (obv > obv_lo), 1, 0))
