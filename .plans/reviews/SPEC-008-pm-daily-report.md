# Project Manager Daily Report: SPEC-008 Portable Research Prompt

**Artifact:** SPEC-008 full artifact set (spec, design, v0.2 prompt, test outputs, instructor baseline, PE review)
**Date:** 2026-04-09
**Dispatch Mode:** Mode 3 (Collaborative Team)

---

## Instructions Received

Assigned as PM teammate on a collaborative review of SPEC-008. Special responsibilities beyond normal PM duties:

1. **Coordination** — Read teammate reports, identify overlaps, contradictions, gaps. Message teammates directly if needed.
2. **Issue breakdown** — Take all findings and create discrete, actionable tasks. Prioritize them.
3. **Daily report** — Summarize each agent's findings, capture reasoning chains, identify agreement/disagreement, list unresolved tensions, propose sequenced action plan for v0.3.
4. **Scope guard** — Flag anything that belongs in future work, not this iteration.

Materials reviewed: spec, design (DESIGN-007), v0.2 prompt, Query Report test output, Research Report test output, instructor baseline, PE review of v0.1, clarity check.

---

## Feasibility Assessment

### [Impact: Advisory] — This project is well-scoped and realistic for a solo developer

**What's planned:** Iterate v0.2 prompt to v0.3 based on this review session's findings.

**Assessment:** The v0.2 -> v0.3 increment is a single-file change (one prompt document). The dependency chain is linear: spec -> design -> prompt -> test -> review -> revise. No infrastructure, no deployment, no code. Each iteration can be tested in under an hour by pasting into a free Claude.ai conversation. This is one of the most feasible deliverables I've seen — the blast radius of each change is small, feedback loops are fast, and rollback is trivial (keep the old prompt).

**No adjustment needed.**

---

### [Impact: Risk] — Session limit viability is the one untestable constraint

**What's planned:** The full prompt workflow (Orient -> Gather -> Plan -> Research -> Deliver) must complete within a single free-tier session.

**Concern:** Free-tier session limits are unpublished and dynamic. The design (DEC-11) explicitly defers this to "test empirically and iterate." This is pragmatic — there is no engineering solution to an unpublished constraint — but it means v0.3 must include a session viability test as part of its testing plan. If the prompt consistently hits limits before completing research, the entire architecture needs to compress or split, which would be a significant scope change.

**Suggested adjustment:** Add a v0.3 testing criterion: "Complete full workflow (paste to both artifacts delivered) within one session, at least 2 out of 3 test runs." If this fails, the next iteration must prioritize token compression before any feature additions.

---

### [Impact: Advisory] — Three open design questions have candidate solutions ready

**What's planned:** DQ-1 (editorial sections), DQ-2 (Wikipedia flagging), DQ-3 (generic landing page URLs) are marked Open in the design.

**Assessment:** All three have candidate instructions written in the design document. None require architectural changes — they are each one sentence added to the prompt. The v0.2 test produced evidence for all three (unsolicited "Public Health Relevance" sections, Wikipedia used for aggregation data, NPR homepage cited). These can all be resolved in v0.3 with low risk.

**No adjustment needed** — just close them during v0.3 implementation.

---

### [Impact: Advisory] — The dependency chain is clean and linear

**What's planned:** The overall workflow is: spec -> design -> v0.1 prompt -> PE review -> v0.2 prompt -> v0.2 test -> this review session -> v0.3 prompt -> v0.3 test.

**Assessment:** No circular dependencies. No parallel workstreams that need to merge. The critical path is straightforward: this review session produces findings -> developer synthesizes -> v0.3 prompt is written -> v0.3 is tested. The only blocking dependency for v0.3 is this review session completing.

---

## Dependency Map

```
SPEC-008 (done) ─────► DESIGN-007 (done) ─────► v0.2 prompt (done)
                                                      │
                                                      ▼
                                              v0.2 test (done)
                                                      │
                                                      ▼
                                         This review session (in progress)
                                                      │
                                    ┌─────────────────┼─────────────────┐
                                    │                 │                 │
                              PE report        Advocate report    Critic report
                                    │                 │                 │
                                    └─────────────────┼─────────────────┘
                                                      │
                                                      ▼
                                            PM daily report (this)
                                                      │
                                                      ▼
                                       Developer synthesizes findings
                                                      │
                                                      ▼
                                              v0.3 prompt written
                                                      │
                                                      ▼
                                              v0.3 test & iterate
```

**Critical path:** Teammate reports -> this PM report -> developer synthesis -> v0.3 prompt.

Nothing on the critical path is blocked by external dependencies. The only external dependency (Claude.ai free tier continuing to support web search and artifacts) is stable and assumed.

---

## Analysis by Domain

### Project Scope

The spec's out-of-scope section (Section 8) is crisp: no framework integration, no multi-conversation workflows, no paid features, no prompt generation tooling. The design stays within these boundaries. I found no scope creep in the design document.

