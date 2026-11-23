"""Study 8: liquidity sweep, fair value gap, return to the gap. 96 registered scenarios on 1-minute bars. One run.

Run from the repo root:
    python lab/intraday/sweep_fvg.py --check     # compares the fast code with a plain bar-by-bar version on made-up prices
    python lab/intraday/sweep_fvg.py --dryrun    # same code on made-up prices with no cost; nothing is written
    python lab/intraday/sweep_fvg.py             # the one real run; refuses to run a second time

The rules are in LAB_RULES.md under "Study 8". They were written and pushed before this rule was run on any lab data.
Source of the rule: a post by @L2WTrades on X, x.com/L2WTrades/status/2124841683896406023 (November 23, 2026).
The post gives the steps in words. The code below is the lab's own, and every choice the post leaves open is a scenario part.

Everything is written for the high side: a level above price is swept, a down gap forms, a sell order rests in the gap.
The low side runs the same code on prices turned upside down.
"""
import sys, os, json, datetime, itertools
from statistics import NormalDist
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.join(HERE, "..")
RESULTS = os.path.join(HERE, "sweep_fvg_results.json")
MARKETS = ["NAS100", "SPX500", "USA30"]
H1_DIR = {"NAS100": "data_new", "SPX500": "data_new", "USA30": "data"}
COST = 0.00005                                              # 0.005% of price per round trip
START, SPLIT, END = datetime.date(2021, 6, 1), datetime.date(2024, 1, 1), datetime.date(2026, 11, 19)
M0 = 9 * 60                                                 # minute bars are used from 9:00 New York time
W0, W1, FLAT, NMIN = 30, 180, 415, 435                      # 9:30, 12:00, 15:55 and 16:15 as minutes after 9:00
GAP_K, AVG_BARS, AVG_MIN = 0.25, 24, 6                      # smallest gap, in average bar ranges, and the bars the average uses
SWING_SIDE, SWING_BACK = 2, 30                              # 4-hour swing: 2 candles each side, looked for in the last 30 candles
S = dict(days=150, t=1.65, pf=1.10)
C = dict(days=150, pf=1.15, min_survivors=5, years=(2024, 2025, 2026), years_ok=2)
SCENARIOS = [dict(level=a, timing=b, tf=c, entry=d, stop=e, target=f) for a, b, c, d, e, f in
             itertools.product(("pdhl", "swing4h"), ("window", "overnight"), (1, 5), ("edge", "mid"), ("gap", "sweep"), ("2r", "3r", "opp"))]
NAN = float("nan")


def name(v):
    return f"{v['level']}.{v['timing']}.m{v['tf']}.{v['entry']}.{v['stop']}stop.{v['target']}"


# ---------------------------------------------------------------- data

def fake_minutes(seed):
    """Made-up 24-hour 1-minute prices, Sunday 18:00 to Friday 17:00 New York time, with the daily 17:00 break."""
    rng = np.random.default_rng(seed)
    t = pd.date_range("2021-04-20 22:00", "2026-11-20 21:14", freq="min", tz="UTC")
    ny = t.tz_convert("America/New_York")
    wd, hr = ny.dayofweek.to_numpy(), ny.hour.to_numpy()
    t = t[~((wd == 5) | ((wd == 6) & (hr < 18)) | ((wd == 4) & (hr >= 17)) | (hr == 17))]
    n = len(t)
    c = 15000 * np.exp(np.cumsum(rng.normal(0, 0.0003, n))); o = np.r_[15000.0, c[:-1]]
    wick = np.abs(rng.normal(0, 0.00015, (n, 2)))
    return pd.DataFrame({"time": t, "open": o, "high": np.maximum(o, c) * (1 + wick[:, 0]), "low": np.minimum(o, c) * (1 - wick[:, 1]), "close": c})


def load(m, fake_seed=None):
    """Returns (minute bars, hourly bars for the whole day)."""
    if fake_seed is not None:
        mn = fake_minutes(fake_seed)
        hr = mn.set_index("time").resample("1h").agg({"open": "first", "high": "max", "low": "min", "close": "last"}).dropna().reset_index()
    else:
        mn = pd.read_csv(os.path.join(LAB, "data_1m", f"{m}_1m_full.csv.gz")); mn["time"] = pd.to_datetime(mn["time"], unit="s", utc=True)
        hr = pd.read_csv(os.path.join(LAB, H1_DIR[m], f"{m}_1h.csv.gz")); hr["time"] = pd.to_datetime(hr["time"], utc=True)
    return mn.sort_values("time").reset_index(drop=True), hr.sort_values("time").reset_index(drop=True)


