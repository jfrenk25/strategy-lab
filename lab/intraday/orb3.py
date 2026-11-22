"""Intraday study 3: the video's own settings (1 ATR stop, 2 ATR target, 10-minute exit). One run.

Run from the repo root:
    python lab/intraday/orb3.py --dryrun    # same code on made-up prices; nothing is written
    python lab/intraday/orb3.py             # the one real run; refuses to run a second time

The rules are in LAB_RULES.md under "Intraday study 3". They were written before any 1-minute data reached the lab.
"""
import sys, os, json, datetime
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orb

RESULTS = os.path.join(orb.HERE, "orb3_results.json")
P = dict(atr=14, stop=1.0, target=2.0, regime_len=14, regime=(1.0, 3.0))


def trades(df, use_regime):
    """One row per traded day. 'gross' counts a bar that touches both levels as a stop; 'gross_best' counts it as a target."""
    rows = []
    for day, g in df.groupby("day", sort=True):
        hm = g["hm"].to_numpy(); o, h, l, c, v = (g[k].to_numpy() for k in ("open", "high", "low", "close", "volume"))
        in_range = (hm >= 930) & (hm <= 944)
        if in_range.sum() < orb.T["range_bars"]:
            continue
        pos = {x: i for i, x in enumerate(hm)}
        if 959 not in pos or 1000 not in pos or 1010 not in pos:
            continue
        i = pos[959]
        if i < P["atr"] + P["regime_len"] - 1:
            continue
        hi, lo = h[in_range].max(), l[in_range].min()
        side = 1 if c[i] > hi else (-1 if c[i] < lo else 0)
        if side == 0:
            continue
        base = v[i - 14:i].mean()
        if not base > 0 or not (orb.T["relvol"][0] <= v[i] / base <= orb.T["relvol"][1]):
            continue
        pc = np.r_[c[0], c[:-1]]; tr = np.maximum(h - l, np.maximum(np.abs(h - pc), np.abs(l - pc))); tr[0] = h[0] - l[0]
        atrs = np.array([tr[k - P["atr"] + 1:k + 1].mean() for k in range(i - P["regime_len"] + 1, i + 1)])
        atr = atrs[-1]
        if not atr > 0:
            continue
        if use_regime and not (P["regime"][0] <= atr / atrs.mean() <= P["regime"][1]):
            continue
        entry = o[pos[1000]]; stop, target = entry - side * P["stop"] * atr, entry + side * P["target"] * atr
        worst = best = None; how = "time"
        for k in range(pos[1000], pos[1010]):
            adverse, favourable = (l[k], h[k]) if side == 1 else (h[k], l[k])
            hit_stop, hit_target = side * (adverse - stop) <= 0, side * (favourable - target) >= 0
            if side * (o[k] - stop) <= 0:                # opened beyond the stop: out at the open
                worst = best = o[k]; how = "stop"; break
            if hit_stop and hit_target:                  # the bar cannot say which came first
                worst, best, how = stop, target, "both"; break
            if hit_stop:
                worst = best = stop; how = "stop"; break
            if hit_target:
                worst = best = target; how = "target"; break
        if worst is None:
            worst = best = o[pos[1010]]
        rows.append((day, side, side * (worst / entry - 1), side * (best / entry - 1), how))
    return pd.DataFrame(rows, columns=["day", "side", "gross", "gross_best", "how"])


