## SPEC-005 Prioritized Action Plan

**Author:** Project Manager agent
**Date:** 2026-03-29
**Based on:** All SPEC-005 review reports (prompt-engineer, consistency-reviewer x5, fresh-eyes-reviewer x2, implementation reviews x2, rename review, team dispatch test, prompt comparison)

---

## Prioritization Framework

Three categories based on one question: **does this need to happen before the agents are used on real work?**

- **Fix Now:** Blocks or degrades real use. Small effort, high payoff. Do before the bootstrapping test.
- **Fix After First Use:** Real issue, but the bootstrapping test will either confirm the problem or reveal it doesn't matter in practice. Schedule after first real dispatch.
- **Reject / Defer Indefinitely:** Theoretical concern, cosmetic, or would cost more to fix than the problem costs to live with. Don't schedule. Revisit only if real use surfaces it as a pain point.

---

## Fix Now

These are changes to make before the bootstrapping test. Total estimated effort: one focused session.

### 1. Reframe "What you ignore" from negations to positive scope boundaries

**Source:** Prompt Engineer report (Elephants finding)
**Affects:** All 8 agent files
**Effort:** Small — rewrite one list per file, ~15 minutes total

The highest-value prompt fix identified by any reviewer. "What you ignore: Quality of implementation -- that's the Critic's job" activates the concept it's trying to suppress. Reframe as "Your scope is limited to: [positive list]." Move cross-agent references to the README roster if they're wanted for human readers.

This affects every agent dispatch. Fix it before agents run on real work so the first real use gets the benefit.

### 2. Remove "(student)" from project-manager.md Project Context

**Source:** Prompt Engineer report (Elephants finding)
**Affects:** project-manager.md only
**Effort:** Trivial — delete one word

The PM agent is reviewing Praxisity's own planning work. The developer is the framework author, not a student user. The "(student)" label biases toward overcautious advice. "Solo developer" captures the real constraint (one person's time).

### 3. Add one-line mode definitions to each agent's output template

**Source:** Prompt Engineer report (Ambiguity finding)
**Affects:** All 8 agent files
**Effort:** Small — add 3 lines to each file

Mode 1 agents get only their own file as context. They have no definition of "Mode 1/2/3" but are asked to self-report it. Add:
```
Mode 1: Single expert consult (one-shot subagent)
Mode 2: Parallel perspectives (multiple one-shot subagents)
Mode 3: Collaborative team (persistent teammates)
```
~20 tokens per file. Eliminates guessing.

### 4. Add severity level definitions to critic.md

**Source:** Prompt Engineer report (Clarity finding)
**Affects:** critic.md only
**Effort:** Trivial — add 3 lines

The Critic is told to calibrate severity but given no scale. Add:
- Critical: Would cause implementation failure or incorrect behavior
- Important: Would degrade quality or create confusion but work proceeds
- Minor: Cosmetic or low-impact; fix if convenient

The Critic is one of the most frequently dispatched agents. Consistent severity calibration matters from the first use.

### 5. Add audience determination procedure to stakeholder.md

**Source:** Prompt Engineer report (Clarity finding)
**Affects:** stakeholder.md only
**Effort:** Small — add one paragraph

Without this, different sessions will infer different audiences for the same artifact. Add the decision procedure: if named in artifact, use that; if not, check the producing command; if still ambiguous, use defaults (specs/designs for implementers, deliverables for external readers, commands for framework developer).

### 6. Fix SPEC-005 AC-6 terminology: "skill file" should be "command file"

**Source:** Fresh-eyes round 2 (Issue 1)
**Affects:** SPEC-005 only
**Effort:** Trivial — change two words

AC-6 says "skill file" when it means "command file." This directs a tester to look in the wrong directory. One-word fix, eliminates a false test path.

---

## Fix After First Use

These are real issues where the bootstrapping test will provide evidence to calibrate the fix. Do them after the first Mode 2 dispatch on real work.

### 7. Deduplicate Project Context boilerplate across agent files

**Source:** Prompt Engineer report (Noise finding)
**Affects:** 7 of 8 agent files
**Effort:** Medium — requires deciding on a shared context mechanism

