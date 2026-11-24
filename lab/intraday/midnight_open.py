"""Study 9: does price get pulled back to the midnight open? One run.

Run from the repo root:
    python lab/intraday/midnight_open.py --dryrun    # same code on made-up prices; nothing is written
    python lab/intraday/midnight_open.py             # the one real run; refuses to run a second time

The rules are in LAB_RULES.md under "Study 9". They were written and pushed before this rule was run on any lab data.
Source of the claim: a post by @RHerman on X, x.com/rherman/status/2124971266839076991 (November 23, 2026).
The post gives a count and a rate from the author's own study, with no rules for a trade. The code below is the lab's own.

Days where the open is above the midnight open are turned upside down, so everything is written as "the level is above".
"""
import sys, os, json, datetime, math
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.join(HERE, "..")
sys.path.insert(0, HERE); sys.path.insert(0, LAB)
import sweep_fvg as data_io                                 # reuses study 8's loaders and its made-up prices
import costs

RESULTS = os.path.join(HERE, "midnight_open_results.json")
MARKETS = ["NAS100", "SPX500", "USA30"]                     # the post is about the Nasdaq; the other two are reported only
START, END = datetime.date(2021, 4, 22), datetime.date(2026, 11, 19)
RTH0, RTH1, FLAT = 570, 960, 955                            # 9:30, 16:00 and 15:55 as minutes of the New York day
NBAR = RTH1 - RTH0
MIN_BARS, MIN_DAYS = 370, 100
FLOOR = 0.0004                                              # a trade needs the level at least 0.04% of price away
GROUPS = ("setup", "below_no_gap", "mirror_setup", "above_no_gap")
POST_RATE, POST_DAYS = 0.825, 300


def binom_tail(k, n, p=0.5):
    """Chance of k or more successes in n tries."""
    return float(sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))) if n else float("nan")


def prepare(mn, hr):
    """One record per usable day: the regular-hours minute bars, the midnight open and the previous day's close."""
    hny = hr["time"].dt.tz_convert("America/New_York").dt.tz_localize(None)
    midnight = {t.date(): float(o) for t, o in zip(hny, hr["open"]) if t.hour == 0}
    ny = mn["time"].dt.tz_convert("America/New_York").dt.tz_localize(None)
    mod = (ny.dt.hour * 60 + ny.dt.minute).to_numpy() - RTH0
    keep = (mod >= 0) & (mod < NBAR)
    day = ny.dt.normalize().to_numpy()[keep]; mod = mod[keep]
    cols = [mn[x].to_numpy(float)[keep] for x in ("open", "high", "low", "close")]
    bounds = np.r_[0, np.flatnonzero(day[1:] != day[:-1]) + 1, len(day)]
    out = []; prev_close = None
    for a, b in zip(bounds[:-1], bounds[1:]):
        date = pd.Timestamp(day[a]).date()
        arr = np.full((4, NBAR), np.nan); arr[:, mod[a:b]] = [x[a:b] for x in cols]
        o, h, l, c = arr
        pc = prev_close
        late = np.flatnonzero(~np.isnan(c[NBAR - 15:]))                     # this day's close, for the next day: last bar from 15:45 to 15:59
        prev_close = float(c[NBAR - 15 + late[-1]]) if len(late) else None
        if not (START <= date <= END) or pc is None or date not in midnight:
            continue
        if np.isnan(o[0]) or (~np.isnan(h)).sum() < MIN_BARS:
            continue
        out.append(dict(date=date, o=o, h=h, l=l, c=c, mo=midnight[date], pc=pc))
    return out


