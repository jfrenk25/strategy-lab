"""Forward watch: track registered ideas on price bars that did not exist when they were registered.

Run from the repo root:
    python lab/forward.py              # register any new candidates or near misses, then update every watched idea
The rules are in LAB_RULES.md under "Forward watch". Thresholds here must match that section.
"""
import sys, os, json, glob, datetime
from statistics import NormalDist
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lab, screen

OUT = os.path.join(HERE, "forward")
WATCH = os.path.join(OUT, "watchlist.json")
VERDICT_TRADES = 200
F = dict(pf=1.15, market_share=0.5)


def register(today):
    """Add every candidate and near miss from the screen that is not on the watchlist yet."""
    watch = json.load(open(WATCH)) if os.path.exists(WATCH) else []
    known = {w["id"] for w in watch}; added = []
    start = (datetime.date.fromisoformat(today) + datetime.timedelta(days=1)).isoformat()
    for f in sorted(glob.glob(os.path.join(HERE, "screen", "confirm", "*.json"))):
        r = json.load(open(f))
        if r["id"] in known:
            continue
        checks = list(r["checks"].items())
        others_ok = all(v for k, v in checks if not k.startswith("t-stat"))
        bar_ok = all(v for k, v in checks if k.startswith("t-stat"))
        why = "candidate" if r["verdict"] == "CANDIDATE" else ("near miss" if others_ok and not bar_ok else None)
        if why is None:
            continue
        watch.append(dict(id=r["id"], name=r["name"], spec=r["spec"], why=why, registered=today, start=start,
                          confirm=dict(trades=r["confirm"]["trades"], pf=round(r["confirm"]["pf"], 3), t=round(r["confirm"]["t"], 2), need_t=round(r["need_t"], 2)),
                          verdict=None))
        added.append(r["name"])
    if added:
        watch.sort(key=lambda w: (w["registered"], -w["confirm"]["t"]))
        os.makedirs(OUT, exist_ok=True); json.dump(watch, open(WATCH, "w"), indent=1)
    return watch, added


def forward_stats(spec, start, data):
    runs = screen.run_spec(spec, data); t0 = pd.Timestamp(start, tz="UTC")
    R, R2, by_market, rows = [], [], {}, []
    for m, run in runs.items():
        times = data[m]["df"].index; ei, r, sd = run["x1"]; ei2, r2, _ = run["x2"]
        k = times[ei] >= t0; R.append(r[k]); R2.append(r2[times[ei2] >= t0])
        if k.any():
            by_market[m] = float(r[k].sum())
            rows += [(str(times[i]), m, int(s), round(float(x), 3)) for i, s, x in zip(ei[k], sd[k], r[k])]
    R = np.concatenate(R); R2 = np.concatenate(R2)
    return dict(trades=int(len(R)), pf=lab._pf(R) if len(R) else None, totalR=round(float(R.sum()), 2) if len(R) else 0.0,
                t=lab._tstat(R) if len(R) > 2 else None, dbl_pf=lab._pf(R2) if len(R2) else None,
                markets_profitable=[int(sum(v > 0 for v in by_market.values())), len(by_market)],
                by_market={k: round(v, 1) for k, v in by_market.items()}), sorted(rows)


def main():
    today = datetime.date.today().isoformat()
    screen.load_registry()
    watch, added = register(today)
    if added:
        with open(os.path.join(HERE, "JOURNAL.md"), "a") as j:
            j.write(f"\n### {today} · forward watch · {len(added)} ideas registered\n"
                    + "".join(f"- `{n}`\n" for n in added)
                    + f"- Forward trades count from {watch[-1]['start']} 00:00 UTC. Verdict at {VERDICT_TRADES} trades. Rules: \"Forward watch\" in `LAB_RULES.md`.\n")
        print(f"registered {len(added)} ideas for the forward watch")
    if not watch:
        print("nothing is on the forward watch"); return
    data = screen.load(); need_t = NormalDist().inv_cdf(1 - 0.05 / len(watch))
    last_bar = {m: str(D["df"].index[-1]) for m, D in data.items()}
    status = dict(updated=today, watched=len(watch), verdict_trades=VERDICT_TRADES, need_t=round(need_t, 2), data_ends=last_bar, ideas=[])
    os.makedirs(os.path.join(OUT, "trades"), exist_ok=True)
    for w in watch:
        st, rows = forward_stats(w["spec"], w["start"], data)
        with open(os.path.join(OUT, "trades", f"{w['id']}.csv"), "w") as fh:
            fh.write("entry_time,market,side,R\n" + "".join(f"{a},{b},{c},{d}\n" for a, b, c, d in rows))
        if w["verdict"] is None and st["trades"] >= VERDICT_TRADES:
            nm = st["markets_profitable"]
            checks = {f"profit factor >= {F['pf']}": bool(st["pf"] >= F["pf"]), "profit factor > 1 at double costs": bool(st["dbl_pf"] > 1.0),
                      "profitable in half the markets that traded": bool(nm[1] and nm[0] / nm[1] >= F["market_share"]),
                      f"t-stat >= {need_t:.2f} ({len(watch)} ideas watched)": bool(st["t"] >= need_t)}
            w["verdict"] = dict(result="FORWARD PASS" if all(checks.values()) else "FORWARD FAIL", date=today, stats=st, checks=checks)
            with open(os.path.join(HERE, "JOURNAL.md"), "a") as j:
                fails = [c for c, v in checks.items() if not v]
                j.write(f"\n### {today} · forward verdict · `{w['name']}` · {w['verdict']['result']}\n"
                        f"- Forward trades since {w['start']}: {st['trades']}, profit factor {st['pf']:.2f}, {st['totalR']:+.1f}R, t-stat {st['t']:.2f} (needed {need_t:.2f})\n"
                        + (f"- Failed: {'; '.join(fails)}\n" if fails else "- Passed every forward check\n"))
        state = w["verdict"]["result"] if w["verdict"] else "WATCHING"
        status["ideas"].append(dict(id=w["id"], name=w["name"], why=w["why"], start=w["start"], status=state, **st))
        pf = "n/a" if st["pf"] is None else f"{st['pf']:.2f}"
        print(f"{state:13s} {w['name']:55s} forward trades {st['trades']:4d} of {VERDICT_TRADES}  PF {pf}  {st['totalR']:+.1f}R")
    json.dump(watch, open(WATCH, "w"), indent=1)
    json.dump(status, open(os.path.join(OUT, "status.json"), "w"), indent=1, default=float)
    print("price data ends: " + ", ".join(f"{m} {t[:10]}" for m, t in last_bar.items()))


if __name__ == "__main__":
    main()
