"""Intraday study 4: the six "with the break, exit at 15:55" versions judged as one group on 2024 onward. One run.

Run from the repo root:
    python lab/intraday/orb4.py --dryrun    # same code on made-up prices; nothing is written
    python lab/intraday/orb4.py             # the one real run; refuses to run a second time

The rules are in LAB_RULES.md under "Intraday study 4". They were written before these versions were computed on 2024 onward.
"""
import sys, os, json, datetime
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orb2

RESULTS = os.path.join(orb2.HERE, "orb4_results.json")
NEED_T, COST = 2.58, orb2.COST
T = dict(days=150, pf=1.15, years=(2024, 2025, 2026), years_ok=2, versions_ok=4)
GROUP = [v for v in orb2.VERSIONS if v["exit"] == "close" and v["direction"] == "with"]


def side_of(day, v):
    """The side study 2's entry rule takes on this day (+1 buy, -1 sell, 0 none). Same rule as orb2.day_trade, written out again to get the side."""
    pos, o, h, l, c = day; R = v["range"]
    idx = [pos[m] for m in range(orb2.OPEN, orb2.OPEN + R) if m in pos]
    if len(idx) < 0.8 * R:
        return 0
    hi, lo = h[idx].max(), l[idx].min()
    if v["entry"] == "fixed":
        m = orb2.OPEN + R + 14
        return 0 if m not in pos else (1 if c[pos[m]] > hi else (-1 if c[pos[m]] < lo else 0))
    for m in range(orb2.OPEN + R, orb2.LAST_BREAK + 1):
        if m in pos and (c[pos[m]] > hi or c[pos[m]] < lo):
            return 1 if c[pos[m]] > hi else -1
    return 0


def all_trades(data):
    rows = []
    for v in GROUP:
        for m in data:
            for d, day in data[m].items():
                if d < orb2.SPLIT:
                    continue                             # the years before 2024 are not part of this study
                g = orb2.day_trade(day, v)
                if g is not None:
                    s = side_of(day, v); assert s != 0, "side and trade disagree"
                    rows.append((orb2.name(v), d, m, s, g))
    return pd.DataFrame(rows, columns=["version", "day", "market", "side", "gross"])


def daily(tr, cost=COST):
    """Per version: average across markets. Then per day: average across versions."""
    if tr.empty:
        return pd.Series(dtype=float)
    return (tr.groupby(["version", "day"])["gross"].mean() - cost).groupby("day").mean()


def stats(d):
    r = d.to_numpy()
    if len(r) < 3 or r.std(ddof=1) == 0:
        return dict(days=int(len(r)))
    wins, losses = r[r > 0], r[r <= 0]
    by_year = d.groupby([x.year for x in d.index]).sum()
    return dict(days=int(len(r)), mean_pct=float(r.mean() * 100), total_pct=float(r.sum() * 100), t=float(r.mean() / (r.std(ddof=1) / np.sqrt(len(r)))),
                pf=float(wins.sum() / -losses.sum()) if losses.sum() < 0 else float("inf"), win_rate=float((r > 0).mean() * 100),
                by_year_pct={int(k): round(float(x) * 100, 3) for k, x in by_year.items()})


