"""Intraday study 1: opening range breakout on 1-minute bars. One run.

Run from the repo root:
    python lab/intraday/orb.py --dryrun    # same code on made-up prices, to check the mechanics; nothing is written
    python lab/intraday/orb.py             # the one real run; refuses to run a second time

The rules are in LAB_RULES.md under "Intraday study 1". They were written before the data was downloaded.
"""
import sys, os, json, datetime
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.join(HERE, "..")
DATA = os.path.join(LAB, "data_1m")
RESULTS = os.path.join(HERE, "orb_results.json")
MARKETS = ["NAS100", "SPX500", "USA30"]                 # the verdict comes from NAS100; the others are reported only
COST, NEED_T = 0.00005, 2.58                            # 0.005% per round trip; t-stat bar for two tests
SPLIT = datetime.date(2024, 1, 1)                       # before: unseen by the video. From here on: the video's years.
T = dict(trades=150, pf=1.15, years_ok=2, relvol=(0.5, 1.5), range_bars=12)


def load(m, fake_seed=None):
    if fake_seed is not None:                           # made-up prices for the dry run
        rng = np.random.default_rng(fake_seed)
        days = pd.bdate_range("2021-04-21", "2026-11-20", tz="UTC")
        t = (days.repeat(165) + pd.to_timedelta(np.tile(np.arange(13 * 60, 15 * 60 + 45), len(days)), unit="m"))
        c = 15000 * np.exp(np.cumsum(rng.normal(0, 0.0004, len(t)))); o = np.r_[c[0], c[:-1]]
        df = pd.DataFrame({"time": t, "open": o, "high": np.maximum(o, c) * 1.0002, "low": np.minimum(o, c) * 0.9998, "close": c, "volume": rng.lognormal(0, 0.5, len(t))})
    else:
        df = pd.read_csv(os.path.join(DATA, f"{m}_1m.csv.gz"))
        df["time"] = pd.to_datetime(df["time"], unit="s", utc=True)
    ny = df["time"].dt.tz_convert("America/New_York")
    df["day"] = ny.dt.date; df["hm"] = ny.dt.hour * 100 + ny.dt.minute
    return df.sort_values("time").reset_index(drop=True)


def trades(df, use_filter):
    """One row per traded day: the day, the side and the return before costs."""
    rows = []
    for day, g in df.groupby("day", sort=True):
        hm = g["hm"].to_numpy()
        rng = g[(hm >= 930) & (hm <= 944)]
        if len(rng) < T["range_bars"]:
            continue
        pos = {h: i for i, h in enumerate(hm)}
        if 959 not in pos or 1000 not in pos or 1010 not in pos:
            continue
        hi, lo = rng["high"].max(), rng["low"].min(); i = pos[959]
        c = g["close"].iloc[i]
        side = 1 if c > hi else (-1 if c < lo else 0)
        if side == 0:
            continue
        if use_filter:
            if i < 14:
                continue
            base = g["volume"].iloc[i - 14:i].mean()
            if not base > 0:
                continue
            rv = g["volume"].iloc[i] / base
            if not (T["relvol"][0] <= rv <= T["relvol"][1]):
                continue
        rows.append((day, side, side * (g["open"].iloc[pos[1010]] / g["open"].iloc[pos[1000]] - 1)))
    return pd.DataFrame(rows, columns=["day", "side", "gross"])


def stats(tr, cost=COST):
    r = (tr["gross"] - cost).to_numpy()
    if len(r) < 3:
        return dict(trades=int(len(r)))
    wins, losses = r[r > 0], r[r <= 0]
    by_year = tr.assign(net=r, year=[d.year for d in tr["day"]]).groupby("year")["net"].sum()
    return dict(trades=int(len(r)), mean_pct=float(r.mean() * 100), total_pct=float(r.sum() * 100),
                t=float(r.mean() / (r.std(ddof=1) / np.sqrt(len(r)))) if r.std(ddof=1) > 0 else float("nan"),
                pf=float(wins.sum() / -losses.sum()) if losses.sum() < 0 else float("inf"),
                win_rate=float((r > 0).mean() * 100), avg_win_pct=float(wins.mean() * 100) if len(wins) else 0.0, avg_loss_pct=float(losses.mean() * 100) if len(losses) else 0.0,
                mean_pct_double_cost=float((tr["gross"] - 2 * cost).mean() * 100), by_year_pct={int(k): round(float(v) * 100, 3) for k, v in by_year.items()})


