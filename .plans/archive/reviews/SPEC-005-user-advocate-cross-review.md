## User Advocate Cross-Review: Collective Agent Output Assessment

**Artifact:** All SPEC-005 agent reports (8 reports from 7 agents, including 2 fresh-eyes passes)
**Date:** 2026-03-29
**Purpose:** Evaluate whether a solo developer receiving all of these reports would know what to do with them

---

## The Experience of Receiving These Reports

A solo developer who runs a Mode 2 consultation and gets back 8 reports totaling roughly 25,000 words faces a specific problem: this is no longer a "quick multi-agent sanity check." It is a research project to read, cross-reference, and triage.

Here is what the developer actually receives:

| Report | Approximate length | Number of distinct findings |
|--------|-------------------|---------------------------|
| Critic | ~3,200 words | 8 findings (2 critical, 4 important, 2 minor) |
| Skeptic | ~2,800 words | 7 verdicts (2 overcomplicated, 1 premature, 1 unnecessary, 3 justified) |
| Designer | ~2,400 words | 7 assessments (2 structural, 2 coupling, 3 minor) |
| Project Manager | ~2,600 words | 4 assessments + dependency map |
| Consistency Reviewer | ~3,800 words | 7 issues + 20 verified consistencies |
| Prompt Engineer | ~3,000 words | 9 typed findings |
| Fresh-Eyes Reviewer (pass 1) | ~2,600 words | 8 issues |
| Fresh-Eyes Reviewer (pass 2) | ~2,400 words | 6 issues + 2 corrections of pass 1 |
| User Advocate (mine) | ~2,800 words | 7 findings (1 blocking, 3 friction, 3 minor) |

**Total: ~58 distinct findings across ~25,000 words.**

The developer must now: read all of these, identify which findings overlap, decide which to act on, figure out the priority order, and actually make the changes. Without a lead review synthesizing the output, the developer IS the synthesis engine.

---

## What Works: The Reports Are Individually High Quality

This is important to state clearly: each report, read on its own, is well-structured and actionable. The formats are consistent enough (severity ratings, specific locations, suggested fixes) that a developer reading any single report knows exactly what to do with it.

Specific strengths:

**The Critic's severity calibration is useful.** "Critical" vs. "Important" vs. "Minor" maps directly to triage decisions. The orphaned fresh-eyes-reviewer memory directory and the verification-claim-overstatement are genuinely critical findings that a solo developer would want to act on first.

**The Skeptic's verdict format is the most decision-friendly.** "Justified," "Overcomplicated," "Premature," "Unnecessary" — these are direct answers to "should I keep this?" A developer scanning the Skeptic's report can immediately see which parts of the system are challenged and which are endorsed. The "simpler alternative" sections are particularly actionable — they don't just say "this is too much," they say "here's what to do instead."

**The Consistency Reviewer's verified-consistencies section builds confidence.** 20 items confirmed correct is as valuable as 7 issues found. It tells the developer "these parts of the system are solid, don't worry about them." This is the only report that explicitly reduces the developer's anxiety rather than adding to it.

**The Project Manager's dependency map is the only report that sequences work.** The critical path (bootstrapping test -> real use -> SPEC-004 resume) gives the developer a concrete next step. The "proceed, don't block on fixes" recommendation is exactly what a solo developer needs to hear when facing 58 findings.

**The fresh-eyes reviewer's second pass correcting its own first pass is honest and useful.** Issue 5 from pass 1 (Mode 1 / AC-10 conflict) was retracted in pass 2 as a misread. This self-correction builds trust in the review process itself.

---

## What Doesn't Work: The Collective Output Is Overwhelming

### Problem 1: Massive duplication across reports

Multiple agents flag the same issues independently. This is by design (independent perspectives), but the developer pays the reading cost:

**The "What you ignore" / elephants problem** is flagged by:
- Prompt Engineer (Issue 2, primary analysis)
- Critic (Important finding, citing the PE report)
- Skeptic (implicitly, in the "What you ignore" sections they quote)

