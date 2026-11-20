"""New-market test: one run of each watched idea on nine markets the lab has never used.

Run from the repo root:
    python lab/newmarkets.py --dryrun    # same code on shuffled prices, to check the mechanics; nothing is written
    python lab/newmarkets.py             # the one real run; refuses to run a second time

The rules are in LAB_RULES.md under "New-market test". They were written before the data arrived.
"""
import sys, os, json, datetime
from statistics import NormalDist
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lab, screen

NEW_FEES = {"NAS100": 0.00025, "SPX500": 0.00025, "USOIL": 0.0003, "EURUSD": 0.00015, "GBPUSD": 0.00015,
            "USDJPY": 0.00015, "AUDUSD": 0.00015, "USDCAD": 0.00015, "EURJPY": 0.00015}      # per side
T = dict(trades=150, pf=1.15, market_share=0.5, random_pct=95.0, ideas=13, registered_by="2026-11-20")
OUT = os.path.join(HERE, "newmarkets")
RESULTS = os.path.join(OUT, "results.json")
WATCH = os.path.join(HERE, "forward", "watchlist.json")


def load_frames(shuffle):
    frames, missing, rng = {}, [], np.random.default_rng(5)
    for m in NEW_FEES:
        path = os.path.join(HERE, "data_new", f"{m}_1h.csv.gz")
        if not os.path.exists(path):
            missing.append(m); continue
        df = pd.read_csv(path, parse_dates=["time"]).set_index("time")
        if shuffle:
            df = lab.permute(df, rng)
        idx = df.index                                   # blocks and ATR exactly as lab.load_market builds them
        block = np.where((idx.month > 4) | ((idx.month == 4) & (idx.day >= 21)), idx.year, idx.year - 1).astype(np.int64)
        pc = df["close"].shift(1)
        tr = pd.concat([df["high"] - df["low"], (df["high"] - pc).abs(), (df["low"] - pc).abs()], axis=1).max(axis=1)
        frames[m] = (df, block, (tr.rolling(14, min_periods=14).mean() / df["close"]).fillna(0.01).to_numpy())
    return frames, missing


def main():
    dry = "--dryrun" in sys.argv
    if os.path.exists(RESULTS) and not dry:
        print("The new-market test has already been run. It runs once. See lab/newmarkets/results.json."); return
    screen.load_registry()
    watch = json.load(open(WATCH))
    ideas = [w for w in watch if w["registered"] <= T["registered_by"]]
    assert len(ideas) == T["ideas"], f"expected {T['ideas']} watched ideas, found {len(ideas)}"
    frames, missing = load_frames(shuffle=dry)
    lab.FEES = {m: NEW_FEES[m] for m in frames}          # this process only: the screen's functions read fees from lab.FEES
    data = screen.load(frames)
    need_t = NormalDist().inv_cdf(1 - 0.05 / T["ideas"])
    everything = lambda b: np.ones(len(b), dtype=bool)
    today = datetime.date.today().isoformat(); results = []
    for w in ideas:
        st = screen.window_stats(screen.run_spec(w["spec"], data), data, everything, random_baseline=True)
        nm = st["markets_profitable"]
        checks = {
            f"trades >= {T['trades']}": bool(st["trades"] >= T["trades"]),
            f"profit factor >= {T['pf']}": bool(st["pf"] >= T["pf"]),
            "profit factor > 1 at double costs": bool(st["dbl_pf"] > 1.0),
            "profitable in half the new markets": bool(nm[1] and nm[0] / nm[1] >= T["market_share"]),
            "beats 95% of random entries": bool(st["beats_random"] >= T["random_pct"]),
            f"t-stat >= {need_t:.2f}": bool(st["t"] >= need_t),
        }
        verdict = "PASS" if all(checks.values()) else "FAIL"
        results.append(dict(id=w["id"], name=w["name"], verdict=verdict, stats=st, checks=checks))
        print(f"{verdict:4s} {w['name']:55s} trades {st['trades']:5d}  PF {st['pf']:.2f}  {st['totalR']:+7.1f}R  t {st['t']:.2f}/{need_t:.2f}  "
              f"double-cost PF {st['dbl_pf']:.2f}  beats random {st['beats_random']:.0f}%  markets {nm[0]}/{nm[1]}")
    if dry:
        print("dry run on shuffled prices: nothing written"); return
    os.makedirs(OUT, exist_ok=True)
    last = {m: str(data[m]["df"].index[-1]) for m in data}
    json.dump(dict(date=today, markets=list(data), markets_missing=missing, data_ends=last, need_t=need_t, results=results), open(RESULTS, "w"), indent=1, default=float)
    by_id = {r["id"]: r["verdict"] for r in results}
    for w in watch:
        if w["id"] in by_id:
            w["new_markets"] = by_id[w["id"]]
    json.dump(watch, open(WATCH, "w"), indent=1)
    passed = [r for r in results if r["verdict"] == "PASS"]
    with open(os.path.join(HERE, "JOURNAL.md"), "a") as j:
        j.write(f"\n### {today} · new-market test · {len(results)} watched ideas · {len(passed)} passed\n"
                f"- Markets: {', '.join(data)}." + (f" Left out (download failed): {', '.join(missing)}." if missing else "") + "\n"
                f"- Hourly bars from 2021-04-21 to {max(last.values())[:10]}. One run per idea. Needed t-stat {need_t:.2f}.\n")
        for r in results:
            s = r["stats"]; fails = [c for c, v in r["checks"].items() if not v]
            j.write(f"- `{r['name']}` · {r['verdict']}: {s['trades']} trades, profit factor {s['pf']:.2f}, {s['totalR']:+.1f}R, t-stat {s['t']:.2f}, "
                    f"markets {s['markets_profitable'][0]} of {s['markets_profitable'][1]}, double-cost profit factor {s['dbl_pf']:.2f}, beats {s['beats_random']:.0f}% of random entries"
                    + (f". Failed: {'; '.join(fails)}" if fails else "") + "\n")
    print(f"{len(passed)} of {len(results)} passed. Written to lab/newmarkets/results.json and the journal.")


if __name__ == "__main__":
    main()