~300 redundant tokens across an 8-agent dispatch. Near-identical paragraphs with copy-paste drift. The fix (extract shared context or canonicalize) is clear, but the right mechanism depends on how agents are actually dispatched. The context block template (DIP-004) was designed for per-dispatch customization, not shared boilerplate. After the first real dispatch, evaluate whether the redundancy actually causes attention problems or is just aesthetically annoying. If agents produce good output despite the boilerplate, deprioritize further.

### 8. Make agent memory instructions actionable or remove them

**Source:** Prompt Engineer report (Ambiguity finding)
**Affects:** All 8 agent files (final line of each)
**Effort:** Small once the decision is made

"Update your agent memory with [patterns]" is underspecified — no path, no format, no trigger. Two options: (a) specify explicitly ("write to `.claude/agent-memory/<your-name>/patterns.md`"), or (b) remove and let the platform's `memory: project` feature handle it natively. The bootstrapping test will reveal whether agents actually attempt memory writes and whether the output is useful. If they don't write anything, remove the instruction. If they write something useful, formalize the path and format.

### 9. Structure self-evaluation prompts more tightly

**Source:** Prompt Engineer report (Drift finding)
**Affects:** All 8 agent files and session-report template
**Effort:** Medium — requires designing the structured prompts

Open-ended self-evaluation varies wildly across sessions. The prompt engineer suggested specific questions (calibration checks, attention audits, confidence ratings). But the prompt engineer also acknowledged no empirical evidence that the current format is bad — the concern is theoretical. After the bootstrapping test, compare self-evaluations across agents and sessions. If they're producing actionable data, leave them. If they're producing platitudes, apply the structured format.

### 10. Test Mode 3 explicitly

**Source:** PM report (Risk finding)
**Affects:** Validation of collab-mode.md, reconstitution notes, team lifecycle guidance
**Effort:** One dedicated test session

Mode 3 is designed but unverified. The experimental flag may not be available. The bootstrapping test plan (PLANNING.md next step 1) should explicitly include a Mode 3 test: create team, spawn 2-3 teammates, do real work, verify reports, verify reconstitution. If Mode 3 doesn't work or isn't practical, the system still functions via Modes 1 and 2 — but the design invested significant complexity in Mode 3 and that investment should be validated.

### 11. Update DIP-006 AC-1 to match implemented approach

**Source:** DIP-006 skill review (Issue 1)
**Affects:** DIP-006 only
**Effort:** Trivial — rewrite one AC line

AC-1 says "embedded index of all 8 agents" but the implementation correctly defers to the platform's native agent listing per the updated INT-2 design. The AC is stale. Fix: "provides guidance for selecting agents via the platform's native agent listing, with a reference to `.claude/agents/README.md`." Group with any other spec/DIP documentation cleanup after the first use cycle.

---

## Reject / Defer Indefinitely

These are findings I'm declining to schedule. Each has a reason.

### R1. Consistency-reviewer's unique output format

**Source:** Prompt Engineer report (Noise finding)
**Decision:** Reject

The consistency-reviewer's different output format is justified by its different function (binary consistency checks vs. graded findings). The prompt engineer acknowledged this is a "mild concern." The synthesis step can handle one structurally different output. Not worth homogenizing.

### R2. Spec-to-design semantic drift on reconstitution location (REQ-N4)

**Source:** Fresh-eyes round 2 (Issue 3)
**Decision:** Defer indefinitely

REQ-N4 says "planning artifacts" but the design routes reconstitution notes to `.plans/reviews/`. The design's choice is operationally better — session reports belong with session reports. The spec language is imprecise but the implementation is correct. If this ever causes real confusion, fix the spec wording then. Fixing it now is documentation churn with no behavioral impact.

### R3. Tier 1 pointer line count inconsistency

**Source:** Fresh-eyes round 2 (Issue 2)
**Decision:** Reject

Three locations describe the pointer length differently (~4 lines, heading + 2, 6-line block). The pointers are implemented and work. The line count was always approximate ("~4"). Nobody will count lines in practice. Not worth fixing.

### R4. REQ-F9 COULD priority vs. AC-10 mandatory phrasing

**Source:** Fresh-eyes round 2 (Issue 4)
**Decision:** Reject

All 8 agents already include `memory: project`. The implementation exceeded the COULD requirement. The mismatch between priority and AC phrasing is academic — there's nothing to fail because the feature is already implemented everywhere.