**The naming convention violation** is flagged by:
- Critic (Important finding, detailed file list)
- Consistency Reviewer (Issue 1, format deviation)
- User Advocate (Minor finding)

**Mode 3 experimental dependency risk** is flagged by:
- Critic (Important finding)
- Project Manager (Risk assessment)
- Designer (Minor finding)
- Skeptic (acknowledged but justified)

**The orphaned fresh-eyes-reviewer directory** is flagged by:
- Critic (Critical finding)
- (Only the Critic caught this, which validates having multiple perspectives — but the point is that many issues ARE caught multiple times)

A developer reading all 8 reports encounters roughly 15-20 findings that are substantively the same issue described from different angles. Each description adds nuance, but the developer must do the deduplication mentally. By the fourth report mentioning the elephants problem, the developer is skimming, not reading — and might miss the one novel detail buried in the fourth mention.

### Problem 2: No triage across reports

Each report has its own severity scale, and the scales don't align:

- Critic uses: Critical / Important / Minor
- Skeptic uses: Justified / Overcomplicated / Premature / Unnecessary
- Designer uses: Structural / Coupling / Minor
- User Advocate uses: Blocking / Friction / Minor
- Prompt Engineer uses: Noise / Elephants / Ambiguity / Drift / Clarity
- Consistency Reviewer uses: Important / Minor / Cosmetic
- Project Manager uses: Advisory / Risk
- Fresh-Eyes Reviewer uses: unmarked severity

These are all reasonable within their own context. But a developer trying to answer "what do I fix first?" cannot compare a Critic "Critical" against a Designer "Structural" against a User Advocate "Blocking." Are these the same priority? Different? The developer must build their own mental mapping.

### Problem 3: Contradictory recommendations without resolution

Several reports directly contradict each other:

**Agent count:** The Skeptic argues to reduce from 8 to 5 agents (merge Critic+Skeptic, Designer+Prompt Engineer, drop Stakeholder). The Project Manager says "agent differentiation is real" and the review cycle demonstrates non-overlapping findings. The Developer says the current count "composes well." Who is right? The developer must decide — but the reports don't acknowledge the disagreement across each other, because they were dispatched independently (Mode 2 snapshot).

**Reporting infrastructure:** The Skeptic calls it "overcomplicated" and says to drop lead reviews, instructions-received sections, and reconstitution notes. The Critic values the self-authored report principle (DEC-3). The Designer calls the report interface "healthy multi-writer design." The developer is told to simplify and to keep the current design in the same batch of reports.

**"Instructions Received" section:** The Critic says the verification claim is "performative, not real" and should be downgraded to "transparency." The Designer calls it "a clever verification mechanism." The Consistency Reviewer flags that no agent actually includes it in their output format. Three different assessments of the same feature.

