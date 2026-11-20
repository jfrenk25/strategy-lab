"""Copy this file, rename it (no leading underscore), and fill it in. One file is one idea."""
import numpy as np

IDEA = dict(
    name="short_snake_case_name",
    source="Link or citation for where the idea came from",
    reason="One sentence: why should this make money?",
    loser="One sentence: who is on the other side, and why do they keep losing?",
    grid=[{"n": 20}, {"n": 50}],          # at most 12 parameter sets; fewer is better
    # markets=["BTCUSD", "ETHUSD"],       # optional; default is every market in lab/data
)


def signals(df, p):
    """df has open, high, low, close, volume on 1-hour bars. Decide at each bar's close.
    Return +1 (go long), -1 (go short) or 0. Never look at a later bar."""
    return np.zeros(len(df), dtype=int)
