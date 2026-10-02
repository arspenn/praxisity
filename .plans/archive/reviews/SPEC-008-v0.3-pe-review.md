## Prompt Engineer Review

**Artifact:** `.plans/references/portable-research-prompt-v0.3.md`
**Date:** 2026-04-14
**Dispatch Mode:** Mode 1 (direct review)

## Instructions Received

Review v0.3 of the portable research prompt for prompt engineering quality. This version is NOT the workshop deliverable — it's a high-end demo for participants who want to see serious prompt engineering, used on paid-tier Claude.ai where session limits are not binding. Cross-reference against v0.1 PE review findings and Mode 3 team findings. Assess whether it's ready as a paid-tier demo. Provide specific rewording for any issues found.

---

## V0.1 Finding Remediation — Final Status

Checking every v0.1 PE finding and Mode 3 team finding against the v0.3 text.

| V0.1 Finding | Status in v0.3 | Evidence |
|---|---|---|
| **#1/#2 — Elephant instructions** (MED) | **Fixed.** | "One source at a time" (line 60), "Keep the specifics" (line 62) — positive framing throughout. No "do not synthesize" or "do not summarize" anywhere in v0.3. |
| **#3 — Gathering collapse** (HIGH) | **Improved, residual risk.** | Questions are in sequential prose with "one at a time" + "Send one question, wait for my response, then send the next" (line 15). Questions still visible in one block. See ISSUE-1 below. |
| **#4 — Accept whatever vs. draw out specifics** (LOW) | **Fixed.** | "If my answer is very broad, ask one follow-up to narrow the scope, then accept whatever I give" (line 17). |
| **#5 — Domain-locked sources** (MED) | **Owned.** | Title is "public health research assistant" (line 1). Source list is explicitly PH (line 39). "Expand beyond these based on my guidance during gathering" (line 39). Design DEC-10 made this intentional. |
| **#6 — IEEE citation format** (MED) | **Fixed.** | Dropped entirely. Source list grouped by section (line 81). |
| **#7 — Vague link verification** (MED) | **Fixed.** | "Search the web for the article title and source organization. Confirm that the URL you cite appears in search results pointing to that content" (line 63). Concrete mechanism prescribed. |
| **#8 — Self-check theater** (HIGH) | **Fixed.** | Problem Log replaces self-check (lines 83-88). "The Problem Log shows what happened during research. It is not a self-assessment." (line 90). |
| **#9 — No opening orientation** (HIGH) | **Fixed.** | Scripted opening message at lines 7-9. Clear, sets expectations. |
| **#10 — No approval rejection handling** (LOW) | **Fixed.** | "If I ask for changes, revise the plan and present the updated version. If I want to change the research question, return to the gathering phase." (line 50). |
| **#11 — Artifact panel not invoked** (HIGH) | **Fixed.** | "Create a markdown document in the artifact panel" (line 70). |
| **#12 — "Follow instructions exactly" noise** (LOW) | **Fixed.** | Removed. Opens with role assignment. |
| **#13 — No tone instruction** (MED) | **Fixed.** | "Be conversational and brief during our conversation. In the report, be precise and formal." (line 3). |
| **#14 — Prompt underweight** (LOW) | **Addressed.** | v0.3 is substantially more specified than v0.1. Well within budget for paid tier. |
| **#15 — No closing behavior** (LOW) | **Fixed.** | "After Delivery" section (lines 96-97) with three options. |

### Mode 3 Team Findings — Status