**Memory: project:** The Skeptic says remove it (premature, no evidence it helps, the user's own memory research suggests marginal/negative impact). The Designer says it enables a feedback loop. Neither cites evidence specific to this system.

A solo developer reading these contradictions has no arbitrator. In a Mode 3 team, teammates could hash this out in real time. In Mode 2, the contradictions just land on the developer's desk unresolved.

### Problem 4: The lead review is missing, and its absence is felt

The session-report template defines a lead review format that synthesizes across agents: areas of agreement, disagreement, unresolved tensions. That review does not exist for this batch. Its absence is exactly the problem it was designed to solve. The developer is the lead reviewer by default, and they didn't sign up for that job.

The Skeptic's report actually calls the lead review template "overcomplicated" and suggests dropping it. The irony is that reading all 8 reports without a lead review is the strongest possible argument FOR a lead review.

---

## What Would Make This Output More Useful

### 1. The lead review is not optional — it is the user's primary interface to multi-agent output

For any Mode 2 dispatch of more than 2 agents, the lead review should be treated as required, not optional. It should contain:

- A deduplicated list of findings (each issue appears once, with citations to which agents flagged it)
- A single priority ranking that resolves cross-report severity differences
- Explicit flagging of contradictions between agents, with enough context for the developer to make a decision
- A short "act on this first" section (3-5 items maximum)

The individual reports become reference material — you read the lead review, and only dive into individual reports if you need the full analysis on a specific finding. This is the difference between 25,000 words as your primary reading and 1,500 words as your primary reading with 25,000 words available for reference.

### 2. Agents should be dispatched in smaller groups, not all at once

Eight reports is too many for a solo developer to process in one batch. The system already has the right primitive for this — Mode 1 (single expert consult). The natural flow for a solo developer is:

1. Draft the artifact
2. Get 1-2 targeted reviews (e.g., Critic + User Advocate for a user-facing spec)
3. Incorporate feedback
4. Get 1-2 more reviews if needed (e.g., Consistency Reviewer after changes, Skeptic if scope feels bloated)

This iterative approach produces fewer findings per round, gives the developer time to act between rounds, and naturally deduplicates (the second round of reviewers see the fixed version). Dispatching all 8 at once is the equivalent of scheduling every specialist appointment on the same day and then trying to reconcile all the advice at once.

The SKILL.md should include guidance on staged dispatch as a recommended pattern, not just "pick the perspectives that matter." Something like: "For most reviews, 2-3 agents per round is sufficient. Dispatch more rounds as needed rather than dispatching the full roster at once."

### 3. The severity/impact taxonomies should either be unified or the lead review should translate

If each agent keeps its own taxonomy (which is reasonable — "Structural" makes sense for the Designer in a way "Critical" doesn't), the lead review must be the Rosetta Stone that maps them to a single action priority. The developer should never have to hold 7 different severity scales in their head simultaneously.

### 4. Contradictions should be surfaced as explicit decision points, not buried in separate reports

When the Skeptic says "reduce to 5 agents" and the Project Manager says "differentiation is real," the developer needs to see these side by side with the evidence for each position. A lead review section called "Decisions for the developer" with 3-4 framed choices (here's Option A with its evidence, here's Option B with its evidence, here's what you lose with each) would transform contradictions from a burden into a feature.

---

## The Meta-Question: Does This Validate the System?

Yes, with caveats.

**The agents work.** They produce differentiated, specific, well-structured output. The Critic finds different things than the Skeptic. The Consistency Reviewer catches things nobody else does. The Prompt Engineer's elephants analysis is genuinely novel. The system delivers on its core promise of multi-perspective review.

**The output pipeline doesn't work for a solo developer yet.** The system produces expert-quality input but doesn't help the developer process it. The lead review is the missing piece. Without it, the system is like having 8 specialists each hand you their report and walk away — you got great analysis, but you're alone with 58 findings and no roadmap.

**The strongest evidence for Mode 3 over Mode 2 is this exact experience.** In a Mode 3 team, the Critic and Skeptic could argue about agent count in real time. The lead could write the synthesis while the team is still assembled. Contradictions would be surfaced and potentially resolved before they reach the developer. Mode 2's snapshot nature means every contradiction arrives unresolved.

---

## Self-Evaluation

- **What worked well:** Reading all reports before forming opinions, then stepping back to evaluate the experience holistically rather than report-by-report. The duplication count and contradiction inventory are the most concrete contributions — they give the developer (and the lead reviewer) specific things to address rather than a vague "it's a lot."

- **What I struggled with:** Separating "this is overwhelming because there are 8 reports" from "this is overwhelming because the reports are too long." Each report individually is well-sized. The problem is the collective, not the individual. I kept wanting to critique individual reports (the Skeptic's agent-merger proposal is underdeveloped, the Fresh-Eyes reviewer's corrections should have been edits to the original report rather than a separate file) — but that's the Critic's job, not mine. I had to keep pulling myself back to the user experience question.

- **Prompt improvement suggestions:** My agent prompt says to evaluate "whether a new user would understand and benefit." For a cross-review task like this, the question shifts to "whether a user can act on the collective output." My prompt doesn't give me guidance for evaluating the system's output as a whole — only individual features and flows. A framing like "after you've read all the material, ask: what does the user do next?" would be useful for meta-review tasks.