def main():
    dry = "--dryrun" in sys.argv
    if os.path.exists(RESULTS) and not dry:
        print("Intraday study 3 has already been run. It runs once. See lab/intraday/orb3_results.json."); return
    out = dict(date=datetime.date.today().isoformat(), markets={}, missing=[])
    for n, m in enumerate(orb.MARKETS):
        if not dry and not os.path.exists(os.path.join(orb.DATA, f"{m}_1m.csv.gz")):
            out["missing"].append(m); continue
        df = orb.load(m, fake_seed=n + 1 if dry else None)
        res = dict(first=str(df["day"].min()), last=str(df["day"].max()))
        for label, use_regime in (("A_all_settings", True), ("B_no_atr_regime", False)):
            tr = trades(df, use_regime); best = tr.assign(gross=tr["gross_best"])
            early, late = tr["day"] < orb.SPLIT, tr["day"] >= orb.SPLIT
            su, sv = orb.stats(tr[early]), orb.stats(tr[late]); checks, verdict = orb.judge(su)
            bu = orb.stats(best[early]); _, verdict_best = orb.judge(bu)
            exits = {k: int(x) for k, x in tr["how"].value_counts().items()}
            res[label] = dict(before_2024=su, from_2024=sv, checks=checks, verdict=verdict, before_2024_if_both_counted_as_wins=bu, verdict_if_both_counted_as_wins=verdict_best,
                              from_2024_if_both_counted_as_wins=orb.stats(best[late]), exits=exits, needs_tick_data=bool(verdict != verdict_best))
            f = lambda s: (f"{s['trades']:4d} trades, win {s['win_rate']:.0f}%, avg {s['mean_pct']:+.4f}%, PF {s['pf']:.2f}, t {s['t']:+.2f}" if s.get("trades", 0) >= 3 else f"{s.get('trades', 0)} trades")
            print(f"{m:7s} {label:16s} before 2024: {f(su)} -> {verdict:4s} (both-touched as wins: {verdict_best}) | from 2024: {f(sv)} | exits {exits}")
        out["markets"][m] = res
    if dry:
        print("dry run on made-up prices: nothing written"); return
    assert "NAS100" in out["markets"], "the Nasdaq file is missing: nothing was run or written"
    json.dump(out, open(RESULTS, "w"), indent=1, default=float)
    line = lambda s: (f"{s['trades']} trades, win rate {s['win_rate']:.0f}%, average {s['mean_pct']:+.4f}% a trade, profit factor {s['pf']:.2f}, t-stat {s['t']:.2f}" if s.get("trades", 0) >= 3 else f"{s.get('trades', 0)} trades")
    nq = out["markets"]["NAS100"]
    with open(os.path.join(orb.LAB, "JOURNAL.md"), "a") as j:
        j.write(f"\n### {out['date']} · intraday study 3 · the video's own settings · A {nq['A_all_settings']['verdict']}, B {nq['B_no_atr_regime']['verdict']}\n"
                f"- Settings from a screenshot of the video's panel: 1 ATR stop, 2 ATR target, 10-minute exit, volume filter 0.5 to 1.5, ATR regime 1 to 3. Rules fixed in LAB_RULES.md before the data arrived.\n"
                f"- Nasdaq 100, 1-minute bars, {nq['first']} to {nq['last']}. Verdict from the years before 2024, with a bar that touches both stop and target counted as a loss; needed t-stat {orb.NEED_T}.\n")
        for m, res in out["markets"].items():
            for label, words in (("A_all_settings", "all settings"), ("B_no_atr_regime", "no ATR regime filter")):
                r = res[label]; fails = [k for k, ok in r["checks"].items() if not ok]
                j.write(f"- {m}, test {label[0]} ({words}): before 2024: {line(r['before_2024'])}. From 2024: {line(r['from_2024'])}. Exits: {r['exits']}. "
                        f"With both-touched bars counted as wins, before 2024: {line(r['before_2024_if_both_counted_as_wins'])}. "
                        f"{'Verdict' if m == 'NAS100' else 'Reported only'}: {r['verdict']}." + (f" Failed: {'; '.join(fails)}." if fails and m == "NAS100" else "")
                        + (" The verdict flips if those bars are counted as wins, so this needs tick data." if r["needs_tick_data"] and m == "NAS100" else "") + "\n")
        if out["missing"]:
            j.write(f"- Not downloaded: {', '.join(out['missing'])}.\n")
    print("written to lab/intraday/orb3_results.json and the journal")


if __name__ == "__main__":
    main()
