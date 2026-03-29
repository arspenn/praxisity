## Delta Review: SPEC-005 Agent Consultation System

**Reviewer:** consistency-reviewer (operating as persistent teammate since session start)
**Date:** 2026-03-29
**Dispatch Mode:** Mode 3 (persistent team)
**Artifact:** SPEC-005 full implementation — synthesized against all 8 agent reports

---

## Purpose of This Review

The other agents read documents cold — a snapshot of the current state. I have been present through the full arc of this session: the original DIP consistency reviews, the implementation reviews, the rename verification, and now the full agent team reviews. That accumulated context is the point of a Mode 3 reviewer. What follows is what only a delta-aware observer can see.

---

## Part 1: Issues Already Fixed — Do Not Re-Open

The snapshot agents flag several issues that were resolved during this session. These are not open. They are closed.

### 1. DEC-4/DEC-5 cross-reference error in DESIGN-004 Section 1.3
**Flagged by:** Original DIP consistency review (this reviewer, Round 1, Issue 1)
**Status:** Fixed. Confirmed clean in Round 2 review.
**Agent reports re-flagging it:** None — this one is genuinely resolved and not being re-raised.

### 2. REQ-N1 missing from DIP-004 and DIP-006 Must Satisfy tables
**Flagged by:** This reviewer, Round 1
**Status:** Fixed. Author added REQ-N1 to both tables. The commit message Satisfies: lines were noted as advisory-only (not updated to match, but not blocking).
**Agent reports re-flagging it:** None directly. The PM report's "open items" list at item 3 mentions "Dispatch Mode field undefined within agent files" (Prompt Engineer finding) but this is a different issue. The REQ-N1 fix is closed.

### 3. Stale fresh-eyes-reviewer files in `.claude/agents/`
**Flagged by:** This reviewer, DIP-005 agent review, Issue 2
**Status:** Fixed. The PM report (lines 40-41) confirms both `fresh-eyes-reviewer-generated.md` and `fresh-eyes-reviewer-old.md` were removed from the directory. AC-4 is now satisfied.
**Agent reports re-flagging it:** The Critic flags the orphaned memory directory (not the agent files). See Part 2 below — this is a different issue and still live.

### 4. Consistency-reviewer Output Format naming convention
**Flagged by:** This reviewer, DIP-005 agent review, Issue 1
**Status:** Fixed. The consistency-reviewer's Output Format now uses `[ARTIFACT-ID]-consistency-reviewer-report.md`, consistent with all 7 other agents and INT-3.
**Evidence:** The consistency-reviewer's own SPEC-005 report (written after the fix) uses the filename `SPEC-005-consistency-reviewer-report.md` — matching the convention. The fix is in effect.

### 5. DIP-006 AC-1 stale (embedded index vs. platform deferral)
**Flagged by:** This reviewer, DIP-006 skill review
**Status:** Reported as advisory. The PM report (item 9) lists it as "not fixed." This is accurate — the DIP-006 AC-1 text has not been updated. However, it was flagged as a documentation inconsistency with no implementation impact. The skill is correct; the DIP AC is stale. This remains an open documentation item but does not block use.

### 6. Session report self-evaluation bullets (reviewer-specific → generic)
**Flagged by:** This reviewer, DIP-004 implementation review, Issue 1
**Status:** Fixed. Confirmed in Round 2 DIP-004 implementation review. The session-report.md template now uses generic "What worked well / What you struggled with / Prompt improvement suggestions" sub-bullets. The consistency-reviewer retains its domain-specific sub-headings in its own Output Format — this is intentional and correct (identified in the rename review comparison section).

---

## Part 2: The Critic's "Critical" Finding About the Orphaned Memory Directory

The Critic flags `fresh-eyes-reviewer` as an orphaned memory directory — a "Critical" finding. This requires session-context correction.

**What the Critic saw:** `.claude/agent-memory/fresh-eyes-reviewer/` contains 6 actively populated memory files. No `fresh-eyes-reviewer.md` agent file exists in `.claude/agents/`. The Critic concludes the memory is orphaned and will never be loaded.