**One scope risk to watch:** The design mentions "downstream prompt chaining" throughout (DEC-9, DATA-2, REQ-F13). The chain-readiness objective is in-scope, but any review agent that starts designing the downstream verification prompt or the prompt chaining workflow is drifting out of scope. The v0.3 deliverable is one prompt, not a pipeline. I will flag this if it appears in teammate reports.

### v0.2 Test Evidence — PM Observations

The v0.2 prompt was tested live. Key observations from the test outputs:

1. **The prompt works.** Both artifacts were produced. The Query Report is well-structured with clear search strategy and error handling. The Research Report has direct quotations, attributed sources, and a functional Problem Log.

2. **The v0.2 output substantially outperforms the instructor baseline.** The instructor's barebones prompt produced a single artifact with no sources, no verification, no quotations, and no problem log. The v0.2 produced two structured artifacts with ~50 cited sources, direct quotations, and six documented problems. This is not a marginal improvement — it demonstrates the value proposition of the prompt.

3. **v0.2 test exposed real issues that the design already anticipated:**
   - Unsolicited "Public Health Relevance" sections added to each topic (DQ-1)
   - Wikipedia used without distinction from primary sources (DQ-2)
   - NPR homepage cited twice instead of specific articles (DQ-3)
   - Only 1 out of ~50 links marked [link unconfirmed] — either verification worked well or was performed superficially

4. **The Problem Log worked.** Six entries documenting real issues: an unconfirmed link, two platform gaps (Instagram, Reddit specifics), unverified protest attendance figures, paraphrasing instances, and a source contradiction. This validates the "show your work" design decision (DEC-2).

5. **The research chose general trending topics, not public health topics.** The instructor baseline focused on public health-specific topics (measles, GLP-1, mental health). The v0.2 output found general trending topics (Iran war, protests, Artemis) and appended "Public Health Relevance" sections to justify each. This is arguably the right interpretation of the gathering results, but it's worth noting as a domain-focus question for v0.3 testing.

### What's Realistic for v0.3

The v0.3 increment should be **tightening, not expanding.** Based on materials reviewed:

- Closing DQ-1, DQ-2, DQ-3 with their candidate instructions: ~3 sentences added to prompt
- Strengthening one-at-a-time gathering reinforcement: minor text change
- Clarifying link verification mechanism (if PE recommends changes): minor text change
- Testing session viability: 2-3 test runs

This is realistically a **half-day of work** for the developer: revise the prompt text, test 2-3 times, document results. No new architecture, no new components, no new dependencies.

---

## Teammate Report Status

As of report writing, teammate reports have not been written to disk. Tasks completed by each agent:

**Prompt Engineer:** Completed v0.1 finding remediation check (#1), test output failure analysis (#2), design decision evaluation (#3), baseline comparison (#4 in progress). Report (#5) pending.

**User Advocate:** Completed first-impression review (#6), test output evaluation (#7), Problem Log assessment (#8), baseline comparison (#9), prompt chaining assessment (#10). Report (#11) in progress.

**Critic:** Report (#12) in progress — reviewing the full artifact set across six angles: domain-agnostic vs hardcoded defaults, chain-ready vs publication-ready, lethal trifecta circularity, Problem Log compliance theater, token budget mismatch, unnecessary design decisions.

I will update this section and the action plan below when teammate reports are available. The feasibility assessment and dependency map above are based on my independent analysis of the source materials and are not affected by teammate findings.

---

## Anticipated Areas of Agreement (Pre-Reports)

Based on the tasks completed and the materials reviewed:

1. **v0.2 is a significant improvement over v0.1.** The PE review of v0.1 found 15 issues. The v0.2 prompt addressed the highest-priority ones (orientation block, artifact panel instruction, gathering pacing, positive framing over prohibition, show-your-work Problem Log).

2. **The Problem Log is the right replacement for self-assessment.** The v0.1 PE review argued self-check is theater. The design chose Problem Log. The v0.2 test validated it produces real, useful entries.

3. **DQ-1, DQ-2, DQ-3 should be resolved in v0.3.** The test evidence makes all three concrete.

## Anticipated Areas of Disagreement

1. **Whether the prompt is domain-specific or domain-agnostic.** The spec says domain-agnostic (Section 8: "specific domain content" is out of scope). The prompt has public health defaults (CDC, WHO, NIH). The PE v0.1 review flagged this (finding #5). The critic is likely reviewing this angle. The design explicitly chose "domain-flexible with PH defaults" (DEC-10) and defers generalization. This is a reasonable v0.3 deferral — the first user is a public health intern.

2. **Whether link verification is genuine or theater.** Only 1 of ~50 links marked unconfirmed in the test. Either Sonnet is actually verifying well, or it's claiming to verify without searching. The PE will likely have a view on this. The design (DEC-8) specifies "search for title + org" as the mechanism, but we can't tell from the output whether Sonnet actually performed those searches.

3. **Whether the unsolicited "Public Health Relevance" sections are a bug or a feature.** From a PM perspective, they represent unrequested synthesis — the prompt didn't ask for them. But from a user advocacy perspective, a public health analyst might actually want them. The design (DQ-1) proposes "stick to Query Report headings," which would remove them. The tension is between prompt compliance and user value.

---

## Scope Guard

The following items are **deferred and should not be addressed in v0.3**:

| Item | Why It's Deferred |
|------|-------------------|
| Framework integration (making this a Praxisity skill) | Spec Section 8: explicitly out of scope |
| Prompt generation tooling / templating | Spec Section 8: explicitly out of scope |
| Multi-conversation verification workflow | Spec Section 8: explicitly out of scope |
| Domain generalization (removing PH defaults) | DEC-10: "test one first, generalize later" — correct for solo dev |
| Downstream verification prompt design | Not in spec; chain-readiness is in scope, the chain itself is not |
| Publication-ready citation formatting | DEC-3: "downstream prompt's job" |

If any teammate report recommends work in these areas, it should be acknowledged as future work, not added to the v0.3 scope.

---

## Proposed Action Plan for v0.3

Sequenced by dependency and priority:

| Order | Action | Dependency | Effort | Rationale |
|-------|--------|------------|--------|-----------|
| 1 | Close DQ-1: Add "stick to Query Report headings" instruction | None | 1 sentence | Prevents unsolicited editorial sections. Test evidence supports this. |
| 2 | Close DQ-2: Add "flag Wikipedia as secondary/aggregation source in Problem Log" | None | 1 sentence | Test showed Wikipedia used without distinction. Low risk. |
| 3 | Close DQ-3: Add "every URL must point to a specific page, not a homepage" | None | 1 sentence | Test showed NPR homepage cited. Low risk. |
| 4 | Strengthen gathering one-at-a-time reinforcement | None | Minor text revision | PE v0.1 review highest priority. v0.2 may have addressed; verify in testing. |
| 5 | Review and tighten link verification instruction based on PE findings | PE report | Minor text revision | DEC-8 has the mechanism; may need reinforcement. |
| 6 | Token audit | Steps 1-5 complete | Measurement | Verify prompt stays under 6000 tokens after additions. |
| 7 | Session viability test | Steps 1-6 complete | 2-3 test runs | Verify full workflow completes within one free-tier session. |
| 8 | Source quality spot-check | Step 7 complete | Manual review | Check 5+ URLs from test output for correctness. |

**Estimated total effort:** Half a day for a solo developer.

---

## Unresolved Tensions Requiring Developer Input

1. **Domain specificity vs. generalization timing.** The prompt has PH defaults and the first user is a PH intern. When does generalization happen? After the internship deliverable is done? After v0.3? This affects whether DEC-10 stays as-is or needs a follow-up task.

2. **Link verification trustworthiness.** We cannot tell from the test output whether Sonnet actually performed web searches for each link. The only signal is the Problem Log (1 unconfirmed out of ~50). Is this good enough? Should v0.3 include a manual spot-check of 5+ links as part of the testing plan, or should the prompt instruction be strengthened?

3. **"Public Health Relevance" sections — remove or formalize?** DQ-1's candidate instruction would remove them. But the user is a public health analyst. Should the prompt instead instruct Sonnet to include a "Relevance to [audience]" section as an explicit part of the Query Report's output structure, so it's requested rather than unsolicited?

---

## What's Well-Planned

- **The artifact chain is clean and evidence-based.** Each iteration builds on tested results, not speculation. The v0.2 test produced concrete evidence that drives specific design refinements. This is exactly how iterative development should work.

- **The spec's out-of-scope boundaries are sharp.** No ambiguity about what v0.3 should NOT include. This protects against scope creep.

- **The design decisions are documented with rationale and alternatives.** DEC-1 through DEC-11 each explain why, what was rejected, and what trade-offs were accepted. This makes review efficient and makes future revisits possible without re-arguing from scratch.

- **The v0.3 increment is appropriately sized.** It's tightening, not expanding. Three one-sentence additions, possible minor text revisions, and testing. This is achievable in a single session.

- **The testing strategy is concrete and prioritized.** The design's testing matrix (Section 7.3) covers the right angles: smoke test, gathering pacing, source quality, quote fidelity, Problem Log honesty, non-technical user test, token measurement, session viability, chain readiness, baseline comparison.

---

## Self-Evaluation

- **What worked well:** Reading all source materials before checking teammate status gave me a complete independent view. I can assess feasibility, dependencies, and scope without being influenced by teammate framings. The PM perspective is most useful when it's orthogonal to the technical and user-experience perspectives.

- **What I struggled with:** I could not read teammate reports because they haven't been written yet. My "anticipated areas of agreement/disagreement" are predictions based on the materials, not confirmed findings. This report should be updated when reports arrive. The chain of reasoning section is limited without the actual arguments from each agent.

- **Prompt improvement suggestions:** The PM agent prompt should include guidance on what to do when teammate reports are delayed — specifically, whether to write the PM report based on source materials alone or wait indefinitely. The current instruction ("wait for teammate reports to come in before writing your daily report") creates a blocking dependency that this report partially violates by proceeding with what's available. A better instruction would be: "Begin your analysis immediately from source materials. Incorporate teammate findings as they arrive. Write your report when you have enough to be useful, even if some reports are still pending."