def prepare(mn, hr):
    """One record per usable day: minute arrays from 9:00, the overnight high and low, and the two kinds of level."""
    ny = hr["time"].dt.tz_convert("America/New_York").dt.tz_localize(None)
    label = (ny + pd.Timedelta(hours=7)).dt.normalize()                     # a trading day runs from 17:00 to 17:00 and is named by the date it ends on
    hh, hl = hr["high"].to_numpy(float), hr["low"].to_numpy(float)
    daily = pd.DataFrame({"label": label.to_numpy(), "h": hh, "l": hl}).groupby("label", sort=True).agg(h=("h", "max"), l=("l", "min"), n=("h", "size"))
    d_keys = daily.index.to_numpy(); d_h, d_l, d_n = daily["h"].to_numpy(), daily["l"].to_numpy(), daily["n"].to_numpy()
    k4 = (ny - pd.Timedelta(hours=17)).dt.floor("4h") + pd.Timedelta(hours=17)  # 4-hour candles start at 17:00, 21:00, 1:00, 5:00, 9:00, 13:00
    c4 = pd.DataFrame({"k": k4.to_numpy(), "h": hh, "l": hl}).groupby("k", sort=True).agg(h=("h", "max"), l=("l", "min"))
    key4 = c4.index.to_numpy(); h4, l4 = c4["h"].to_numpy(), c4["l"].to_numpy()
    n4 = len(h4); sh = np.zeros(n4, bool); sl = np.zeros(n4, bool)
    for j in range(SWING_SIDE, n4 - SWING_SIDE):
        around = list(range(j - SWING_SIDE, j)) + list(range(j + 1, j + SWING_SIDE + 1))
        sh[j] = all(h4[j] > h4[x] for x in around); sl[j] = all(l4[j] < l4[x] for x in around)
    hour = ny.dt.hour.to_numpy(); early = (hour < 9) | (hour >= 17)         # with the label, this picks the bars from 18:00 to 8:59
    lab_np = label.to_numpy()

    nym = mn["time"].dt.tz_convert("America/New_York").dt.tz_localize(None)
    mod = (nym.dt.hour * 60 + nym.dt.minute).to_numpy() - M0
    keep = (mod >= 0) & (mod < NMIN)
    mday = nym.dt.normalize().to_numpy()[keep]; mod = mod[keep]
    cols = [mn[x].to_numpy(float)[keep] for x in ("open", "high", "low", "close")]
    bounds = np.r_[0, np.flatnonzero(mday[1:] != mday[:-1]) + 1, len(mday)]
    out = []
    for a, b in zip(bounds[:-1], bounds[1:]):
        D = mday[a]; date = pd.Timestamp(D).date()
        if not (START <= date <= END):
            continue
        arr = np.full((4, NMIN), NAN); arr[:, mod[a:b]] = [x[a:b] for x in cols]
        have = ~np.isnan(arr[1])
        on = (lab_np == D) & early
        if have[:W0].sum() < 27 or have[W0:W1].sum() < 140 or on.sum() < 13:
            continue                                                        # a day with too few bars is skipped for this market
        rec = dict(date=date, o=arr[0], h=arr[1], l=arr[2], c=arr[3], omax=float(hh[on].max()), omin=float(hl[on].min()), levels={})
        i = int(np.searchsorted(d_keys, D))                                 # previous day's high and low
        rec["levels"]["pdhl"] = (float(d_h[i - 1]), float(d_l[i - 1])) if i >= 1 and d_keys[i] == D and d_n[i - 1] >= 18 else (None, None)
        e = int(np.searchsorted(key4, D - np.timedelta64(7, "h")))          # 4-hour candles that closed by 17:00 the day before
        hi = lo = None
        for j in range(e - 1 - SWING_SIDE, max(SWING_SIDE, e - SWING_BACK) - 1, -1):
            if hi is None and sh[j] and h4[j + 1:e].max() <= h4[j]: hi = float(h4[j])
            if lo is None and sl[j] and l4[j + 1:e].min() >= l4[j]: lo = float(l4[j])
            if hi is not None and lo is not None: break
        rec["levels"]["swing4h"] = (hi, lo)
        out.append(rec)
    return out