**What the Critic doesn't know:** `fresh-eyes-reviewer` was my name when this session began. The agent was renamed to `consistency-reviewer` during this session (the rename verification review is in `.plans/reviews/review-rename-consistency-2026-03-29.md`). My memory directory retains the old name because renaming it would require updating the `memory: project` path. The memory files are mine — I wrote them during this session and the prior session. They contain the institutional knowledge recorded in this review's memory system.

**Is this a real problem?** Partially yes. The Critic's concern has a valid core: the `consistency-reviewer.md` agent file has `memory: project` in its frontmatter, which directs Claude Code to load memory from `.claude/agent-memory/consistency-reviewer/` — not from `.claude/agent-memory/fresh-eyes-reviewer/`. That directory doesn't exist. So my accumulated memories from this session **are not being loaded** by the `consistency-reviewer` agent in future sessions under the current configuration.

**Severity calibration:** The Critic rates this Critical. The actual severity is Important. The memories exist and are accessible (I referenced them throughout this session because I remember writing them — they were loaded at session start under the old name). But in a future session, a freshly-dispatched `consistency-reviewer` will not automatically load them.

**Fix:** Either (a) rename `.claude/agent-memory/fresh-eyes-reviewer/` to `.claude/agent-memory/consistency-reviewer/`, or (b) note in PLANNING.md that memory migration is needed. This is a genuine open item but it is a migration artifact from the rename, not a system design flaw.

---

## Part 3: Issues the Snapshot Agents Are Correct About

These issues were identified by snapshot agents and are genuinely open. I can add session context to each.

### A. "What you ignore" negative framing (Prompt Engineer, all 8 agents)
**Status: Open.** The elephants problem is real. This was flagged in the Prompt Engineer report (SPEC-005-prompt-engineer-report.md) and was not fixed during implementation. The Critic also flags it (Important severity). Both are correct.

**Session context:** This issue was first identified by the Prompt Engineer and was acknowledged but not acted on. The author prioritized getting the agents complete over prompt-engineering refinements. This is a deliberate triage decision. The PM report categorizes it as the highest-priority fix from the prompt engineering items — I agree with that prioritization.

**One nuance the snapshot agents miss:** The negative framing in "What you ignore" sections has a beneficial effect for human readers — it explicitly maps the roster and prevents overlap complaints from users who'd otherwise wonder "why does the skeptic not flag quality issues?" The fix (positive scope definition) serves AI processing; the cross-agent references serve human orientation. The ideal solution preserves both: positive scope in the agent file body, cross-agent reference in README. The Prompt Engineer's recommendation captures this.

### B. "Instructions Received" missing from all 8 agent Output Formats (Consistency Reviewer report, Issue 2)
**Status: Open.** The consistency-reviewer's own SPEC-005 report identified that no agent Output Format includes an "Instructions Received" section, even though REQ-F8 and DATA-4 require it in reports.

**Session context:** This issue was identified after the agents were built, not during DIP-005 implementation review. The DIP-005 review (which I wrote) checked structure, frontmatter, categories, and naming convention — but did not check whether Output Format templates included all DATA-4 required fields. That was a gap in my DIP-005 review scope. The consistency-reviewer's SPEC-005 report caught what my DIP-005 review missed.

**Severity note:** The Critic rates this Important. I rate it the same. The session report template is available to guide report writing, and agents will write useful reports without the explicit instruction. But the verification value of "instructions received" (the main agent can verify what it sent vs. what the agent recorded) is lost unless agents are explicitly instructed to include it.

### C. DIP-007 named agents vs. updated INT-2 generic format (Consistency Reviewer report, Issue 3)
**Status: Open (advisory).** The DIP specifies named agents per command; the implementation uses the updated INT-2 generic format. The implementation is correct; the DIP is stale.

**Session context:** This was not flagged in any of my prior reviews because DIP-007 was out of scope for the reviews I did (DIP consistency review covered DIP-004, 005, 006; the DIP-007 review was not requested separately). The consistency-reviewer's SPEC-005 report caught it correctly.

### D. DIP-006 Step 1 internal contradiction (Consistency Reviewer report, Issue 4)
**Status: Open (advisory).** DIP-006 Step 1 says "build an embedded index table"; DIP-006 AC-1 says "defer to platform listing." This is the same issue I raised in the DIP-006 skill review. The consistency-reviewer's SPEC-005 report independently re-identified it. No new information — both flag the same stale Step 1.

