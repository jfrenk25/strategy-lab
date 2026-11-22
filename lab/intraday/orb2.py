"""Intraday study 2: 36 opening range variations on full-session 1-minute bars. One run.

Run from the repo root:
    python lab/intraday/orb2.py --dryrun    # same code on made-up prices, to check the mechanics; nothing is written
    python lab/intraday/orb2.py             # the one real run; refuses to run a second time

The rules are in LAB_RULES.md under "Intraday study 2". They were written before any 1-minute data reached the lab.
"""
import sys, os, json, datetime, itertools
from statistics import NormalDist
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.join(HERE, "..")
DATA = os.path.join(LAB, "data_1m")
RESULTS = os.path.join(HERE, "orb2_results.json")
MARKETS = ["NAS100", "SPX500", "USA30"]
COST = 0.00005                                          # 0.005% per round trip
SPLIT = datetime.date(2024, 1, 1)                       # before: screen years. From here on: confirm years.
OPEN, LAST_BREAK, CLOSE_EXIT = 9 * 60 + 30, 10 * 60 + 59, 15 * 60 + 55      # minutes after midnight, New York time
S = dict(days=150, t=1.65, pf=1.10)
C = dict(days=150, pf=1.15, min_survivors=5, years=(2024, 2025, 2026), years_ok=2)
VERSIONS = [dict(range=r, entry=e, exit=x, direction=d) for r, e, x, d in
            itertools.product((5, 15, 30), ("breakout", "fixed"), (10, 60, "close"), ("with", "against"))]


def name(v):
    return f"range{v['range']}.{v['entry']}.exit{v['exit']}.{v['direction']}"


def load(m, fake_seed=None):
    """Per day: minute-of-day (New York) and the open, high, low, close arrays."""
    if fake_seed is not None:                           # made-up prices for the dry run
        rng = np.random.default_rng(fake_seed)
        days = pd.bdate_range("2021-04-21", "2026-11-20", tz="UTC")
        t = days.repeat(495) + pd.to_timedelta(np.tile(np.arange(13 * 60, 21 * 60 + 15), len(days)), unit="m")
        c = 15000 * np.exp(np.cumsum(rng.normal(0, 0.0004, len(t)))); o = np.r_[c[0], c[:-1]]
        df = pd.DataFrame({"time": t, "open": o, "high": np.maximum(o, c) * 1.0002, "low": np.minimum(o, c) * 0.9998, "close": c})
    else:
        df = pd.read_csv(os.path.join(DATA, f"{m}_1m_full.csv.gz"))
        df["time"] = pd.to_datetime(df["time"], unit="s", utc=True)
    ny = df["time"].dt.tz_convert("America/New_York")
    df["day"] = ny.dt.date; df["mod"] = ny.dt.hour * 60 + ny.dt.minute
    df = df.sort_values("time")
    out = {}
    for day, g in df.groupby("day", sort=True):
        mod = g["mod"].to_numpy()
        out[day] = (dict(zip(mod.tolist(), range(len(mod)))), g["open"].to_numpy(), g["high"].to_numpy(), g["low"].to_numpy(), g["close"].to_numpy())
    return out


def day_trade(day, v):
    """Return before costs for one market on one day, or None if the version does not trade."""
    pos, o, h, l, c = day
    R = v["range"]
    idx = [pos[m] for m in range(OPEN, OPEN + R) if m in pos]
    if len(idx) < 0.8 * R:
        return None
    hi, lo = h[idx].max(), l[idx].min()
    side, entry_min = 0, None
    if v["entry"] == "fixed":
        check = OPEN + R + 14                           # the bar that ends 15 minutes after the range ends
        if check not in pos:
            return None
        cc = c[pos[check]]; side = 1 if cc > hi else (-1 if cc < lo else 0); entry_min = check + 1
    else:
        for m in range(OPEN + R, LAST_BREAK + 1):       # first close outside the range, before 11:00
            if m in pos:
                cc = c[pos[m]]
                if cc > hi or cc < lo:
                    side = 1 if cc > hi else -1; entry_min = m + 1; break
    if side == 0 or entry_min not in pos:
        return None
    exit_min = CLOSE_EXIT if v["exit"] == "close" else entry_min + v["exit"]
    if exit_min not in pos or exit_min <= entry_min:
        return None
    gross = side * (o[pos[exit_min]] / o[pos[entry_min]] - 1)
    return gross if v["direction"] == "with" else -gross


def run_version(v, data):
    """One row per (day, market) with the return before costs."""
    rows = [(d, m, g) for m in data for d, day in data[m].items() if (g := day_trade(day, v)) is not None]
    return pd.DataFrame(rows, columns=["day", "market", "gross"])


def stats(tr, cost=COST):
    """Statistics on daily averages: a day counts once however many of the three markets traded."""
    if tr.empty:
        return dict(days=0)
    daily = tr.groupby("day")["gross"].mean() - cost; r = daily.to_numpy()
    if len(r) < 3 or r.std(ddof=1) == 0:
        return dict(days=int(len(r)))
    wins, losses = r[r > 0], r[r <= 0]
    by_year = daily.groupby([d.year for d in daily.index]).sum()
    per_market = (tr.groupby("market")["gross"].mean() - cost)
    return dict(days=int(len(r)), trades=int(len(tr)), mean_pct=float(r.mean() * 100), total_pct=float(r.sum() * 100),
                t=float(r.mean() / (r.std(ddof=1) / np.sqrt(len(r)))), pf=float(wins.sum() / -losses.sum()) if losses.sum() < 0 else float("inf"),
                win_rate=float((r > 0).mean() * 100), mean_pct_double_cost=float((r - cost).mean() * 100),
                markets_positive=int((per_market > 0).sum()), per_market_mean_pct={k: round(float(x) * 100, 5) for k, x in per_market.items()},
                by_year_pct={int(k): round(float(x) * 100, 3) for k, x in by_year.items()})


