"""Pre-test check for one idea: header fields, grid size, and a look-ahead test.
Usage (from the repo root): python lab/tools/check_idea.py NAME"""
import sys, os, importlib.util
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import lab


def check(name):
    path = os.path.join(lab.HERE, "ideas", name + ".py")
    spec = importlib.util.spec_from_file_location(name, path); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    idea, problems = mod.IDEA, []
    for k in ("name", "source", "reason", "loser", "grid"):
        if not idea.get(k): problems.append(f"missing {k}")
    if len(idea.get("grid", [])) > lab.MAX_GRID: problems.append("grid larger than 12")
    if idea.get("mode") == "position":
        import position_mode as pm
        data, _ = pm.load_daily(idea.get("markets", "all"))
        for p in idea.get("grid", []):
            full = mod.positions(data, p).reindex(index=data["close"].index, columns=data["close"].columns).fillna(0.0).to_numpy()
            rng = np.random.default_rng(0)
            for t in sorted({int(len(full) * 0.6), int(len(full) * 0.85)} | {int(x) for x in rng.integers(len(full) // 4, len(full) - 1, size=20)}):
                part = mod.positions({k: v.iloc[:t] for k, v in data.items()}, p).reindex(index=data["close"].index[:t], columns=data["close"].columns).fillna(0.0).to_numpy()
                bad = int((np.abs(part - full[:t]) > 1e-9).any(axis=1).sum())
                if bad: problems.append(f"{p}: look-ahead, weights on {bad} days change when later data is removed")
        return problems
    df, _, _ = lab.load_market("BTCUSD")
    for p in idea.get("grid", []):
        full = np.nan_to_num(np.asarray(mod.signals(df, p), dtype=float))
        if len(full) != len(df): problems.append(f"{p}: wrong output length"); continue
        bad = 0
        for t in lab.lookahead_cuts(full):               # half way, four fifths, and right after 40 bars on which the idea signals
            part = np.nan_to_num(np.asarray(mod.signals(df.iloc[:t], p), dtype=float))
            bad += int((part != full[:t]).sum())
        if bad: problems.append(f"{p}: look-ahead, {bad} signals change when later data is removed")
    return problems


if __name__ == "__main__":
    probs = check(sys.argv[1])
    print("OK: header valid, no look-ahead" if not probs else "PROBLEMS:\n- " + "\n- ".join(probs))
    sys.exit(1 if probs else 0)
