"""Paper track helper.

Usage (from the repo root):
    python lab/tools/paper.py validate            # check every file in lab/papers
    python lab/tools/paper.py verdict IDEA_NAME   # after lab.py has tested the idea: write the lab's result and the verdict into the paper's file
    python lab/tools/paper.py brief               # write lab/briefs/DATE.md

The rules are in LAB_RULES.md under "Paper track".
"""
import sys, os, glob, json, csv, datetime, collections
import yaml

LAB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PAPERS = os.path.join(LAB, "papers")
REQUIRED = ["id", "title", "published", "url", "found", "status", "market", "timeframe", "data_needed", "testable_here",
            "formulas", "rules", "reported_results", "verdict"]
STATUSES = {"extracted", "cant_test", "coded", "tested"}
VERDICTS = {"pending", "holds_up", "decayed", "failed", "cant_test"}
MAX_TEXT = 1200          # a longer field is probably copied text: summarise instead


def load_all():
    out = {}
    for f in sorted(glob.glob(os.path.join(PAPERS, "*.yaml"))):
        if os.path.basename(f).startswith("_"):
            continue
        out[os.path.basename(f)[:-5]] = (f, yaml.safe_load(open(f, encoding="utf-8")))
    return out


def _date(v):
    return v if isinstance(v, datetime.date) else datetime.date.fromisoformat(str(v))


