"""New moon and full moon.

Source: Dichev and Janes, "Lunar Cycle Effects in Stock Returns", Journal of Private Equity 6(4), 2003; Yuan, Zheng and
Zhu, "Are Investors Moonstruck? Lunar Phases and Stock Returns", Journal of Empirical Finance 13(1), 2006. Both report
that stock index returns in the days around a new moon are higher than in the days around a full moon, in many
countries. Written from the published findings as recalled: neither paper was opened on 2026-11-23.
Rule: +1 on the first bar at or after a new moon, -1 on the first bar at or after a full moon.
The moon's phase is worked out from the bar's time alone: new moons are taken as evenly spaced, one mean synodic month
(29.530588853 days) apart, counted from the new moon of 6 January 2000, 18:14 UTC. A real new moon can be up to about
14 hours away from that. The papers compare windows of about a week each side, so the slip is small against them.
Kept: the direction (new moon up, full moon down). Changed: the papers compare average returns over windows of days;
this marks one bar per phase and leaves the holding time to the lab's exits. A market that is closed at the moment
gets the event on its next bar.
Not a repeat: clock uses weekday and hour, turn_of_month the day of the month, opex_week the third Friday.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="lunar_phase",
    source='Dichev and Janes, "Lunar Cycle Effects in Stock Returns", Journal of Private Equity 6(4), 2003; Yuan, Zheng and Zhu, "Are Investors Moonstruck? Lunar Phases and Stock Returns", Journal of Empirical Finance 13(1), 2006',
    summary="+1 on the first bar at or after each new moon, -1 on the first bar at or after each full moon (mean lunar cycle).",
    variants=[{"synodic": 29.530588853}],
    timed=True,
)


def event(df, p):
    ref = pd.Timestamp("2000-01-06 18:14", tz="UTC")
    idx = df.index if df.index.tz is not None else df.index.tz_localize("UTC")
    cycles = np.asarray((idx - ref) / pd.Timedelta(days=1), dtype=np.float64) / float(p["synodic"])
    new = np.floor(cycles); full = np.floor(cycles - 0.5)
    is_new = np.r_[False, new[1:] != new[:-1]]; is_full = np.r_[False, full[1:] != full[:-1]]
    return np.where(is_new, 1, np.where(is_full, -1, 0))
