"""Study 10: thirteen published claims from one X account (@RHerman), each checked once.

Run from the repo root:
    python lab/intraday/herman_claims.py --dryrun    # same code on made-up prices; nothing is written
    python lab/intraday/herman_claims.py --check     # made-up prices: the mixed hourly and minute path against a pure minute path
    python lab/intraday/herman_claims.py             # the one real run; refuses to run a second time

The rules are in LAB_RULES.md under "Study 10". They were written and pushed before this code was run on any lab data.
The posts give a rate for a price level being reached or left alone. None gives an entry, a stop or costs.
Every level claim is turned into the same test: from the check time, is the level reached before a phantom level
the same distance away on the other side? A claim that the level is taken trades toward it. A claim that it
survives trades away from it. Target and stop are the level and the phantom level.
"""
import sys, os, json, datetime, math
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.join(HERE, "..")
sys.path.insert(0, HERE); sys.path.insert(0, LAB)
import sweep_fvg as data_io
import costs

RESULTS = os.path.join(HERE, "herman_claims_results.json")
START, END = datetime.date(2021, 5, 3), datetime.date(2026, 11, 19)
M0, M1 = 480, 975                    # minute bars are kept from 8:00 to 16:14 New York time
RTH0, RTH1 = 570, 960
FLOOR = 0.0004                       # a trade needs the level at least 0.04% of price away
N_TESTS = 13
Z_BAR = 2.67                         # one-sided 5% shared over 13 tests
P_BAR = 0.05 / N_TESTS
MIN_TRADES = 50
ASIA, LONDON, NY = (18, 19, 20, 21, 22, 23, 0, 1), (2, 3, 4, 5, 6, 7), tuple(range(8, 16))

CLAIMS = {   # name: (market, what the post says, the post's rate for the level being reached, post id)
    "c01_sweep_reclaim_0800": ("NAS100", "8:00 candle sweeps the 7:00 low and closes back above it; the 9:00 candle takes the 8:00 high", 0.859, "2121347390456443239"),
    "c02_hour_sweep_reclaim": ("NAS100", "1H candle sweeps the prior low (high) and closes back inside; the next hour takes its high (low)", 0.604, "2107087504218452357"),
    "c03_hour_sweep_continue": ("NAS100", "1H candle sweeps the prior low (high) and closes beyond it; the next hour takes that low (high) again", 0.675, "2107087504218452357"),
    "c04_wide_breakout_holds": ("NAS100", "wide 1H candle breaks the prior high (low) and closes beyond; the next hour leaves its low (high) alone", 0.132, "2122434552027312558"),
    "c05_friday_last_hour": ("NAS100", "Friday: the 16:00 hour leaves the 15:00 high alone", 0.151, "2110981587475349781"),
    "c06_red_morning": ("NAS100", "red 9:30-11:59 morning; the 13:30-15:59 afternoon leaves the morning high alone", 0.145, "2118372793083732293"),
    "c07_asia_low_taken_below_opens": ("NAS100", "London took the Asia low, 9:30 open below the midnight and 18:00 opens; the Asia high survives", 0.256, "2121271896281059710"),
    "c08_dow_expansion_below_pdl": ("USA30", "London expanded past an Asia side, 9:30 open below yesterday's low; the overnight high survives", 0.167, "2121709773557289321"),
    "c09_quiet_london_above_pdh": ("NAS100", "narrow London, 9:30 open above yesterday's high; yesterday's New York low survives", 0.032, "2122721451765850502"),
    "c10_prior_low_only_bearish_london": ("NAS100", "yesterday took only the prior day's low, London red; the overnight low is taken after 8:00", 0.888, "2114620555794305292"),
    "c11_wide_day_untouched": ("NAS100", "wide day yesterday, neither of its ends taken by 8:00; the overnight high is taken after 8:00", 0.866, "2112793523636596754"),
    "c12_gold_below_two_opens": ("XAUUSD", "gold at 8:00 below yesterday's open and the midnight open; the overnight high survives", 0.132, "2123808611596177583"),
    "c13_weekday_direction": ("NAS100", "9:30 to the close: long Monday, Tuesday, Friday; short Wednesday, Thursday", None, "2106451718431187258"),
}
HOLD = {"c05_friday_last_hour", "c12_gold_below_two_opens"}       # hourly bars only: stop at the level, out at the end
TOWARD = {"c01_sweep_reclaim_0800", "c02_hour_sweep_reclaim", "c03_hour_sweep_continue", "c10_prior_low_only_bearish_london", "c11_wide_day_untouched"}
WEEKDAY_SIDE = {0: 1, 1: 1, 2: -1, 3: -1, 4: 1}


