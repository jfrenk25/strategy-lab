"""Study 14: Gapline ORB. Rules: claude/gapline-orb-rules-2026-11-25.md (written before this ran).

Usage: python -I gapline_orb.py MODE [LAB_DIR] [OUT_JSON]
  MODE  selftest  hand-built bars for the exit logic (no data read)
        dryrun    the same code on made-up prices with no edge
        run       the study (once)
LAB_DIR is the repo's lab folder (holds costs.py, data_1m, data, data_new).
"""
import json
import os
import sys

import numpy as np
import pandas as pd

COST = 0.00005                     # per side, NAS100 / SPX500 / USA30 in lab/costs.py (checked against the file in main)
MIN_DIST = 0.0003                  # stop distance floor, as a fraction of price
TARGET_R = 1.5
EMA5, EMA_H = 200, 17
NEED_T, NEED_DAYS, NEED_PF, NEED_YEARS = 2.58, 150, 1.15, 4
RISKS = (0.25, 0.5, 0.75, 1.0, 1.5)
GAP = {"NAS100": ("points", 0.5), "SPX500": ("frac", 0.000025), "USA30": ("frac", 0.000025)}
HOURLY = {"NAS100": "data_new/NAS100_1h.csv.gz", "SPX500": "data_new/SPX500_1h.csv.gz", "USA30": "data/USA30_1h.csv.gz"}
FIRMS = {   # copied from claude/qs_challenge.py
    "FTMO 1-Step": dict(target=10.0, daily=3.0, ref="balance", maxloss=10.0, trailing=True, need=0, best=0.5),
    "The5ers 1-step": dict(target=10.0, daily=3.0, ref="higher", maxloss=6.0, trailing=False, need=3, best=None),
}
CAP = 500


def challenge(tab, S, size):
    """Copied unchanged from claude/qs_challenge.py."""
    a, m_, d_, f0, f1 = (tab[k].to_numpy() for k in ("a", "dmin", "dbal", "flat0", "flat1"))
    n = len(tab)
    res = []
    for s in range(n - CAP):
        if not f0[s]:
            continue
        bal = hwm = best = 0.0
        pdays = 0
        out, took = "dropped", None
        for k in range(s, s + CAP):
            fl, m, d = a[k] * size, m_[k] * size, d_[k] * size
            if S["trailing"]:
                hwm = max(hwm, bal)
            ref = fl if S["ref"] == "balance" else min(fl, 0.0)
            floor = hwm - S["maxloss"] if S["trailing"] else -S["maxloss"]
            if m + ref <= -S["daily"] + 1e-9:
                out = "breach_daily"; break
            if bal + fl + m <= floor + 1e-9:
                out = "breach_max"; break
            bal += d
            best = max(best, d)
            pdays += d >= 0.5 - 1e-9
            ok = bal >= S["target"] - 1e-9 and f1[k] and pdays >= S["need"]
            if S["best"] is not None:
                ok = ok and best <= S["best"] * bal + 1e-9
            if ok:
                out, took = "passed", k - s + 1; break
        res.append((out, took))
    r = pd.DataFrame(res, columns=["o", "d"])
    share = r["o"].value_counts(normalize=True)
    return {"starts": int(len(r)), "passed_pct": round(100 * float(share.get("passed", 0)), 1),
            "breach_daily_pct": round(100 * float(share.get("breach_daily", 0)), 1),
            "breach_max_pct": round(100 * float(share.get("breach_max", 0)), 1),
            "dropped_pct": round(100 * float(share.get("dropped", 0)), 1),
            "median_days_to_pass": None if r["d"].isna().all() else float(r["d"].median())}


def walk(o, h, l, c, i, stop, target):
    """From bar i (entry at o[i]) to the last bar: (exit index, exit price, kind, both_touched). Stop wins a bar that touches both."""
    for j in range(i, len(o)):
        if l[j] <= stop:
            return j, float(min(o[j], stop)), "stop", bool(h[j] >= target)
        if h[j] >= target:
            return j, float(target), "target", False
    j = len(o) - 1
    return j, float(c[j]), "close", False


