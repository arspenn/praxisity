## Prompt Engineer Review

**Artifact:** SPEC-008 full artifact set — spec, design (DESIGN-007), v0.2 prototype, and live test outputs (Query_Report1, Research_Report1)
**Date:** 2026-04-09
**Dispatch Mode:** Mode 3 (collaborative team)

## Instructions Received

Review the full artifact set for SPEC-008 Portable Research Prompt before v0.3 implementation. Focus areas: whether v0.2 addressed v0.1 PE findings, new issues revealed by test data (unsolicited editorial sections, Wikipedia without distinction, generic landing page URLs), recommendations on three open design questions (DQ-1, DQ-2, DQ-3), and baseline comparison against the instructor's barebones prompt output.

---

## V0.1 Finding Remediation Assessment

### Fully Addressed

| V0.1 Finding | How V0.2 Fixed It | Confirmed by Test? |
|---|---|---|
| **#8 — Self-check theater** (HIGH) | Problem Log replaces pass/fail self-assessment. "Do not evaluate whether your work is good or bad. Just show what happened." | Yes — Problem Log produced 6 genuinely useful entries (unconfirmed links, data gaps, organizer claims, paraphrasing rationale, source contradictions) |
| **#9 — No opening orientation** (HIGH) | Scripted opening message delivered verbatim: "I'm going to help you research a topic through a structured process..." | Yes — test output structure is consistent with successful orientation |
| **#11 — Artifact panel not invoked** (HIGH) | "Create a document in the artifact panel" explicit in both report instructions | Yes — both artifacts appeared in artifact panel |
| **#1/#2 — Elephant instructions** (MED) | "Do not synthesize" / "Do not summarize" replaced with positive framing: "Quote directly," "Keep sources separate," "Preserve specifics" | Mostly — direct quotations are present throughout; but see unsolicited editorial sections below |
| **#6 — IEEE citation format** (MED) | Dropped entirely (DEC-3). Source list grouped by section. | Yes — consistent grouping across 40+ sources |
| **#5 — Domain-locked sources** (MED) | Kept public health defaults, owned as intentional (DEC-10). Added "Expand beyond these based on my guidance." | Yes — sources expanded well beyond PH defaults |
| **#12 — "Follow instructions exactly" noise** (LOW) | Removed. Opening is now "You are a research assistant guiding me through a structured process." | N/A |
| **#14 — Prompt underweight** (LOW) | v0.2 estimated ~1500 tokens, substantially more specific than v0.1's ~1100 | N/A |

### Partially Addressed

| V0.1 Finding | V0.2 Status | Gap |
|---|---|---|
| **#3 — Gathering collapse** (HIGH) | Sequential prose replaces numbered list (DEC-1). "Ask these questions ONE AT A TIME" reinforced. | Questions still fully visible in one block. Sonnet can read ahead and batch timeframe+geography. Design documents the fix; v0.2 improves but doesn't fully resolve. |
| **#7 — Vague link verification** (MED) | "Use web search to confirm it leads to the correct content" — more specific than v0.1 but doesn't prescribe the mechanism. | DEC-8 recommends "search for article title + source organization" — not yet in v0.2 text. NPR homepage citations in test output confirm this gap. |
| **#10 — No approval rejection handling** (LOW) | "I may ask you to adjust the plan. Do not begin researching until I approve." | Missing "change research question entirely -> return to gathering" path (documented in INT-3 but not in prompt). |

### Not Yet Implemented

| V0.1 Finding | Design Status | Notes |
|---|---|---|
| **#13 — No tone instruction** (MED) | DEC-7 specifies the fix. Not in v0.2. | One line: conversational during gathering, precise in reports. |
| **#4 — Accept whatever vs. draw out specifics** (LOW) | COMP-2 design says "one follow-up if very broad, then accept." Not in v0.2. | Needs adding for v0.3. |
| **#15 — No closing behavior** (LOW) | COMP-6 design defines three follow-up options. Not in v0.2. | Needs adding for v0.3. |

---

## New Issues from Test Data

### ISSUE-T1: Unsolicited "Public Health Relevance" Editorial Sections

**Location:** Research_Report1, every Topic Deep Dive (lines 64, 102, 135, 171, 203)

**What happened:** Sonnet appended a "**Public Health Relevance:**" subsection to each of the 5 topics. These contain unsolicited synthesis — the user asked for "top 5 trending topics," not public health analysis per topic.