def binom_tail(k, n, p=0.5):
    """Chance of k or more successes in n tries."""
    if not n:
        return float("nan")
    logs = [math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) + i * math.log(p) + (n - i) * math.log(1 - p) for i in range(k, n + 1)]
    return float(min(1.0, sum(math.exp(x) for x in logs)))


class Market:
    """Hourly bars for the whole day and minute bars from 8:00 or 9:00, by trading day (18:00 the evening before to 17:00)."""

    def __init__(self, mn, hr, minute_from=None):
        ny = hr["time"].dt.tz_convert("America/New_York").dt.tz_localize(None)
        self.ht = ny.to_numpy(); self.hb = hr[["open", "high", "low", "close"]].to_numpy(float)
        tday = (ny + pd.Timedelta(hours=6)).dt.date.to_numpy(); hour = ny.dt.hour.to_numpy()
        self.H = {}; self.hidx = {}
        for i, (d, h) in enumerate(zip(tday, hour)):
            self.H.setdefault(d, {})[int(h)] = self.hb[i]; self.hidx[(d, int(h))] = i
        self.M = {}; self.first = {}
        if mn is not None:
            mny = mn["time"].dt.tz_convert("America/New_York").dt.tz_localize(None)
            mod = (mny.dt.hour * 60 + mny.dt.minute).to_numpy()
            lo = M0 if minute_from is None else minute_from
            keep = (mod >= lo) & (mod < M1)
            day = mny.dt.date.to_numpy()[keep]; mod = mod[keep]; arr = mn[["open", "high", "low", "close"]].to_numpy(float)[keep]
            bounds = np.r_[0, np.flatnonzero(day[1:] != day[:-1]) + 1, len(day)]
            for a, b in zip(bounds[:-1], bounds[1:]):
                x = np.full((M1 - M0, 4), np.nan); x[mod[a:b] - M0] = arr[a:b]
                self.M[day[a]] = x; self.first[day[a]] = int(mod[a])
        self.days = sorted(d for d, hs in self.H.items() if len(hs) >= 20 and sum(h in hs for h in LONDON) >= 5 and sum(h in hs for h in ASIA) >= 6)
        self.prev = {d: p for p, d in zip(self.days[:-1], self.days[1:])}
        self.S = {d: self._sessions(d) for d in self.days}

    def _agg(self, d, hours):
        b = [self.H[d][h] for h in hours if h in self.H[d]]
        return dict(o=b[0][0], h=max(x[1] for x in b), l=min(x[2] for x in b), c=b[-1][3]) if b else None

    def _sessions(self, d):
        s = dict(asia=self._agg(d, ASIA), london=self._agg(d, LONDON), ny=self._agg(d, NY), day=self._agg(d, ASIA + LONDON + NY + (16,)))
        s["on_h"] = max(s["asia"]["h"], s["london"]["h"]); s["on_l"] = min(s["asia"]["l"], s["london"]["l"])
        s["mid"] = self.H[d][0][0] if 0 in self.H[d] else None
        return s

    def rth_ok(self, d):
        return d in self.M and (~np.isnan(self.M[d][RTH0 - M0:RTH1 - M0, 1])).sum() >= 370 and not np.isnan(self.M[d][RTH0 - M0, 0])

    def path(self, d, start, end, hourly_only=False):
        """Bars from start to end as (minute, open, high, low, close, kind): minute bars where the day has them, hourly bars before."""
        bars = []; t = start; first = 10 ** 9 if hourly_only else self.first.get(d, 10 ** 9)
        while t < end:
            if first <= t < M1:
                x = self.M[d][t - M0]
                if not np.isnan(x[1]):
                    bars.append((t, x[0], x[1], x[2], x[3], "m"))
                t += 1
            else:
                if t % 60:
                    return None
                x = self.H[d].get(t // 60)
                if x is not None:
                    bars.append((t, x[0], x[1], x[2], x[3], "h"))
                t += 60
        return bars if bars and bars[0][0] == start else None


def bracket(bars, L, toward, cost, hold=False):
    """First touch of the level L against the phantom level the same distance on the other side of the first open, and the trade.
    hold=True is for claims that only have hourly bars: stop at the level, no target, out at the end of the window."""
    P = bars[0][1]
    if L == P:
        return None
    up = L > P; d = abs(L - P); hi, lo = (L, 2 * P - L) if up else (2 * P - L, L)
    first = None; px = None; touched = False; lpx = None
    for i, (t, o, h, l, c, k) in enumerate(bars):
        if first is None:
            if i > 0 and o >= hi: first, px = "hi", o
            elif i > 0 and o <= lo: first, px = "lo", o
            else:
                a, b = h >= hi, l <= lo
                if a and b: first = "both"
                elif a: first, px = "hi", hi
                elif b: first, px = "lo", lo
        if not touched and (h >= L if up else l <= L):
            touched = True; lpx = o if (i > 0 and (o >= L if up else o <= L)) else L      # the price a stop at the level would get
    level_first = None if first in (None, "both") else ((first == "hi") == up)
    side = 1 if (toward == up) else -1                      # toward an upper level or away from a lower one is a long
    rec = dict(touched=bool(touched), first="neither" if first is None else ("same_bar" if first == "both" else ("level" if level_first else "phantom")),
               dist_pct=float(d / P * 100))
    if d / P < FLOOR:
        return rec
    if hold:
        px, how = (lpx, "stop") if touched else (bars[-1][4], "time")
    elif first == "both":
        return rec                                          # one hourly bar reached both sides: the order is unknown, so no trade is counted
    elif first is None: px, how = bars[-1][4], "time"
    else: how = "target" if (first == "hi") == (side == 1) else "stop"
    rec.update(r=float(side * (px - P) / d), cost=float(cost * P / d * (3 if how == "stop" else 2)), how=how)
    return rec


def med_prev(vals, i, n):
    x = [v for v in vals[max(0, i - n):i] if v is not None]
    return float(np.median(x)) if len(x) >= n // 2 else None


def events(name, mk):
    """Yields (date, in the claim's setup or not, bars, level) for one claim. Days outside the setup are the comparison group."""
    D = mk.days; S = mk.S
    rng = lambda s: s["h"] - s["l"]
    if name in ("c01_sweep_reclaim_0800", "c02_hour_sweep_reclaim", "c03_hour_sweep_continue", "c04_wide_breakout_holds"):
        hours = [9] if name.startswith("c01") else range(10, 16)
        hist = {h: [] for h in range(24)}                   # ranges of each hour on earlier days, for the "wide" test
        for d in D:
            Hd = mk.H[d]
            for n in hours:
                if not (mk.rth_ok(d) and n - 1 in Hd and n - 2 in Hd):
                    continue
                s, p = Hd[n - 1], Hd[n - 2]
                bars = mk.path(d, n * 60, n * 60 + 60)
                if not bars:
                    continue
                lo_sw, hi_sw = s[2] < p[2], s[1] > p[1]
                if name.startswith("c01"):
                    yield d, bool(lo_sw and not hi_sw and s[3] > p[2]), bars, s[1]
                elif lo_sw and hi_sw:
                    continue                                # a candle that swept both sides is left out
                elif name.startswith("c02"):
                    if lo_sw: yield d, bool(s[3] > p[2]), bars, s[1]
                    if hi_sw: yield d, bool(s[3] < p[1]), bars, s[2]
                elif name.startswith("c03"):
                    if lo_sw: yield d, bool(s[3] < p[2]), bars, s[2]
                    if hi_sw: yield d, bool(s[3] > p[1]), bars, s[1]
                else:
                    past = hist[n - 1][-20:]; wide = len(past) >= 10 and (s[1] - s[2]) > 1.3 * float(np.median(past))
                    if hi_sw and s[3] > p[1]: yield d, bool(wide), bars, s[2]
                    if lo_sw and s[3] < p[2]: yield d, bool(wide), bars, s[1]
            for h, b in Hd.items():
                hist[h].append(b[1] - b[2])
        return
    if name == "c05_friday_last_hour":
        for d in D:
            if 15 not in mk.H[d] or 16 not in mk.H[d]:
                continue
            i = mk.hidx[(d, 16)]
            if i < 24:
                continue
            tr = float(np.median(mk.hb[i - 24:i, 1] - mk.hb[i - 24:i, 2])); L = mk.H[d][15][1]
            if mk.H[d][16][0] >= L - 0.10 * tr:
                continue                                    # the post leaves out "free sweeps"
            yield d, d.weekday() == 4, mk.path(d, 960, 1020, hourly_only=True), L
        return
    lon_rng = [rng(S[d]["london"]) for d in D]; day_rng = [rng(S[d]["day"]) for d in D]
    for i, d in enumerate(D):
        p = mk.prev.get(d); pp = mk.prev.get(p) if p else None
        if p is None or pp is None:
            continue
        s, sp, spp = S[d], S[p], S[pp]
        if name == "c12_gold_below_two_opens":
            bars = mk.path(d, 480, 1020, hourly_only=True); tr = med_prev(day_rng, i, 24)
            if not bars or tr is None or s["mid"] is None:
                continue
            P = bars[0][1]
            yield d, bool(P < sp["day"]["o"] - 0.25 * tr and P < s["mid"] - 0.25 * tr), bars, s["on_h"]
            continue
        if not mk.rth_ok(d):
            continue
        if name == "c06_red_morning":
            m = mk.M[d][RTH0 - M0:720 - M0]; ok = ~np.isnan(m[:, 1]); bars = mk.path(d, 810, RTH1)
            if not bars or not ok.any():
                continue
            yield d, bool(m[ok][-1, 3] < m[0, 0]), bars, float(np.nanmax(m[:, 1]))
        elif name == "c07_asia_low_taken_below_opens":
            bars = mk.path(d, RTH0, RTH1)
            if not bars or s["mid"] is None:
                continue
            P = bars[0][1]
            yield d, bool(s["london"]["l"] < s["asia"]["l"] and P < s["mid"] and P < s["asia"]["o"]), bars, s["asia"]["h"]
        elif name == "c08_dow_expansion_below_pdl":
            bars = mk.path(d, RTH0, RTH1)
            if not bars:
                continue
            lo, a = s["london"], s["asia"]
            exp = (lo["h"] > a["h"] and lo["c"] > a["h"]) or (lo["l"] < a["l"] and lo["c"] < a["l"])
            yield d, bool(exp and bars[0][1] < sp["day"]["l"]), bars, s["on_h"]
        elif name == "c09_quiet_london_above_pdh":
            bars = mk.path(d, RTH0, RTH1); med = med_prev(lon_rng, i, 20)
            if not bars or med is None or sp["ny"] is None:
                continue
            yield d, bool(lon_rng[i] < 0.7 * med and bars[0][1] > sp["day"]["h"]), bars, sp["ny"]["l"]
        elif name == "c10_prior_low_only_bearish_london":
            bars = mk.path(d, 480, RTH1)
            if not bars:
                continue
            cond = sp["day"]["l"] < spp["day"]["l"] and sp["day"]["h"] <= spp["day"]["h"] and s["london"]["c"] < s["london"]["o"]
            yield d, bool(cond), bars, s["on_l"]
        elif name == "c11_wide_day_untouched":
            bars = mk.path(d, 480, RTH1); tr = med_prev(day_rng, i - 1, 24)
            if not bars or tr is None:
                continue
            cond = day_rng[i - 1] > 1.3 * tr and s["on_h"] < sp["day"]["h"] and s["on_l"] > sp["day"]["l"]
            yield d, bool(cond), bars, s["on_h"]


def summarise(rows, toward):
    n = len(rows)
    if n == 0:
        return dict(events=0)
    lvl = sum(r["first"] == "level" for r in rows); ph = sum(r["first"] == "phantom" for r in rows)
    good = lvl if toward else ph                            # the side the claim points to
    out = dict(events=n, level_reached_rate=float(np.mean([r["touched"] for r in rows])), level_first=lvl, phantom_first=ph,
               same_bar=sum(r["first"] == "same_bar" for r in rows), neither=sum(r["first"] == "neither" for r in rows),
               claim_side_share=float(good / (lvl + ph)) if lvl + ph else float("nan"), p_above_half=binom_tail(good, lvl + ph),
               median_dist_pct=float(np.median([r["dist_pct"] for r in rows])))
    tr = [r for r in rows if "r" in r]
    out["trade"] = trade_stats(tr, [r["r"] for r in tr], [r["cost"] for r in tr])
    if tr:
        out["trade"]["endings"] = {k: sum(r["how"] == k for r in tr) for k in ("target", "stop", "time")}
    return out


def trade_stats(tr, gross, cost):
    if len(tr) < 3:
        return dict(trades=len(tr))
    gross, cost = np.array(gross), np.array(cost); net = gross - cost
    wins, losses = net[net > 0], net[net <= 0]; by_year = {}
    for r, x in zip(tr, net):
        by_year[r["date"].year] = by_year.get(r["date"].year, 0.0) + float(x)
    sd = net.std(ddof=1)
    return dict(trades=len(net), mean=float(net.mean()), t=float(net.mean() / (sd / math.sqrt(len(net)))) if sd > 0 else float("nan"),
                pf=float(wins.sum() / -losses.sum()) if losses.sum() < 0 else float("inf"), win_rate=float((net > 0).mean()),
                mean_before_cost=float(gross.mean()), mean_double_cost=float((gross - 2 * cost).mean()), total=float(net.sum()),
                by_year={int(k): round(v, 2) for k, v in sorted(by_year.items())})


def run_claim(name, mk, cost):
    toward = name in TOWARD
    if name == "c13_weekday_direction":
        tr = []
        for d in mk.days:
            if not (START <= d <= END and mk.rth_ok(d) and d.weekday() in WEEKDAY_SIDE):
                continue
            bars = mk.path(d, RTH0, RTH1)
            tr.append(dict(date=d, r=WEEKDAY_SIDE[d.weekday()] * (bars[-1][4] - bars[0][1]) / bars[0][1] * 100, cost=2 * cost * 100))
        return dict(setup=dict(events=len(tr), trade=trade_stats(tr, [r["r"] for r in tr], [r["cost"] for r in tr])), unit="percent of price")
    setup, other = [], []
    for d, cond, bars, L in events(name, mk):
        if not (START <= d <= END) or not bars:
            continue
        rec = bracket(bars, L, toward, cost, hold=name in HOLD)
        if rec is None:
            continue
        rec["date"] = d
        (setup if cond else other).append(rec)
    return dict(setup=summarise(setup, toward), other_days=summarise(other, toward), unit="R")


def verdict_of(name, res):
    t = res["setup"].get("trade", {})
    trade_ok = bool(t.get("trades", 0) >= MIN_TRADES and t["mean"] > 0 and t["t"] >= Z_BAR and t["mean_double_cost"] > 0)
    if name == "c13_weekday_direction":
        return dict(trade_passes=trade_ok)
    s = res["setup"]
    side_ok = bool(s["events"] and s["claim_side_share"] > 0.5 and s["p_above_half"] <= P_BAR)
    return dict(claim_side_first_more_than_half=side_ok, trade_passes=trade_ok)


def load_market(m, dry_seed=None):
    if dry_seed is not None:
        mn, hr = data_io.load(m, fake_seed=dry_seed)
        return Market(mn, hr, minute_from=540), mn
    if m == "XAUUSD":
        hr = pd.read_csv(os.path.join(LAB, "data", "XAUUSD_1h.csv.gz")); hr["time"] = pd.to_datetime(hr["time"], utc=True)
        return Market(None, hr[hr["time"] >= costs.DATA_START].sort_values("time").reset_index(drop=True)), None
    mn, hr = data_io.load(m)
    return Market(mn, hr[hr["time"] >= costs.DATA_START].reset_index(drop=True)), mn


def check():
    """Made-up prices: every decided first touch on the mixed path must match a pure minute path."""
    mn, hr = data_io.load("NAS100", fake_seed=77)
    mixed = Market(mn, hr, minute_from=540)
    ny = mn["time"].dt.tz_convert("America/New_York").dt.tz_localize(None)
    mod = (ny.dt.hour * 60 + ny.dt.minute).to_numpy(); day = ny.dt.date.to_numpy(); arr = mn[["open", "high", "low", "close"]].to_numpy(float)
    by_day = {}
    for i in range(len(day)):
        by_day.setdefault(day[i], {})[int(mod[i])] = arr[i]
    n = bad = undecided = 0
    for name in CLAIMS:
        if name in ("c13_weekday_direction", "c05_friday_last_hour", "c12_gold_below_two_opens"):
            continue
        for d, cond, bars, L in events(name, mixed):
            if not bars or not cond:
                continue
            a = bracket(bars, L, name in TOWARD, 0.0)
            truth = [(t, *by_day[d][t], "m") for t in range(bars[0][0], bars[-1][0] + (60 if bars[-1][5] == "h" else 1)) if t in by_day.get(d, {})]
            if a is None or not truth or truth[0][1] != bars[0][1]:
                continue
            b = bracket(truth, L, name in TOWARD, 0.0); n += 1
            if a["first"] == "same_bar": undecided += 1
            elif a["first"] != b["first"]: bad += 1
    print(f"check: {n} setups compared, {bad} mismatches, {undecided} left undecided by an hourly bar")
    return bad == 0 and n > 500


def main():
    dry = "--dryrun" in sys.argv
    if "--check" in sys.argv:
        print("check passed" if check() else "CHECK FAILED"); return
    if os.path.exists(RESULTS) and not dry:
        print("Study 10 has already been run. It runs once. See lab/intraday/herman_claims_results.json."); return
    mks = {}; res = {}
    for k, m in enumerate(sorted({v[0] for v in CLAIMS.values()})):
        mks[m] = load_market(m, dry_seed=k + 31 if dry else None)[0]
    for name, (m, text, post_rate, post_id) in CLAIMS.items():
        r = run_claim(name, mks[m], 0.0 if dry else costs.COST[m])
        r.update(market=m, claim=text, post_rate_level_reached=post_rate, post=f"x.com/RHerman/status/{post_id}", checks=verdict_of(name, r))
        res[name] = r
        s = r["setup"]; t = s.get("trade", {})
        line = f"{name:36s} {m:7s} {s['events']:5d} events"
        if name != "c13_weekday_direction" and s["events"]:
            o = r["other_days"]
            line += (f" | level reached {s['level_reached_rate']*100:5.1f}% (post {post_rate*100:.1f}%) | claim side first {s['claim_side_share']*100:5.1f}% of "
                     f"{s['level_first'] + s['phantom_first']} decided (p {s['p_above_half']:.3f}; other days {o.get('claim_side_share', float('nan'))*100:.1f}%)")
        if t.get("trades", 0) >= 3:
            line += f" | trade: {t['trades']} trades, avg {t['mean']:+.3f} ({t['mean_before_cost']:+.3f} before costs), win {t['win_rate']*100:.0f}%, PF {t['pf']:.2f}, t {t['t']:+.2f}"
        print(line, "| PASS" if r["checks"]["trade_passes"] else "| no")
    passed = [n for n, r in res.items() if r["checks"]["trade_passes"]]
    print(f"claims whose trade passes: {len(passed)} of {N_TESTS}", passed)
    if dry:
        print("dry run on made-up prices with no cost: nothing written"); return
    today = datetime.date.today().isoformat()
    json.dump(dict(date=today, first_day=str(START), last_day=str(END), bar=dict(t=Z_BAR, p=P_BAR, min_trades=MIN_TRADES), passed=passed, claims=res),
              open(RESULTS, "w"), indent=1, default=str)
    with open(os.path.join(LAB, "JOURNAL.md"), "a") as j:
        j.write(f"\n### {today} · study 10 · thirteen claims from @RHerman · {len(passed)} of {N_TESTS} pass as a trade\n"
                f"- Source: posts on X by @RHerman, found in a scan of the account (about 1,400 posts back to August 2025). The posts give rates for a level being reached. "
                f"They give no entry, stop or cost, and most say so.\n"
                f"- Lab data: {START} to {END}. Hourly bars for the whole day, 1-minute bars from 8:00 or 9:00 New York time. Costs from `costs.py`. "
                f"Test for each level claim: is the level reached before a phantom level the same distance on the other side, and does trading the claim's side pay after costs. "
                f"Bar for a trade: at least {MIN_TRADES} trades, average above zero, t-stat {Z_BAR} or more, still above zero at double cost.\n")
        for name, r in res.items():
            s = r["setup"]; t = s.get("trade", {})
            txt = f"- `{name}` ({r['market']}): {r['claim']}. {s['events']} events."
            if name != "c13_weekday_direction" and s["events"]:
                txt += (f" Level reached on {s['level_reached_rate']*100:.1f}% (post: {r['post_rate_level_reached']*100:.1f}%). The claim's side came first on {s['claim_side_share']*100:.1f}% of "
                        f"{s['level_first'] + s['phantom_first']} decided events (p {s['p_above_half']:.3f}); on other days {r['other_days'].get('claim_side_share', float('nan'))*100:.1f}%.")
            if t.get("trades", 0) >= 3:
                txt += (f" Trade: {t['trades']} trades, average {t['mean']:+.3f} {r['unit']} after costs ({t['mean_before_cost']:+.3f} before), win rate {t['win_rate']*100:.0f}%, "
                        f"profit factor {t['pf']:.2f}, t-stat {t['t']:.2f}.")
            j.write(txt + (" PASS.\n" if r["checks"]["trade_passes"] else " No pass.\n"))
    print("written to lab/intraday/herman_claims_results.json and the journal")


if __name__ == "__main__":
    main()