# ---------------------------------------------------------------- the rule, high side

def make_bars(h, l, tf):
    """Bars of tf minutes from 9:00. A bar with a missing minute is not complete and cannot be part of a gap."""
    if tf == 1:
        hi, lo, ok = h, l, ~np.isnan(h); start = np.arange(NMIN)
    else:
        nb = NMIN // tf; H = h[:nb * tf].reshape(nb, tf); L = l[:nb * tf].reshape(nb, tf)
        ok = ~np.isnan(H).any(axis=1); hi = np.where(ok, np.nanmax(np.where(np.isnan(H), -np.inf, H), axis=1), NAN)
        lo = np.where(ok, np.nanmin(np.where(np.isnan(L), np.inf, L), axis=1), NAN); start = np.arange(nb) * tf
    rng = np.where(ok, hi - lo, 0.0); cs = np.r_[0.0, np.cumsum(rng)]; cn = np.r_[0, np.cumsum(ok)]
    k = np.arange(len(hi)); a = np.maximum(0, k - AVG_BARS)
    cnt = cn[k] - cn[a]
    avg = np.where(cnt >= AVG_MIN, (cs[k] - cs[a]) / np.maximum(cnt, 1), NAN)   # average range of the up to 24 complete bars before bar k
    return dict(hi=hi, lo=lo, ok=ok, start=start, end=start + tf - 1, avg=avg, tf=tf)


def find_setup(d, h, omax, level, timing, bars):
    """The sweep and the first down gap after it. Returns None, or the order's two prices and the minute it goes live."""
    if level is None:
        return None
    if max(omax, np.nanmax(h[:W0])) > level:                 # traded above the level before 9:30
        if timing == "window":
            return None
        s = W0
    else:
        hit = np.flatnonzero(h[W0:W1] > level)
        if len(hit) == 0:
            return None
        s = W0 + int(hit[0])
    hi, lo, ok, start, end, avg, tf = (bars[x] for x in ("hi", "lo", "ok", "start", "end", "avg", "tf"))
    n = len(hi) - 2
    with np.errstate(invalid="ignore"):
        gap = lo[:n] - hi[2:]
        good = ok[:n] & ok[1:n + 1] & ok[2:] & (gap > 0) & (gap >= GAP_K * avg[:n]) & (start[:n] >= s - s % tf) & (end[2:] <= W1 - 2)
    ks = np.flatnonzero(good)
    if len(ks) == 0:
        return None
    k = int(ks[0]); place = int(end[k + 2]) + 1
    return dict(near=float(hi[k + 2]), far=float(lo[k]), place=place, ext=float(max(omax, np.nanmax(h[:place]))))


def find_trade(o, h, l, c, omin, st, entry_opt, stop_opt, target_opt, opp):
    """A sell order in the gap. Returns None, or (fill minute, minute placed, R before cost, cost in R, how it ended)."""
    entry = st["near"] if entry_opt == "edge" else (st["near"] + st["far"]) / 2
    stop = st["far"] if stop_opt == "gap" else st["ext"]
    risk = stop - entry
    if not risk > 0:
        return None
    place = st["place"]
    if target_opt == "opp":
        if opp is None or min(omin, np.nanmin(l[:place])) <= opp or entry - opp < 3 * risk:
            return None                                      # no pool on the other side, already traded, or closer than 3R
        target = opp
    else:
        target = entry - (2 if target_opt == "2r" else 3) * risk
    with np.errstate(invalid="ignore"):
        fills = np.flatnonzero(h[place:W1] >= entry)
        if len(fills) == 0:
            return None
        f = place + int(fills[0])
        if target_opt == "opp" and (l[place:f + 1] <= target).any():
            return None                                      # the pool on the other side traded before the order filled: cancelled
        cost = COST * abs(entry) / risk
        if h[f] >= stop:
            return (f, place, -1.0, cost, "stop_fill_minute")
        oo, hh, ll = o[f + 1:FLAT], h[f + 1:FLAT], l[f + 1:FLAT]
        ev = np.flatnonzero((oo >= stop) | (hh >= stop) | (oo <= target) | (ll <= target))
    if len(ev):
        j = int(ev[0])
        if oo[j] >= stop: px, how = oo[j], "stop"
        elif oo[j] <= target: px, how = oo[j], "target"
        elif hh[j] >= stop: px, how = stop, "stop"
        else: px, how = target, "target"
    elif o[FLAT] == o[FLAT]:
        px, how = o[FLAT], "time"
    else:
        last = np.flatnonzero(~np.isnan(c[f:FLAT])); px, how = c[f + int(last[-1])], "time"
    return (f, place, float((entry - px) / risk), cost, how)


