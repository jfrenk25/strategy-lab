"""Look-ahead check for the screen's signal parts.

Every trigger x direction x regime x session combination is computed on the full BTCUSD history and again on
shortened copies of it. Each trigger is also checked alone on 20 copies that end right after a bar on which it fires,
and each regime filter on 40 copies: a part that peeks even one bar ahead changes on the last bar of such a copy.
A signal that changes when later bars are removed is using the future.
Usage (from the repo root): python lab/tools/check_screen.py
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import lab, screen


def check(market="BTCUSD"):
    df, _, _ = lab.load_market(market)
    full = screen.Feats(df); problems = []
    # 1. every trigger on its own: shortened copies that end right after bars on which it fires
    keys = {}
    for spec in screen.catalogue():
        keys.setdefault((spec["trigger"], str(sorted(spec["params"].items()))), spec)
    for key, spec in keys.items():
        a = full.event(spec["trigger"], spec["params"]); bad = 0
        if len(a) != len(df):
            problems.append(f"{key}: wrong output length"); continue
        for t in lab.lookahead_cuts(a, n_fired=20):
            bad += int((screen.Feats(df.iloc[:t]).event(spec["trigger"], spec["params"]) != a[:t]).sum())
        if bad: problems.append(f"{key}: look-ahead, {bad} trigger values change when later data is removed")
    # 2. every regime filter: 40 shortened copies
    cuts = [int(x) for x in np.random.default_rng(0).integers(len(df) // 4, len(df) - 1, size=40)]
    for rg in screen.REGIMES:
        if rg == "none": continue
        a = full.regime(rg); bad = sum(int((screen.Feats(df.iloc[:t]).regime(rg) != a[:t]).sum()) for t in cuts)
        if bad: problems.append(f"regime {rg}: look-ahead, {bad} values change when later data is removed")
    # 3. every full combination, on the first 50% and 80% (guards the code that puts the parts together)
    cuts = [int(len(df) * f) for f in (0.5, 0.8)]; parts = [screen.Feats(df.iloc[:t]) for t in cuts]; seen = set()
    for spec in screen.catalogue():
        key = (spec["trigger"], str(sorted(spec["params"].items())), spec["direction"], spec["regime"], spec["session"])
        if key in seen:
            continue
        seen.add(key)
        a = screen.signals(spec, full)
        for t, f in zip(cuts, parts):
            bad = int((screen.signals(spec, f) != a[:t]).sum())
            if bad:
                problems.append(f"{key}: look-ahead, {bad} signals change when later data is removed")
    return len(seen), problems


if __name__ == "__main__":
    n, probs = check()
    print(f"OK: {n} signal combinations, no look-ahead" if not probs else "PROBLEMS:\n- " + "\n- ".join(probs))
    sys.exit(1 if probs else 0)
