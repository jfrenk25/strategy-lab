"""Forward watch for the three-leg book: Cutler RSI dip-buy and RTH open ATR breakout on NAS100, copy v3 on gold.
The registration, with sizes and the verdict rules, is lab/book/REGISTRATION.md. It was written before any forward bar existed.

Run from the repo root:
    python lab/book/forward_book.py            # update lab/book/status.json from the price data in lab/
    python lab/book/forward_book.py selftest   # hand-built checks, no data read

Only trades entered at or after START count. Sizes never change. Nothing here places trades.
Testing only: --start YYYY-MM-DD --end YYYY-MM-DD --gold DIR --out FILE replay an older stretch and never touch status.json.
"""
import argparse
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import numpy as np
import pandas as pd
from dateutil.easter import easter

import book2_members as b2
import book_members as bm

REGISTERED = "2026-11-25"
START = "2026-11-26"                                   # 00:00 UTC; trades entered before this never count
SIZES = {                                              # frozen: the PASSED3 book at the 6% size (Study 20)
    "cutler_dip_buy": 0.3754,                          # position worth this many times the starting balance
    "copy_v3_gold": 0.2514,                            # % of the starting balance risked per position (three positions a signal)
    "rth_breakout_A": 0.1457,                          # % of the starting balance risked per trade
}
CAP = 500
FIRMS = {
    "FTMO 1-Step": dict(target=10.0, daily=3.0, ref="balance", maxloss=10.0, trailing=True, need=0, best=0.5),
    "The5ers 1-step": dict(target=10.0, daily=3.0, ref="higher", maxloss=6.0, trailing=False, need=3, best=None),
}
HOUR = pd.Timedelta(hours=1)


def nyse_holidays(y):
    """Full-day New York Stock Exchange closures by rule. Checked against the calendar Study 12 used: same days, 2021 to November 2026."""
    def obs(d):
        d = pd.Timestamp(d)
        return d - pd.Timedelta(days=1) if d.weekday() == 5 else (d + pd.Timedelta(days=1) if d.weekday() == 6 else d)

    def nth(m, wd, k):
        d = pd.Timestamp(y, m, 1)
        return d + pd.Timedelta(days=(wd - d.weekday()) % 7) + pd.Timedelta(weeks=k - 1)

    last_mon_may = pd.Timestamp(y, 5, 31) - pd.Timedelta(days=pd.Timestamp(y, 5, 31).weekday())
    h = [nth(1, 0, 3), nth(2, 0, 3), pd.Timestamp(easter(y)) - pd.Timedelta(days=2), last_mon_may, obs(f"{y}-07-04"),
         nth(9, 0, 1), nth(11, 3, 4), obs(f"{y}-12-25")]
    ny = pd.Timestamp(y, 1, 1)
    if ny.weekday() != 5:                              # a Saturday New Year's Day is not observed
        h.append(ny + pd.Timedelta(days=1) if ny.weekday() == 6 else ny)
    if y >= 2022:
        h.append(obs(f"{y}-06-19"))
    return {pd.Timestamp(x).normalize() for x in h}


def exchange_days(last_year):
    hol = set().union(*[nyse_holidays(y) for y in range(2021, last_year + 2)])
    return [d for d in pd.bdate_range("2021-01-01", f"{last_year + 1}-12-31") if d not in hol]


def set_grid(t0, t1):
    """Point both member modules at the forward grid. A trade entered before t0 falls off the grid and is dropped by the marking."""
    for m in (bm, b2):
        m.T0, m.T1, m.NG = t0, t1, int((t1 - t0) / HOUR)
    bm.DAYS, bm.DAY_FIRST, bm.DAY_END = bm.firm_days()
    b2.DAY_END = bm.DAY_END


