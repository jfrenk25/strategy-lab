"""Study 7: the "7H Profile · Fractal Model" script on 1-hour bars, fifteen markets. One run.

Run from the repo root:
    python lab/intraday/fractal7h.py --dryrun    # same code on made-up prices with no cost; nothing is written
    python lab/intraday/fractal7h.py             # the one real run; refuses to run a second time

The rules are in LAB_RULES.md under "Study 7". They were written and pushed before this file existed.
Source of the rule: an anonymous Pine Script paste, pastebin.com/9AMMivPh, default settings. The logic below is
written from that script's rules in the lab's own code, in the script's own order of steps. Drawing code is left out.
"""
import sys, os, json, datetime
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.join(HERE, "..")
sys.path.insert(0, LAB)
RESULTS = os.path.join(HERE, "fractal7h_results.json")
FEES = {"BTCUSD": 0.0003, "ETHUSD": 0.0004, "XAUUSD": 0.0002, "GBPJPY": 0.00015, "USA30": 0.00025, "DEU30": 0.00025,
        "NAS100": 0.00025, "SPX500": 0.00025, "USOIL": 0.0003, "EURUSD": 0.00015, "GBPUSD": 0.00015,
        "USDJPY": 0.00015, "AUDUSD": 0.00015, "USDCAD": 0.00015, "EURJPY": 0.00015}          # per side, as in lab.py
