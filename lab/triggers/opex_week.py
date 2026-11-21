"""Option-expiration week.

Source: Stivers and Sun, "Returns and option activity over the option-expiration week for S&P 100 stocks", Journal of
Banking & Finance 37(11), 2013, 4226-4240. The abstract was read (on RePEc) in the session that wrote this file; the
full text is behind a paywall, so the size of the effect and the sample years were not seen.
The paper's finding: large US stocks tend to have high returns in the week of a month's third Friday, when monthly
options expire. Its explanations: option market makers reduce their short-stock hedges over that week, and perceived
risk falls.
Kept: the week of the third Friday, pointing up.
Changed: the event fires once, at a fixed UTC hour on the Monday of that week (the Monday whose day of the month is
11 to 17), instead of holding for the whole week. It is applied to every market, although the source is about US stocks.
The built-in clock trigger uses weekdays and hours only, and turn_of_month uses the month's edges.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="opex_week",
    source='Stivers and Sun, "Returns and option activity over the option-expiration week for S&P 100 stocks", Journal of Banking & Finance 37(11), 2013, 4226-4240',
    summary="+1 at a fixed UTC hour on the Monday of the week that holds the month's third Friday.",
    variants=[{"hour": 8}, {"hour": 14}],
    timed=True,
)


def event(df, p):
    idx = df.index
    monday = (idx.dayofweek == 0) & (idx.day >= 11) & (idx.day <= 17)
    return np.where(monday & (idx.hour == int(p["hour"])), 1, 0)
