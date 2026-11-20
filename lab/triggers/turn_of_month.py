"""Turn of the month.

Source: Lakonishok and Smidt, "Are Seasonal Anomalies Real? A Ninety-Year Perspective", Review of Financial Studies
1(4), 1988; McConnell and Xu, "Equity Returns at the Turn of the Month", Financial Analysts Journal 64(2), 2008.
Stock returns are concentrated in the last trading day of a month and the first three of the next.
Kept: the four-day window. Changed: calendar days stand in for trading days (the last calendar day of the month and
days 1 to 3), and the event fires once a day at a fixed UTC hour. It only points up: follow buys, fade sells.
The built-in clock trigger uses weekdays and hours, never the day of the month.
Note: the source could not be opened in the session that wrote this file, so the rule is written from the published description as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="turn_of_month",
    source='Lakonishok and Smidt, "Are Seasonal Anomalies Real? A Ninety-Year Perspective", Review of Financial Studies 1(4), 1988; McConnell and Xu, "Equity Returns at the Turn of the Month", Financial Analysts Journal 64(2), 2008',
    summary="+1 at a fixed UTC hour on the last calendar day of a month and on days 1 to 3 of the next.",
    variants=[{"hour": 0}, {"hour": 13}],
    timed=True,
)


def event(df, p):
    idx = df.index
    window = (idx.day == idx.days_in_month) | (idx.day <= 3)
    return np.where(window & (idx.hour == int(p["hour"])), 1, 0)