def day_sides(d):
    """Both sides of one day: the day as it is (sell after a swept high) and upside down (buy after a swept low)."""
    up = dict(o=d["o"], h=d["h"], l=d["l"], c=d["c"], omax=d["omax"], omin=d["omin"], side=-1,
              levels={k: v for k, v in d["levels"].items()})
    dn = dict(o=-d["o"], h=-d["l"], l=-d["h"], c=-d["c"], omax=-d["omin"], omin=-d["omax"], side=1,
              levels={k: (None if v[1] is None else -v[1], None if v[0] is None else -v[0]) for k, v in d["levels"].items()})
    for s in (up, dn):
        s["bars"] = {tf: make_bars(s["h"], s["l"], tf) for tf in (1, 5)}
    return up, dn


def run_market(days):
    """Trades of every scenario for one market: {scenario name: [(date, R before cost, cost in R, side, how it ended)]}."""
    out = {name(v): [] for v in SCENARIOS}
    for d in days:
        sides = day_sides(d)
        setups = {}
        for si, s in enumerate(sides):
            for lv in ("pdhl", "swing4h"):
                for tm in ("window", "overnight"):
                    for tf in (1, 5):
                        setups[(si, lv, tm, tf)] = find_setup(s, s["h"], s["omax"], s["levels"][lv][0], tm, s["bars"][tf])
        for v in SCENARIOS:
            cands = []
            for si, s in enumerate(sides):
                st = setups[(si, v["level"], v["timing"], v["tf"])]
                if st is None:
                    continue
                tr = find_trade(s["o"], s["h"], s["l"], s["c"], s["omin"], st, v["entry"], v["stop"], v["target"], s["levels"][v["level"]][1])
                if tr is not None:
                    cands.append(tr + (s["side"],))
            if not cands:
                continue
            cands.sort(key=lambda x: (x[0], x[1]))
            if len(cands) == 2 and cands[0][:2] == cands[1][:2]:
                continue                                     # both sides filled in the same minute from orders placed together: no trade
            f, place, r, cost, how, side = cands[0]
            out[name(v)].append((d["date"], r, cost, side, how))
    return out


# ---------------------------------------------------------------- a plain version of the same rule, for --check