def _texts(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from _texts(v)
    elif isinstance(node, list):
        for v in node:
            yield from _texts(v)


def validate():
    problems = []
    for pid, (path, d) in load_all().items():
        if not isinstance(d, dict):
            problems.append(f"{pid}: not a mapping"); continue
        miss = [k for k in REQUIRED if k not in d]
        if miss:
            problems.append(f"{pid}: missing {', '.join(miss)}"); continue
        if d["id"] != pid: problems.append(f"{pid}: id does not match the file name")
        if d["status"] not in STATUSES: problems.append(f"{pid}: status must be one of {sorted(STATUSES)}")
        if d["verdict"] not in VERDICTS: problems.append(f"{pid}: verdict must be one of {sorted(VERDICTS)}")
        for k in ("published", "found"):
            try: _date(d[k])
            except Exception: problems.append(f"{pid}: {k} must be a date like 2026-01-31")
        if d["testable_here"] is False:
            if not d.get("why_not") or not d.get("missing_data"): problems.append(f"{pid}: not testable, so why_not and missing_data are needed")
            if d["verdict"] != "cant_test" or d["status"] != "cant_test": problems.append(f"{pid}: not testable, so status and verdict must both be cant_test")
        if d["status"] in ("coded", "tested") and not (d.get("idea") and os.path.exists(os.path.join(LAB, "ideas", f"{d['idea']}.py"))):
            problems.append(f"{pid}: status {d['status']} but the idea file is missing")
        if d["verdict"] in ("holds_up", "decayed", "failed") and not d.get("lab_result"):
            problems.append(f"{pid}: verdict {d['verdict']} must come from `paper.py verdict`, with lab_result filled")
        if any(len(t) > MAX_TEXT for t in _texts(d)): problems.append(f"{pid}: a text field is over {MAX_TEXT} characters; summarise in your own words")
    return problems


def split_by_publication(by_block, published):
    """Test years that end before the publication date, and test years that start on or after it."""
    before, after = {}, {}
    for b, v in by_block.items():
        b = int(b)
        if datetime.date(b + 1, 4, 21) <= published: before[b] = v
        elif datetime.date(b, 4, 21) >= published: after[b] = v
    half = lambda d: dict(years=len(d), total=round(float(sum(d.values())), 4), profitable_years=int(sum(v > 0 for v in d.values())))
    return half(before), half(after)


def verdict(idea_name):
    hits = [(p, d) for p, d in load_all().values() if d.get("idea") == idea_name]
    assert len(hits) == 1, f"expected one paper with idea: {idea_name}, found {len(hits)}"
    path, d = hits[0]
    results = sorted(glob.glob(os.path.join(LAB, "results", f"{idea_name}_*.json")), key=os.path.getmtime)
    assert results, f"no lab result for {idea_name}: run lab.py first"
    r = json.load(open(results[-1]))
    before, after = split_by_publication(r.get("by_block", {}), _date(d["published"]))
    position = r.get("mode") == "position"
    if r["verdict"] == "CANDIDATE":
        v = "holds_up"
    elif before["years"] >= 2 and before["total"] > 0 and before["profitable_years"] / before["years"] >= 0.6 and after["years"] >= 1 and after["total"] <= 0:
        v = "decayed"
    else:
        v = "failed"
    d["lab_result"] = dict(
        date=r["date"], attempt=r["attempts"], lab_verdict=r["verdict"], markets=r.get("markets", []),
        headline=(f"{r['days']} days, Sharpe {r['sharpe']:.2f}, t-stat {r['t']:.2f} (needed {r['need_t']:.2f})" if position else
                  f"{r['trades']} trades, profit factor {r['pf']:.2f}, t-stat {r['t']:.2f} (needed {r['need_t']:.2f})"),
        unit="return" if position else "R (risk units)",
        failed_checks=[k for k, ok in r["checks"].items() if not ok],
        before_publication=before, after_publication=after)
    d["verdict"], d["status"] = v, "tested"
    yaml.safe_dump(d, open(path, "w", encoding="utf-8"), sort_keys=False, allow_unicode=True, width=110)
    print(f"{d['id']}: {v}  ({d['lab_result']['headline']}; before publication {before}; after {after})")


def brief():
    today = datetime.date.today().isoformat(); papers = [d for _, d in load_all().values()]
    seen_path = os.path.join(PAPERS, "seen.csv")
    seen = [r for r in csv.DictReader(open(seen_path, encoding="utf-8"))] if os.path.exists(seen_path) else []
    seen_today = [r for r in seen if r["date"] == today]
    kept = sum(r["decision"] == "keep" for r in seen_today)
    by_v = collections.Counter(d["verdict"] for d in papers)
    tested_today = [d for d in papers if (d.get("lab_result") or {}).get("date") == today]
    cant_today = [d for d in papers if d["verdict"] == "cant_test" and str(d["found"]) == today]
    need = collections.Counter(t for d in papers if d["verdict"] == "cant_test" for t in (d.get("missing_data") or []))
    L = [f"# Morning brief · {today}", "", "## Papers",
         f"- Abstracts looked at today: {len(seen_today)}. Kept: {kept}. Dropped: {len(seen_today) - kept}.",
         f"- All abstracts so far: {len(seen)}. Papers written up: {len(papers)}."]
    if tested_today:
        L.append("- Tested today:")
        L += [f"  - {d['title']} ({str(d['published'])[:4]}): **{d['verdict'].replace('_', ' ')}**. {d['lab_result']['headline']}." for d in tested_today]
    else:
        L.append("- Tested today: none.")
    if cant_today:
        L.append("- Could not be tested today:")
        L += [f"  - {d['title']}: {d.get('why_not', '')}" for d in cant_today]
    holds = [d for d in papers if d["verdict"] == "holds_up"]
    L.append("- Holds up so far: " + ("none." if not holds else ""))
    for d in holds:
        L.append(f"  - {d['title']}. Theory, not a finding: it might stop working when {d.get('may_stop_working') or 'conditions change in ways not yet written down'}.")
    L.append(f"- Totals: holds up {by_v['holds_up']}, decayed {by_v['decayed']}, failed {by_v['failed']}, can't test {by_v['cant_test']}, waiting {by_v['pending']}.")
    if need:
        L.append("- Data that would unlock the most papers: " + ", ".join(f"{t.replace('_', ' ')} ({n})" for t, n in need.most_common(5)) + ".")
    try:
        s = json.load(open(os.path.join(LAB, "screen", "state.json")))
        L += ["", "## Machine-built ideas", f"- Screened {s['screened']:,}. Passed the screen: {s['survivors']}. Confirmed on unseen years: {s['confirmed']}. Candidates: {s['candidates']}."]
    except Exception:
        pass
    try:
        f = json.load(open(os.path.join(LAB, "forward", "status.json")))
        trades = sum(i["trades"] for i in f["ideas"]); ends = max(v[:10] for v in f["data_ends"].values())
        L += ["", "## Forward watch", f"- {f['watched']} ideas watched. Forward trades so far: {trades}. Price data ends {ends}.",
              f"- Verdicts so far: {sum(i['status'] != 'WATCHING' for i in f['ideas'])}."]
    except Exception:
        pass
    L += ["", "Nothing here is a recommendation to trade."]
    os.makedirs(os.path.join(LAB, "briefs"), exist_ok=True)
    out = os.path.join(LAB, "briefs", f"{today}.md"); open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L)); print(f"\nwritten to lab/briefs/{today}.md")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "validate":
        probs = validate(); print("OK: every paper file is valid" if not probs else "PROBLEMS:\n- " + "\n- ".join(probs)); sys.exit(1 if probs else 0)
    elif cmd == "verdict":
        verdict(sys.argv[2])
    elif cmd == "brief":
        brief()
    else:
        print(__doc__)
