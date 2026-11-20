"""Returns that have been following, or reversing, each other unusually strongly.

Source: B. LeBaron, "Some Relations Between Volatility and Serial Correlations in Stock Market Returns", Journal of
Business 65(2), 1992. The first-order serial correlation of returns changes over time (it is higher in calm periods),
so the last return says more about the next one at some times than at others. Written from the published finding as
recalled; the paper was not opened.
Kept: the rolling first-order serial correlation of returns as the state. Changed: the paper gives no trading rule.
Here the event fires when the n-bar serial correlation of hourly returns is above the 95% quantile of its own previous
500 bars (pointing the way the last bar went) or below the 5% quantile (pointing against the last bar).
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="serial_corr",
    source='B. LeBaron, "Some Relations Between Volatility and Serial Correlations in Stock Market Returns", Journal of Business 65(2), 1992',
    summary="When hourly returns have been unusually self-following over n bars, point with the last bar; when unusually self-reversing, point against it.",
    variants=[{"n": 48}],
    timed=False,
)


def event(df, p):
    c = df["close"]; r = c / c.shift(1) - 1
    x = r.rolling(int(p["n"])).corr(r.shift(1)).replace([np.inf, -np.inf], np.nan)
    hi = x.rolling(500).quantile(0.95).shift(1); lo = x.rolling(500).quantile(0.05).shift(1)
    s = np.sign(r.to_numpy())
    return np.nan_to_num(np.where((x > hi).to_numpy(), s, np.where((x < lo).to_numpy(), -s, 0))).astype(int)
