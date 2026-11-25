"""Cooper's price-and-volume filter: a large move, sorted by whether trading volume rose or fell while it happened.

Source: M. Cooper, "Filter Rules Based on Price and Volume in Individual Security Overreaction", Review of Financial
Studies 12(4), 1999. Written from the published finding as recalled; the paper was not opened. The finding, on weekly
returns of large US stocks: a large one-week move tends to reverse the next week, and it reverses more when volume
fell during the move and less (or not at all) when volume grew.
Kept: the two filters, the size of the last move and the growth in volume over the same span.
Changed: the paper sorts single stocks by fixed percent bands of weekly return and of volume growth; here one market
is compared with its own past. A move is "large" when the n-bar return is beyond 1.5 standard deviations of the n-bar
returns of the 20 spans before it. Volume growth is the volume of the last n bars against the n bars before them.
`falling` = 1 keeps the moves made on lower volume, `falling` = 0 the moves made on higher volume. The event is signed
the way the move went (+1 up, -1 down), so the fade side is the paper's reversal and the follow side its opposite.
1-hour bars, not weeks.
Not the built-in zmove (size of the move only) nor vol_spike (one bar's volume): the same move is kept or dropped by
what volume did, which no built-in part or regime filter looks at.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="cooper_volume_filter",
    source="M. Cooper, Filter Rules Based on Price and Volume in Individual Security Overreaction, Review of Financial Studies 12(4), 1999",
    summary="+1 after a large n-bar rise and -1 after a large n-bar fall, kept only when volume over those n bars was lower (falling=1) or higher (falling=0) than over the n bars before.",
    variants=[{"n": 24, "falling": 1}, {"n": 24, "falling": 0}],
    timed=False,
)


def event(df, p):
    n = int(p["n"])
    c, v = df["close"], df["volume"].astype(float)
    r = c / c.shift(n) - 1.0
    sd = r.rolling(20 * n).std().shift(n)                 # spread of n-bar returns over the 20 spans before this one
    vnow = v.rolling(n).sum()
    vold = vnow.shift(n)
    growth = np.where(vold > 0, vnow / vold.where(vold > 0) - 1.0, np.nan)
    keep = (growth < 0) if int(p["falling"]) == 1 else (growth > 0)
    big = (r.abs() > 1.5 * sd).to_numpy()
    first = big & ~np.roll(big, 1)                        # only the bar on which the move first counts as large
    first[0] = False
    sig = np.sign(r.to_numpy())
    return np.where(first & keep, np.nan_to_num(sig), 0).astype(int)