### R5. DESIGN-004 COMP-1 vs. Section 7.2 on tool access for Designer/PM

**Source:** Fresh-eyes round 2 (Issue 5)
**Decision:** Defer indefinitely

COMP-1 decided uniform tool access. Section 7.2 noted Designer/PM might need more. In practice, both agents are implemented with `tools: Read, Grep, Glob, Write` and it works. If a real use case surfaces where Designer or PM needs Bash or Edit access, revisit then. Don't expand blast radius preemptively.

### R6. SPEC-005 deliverable enumeration gap (collab-mode.md, context-block.md not named in spec)

**Source:** Fresh-eyes round 1 (Issue 1)
**Decision:** Reject

The spec doesn't name every file — the design does. This is normal spec-to-design refinement. The files exist and work. Retroactively adding filenames to the spec adds no value.

### R7. "7x duplication" arithmetic ambiguity in DESIGN-004 COMP-2

**Source:** Fresh-eyes round 1 (Issue 2)
**Decision:** Reject

Cosmetic. "7x" vs "8x" vs "7 extra copies." Everyone understands the meaning. Not worth a commit.

### R8. SPEC-005 UC-1 missing lead review postcondition

**Source:** Fresh-eyes round 2 (Issue 6)
**Decision:** Defer indefinitely

UC-1 doesn't mention the lead review. The skill does. The skill is what the main agent reads at dispatch time. If agents are consistently not producing lead reviews because of this gap, fix the skill guidance (which is the runtime artifact), not the spec (which is the historical artifact).

### R9. REQ-F1 spec vs. DESIGN-004 DATA-1 on required fields

**Source:** Fresh-eyes round 1 (Issue 3)
**Decision:** Reject

Spec lists 5 fields together. Design marks 3 as optional. Implementation includes all 5 in every file. No gap exists. The documents disagree on optionality but the implementation resolved it by including everything. Academic.

### R10. DIP-006 README.md undocumented deliverable

**Source:** DIP-006 skill review (Observation)
**Decision:** Reject

The README exists, is correct, and is referenced by the skill. Not every file needs to be traced to a DIP. Documenting it retroactively in PLANNING.md is busywork.

### R11. Decision gate cost signal

**Source:** DIP-006 skill review (Advisory)
**Decision:** Defer — revisit after Mode 3 test

Adding "Mode 3 costs significantly more" to the decision gate is sensible but low urgency. The decision gate already frames Mode 3 as the heavier option. If the bootstrapping test shows the main agent overusing Mode 3, add the cost signal then.

---

## Execution Order

**Before bootstrapping test (one session):**
1. Items 1-6 above (Fix Now) — all are small edits to existing files
2. Commit as a single prompt-quality improvement batch

**During bootstrapping test:**
3. Item 10 (Mode 3 test) — if experimental flag is available
4. Observe agent behavior for items 7-9 (boilerplate impact, memory writes, self-eval quality)

**After bootstrapping test, before framework rework spec work:**
5. Items 7-9 based on observed evidence — skip any that aren't confirmed problems
6. Item 11 (AC-1 fix) — batch with any other documentation cleanup

**Not scheduled:**
7. Items R1-R11 — revisit only if real use surfaces them as pain points

---

## Self-Evaluation

- **What worked well:** Having the full set of reports from different perspectives made it possible to cross-reference findings and identify which issues were flagged by multiple reviewers (validating importance) vs. only one (suggesting lower urgency). The prompt engineer and fresh-eyes reviewer had almost zero overlap in their findings, confirming the agents are genuinely differentiated.

- **What you struggled with:** Drawing the line between "Fix After First Use" and "Reject." Several items (boilerplate dedup, self-eval structure, memory instructions) have clear theoretical justification but unknown practical impact. I defaulted to "wait for evidence" — but if the bootstrapping test isn't specifically designed to evaluate these concerns, the evidence may never surface naturally. The risk is that deferred items become permanently deferred. Mitigation: explicitly note what to watch for during the bootstrapping test for each deferred item.

- **Prompt improvement suggestions:** My agent prompt asks me to assess feasibility and sequencing but gives no framework for triage decisions specifically. A decision matrix (effort vs. impact vs. evidence-available) would make prioritization more systematic and less judgment-dependent. The current approach works but relies on calibration I'm building in real time rather than calibration built into my instructions.
