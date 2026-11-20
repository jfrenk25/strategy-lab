"""Close crosses a round number.

Source: C. Osler, "Currency Orders and Exchange Rate Dynamics: An Explanation for the Predictive Success of Technical
Analysis", Journal of Finance 58(5), 2003. Stop-loss and take-profit orders cluster at round numbers; trends tend to
speed up once a round number is crossed and to stall just before one.
Kept: the event of price crossing a round number. Changed: the paper uses currency rates ending in 00 or 50. Here the
spacing of round numbers is set from each market's own price: a power of ten between about 0.3% and 3% of the previous
close (0.01 for a rate near 1.08, 1000 for a price near 95,000). No fixed price scale is assumed.
Note: the source could not be opened in the session that wrote this file, so the rule is written from the published description as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="round_number_cross",
    source='C. Osler, "Currency Orders and Exchange Rate Dynamics: An Explanation for the Predictive Success of Technical Analysis", Journal of Finance 58(5), 2003',
    summary="+1 when the close moves up through a round number (a power-of-ten step sized to the market's own price), -1 when it moves down through one.",
    variants=[{"decades": 2}],
    timed=False,
)


def event(df, p):
    c = df["close"]; pc = c.shift(1).where(c.shift(1) > 0)
    step = 10.0 ** np.round(np.log10(pc) - p["decades"])
    k_now = np.floor(c / step); k_prev = np.floor(pc / step)
    return np.where(k_now > k_prev, 1, np.where(k_now < k_prev, -1, 0))