**Root cause:** The Query Report scope says "findings should highlight topics with potential public health relevance, population-level impact, or policy implications where applicable." Sonnet wrote this into scope based on the audience being a "public health industry analyst." The scope statement *invited* these sections. The Output Structure defines Topic Deep Dives as containing "platform-by-platform sourcing, direct quotes, URLs" — but this definition lives in the Query Report, not the prompt, so it's Sonnet's own contract with itself, and Sonnet decided to extend it.

**Problem for AI:** The Output Structure contract isn't enforceable because it's generated, not embedded. Sonnet can (and did) extend its own contract.

**Problem for humans:** The editorial sections look valuable — they're arguably the most audience-relevant content. But they're unsourced synthesis, which undermines the report's verifiability.

**Recommended fix for v0.3:** Tighten the Output Structure definition *in the prompt* to specify the internal structure of each topic subsection. If the prompt says each topic contains only "platform-by-platform findings with direct quotes and URLs," there's no structural slot for editorial commentary. This is structural, not prohibitive. Do NOT add "do not add editorial sections" — that's an elephant.

---

### ISSUE-T2: Wikipedia Without Source Tier Distinction

**Location:** Research_Report1, Topics 1, 2, 3 (lines 62, 99-100, source list lines 215-217, 230, 243-244). 7 Wikipedia entries across the report.

**What happened:** Wikipedia appears alongside primary sources (NPR, CNN, NASA, Al Jazeera) with identical formatting. The "March 2026 No Kings protests" Wikipedia article is the source for the "8-9 million" attendance claim. The Problem Log notes the attendance figure is an organizer claim (entry 4) but doesn't identify the source tier issue.

**Root cause:** The prompt's Source Priority section lists only primary sources ("CDC, WHO, NIH...") and says "expand beyond these based on my guidance." Wikipedia isn't mentioned, so Sonnet treats it as equivalent to any other web source.

**Problem for AI:** Sonnet has no instruction to distinguish aggregation sources from primary reporting. It treats "Wikipedia says X" the same as "NASA says X."

**Problem for humans:** A verifier downstream can't tell which claims rest on primary sources vs. aggregation without reading every URL.

**Recommended fix for v0.3:** Add "Wikipedia or other secondary/aggregation sources used" as a fifth Problem Log category. This doesn't prohibit Wikipedia — which would lose useful context for aggregation and timelines — but makes the source tier visible and auditable. The downstream verifier can then decide whether to seek primary sources.

---

### ISSUE-T3: Generic Landing Page URLs Cited as Sources

**Location:** Research_Report1, lines 117 and 201 — both cite `https://www.npr.org/sections/national/`

**What happened:** Two NPR citations point to the NPR national news section landing page, not specific articles. Topic 3 uses it to source an Artemis II claim; Topic 5 uses it to source a higher education headline reference.

**Root cause:** Sonnet found content on a section/landing page via web search but couldn't locate the specific article URL. The prompt says "the URL you provide must point to the actual page where the information can be found" but the error handling plan doesn't cover the case where Sonnet found the content only on a landing page. Sonnet defaulted to citing what it had rather than flagging the gap.

**Problem for AI:** The link verification instruction ("use web search to confirm it leads to the correct content") doesn't distinguish between "I found the content on this page" and "this URL is a persistent link to the specific article."

**Problem for humans:** A verifier clicking these links lands on a news section front page that rotates daily — the cited content won't be there.

**Recommended fix for v0.3:** Add a fifth error handling scenario: "If you can only find a section or homepage URL rather than a specific article page, cite the source but mark it '[landing page only — specific article URL not found]' in the Problem Log." This extends the existing error-handling pattern (mark and log) rather than adding a prohibition. Also implement DEC-8's concrete verification mechanism: "search for article title + source organization" — this would have caught the NPR case because searching "Artemis II NPR" would return the specific article URL, not the section page.

---

### ISSUE-T4: Query Report Commits to Infeasible Search Phases

**Location:** Query_Report1, Phases 4 and 5 (Reddit/Quora/Medium, Instagram)

**What happened:** The Query Report committed to 5 search phases. The Problem Log honestly reports that Instagram data wasn't found (entry 2) and Reddit/Quora/Medium specifics weren't found (entry 3). Three of five search phases produced no platform-specific results.

**Root cause:** The search strategy was shaped by the user's research interests (which were themselves influenced by the instructor's original prompt that specified these platforms). The v0.2 prompt doesn't instruct Sonnet to assess feasibility of its planned search phases before committing to them.

**Problem for AI:** Sonnet commits to searches it can't execute, then must report failure in the Problem Log. The failures are honest but preventable.

**Problem for humans:** A user reviewing the Query Report sees 5 phases and expects 5 phases of results. Getting "no data found" for 3 of them undermines trust in the plan.

