# Cross-Document Consistency Review

**Documents reviewed:**
- `/home/arspenn/Dev/praxisity/.plans/specs/005-agent-consultation-system.md` (SPEC-005)
- `/home/arspenn/Dev/praxisity/.plans/designs/004-agent-consultation-system.md` (DESIGN-004)

**Reviewer:** Fresh Eyes Reviewer (cold read, no conversation context)
**Date:** 2026-03-28
**Prior review on file:** `SPEC-005-fresh-eyes-reviewer-report.md` — this is a second independent pass.

**Status:** Issues Found

---

## Issues

### 1. SPEC-005 AC-6 calls doing-command files "skill files"

**Location:** SPEC-005, Section 5 (Acceptance Criteria), AC-6

**Text:** "Given a doing command (`/build`, `/deliver`, `/breakdown`, `/define`), when its **skill file** is inspected, then it contains no agent consultation pointers."

Doing commands live in `.claude/commands/` and are invoked as commands. They are not skills. DESIGN-004 COMP-4 correctly calls these "Existing command files in `.claude/commands/`." AC-5 for thinking commands uses the correct term "command file." AC-6 alone uses "skill file," which is the wrong term.

**Why it matters for implementation:** The acceptance criterion directs the implementer to look in the wrong artifact type. If an implementer reads AC-6 as a test step — "inspect the skill file for `/build`" — they will look in `.claude/skills/` rather than `.claude/commands/` and either fail to find the file or test the wrong file. Since `/build` does have a skill file (it is a command-as-skill in the Praxisity framework), there is real risk of testing the command skill file rather than verifying the right artifact has no pointer.

---

### 2. DESIGN-004 Tier 1 pointer line count is inconsistent across three locations within the design

**Locations:**
- DESIGN-004, COMP-4 Responsibilities (Section 3): "~4-line pointer (heading + 2 guidance lines)"
- DESIGN-004, Appendix A Glossary: "Tier 1: ~4 lines: heading + guidance, always loaded"
- DESIGN-004, INT-2 Contract (Section 4): shows a 6-line block (heading + 5 lines of content across 4 labeled entries)

The INT-2 contract section shows the actual format the main agent would use:
```
## Agent Consultation                                        ← line 1 (heading)

For a quick single perspective, dispatch: [...]             ← line 2
For multi-agent input (parallel or collaborative), invoke   ← line 3

Mode 1: Main agent dispatches directly via Agent tool       ← line 4
Modes 2 & 3: Main agent invokes consult-team skill via      ← lines 5-6
             Skill tool, then follows loaded guidance
```

That is a heading plus 4-5 lines of content = 5-6 total, not "~4" or "heading + 2 guidance lines."

SPEC-005 AC-5 also says "~4 lines (heading + guidance)" — an implementer checking this against the INT-2 template will see a mismatch.

**Why it matters for implementation:** An implementer following COMP-4 will write a 3-line pointer (heading + 2 lines). An implementer following INT-2 will write a 6-line block. The acceptance criterion (AC-5) tests for "~4 lines." None of these three numbers agree. The implementer has no single authoritative specification for pointer length.

---

### 3. REQ-N4 says reconstitution lives in "planning artifacts (specs, designs, DIPs)" — the design routes it to session reports in `.plans/reviews/`

**Location:** SPEC-005, REQ-N4; DESIGN-004, DATA-4 (Session Report), INT-3

**Spec text:** "Team composition for multi-session work shall be documented in planning artifacts (specs, designs, DIPs) so teams can be reconstituted across terminal sessions"

**Design implementation:** DATA-4's lead review schema includes a "Reconstitution notes (Mode 3 only)" section. INT-3 locates this in `.plans/reviews/[ARTIFACT-ID]-lead-review.md`. Session reports in `.plans/reviews/` are not specs, designs, or DIPs.

DESIGN-004's Requirements Coverage table (Section 1.3) maps REQ-N4 to "COMP-2, DATA-4, INT-3" — all of which resolve to `.plans/reviews/`, not to the planning artifacts the spec names.

**Why it matters for implementation:** An implementer satisfying REQ-N4 by the spec's terms would add team composition notes to the spec, design, or DIP. An implementer following the design would write a lead review to `.plans/reviews/`. These are different files in different locations. The design's choice may be better operationally, but it contradicts the spec's explicit statement about where this information lives. UC-3 (Spec Section 4) describes the reconstitution flow as: "DIP references the team composition and previous session report" — which implies both a DIP and a reviews entry, but REQ-N4 only says "planning artifacts."

---

### 4. SPEC-005 REQ-F9 is COULD priority but AC-10 tests it as a mandatory condition

**Location:** SPEC-005, REQ-F9 and AC-10

**REQ-F9 (Priority: COULD):** "Agent definitions shall use Claude Code's native `memory: project` feature..."

**AC-10:** "Given an agent definition file, when its frontmatter is inspected, then it includes `memory: project` enabling persistent knowledge accumulation..."

The AC-10 criterion is phrased as a mandatory pass/fail check — "then it includes `memory: project`." There is no qualification that this is optional. An implementer testing the 8 agent files against AC-10 would fail any file that omits the `memory` field, even though the requirement itself is COULD priority.

**Why it matters for implementation:** An implementer who skips `memory: project` on some or all agents (a reasonable choice given COULD priority) will fail AC-10. Either the priority level of REQ-F9 should be raised to align with the AC, or AC-10 should be re-phrased as advisory ("should include" rather than "then it includes").

---

### 5. DESIGN-004 COMP-1 states all agents have identical tool restrictions but Section 7.2 introduces exceptions for some agents

