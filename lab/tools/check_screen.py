"""Look-ahead check for the screen's signal parts.

Every trigger x direction x regime x session combination is computed on the full BTCUSD history and again on the
first 50% and 80% of it. A signal that changes when later bars are removed is using the future.
Usage (from the repo root): python lab/tools/check_screen.py
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import lab, screen


def check(market="BTCUSD"):
    df, _, _ = lab.load_market(market)
    cuts = [int(len(df) * f) for f in (0.5, 0.8)]
    full = screen.Feats(df); parts = [screen.Feats(df.iloc[:t]) for t in cuts]
    seen, problems = set(), []
    for spec in screen.catalogue():
        key = (spec["trigger"], str(sorted(spec["params"].items())), spec["direction"], spec["regime"], spec["session"])
        if key in seen:
            continue
        seen.add(key)
        a = screen.signals(spec, full)
        if len(a) != len(df):
            problems.append(f"{key}: wrong output length"); continue
        for t, f in zip(cuts, parts):
            bad = int((screen.signals(spec, f) != a[:t]).sum())
            if bad:
                problems.append(f"{key}: look-ahead, {bad} signals change when later data is removed")
    return len(seen), problems


if __name__ == "__main__":
    n, probs = check()
    print(f"OK: {n} signal combinations, no look-ahead" if not probs else "PROBLEMS:\n- " + "\n- ".join(probs))
    sys.exit(1 if probs else 0)