**Recommended fix for v0.3:** In COMP-3 (Query Report generation), add: "In the search strategy, only include search phases where web search is likely to return usable results. If a platform's trending data is not typically available through web search, note this as a known limitation rather than including it as a planned search phase."

---

### ISSUE-T5: Unsourced Claims in Editorial Sections

**Location:** Research_Report1, Public Health Relevance sections throughout

**What happened:** Claims in the editorial sections often lack specific source attribution. Example (line 172): "Oxford Economics' Bernard Yaros noted that..." — this is attributed to a person but has no URL or source title. Line 64: "The WHO identified 13 Iranian health infrastructure sites struck during the war" — attributed to WHO but no URL. These claims exist in the editorial sections that shouldn't be there per Issue T1, but if the editorial content were retained, the sourcing standard drops below the main findings.

**Root cause:** The prompt's sourcing rules ("Quote directly... The URL... source name and organization") apply to the Research Phase. Sonnet interprets its self-generated editorial sections as commentary rather than findings, so it applies a lower sourcing standard.

**Impact on v0.3:** Resolving ISSUE-T1 (removing unsolicited editorial sections via Output Structure tightening) eliminates this issue. No separate fix needed.

---

## Design Decision Assessment

| Decision | Assessment | Notes |
|---|---|---|
| DEC-1 (Sequential prose) | Sound, partially validated | Gathering didn't collapse in test. Remaining risk: questions visible in block. |
| DEC-2 (Problem Log) | Validated by test | Standout decision. 6 useful entries. |
| DEC-3 (Drop IEEE) | Validated | Source-by-section grouping is clean and auditable. |
| DEC-4 (Positive framing) | Mostly validated | Positive framing worked for research behavior; failed to prevent additive behavior (editorial sections). Needs Output Structure tightening. |
| DEC-5 (Fixed limitations text) | Validated | Reproduced verbatim in both artifacts. |
| DEC-6 (Two gates) | Sound | Query Report gate is the high-value one. |
| DEC-7 (Tone directive) | Not yet implemented | Add for v0.3. One line is sufficient. |
| DEC-8 (Link verification scope) | Not yet implemented in prompt | Design is correct; v0.2 prototype lacks the specific mechanism. Test data (NPR homepage) confirms the gap. |
| DEC-9 (Separate artifacts) | Validated | Both appeared independently in artifact panel. |
| DEC-10 (Domain-flexible with PH defaults) | Working | Defaults provided good starting point; expansion worked. |
| DEC-11 (Prompt brevity) | On track | ~1500 tokens leaves room for all missing components. |

---

## Open Question Recommendations

### DQ-1: Should the prompt explicitly instruct Sonnet to avoid editorial sections?

**Recommendation: Resolve — structural tightening, not prohibition.**

Do NOT add "do not add sections not defined in the Query Report." While this is better than "do not add editorial sections," it's still a prohibition that risks priming Sonnet to think about what extra sections it could add.

Instead, define the internal structure of Topic Deep Dives more precisely in the prompt's Output Structure instructions. Change COMP-5 to specify that each topic subsection contains:
- Platform-by-platform findings (which sources said what)
- Direct quotations with attribution
- URLs for each source

When the template is complete, there's no structural slot for commentary. The Output Structure contract in the *prompt* (not the Query Report) is the enforcement mechanism.

### DQ-2: Should Wikipedia be flagged differently from primary sources?

**Recommendation: Resolve — add Problem Log category.**

Add a fifth Problem Log category: "Instances where Wikipedia or other secondary/aggregation sources were used." Do not prohibit Wikipedia. The value of aggregation sources for timelines and event summaries is real. Making them visible in the Problem Log lets the downstream verifier decide whether to seek primary sources for those claims.

### DQ-3: How should the prompt handle generic landing page URLs?

**Recommendation: Resolve — add error handling scenario + implement DEC-8.**

Two changes:
1. Add a fifth error handling scenario: "If you can only find a section landing page or homepage URL rather than a specific article URL, include the source but mark it '[landing page only]' in the Problem Log."
2. Implement DEC-8's concrete verification mechanism in the prompt text: "For each source, search the web for the article title and source organization to confirm the URL points to the right content." This prescribes the action (search title + org) rather than the abstract goal (verify the link), and would catch the NPR case — searching "Artemis II record NPR" would return the specific article URL.

---

## Baseline Comparison Summary

v0.2 dramatically outperforms the instructor's barebones prompt on every quality dimension the spec targets:

