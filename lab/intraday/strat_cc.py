"""Study 11: the 1-hour and 15-minute "CC" setups from a post by @tradermike1234 on X. 8 registered scenarios on 1-minute bars. One run.

Run from the repo root:
    python lab/intraday/strat_cc.py --check     # hand-built days, a plain minute-by-minute version, and a look-ahead test, all on made-up prices
    python lab/intraday/strat_cc.py --dryrun    # same code on made-up prices with no cost; nothing is written
    python lab/intraday/strat_cc.py             # the one real run; refuses to run a second time

The rules are in LAB_RULES.md under "Study 11". They were written before this rule was run on any lab data.
Source of the rule: x.com/tradermike1234/status/2125172071374237862 (November 24, 2026), two images of written steps.
The code below is the lab's own. Every choice the post leaves open is either a scenario part or is named in the rules.

Everything is written for the short side: a candle closes below the prior candle's low, its low is the target,
a smaller candle pokes above the candle before it and closes lower, and the trade is sold with the stop as far above as the target is below.
The long side runs the same code on prices turned upside down.
"""
import sys, os, json, datetime, itertools
from statistics import NormalDist
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.join(HERE, "..")
sys.path.insert(0, HERE); sys.path.insert(0, LAB)
import sweep_fvg as data_io                                  # study 8's loader, made-up prices and counting
import costs

RESULTS = os.path.join(HERE, "strat_cc_results.json")
MARKETS = ["NAS100", "SPX500", "USA30"]
START, SPLIT, END = datetime.date(2021, 6, 1), datetime.date(2024, 1, 1), datetime.date(2026, 11, 19)
M0, NMIN, FLAT = 9 * 60, 435, 415                           # minute bars are used from 9:00 New York time; 15:55 is minute 415
PRE_MIN, SES_MIN = 27, 370                                  # a day needs 27 of the 30 minutes before 9:30 and 370 of the 385 from 9:30 to 15:54
GAP_K = 0.25                                                # smallest 1-minute gap, in average 1-minute ranges (the lab's fair_value_gap floor)
MIN_RISK = 4.0                                              # no trade if the risk is under 4 round-trip costs (cost above 0.25R)
H1_BIAS = (0, 60, 120, 180, 240, 300)                       # 1-hour model: the candle after the setup starts at 9:00 ... 14:00
M15_BIAS = tuple(range(30, 346, 15))                        # 15-minute model: the candle after the setup starts at 9:30 ... 14:45
S, C = data_io.S, data_io.C
SCENARIOS = ([dict(model="h1", timing=t, stop=s) for t, s in itertools.product(("early", "any"), ("plain", "minstop"))] +
             [dict(model="m15", setup=k, timing=t) for k, t in itertools.product(("two", "twothree"), ("early", "any"))])
NAN = float("nan")


def name(v):
    return f"h1.{v['timing']}.{v['stop']}" if v["model"] == "h1" else f"m15.{v['setup']}.{v['timing']}"


# ---------------------------------------------------------------- data

def prepare(mn, hr):
    """One record per usable day: minute arrays from 9:00 and the 7:00 and 8:00 hourly candles."""
    ny = hr["time"].dt.tz_convert("America/New_York").dt.tz_localize(None)
    hday, hhour = ny.dt.normalize().to_numpy(), ny.dt.hour.to_numpy()
    hv = hr[["open", "high", "low", "close"]].to_numpy(float)
    pre = {}
    for i in np.flatnonzero((hhour == 7) | (hhour == 8)):
        pre[(hday[i], int(hhour[i]))] = tuple(hv[i])
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
        if have[:30].sum() < PRE_MIN or have[30:FLAT].sum() < SES_MIN:
            continue                                         # a day with too few bars is skipped for this market
        out.append(dict(date=date, o=arr[0], h=arr[1], l=arr[2], c=arr[3], h7=pre.get((D, 7)), h8=pre.get((D, 8))))
    return out


def flip(d):
    """The same day upside down, so the long side can use the short-side code."""
    f = lambda k: None if k is None else (-k[0], -k[2], -k[1], -k[3])
    return dict(date=d["date"], o=-d["o"], h=-d["l"], l=-d["h"], c=-d["c"], h7=f(d["h7"]), h8=f(d["h8"]))