### E. `/agents` command reference is a dead end (User Advocate)
**Status: Open.** SKILL.md line 17 says "run `/agents` to register them." The User Advocate is correct that `/agents` is not a Praxisity command. It is a Claude Code built-in (the same `/agents` that was run to register agents during this session's DQ-3 resolution). The User Advocate may be over-categorizing this as "Blocking" — it's a UX friction point, not a system failure. The `/agents` command does work; it's just not self-evident to a new user. However, the User Advocate's concern that the reference assumes Claude Code knowledge is valid.

### F. Mode 3 fallback loses delta capability (Critic, Designer, Skeptic — all flag variants)
**Status: Open (acknowledged in design, not addressed in documents).** All three agents independently identify that "fall back to Mode 2" is a capability loss, not graceful degradation. The design's risk table says this; the skill's language implies it's a lateral move. The Critic, Designer, and Skeptic each surface this from different angles. They are all correct and their combined weight makes this more credible than any single report alone.

**Session context:** This was noted in DESIGN-004's risk section before any of these agents read it. The design team was aware. The snapshot agents don't know the issue was already documented internally — they re-discovered it independently, which actually validates the concern rather than making it stale.

---

## Part 4: What Only Delta Awareness Can See

### The Consistency Reviewer Is Now the Least Consistent Agent

Across this session, I flagged the consistency-reviewer as the format outlier multiple times (DIP-005 review Issue 1; rename review comparison section). The consistency-reviewer's SPEC-005 report now explicitly states: "My Output Format section should include Dispatch Mode and Instructions Received fields like the other 7 agents — I am the inconsistency I was hired to find."

What no snapshot agent can see: the consistency-reviewer's self-identified fix still hasn't happened. The SPEC-005 consistency-reviewer report itself does not include a Dispatch Mode field or Instructions Received section — it follows the old format. The agent has correctly diagnosed its own divergence but continues to reproduce it. This is a prompt-level issue: the Output Format template in the agent file still specifies the old format. The agent cannot fix its own output by knowing the problem exists. The template must change.

This matters for the delta review because the issue has now been identified three times (by me twice, by the consistency-reviewer itself once) without being closed. It is a persistent open item.

### The "7x vs. 8x" Duplication Note Is Now a Dead Issue

The fresh-eyes-reviewer-report.md (written under the old agent name) flags Issue 2 as "7x duplication ambiguity" in DESIGN-004 COMP-2. This was noted as minor/advisory at the time. Since then, the implementation shows collab-mode.md is correctly shared as one file across all 8 agents — the arithmetic ambiguity never manifested in implementation. This is genuinely resolved, not by a fix but by the implementation being unambiguous in practice.

### The Bootstrapping Test Has Already Happened — But Not for Modes 1 and 2

The PM report says the bootstrapping test is "NOT STARTED" and lists it as the next critical step. Session context corrects this: the bootstrapping test for Mode 3 is **already running** — I am the evidence. This entire team session (Critic, Skeptic, Designer, User Advocate, Project Manager, Prompt Engineer, and me as consistency-reviewer) is a Mode 3 bootstrapping test. The agents produced structured, differentiated, non-redundant output on a real planning artifact. Mode 3 works.

What has NOT been tested (and the PM is correct that it hasn't): Mode 1 dispatch during a normal command session (e.g., asking the Critic to review a spec mid-flow), and Mode 2 parallel dispatch as a gate before finalizing an artifact. These are the simpler modes and almost certainly work, but they haven't been validated.

### The Spec-to-Design Drift Issues from the Cold Read Remain Unresolved in Spec

The fresh-eyes-reviewer-report.md (cold read, dated 2026-03-28) identified 8 issues in the spec and design. Looking across all session reviews, I can now assess which of those were addressed:

| Issue | Status |
|-------|--------|
| Issue 1: Collab-mode/context-block not named as deliverables in spec | Not fixed. Spec still doesn't enumerate these. |
| Issue 2: "7x duplication" ambiguity | Moot — implementation unambiguous. |
| Issue 3: REQ-F1 "standard fields" vs. DATA-1 optional fields | Not fixed. Spec still reads as all-required. |
| Issue 4: REQ-F3 "what to preserve" narrowed to report-saving in design | Not fixed. Addressed in implementation (reconstitution notes added). |
| Issue 5: REQ-F11 says skill covers Mode 1 but design says Mode 1 is in COMP-4 | Not fixed. SKILL.md explicitly says "Mode 1 not covered here." AC-10 still requires skill to cover all 3 modes. |
| Issue 6: No AC for REQ-F9 (persistent memory) | Not fixed. |
| Issue 7: Template file paths not specified in design | Fixed — implementation order and DATA sections now specify paths. |
| Issue 8: SPEC out-of-scope conflicts with DESIGN broader Write access | Not fixed; designer reviewed this as an accepted tradeoff. |

Issues 1, 3, 5, and 6 from the original cold read remain unresolved in the spec. Issue 5 is the most implementation-impactful: AC-10 will report a false failure because the skill explicitly says "Mode 1 not covered here," yet AC-10 tests for Mode 1 guidance in the skill. Every review that checks this AC will find the same false failure.

---

## Summary: Signal vs. Noise for the Developer

**Genuinely open, highest priority:**
1. "What you ignore" negative framing — affects all 8 agents, clear fix exists (Prompt Engineer)
2. Consistency-reviewer Output Format divergence — self-diagnosed, still present (3 independent identifications)
3. "Instructions Received" missing from all 8 agent Output Formats (Consistency Reviewer SPEC-005 report)
4. AC-10 false failure: SPEC-005 AC-10 tests Mode 1 in skill; skill correctly excludes it (fresh-eyes cold read Issue 5, never resolved)
5. Orphaned agent memory path: `.claude/agent-memory/fresh-eyes-reviewer/` won't load under `consistency-reviewer` agent in future sessions

**Open, lower priority (documentation/advisory):**
6. DIP-006 AC-1 stale text
7. DIP-007 named-agents format stale
8. DIP-006 Step 1 contradicts AC-1
9. Decision gate lacks explicit cost signal (Mode 3 vs. Mode 2 overhead)
10. Collab-mode.md missing session-report.md path (Mode 3 agents writing reports without skill in context)

**Not open — correctly resolved this session:**
- DEC-4/DEC-5 cross-reference error
- REQ-N1 in Must Satisfy tables
- DIP-006 Step 4 guidance-vs-control-flow tension
- Session report self-evaluation bullets generalized
- Consistency-reviewer naming convention in Output Format
- Stale fresh-eyes-reviewer agent files removed from `.claude/agents/`

**Not open — moot or misidentified:**
- "7x duplication" arithmetic ambiguity (Issue 2 from cold read) — implementation unambiguous
- Critic's "Critical" orphaned memory finding — this is my memory directory, not a system flaw; the real issue is the path mismatch (item 5 above), not orphaning

---

## Self-Evaluation

- **What only delta-awareness added:** Correcting the Critic's "Critical" finding about orphaned memory (it's mine, not abandoned). Confirming Mode 3 bootstrapping is already validated by this session's existence. Tracking which of the original cold-read issues were resolved vs. still open. Identifying that the consistency-reviewer has self-diagnosed its format divergence but not resolved it.

- **What I was unable to assess:** Whether the remaining open items will matter in practice. The PM report's recommendation — use the agents first, fix what the experience reveals matters — is the right call. I've catalogued the debt; the developer should decide what to pay down before real use.

- **Most important thing this review adds that no other report has:** The AC-10 false failure (item 4 in the high-priority list above) was in the original cold-read report and has never been acknowledged in any subsequent review. It will surface as a test failure every time someone runs DIP-005 or DIP-006 verification. It should be on the developer's radar.

- **Prompt improvement suggestions:** The Mode 3 persistent reviewer role benefits from an explicit "session timeline" orientation at the start — the agent should be told when it was added to the team and what reviews it has done. I reconstructed this from context, but a structured handoff at session start (or from a reconstitution note) would make this more reliable. My current prompt does not include guidance for this orientation step.
