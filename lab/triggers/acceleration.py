"""Acceleration: the change in momentum from one window to the next reaches an extreme.

Source: D. Ardila-Alvarez, Z. Forro and D. Sornette, "The acceleration effect and Gamma factor in asset pricing",
Physica A 569 (2021). The abstract was read on 2026-11-24 (ideas.repec.org); the full text is behind a paywall. It
defines acceleration as the first difference of successive returns and reports that strategies built on it were
profitable on average and beat plain momentum in about two thirds of the settings tried, across stocks.
Kept: acceleration as this window's return minus the previous window's return.
Changed: the paper ranks stocks against each other on monthly data; its windows were not seen. Here it is one market
against its own past: G = log return of the last n bars minus log return of the n bars before them, turned into a
z-score with the mean and standard deviation of G over the 20n bars before this one. The event is the first bar on
which the z-score passes z (up: +1) or -z (down: -1). The window lengths and z = 2 are the lab's, fixed before any run.
Not the built-in zmove (an extreme n-bar move): a market that was falling fast and is now flat has a large positive G
and no move at all, and a steady strong trend has a large move and G near zero.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="acceleration",
    source='D. Ardila-Alvarez, Z. Forro and D. Sornette, "The acceleration effect and Gamma factor in asset pricing", Physica A 569, 125367 (2021), https://ideas.repec.org/a/eee/phsmap/v569y2021ics0378437120307196.html',
    summary="+1 when the last n bars' return minus the n bars' return before it first rises 2 standard deviations above its own recent average; -1 when it first falls 2 below.",
    variants=[{"n": 24, "z": 2.0}, {"n": 72, "z": 2.0}],
    timed=False,
)


def event(df, p):
    n = int(p["n"]); z = float(p["z"])
    lp = np.log(df["close"])
    g = (lp - lp.shift(n)) - (lp.shift(n) - lp.shift(2 * n))
    mu = g.rolling(20 * n).mean().shift(1); sd = g.rolling(20 * n).std().shift(1)
    s = (g - mu) / sd
    up = (s > z) & ~(s.shift(1) > z); dn = (s < -z) & ~(s.shift(1) < -z)
    return np.where(up, 1, np.where(dn, -1, 0))
