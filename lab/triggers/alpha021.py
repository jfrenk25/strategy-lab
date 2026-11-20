"""Two-bar average outside the eight-bar band (101 Formulaic Alphas: Alpha#21).

Source formula, in words: -1 if the 8-bar mean of close plus its 8-bar standard deviation is below the 2-bar mean;
+1 if the 2-bar mean is below the 8-bar mean minus the standard deviation; otherwise a sign set by volume against
its 20-bar average.
Kept: the first two branches, their windows and their signs. Changed: the volume fallback is dropped because it is
never zero, and the event fires only on the bar where a branch first becomes true.
Note: the source page could not be opened in the session that wrote this file, so the formula is written from the published definition as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="alpha021",
    source='Z. Kakushadze, "101 Formulaic Alphas" (2016), arXiv:1601.00991, Alpha#21',
    summary="+1 when the 2-bar average close first drops below the 8-bar average minus one standard deviation, -1 when it first rises above the average plus one.",
    variants=[{"n": 8}],
    timed=False,
)


def event(df, p):
    n = int(p["n"]); c = df["close"]
    m, s, m2 = c.rolling(n).mean(), c.rolling(n).std(), c.rolling(2).mean()
    above = (m + s) < m2; below = m2 < (m - s)
    return np.where(below & ~below.shift(1, fill_value=False), 1, np.where(above & ~above.shift(1, fill_value=False), -1, 0))