def screen_checks(s):
    if "t" not in s:
        return {f"traded days >= {S['days']}": False}
    return {f"traded days >= {S['days']}": bool(s["days"] >= S["days"]), f"average above zero with t-stat >= {S['t']}": bool(s["mean_pct"] > 0 and s["t"] >= S["t"]),
            f"profit factor >= {S['pf']}": bool(s["pf"] >= S["pf"]), "positive on two of three markets": bool(s["markets_positive"] >= 2),
            "average above zero at double cost": bool(s["mean_pct_double_cost"] > 0)}


def confirm_checks(s, need_t):
    if "t" not in s:
        return {f"traded days >= {C['days']}": False}
    years_ok = sum(s["by_year_pct"].get(y, 0) > 0 for y in C["years"])
    return {f"traded days >= {C['days']}": bool(s["days"] >= C["days"]), f"average above zero with t-stat >= {need_t:.2f}": bool(s["mean_pct"] > 0 and s["t"] >= need_t),
            f"profit factor >= {C['pf']}": bool(s["pf"] >= C["pf"]), "positive on two of three markets": bool(s["markets_positive"] >= 2),
            "average above zero at double cost": bool(s["mean_pct_double_cost"] > 0), "positive in two of 2024, 2025, 2026": bool(years_ok >= C["years_ok"])}


def main():
    dry = "--dryrun" in sys.argv
    if os.path.exists(RESULTS) and not dry:
        print("Intraday study 2 has already been run. It runs once. See lab/intraday/orb2_results.json."); return
    missing = [m for m in MARKETS if not dry and not os.path.exists(os.path.join(DATA, f"{m}_1m_full.csv.gz"))]
    assert not missing, f"missing full-session files for {missing}: the study needs all three markets"
    data = {m: load(m, fake_seed=k + 1 if dry else None) for k, m in enumerate(MARKETS)}
    assert len(VERSIONS) == 36
    rows = []
    for v in VERSIONS:                                   # screen: the screen years only
        tr = run_version(v, data)
        s = stats(tr[tr["day"] < SPLIT]); ch = screen_checks(s)
        rows.append(dict(version=name(v), parts=v, screen=s, screen_checks=ch, screen_pass=all(ch.values()), trades=tr))
    survivors = [r for r in rows if r["screen_pass"]]
    need_t = NormalDist().inv_cdf(1 - 0.05 / max(len(survivors), C["min_survivors"]))
    for r in rows:                                       # confirm: only survivors ever have their confirm years computed
        tr = r.pop("trades")
        if r["screen_pass"]:
            s = stats(tr[tr["day"] >= SPLIT]); ch = confirm_checks(s, need_t)
            r.update(confirm=s, confirm_checks=ch, verdict="CONFIRMED" if all(ch.values()) else "REJECT")
        else:
            r["verdict"] = "REJECT"
        s = r["screen"]; line = f"{s['days']:4d} days, avg {s['mean_pct']:+.4f}%, PF {s['pf']:.2f}, t {s['t']:+.2f}, markets {s['markets_positive']}/3" if "t" in s else f"{s['days']} days"
        tail = ""
        if "confirm" in r:
            c = r["confirm"]; tail = f" | confirm: {c['days']} days, avg {c['mean_pct']:+.4f}%, PF {c['pf']:.2f}, t {c['t']:+.2f}/{need_t:.2f}" if "t" in c else f" | confirm: {c['days']} days"
        print(f"{r['verdict']:9s} {r['version']:36s} screen: {line}{' PASS' if r['screen_pass'] else ''}{tail}")
    confirmed = [r for r in rows if r["verdict"] == "CONFIRMED"]
    print(f"{len(rows)} versions, {len(survivors)} passed the screen, {len(confirmed)} confirmed (bar {need_t:.2f})")
    if dry:
        print("dry run on made-up prices: nothing written"); return
    today = datetime.date.today().isoformat()
    days = sorted(set().union(*[set(data[m]) for m in MARKETS]))
    json.dump(dict(date=today, first_day=str(days[0]), last_day=str(days[-1]), need_t=need_t, survivors=len(survivors), confirmed=len(confirmed), versions=rows),
              open(RESULTS, "w"), indent=1, default=float)
    with open(os.path.join(LAB, "JOURNAL.md"), "a") as j:
        j.write(f"\n### {today} · intraday study 2 · 36 opening range variations · {len(survivors)} passed the screen, {len(confirmed)} confirmed\n"
                f"- Nasdaq 100, S&P 500 and Dow, 1-minute bars, {days[0]} to {days[-1]}. Screen: before 2024. Confirm: 2024 on, t-stat bar {need_t:.2f}.\n")
        for r in rows:
            s = r["screen"]
            if "t" not in s:
                j.write(f"- `{r['version']}` · REJECT: {s['days']} traded days\n"); continue
            txt = f"- `{r['version']}` · {r['verdict']}: screen {s['days']} days, average {s['mean_pct']:+.4f}%, profit factor {s['pf']:.2f}, t-stat {s['t']:.2f}"
            if "confirm" in r and "t" in r["confirm"]:
                c = r["confirm"]; fails = [k for k, ok in r["confirm_checks"].items() if not ok]
                txt += f"; confirm {c['days']} days, average {c['mean_pct']:+.4f}%, profit factor {c['pf']:.2f}, t-stat {c['t']:.2f}" + (f". Failed: {'; '.join(fails)}" if fails else "")
            j.write(txt + "\n")
    print("written to lab/intraday/orb2_results.json and the journal")


if __name__ == "__main__":
    main()