| Dimension | Instructor Baseline | v0.2 Output |
|---|---|---|
| Source traceability | Generic source list at bottom, no per-claim attribution, no URLs | Per-claim attribution with quotations, URLs, source names |
| Verifiability | Not independently verifiable | Chain-ready — can be pasted into new conversation for verification |
| Problem transparency | None | 6-entry Problem Log identifying gaps, unconfirmed links, contradictions |
| Source depth | ~15 sources, no quotations | ~40 sources with direct quotations |
| Structural separation | Single artifact mixing intent and evidence | Two artifacts separating plan from findings |

The baseline wins on: simplicity (one prompt, one output), topic relevance to domain (public health-specific topics vs. general trending with PH angles), and session economy (fewer messages consumed).

The v0.2 prompt's value proposition is validated: a structured gathering+planning+research workflow produces fundamentally different — and for the spec's purposes, fundamentally better — output than a bare directive.

---

## V0.3 Implementation Priorities

### Must-have for v0.3

1. **Tighten Output Structure template in prompt** (resolves DQ-1, ISSUE-T1) — define the internal structure of each topic subsection so there's no slot for editorial commentary
2. **Implement DEC-8 verification mechanism** (resolves DQ-3, ISSUE-T3) — "search for article title + source organization" explicit in prompt text
3. **Add fifth Problem Log category** (resolves DQ-2, ISSUE-T2) — "Wikipedia or other secondary/aggregation sources used"
4. **Add fifth error handling scenario** (resolves DQ-3, ISSUE-T3) — landing page URL case
5. **Add feasibility constraint to search strategy** (resolves ISSUE-T4) — only commit to searchable phases

### Should-have for v0.3

6. **Implement DEC-7 tone directive** — one line, covers a real drift risk
7. **Add one-follow-up rule** (v0.1 finding #4) — "If my answer is very broad, you may ask one follow-up to narrow scope, then accept"
8. **Add closing block** (v0.1 finding #15, COMP-6) — three options: expand, add sources, revise
9. **Add approval rejection path** (v0.1 finding #10, INT-3) — "If I want to change the research question, return to gathering"

### Token budget check

v0.2 is ~1500 tokens. The 9 additions above are estimated at 200-300 additional tokens, bringing v0.3 to ~1800. Well within the 4000 minimum budget. There's room for all must-have and should-have items.

---

## What's Well-Engineered

- **Problem Log (DEC-2)** is the single best design decision in the artifact set. The test validated it completely — 6 entries with genuine audit value, zero self-congratulation. This pattern should be extracted as a reusable technique for other Praxisity prompts.

- **Positive framing of research rules (DEC-4)** works for behavioral constraints. "Quote directly," "keep sources separate," "preserve specifics" — these produced well-sourced, quotation-heavy findings. The v0.1 "don't synthesize" elephants are gone.

- **Fixed limitations statement (DEC-5)** was reproduced verbatim. Simple, reliable, correct.

- **Two-gate architecture (DEC-6)** balances user control with session economy. The Query Report approval gate is particularly valuable — it creates a contract that the research phase must follow.

- **Separation of artifacts (DEC-9)** produces genuinely independent verification targets. The Query Report and Research Report can each be verified in separate conversations.

- **Overall design quality** — the DESIGN-007 document is thorough, well-structured, and makes explicit tradeoffs at each decision point. The requirements coverage matrix (section 1.3) provides clean traceability from spec to design to component.

---

## Self-Evaluation

- **What worked well:** Having both the design document and live test data made this review substantially more concrete than v0.1. Every design claim could be checked against actual Sonnet behavior. The test data revealed issues (editorial sections, Wikipedia, landing pages, infeasible search phases) that design-only review would have missed. Cross-referencing v0.1 findings against v0.2 implementation gave a clear picture of what's been addressed vs. what's pending.

- **What I struggled with:** The "Public Health Relevance" editorial sections present a genuine tension. They're the most audience-relevant content in the report — exactly what a public health analyst would want. But they violate the prompt's structural intent and contain unsourced synthesis. My recommendation (tighten the template to exclude them) is correct for prompt engineering integrity but may sacrifice the most useful content for the target user. The user/lead should weigh whether the audience-value of these sections outweighs the verifiability cost, and if so, whether to make them an explicit part of the template with sourcing requirements.

- **Prompt improvement suggestions for my own agent prompt:** I would benefit from a standing catalog of "structural vs. prohibitive" fix patterns. I applied this principle correctly here (template tightening > "don't add sections") but I had to reason through it each time. A reference of known structural alternatives to common prohibitions — "instead of 'don't batch,' use sequential reveal; instead of 'don't synthesize,' use 'one source per block'; instead of 'don't add sections,' tighten the output template" — would make reviews faster and more consistent.