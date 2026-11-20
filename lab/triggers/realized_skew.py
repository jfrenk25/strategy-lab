"""Realized skewness at an extreme.

Source: Amaya, Christoffersen, Jacobs and Vasquez, "Does Realized Skewness Predict the Cross-Section of Equity
Returns?", Journal of Financial Economics 118(1), 2015. Skewness measured from intraday returns over a week predicts
the next week's return: low skew is followed by higher returns.
Kept: skewness of high-frequency returns over a short window. Changed: one market, hourly returns over n bars, and the
event fires when the skewness first moves above the 95% quantile (+1) or below the 5% quantile (-1) of its own previous
500 bars. The source's direction is the fade side.
Note: the source could not be opened in the session that wrote this file, so the rule is written from the published description as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="realized_skew",
    source='Amaya, Christoffersen, Jacobs and Vasquez, "Does Realized Skewness Predict the Cross-Section of Equity Returns?", Journal of Financial Economics 118(1), 2015',
    summary="+1 when the skewness of the last n hourly returns is unusually positive, -1 when unusually negative.",
    variants=[{"n": 120}],
    timed=False,
)


def event(df, p):
    c = df["close"]
    x = np.log(c / c.shift(1)).rolling(int(p["n"])).skew()
    hi = x.rolling(500).quantile(0.95).shift(1); lo = x.rolling(500).quantile(0.05).shift(1)
    up = x > hi; dn = x < lo
    return np.where(up & ~up.shift(1, fill_value=False), 1, np.where(dn & ~dn.shift(1, fill_value=False), -1, 0))