def candles(d, tf):
    """Candles of tf minutes from 9:00: open, high, low, close, complete. A candle with a missing minute is not complete."""
    nb = NMIN // tf
    O, H, L, Cl = (d[k][:nb * tf].reshape(nb, tf) for k in ("o", "h", "l", "c"))
    ok = ~np.isnan(H).any(axis=1)
    with np.errstate(invalid="ignore"):
        return dict(o=np.where(ok, O[:, 0], NAN), h=np.where(ok, np.nanmax(np.where(np.isnan(H), -np.inf, H), axis=1), NAN),
                    l=np.where(ok, np.nanmin(np.where(np.isnan(L), np.inf, L), axis=1), NAN), c=np.where(ok, Cl[:, -1], NAN), ok=ok)


# ---------------------------------------------------------------- the rule, short side

def is_setup(prev, cur, allow3):
    """cur closes below prev's low. A 2 has not traded above prev's high; a 3 has. Each is (open, high, low, close)."""
    if prev is None or cur is None or any(x != x for x in prev) or any(x != x for x in cur):
        return False
    return cur[2] < prev[2] and cur[3] < prev[2] and (allow3 or cur[1] <= prev[1])


def setups(d, model, allow3, cs):
    """All short setups of the day: (first minute of the candle after the setup, its last minute + 1, target)."""
    out = []
    if model == "h1":
        c60 = cs[60]; hour = lambda k: (c60["o"][k], c60["h"][k], c60["l"][k], c60["c"][k]) if c60["ok"][k] else None
        for s in H1_BIAS:
            k = s // 60 - 1                                  # the setup candle, counted in hours from 9:00; -1 is the 8:00 candle
            cur = d["h8"] if k == -1 else hour(k)
            prev = d["h7"] if k == -1 else d["h8"] if k == 0 else hour(k - 1)
            if is_setup(prev, cur, False):
                out.append((s, s + 60, cur[2]))
    else:
        c15 = cs[15]; q = lambda k: (c15["o"][k], c15["h"][k], c15["l"][k], c15["c"][k]) if c15["ok"][k] else None
        for s in M15_BIAS:
            k = s // 15 - 1
            if is_setup(q(k - 1), q(k), allow3):
                out.append((s, s + 15, q(k)[2]))
    return out


