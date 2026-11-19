"""Grade live-call suggestions against the 25-moment test.

usage:
  python3 grade.py suggestions.jsonl          # score a run file
  python3 grade.py --demo                     # build and score a constructed demo run
  python3 grade.py --export eval.md eval.xlsx # write the one-page table and the scoring workbook

Each line of suggestions.jsonl is one suggestion for one moment and one run:
  {"case": 4, "run": 1, "step": "FACT", "text": "Pro is from $15 per host...", "latency_ms": 310}
"step" is the method step the suggestion serves (Othello's own tag, or a reviewer's label);
use "NONE" with empty text when nothing was shown. Every case runs 3 times and passes only
if all 3 runs pass. Gate: 24 of 25 cases on all three runs and zero critical (E3) errors.
"""
import json, re, sys, os
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cases import CASES, ERRORS, METRICS

LATENCY_MS = 500

def grade_one(i, s):
    tier, covered, says, expected, steps, must, must_not, err = CASES[i - 1]
    step = (s.get("step") or "NONE").upper()
    text = s.get("text") or ""
    low = text.lower()
    for pat in must_not:
        if re.search(pat, text, re.I):
            return "E3"
    if "NONE" in steps:
        return None if step == "NONE" and not text.strip() else "E4"
    if step not in steps:
        return err if err != "E3" else "E1"
    for group in must:
        if not any(g.lower() in low for g in group):
            return err if err != "E3" else "E1"
    lat = s.get("latency_ms")
    if lat is not None and lat > LATENCY_MS:
        return "E5"
    return None

def grade(rows):
    runs = defaultdict(dict)
    for r in rows:
        runs[int(r["case"])][int(r["run"])] = r
    results, errs = {}, defaultdict(int)
    for i in range(1, len(CASES) + 1):
        got = runs.get(i, {})
        if len(got) < 3:
            results[i] = ("INCOMPLETE", [])
            continue
        e = [grade_one(i, got[k]) for k in sorted(got)[:3]]
        for x in e:
            if x: errs[x] += 1
        results[i] = ("PASS" if not any(e) else "FAIL", e)
    return results, errs

def report(results, errs):
    by_tier = defaultdict(lambda: [0, 0])
    for i, (res, _) in results.items():
        t = CASES[i - 1][0]
        by_tier[t][1] += 1
        by_tier[t][0] += res == "PASS"
    passed = sum(r == "PASS" for r, _ in results.values())
    print(f"{'#':>2}  tier  result  errors (run 1/2/3)")
    for i, (res, e) in results.items():
        print(f"{i:>2}  {CASES[i-1][0]:<4}  {res:<6}  {' '.join(x or '-' for x in e)}")
    print("\nBy tier: " + ", ".join(f"{t} {p} of {n}" for t, (p, n) in sorted(by_tier.items())))
    print("Errors: " + (", ".join(f"{k} x{v}" for k, v in sorted(errs.items())) or "none"))
    gate = passed >= 24 and errs.get("E3", 0) == 0
    print(f"\nKeyword gate (24 of 25 on all three runs, zero E3): {passed} of 25 -> {'PASS' if gate else 'FAIL'}")
    print("Not final until a reviewer reads every suggestion on moments 4, 5, 8, 13, 14, 16 to 19, 24, and 25 for wrong facts and invented commitments.")
    return gate

def demo_rows():
    # Constructed to show the grader working. NOT Othello output.
    ok = {
        1: ("M", "Ask how many incidents a month hit on-call, and how long the first triage takes."),
        2: ("DP", "Ask who has to sign off after a trial, and by when they want a decision."),
        3: ("EB", "Ask what your VP of Engineering cares about most, and offer to meet them."),
        4: ("FACT", "Infrastructure Pro is from $15 per host a month billed annually, $18 on-demand; Enterprise from $23."),
        5: ("FACT", "No re-instrumenting: send OTLP to the Datadog Agent or use the DDOT Collector."),
        6: ("DC", "Ask which capabilities will decide it, and who sets those criteria."),
        7: ("CH", "Ask what Sam gains if this lands, and whether Sam can join the next call."),
        8: ("FACT", "Ingest is from $0.10 per GB, about $200 a month for 2 TB; indexing is billed per million events, so ask how many they search."),
        9: ("M", "Ask how many outages last quarter, and how many hours each took."),
        10: ("IP", "Ask which of the two matters more to leadership right now."),
        11: ("EB", "Ask which of them owns the budget and approves this."),
        12: ("DP", "Before you go, ask for the next step and the decision timeline."),
        13: ("FACT", "Flex Logs keeps logs for 3, 6, 12, or 15 months, versus 3 to 30 days or more on Standard Indexing."),
        14: ("OBJ", "Acknowledge it, and ask what drove the bill: logs, custom metrics, or hosts."),
        15: ("M", "Ask how many hours a week, and how many engineers."),
        16: ("FACT", "Yes: up to five hosts are free, with 1-day metric retention."),
        17: ("DEFER", "Do not commit; say volume and multi-year pricing exist and you will come back with a proposal before their decision date."),
        18: ("DEFER", "Point to the Datadog Trust Center and offer to send the documentation."),
        19: ("DC", "Ask what the quote includes, hosts, data, and users, and which capabilities they need."),
        20: ("CH", "Ask who will take over the project after Sam, and meet them before he leaves."),
        21: ("BA", "Reflect that back, then ask what good would look like if alerts were trusted again."),
        22: ("NONE", ""), 23: ("NONE", ""),
        24: ("DEFER", "Offer a follow-up with Datadog's legal and security team."),
        25: ("DEFER", "Offer a follow-up with a product specialist."),
    }
    rows = []
    for c, (st, tx) in ok.items():
        for run in (1, 2, 3):
            rows.append({"case": c, "run": run, "step": st, "text": tx, "latency_ms": 320})
    # one deliberate critical failure, to show the gate
    rows = [r for r in rows if not (r["case"] == 17 and r["run"] == 2)]
    rows.append({"case": 17, "run": 2, "step": "DEFER", "text": "We can likely do 10% off if you sign this month.", "latency_ms": 300})
    return rows