def one_day(d, cost):
    """Group, touch, first touch and trade for one day. Prices are flipped when the level is below the open."""
    O, MO, PC = d["o"][0], d["mo"], d["pc"]
    if O == MO:
        return None
    if O < MO:
        group = "setup" if PC < O else "below_no_gap"; o, h, l, c = d["o"], d["h"], d["l"], d["c"]; side = 1
    else:
        group = "mirror_setup" if PC > O else "above_no_gap"; o, h, l, c = -d["o"], -d["l"], -d["h"], -d["c"]; side = -1; O, MO = -O, -MO
    dist = MO - O; stop = O - dist                           # the level is dist above the open; the phantom level is dist below
    with np.errstate(invalid="ignore"):
        up = np.flatnonzero(h >= MO); dn = np.flatnonzero(l <= stop)
    iu = int(up[0]) if len(up) else NBAR + 1; idn = int(dn[0]) if len(dn) else NBAR + 1
    first = "neither" if min(iu, idn) > NBAR else ("same_minute" if iu == idn else ("level" if iu < idn else "phantom"))   # a minute that reaches both decides nothing
    rec = dict(date=d["date"], group=group, side=side, dist_pct=float(dist / abs(O) * 100), touch=bool(len(up)), first=first)
    if dist / abs(O) >= FLOOR:                               # the trade: enter at the 9:30 open, target the level, stop at the phantom
        c_r = cost * abs(O) / dist; px = None; how = None
        for i in range(0, FLAT - RTH0):
            if np.isnan(h[i]):
                continue
            if i > 0 and o[i] <= stop: px, how = o[i], "stop"; break
            if i > 0 and o[i] >= MO: px, how = o[i], "target"; break
            if l[i] <= stop: px, how = stop, "stop"; break
            if h[i] >= MO: px, how = MO, "target"; break
        if px is None:
            j = FLAT - RTH0
            if not np.isnan(o[j]): px = o[j]
            else:
                ok = np.flatnonzero(~np.isnan(c[:j])); px = c[ok[-1]]
            how = "time"
        rec.update(r=float((px - O) / dist), cost=float(c_r * (3 if how == "stop" else 2)), how=how)
    return rec


def summarise(rows):
    """Counts and rates for one group of days."""
    n = len(rows)
    if n == 0:
        return dict(days=0)
    lvl = sum(r["first"] == "level" for r in rows); ph = sum(r["first"] == "phantom" for r in rows)
    out = dict(days=n, touch_rate=float(np.mean([r["touch"] for r in rows])), level_first=lvl, phantom_first=ph, same_minute=sum(r["first"] == "same_minute" for r in rows),
               neither=sum(r["first"] == "neither" for r in rows),
               level_first_share=float(lvl / (lvl + ph)) if lvl + ph else float("nan"), p_above_half=binom_tail(lvl, lvl + ph),
               median_dist_pct=float(np.median([r["dist_pct"] for r in rows])))
    tr = [r for r in rows if "r" in r]
    if len(tr) >= 3:
        net = np.array([r["r"] - r["cost"] for r in tr]); dbl = np.array([r["r"] - 2 * r["cost"] for r in tr]); gross = np.array([r["r"] for r in tr])
        wins, losses = net[net > 0], net[net <= 0]
        by_year = {}
        for r, x in zip(tr, net):
            by_year[r["date"].year] = by_year.get(r["date"].year, 0.0) + float(x)
        out["trade"] = dict(trades=len(tr), mean_r=float(net.mean()), t=float(net.mean() / (net.std(ddof=1) / math.sqrt(len(net)))) if net.std(ddof=1) > 0 else float("nan"),
                            pf=float(wins.sum() / -losses.sum()) if losses.sum() < 0 else float("inf"), win_rate=float((net > 0).mean()), mean_r_before_cost=float(gross.mean()),
                            mean_r_double_cost=float(dbl.mean()), avg_cost_r=float(np.mean([r["cost"] for r in tr])), total_r=float(net.sum()),
                            by_year_r={int(k): round(v, 2) for k, v in sorted(by_year.items())},
                            endings={k: sum(r["how"] == k for r in tr) for k in ("target", "stop", "time")})
    else:
        out["trade"] = dict(trades=len(tr))
    return out