**Location:** DESIGN-004, COMP-1 Key Design Decisions; DESIGN-004, Section 7.2 Risk Areas

**COMP-1 text:** "All agents use restricted tool access: `tools: Read, Grep, Glob, Write` — read-only for project files, Write for `.plans/reviews/` reports only"

**Section 7.2 Risk entry:** "Custom agents not available via subagent_type (DQ-3)" — in the same table, a separate row reads: "action-oriented agents (Designer, Project Manager) may need broader tool access" [listed as a risk, not a decision].

COMP-1 makes a definitive design decision (uniform tool set for all 8 agents). Section 7.2 then opens the question for two named agents. These two statements cannot both be authoritative. If COMP-1 is the decision, the 7.2 risk item is misleading because it implies the decision is open. If 7.2 is acknowledging genuine uncertainty, then COMP-1's "all agents" claim is premature.

**Why it matters for implementation:** When implementing Designer and Project Manager agent files, the implementer faces conflicting direction: use the uniform tool set (COMP-1) or consider broader access (7.2). The design does not resolve this, meaning the decision will be deferred to implementation — which is exactly what design documents should prevent.

---

### 6. SPEC-005 UC-1 Step 10 omits the lead review that DESIGN-004 defines as a required output for Mode 2

**Location:** SPEC-005, Section 4 UC-1, Postconditions; DESIGN-004, INT-3, DATA-4

**UC-1 Postconditions:** "Agent self-evaluations are persisted for future prompt refinement." UC-1 Step 10 says "Agent outputs and self-evaluations are saved to `.plans/reviews/`."

**DESIGN-004 INT-3:** For Mode 2 and Mode 3, the main agent writes a separate lead review (`[ARTIFACT-ID]-lead-review.md`) covering synthesis, per-agent assessment, and instruction fidelity verification. This is a required output in the design.

UC-1 describes exactly the Mode 2 scenario (parallel dispatch of Critic, User Advocate, Skeptic). The lead review is not mentioned in any part of UC-1 — not in the flow, not in the postconditions.

**Why it matters for implementation:** UC-1 is the primary use case for Mode 2. If an implementer uses it as a behavioral specification for the `/spec` command's consultation flow, they will not implement the lead review step. The lead review is a core design element — it provides synthesis, instruction fidelity verification, and (for Mode 3) reconstitution notes. Missing it from the most prominent use case underspecifies expected behavior.

---

## Issues Not Confirmed From Prior Review

The prior review (Issue 6) claimed there is no acceptance criterion for REQ-F9. This is incorrect. AC-10 explicitly validates REQ-F9 in the spec (line 168). The prior review miscounted the AC-to-REQ mapping. REQ-F9 does have an AC — Issue 4 above addresses a different problem with that AC (priority mismatch), but the gap the prior review identified does not exist.

The prior review (Issue 5) claimed a conflict between REQ-F11 and COMP-3's exclusion of Mode 1. On careful re-reading, REQ-F11 itself assigns Mode 1 guidance to "Tier 1 command pointers (COMP-4)" — the design is consistent with the spec on this point. AC-11 also explicitly states Mode 1 is in COMP-4. This is not a real inconsistency.

---

## Recommendations (advisory, do not block approval)

1. **AC-5 should clarify "~4 lines" is approximate, not a hard count.** Given the INT-2 format shows more lines, specifying "compact, non-bloating pointer" rather than a line count would be more testable and less likely to conflict with the actual format.

2. **PLANNING.md Session Notes says "7-agent consultation system."** Both design and spec have settled on 8 agents. The PLANNING.md note was not updated when the Fresh Eyes Reviewer was added. This doesn't affect implementation but will cause confusion if PLANNING.md is read during future work.

3. **UC-1 would be strengthened by naming the lead review as a postcondition.** Since UC-1 is the primary Mode 2 example, adding "Main agent writes lead review to `.plans/reviews/[ARTIFACT-ID]-lead-review.md`" to its postconditions would make it consistent with the design.

4. **The DEC-2 "avoids 7x duplication" phrasing** (flagged in the prior review) still reads ambiguously with 8 agents. A note clarifying "7 extra copies beyond the first" would remove the ambiguity without changing anything else.

---

## Self-Evaluation

**Most frequent inconsistency types:** Internal design contradictions (a design component making a decision that another section of the same design reopens) and spec-to-design semantic drift (spec says "planning artifacts," design implements in "reviews"). Also: unit count disagreements between a component description and the interface contract.

**Unable to assess:**
- Whether the INT-2 format block is intentionally more detailed than the COMP-4 description (the extra lines may be intentional elaboration, not a count error).
- Whether the `.plans/reviews/` location for reconstitution notes is a deliberate improvement over the spec's "planning artifacts" — it may be. The design may have concluded session reports are a better home. If so, the spec's REQ-N4 should be updated to reflect the design decision.
- Technical accuracy of Claude Code platform claims (tool restrictions, TeamCreate behavior, experimental flag requirements).

**Document structure quality:** Cross-referencing was generally straightforward. The design's Requirements Coverage table (Section 1.3) is the right tool for ensuring traceability and the explicit "Validates" column in the spec's AC table works well. The main difficulty was that the INT-2 contract section and the COMP-4 description are far apart in the document and describe the same artifact with different specificity — easy to read each in isolation without catching the discrepancy.

**Prompt improvement suggestions:**
- Asking the reviewer to explicitly check every AC against the component it tests (not just against the requirement ID) would surface implementation-path gaps like Issue 6 above (UC-1 missing lead review step) faster.
- A "what does a cold implementer do on Day 1?" framing would help prioritize which inconsistencies are blocking vs. resolvable by reading context.