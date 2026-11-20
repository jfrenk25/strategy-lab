"""Unusually high or low volume, whatever the price did.

Source: Gervais, Kaniel and Mingelgrin, "The High-Volume Return Premium", Journal of Finance 56(3), 2001. Stocks with
unusually high volume over a day tend to rise over the following weeks and those with unusually low volume tend to
lag, regardless of the day's price move. The paper ranks a day's volume against the previous 49 days and uses the top
and bottom tenth.
Kept: the 50-observation window and the top and bottom tenth. Changed: one market on hourly bars; each bar's volume is
ranked against the same clock hour on earlier days, so the daily rhythm of volume does not set the signal off.
This is not the built-in vol_spike, which takes its direction from the bar's own move.
Note: the source could not be opened in the session that wrote this file, so the rule is written from the published description as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="high_volume_premium",
    source='Gervais, Kaniel and Mingelgrin, "The High-Volume Return Premium", Journal of Finance 56(3), 2001',
    summary="+1 when this bar's volume is in the top tenth of the same hour's volume over the last 50 days, -1 when it is in the bottom tenth.",
    variants=[{"days": 50}],
    timed=False,
)


def event(df, p):
    n = int(p["days"]); v = df["volume"]
    rk = v.groupby(df.index.hour).transform(lambda s: s.rolling(n).rank(pct=True))
    return np.where(rk >= 0.9, 1, np.where(rk <= 0.1, -1, 0))