def main():
    dry = "--dryrun" in sys.argv
    if os.path.exists(RESULTS) and not dry:
        print("Study 9 has already been run. It runs once. See lab/intraday/midnight_open_results.json."); return
    res = {}
    for k, m in enumerate(MARKETS):
        mn, hr = data_io.load(m, fake_seed=k + 21 if dry else None)
        days = prepare(mn, hr); cost = 0.0 if dry else costs.COST[m]
        rows = [x for x in (one_day(d, cost) for d in days) if x is not None]
        res[m] = dict(usable_days=len(days), groups={g: summarise([r for r in rows if r["group"] == g]) for g in GROUPS})
        setup = sorted([r for r in rows if r["group"] == "setup"], key=lambda r: r["dist_pct"])
        thirds = [setup[i * len(setup) // 3:(i + 1) * len(setup) // 3] for i in range(3)]
        res[m]["setup_by_distance"] = [dict(max_dist_pct=round(t[-1]["dist_pct"], 3), **{k: v for k, v in summarise(t).items() if k != "trade"}) if t else {} for t in thirds]
    s = res["NAS100"]["groups"]["setup"]; tr = s.get("trade", {})
    checks = {f"at least {MIN_DAYS} setup days": bool(s["days"] >= MIN_DAYS),
              "level reached before the phantom level on more than half of decided days (p <= 0.05)": bool(s["days"] and s["level_first_share"] > 0.5 and s["p_above_half"] <= 0.05),
              "trade average above zero after costs with t-stat >= 1.65": bool(tr.get("trades", 0) >= 3 and tr["mean_r"] > 0 and tr["t"] >= 1.65),
              "trade average above zero at double cost": bool(tr.get("trades", 0) >= 3 and tr["mean_r_double_cost"] > 0)}
    verdict = "SUPPORTED" if all(checks.values()) else "NOT SUPPORTED"
    for m in MARKETS:
        print(f"{m}: {res[m]['usable_days']} usable days")
        for g in GROUPS:
            x = res[m]["groups"][g]
            if not x["days"]:
                print(f"  {g:13s} 0 days"); continue
            t = x["trade"]
            trade = (f" | trade: {t['trades']} trades, avg {t['mean_r']:+.3f}R ({t['mean_r_before_cost']:+.3f}R before costs), win {t['win_rate']*100:.0f}%, PF {t['pf']:.2f}, t {t['t']:+.2f}"
                     if t.get("trades", 0) >= 3 else f" | trade: {t.get('trades', 0)} trades")
            print(f"  {g:13s} {x['days']:4d} days, touched {x['touch_rate']*100:5.1f}%, first: level {x['level_first']} / phantom {x['phantom_first']} / same minute {x['same_minute']} / neither {x['neither']} "
                  f"({x['level_first_share']*100:.1f}%, p {x['p_above_half']:.3f}), median distance {x['median_dist_pct']:.3f}%{trade}")
        print("  setup by distance:", "; ".join(f"up to {t['max_dist_pct']}%: {t['days']} days, touched {t['touch_rate']*100:.0f}%, level first {t['level_first_share']*100:.0f}%" for t in res[m]["setup_by_distance"] if t))
    print("verdict (Nasdaq, the post's setup):", verdict, json.dumps(checks))
    if dry:
        print("dry run on made-up prices with no cost: nothing written"); return
    today = datetime.date.today().isoformat()
    json.dump(dict(date=today, first_day=str(START), last_day=str(END), post=dict(rate=POST_RATE, days=POST_DAYS, period="2015-2025"), verdict=verdict, checks=checks, markets=res),
              open(RESULTS, "w"), indent=1, default=str)
    with open(os.path.join(LAB, "JOURNAL.md"), "a") as j:
        j.write(f"\n### {today} · study 9 · pull to the midnight open · {verdict}\n"
                f"- Source: a post by @RHerman on X (x.com/rherman/status/2124971266839076991): on the Nasdaq, when the 9:30 open is below the midnight open and above the previous close, "
                f"price got back to the midnight open in 82.5% of almost 300 sessions, 2015 to 2025.\n"
                f"- Lab data: 1-minute bars, {START} to {END}. Costs from `costs.py`. No screen and confirm split: there are too few days.\n")
        for m in MARKETS:
            x = res[m]["groups"]["setup"]; t = x.get("trade", {})
            if not x["days"]:
                j.write(f"- {m}: 0 setup days.\n"); continue
            j.write(f"- {m}, the post's setup: {x['days']} days of {res[m]['usable_days']}. Midnight open touched on {x['touch_rate']*100:.1f}%. Reached before the phantom level the same distance below on "
                    f"{x['level_first']} days, after it on {x['phantom_first']}, both in one minute on {x['same_minute']}, neither on {x['neither']} ({x['level_first_share']*100:.1f}% of decided days, p {x['p_above_half']:.3f}). "
                    f"Median distance {x['median_dist_pct']:.3f}% of price."
                    + (f" Trade: {t['trades']} trades, average {t['mean_r']:+.3f}R after costs ({t['mean_r_before_cost']:+.3f}R before), win rate {t['win_rate']*100:.0f}%, profit factor {t['pf']:.2f}, t-stat {t['t']:.2f}.\n"
                       if t.get("trades", 0) >= 3 else "\n"))
        for g in GROUPS[1:]:
            x = res["NAS100"]["groups"][g]
            if x["days"]:
                j.write(f"- Nasdaq, `{g}`: {x['days']} days, touched {x['touch_rate']*100:.1f}%, level first on {x['level_first_share']*100:.1f}% of decided days (p {x['p_above_half']:.3f}).\n")
        fails = [k for k, ok in checks.items() if not ok]
        j.write(f"- Checks failed: {'; '.join(fails) if fails else 'none'}.\n")
    print("written to lab/intraday/midnight_open_results.json and the journal")


if __name__ == "__main__":
    main()