def trade_day(mins, o, h, l, c, prev_close, ema0, gap_rule, use_filters, cost=COST):
    """One day. mins = minutes after midnight of each 1-minute bar (from 9:00 on). Returns (trades, day low point in R).
    A trade is a dict with R, kind, both, entry minute. Returns None if the day is skipped."""
    pos = {int(m): k for k, m in enumerate(mins)}
    if 15 * 60 + 59 not in pos or 9 * 60 + 30 not in pos:
        return None
    rb = [pos[m] for m in range(570, 585) if m in pos]
    if len(rb) < 12:
        return None
    last = pos[15 * 60 + 59]
    r_hi, r_lo = float(max(h[k] for k in rb)), float(min(l[k] for k in rb))
    # moving average: start value at 9:00, then every 5-minute close from 9:00 on
    ema, a5 = ema0, 2.0 / (EMA5 + 1)
    bars5 = {}
    for b in range(540, 16 * 60, 5):
        ks = [pos[m] for m in range(b, b + 5) if m in pos]
        if ks:
            ema = ema + a5 * (c[ks[-1]] - ema)
            bars5[b] = (float(c[ks[-1]]), ema)
    open930 = float(o[pos[570]])
    if use_filters:
        kind, x = gap_rule
        need = x if kind == "points" else x * prev_close
        if open930 - prev_close < need:
            return [], 0.0
    trades, realized, low_point, free_after = [], 0.0, 0.0, -1
    for b in range(585, 15 * 60 + 50, 5):                        # signal bars start 9:45 ... 15:45
        if b not in bars5 or b + 5 < free_after:               # the signal bar must close after the last exit
            continue
        close5, ema_b = bars5[b]
        if not (close5 > r_hi and (close5 > ema_b or not use_filters)):
            continue
        if b + 5 not in pos:
            continue
        i = pos[b + 5]
        if i > last:
            continue
        entry = float(o[i])
        dist = entry - r_lo
        if dist <= 0:
            continue
        denom = max(dist, MIN_DIST * entry) / entry
        target = entry + TARGET_R * dist
        j, px, kind, both = walk(o[:last + 1], h[:last + 1], l[:last + 1], c[:last + 1], i, r_lo, target)
        costs = 2 * cost + (cost if kind == "stop" else 0.0)
        R = (px / entry - 1 - costs) / denom
        worst_open = (float(np.min(l[i:j + 1])) if kind != "stop" else px) / entry - 1
        low_point = min(low_point, realized + min((worst_open - cost) / denom, R))
        realized += R
        low_point = min(low_point, realized)
        trades.append({"R": R, "kind": kind, "both": both, "entry_min": int(mins[i]), "exit_min": int(mins[j])})
        free_after = int(mins[j]) + 1 if kind != "close" else 10 ** 6
    return trades, low_point


def load(lab, market, fake_seed=None):
    if fake_seed is not None:
        rng = np.random.default_rng(fake_seed)
        days = pd.bdate_range("2021-04-21", "2026-11-19")
        mins = np.arange(540, 16 * 60 + 15)
        ts = (days.repeat(len(mins)) + pd.to_timedelta(np.tile(mins, len(days)), unit="m"))
        cl = 15000 * np.exp(np.cumsum(rng.normal(0, 0.0004, len(ts)))); op = np.r_[cl[0], cl[:-1]]
        m = pd.DataFrame({"ts": ts, "open": op, "high": np.maximum(op, cl) * 1.0002, "low": np.minimum(op, cl) * 0.9998, "close": cl})
        hh = m[m["ts"].dt.hour * 60 + m["ts"].dt.minute == 540].copy()        # one made-up hourly bar a day, 8:00 to 9:00
        hh["ts"] = hh["ts"].dt.normalize() + pd.Timedelta(hours=8); hh["close"] = hh["open"]
        return m, hh[["ts", "close"]].reset_index(drop=True)
    m = pd.read_csv(os.path.join(lab, "data_1m", f"{market}_1m_full.csv.gz"))
    m["ts"] = pd.to_datetime(m["time"], unit="s", utc=True).dt.tz_convert("America/New_York").dt.tz_localize(None)
    hh = pd.read_csv(os.path.join(lab, HOURLY[market]))
    hh["ts"] = pd.to_datetime(hh["time"], utc=True).dt.tz_convert("America/New_York").dt.tz_localize(None)
    return m.sort_values("ts").reset_index(drop=True), hh.sort_values("ts").reset_index(drop=True)[["ts", "close"]]