def paper(E, R, L, S):
    """One paper challenge from a flat start. E, R, L: account value at each day's end, closed profit to date, lowest value in the day (% of start)."""
    bal_mid = eq_mid = hwm = 0.0
    best, pdays = -1e18, 0
    for k in range(min(len(E), CAP)):
        hwm = max(hwm, bal_mid)
        ref = bal_mid if S["ref"] == "balance" else max(bal_mid, eq_mid)
        if L[k] <= ref - S["daily"] + 1e-9:
            return "PAPER FAIL: daily loss limit", k + 1
        if L[k] <= (hwm - S["maxloss"] if S["trailing"] else -S["maxloss"]) + 1e-9:
            return "PAPER FAIL: max loss", k + 1
        d = R[k] - bal_mid
        best = max(best, d)
        pdays += d >= 0.5 - 1e-9
        good = E[k] >= S["target"] - 1e-9 and pdays >= S["need"]
        if S["best"] is not None:
            good = good and best <= S["best"] * E[k] + 1e-9
        if good:
            return "PAPER PASS", k + 1
        bal_mid, eq_mid = R[k], E[k]
    return ("TOO SLOW" if len(E) >= CAP else "WATCHING"), int(min(len(E), CAP))


def last_time(path, unit):
    t = pd.read_csv(path, usecols=["time"])["time"]
    return pd.to_datetime(t.iloc[-1], unit="s", utc=True) if unit == "s" else pd.to_datetime(t.iloc[-1], utc=True)


def build(start, end, gold_dir):
    """Returns the status dict. end=None means: as far as every leg has data."""
    nas_1m = os.path.join(LAB, "data_1m", "NAS100_1m_full.csv.gz")
    nas_1h = os.path.join(LAB, "data_new", "NAS100_1h.csv.gz")
    gold_files = sorted(glob.glob(os.path.join(gold_dir, "*XAUUSD_1m_*.csv.gz")))
    ends = {"NAS100 minute bars": last_time(nas_1m, "s"), "NAS100 hourly bars": last_time(nas_1h, "iso")}
    if gold_files:
        ends["Gold minute bars"] = last_time(gold_files[-1], "s")
    out = {"registered": REGISTERED, "start": str(start.date()), "sizes": SIZES,
           "data_ends": {k: str(v) for k, v in ends.items()}}
    if not gold_files:
        out["state"] = "WAITING: no gold minute files in lab/data_1m (XAUUSD_1m_<year>.csv.gz)"
        return out, None
    t1 = min(ends.values()).floor("h") + HOUR
    if end is not None:
        t1 = min(t1, end)
    out["counted_to"] = str(t1)
    if t1 <= start + HOUR:
        out["state"] = "WATCHING: no price bars after the start date yet"
        out["firm_days"] = 0
        return out, None
    set_grid(start, t1)
    legs = {}
    # leg 1: Cutler RSI dip-buy, exactly as Study 12 rule D (book member 1)
    days = exchange_days(t1.year)
    nas = bm.lab_daily(nas_1m, days)
    nas = nas[nas["date"] < t1.tz_localize(None).normalize() + pd.Timedelta(days=1)]
    nd, no, nc = list(nas["date"]), nas["open"].to_numpy(float), nas["close"].to_numpy(float)
    A, _ = bm.qs_member(bm.run_D(nc, no), nd, 1, bm.bars(LAB, "NAS100"))
    legs["cutler_dip_buy"] = A
    # leg 2: copy v3 on gold (book member 10)
    years = sorted(int(re.search(r"XAUUSD_1m_(\d{4})", f).group(1)) for f in gold_files)
    d = b2.load_gold(gold_dir, years)
    d = d[d.time < int(t1.timestamp())].reset_index(drop=True)
    A = bm.Arr()
    b2.copy_v3_member(d, b2.copy_v3_positions(d), A)
    legs["copy_v3_gold"] = A
    # leg 3: RTH open ATR breakout, version A (book member 11)
    A = bm.Arr()
    b2.rth(LAB, A)
    legs["rth_breakout_A"] = A

    end_i, first_i = bm.DAY_END, bm.DAY_FIRST
    E = np.zeros(len(end_i)); R = np.zeros(len(end_i)); Lh = np.zeros(bm.NG)
    out["legs"] = {}
    for name, A in legs.items():
        w = SIZES[name]
        r = np.cumsum(A.real)
        E += w * (r + A.fc)[end_i]
        R += w * r[end_i]
        Lh += w * (np.r_[0.0, r[:-1]] + A.lo)
        day_change = np.diff(np.r_[0.0, (r + A.fc)[end_i]]) * w
        out["legs"][name] = {"closed_trades": int(A.n), "closed_profit_pct": round(float(w * A.real.sum()), 3),
                             "worst_day_pct": round(float(day_change.min()), 3)}
    L = np.minimum.reduceat(Lh, first_i)
    mid = np.r_[0.0, R[:-1]]
    out["firm_days"] = int(len(E))
    out["book"] = {"account_change_pct": round(float(E[-1]), 3), "closed_profit_pct": round(float(R[-1]), 3),
                   "worst_day_pct": round(float(np.diff(np.r_[0.0, E]).min()), 3),
                   "furthest_under_midnight_balance_pct": round(float((L - mid).min()), 3),
                   "deepest_drawdown_pct": round(float((E - np.maximum.accumulate(np.r_[0.0, E])[1:]).min()), 3)}
    out["paper_challenge"] = {}
    for firm, S in FIRMS.items():
        state, day = paper(E, R, L, S)
        out["paper_challenge"][firm] = {"state": state, "on_firm_day": day}
    out["state"] = "; ".join(f"{f}: {v['state']}" for f, v in out["paper_challenge"].items())
    return out, (E, R, L, bm.DAYS)