def judge(s):
    if s.get("trades", 0) < 3:
        return {"at least 150 trades": False}, "FAIL"
    years_ok = sum(s["by_year_pct"].get(y, 0) > 0 for y in (2021, 2022, 2023))
    checks = {f"trades >= {T['trades']}": s["trades"] >= T["trades"], f"average above zero with t-stat >= {NEED_T}": s["mean_pct"] > 0 and s["t"] >= NEED_T,
              f"profit factor >= {T['pf']}": s["pf"] >= T["pf"], "average above zero at double cost": s["mean_pct_double_cost"] > 0,
              "positive in two of 2021, 2022, 2023": years_ok >= T["years_ok"]}
    checks = {k: bool(v) for k, v in checks.items()}
    return checks, ("PASS" if all(checks.values()) else "FAIL")


def main():
    dry = "--dryrun" in sys.argv
    if os.path.exists(RESULTS) and not dry:
        print("Intraday study 1 has already been run. It runs once. See lab/intraday/orb_results.json."); return
    out = dict(date=datetime.date.today().isoformat(), markets={}, missing=[])
    for k, m in enumerate(MARKETS):
        if not dry and not os.path.exists(os.path.join(DATA, f"{m}_1m.csv.gz")):
            out["missing"].append(m); continue
        df = load(m, fake_seed=k + 1 if dry else None)
        res = dict(days=int(df["day"].nunique()), first=str(df["day"].min()), last=str(df["day"].max()))
        for label, use_filter in (("A_volume_filter", True), ("B_no_filter", False)):
            tr = trades(df, use_filter)
            unseen, video = tr[tr["day"] < SPLIT], tr[tr["day"] >= SPLIT]
            su, sv = stats(unseen), stats(video); checks, verdict = judge(su)
            res[label] = dict(unseen_years=su, video_years=sv, checks=checks, verdict=verdict)
            f = lambda s: (f"{s['trades']:4d} trades, win {s['win_rate']:.0f}%, avg {s['mean_pct']:+.4f}%, PF {s['pf']:.2f}, t {s['t']:+.2f}" if s.get("trades", 0) >= 3 else f"{s.get('trades', 0)} trades")
            print(f"{m:7s} {label:16s} unseen years: {f(su)} -> {verdict:4s} | video's years: {f(sv)}")
        out["markets"][m] = res
    if dry:
        print("dry run on made-up prices: nothing written"); return
    assert "NAS100" in out["markets"], "the Nasdaq file is missing: nothing was run or written"
    json.dump(out, open(RESULTS, "w"), indent=1, default=float)
    n = out["markets"]["NAS100"]
    with open(os.path.join(LAB, "JOURNAL.md"), "a") as j:
        j.write(f"\n### {out['date']} · intraday study 1 · opening range breakout · A {n['A_volume_filter']['verdict']}, B {n['B_no_filter']['verdict']}\n"
                f"- Source: YouTube, \"I Built a Trading Bot to Pass Prop Firm Challenges\" (Jan - Algo Trader, 2026-10-29). Lab version of the core rule, fixed in LAB_RULES.md before the data arrived.\n"
                f"- Nasdaq 100, 1-minute bars, {n['first']} to {n['last']}. Verdict from the years before 2024; needed t-stat {NEED_T}.\n")
        for m, res in out["markets"].items():
            for label in ("A_volume_filter", "B_no_filter"):
                u, v = res[label]["unseen_years"], res[label]["video_years"]
                line = lambda s: (f"{s['trades']} trades, win rate {s['win_rate']:.0f}%, average {s['mean_pct']:+.4f}% a trade, profit factor {s['pf']:.2f}, t-stat {s['t']:.2f}" if s.get("trades", 0) >= 3 else f"{s.get('trades', 0)} trades")
                fails = [c for c, ok in res[label]["checks"].items() if not ok]
                j.write(f"- {m}, test {label[0]} ({'volume filter' if label[0] == 'A' else 'no filter'}): before 2024: {line(u)}. From 2024: {line(v)}."
                        + (f" {'Verdict' if m == 'NAS100' else 'Reported only'}: {res[label]['verdict']}." ) + (f" Failed: {'; '.join(fails)}." if fails and m == "NAS100" else "") + "\n")
        if out["missing"]:
            j.write(f"- Not downloaded: {', '.join(out['missing'])}.\n")
    print("written to lab/intraday/orb_results.json and the journal")


if __name__ == "__main__":
    main()