def reference_trade(d, v):
    """One scenario on one day, one minute at a time, with no shortcuts. Used only to check the fast code."""
    best = None
    for side in (-1, 1):
        if side == -1:
            o, h, l, c, omax, omin = d["o"], d["h"], d["l"], d["c"], d["omax"], d["omin"]; level, opp = d["levels"][v["level"]]
        else:
            o, h, l, c, omax, omin = -d["o"], -d["l"], -d["h"], -d["c"], -d["omin"], -d["omax"]; lo_hi = d["levels"][v["level"]]
            level, opp = (None if lo_hi[1] is None else -lo_hi[1]), (None if lo_hi[0] is None else -lo_hi[0])
        if level is None:
            continue
        run_hi, run_lo, swept_at = omax, omin, None
        for i in range(W0):
            if h[i] == h[i]: run_hi = max(run_hi, h[i]); run_lo = min(run_lo, l[i])
        if run_hi > level:
            if v["timing"] == "window":
                continue
            swept_at = W0
        tf = v["tf"]; bars = []                              # finished bars so far today: (start, high, low, complete)
        order = None; res = None; pos = None
        for i in range(NMIN):
            if i % tf == tf - 1:                             # a bar of tf minutes ends with this minute
                seg_h, seg_l = h[i - tf + 1:i + 1], l[i - tf + 1:i + 1]; okb = not np.isnan(seg_h).any()
                bars.append((i - tf + 1, max(seg_h) if okb else NAN, min(seg_l) if okb else NAN, okb))
            if i < W0:
                continue
            if pos is None and order is None and swept_at is None and i < W1 and h[i] == h[i] and h[i] > level:
                swept_at = i
            if h[i] == h[i]:
                run_hi = max(run_hi, h[i]); run_lo = min(run_lo, l[i])
            if pos is not None:                              # in a trade
                entry, stop, target, risk, f = pos
                if i < FLAT and o[i] == o[i]:
                    if o[i] >= stop or o[i] <= target: res = (f, (entry - o[i]) / risk); break
                    if h[i] >= stop: res = (f, -1.0); break
                    if l[i] <= target: res = (f, (entry - target) / risk); break
                    last_close = c[i]
                elif i == FLAT:
                    res = (f, (entry - (o[i] if o[i] == o[i] else last_close)) / risk); break
                continue
            if order is not None and i < W1 and h[i] == h[i]:  # resting order
                entry, stop, target, risk, placed = order
                if v["target"] == "opp" and l[i] <= target: break   # cancelled
                if h[i] >= entry:
                    if h[i] >= stop: res = (i, -1.0); break
                    pos = (entry, stop, target, risk, i); last_close = c[i]
                continue
            if order is not None and i >= W1:
                break
            if order is None and swept_at is not None and i % tf == tf - 1 and i <= W1 - 2 and len(bars) >= 3:
                b1, b2, b3 = bars[-3], bars[-2], bars[-1]
                prior = [x for x in bars[:-3][-AVG_BARS:] if x[3]]
                if b1[3] and b2[3] and b3[3] and len(prior) >= AVG_MIN and b1[0] >= swept_at - swept_at % tf and b1[0] >= W0:
                    gap = b1[2] - b3[1]; avg = sum(x[1] - x[2] for x in prior) / len(prior)
                    if gap > 0 and gap >= GAP_K * avg:
                        near, far = b3[1], b1[2]
                        entry = near if v["entry"] == "edge" else (near + far) / 2
                        stop = far if v["stop"] == "gap" else run_hi
                        risk = stop - entry
                        if v["target"] == "opp":
                            if opp is None or run_lo <= opp or entry - opp < 3 * risk: break
                            target = opp
                        else:
                            target = entry - (2 if v["target"] == "2r" else 3) * risk
                        order = (entry, stop, target, risk, i + 1)
        if res is not None:
            cand = (res[0], order[4], res[1], side)
            if best is None or cand[:2] < best[:2]: best = cand
            elif cand[:2] == best[:2]: best = "tie"
    return None if best in (None, "tie") else (best[2], best[3])


def check():
    """Fast code against the plain version, on made-up prices."""
    mn, hr = load("X", fake_seed=7); days = prepare(mn, hr)[:260]
    fast = run_market(days); bad = n = 0
    for v in SCENARIOS:
        got = {t[0]: (t[1], t[3]) for t in fast[name(v)]}
        for d in days:
            ref = reference_trade(d, v); g = got.get(d["date"]); n += ref is not None
            if (ref is None) != (g is None) or (ref is not None and (abs(ref[0] - g[0]) > 1e-9 or ref[1] != g[1])):
                bad += 1
                if bad <= 10: print("MISMATCH", name(v), d["date"], "plain:", ref, "fast:", g)
    print(f"check: {len(days)} days x {len(SCENARIOS)} scenarios, {n} trades in the plain version, {bad} mismatches")
    return bad == 0


# ---------------------------------------------------------------- counting

