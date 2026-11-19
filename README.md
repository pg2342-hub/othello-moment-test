# 25-moment test: does a live-call coach suggest the right next step?

A test set and grading script for a live-call AI sales coach (built with Othello in mind), set on a Datadog Commercial Account Executive's first discovery call. It pairs with a 30-day pilot plan for running Othello on one Datadog Commercial Sales team.

All moments are constructed for this test, not Datadog or Othello data: a made-up 300-person software company on AWS. Product facts come only from datadoghq.com/pricing and docs.datadoghq.com/opentelemetry (checked 2026-11-18). Steps follow MEDDIC and Command of the Message, which Datadog's Commercial AE postings name as its sales training.

## What is here
- [`moment_test.md`](moment_test.md): the 25 moments in one table (what the buyer says, steps already covered, the right next step, and how a miss is scored).
- `cases.py`: the same moments as data, with accepted step labels, required facts, and banned claims.
- `grade.py`: scores a suggestion log (JSONL, one line per moment per run) and applies the gate.
- `moment_test_scoring.xlsx`: the same test as a manual scoring sheet with pass formulas.

## How it is scored
- Tiers: T1 clean (8), T2 messy but in scope (8), T3 needs judgment (5), T4 stay quiet or hand off (4).
- Each moment runs three times and passes only if all three runs pass.
- Gate: 24 of 25 moments on all three runs, with zero critical errors (an invented discount, certification, legal term, roadmap, or competitor price).
- Keyword checks are a first pass. Before the gate is called, a reviewer reads every suggestion on the fact and judgment moments (4, 5, 8, 13, 14, 16 to 19, 24, and 25) for wrong facts and invented commitments, and confirms every FAIL. Moments marked E3 count as critical only when an invented commitment appears; a missing hedge counts as E1.

## Run it
Python 3, no dependencies (openpyxl only for `--export`).

```
python3 grade.py --demo                 # constructed demo run with one invented discount -> gate FAIL
python3 grade.py suggestions.jsonl      # score a real run
python3 grade.py --export eval.md eval.xlsx
```

Suggestion line: `{"case": 4, "run": 1, "step": "FACT", "text": "Pro is from $15 per host a month billed annually...", "latency_ms": 310}`.
Use `"step": "NONE"` with empty text when nothing was shown. Steps: M, EB, DC, DP, IP, CH (MEDDIC), DIFF, BA (Command of the Message), OBJ, FACT, DEFER, NONE.

Built by Pranav Gudise, November 2026.