def main():
    dry = "--dryrun" in sys.argv
    if os.path.exists(RESULTS) and not dry:
        print("Intraday study 4 has already been run. It runs once. See lab/intraday/orb4_results.json."); return
    assert len(GROUP) == 6
    data = {m: orb2.load(m, fake_seed=k + 1 if dry else None) for k, m in enumerate(orb2.MARKETS)}
    tr = all_trades(data)
    g = stats(daily(tr)); mean = lambda x: float(x.mean() * 100) if len(x) else float("nan")
    per_market = {m: mean(daily(tr[tr["market"] == m])) for m in orb2.MARKETS}
    per_version = {name: stats(daily(tr[tr["version"] == name])) for name in [orb2.name(v) for v in GROUP]}
    by_side = lambda k: (lambda r: dict(trades=int(len(r)), mean_pct=float(r.mean() * 100) if len(r) else float("nan"), win_rate=float((r > 0).mean() * 100) if len(r) else float("nan")))((tr[tr["side"] == k]["gross"] - COST).to_numpy())
    shorts, longs = by_side(-1), by_side(1)                 # every trade counted equally: averaging these per day is biased (see the rules)
    double = mean(daily(tr, cost=2 * COST))
    ok = "t" in g
    checks = {f"traded days >= {T['days']}": g["days"] >= T["days"],
              f"average above zero with t-stat >= {NEED_T}": ok and g["mean_pct"] > 0 and g["t"] >= NEED_T,
              f"profit factor >= {T['pf']}": ok and g["pf"] >= T["pf"],
              "average above zero on two of three markets": sum(x > 0 for x in per_market.values()) >= 2,
              "average above zero at double cost": double > 0,
              "positive in two of 2024, 2025, 2026": ok and sum(g["by_year_pct"].get(y, 0) > 0 for y in T["years"]) >= T["years_ok"],
              "four of six versions above zero alone": sum(s.get("mean_pct", -1) > 0 for s in per_version.values()) >= T["versions_ok"],
              "short trades alone above zero": shorts["mean_pct"] > 0}
    checks = {k: bool(x) for k, x in checks.items()}; verdict = "PASS" if all(checks.values()) else "FAIL"
    line = lambda s: (f"{s['days']} days, win rate {s['win_rate']:.0f}%, average {s['mean_pct']:+.4f}% a day, profit factor {s['pf']:.2f}, t-stat {s['t']:.2f}" if "t" in s else f"{s['days']} days")
    print(f"group: {line(g)} -> {verdict}"); print(f"  by year: {g.get('by_year_pct')} | double cost avg {double:+.4f}% | per market {({k: round(x, 4) for k, x in per_market.items()})}")
    side_line = lambda s: f"{s['trades']} trades, win rate {s['win_rate']:.0f}%, average {s['mean_pct']:+.4f}% a trade"
    print(f"  longs: {side_line(longs)}\n  shorts: {side_line(shorts)}")
    for name, s in per_version.items():
        print(f"  {name:34s} {line(s)}")
    for k, x in checks.items():
        print(f"  {'ok  ' if x else 'FAIL'} {k}")
    if dry:
        print("dry run on made-up prices: nothing written"); return
    today = datetime.date.today().isoformat(); days = sorted(tr["day"].unique())
    json.dump(dict(date=today, first_day=str(days[0]), last_day=str(days[-1]), need_t=NEED_T, verdict=verdict, checks=checks, group=g, mean_pct_double_cost=double,
                   per_market_mean_pct=per_market, per_version=per_version, longs=longs, shorts=shorts, trades=int(len(tr))), open(RESULTS, "w"), indent=1, default=float)
    fails = [k for k, x in checks.items() if not x]
    with open(os.path.join(orb2.LAB, "JOURNAL.md"), "a") as j:
        j.write(f"\n### {today} · intraday study 4 · hold to the close, six versions as one group · {verdict}\n"
                f"- Nasdaq 100, S&P 500 and Dow, 1-minute bars, {days[0]} to {days[-1]}. One test, t-stat bar {NEED_T}. Rules fixed in LAB_RULES.md before these versions were computed on these years.\n"
                f"- Group: {line(g)}. By year: {g.get('by_year_pct')}. Average at double cost {double:+.4f}%. Per market: {({k: round(x, 4) for k, x in per_market.items()})}.\n"
                f"- Long trades alone: {side_line(longs)}. Short trades alone: {side_line(shorts)}.\n")
        for name, s in per_version.items():
            j.write(f"- `{name}` alone: {line(s)}\n")
        j.write(f"- Verdict: {verdict}." + (f" Failed: {'; '.join(fails)}." if fails else "") + "\n")
    print("written to lab/intraday/orb4_results.json and the journal")


if __name__ == "__main__":
    main()