def selftest():
    flat = np.zeros(30)
    up = np.cumsum(np.full(30, 0.6))
    assert paper(up, up, np.r_[0.0, up[:-1]], FIRMS["The5ers 1-step"]) == ("PAPER PASS", 17)      # +0.6% a day reaches 10% on day 17
    assert paper(up, up, np.r_[0.0, up[:-1]], FIRMS["FTMO 1-Step"]) == ("PAPER PASS", 17)
    L = flat.copy(); L[4] = -3.0
    assert paper(flat, flat, L, FIRMS["FTMO 1-Step"]) == ("PAPER FAIL: daily loss limit", 5)
    dn = np.cumsum(np.full(30, -0.7))
    assert paper(dn, dn, dn, FIRMS["The5ers 1-step"]) == ("PAPER FAIL: max loss", 9)             # -0.7% a day is 6% down inside day 9
    assert paper(dn, dn, dn, FIRMS["FTMO 1-Step"]) == ("PAPER FAIL: max loss", 15)               # 10% down inside day 15
    one = np.r_[np.zeros(5), np.full(25, 10.5)]                                                   # the whole gain in one day
    assert paper(one, one, np.r_[0.0, one[:-1]], FIRMS["FTMO 1-Step"])[0] == "WATCHING"           # best day over half the profit: not a pass
    assert paper(flat, flat, flat, FIRMS["FTMO 1-Step"]) == ("WATCHING", 30)
    floaty = np.r_[np.zeros(5), np.full(25, 10.5)]
    assert paper(floaty, flat, np.r_[0.0, floaty[:-1]], FIRMS["The5ers 1-step"])[0] == "WATCHING" # open profit only: no three profitable days
    assert pd.Timestamp("2027-03-26") in nyse_holidays(2027) and pd.Timestamp("2026-11-26") in nyse_holidays(2026)
    assert pd.Timestamp("2021-12-31") not in nyse_holidays(2022) and pd.Timestamp("2027-01-01") in nyse_holidays(2027)
    assert pd.Timestamp("2026-07-03") in nyse_holidays(2026)                                      # July 4, 2026 is a Saturday
    print("selftest OK")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        return selftest()
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end"); ap.add_argument("--gold"); ap.add_argument("--out")
    a = ap.parse_args()
    test = bool(a.start or a.end or a.gold or a.out)
    start = pd.Timestamp(a.start or START, tz="UTC")
    end = pd.Timestamp(a.end, tz="UTC") if a.end else None
    out, _ = build(start, end, a.gold or os.path.join(LAB, "data_1m"))
    out["updated"] = pd.Timestamp.now(tz="UTC").strftime("%Y-%m-%d")
    if test:
        out["test_only"] = True
    path = a.out if test else os.path.join(HERE, "status.json")
    if path:
        json.dump(out, open(path, "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