def stats(tr, cost_mult=1.0):
    """Statistics on daily averages in R: a day counts once however many of the three markets traded."""
    if tr.empty:
        return dict(days=0)
    tr = tr.assign(net=tr["r"] - cost_mult * tr["cost"])
    daily = tr.groupby("day")["net"].mean(); r = daily.to_numpy()
    if len(r) < 3 or r.std(ddof=1) == 0:
        return dict(days=int(len(r)))
    wins, losses = r[r > 0], r[r <= 0]
    by_year = daily.groupby([d.year for d in daily.index]).sum()
    per_market = tr.groupby("market")["net"].mean()
    dbl = (tr["r"] - 2 * cost_mult * tr["cost"]).groupby(tr["day"]).mean()
    gross = tr.groupby("day")["r"].mean()
    return dict(days=int(len(r)), trades=int(len(tr)), mean_r=float(r.mean()), total_r=float(r.sum()),
                t=float(r.mean() / (r.std(ddof=1) / np.sqrt(len(r)))), pf=float(wins.sum() / -losses.sum()) if losses.sum() < 0 else float("inf"),
                win_rate=float((tr["net"] > 0).mean() * 100), mean_r_double_cost=float(dbl.mean()), mean_r_before_cost=float(gross.mean()),
                avg_cost_r=float(tr["cost"].mean() * cost_mult), markets_positive=int((per_market > 0).sum()),
                per_market_mean_r={k: round(float(x), 4) for k, x in per_market.items()},
                by_year_r={int(k): round(float(x), 2) for k, x in by_year.items()},
                long_mean_r=float(tr.loc[tr["side"] == 1, "net"].mean()) if (tr["side"] == 1).any() else NAN,
                short_mean_r=float(tr.loc[tr["side"] == -1, "net"].mean()) if (tr["side"] == -1).any() else NAN,
                endings={k: int(x) for k, x in tr["how"].value_counts().items()})


def screen_checks(s):
    if "t" not in s:
        return {f"traded days >= {S['days']}": False}
    return {f"traded days >= {S['days']}": bool(s["days"] >= S["days"]), f"average above zero with t-stat >= {S['t']}": bool(s["mean_r"] > 0 and s["t"] >= S["t"]),
            f"profit factor >= {S['pf']}": bool(s["pf"] >= S["pf"]), "positive on two of three markets": bool(s["markets_positive"] >= 2),
            "average above zero at double cost": bool(s["mean_r_double_cost"] > 0)}


def confirm_checks(s, need_t):
    if "t" not in s:
        return {f"traded days >= {C['days']}": False}
    years_ok = sum(s["by_year_r"].get(y, 0) > 0 for y in C["years"])
    return {f"traded days >= {C['days']}": bool(s["days"] >= C["days"]), f"average above zero with t-stat >= {need_t:.2f}": bool(s["mean_r"] > 0 and s["t"] >= need_t),
            f"profit factor >= {C['pf']}": bool(s["pf"] >= C["pf"]), "positive on two of three markets": bool(s["markets_positive"] >= 2),
            "average above zero at double cost": bool(s["mean_r_double_cost"] > 0), "positive in two of 2024, 2025, 2026": bool(years_ok >= C["years_ok"]),
            "longs and shorts each above zero": bool(s["long_mean_r"] > 0 and s["short_mean_r"] > 0)}


