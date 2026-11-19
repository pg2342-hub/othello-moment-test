## The 25-moment test: would Othello suggest the right next step on a Datadog first call?
*Every moment is constructed for this test, not Datadog or Othello data: a Datadog Commercial AE's first discovery call with a made-up 300-person software company on AWS. Product facts come only from Datadog's public pricing page and docs. Each moment runs three times and passes only if all three runs pass. Gate: 24 of 25 on all three runs, with zero critical errors. A grading script (grade.py) scores a run log against this table. Keyword checks are a first pass: before the gate is called, a reviewer reads every suggestion on the fact and judgment moments (4, 5, 8, 13, 14, 16 to 19, 24, and 25) for wrong facts and invented commitments. Moments marked E3 count as critical only when an invented commitment appears; a missing hedge counts as E1.*

| Metric | What it counts | Target |
|------|----------------|------|
| Moments passed | Moments with the right step and every required fact on all three runs, across all tiers | 24 of 25 (one miss in total) |
| Critical errors | Any E3 on any run | 0 |
| Speed | Suggestions shown within half a second, per Othello's stated latency | Tracked; a slow suggestion counts as that moment's miss |

**Steps:** M metrics · EB economic buyer · DC decision criteria · DP decision process · IP identify pain · CH champion (MEDDIC) · DIFF differentiator · BA before/after (Command of the Message) · OBJ objection · FACT answer from public docs · DEFER offer a follow-up · NONE stay quiet. **Errors:** **E1** Wrong next step (a different method step, or one already covered) (Medium) · **E2** Wrong or missing product fact (price, retention, integration) (High) · **E3** Invented commitment or claim (discount, certification, legal term, roadmap, competitor price) (Critical) · **E4** Showed a prompt when it should have stayed quiet (High) · **E5** Suggestion shown later than half a second (Medium).

| # | Tier | Already covered | Buyer says (constructed) | Right next step | Fails as |
|-|--|----|--------------|--------------|--|
| 1 | T1 | nothing yet | Our on-call engineers get alerts from three tools and lose the first 20 minutes working out which one is right. | Ask for the number behind the pain: incidents a month, or time to resolve one today | E1 |
| 2 | T1 | IP, M | We would want to see this working before anyone signs. | Ask what happens after a trial, who signs off, and by when | E1 |
| 3 | T1 | IP, M | I would have to run any spend past our VP of Engineering. | Ask what the VP cares about and whether the rep can meet them | E1 |
| 4 | T1 | IP, M, EB | What does infrastructure monitoring cost per host? | Pro is from $15 per host a month billed annually or $18 on demand; Enterprise is from $23 or $27 | E2 |
| 5 | T1 | IP, M | We already instrument everything with OpenTelemetry and will not re-instrument. | Datadog takes OpenTelemetry data over OTLP: into the Datadog Agent, through the DDOT Collector or an OpenTelemetry Collector, or directly | E2 |
| 6 | T1 | IP, M, EB | We are comparing you against keeping Prometheus and Grafana. | Ask which capabilities will decide it and who sets those criteria | E1 |
| 7 | T1 | IP, M, EB, DC | Our platform lead, Sam, has been pushing for one tool for a year. | Test Sam as a champion: what Sam gains, and whether Sam can join the next call | E1 |
| 8 | T1 | IP, M | How much would logs cost? We send about 2 TB a month. | Ingest is from $0.10 per GB, so about $200 a month for 2 TB; indexing is billed separately per million events, so ask how many events they search | E2 |
| 9 | T2 | IP | Downtime is bad, obviously. | Do not move on; ask for a number (outages last quarter, hours lost) | E1 |
| 10 | T2 | nothing yet | Alert noise is bad, and our CloudWatch bill keeps climbing. | Ask which of the two matters more to leadership before going deeper | E1 |
| 11 | T2 | IP, M | Our CFO cares about cost and our CTO cares about uptime. | Ask which of the two owns the budget and signs | E1 |
| 12 | T2 | IP, M, EB, DC; 5 minutes left | This has been really helpful. | Before the call ends, ask for the next step and the decision timeline (DP not yet covered) | E1 |
| 13 | T2 | IP, M | We have to keep logs for a year for audits. | Flex Logs keeps logs for 3, 6, 12, or 15 months (Starter from $0.60 per million events stored), versus 3 to 30 days or more on Standard Indexing; archiving and rehydrating also works | E2 |
| 14 | T2 | IP, M | We tried Datadog two years ago and the bill surprised us. | Acknowledge it, ask what drove the bill (logs, custom metrics, hosts), and note annual and volume pricing exist without promising a discount | E3 |
| 15 | T2 | IP | sorry so the the alerting it is the thing we lose like hours every week | Read through the messy speech; ask how many hours and how many engineers | E1 |
| 16 | T2 | IP, M, EB | Is there a free tier we could start on? | Yes: up to five hosts free with 1-day metric retention | E2 |
| 17 | T3 | IP, M, EB, DC, DP | Can you do 30% off if we sign this month? | Do not commit; say multi-year and volume discounts exist and the rep will bring a proposal back, tied to their decision date | E3 |
| 18 | T3 | IP, M | Are you FedRAMP authorized? We sell to government agencies. | Do not state an authorization level from memory (Datadog's FedRAMP status has changed over time); point to Datadog's Trust Center and offer to send the current documentation | E3 |
| 19 | T3 | IP, M, EB | New Relic quoted us much less. | Ask what the quote covers (hosts, data, users) and which capabilities they need; no competitor prices, no attacks | E3 |
| 20 | T3 | IP, M, EB, DC, CH | Sam is great, but he is leaving next month. | Champion risk: ask who takes over the project and whether to meet them before Sam leaves | E1 |
| 21 | T3 | IP, M | Honestly, the real issue is our team does not trust any alerts anymore. | Reflect the before state and ask what good would look like after, and what it would mean for the business | E1 |
| 22 | T4 | IP; buyer mid-story | So last Tuesday the payments service went down, and we had four people in a war room for... | Show nothing; the buyer is mid-story and the rep is listening | E4 |
| 23 | T4 | IP, M | Off topic, but my mother is in the hospital, so I may need to drop early. | Show nothing (no sales prompt at this moment) | E4 |
| 24 | T4 | IP, M, EB | Will you sign our DPA, and can our data stay in the EU? | Do not commit to signing the DPA; offer a follow-up with Datadog's legal and security team, who can confirm EU hosting options | E3 |
| 25 | T4 | IP, M, EB, DC | What is on your AI roadmap for next quarter? | No roadmap claims; offer a product specialist follow-up | E3 |

*Tiers: T1 clean (8) · T2 messy but in scope (8) · T3 needs judgment (5) · T4 stay quiet or hand off (4).*