def run_market(m, hh, gap_rule, use_filters=True, cost=COST):
    """Returns a per-day table (every usable day) and the trade list."""
    hh = hh.copy()
    hh["ema"] = hh["close"].ewm(span=EMA_H, adjust=False).mean()
    h_ts, h_ema = hh["ts"].to_numpy(), hh["ema"].to_numpy()
    m = m[m["ts"].dt.hour * 60 + m["ts"].dt.minute >= 540]
    rows, trades, prev_close = [], [], None
    for day, g in m.groupby(m["ts"].dt.normalize(), sort=True):
        mins = (g["ts"].dt.hour * 60 + g["ts"].dt.minute).to_numpy()
        o, h, l, c = (g[k].to_numpy(float) for k in ("open", "high", "low", "close"))
        has_close = (mins == 959).any()
        k = np.searchsorted(h_ts, np.datetime64(day + pd.Timedelta(hours=9)), side="left") - 1    # last hourly bar starting before 9:00
        fresh = k >= EMA_H and (day + pd.Timedelta(hours=9) - pd.Timestamp(h_ts[k])) <= pd.Timedelta(hours=1)
        if prev_close is not None and fresh:
            res = trade_day(mins, o, h, l, c, prev_close, float(h_ema[k]), gap_rule, use_filters, cost)
            if res is not None:
                tr, low = res
                for t in tr:
                    t["day"] = day
                trades += tr
                rows.append({"day": day, "dbal": sum(t["R"] for t in tr), "dmin": low, "n": len(tr)})
        prev_close = float(c[mins == 959][-1]) if has_close else None
    tab = pd.DataFrame(rows)
    tab["a"] = 0.0; tab["flat0"] = True; tab["flat1"] = True
    return tab, trades


def stats(tab):
    d = tab[tab["n"] > 0]["dbal"].to_numpy()
    if len(d) < 2:
        return {"traded_days": int(len(d))}
    wins, losses = d[d > 0].sum(), -d[d < 0].sum()
    return {"traded_days": int(len(d)), "trades": int(tab["n"].sum()), "win_day_pct": round(100 * float((d > 0).mean()), 1),
            "avg_R_per_day": round(float(d.mean()), 4), "sum_R": round(float(d.sum()), 1),
            "profit_factor": round(float(wins / losses), 2) if losses > 0 else None,
            "t_stat": round(float(d.mean() / (d.std(ddof=1) / np.sqrt(len(d)))), 2)}


def describe(tab, trades):
    s = stats(tab)
    yr = tab.groupby(tab["day"].dt.year)["dbal"].sum()
    s["by_year_sum_R"] = {int(y): round(float(v), 1) for y, v in yr.items()}
    s["years_positive"] = int((yr > 0).sum())
    kinds = pd.Series([t["kind"] for t in trades]).value_counts(normalize=True)
    s["exits_pct"] = {k: round(100 * float(v), 1) for k, v in kinds.items()}
    s["both_touched_bars"] = int(sum(t["both"] for t in trades))
    s["avg_R_per_trade"] = round(float(np.mean([t["R"] for t in trades])), 4)
    s["win_trade_pct"] = round(100 * float(np.mean([t["R"] > 0 for t in trades])), 1)
    s["trades_per_traded_day"] = {int(k): int(v) for k, v in tab[tab["n"] > 0]["n"].value_counts().sort_index().items()}
    s["worst_day_R"] = round(float(tab["dbal"].min()), 2)
    s["worst_intraday_low_R"] = round(float(tab["dmin"].min()), 2)
    eq = tab["dbal"].cumsum()
    s["max_drawdown_R"] = round(float((eq - np.maximum.accumulate(np.r_[0.0, eq.to_numpy()])[1:]).min()), 1)
    s["usable_days"] = int(len(tab))
    return s