NEW = {"NAS100", "SPX500", "USOIL", "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "EURJPY"}  # files in lab/data_new
GROUP = {"BTCUSD": "crypto", "ETHUSD": "crypto", "XAUUSD": "gold and oil", "USOIL": "gold and oil",
         "USA30": "indices", "DEU30": "indices", "NAS100": "indices", "SPX500": "indices"}
SLIP = 0.0002                                               # on stop exits, as in lab.py
DATA_FROM = pd.Timestamp("2021-04-21", tz="UTC")
DATA_TO = pd.Timestamp("2026-04-21", tz="UTC")              # from here on: the lab's quarantine, not touched
START, END = datetime.date(2021, 6, 1), datetime.date(2026, 4, 20)
PASS = dict(days=150, t=2.58, pf=1.15, markets_ok=8, years=(2021, 2022, 2023, 2024, 2025, 2026), years_ok=4)
P = dict(day_start=18, prof_hours=7, atr_len=14, wick_max=40.0, sep_mult=0.5, fail_pct=50.0, piv_len=3, cisd_max=20,
         end_hour=12, max_entries=1, cool=4, rr=2.0, exit_hour=15)
PROFILE = {1: "asia", 2: "london", 3: "new york"}


class Candle:
    __slots__ = ("o", "h", "l", "c", "tE", "tH", "tL", "blk")

    def __init__(self, o, h, l, c, t, blk):
        self.o, self.h, self.l, self.c, self.tE, self.tH, self.tL, self.blk = o, h, l, c, t, t, t, blk

    def grow(self, h, l, c, t):
        if h > self.h: self.h, self.tH = h, t
        if l < self.l: self.l, self.tL = l, t
        self.c, self.tE = c, t


class Swing:
    __slots__ = ("p", "t")

    def __init__(self):
        self.p, self.t = None, None


# ---------------------------------------------------------------- data

def fake_hours(seed):
    """Made-up 24-hour hourly prices, Sunday 18:00 to Friday 17:00 New York time, with the daily 17:00 break."""
    rng = np.random.default_rng(seed)
    t = pd.date_range("2021-04-20 22:00", "2026-04-20 21:00", freq="h", tz="UTC")
    ny = t.tz_convert("America/New_York"); wd, hr = ny.dayofweek.to_numpy(), ny.hour.to_numpy()
    t = t[~((wd == 5) | ((wd == 6) & (hr < 18)) | ((wd == 4) & (hr >= 17)) | (hr == 17))]; n = len(t)
    steps = rng.normal(0, 0.0005, (n, 12)).cumsum(axis=1)
    base = np.r_[0.0, steps[:-1, -1].cumsum()]
    path = 100 * np.exp(base[:, None] + steps); o = np.r_[100.0, path[:-1, -1]]
    return pd.DataFrame({"time": t, "open": o, "high": np.maximum(o, path.max(axis=1)), "low": np.minimum(o, path.min(axis=1)), "close": path[:, -1]})


def load(m, fake_seed=None):
    if fake_seed is not None:
        return fake_hours(fake_seed)
    df = pd.read_csv(os.path.join(LAB, "data_new" if m in NEW else "data", f"{m}_1h.csv.gz"))
    df["time"] = pd.to_datetime(df["time"], utc=True)
    return df[(df["time"] >= DATA_FROM) & (df["time"] < DATA_TO)].sort_values("time").reset_index(drop=True)


# ---------------------------------------------------------------- the rule

def simulate(df):
    """Returns the trades of one market: entry at the open of the bar after the trigger, stops and targets as the script sets them."""
    ny = df["time"].dt.tz_convert("America/New_York")
    hour = ny.dt.hour.to_numpy(); minute = ny.dt.minute.to_numpy(); date = ny.dt.date.to_numpy()
    tms = (df["time"].astype("int64") // 10**6).to_numpy()            # bar open time, milliseconds
    o, h, l, c = (df[x].to_numpy(dtype=float) for x in ("open", "high", "low", "close"))
    n = len(o); blk_len = P["prof_hours"] * 60
    rel = (hour * 60 + minute - P["day_start"] * 60 + 1440) % 1440
    blk = rel // blk_len
    exit_rel = (P["exit_hour"] * 60 - P["day_start"] * 60 + 1440) % 1440

    dH = []; pH = []; d_cur = None; p_cur = None
    sL, sH = Swing(), Swing()
    bias = today_bias = 0; cont_lvl = None; cont_invalid = False
    p_state = p_type = p_dir = 0; p_rev = None; p_ext = p_inv = None; day_lo = day_hi = None; ent_count = 0
    refL = refLB = refH = refHB = None
    dnO = upO = None
    swL = swLB = cLvlB = None; usedLB = -1
    swH = swHB = cLvlS = None; usedHB = -1
    act = None; last_ent = -1000
    trades = []; counts = dict(days=0, bias_days=0, skipped_wick=0, cont_invalid=0, profiles={1: 0, 2: 0, 3: 0}, profile_invalid=0, triggers=0)

    def leg_x(is_low, a, b, t_min):
        r = None
        for j in range(a, b + 1):
            cj = dH[j]
            if cj.tE >= t_min:
                v = cj.h if is_low else cj.l
                r = v if r is None else (max(r, v) if is_low else min(r, v))
        return r

    def pivot(sw, is_low, pc, k, atr_u):
        p = pc.l if is_low else pc.h; t = pc.tL if is_low else pc.tH
        if sw.p is None or (p < sw.p if is_low else p > sw.p):
            sw.p, sw.t = p, t
        elif p != sw.p:
            leg = leg_x(is_low, 0, k, sw.t)
            rng = None if leg is None else (leg - sw.p if is_low else sw.p - leg)
            sep = p - sw.p if is_low else sw.p - p
            retr = 100.0 if (rng is None or rng <= 0) else ((leg - p) if is_low else (p - leg)) / rng * 100
            if sep >= P["sep_mult"] * atr_u and retr <= P["fail_pct"]:
                sw.p, sw.t = p, t

    for i in range(n):
        gap = i > 0 and tms[i] - tms[i - 1] >= blk_len * 60000
        new_blk = i == 0 or blk[i] != blk[i - 1] or gap
        new_day = new_blk and (i == 0 or blk[i] <= blk[i - 1])
        bull_c = c[i] > o[i]; bear_c = c[i] < o[i]

        # the daily candle, built from the bars
        day_closed = False
        if new_day:
            if d_cur is not None:
                dH.append(d_cur)
                if len(dH) > 150: dH.pop(0)
                day_closed = True
            d_cur = Candle(o[i], h[i], l[i], c[i], tms[i], -1)
        elif d_cur is not None:
            d_cur.grow(h[i], l[i], c[i], tms[i])

        if day_closed:                                         # daily direction
            dc = dH[-1]; sz = len(dH)
            m = min(P["atr_len"], sz - 1); atr_u = dc.h - dc.l
            if m >= 1:
                s = 0.0
                for q in range(m):
                    a, b = dH[sz - 1 - q], dH[sz - 2 - q]
                    s += max(a.h - a.l, abs(a.h - b.c), abs(a.l - b.c))
                atr_u = s / m
            if sz >= 3:
                k = sz - 2; pc, lc, rc = dH[k], dH[k - 1], dH[k + 1]
                if not (lc.l <= pc.l or rc.l < pc.l): pivot(sL, True, pc, k, atr_u)
                if not (lc.h >= pc.h or rc.h > pc.h): pivot(sH, False, pc, k, atr_u)
            bull_r = sL.p is not None and dc.l < sL.p and dc.c > sL.p
            bear_r = sH.p is not None and dc.h > sH.p and dc.c < sH.p
            if bull_r and bear_r:
                bull_r = dc.c >= dc.o; bear_r = not bull_r
            if not bull_r and sL.p is not None and dc.c < sL.p:
                sL.p = None; bias = -1
            if not bear_r and sH.p is not None and dc.c > sH.p:
                sH.p = None; bias = 1
            if bull_r:
                sL.p, sL.t = dc.l, dc.tL; bias = 1
            if bear_r:
                sH.p, sH.t = dc.h, dc.tH; bias = -1

        if new_day:
            today_bias = bias; cont_invalid = False; cont_lvl = None; counts["days"] += 1
            if day_closed and bias != 0:
                d1 = dH[-1]; rg = d1.h - d1.l
                if rg > 0:
                    opw = (d1.h - max(d1.o, d1.c)) if bias == 1 else (min(d1.o, d1.c) - d1.l)
                    if opw / rg * 100 > P["wick_max"]:
                        today_bias = 0; counts["skipped_wick"] += 1
                if today_bias != 0:
                    counts["bias_days"] += 1
                    opp = sL.p if today_bias == 1 else sH.p
                    if opp is not None and (opp < d1.c if today_bias == 1 else opp > d1.c):
                        cont_lvl = (d1.c + opp) / 2
        if cont_lvl is not None and not cont_invalid and today_bias != 0:
            if (c[i] < cont_lvl) if today_bias == 1 else (c[i] > cont_lvl):
                cont_invalid = True; today_bias = 0; counts["cont_invalid"] += 1

        # the 7-hour candle that just closed
        if p_cur is not None and new_blk:
            pH.append(p_cur)
            if len(pH) > 30: pH.pop(0)
            C = pH[-1]; Pv = pH[-2] if len(pH) >= 2 else None
            if C.blk == 1 and p_type == 1 and p_state in (1, 2) and p_rev is not None:
                p_inv = (p_ext + C.c) / 2
                if (C.c > p_rev.h) if p_dir == 1 else (C.c < p_rev.l):
                    p_state = 2
            elif Pv is not None and C.blk in (0, 1) and p_state in (0, 3):
                fb = C.l < Pv.l and C.c > Pv.l and today_bias == 1
                fs = C.h > Pv.h and C.c < Pv.h and today_bias == -1
                if fb and fs:
                    fb = C.c >= C.o; fs = not fb
                if fb or fs:
                    p_state, p_type, p_dir, p_rev = 1, C.blk + 1, (1 if fb else -1), C
                    p_ext = C.l if fb else C.h; p_inv = None; counts["profiles"][p_type] += 1
                    if C.blk == 1:
                        p_inv = (p_ext + C.c) / 2
            if C.blk in (0, 1):
                if day_lo is None or C.l < day_lo: day_lo = C.l
                if day_hi is None or C.h > day_hi: day_hi = C.h
        if p_cur is None or new_blk:
            p_cur = Candle(o[i], h[i], l[i], c[i], tms[i], int(blk[i]))
        else:
            p_cur.grow(h[i], l[i], c[i], tms[i])
        if new_day:
            p_state = p_type = p_dir = 0; p_rev = None; p_ext = p_inv = None; day_lo = day_hi = None; ent_count = 0

        # the New York profile forms on a bar inside its block
        if blk[i] == 2 and p_state == 0 and day_lo is not None and day_hi is not None:
            bull_ny = today_bias == 1 and p_cur.l < day_lo and c[i] > day_lo and bull_c
            bear_ny = today_bias == -1 and p_cur.h > day_hi and c[i] < day_hi and bear_c
            if bull_ny or bear_ny:
                p_state, p_type, p_dir, p_rev = 1, 3, (1 if bull_ny else -1), p_cur
                p_ext = p_cur.l if bull_ny else p_cur.h; p_inv = p_ext; counts["profiles"][3] += 1
        if p_state == 1 and p_rev is not None:
            if p_type == 2 and ((c[i] > p_rev.h) if p_dir == 1 else (c[i] < p_rev.l)): p_state = 2
            elif p_type == 3 and ((c[i] > p_rev.o) if p_dir == 1 else (c[i] < p_rev.o)): p_state = 2
        if p_state in (1, 2) and p_ext is not None:
            inv = (l[i] < p_ext) if p_dir == 1 else (h[i] > p_ext)
            if not inv and blk[i] == 2 and p_type in (1, 2) and p_inv is not None:
                inv = (l[i] < p_inv) if p_dir == 1 else (h[i] > p_inv)
            if inv:
                p_state = 3; counts["profile_invalid"] += 1

        # swings on the chart bars: a low below the 3 bars on each side, known 3 bars later
        j = i - P["piv_len"]
        if j - P["piv_len"] >= 0:
            if l[j] < l[j - 3:j].min() and l[j] < l[j + 1:i + 1].min(): refL, refLB = l[j], j
            if h[j] > h[j - 3:j].max() and h[j] > h[j + 1:i + 1].max(): refH, refHB = h[j], j
        if bear_c and not (i > 0 and c[i - 1] < o[i - 1]): dnO = o[i]
        if bull_c and not (i > 0 and c[i - 1] > o[i - 1]): upO = o[i]

        if new_day: swL = None; cLvlB = None
        if swL is None:
            if refL is not None and refLB != usedLB and l[i] < refL:
                swL, swLB, usedLB, cLvlB = l[i], i, refLB, dnO
        else:
            if l[i] <= swL: swL, swLB, cLvlB = l[i], i, dnO
            if i - swLB > P["cisd_max"]: swL = None
        if new_day: swH = None; cLvlS = None
        if swH is None:
            if refH is not None and refHB != usedHB and h[i] > refH:
                swH, swHB, usedHB, cLvlS = h[i], i, refHB, upO
        else:
            if h[i] >= swH: swH, swHB, cLvlS = h[i], i, upO
            if i - swHB > P["cisd_max"]: swH = None
        cisd_bull = swL is not None and cLvlB is not None and c[i] > cLvlB and bull_c
        cisd_bear = swH is not None and cLvlS is not None and c[i] < cLvlS and bear_c

        # an open trade
        time_out = new_day or (rel[i] >= exit_rel and (rel[i - 1] if i > 0 else 0) < exit_rel)
        if act is not None and i >= act["bE"]:
            d = act["dir"]
            gap_sl = o[i] <= act["sl"] if d == 1 else o[i] >= act["sl"]
            gap_tp = o[i] >= act["tp"] if d == 1 else o[i] <= act["tp"]
            at_open = gap_sl or gap_tp or time_out
            hit_sl = not at_open and (l[i] <= act["sl"] if d == 1 else h[i] >= act["sl"])
            hit_tp = not at_open and (h[i] >= act["tp"] if d == 1 else l[i] <= act["tp"])
            if at_open or hit_sl or hit_tp:
                xp = o[i] if at_open else act["sl"] if hit_sl else act["tp"]
                kind = "stop" if (gap_sl or hit_sl) else "target" if (gap_tp or hit_tp) else "time"
                trades.append(dict(day=act["day"], side=d, entry=act["entry"], exit=float(xp), f=act["risk"] / act["entry"], kind=kind, profile=act["profile"],
                                   signal_hour=act["hour"], exit_hour=int(hour[i])))
                act = None

        # a new trade
        in_win = blk[i] == 1 or (blk[i] == 2 and hour[i] < P["end_hour"])
        live = p_state in (1, 2)
        can_new = act is None and ent_count < P["max_entries"] and i - last_ent >= P["cool"]
        go_b = can_new and cisd_bull and in_win and today_bias == 1 and live and p_dir == 1
        go_s = can_new and cisd_bear and in_win and today_bias == -1 and live and p_dir == -1 and not go_b
        if go_b or go_s:
            d = 1 if go_b else -1
            sl = swL if go_b else swH
            if sl is None or (sl >= c[i] if d == 1 else sl <= c[i]):
                sl = l[i] if d == 1 else h[i]
            risk = abs(c[i] - sl)
            if risk > 0:
                counts["triggers"] += 1
                ent_count += 1; last_ent = i
                if i + 1 < n and START <= date[i] <= END:            # entry at the next bar's open; stop and target as the script set them
                    act = dict(dir=d, sl=sl, tp=c[i] + d * P["rr"] * risk, risk=risk, entry=o[i + 1], bE=i + 1, day=date[i], profile=PROFILE[p_type], hour=int(hour[i]))
                else:
                    act = dict(dir=d, sl=sl, tp=c[i] + d * P["rr"] * risk, risk=risk, entry=o[i + 1] if i + 1 < n else c[i], bE=i + 1, day=None, profile=PROFILE[p_type], hour=int(hour[i]))
        if cisd_bull: swL = None; cLvlB = None
        if cisd_bear: swH = None; cLvlS = None
    return [t for t in trades if t["day"] is not None], counts


# ---------------------------------------------------------------- statistics

def net_r(tr, mult):
    """R after costs: the market's fee on entry and exit, slippage on a stop. mult 0 is before costs, 2 is double cost."""
    ex = np.where(tr["kind"] == "stop", tr["exit"] * (1 - tr["side"] * SLIP * mult), tr["exit"])
    return (tr["side"] * (ex / tr["entry"] - 1) - tr["fee"] * mult * (1 + ex / tr["entry"])) / tr["f"]


def stats(x):
    x = np.asarray(x, dtype=float); n = len(x)
    if n == 0:
        return dict(n=0, mean=0.0, t=0.0, pf=0.0, win=0.0, total=0.0)
    sd = x.std(ddof=1) if n > 1 else 0.0; pos = x[x > 0].sum(); neg = -x[x < 0].sum()
    return dict(n=n, mean=float(x.mean()), t=float(x.mean() / (sd / np.sqrt(n))) if sd > 0 else 0.0,
                pf=float(pos / neg) if neg > 0 else float("inf"), win=float((x > 0).mean()), total=float(x.sum()))


def report(tr, markets, cost_on=True):
    base = 1.0 if cost_on else 0.0
    r = net_r(tr, base); r2 = net_r(tr, 2 * base); r0 = net_r(tr, 0.0)
    d = r.groupby(tr["day"]).mean(); d2 = r2.groupby(tr["day"]).mean(); d0 = r0.groupby(tr["day"]).mean()
    s = stats(d)
    yr = {y: float(d[[k.year == y for k in d.index]].sum()) for y in PASS["years"]}
    mk = {m: stats(r[tr["market"] == m]) for m in markets}
    grp = {g: stats(r[tr["group"] == g]) for g in sorted(tr["group"].unique())}
    prof = {p: stats(r[tr["profile"] == p]) for p in sorted(tr["profile"].unique())}
    long_s, short_s = stats(r[tr["side"] == 1]), stats(r[tr["side"] == -1])
    need = PASS["markets_ok"] if len(markets) == 15 else (len(markets) + 1) // 2
    checks = {
        "at least 150 traded days": s["n"] >= PASS["days"],
        "average above zero with t-stat >= 2.58": s["mean"] > 0 and s["t"] >= PASS["t"],
        "profit factor >= 1.15": s["pf"] >= PASS["pf"],
        "average above zero at double cost": d2.mean() > 0,
        f"positive on {need} of {len(markets)} markets": sum(1 for v in mk.values() if v["mean"] > 0) >= need,
        "positive in four of six years": sum(1 for v in yr.values() if v > 0) >= PASS["years_ok"],
        "longs and shorts each above zero": long_s["n"] > 0 and short_s["n"] > 0 and long_s["mean"] > 0 and short_s["mean"] > 0,
    }
    return dict(days=s, before_costs=stats(d0), double_cost_mean=float(d2.mean()), by_year=yr, by_market=mk, by_group=grp, by_profile=prof,
                longs=long_s, shorts=short_s, trades=int(len(tr)), trade_stats=stats(r), trade_stats_before_costs=stats(r0),
                avg_cost_r=float((r0 - r).mean()), endings=tr["kind"].value_counts().to_dict(), checks=checks, passed=bool(all(checks.values())))


def main():
    dry = "--dryrun" in sys.argv
    if not dry and os.path.exists(RESULTS):
        sys.exit("This study has already run. Its result is in lab/intraday/fractal7h_results.json and the journal. It runs once.")
    markets = [f"FAKE{k}" for k in range(6)] if dry else list(FEES)
    rows = []; cnt = {}
    for k, m in enumerate(markets):
        tr, c = simulate(load(m, fake_seed=200 + k if dry else None))
        for t in tr:
            t["market"] = m; t["fee"] = 0.0 if dry else FEES[m]; t["group"] = "made-up" if dry else GROUP.get(m, "forex")
        rows += tr; cnt[m] = c
    tr = pd.DataFrame(rows)
    out = report(tr, markets, cost_on=not dry); out["counts"] = cnt
    s, b = out["days"], out["before_costs"]
    print(f"{out['trades']} trades on {s['n']} days · day average {s['mean']:+.4f}R · t-stat {s['t']:.2f} · profit factor {s['pf']:.2f} · trade win rate {out['trade_stats']['win']:.0%}")
    print(f"   before costs: day average {b['mean']:+.4f}R · t-stat {b['t']:.2f} · profit factor {b['pf']:.2f} · cost per trade {out['avg_cost_r']:.4f}R · double cost {out['double_cost_mean']:+.4f}R")
    print(f"   by year {{{', '.join(f'{y}: {v:+.1f}' for y, v in out['by_year'].items())}}} · longs {out['longs']['n']} avg {out['longs']['mean']:+.4f} · shorts {out['shorts']['n']} avg {out['shorts']['mean']:+.4f}")
    print(f"   by market {{{', '.join(f'{m}: {v['mean']:+.3f} ({v['n']})' for m, v in out['by_market'].items())}}}")
    print(f"   by group {{{', '.join(f'{g}: {v['mean']:+.3f} ({v['n']})' for g, v in out['by_group'].items())}}} · by profile {{{', '.join(f'{p}: {v['mean']:+.3f} ({v['n']})' for p, v in out['by_profile'].items())}}} · endings {out['endings']}")
    tot = {k: sum(c[k] for c in cnt.values()) for k in ("days", "bias_days", "skipped_wick", "cont_invalid", "profile_invalid", "triggers")}
    tot["profiles"] = {PROFILE[k]: sum(c["profiles"][k] for c in cnt.values()) for k in (1, 2, 3)}
    print(f"   counts {tot}")
    verdict = "PASS" if out["passed"] else ("FAIL (too few trades)" if not out["checks"]["at least 150 traded days"] else "FAIL")
    out["verdict"] = verdict; out["totals"] = tot
    failed = [k for k, ok in out["checks"].items() if not ok]
    print(("DRY RUN on made-up prices, no cost. " if dry else "") + f"Verdict: {verdict}" + (f" · failed: {'; '.join(failed)}" if failed else ""))
    if not dry:
        out["run_date"] = datetime.date.today().isoformat()
        json.dump(out, open(RESULTS, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
