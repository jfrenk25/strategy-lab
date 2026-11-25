"""Study 17: RTH open ATR breakout. Rules: claude/rth-breakout-rules-2026-11-25.md (written before this ran).

Usage: python -I rth_breakout.py MODE [LAB_DIR] [OUT_JSON]
  MODE  selftest  hand-built bars (no data read)
        dryrun    the same code on made-up prices with no edge
        run       the study (once)
Needs gapline_orb.py (Study 14) in the same folder for the data loader and the challenge replay.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # this script's own folder (needed under python -I)

import numpy as np
import pandas as pd

import gapline_orb as g14

COST = g14.COST
ENTRY_ATR, STOP_ATR, FILTER_MULT, ATR_DAYS = 0.2, 0.25, 1.2, 5
CHECKS = tuple(range(600, 931, 30))                      # 10:00 ... 15:30
NEED_T, NEED_DAYS, NEED_PF, NEED_YEARS = 2.58, 150, 1.15, 4
RISKS = (0.25, 0.5, 0.75, 1.0, 1.5)


def trade_day(mins, o, h, l, c, atr, cap, cost=COST):
    """One day. Returns (trades, lowest point of the day in R), or None if the day cannot be traded."""
    pos = {int(m): k for k, m in enumerate(mins)}
    if 570 not in pos or 959 not in pos:
        return None
    last = pos[959]
    ref = float(o[pos[570]])
    up, dn, dist = ref + ENTRY_ATR * atr, ref - ENTRY_ATR * atr, STOP_ATR * atr
    trades, realized, low_point, free_from, stops = [], 0.0, 0.0, 0, 0
    for cm in CHECKS:
        if cm < free_from or (cap is not None and stops >= cap):
            continue
        if cm - 1 not in pos or cm not in pos:
            continue
        px0 = float(c[pos[cm - 1]])
        side = 1 if px0 > up else (-1 if px0 < dn else 0)
        if side == 0:
            continue
        i = pos[cm]
        entry = float(o[i])
        stop = entry - side * dist
        j, px, kind = last, float(c[last]), "close"
        for q in range(i, last + 1):
            if side == 1 and l[q] <= stop:
                j, px, kind = q, float(min(o[q], stop)), "stop"; break
            if side == -1 and h[q] >= stop:
                j, px, kind = q, float(max(o[q], stop)), "stop"; break
        denom = dist / entry
        costs = 2 * cost + (cost if kind == "stop" else 0.0)
        R = (side * (px / entry - 1) - costs) / denom
        worst = (float(np.min(l[i:j + 1])) if side == 1 else float(np.max(h[i:j + 1]))) if kind != "stop" else px
        low_point = min(low_point, realized + min((side * (worst / entry - 1) - cost) / denom, R))
        realized += R
        low_point = min(low_point, realized)
        trades.append({"R": R, "kind": kind, "side": side, "entry_min": int(mins[i]), "exit_min": int(mins[j])})
        if kind == "close":
            break
        stops += 1
        free_from = int(mins[j]) + 1                     # the next check must come after the exit minute
    return trades, low_point


def daily_series(m):
    """One row per full session (9:30 to 15:59 both present): range and five-day ATR through that day."""
    mm = m["ts"].dt.hour * 60 + m["ts"].dt.minute
    r = m[(mm >= 570) & (mm <= 959)]
    rm = mm[r.index]
    grp = r.groupby(r["ts"].dt.normalize())
    d = grp.agg(h=("high", "max"), l=("low", "min"), c=("close", "last"))
    d["full"] = grp.apply(lambda x: bool(((x["ts"].dt.hour * 60 + x["ts"].dt.minute) == 570).any() and ((x["ts"].dt.hour * 60 + x["ts"].dt.minute) == 959).any()))
    d = d[d["full"]]
    pc = d["c"].shift()
    tr = np.maximum(d["h"], pc.fillna(d["h"])) - np.minimum(d["l"], pc.fillna(d["l"]))
    d["atr"] = tr.rolling(ATR_DAYS).mean()
    d["range"] = d["h"] - d["l"]
    return d


def run_market(m, cap, use_filter=True, cost=COST):
    d = daily_series(m)
    prev_atr, prev_range = d["atr"].shift(), d["range"].shift()
    m = m[m["ts"].dt.hour * 60 + m["ts"].dt.minute >= 570]
    rows, trades = [], []
    for day, g in m.groupby(m["ts"].dt.normalize(), sort=True):
        if day not in d.index or np.isnan(prev_atr.get(day, np.nan)):
            continue
        a, rg = float(prev_atr[day]), float(prev_range[day])
        if use_filter and not (rg < FILTER_MULT * a):
            rows.append({"day": day, "dbal": 0.0, "dmin": 0.0, "n": 0})
            continue
        mins = (g["ts"].dt.hour * 60 + g["ts"].dt.minute).to_numpy()
        res = trade_day(mins, *(g[k].to_numpy(float) for k in ("open", "high", "low", "close")), a, cap, cost)
        if res is None:
            continue
        tr, low = res
        for t in tr:
            t["day"] = day
        trades += tr
        rows.append({"day": day, "dbal": sum(t["R"] for t in tr), "dmin": low, "n": len(tr)})
    tab = pd.DataFrame(rows)
    tab["a"] = 0.0; tab["flat0"] = True; tab["flat1"] = True
    return tab, pd.DataFrame(trades)


def describe(tab, tr):
    s = g14.stats(tab)
    yr = tab.groupby(tab["day"].dt.year)["dbal"].sum()
    s["by_year_sum_R"] = {int(y): round(float(v), 1) for y, v in yr.items()}
    s["years_positive"] = int((yr > 0).sum())
    s["exits_pct"] = {k: round(100 * float(v), 1) for k, v in tr["kind"].value_counts(normalize=True).items()}
    s["win_trade_pct"] = round(100 * float((tr["R"] > 0).mean()), 1)
    s["avg_R_per_trade"] = round(float(tr["R"].mean()), 4)
    s["buys"] = {"trades": int((tr["side"] == 1).sum()), "sum_R": round(float(tr[tr["side"] == 1]["R"].sum()), 1)}
    s["sells"] = {"trades": int((tr["side"] == -1).sum()), "sum_R": round(float(tr[tr["side"] == -1]["R"].sum()), 1)}
    s["trades_per_traded_day"] = {int(k): int(v) for k, v in tab[tab["n"] > 0]["n"].value_counts().sort_index().items()}
    s["worst_day_R"] = round(float(tab["dbal"].min()), 2)
    eq = tab["dbal"].cumsum()
    s["max_drawdown_R"] = round(float((eq - np.maximum.accumulate(np.r_[0.0, eq.to_numpy()])[1:]).min()), 1)
    s["usable_days"] = int(len(tab))
    s["periods"] = {"2021-2023": g14.stats(tab[tab["day"] < "2024-01-01"]), "2024-2026": g14.stats(tab[tab["day"] >= "2024-01-01"])}
    return s


def selftest():
    mins = np.arange(570, 960)
    n = len(mins)
    base = lambda v: (np.full(n, v), np.full(n, v + 0.05), np.full(n, v - 0.05), np.full(n, v))
    at = lambda m: m - 570
    # ATR 10: buy above 102, sell below 98, stop 2.5 away. Reference open 100.
    o, h, l, c = base(100.0)
    for a in (o, h, l, c):
        a[at(599):] += 3.0                                                           # 103 from 9:59: buy at the 10:00 open
    l[at(620)] = 100.0                                                               # 10:20 trades down through the stop (100.5)
    for a in (o, h, l, c):
        a[at(621):] -= 6.0                                                           # 97 from 10:21: sell at the 10:30 check
    h[at(700)] = 100.0                                                               # 11:40 trades up through the sell stop (99.5)
    tr, low = trade_day(mins, o, h, l, c, 10.0, None, cost=0.0)
    assert [t["side"] for t in tr[:2]] == [1, -1] and tr[0]["entry_min"] == 600 and tr[1]["entry_min"] == 630
    assert abs(tr[0]["R"] + 1.0) < 1e-9 and abs(tr[1]["R"] + 1.0) < 1e-9 and tr[0]["kind"] == "stop"
    assert len(tr) == 3 and tr[2]["entry_min"] == 720 and tr[2]["side"] == -1 and tr[2]["kind"] == "close" and abs(tr[2]["R"]) < 1e-9   # re-entry at 12:00
    assert low <= -2.0 + 1e-9
    tr2, _ = trade_day(mins, o, h, l, c, 10.0, 2, cost=0.0)
    assert len(tr2) == 2                                                             # the cap blocks the third entry
    o3, h3, l3, c3 = (a.copy() for a in (o, h, l, c))
    o3[at(620)] = 99.0; l3[at(620)] = 98.9                                           # 10:20 opens below the stop: fill at the open
    tr3, _ = trade_day(mins, o3, h3, l3, c3, 10.0, None, cost=0.0)
    assert abs(tr3[0]["R"] - (99.0 / 103.0 - 1) / (2.5 / 103.0)) < 1e-9
    q, hq, lq, cq = base(100.0)
    tr4, _ = trade_day(mins, q, hq, lq, cq, 10.0, None, cost=0.0)
    assert tr4 == []                                                                 # price never leaves the band: no trades
    # the filter: yesterday's range must be under 1.2 times the ATR
    days = pd.bdate_range("2026-01-05", periods=8)
    ts = days.repeat(n) + pd.to_timedelta(np.tile(mins, len(days)), unit="m")
    m = pd.DataFrame({"ts": ts, "open": 100.0, "high": 100.5, "low": 99.5, "close": 100.0})
    wide = m["ts"].dt.normalize() == days[6]
    m.loc[wide, "high"] = 110.0                                                      # day 6 has a wide range
    tab, _ = run_market(m, None)
    assert list(tab["day"]) == list(days[5:]) and len(tab) == 3                      # five full days are needed first
    d = daily_series(m)
    assert d["range"].iloc[6] > FILTER_MULT * d["atr"].iloc[6]                       # so day 7 is blocked by the filter
    print("selftest OK")


def main():
    mode = sys.argv[1]
    if mode == "selftest":
        return selftest()
    if mode == "dryrun":
        m, _ = g14.load(None, "NAS100", fake_seed=17)
        for cap in (None, 2):
            tab, tr = run_market(m, cap)
            s = describe(tab, tr)
            print(cap, json.dumps({k: s[k] for k in ("traded_days", "trades", "avg_R_per_day", "avg_R_per_trade", "profit_factor", "t_stat", "exits_pct")}))
        return
    lab, out_path = sys.argv[2], sys.argv[3]
    sys.path.insert(0, lab)
    import costs
    assert all(costs.COST[k] == COST and costs.STOP_SLIP[k] == COST for k in ("NAS100", "SPX500", "USA30")), "cost table changed"
    out = {"settings": {"entry_atr": ENTRY_ATR, "stop_atr": STOP_ATR, "filter": FILTER_MULT, "atr_days": ATR_DAYS, "cost_per_side": COST}}
    m, _ = g14.load(lab, "NAS100")
    for name, cap in (("A_as_posted", None), ("B_daily_cap", 2)):
        tab, tr = run_market(m, cap)
        s = describe(tab, tr)
        tab2, _ = run_market(m, cap, cost=2 * COST)
        s["avg_R_per_day_double_cost"] = g14.stats(tab2)["avg_R_per_day"]
        s["test1"] = "PASS" if (s["traded_days"] >= NEED_DAYS and s["avg_R_per_day"] > 0 and s["t_stat"] >= NEED_T and (s["profit_factor"] or 0) >= NEED_PF
                                and s["avg_R_per_day_double_cost"] > 0 and s["years_positive"] >= NEED_YEARS) else "FAIL"
        cells = {}
        for firm, S in g14.FIRMS.items():
            cells[firm] = {}
            for risk in RISKS:
                r = g14.challenge(tab, S, risk)
                r["fits"] = bool(r["passed_pct"] >= 50 and r["breach_daily_pct"] + r["breach_max_pct"] <= 10
                                 and r["median_days_to_pass"] is not None and r["median_days_to_pass"] <= 250)
                cells[firm][str(risk)] = r
        s["challenge"] = cells
        out[name] = s
        tr.assign(day=tr["day"].dt.strftime("%Y-%m-%d")).to_csv(out_path.replace(".json", f"_{name}_trades.csv"), index=False)
        tab.assign(day=tab["day"].dt.strftime("%Y-%m-%d")).to_csv(out_path.replace(".json", f"_{name}_days.csv"), index=False)
    tab, tr = run_market(m, None, use_filter=False)
    out["A_no_filter"] = describe(tab, tr)
    for mk in ("SPX500", "USA30"):
        mm, _ = g14.load(lab, mk)
        for name, cap in (("A", None), ("B", 2)):
            tab, tr = run_market(mm, cap)
            out[f"{mk}_{name}"] = describe(tab, tr)
    json.dump(out, open(out_path, "w"), indent=1)
    print("done")


if __name__ == "__main__":
    main()
