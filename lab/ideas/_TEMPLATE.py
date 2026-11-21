"""Copy this file, rename it (no leading underscore), and fill it in. One file is one idea."""
import numpy as np

IDEA = dict(
    name="short_snake_case_name",
    source="Link or citation for where the idea came from",
    reason="One sentence: why should this make money?",
    loser="One sentence: who is on the other side, and why do they keep losing?",
    grid=[{"n": 20}, {"n": 50}],          # at most 12 parameter sets; fewer is better
    # markets=["BTCUSD", "ETHUSD"],       # optional. Default: the original six. "fifteen" = every market. Or name any of the fifteen.
    # paper="arxiv_2401_01234",           # for an idea that comes from lab/papers: the paper's id
)


def signals(df, p):
    """df has open, high, low, close, volume on 1-hour bars. Decide at each bar's close.
    Return +1 (go long), -1 (go short) or 0. Never look at a later bar."""
    return np.zeros(len(df), dtype=int)


# For an idea from a paper, also write reference(df, p): the same rule the plainest way possible, one bar at a time,
# straight from the paper's formula. `python lab/tools/check_formula.py NAME` compares the two on random prices.
# def reference(df, p):
#     out = np.zeros(len(df), dtype=int)
#     for i in range(len(df)):
#         ...
#     return out