def selftest():
    o = np.array([100.0, 100.5, 101.0, 99.0]); h = np.array([100.6, 101.2, 103.2, 99.5])
    l = np.array([99.8, 100.2, 100.8, 98.0]); c = np.array([100.5, 101.0, 103.0, 98.5])
    assert walk(o, h, l, c, 0, 99.0, 103.0) == (2, 103.0, "target", False)          # target reached in bar 2, fill at the target
    assert walk(o, h, l, c, 0, 99.9, 103.0) == (0, 99.9, "stop", False)             # stop touched in the entry bar
    assert walk(o, h, l, c, 3, 99.2, 104.0) == (3, 99.0, "stop", False)             # bar opens below the stop: fill at its open
    assert walk(o, h, l, c, 0, 90.0, 110.0) == (3, 98.5, "close", False)            # neither: out at the last close
    assert walk(o, h, l, c, 2, 100.9, 103.1) == (2, 100.9, "stop", True)            # both touched: counted as a stop
    # a whole hand-built day: gap up, range 100-101, a 9:45 bar closing at 102, entry 102, stop 100, target 105
    mins = np.arange(540, 960)
    n = len(mins)
    oo = np.full(n, 100.5); hi = np.full(n, 100.6); lo = np.full(n, 100.4); cc = np.full(n, 100.5)
    r = slice(30, 45); hi[r] = 101.0; lo[r] = 100.0
    s5 = slice(45, 50); oo[s5] = 101.5; hi[s5] = 102.1; lo[s5] = 101.4; cc[s5] = 102.0
    after = slice(50, n); oo[after] = 102.0; hi[after] = 102.2; lo[after] = 101.8; cc[after] = 102.0
    hi[60] = 105.5                                                                   # target (105) hit at 10:00
    tr, low = trade_day(mins, oo, hi, lo, cc, 100.0, 99.0, ("points", 0.5), True, cost=0.0)
    assert len(tr) >= 1 and tr[0]["kind"] == "target" and abs(tr[0]["R"] - 1.5) < 1e-9 and tr[0]["entry_min"] == 590
    assert tr[1]["entry_min"] >= 605                                                 # the next signal bar closes after the exit
    tr2, _ = trade_day(mins, oo, hi, lo, cc, 100.2, 99.0, ("points", 0.5), True, cost=0.0)
    assert tr2 == []                                                                 # gap of 0.3 points: no trades
    tr3, _ = trade_day(mins, oo, hi, lo, cc, 100.0, 200.0, ("points", 0.5), True, cost=0.0)
    assert tr3 == []                                                                 # price below the moving average: no trades
    lo2 = lo.copy(); lo2[55] = 99.9                                                  # stop (100) hit at 9:55 before the target
    tr4, low4 = trade_day(mins, oo, hi, lo2, cc, 100.0, 99.0, ("points", 0.5), True, cost=0.0)
    assert tr4[0]["kind"] == "stop" and abs(tr4[0]["R"] + 1.0) < 1e-9 and low4 <= -1.0
    print("selftest OK")


def main():
    mode = sys.argv[1]
    if mode == "selftest":
        return selftest()
    if mode == "dryrun":
        m, hh = load(None, "NAS100", fake_seed=14)
        tab, trades = run_market(m, hh, GAP["NAS100"])
        s = describe(tab, trades)
        print(json.dumps({k: s[k] for k in ("traded_days", "trades", "avg_R_per_day", "avg_R_per_trade", "profit_factor", "t_stat", "exits_pct")}, indent=1))
        return
    lab, out_path = sys.argv[2], sys.argv[3]
    sys.path.insert(0, lab)
    import costs
    assert all(costs.COST[k] == COST and costs.STOP_SLIP[k] == COST for k in GAP), "cost table changed"
    out = {"settings": {"cost_per_side": COST, "target_R": TARGET_R, "min_dist": MIN_DIST, "risks_pct": RISKS}}
    m, hh = load(lab, "NAS100")
    tab, trades = run_market(m, hh, GAP["NAS100"])
    s = describe(tab, trades)
    tab2, _ = run_market(m, hh, GAP["NAS100"], cost=2 * COST)
    s["avg_R_per_day_double_cost"] = stats(tab2)["avg_R_per_day"]
    s["test1"] = "PASS" if (s["traded_days"] >= NEED_DAYS and s["avg_R_per_day"] > 0 and s["t_stat"] >= NEED_T and (s["profit_factor"] or 0) >= NEED_PF
                            and s["avg_R_per_day_double_cost"] > 0 and s["years_positive"] >= NEED_YEARS) else "FAIL"
    s["periods"] = {"2021-2024": stats(tab[tab["day"] < "2025-01-01"]), "2025-2026": stats(tab[tab["day"] >= "2025-01-01"])}
    cells = {}
    for firm, S in FIRMS.items():
        cells[firm] = {}
        for risk in RISKS:
            r = challenge(tab, S, risk)
            breach = r["breach_daily_pct"] + r["breach_max_pct"]
            r["fits"] = bool(r["passed_pct"] >= 50 and breach <= 10 and r["median_days_to_pass"] is not None and r["median_days_to_pass"] <= 250)
            cells[firm][str(risk)] = r
    s["challenge"] = cells
    out["NAS100"] = s
    tabn, trn = run_market(m, hh, GAP["NAS100"], use_filters=False)
    out["NAS100_no_filters"] = describe(tabn, trn)
    for mk in ("SPX500", "USA30"):
        mm, h2 = load(lab, mk)
        t2, tr2 = run_market(mm, h2, GAP[mk])
        out[mk] = describe(t2, tr2)
    tab.assign(day=tab["day"].dt.strftime("%Y-%m-%d")).to_csv(out_path.replace(".json", "_days.csv"), index=False)
    pd.DataFrame(trades).assign(day=lambda d: d["day"].dt.strftime("%Y-%m-%d")).to_csv(out_path.replace(".json", "_trades.csv"), index=False)
    json.dump(out, open(out_path, "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