| Team Finding | Status in v0.3 | Evidence |
|---|---|---|
| **PE-T1: Unsolicited editorial sections** | **Fixed.** | "Stick to the section headings defined in the research plan. Do not add sections that were not part of the approved plan." (line 79). Plus report structure is tightly defined (lines 73-78). |
| **PE-T2: Wikipedia without distinction** | **Fixed.** | Problem Log category added: "You used Wikipedia or another secondary/aggregation source" (line 88). |
| **PE-T3: Generic landing page URLs** | **Fixed.** | Error handling scenario added: "A URL points to a homepage or section landing page rather than a specific article" (line 48). Plus "Every URL must point to a specific page — not a homepage or section landing page" (line 64). |
| **PE-T4: Infeasible search phases** | **Fixed.** | "Only commit to searches you can actually perform with web search — if a platform's data is not accessible through web search (e.g., direct Instagram or Reddit searches), plan to search for news coverage or analytics reports about that platform's trends instead." (lines 37-38). |
| **Critic: Remaining elephant constructions** | **Fixed.** | No "do not" elephant constructions remain. The one "Do not add sections" in line 79 is a structural constraint, not an elephant — it references a concrete contract (the approved plan) rather than priming a behavior. |
| **Critic: Fixed limitations text paraphrased** | **Partially addressed.** | Fixed text is present (line 92) and uses a blockquote style. See ISSUE-4 below for residual concern. |
| **Critic: Problem Log entry #5 fabricated rationale** | **Partially addressed.** | "When you must describe rather than quote, stay as close to the original language as possible and log it in the Problem Log" (line 58). The instruction now links paraphrasing to logging but doesn't require a concrete reason. See ISSUE-3. |
| **Advocate: No post-conversation guidance** | **Not addressed.** | No instruction about what the user does with the output afterward. See ISSUE-6. |
| **Advocate: Prompt reads as AI instructions, not user guidance** | **Not addressed.** | No user-facing preamble. Acceptable for a "high-end demo" audience who are there specifically to see prompt engineering. |
| **Stakeholder: Output depth mismatched to question scope** | **Not directly addressable.** | This was a gathering-phase issue (user asked for "trending topics" generally). The v0.3 gathering phase has the one-follow-up rule (line 17) and domain focus (line 1) which would partially mitigate. |

---

## New Issues

### ISSUE-1: Ambiguity — "If I answered a question previously present that answer with each question for approval"

**Location:** Gathering Phase, line 15

**Problem for AI:** This sentence is grammatically broken. It's missing punctuation that separates two clauses. Claude will likely parse it as one of:
- (a) "If I answered a question previously, present that answer with each question for approval" — meaning: if the user already answered something in the initial message, show it back and confirm
- (b) "If I answered a question, previously present that answer with each question for approval" — which doesn't parse

Interpretation (a) is probably intended: if the user front-loads answers in their initial message, Claude should acknowledge those answers rather than re-asking. But the instruction is ambiguous enough that Claude might instead interpret it as "repeat all previous answers with each new question" — creating a growing summary that balloons each message.

**Problem for humans:** The sentence is hard to read. For a "high-end demo" that's meant to impress, this is a polish issue.

**Suggested fix:**

Replace:
> Ask these questions one at a time. Send one question, wait for my response, then send the next. If I answered a question previously present that answer with each question for approval.

With:
> Ask these questions one at a time. Send one question, wait for my response, then send the next. If I already answered a question in a previous message, confirm what you understood rather than re-asking.

---

### ISSUE-2: Noise — Research Plan section is doing double duty as output template AND behavioral instruction

**Location:** Research Plan, lines 29-50

**Problem for AI:** The Research Plan section defines what the plan should contain (output template) AND embeds behavioral instructions within those definitions. For example, "Only commit to searches you can actually perform with web search" (line 37) is a behavioral constraint living inside an output format spec. This mixing means Claude processes the behavioral instructions only when generating the plan, not when executing the research. If Claude's attention budget treats the Research Plan section as "template I've already used," it may deprioritize the behavioral constraints during the research phase itself.

The more critical example: the Error Handling section (lines 43-49) defines what to include in the plan, but the actual error handling behavior during research is governed by "follow the error handling plan from the research plan" (line 66). This creates a referential chain: prompt defines template -> Claude generates plan -> Claude follows its own plan. The plan is a self-generated contract, which the v0.2 test showed Claude will extend (adding "Public Health Relevance" sections).

**Problem for humans:** Not an issue — the structure reads clearly.

**Suggested fix:** This is acceptable for v0.3 given the design intent. The plan-as-contract architecture is the core innovation and is worth preserving. The risk is mitigated by the explicit instruction "Stick to the section headings defined in the research plan" (line 79) in the Research Report section, which constrains the output side. No change needed, but flag for testing: does Claude follow its own error handling plan during research, or does it drift?

---

### ISSUE-3: Ambiguity — Problem Log paraphrasing category lacks concrete reason requirement

**Location:** Problem Log, line 87