def confirm(d, cs, tf, s, e, early, T):
    """The first smaller candle inside [s, e) that trades above the candle before it, not below it, and closes below its own open
    and below that candle's high. Returns None, or (first minute after it, its first minute). The target must not trade first."""
    c = cs[tf]; j0 = s // tf; n = (e - s) // tf
    last = j0 + (n // 2 if tf == 15 else 1) if early else j0 + n     # early: the first half hour, or the first 5 minutes
    for j in range(j0, last):
        with np.errstate(invalid="ignore"):
            if np.nanmin(d["l"][s:(j + 1) * tf]) <= T:
                return None                                  # the target traded before any confirmation: the setup is over
        if j >= 1 and c["ok"][j] and c["ok"][j - 1] and c["h"][j] > c["h"][j - 1] and c["l"][j] >= c["l"][j - 1] \
                and c["c"][j] < c["o"][j] and c["c"][j] < c["h"][j - 1]:
            return (j + 1) * tf, j * tf
    return None


def entry_1m(d, avg, t0, e, f2, s, T):
    """1-hour model: the first minute from t0 to the end of the hour that closes below the latest 1-minute swing low,
    with a down gap already formed. Swing lows and gaps are looked for from the first minute of the 15-minute confirmation candle.
    Returns the signal minute, or None."""
    h, l, c = d["h"], d["l"], d["c"]
    gap_at = None                                            # the minute at which the first down gap is complete
    for a in range(f2, e - 2):
        g = l[a] - h[a + 2]
        if g > 0 and avg[a] == avg[a] and g >= GAP_K * avg[a] and h[a + 1] == h[a + 1]:
            gap_at = a + 2; break
    with np.errstate(invalid="ignore"):
        if np.nanmin(l[s:t0]) <= T:
            return None
    for i in range(t0, e):
        if l[i] != l[i]:
            continue
        if l[i] <= T:
            return None                                      # the target traded before an entry: the setup is over
        if gap_at is None or gap_at > i:
            continue
        for q in range(i - 2, f2, -1):                       # the latest swing low that was complete before minute i
            if l[q] < l[q - 1] and l[q] < l[q + 1]:
                if c[i] < l[q]:
                    return i
                break
    return None


def manage(d, f, entry, stop, T, at_open):
    """A short from minute f. Returns (fill minute, exit minute, R before cost, how it ended)."""
    o, h, l, c = d["o"], d["h"], d["l"], d["c"]; R = entry - T
    if h[f] >= stop:
        return (f, f, -1.0, "stop" if at_open else "stop_fill_minute")       # a fill minute that reaches the stop is a loss
    if at_open and l[f] <= T:
        return (f, f, 1.0, "target")
    oo, hh, ll = o[f + 1:FLAT], h[f + 1:FLAT], l[f + 1:FLAT]
    with np.errstate(invalid="ignore"):
        ev = np.flatnonzero((oo >= stop) | (hh >= stop) | (oo <= T) | (ll <= T))
    if len(ev):
        j = int(ev[0]); x = f + 1 + j
        if oo[j] >= stop: return (f, x, float((entry - oo[j]) / R), "stop")
        if oo[j] <= T: return (f, x, float((entry - oo[j]) / R), "target")
        if hh[j] >= stop: return (f, x, -1.0, "stop")        # a minute that reaches both counts as a stop
        return (f, x, 1.0, "target")
    if o[FLAT] == o[FLAT]:
        return (f, FLAT, float((entry - o[FLAT]) / R), "time")
    last = np.flatnonzero(~np.isnan(c[f:FLAT]))
    return (f, FLAT, float((entry - c[f + int(last[-1])]) / R), "time")


def place(d, f, T, Smin, minstop, floor, skips):
    """Sell at the open of minute f if the 1:1 stop clears Smin (or always, when minstop is off). Otherwise rest a sell order
    halfway between Smin and the target. Returns None, or (fill, exit, R, how, entry, risk)."""
    o, h, l = d["o"], d["h"], d["l"]
    if f >= FLAT or o[f] != o[f]:
        return None
    p = o[f]
    if not p > T:
        return None
    mid = (Smin + T) / 2 if minstop else -np.inf
    if p >= mid:
        R = p - T
        if R < floor * abs(p):
            skips[0] += 1; return None
        return manage(d, f, p, p + R, T, True) + (p, R)
    if mid - T < floor * abs(mid):
        skips[0] += 1; return None
    for g in range(f, FLAT):
        if o[g] != o[g]:
            continue
        if g > f and o[g] >= mid:                            # opened above the order: filled at the open, stop still 1:1
            R = o[g] - T
            return manage(d, g, o[g], o[g] + R, T, True) + (o[g], R)
        if l[g] <= T:
            return None                                      # the target traded first, or in the same minute: no trade
        if h[g] >= mid:
            return manage(d, g, mid, Smin, T, False) + (mid, mid - T)
    return None


def with_parts(d):
    d["cs"] = {tf: candles(d, tf) for tf in (5, 15, 60)}
    d["avg"] = data_io.make_bars(d["h"], d["l"], 1)["avg"]
    return d


def run_market(days, cost_rate, floor_rate=None):
    """Trades of every scenario for one market: {scenario: [(date, R before cost, cost in R, side, how)]}, and skipped small trades."""
    out = {name(v): [] for v in SCENARIOS}; small = {name(v): 0 for v in SCENARIOS}
    fr = cost_rate if floor_rate is None else floor_rate
    for d in days:
        sides = ((with_parts(dict(d)), -1), (with_parts(flip(d)), 1))
        for v in SCENARIOS:
            cands = []; sk = [0]
            for sd, side in sides:
                cands += [c + (side,) for c in day_candidates(sd, v, cost_rate, fr, sk)]
            small[name(v)] += sk[0]
            cands.sort(key=lambda c: (c[0], c[2]))
            busy_until = -1
            for f, x, s, r, cost, how, side in cands:        # one trade at a time per market
                if f > busy_until:
                    out[name(v)].append((d["date"], r, cost, side, how)); busy_until = x
    return out, small


def day_candidates(d, v, cost_rate, floor_rate, skips):
    """Every trade the scenario could take on one side of one day: (fill, exit, setup minute, R, cost in R, how).
    The small-trade floor comes from floor_rate, so the dry run (no cost) keeps the same floor."""
    cs = d["cs"]; out = []; floor = MIN_RISK * 2 * floor_rate
    for s, e, T in setups(d, v["model"], v.get("setup") == "twothree", cs):
        cf = confirm(d, cs, 15 if v["model"] == "h1" else 5, s, e, v["timing"] == "early", T)
        if cf is None:
            continue
        t0, f2 = cf
        if v["model"] == "h1":
            i = entry_1m(d, d["avg"], t0, e, f2, s, T)
            if i is None:
                continue
            f = i + 1
            with np.errstate(invalid="ignore"):
                Smin = float(np.nanmax(d["h"][f2:f]))
            tr = place(d, f, T, Smin, v["stop"] == "minstop", floor, skips)
        else:
            tr = place(d, t0, T, float(cs[5]["h"][f2 // 5]), True, floor, skips)
        if tr is None:
            continue
        f, x, r, how, entry, R = tr
        out.append((f, x, s, r, cost_rate * abs(entry) / R * (3 if how.startswith("stop") else 2), how))
    return out


# ---------------------------------------------------------------- a plain version of the same rule, for --check

def reference_candidates(d, v, floor):
    """One scenario on one side of one day, one minute at a time, with no array shortcuts. Returns [(fill, exit, setup minute, R, how)]."""
    o, h, l, c = d["o"], d["h"], d["l"], d["c"]
    ok = lambda i: h[i] == h[i]

    def cndl(a, b):                                          # candle over minutes a .. b-1, or None if a minute is missing
        if a < 0 or any(not ok(i) for i in range(a, b)):
            return None
        return (o[a], max(h[i] for i in range(a, b)), min(l[i] for i in range(a, b)), c[b - 1])

    big = 60 if v["model"] == "h1" else 15; small = 15 if v["model"] == "h1" else 5
    out = []
    for s in (H1_BIAS if v["model"] == "h1" else M15_BIAS):
        cur = d["h8"] if (big == 60 and s == 0) else cndl(s - big, s)
        prev = d["h7"] if (big == 60 and s == 0) else d["h8"] if (big == 60 and s == 60) else cndl(s - 2 * big, s - big)
        if prev is None or cur is None:
            continue
        if not (cur[2] < prev[2] and cur[3] < prev[2]):
            continue
        if cur[1] > prev[1] and not (v["model"] == "m15" and v["setup"] == "twothree"):
            continue
        T = cur[2]; e = s + big
        n_small = (2 if big == 60 else 1) if v["timing"] == "early" else big // small
        state = "confirm"; f2 = t0 = None; order = None; pos = None; res = None; run_hi = -np.inf; gap_done = False
        for i in range(s, FLAT + 1):
            if i == FLAT:
                if pos is not None:
                    entry, stop, R, f = pos
                    px = o[i] if o[i] == o[i] else last_close
                    res = (f, FLAT, (entry - px) / R, "time")
                break
            if not ok(i):
                continue
            if state == "confirm":
                if l[i] <= T:
                    break
                if (i + 1) % small == 0 and (i + 1 - small) >= s and (i + 1 - s) // small <= n_small:
                    a = i + 1 - small; k = cndl(a, i + 1); kp = cndl(a - small, a)
                    if k is not None and kp is not None and k[1] > kp[1] and k[2] >= kp[2] and k[3] < k[0] and k[3] < kp[1]:
                        f2, t0 = a, i + 1; run_hi = k[1]
                        state = "entry" if v["model"] == "h1" else "place"
                if state == "confirm" and i + 1 >= s + n_small * small:
                    break
                continue
            if state == "entry":                             # 1-hour model: wait for the 1-minute signal
                if i >= e or l[i] <= T:
                    break
                run_hi = max(run_hi, h[i])
                sig = False
                gap_ok = False
                for a in range(f2, i - 1):                   # a down gap whose third minute is i or earlier
                    if ok(a) and ok(a + 1) and ok(a + 2) and l[a] - h[a + 2] > 0:
                        prior = [h[x] - l[x] for x in range(max(0, a - 24), a) if ok(x)]
                        if len(prior) >= 6 and l[a] - h[a + 2] >= GAP_K * (sum(prior) / len(prior)):
                            gap_ok = True; break
                if gap_ok:
                    for q in range(i - 2, f2, -1):
                        if ok(q - 1) and ok(q) and ok(q + 1) and l[q] < l[q - 1] and l[q] < l[q + 1]:
                            sig = c[i] < l[q]; break
                if sig:
                    state = "place"; t0 = i + 1
                continue
            if state == "place":                             # the open of the minute after the signal or confirmation
                if i != t0:
                    break                                    # that minute is missing
                p = o[i]
                if not p > T:
                    break
                minstop = v["model"] == "m15" or v["stop"] == "minstop"
                mid = (run_hi + T) / 2
                if not minstop or p >= mid:
                    R = p - T
                    if R < floor * abs(p):
                        break
                    pos = (p, p + R, R, i); state = "trade"
                    if h[i] >= p + R: res = (i, i, -1.0, "stop"); break
                    if l[i] <= T: res = (i, i, 1.0, "target"); break
                    last_close = c[i]; continue
                if mid - T < floor * abs(mid):
                    break
                order = mid; state = "order"
                # the order can fill in this same minute, checked below
            if state == "order":
                if i > t0 and o[i] >= order:
                    R = o[i] - T; pos = (o[i], o[i] + R, R, i); state = "trade"
                    if h[i] >= o[i] + R: res = (i, i, -1.0, "stop"); break
                    if l[i] <= T: res = (i, i, 1.0, "target"); break
                    last_close = c[i]; continue
                if l[i] <= T:
                    break
                if h[i] >= order:
                    R = order - T; pos = (order, run_hi, R, i); state = "trade"
                    if h[i] >= run_hi: res = (i, i, -1.0, "stop_fill_minute"); break
                    last_close = c[i]
                continue
            if state == "trade":
                entry, stop, R, f = pos
                if o[i] >= stop or o[i] <= T: res = (f, i, (entry - o[i]) / R, "stop" if o[i] >= stop else "target"); break
                if h[i] >= stop: res = (f, i, -1.0, "stop"); break
                if l[i] <= T: res = (f, i, 1.0, "target"); break
                last_close = c[i]
        if res is not None:
            out.append((res[0], res[1], s, float(res[2]), res[3]))
    return out


def hand_built():
    """Four days written by hand, each with a known answer."""
    def day(path, h7=None, h8=None):
        """path: {minute: (open, high, low, close)}; missing minutes repeat the last close as a flat bar."""
        o = np.zeros(NMIN); h = np.zeros(NMIN); l = np.zeros(NMIN); c = np.zeros(NMIN); last = path[0][3] if 0 in path else 100.0
        for i in range(NMIN):
            if i in path: o[i], h[i], l[i], c[i] = path[i]; last = c[i]
            else: o[i] = h[i] = l[i] = c[i] = last
        return with_parts(dict(date=None, o=o, h=h, l=l, c=c, h7=h7, h8=h8))
    v_m15 = dict(model="m15", setup="two", timing="early"); bad = 0

    # 1. 15-minute model, resting order. 9:00 candle 100..110. 9:15 candle falls to 95 and closes 97: setup, target 95.
    #    9:25-9:29 highs up to 98. 9:30-9:34 pokes to 99 and closes 97.0, below its open 97.6: failed 2. The midpoint of 99 and 95 is 97.0.
    #    9:35 opens at 97.0, so it is sold at the open: risk 2, stop 99. Target 95 is hit at 9:36.
    p = {0: (105, 110, 100, 105), 15: (105, 105, 104, 104), 20: (104, 104, 95, 96), 25: (96, 98, 96, 97.6),
         30: (97.6, 99, 97.5, 98), 34: (98, 98, 97, 97.0), 35: (97.0, 97.2, 96.5, 96.6), 36: (96.6, 96.7, 94.9, 95.2)}
    got = day_candidates(day(p), v_m15, 0.0, 0.0, [0])
    want = [(35, 36, 30, 1.0, 0.0, "target")]
    if got != want: bad += 1; print("HAND 1", got, "wanted", want)

    # 2. Same day, but 9:35 opens at 96.4, below the midpoint 97.0: a sell order rests at 97.0, fills at 9:37, stop 99, target 95.
    p2 = dict(p); p2[34] = (98, 98, 96.4, 96.4); p2[35] = (96.4, 96.8, 96.2, 96.5); p2[36] = (96.5, 96.9, 96.3, 96.8)
    p2[37] = (96.8, 97.3, 96.7, 97.1); p2[38] = (97.1, 99.2, 97.0, 99.1)
    got = day_candidates(day(p2), v_m15, 0.0, 0.0, [0])
    want = [(37, 38, 30, -1.0, 0.0, "stop")]
    if got != want: bad += 1; print("HAND 2", got, "wanted", want)

    # 3. Same as 2, but the target 95 trades at 9:36 before the order fills: no trade.
    p3 = dict(p2); p3[36] = (96.5, 96.6, 94.9, 96.0)
    got = day_candidates(day(p3), v_m15, 0.0, 0.0, [0])
    if got != []: bad += 1; print("HAND 3", got, "wanted []")

    # 4. 1-hour model. 7:00 candle low 100, 8:00 candle falls to 95 and closes 97 without trading above the 7:00 high: setup, target 95.
    #    9:00-9:14 quiet near 97. 9:15-9:29 pokes to 98.5 and closes 97.2 under its open 97.6: failed 2 on the 15-minute chart.
    #    From 9:15: swing low 97.1 at 9:20; a down gap is complete at 9:30; 9:31 closes 96.65 below the swing low: signal. 9:32 opens 96.65.
    #    plain: sell 96.65, risk 1.65, stop 98.3, target hit at 9:35.
    #    minstop: the stop must clear 98.5, so the midpoint is 96.75; the order rests there, fills at 9:34, target hit at 9:35.
    q = {i: (97.0, 97.3, 96.9, 97.0) for i in range(0, 15)}
    q.update({15: (97.6, 98.5, 97.4, 97.5), 16: (97.5, 97.6, 97.3, 97.4), 19: (97.4, 97.5, 97.3, 97.3), 20: (97.3, 97.4, 97.1, 97.3),
              21: (97.3, 97.5, 97.2, 97.4), 29: (97.4, 97.4, 97.2, 97.2), 30: (97.2, 97.25, 97.15, 97.15), 31: (97.15, 97.15, 96.6, 96.65),
              32: (96.65, 96.7, 96.55, 96.6), 33: (96.6, 96.7, 96.5, 96.6), 34: (96.6, 96.8, 96.5, 96.7), 35: (96.7, 96.7, 94.9, 95.0)})
    d4 = day(q, h7=(101, 103, 100, 101), h8=(101, 102, 95, 97))
    got = day_candidates(d4, dict(model="h1", timing="early", stop="plain"), 0.0, 0.0, [0])
    want = [(32, 35, 0, 1.0, 0.0, "target")]
    if got != want: bad += 1; print("HAND 4 plain", got, "wanted", want)
    got = day_candidates(d4, dict(model="h1", timing="early", stop="minstop"), 0.0, 0.0, [0])
    want = [(34, 35, 0, 1.0, 0.0, "target")]
    if got != want: bad += 1; print("HAND 4 minstop", got, "wanted", want)
    # 5. The same day upside down must give the same trades on the long side.
    got = day_candidates(with_parts(flip(with_parts(flip(d4)))), dict(model="h1", timing="early", stop="minstop"), 0.0, 0.0, [0])
    if got != want: bad += 1; print("HAND 5 flip", got, "wanted", want)
    print(f"hand-built days: {bad} wrong of 6")
    return bad == 0


def check():
    """Hand-built days, the fast code against the plain version, and a look-ahead test, all on made-up prices."""
    ok = hand_built()
    mn, hr = data_io.load("X", fake_seed=7); days = prepare(mn, hr)[:400]
    floor = MIN_RISK * 2 * 0.00005
    bad = n = 0; trades = []
    for d in days:
        for sd, side in ((with_parts(dict(d)), -1), (with_parts(flip(d)), 1)):
            for v in SCENARIOS:
                fast = [(f, x, s, round(r, 9), how) for f, x, s, r, cost, how in day_candidates(sd, v, 0.00005, 0.00005, [0])]
                ref = [(f, x, s, round(r, 9), how) for f, x, s, r, how in reference_candidates(sd, v, floor)]
                n += len(ref)
                if fast != ref:
                    bad += 1
                    if bad <= 8: print("MISMATCH", name(v), d["date"], side, "plain:", ref, "fast:", fast)
                trades += [(sd, v, t) for t in fast]
    print(f"plain version: {len(days)} days x 2 sides x {len(SCENARIOS)} scenarios, {n} trades, {bad} mismatches")
    rng = np.random.default_rng(3); peek = 0
    for sd, v, t in trades[::7]:                             # change every price after the fill minute: the fill must not move
        f = t[0]; d2 = dict(sd)
        for k in ("o", "h", "l", "c"):
            d2[k] = sd[k].copy()
        noise = sd["c"][f] * (1 + np.cumsum(rng.normal(0, 0.0004, NMIN - f - 1)))
        d2["o"][f + 1:] = noise; d2["c"][f + 1:] = noise; d2["h"][f + 1:] = noise * 1.0002; d2["l"][f + 1:] = noise * 0.9998
        d2 = with_parts(d2)
        again = [x for x in day_candidates(d2, v, 0.00005, 0.00005, [0]) if x[2] == t[2]]
        if not again or again[0][0] != f:
            peek += 1
    print(f"look-ahead test: {len(trades[::7])} trades re-run with every later price changed, {peek} fills moved")
    return ok and bad == 0 and peek == 0


# ---------------------------------------------------------------- counting

def stats(tr, cost_mult=1.0):
    s = data_io.stats(tr, cost_mult)
    if "t" in s:
        s["win_rate_before_cost"] = float((tr["r"] > 0).mean() * 100)
        s["trades_per_traded_day"] = float(len(tr) / s["days"])
    return s


def main():
    if "--check" in sys.argv:
        sys.exit(0 if check() else 1)
    dry = "--dryrun" in sys.argv
    if os.path.exists(RESULTS) and not dry:
        print("Study 11 has already been run. It runs once. See lab/intraday/strat_cc_results.json."); return
    assert len(SCENARIOS) == 8
    per = {}; n_days = {}; small = {name(v): 0 for v in SCENARIOS}
    for k, m in enumerate(MARKETS):
        mn, hr = data_io.load(m, fake_seed=k + 11 if dry else None)
        if not dry:
            hr = hr[hr["time"] >= costs.DATA_START].reset_index(drop=True)
        days = prepare(mn, hr); n_days[m] = len(days)
        per[m], sk = run_market(days, 0.0 if dry else costs.COST[m], floor_rate=costs.COST[m])
        for a, b in sk.items(): small[a] += b
    rows = []
    for v in SCENARIOS:                                      # screen: the screen years only
        nm = name(v)
        tr = pd.DataFrame([(d, m, r, c, side, how) for m in MARKETS for d, r, c, side, how in per[m][nm]], columns=["day", "market", "r", "cost", "side", "how"])
        s = stats(tr[tr["day"] < SPLIT]); ch = data_io.screen_checks(s)
        rows.append(dict(scenario=nm, parts=v, skipped_small=small[nm], screen=s, screen_checks=ch, screen_pass=all(ch.values()), trades=tr))
    survivors = [r for r in rows if r["screen_pass"]]
    need_t = NormalDist().inv_cdf(1 - 0.05 / max(len(survivors), C["min_survivors"]))
    for r in rows:                                           # confirm: only survivors ever have their confirm years computed
        tr = r.pop("trades")
        if r["screen_pass"]:
            s = stats(tr[tr["day"] >= SPLIT]); ch = data_io.confirm_checks(s, need_t)
            r.update(confirm=s, confirm_checks=ch, verdict="CONFIRMED" if all(ch.values()) else "REJECT")
        else:
            r["verdict"] = "REJECT"
        s = r["screen"]
        line = (f"{s['days']:4d} days, {s['trades']:5d} trades, win {s['win_rate_before_cost']:.1f}% before cost, avg {s['mean_r']:+.3f}R "
                f"(before cost {s['mean_r_before_cost']:+.3f}R, cost {s['avg_cost_r']:.3f}R), PF {s['pf']:.2f}, t {s['t']:+.2f}, markets {s['markets_positive']}/3") if "t" in s else f"{s['days']} days"
        tail = ""
        if "confirm" in r:
            c = r["confirm"]; tail = f" | confirm: {c['days']} days, avg {c['mean_r']:+.3f}R, PF {c['pf']:.2f}, t {c['t']:+.2f}/{need_t:.2f}" if "t" in c else f" | confirm: {c['days']} days"
        print(f"{r['verdict']:9s} {r['scenario']:20s} screen: {line}{' PASS' if r['screen_pass'] else ''}{tail}")
    confirmed = [r for r in rows if r["verdict"] == "CONFIRMED"]
    print(f"{len(rows)} scenarios, {len(survivors)} passed the screen, {len(confirmed)} confirmed (bar {need_t:.2f})")
    if dry:
        print("dry run on made-up prices with no cost: nothing written"); return
    today = datetime.date.today().isoformat()
    json.dump(dict(date=today, first_day=str(START), split=str(SPLIT), last_day=str(END), usable_days=n_days, need_t=need_t, survivors=len(survivors),
                   confirmed=len(confirmed), scenarios=rows), open(RESULTS, "w"), indent=1, default=float)
    with open(os.path.join(LAB, "JOURNAL.md"), "a") as j:
        j.write(f"\n### {today} · study 11 · the 1-hour and 15-minute \"CC\" setups · 8 scenarios · {len(survivors)} passed the screen, {len(confirmed)} confirmed\n"
                f"- Source: a post by @tradermike1234 on X (x.com/tradermike1234/status/2125172071374237862). Nasdaq 100, S&P 500 and Dow, 1-minute bars, 9:00 to 15:55 New York time.\n"
                f"- Screen: {START} to 2023-12-31. Confirm: 2024-01-01 to {END}, t-stat bar {need_t:.2f}. Every trade risks the distance to its target (1 to 1). "
                f"Results in R after the costs in `costs.py`. A win rate of 50% before costs is what no edge looks like.\n")
        for r in rows:
            s = r["screen"]
            if "t" not in s:
                j.write(f"- `{r['scenario']}` · REJECT: {s['days']} traded days\n"); continue
            fails = [k for k, ok in r["screen_checks"].items() if not ok]
            txt = (f"- `{r['scenario']}` · {r['verdict']}: screen {s['days']} days, {s['trades']} trades, win rate {s['win_rate_before_cost']:.1f}% before costs, "
                   f"average {s['mean_r']:+.3f}R ({s['mean_r_before_cost']:+.3f}R before costs, cost {s['avg_cost_r']:.3f}R), profit factor {s['pf']:.2f}, t-stat {s['t']:.2f}")
            if "confirm" in r and "t" in r["confirm"]:
                c = r["confirm"]; cf = [k for k, ok in r["confirm_checks"].items() if not ok]
                txt += f"; confirm {c['days']} days, average {c['mean_r']:+.3f}R, profit factor {c['pf']:.2f}, t-stat {c['t']:.2f}" + (f". Failed: {'; '.join(cf)}" if cf else "")
            elif fails:
                txt += f". Failed: {'; '.join(fails)}"
            j.write(txt + "\n")
    print("written to lab/intraday/strat_cc_results.json and the journal")


if __name__ == "__main__":
    main()
