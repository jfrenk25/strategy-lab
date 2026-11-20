"""Unusually illiquid or unusually liquid trading (Amihud's illiquidity ratio).

Source: Y. Amihud, "Illiquidity and Stock Returns: Cross-Section and Time-Series Effects", Journal of Financial
Markets 5(1), 2002. Illiquidity is the average of absolute return divided by volume; higher expected illiquidity goes
with higher expected returns. The rule is written from the published definition as recalled; the paper was not opened.
Kept: the ratio, averaged over n bars. Changed: one market on hourly bars; volume is the bar's own unit volume, since
only its level against the market's own past matters. The event fires when the average first moves above the 95%
quantile (+1) or below the 5% quantile (-1) of its own previous 500 bars.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="amihud_illiq",
    source='Y. Amihud, "Illiquidity and Stock Returns: Cross-Section and Time-Series Effects", Journal of Financial Markets 5(1), 2002',
    summary="+1 when price has been moving unusually far per unit of volume over n bars, -1 when unusually little.",
    variants=[{"n": 24}],
    timed=False,
)


def event(df, p):
    c, v = df["close"], df["volume"]
    x = ((c / c.shift(1) - 1).abs() / v.where(v > 0)).rolling(int(p["n"])).mean()
    hi = x.rolling(500).quantile(0.95).shift(1); lo = x.rolling(500).quantile(0.05).shift(1)
    up = x > hi; dn = x < lo
    return np.where(up & ~up.shift(1, fill_value=False), 1, np.where(dn & ~dn.shift(1, fill_value=False), -1, 0))