**Problem for AI:** "You described or summarized rather than quoting directly, and why" — the "and why" is vague. The Critic review (entry #5 analysis) showed Sonnet fabricating a plausible-sounding reason ("to comply with citation limits" — a constraint that doesn't exist). The v0.3 instruction says to log the "why" but doesn't specify what counts as a valid reason. Claude will manufacture rationales.

**Suggested fix:**

Replace:
> - You described or summarized rather than quoting directly, and why

With:
> - You described or summarized rather than quoting directly — state the specific reason (e.g., source was behind a paywall, search result showed only a snippet, original text was too long to quote in full)

This forces Claude into a closed set of concrete, checkable reasons rather than open-ended rationalization.

---

### ISSUE-4: Drift — Fixed limitations text may still be paraphrased

**Location:** Limitations section, line 92

**Problem for AI:** The Critic review found that Sonnet paraphrased the v0.2 limitations text despite "include this text exactly." The v0.3 version uses the same construction: 'Include this text exactly: "..."' The instruction hasn't changed in kind, only in wording. If the failure mode was "Sonnet paraphrases fixed text," the same instruction class will produce the same failure.

**Problem for humans:** The paraphrased version in v0.2 testing was "close enough" — it communicated the same message. For a demo, this may not matter.

**Suggested fix:** Two options, choose based on priority:

(a) Accept the paraphrasing risk. The v0.2 paraphrase was adequate. For a demo, "close enough" is fine. No change.

(b) If verbatim reproduction matters, wrap the text in a markdown code block within the prompt. Claude is more likely to reproduce code blocks verbatim than prose:

```
**Limitations** — Include this section with the following text:

> This report is AI-generated. All findings, sources, and links should be independently verified before being treated as reliable. Spot-check key claims by clicking through the source links and comparing the quoted text against the original.
```

I'd go with (a) for v0.3. The text is well-written and a close paraphrase still works.

---

### ISSUE-5: Clarity — "titled 'Research Report'" could produce wrong artifact title

**Location:** Research Report, line 70

**Problem for AI:** "Create a markdown document in the artifact panel titled 'Research Report'" — for a public health demo, the user might want the title to reflect their topic. Claude may use "Research Report" as a generic title when something like "Research Report: [Topic]" would be more useful. This is minor but affects the demo impression.

**Suggested fix:**

Replace:
> Create a markdown document in the artifact panel titled "Research Report".

With:
> Create a markdown document in the artifact panel. Title it with the research topic.

---

### ISSUE-6: Missing — No post-delivery guidance for verification

**Location:** After Delivery, lines 96-97

**Problem for AI:** Not an AI processing issue.

**Problem for humans:** The Advocate review flagged this clearly: "the user is never told what to do after the conversation ends." The v0.3 After Delivery section asks about expanding or revising but doesn't teach the user about verification. For a high-end demo meant to show "what serious prompt engineering looks like," the verification step IS the differentiator. A prompt that produces research AND teaches the user to verify it is more impressive than one that just produces research.

**Suggested fix:**

Replace:
> After delivering the report, ask if I want to expand any section, search for additional sources, or revise anything.

With:
> After delivering the report, tell me: "You can verify this report by starting a new conversation, pasting the report, and asking Claude to check the sources and claims. That verification should happen separately from this conversation." Then ask if I want to expand any section, search for additional sources, or revise anything first.

This teaches the verification concept in one sentence without jargon.

---

### ISSUE-7: Ambiguity — "present a research plan in the conversation (not as an artifact)"

**Location:** Research Plan, line 31

**Problem for AI:** "Present a research plan in the conversation (not as an artifact)" — the parenthetical is important because it prevents Claude from burning an artifact creation on the plan. However, the construction "(not as an artifact)" is a soft elephant. It puts "artifact" in Claude's processing at the plan stage, making it more salient. A stronger construction would be:

Replace:
> After I confirm, present a research plan in the conversation (not as an artifact) containing:

With:
> After I confirm, present a research plan in the conversation containing:

The artifact panel instruction only appears later in the Research Report section (line 70), which is the right place. Mentioning artifacts here is unnecessary — Claude defaults to inline responses unless told otherwise.

---

### ISSUE-8: Clarity — The report structure defines "Findings" loosely

**Location:** Research Report, lines 74-78

**Problem for AI:** The Findings section says "organized by the section headings defined in the research plan" and each finding should include "the specific information, quoted directly where possible / the source name and organization / the URL." This is good but doesn't define the INTERNAL structure of each section. The v0.2 test showed that when the internal structure isn't defined, Claude adds subsections (like "Public Health Relevance").

v0.3 adds "Stick to the section headings defined in the research plan. Do not add sections that were not part of the approved plan." (line 79). This is a prohibition, but it's attached to a concrete contract (the approved plan), which makes it enforceable rather than an elephant. The question is whether "sections" is precise enough — Claude might interpret "Public Health Relevance" as a subsection within a topic, not a new section.

**Suggested fix:**

Replace:
> Stick to the section headings defined in the research plan. Do not add sections that were not part of the approved plan.

With:
> Stick to the structure defined in the research plan. Do not add sections, subsections, or commentary categories that were not part of the approved plan.

Adding "subsections" and "commentary categories" closes the interpretive gap.

---

## Is This Ready as a High-End Demo?

**Nearly.** The v0.3 prompt is well-engineered and addresses the substantial majority of issues identified across three rounds of review. Someone pasting this into paid-tier Claude.ai will get an impressive result: a structured gathering phase, an approval gate, sourced research with direct quotations, and a Problem Log that demonstrates genuine transparency.

**What would make it demo-ready:**

1. Fix the grammatical break in line 15 (ISSUE-1) — this is the most visible quality issue for someone reading the prompt itself.
2. Tighten the paraphrasing reason in the Problem Log (ISSUE-3) — this prevents the fabricated-rationale failure mode that was the weakest point in v0.2 testing.
3. Add "subsections" to the structural constraint (ISSUE-8) — this closes the gap that produced the "Public Health Relevance" editorial sections in v0.2.
4. Add post-delivery verification guidance (ISSUE-6) — this is what elevates the prompt from "good research tool" to "teaches you how to use AI responsibly," which is the demo's selling point.

The remaining issues (ISSUE-2, 4, 5, 7) are refinements, not blockers.

---

## What's Well-Engineered

**The prompt has matured significantly across three iterations.** The progression from v0.1 to v0.3 demonstrates exactly what iterative review produces: v0.1 had 15 findings, v0.3 has resolved 14 of them substantively.

**The Research Plan as approval gate is the architectural centerpiece and it's well-executed.** The plan contains scope, search strategy, source priority, report structure, AND error handling — all user-reviewable before research begins. The instruction to present it in the conversation (not as an artifact) is correct: it keeps the plan in the conversational flow where the user can modify it naturally.

**The Problem Log categories are comprehensive and well-chosen.** Five categories (unconfirmed links, contradictions, unsourceable claims, paraphrasing, Wikipedia/secondary sources) cover the failure modes revealed by v0.2 testing. The closing line "The Problem Log shows what happened during research. It is not a self-assessment." is excellent — it's a behavioral frame that prevents the "All checks passed" theater.

**Error handling pre-commitment with five scenarios is thorough.** The addition of the landing-page-URL scenario (from ISSUE-T3) and the infeasible-search-phase constraint (from ISSUE-T4) show the prompt learning from test data. The error handling section is the strongest example of "structure over prohibition" in the prompt.

**Tone instruction is minimal and effective.** "Be conversational and brief during our conversation. In the report, be precise and formal." — two registers, one line. This will produce consistent behavior across sessions.

**The gathering phase flow is well-paced.** Topic -> audience -> timeframe -> geography -> anything else -> confirm. Each question builds on the previous. The one-follow-up rule for broad answers is correctly calibrated. The confirmation step before proceeding creates a natural checkpoint.

**Link verification has a concrete, actionable mechanism.** "Search the web for the article title and source organization. Confirm that the URL you cite appears in search results" — this prescribes the action rather than the goal, which is the right level of specificity for this behavior.

---

## Self-Evaluation

- **What worked well:** Cross-referencing against a specific finding list (v0.1 review + 4 Mode 3 reports) made this review systematic rather than impressionistic. The finding-by-finding remediation table at the top gives a clear audit trail. Having v0.2 test outputs as evidence of actual model behavior grounded every assessment — I could say "this will happen" because it already happened in testing.

- **What I struggled with:** Calibrating severity for a "high-end demo" context vs. a "production tool" context. Several issues that would be important for a production tool (ISSUE-2, ISSUE-4) are refinements for a demo. I had to resist the instinct to flag everything as critical and instead ask "would a paid-tier user pasting this be impressed?" — the answer is yes for most of the prompt, with specific fixes to close the remaining gaps.

- **Prompt improvement suggestions:** My own process would benefit from a standing template for "remediation audit" — a structured way to check each previous finding against the current version. I built the table ad hoc this time; having it as a reusable pattern would be faster and ensure nothing is missed. I should also maintain a catalog of "fixed in v0.N" annotations so that future reviews don't re-litigate resolved issues.