def main():
    if "--check" in sys.argv:
        sys.exit(0 if check() else 1)
    dry = "--dryrun" in sys.argv
    if os.path.exists(RESULTS) and not dry:
        print("Study 8 has already been run. It runs once. See lab/intraday/sweep_fvg_results.json."); return
    assert len(SCENARIOS) == 96
    per = {}; n_days = {}
    for k, m in enumerate(MARKETS):
        mn, hr = load(m, fake_seed=k + 1 if dry else None)
        days = prepare(mn, hr); n_days[m] = len(days); per[m] = run_market(days)
    rows = []
    for v in SCENARIOS:                                      # screen: the screen years only
        nm = name(v)
        tr = pd.DataFrame([(d, m, r, c, side, how) for m in MARKETS for d, r, c, side, how in per[m][nm]], columns=["day", "market", "r", "cost", "side", "how"])
        s = stats(tr[tr["day"] < SPLIT], cost_mult=0.0 if dry else 1.0); ch = screen_checks(s)
        rows.append(dict(scenario=nm, parts=v, screen=s, screen_checks=ch, screen_pass=all(ch.values()), trades=tr))
    survivors = [r for r in rows if r["screen_pass"]]
    need_t = NormalDist().inv_cdf(1 - 0.05 / max(len(survivors), C["min_survivors"]))
    for r in rows:                                           # confirm: only survivors ever have their confirm years computed
        tr = r.pop("trades")
        if r["screen_pass"]:
            s = stats(tr[tr["day"] >= SPLIT], cost_mult=0.0 if dry else 1.0); ch = confirm_checks(s, need_t)
            r.update(confirm=s, confirm_checks=ch, verdict="CONFIRMED" if all(ch.values()) else "REJECT")
        else:
            r["verdict"] = "REJECT"
        s = r["screen"]
        line = (f"{s['days']:4d} days, avg {s['mean_r']:+.3f}R (before cost {s['mean_r_before_cost']:+.3f}R, cost {s['avg_cost_r']:.3f}R), PF {s['pf']:.2f}, "
                f"t {s['t']:+.2f}, markets {s['markets_positive']}/3") if "t" in s else f"{s['days']} days"
        tail = ""
        if "confirm" in r:
            c = r["confirm"]; tail = f" | confirm: {c['days']} days, avg {c['mean_r']:+.3f}R, PF {c['pf']:.2f}, t {c['t']:+.2f}/{need_t:.2f}" if "t" in c else f" | confirm: {c['days']} days"
        print(f"{r['verdict']:9s} {r['scenario']:44s} screen: {line}{' PASS' if r['screen_pass'] else ''}{tail}")
    confirmed = [r for r in rows if r["verdict"] == "CONFIRMED"]
    full = [r["screen"] for r in rows if "t" in r["screen"]]
    family = dict(scenarios=len(rows), with_statistics=len(full), enough_days=sum(s["days"] >= S["days"] for s in full),
                  positive_after_cost=sum(s["mean_r"] > 0 for s in full), positive_before_cost=sum(s["mean_r_before_cost"] > 0 for s in full),
                  median_mean_r=float(np.median([s["mean_r"] for s in full])) if full else NAN,
                  median_mean_r_before_cost=float(np.median([s["mean_r_before_cost"] for s in full])) if full else NAN,
                  median_pf=float(np.median([s["pf"] for s in full])) if full else NAN, median_cost_r=float(np.median([s["avg_cost_r"] for s in full])) if full else NAN)
    print(f"{len(rows)} scenarios, {len(survivors)} passed the screen, {len(confirmed)} confirmed (bar {need_t:.2f})")
    print("family, screen years:", json.dumps(family))
    if dry:
        print("dry run on made-up prices with no cost: nothing written"); return
    today = datetime.date.today().isoformat()
    json.dump(dict(date=today, first_day=str(START), split=str(SPLIT), last_day=str(END), usable_days=n_days, need_t=need_t, survivors=len(survivors),
                   confirmed=len(confirmed), family=family, scenarios=rows), open(RESULTS, "w"), indent=1, default=float)
    with open(os.path.join(LAB, "JOURNAL.md"), "a") as j:
        j.write(f"\n### {today} · study 8 · sweep, fair value gap, return to the gap · 96 scenarios · {len(survivors)} passed the screen, {len(confirmed)} confirmed\n"
                f"- Source: a post by @L2WTrades on X (x.com/L2WTrades/status/2124841683896406023). Nasdaq 100, S&P 500 and Dow, 1-minute bars, 9:30 to 12:00 New York time.\n"
                f"- Screen: {START} to 2023-12-31. Confirm: 2024-01-01 to {END}, t-stat bar {need_t:.2f}. Results in R after a cost of 0.005% of price per round trip.\n"
                f"- The family in the screen years: {family['positive_after_cost']} of {family['with_statistics']} scenarios with trades had an average above zero after costs, "
                f"{family['positive_before_cost']} before costs. Median average {family['median_mean_r']:+.3f}R a day after costs, {family['median_mean_r_before_cost']:+.3f}R before. "
                f"Median cost {family['median_cost_r']:.3f}R a trade. {family['enough_days']} scenarios had 150 or more traded days.\n")
        for r in rows:
            s = r["screen"]
            if "t" not in s:
                j.write(f"- `{r['scenario']}` · REJECT: {s['days']} traded days\n"); continue
            txt = (f"- `{r['scenario']}` · {r['verdict']}: screen {s['days']} days, average {s['mean_r']:+.3f}R ({s['mean_r_before_cost']:+.3f}R before costs), "
                   f"profit factor {s['pf']:.2f}, t-stat {s['t']:.2f}")
            if "confirm" in r and "t" in r["confirm"]:
                c = r["confirm"]; fails = [k for k, ok in r["confirm_checks"].items() if not ok]
                txt += f"; confirm {c['days']} days, average {c['mean_r']:+.3f}R, profit factor {c['pf']:.2f}, t-stat {c['t']:.2f}" + (f". Failed: {'; '.join(fails)}" if fails else "")
            j.write(txt + "\n")
    print("written to lab/intraday/sweep_fvg_results.json and the journal")


if __name__ == "__main__":
    main()