def export(md_path, xlsx_path):
    o = ["## The 25-moment test: would Othello suggest the right next step on a Datadog first call?",
         "*Every moment is constructed for this test, not Datadog or Othello data: a Datadog Commercial AE's first discovery call with a made-up 300-person software company on AWS. Product facts come only from Datadog's public pricing page and docs. Each moment runs three times and passes only if all three runs pass. Gate: 24 of 25 on all three runs, with zero critical errors. A grading script (grade.py) scores a run log against this table. Keyword checks are a first pass: before the gate is called, a reviewer reads every suggestion on the fact and judgment moments (4, 5, 8, 13, 14, 16 to 19, 24, and 25) for wrong facts and invented commitments. Moments marked E3 count as critical only when an invented commitment appears; a missing hedge counts as E1.*",
         "", "| Metric | What it counts | Target |", "|------|----------------|------|"]
    o += [f"| {a} | {b} | {c} |" for a, b, c in METRICS]
    o += ["", "**Steps:** M metrics · EB economic buyer · DC decision criteria · DP decision process · IP identify pain · CH champion (MEDDIC) · DIFF differentiator · BA before/after (Command of the Message) · OBJ objection · FACT answer from public docs · DEFER offer a follow-up · NONE stay quiet. "
          "**Errors:** " + " · ".join(f"**{c}** {d} ({s})" for c, d, s in ERRORS) + ".", "",
          "| # | Tier | Already covered | Buyer says (constructed) | Right next step | Fails as |",
          "|-|--|----|--------------|--------------|--|"]
    o += [f"| {i} | {t} | {cov} | {says} | {exp} | {e} |" for i, (t, cov, says, exp, st, m, mn, e) in enumerate(CASES, 1)]
    o += ["", "*Tiers: T1 clean (8) · T2 messy but in scope (8) · T3 needs judgment (5) · T4 stay quiet or hand off (4).*"]
    open(md_path, "w").write("\n".join(o) + "\n")
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, Border, Side
    wb = Workbook(); thin = Side(style="thin", color="000000"); B = Border(left=thin, right=thin, top=thin, bottom=thin)
    ws = wb.active; ws.title = "Moments"
    head = ["#", "Tier", "Already covered", "Buyer says (constructed)", "Right next step", "Accepted steps", "Fails as",
            "Run 1 pass (Y/N)", "Run 2 pass (Y/N)", "Run 3 pass (Y/N)", "Critical error (Y/N)", "Moment result"]
    ws.append(head)
    for i, (t, cov, says, exp, st, m, mn, e) in enumerate(CASES, 1):
        r = i + 1
        ws.append([i, t, cov, says, exp, ", ".join(st), e, None, None, None, None,
                   f'=IF(COUNTA(H{r}:J{r})<3,"",IF(AND(COUNTIF(H{r}:J{r},"Y")=3,K{r}<>"Y"),"PASS","FAIL"))'])
    n = len(CASES) + 1
    ws.append([]); ws.append(["", "", "", "Moments passed", f'=COUNTIF(L2:L{n},"PASS")'])
    ws.append(["", "", "", "Critical errors", f'=COUNTIF(K2:K{n},"Y")'])
    ws.append(["", "", "", "Gate (24 of 25, zero critical)", f'=IF(COUNTA(L2:L{n})-COUNTBLANK(L2:L{n})<25,"",IF(AND(E{n+2}>=24,E{n+3}=0),"PASS","FAIL"))'])
    for row in ws.iter_rows():
        for c in row:
            c.font = Font(name="Arial", size=10, bold=(c.row == 1)); c.alignment = Alignment(wrap_text=True, vertical="top")
            if c.row <= n: c.border = B
    for col, w in zip("ABCDEFGHIJKL", [4, 6, 18, 44, 44, 12, 8, 9, 9, 9, 10, 10]):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"
    e = wb.create_sheet("Errors"); e.append(["Code", "Error type", "Severity"])
    for x in ERRORS: e.append(list(x))
    for col, w in zip("ABC", [6, 80, 10]): e.column_dimensions[col].width = w
    wb.save(xlsx_path)

if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--export":
        export(a[1], a[2]); print("wrote", a[1], a[2])
    elif a and a[0] == "--demo":
        rows = demo_rows()
        print("DEMO: constructed suggestions to show the grader, not Othello output\n")
        report(*grade(rows))
    elif a:
        rows = [json.loads(l) for l in open(a[0]) if l.strip()]
        sys.exit(0 if report(*grade(rows)) else 1)
    else:
        print(__doc__)
