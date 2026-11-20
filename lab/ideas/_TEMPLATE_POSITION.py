"""Template for a position-mode idea: one that holds weights across markets day by day.
Copy this file, rename it (no leading underscore), and fill it in."""
import numpy as np

IDEA = dict(
    name="short_snake_case_name",
    mode="position",
    source="Link or citation for where the idea came from",
    reason="One sentence: why should this make money?",
    loser="One sentence: who is on the other side, and why do they keep losing?",
    grid=[{"lookback": 20}, {"lookback": 60}],     # at most 12 parameter sets; fewer is better
    # markets=["BTCUSD", "ETHUSD"],                # optional; default is every market in lab/data
)


def positions(data, p):
    """data["close"], ["open"], ["high"], ["low"], ["volume"] are tables of days x markets (NaN when a market is closed).
    Return a table of target weights with the same shape, decided at each day's close.
    Positive is long, negative is short. The lab caps total exposure at 1 and charges costs on every change.
    Never use a later day. Rebalance weekly or slower unless the idea needs daily changes: turnover is charged."""
    close = data["close"]
    return close * 0.0
