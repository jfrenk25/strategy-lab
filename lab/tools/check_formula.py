"""Formula check: compare an idea's fast code with a slow, literal second version on random price paths.

Usage (from the repo root):
    python lab/tools/check_formula.py NAME              # an idea in lab/ideas
    python lab/tools/check_formula.py NAME --trigger    # a trigger in lab/triggers

The file must define reference(df, p) (or reference(data, p) for a position idea): the same rule written the plainest
way possible, one bar at a time, straight from the paper's formula. The two versions must agree on every bar.
This catches slips in the code. It cannot catch a misreading of the paper, because both versions share the reading.
"""
import sys, os, importlib.util
import numpy as np
import pandas as pd

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
N_BARS, SEEDS = 3000, (1, 2, 3)


def random_frame(seed, weekdays_only):
    """A made-up hourly market: fat-tailed moves, gaps, a few dead bars and zero-volume bars."""
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2022-01-03", periods=N_BARS * 2, freq="1h", tz="UTC")
    if weekdays_only:
        idx = idx[idx.dayofweek < 5]
    idx = idx[:N_BARS]
    close = 100 * np.exp(np.cumsum(rng.standard_t(4, N_BARS) * 0.004))
    gap = rng.normal(0, 0.001, N_BARS) * np.where(np.r_[False, np.diff(idx.asi8) > 3.6e12], 8, 1)
    open_ = np.r_[close[0], close[:-1]] * np.exp(gap)
    high = np.maximum(open_, close) * np.exp(np.abs(rng.normal(0, 0.002, N_BARS)))
    low = np.minimum(open_, close) * np.exp(-np.abs(rng.normal(0, 0.002, N_BARS)))
    volume = rng.lognormal(3, 1, N_BARS)
    dead = rng.random(N_BARS) < 0.01                         # bars with no movement and no volume
    close = np.where(dead, open_, close); high = np.where(dead, open_, high); low = np.where(dead, open_, low); volume = np.where(dead, 0.0, volume)
    return pd.DataFrame({"open": open_, "high": high, "low": low, "close": close, "volume": volume}, index=pd.Index(idx, name="time"))


def random_daily(seed):
    """Daily data for four made-up markets, in the shape position ideas receive."""
    wide = {f: {} for f in ("open", "high", "low", "close", "volume")}
    for i, wk in enumerate((False, True, True, False)):
        h = random_frame(seed * 10 + i, wk); day = (h.index + pd.Timedelta(hours=2)).floor("D").tz_localize(None)
        d = h.groupby(day).agg(open=("open", "first"), high=("high", "max"), low=("low", "min"), close=("close", "last"), volume=("volume", "sum"))
        for f in wide:
            wide[f][f"M{i}"] = d[f]
    return {f: pd.DataFrame(wide[f]).sort_index() for f in wide}


def check(name, trigger=False):
    path = os.path.join(HERE, "triggers" if trigger else "ideas", name + ".py")
    spec = importlib.util.spec_from_file_location(name, path); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    if not hasattr(mod, "reference"):
        return ["no reference() function: write the rule a second time, one bar at a time, straight from the formula"]
    head = mod.TRIGGER if trigger else mod.IDEA
    params = head["variants"] if trigger else head["grid"]
    fast = mod.event if trigger else (mod.positions if head.get("mode") == "position" else mod.signals)
    problems = []
    for p in params:
        for seed in SEEDS:
            if not trigger and head.get("mode") == "position":
                data = random_daily(seed); idx, cols = data["close"].index, data["close"].columns
                a = fast(data, p).reindex(index=idx, columns=cols).fillna(0.0).to_numpy(); b = mod.reference(data, p).reindex(index=idx, columns=cols).fillna(0.0).to_numpy()
                bad = np.abs(a - b) > 1e-9
                if bad.any():
                    problems.append(f"{p} seed {seed}: weights differ on {int(bad.any(axis=1).sum())} days, first at {idx[np.argmax(bad.any(axis=1))].date()}")
                continue
            for wk in (False, True):
                df = random_frame(seed, wk)
                a = np.sign(np.nan_to_num(np.asarray(fast(df, p), dtype=float))); b = np.sign(np.nan_to_num(np.asarray(mod.reference(df, p), dtype=float)))
                if len(a) != len(df) or len(b) != len(df):
                    problems.append(f"{p}: wrong output length"); continue
                bad = a != b
                if bad.any():
                    problems.append(f"{p} seed {seed}{' weekdays' if wk else ''}: {int(bad.sum())} of {len(df)} bars differ, first at bar {int(np.argmax(bad))} (fast {int(a[np.argmax(bad)])}, reference {int(b[np.argmax(bad)])})")
                elif not (a != 0).any():
                    problems.append(f"{p} seed {seed}: never fires on random data, so nothing was compared")
    return problems


if __name__ == "__main__":
    probs = check(sys.argv[1], trigger="--trigger" in sys.argv)
    print("OK: fast code and reference agree on every bar" if not probs else "PROBLEMS:\n- " + "\n- ".join(probs[:12]))
    sys.exit(1 if probs else 0)
