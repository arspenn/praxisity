## Project Manager Review

**Artifact:** SPEC-005 Agent Consultation System — full implementation (spec, design, 4 DIPs, all deliverables)
**Date:** 2026-03-29
**Dispatch Mode:** Mode 3

---

## Feasibility Assessment

### [Impact: Advisory] — Single-session delivery of spec + design + 4 DIPs is ambitious but the output exists and mostly works

**What was planned:** Brainstorm, specify, design, break down into 4 DIPs, and implement all 4 — in one session.

**What happened:** It got done. 8 agent files, 3 templates, 1 skill, 3 command pointer edits, directory structure, README. The git history shows 20 commits covering the full arc from initial agent test through implementation and multiple review-fix cycles.

**Concern:** Single-session delivery compresses the feedback loop. Normally the design-first workflow (Specify -> Design -> Breakdown -> Implement) spaces out decision points so each phase benefits from distance. Here, the spec author, designer, DIP author, and implementer were all the same agent in the same context window. This means:
- Ambiguities in the spec were resolved by the designer who wrote the spec, not by a cold reader
- DIP instructions were shaped by the designer's intent, not just by what the design document says
- The implementation reflects conversation context that is not captured in the documents

The review cycle partially compensated for this — the consistency reviewer, prompt engineer, and fresh-eyes reviewer caught real issues across multiple rounds. But the reviews happened post-implementation, not between phases.

**Suggested adjustment:** None for existing work — what's built is built and the reviews have validated it. For future single-session deliveries, consider running at least one agent review between spec and design (before the spec author's context shapes the design).

---

### [Impact: Advisory] — Known issues from reviews remain unresolved

**What's planned:** The review reports collectively identify issues that were flagged but not fixed.

**Concern:** Across the 12 review reports in `.plans/reviews/`, I count the following categories of open items:

**Fixed (confirmed in round 2 reviews or git history):**
- DEC-4/DEC-5 cross-reference error in DESIGN-004 Section 1.3
- REQ-N1 missing from DIP-004 and DIP-006 Must Satisfy tables
- DIP-006 Step 4 guidance-vs-control-flow tension
- Session report self-evaluation bullets (fresh-eyes-reviewer-specific -> generic)
- Consistency-reviewer naming convention mismatch
- Stale fresh-eyes-reviewer files removed from `.claude/agents/`
- REQ-N1 added to commit message templates

**Not fixed (flagged, acknowledged, not addressed):**
1. Prompt Engineer report: "What you ignore" sections use negative framing across all 8 agents (elephants problem)
2. Prompt Engineer report: Project Context sections are near-identical boilerplate across 7 agents (~300 tokens redundant in 8-agent dispatch)
3. Prompt Engineer report: "Dispatch Mode" field in output templates undefined within agent files
4. Prompt Engineer report: Self-evaluation sections are open-ended without calibration criteria
5. Prompt Engineer report: Agent memory update instructions are underspecified
6. Prompt Engineer report: Critic's severity levels undefined
7. Prompt Engineer report: Stakeholder lacks audience determination guidance
8. Prompt Engineer report: Project-manager "(student)" label may bias advice
9. DIP-006 skill review: AC-1 stale (DIP says embedded index, implementation defers to platform)
10. DIP-006 skill review: README.md is an undocumented deliverable
11. DIP-006 skill review: Decision gate lacks cost signal
12. Fresh-eyes round 2: AC-6 says "skill file" instead of "command file"
13. Fresh-eyes round 2: Tier 1 pointer line count inconsistent across 3 locations
14. Fresh-eyes round 2: REQ-N4 says "planning artifacts" but design routes to `.plans/reviews/`
15. Fresh-eyes round 2: REQ-F9 is COULD priority but AC-10 tests it as mandatory

**Suggested adjustment:** These do not block use. Most are documentation fixes or prompt refinements. But they should be tracked. The prompt engineering items (1-8) are the highest-value improvements for agent output quality. I recommend batching them as a follow-up ticket after the bootstrapping test validates which agents actually need tuning.

---

### [Impact: Risk] — Mode 3 (collaborative teams) is untested and depends on an experimental feature

**What's planned:** The system supports three dispatch modes. Mode 3 uses `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` and `TeamCreate`.

**Concern:** Mode 3 is the most complex mode and the one with the highest value proposition (delta-aware, cross-perspective regression catching). It also:
- Depends on an experimental flag that could change or be removed
- Has not been tested in this session (the team dispatch test used Mode 2, not Mode 3)
- Has the highest token cost ("full session per agent")
- Is the mode where the skill's guidance matters most (team lifecycle, reconstitution)

The skill includes a fallback ("If unavailable, fall back to Mode 2"), which is the right defensive choice. But Mode 3 is currently a designed-but-unverified capability.

**Suggested adjustment:** The bootstrapping test (PLANNING.md next step 1) should explicitly include a Mode 3 test — not just "register agents and test consultation flow" but specifically: create a team, spawn 2-3 teammates, have them do real review work, verify report writing, verify reconstitution notes. If Mode 3 fails or is impractical, the system still works via Modes 1 and 2 — but the design invested significant complexity in Mode 3 (collab-mode.md, reconstitution notes, team lifecycle guidance), and that complexity should be validated before building more on top of it.

---

### [Impact: Advisory] — The system was designed for the framework rework use case but hasn't been used on it yet

**What's planned:** PLANNING.md next step 2 is "Use agents on real framework rework spec work." The entire agent roster was designed around the perspectives needed for spec and design review.

**Concern:** The agents have been used to review their own implementation (meta-review), which is useful for catching prompt issues but is not the intended use case. The real test is: does dispatching a Critic, Skeptic, and User Advocate on a framework rework spec produce feedback that changes the spec for the better?

Until that happens, the system's value is theoretical. The review reports demonstrate that the agents produce structured, differentiated output. They do not demonstrate that the output improves planning artifacts in practice.

**Suggested adjustment:** This is already planned. Just prioritize it over further refinement of the agent system itself. The temptation will be to fix every issue from the reviews before using the agents — resist that. Use them first, fix what matters after.

---

## Dependency Map

```
SPEC-005 (approved)
  └── DESIGN-004 (approved)
       ├── DIP-004: Templates & extensions ── implemented, committed
       ├── DIP-005: 8 agent files ── implemented, committed
       ├── DIP-006: consult-team skill ── implemented, committed
       └── DIP-007: Tier 1 command pointers ── implemented, committed

Downstream dependencies:
  ├── Bootstrapping test (next step 1) ── NOT STARTED
  │     └── blocks: confidence that Modes 1/2/3 work in practice
  ├── Framework rework spec (next step 2) ── NOT STARTED
  │     └── blocks: validation that agents improve real planning work
  └── SPEC-004 resume (next step 3) ── NOT STARTED
        └── depends on: agent system available for consultation during command fixes
```

**Critical path:** Bootstrapping test -> Framework rework spec work -> (in parallel) SPEC-004 resume + agent refinement from self-evaluation data.

**No circular dependencies.** Each step feeds forward. The agent system is usable now even without fixing the open review items.

---

## What's Well-Planned

**The progressive loading architecture is sound.** Tier 1 (command pointers) adds ~4 lines to thinking commands. Tier 2 (skill) loads only on demand. Tier 3 (agent files) loads only for dispatched agents. A `/build` session that doesn't need consultation pays zero context cost. This is the right design for a framework where context budget matters.

**The decision gate between Mode 2 and Mode 3 is well-articulated.** "Will the agents need to see how the work changes during this session?" is a concrete, answerable question. The tie-breaker heuristic ("start with Mode 2, escalate if needed") is practical. The skill avoids the failure mode of always defaulting to the cheapest option by explicitly framing when Mode 3 is worth the cost.

**The review cycle was thorough.** 12 review reports across 5 agents (consistency-reviewer, prompt-engineer, fresh-eyes-reviewer x2, plus implementation verification passes). Issues were found, tracked, and most were fixed within the same session. The round-2 verification pattern (fix, then re-review) is exactly the right process. The fact that round 2 found a secondary propagation issue (commit message templates not updated) validates the iterative approach.

**Agent differentiation is real.** The prompt engineer found prompt-quality issues (elephants, boilerplate). The consistency reviewer found cross-reference errors and naming mismatches. The fresh-eyes reviewer found spec-to-design semantic drift. These are genuinely different perspectives producing non-overlapping findings. The roster is not redundant.

**The "if the work is solid, say so" rule in every agent's Critical Rules is important.** It prevents the common failure mode where evaluative agents manufacture criticism to justify their existence. Multiple reviews confirmed this rule works — agents that found no issues said so clearly.

**Document-based persistence is the right choice.** All continuity lives in `.plans/reviews/` files, not in terminal state. Sessions can end unexpectedly and the work survives. Reconstitution notes (for Mode 3) enable team continuity across sessions without custom infrastructure.

---

## Verdict: Feasibility and Readiness

**Is the result stable enough to use?** Yes, for Modes 1 and 2. The agent files exist, the skill works, the templates are in place, the command pointers are added. A developer can run `/spec`, see the consultation pointer, dispatch a Critic or Skeptic, and get a structured review report. This works today.

**What's the realistic next step?** The bootstrapping test, exactly as planned. Register agents, dispatch a Mode 2 team on real work, verify the end-to-end flow. Add a Mode 3 test if the experimental flag is available. Do not block on fixing the 15 open review items first — use the agents, then fix what the experience reveals matters.

**Is there technical debt to address before real use?** The debt is documentation-level, not structural. The open review items are prompt refinements (elephants, boilerplate, underspecified memory instructions) and spec-to-implementation drift (stale ACs, line count inconsistencies, terminology errors). None of these prevent the system from functioning. The highest-priority fix is the "What you ignore" negative framing (prompt engineer item 1) because it affects all 8 agents and has a well-documented negative effect on AI behavior — but even this is a quality improvement, not a blocker.

**Risk of proceeding vs. cost of more iteration:** Proceed. The risk of using the agents now is that prompt quality issues (elephants, underspecified instructions) may produce slightly lower-quality output than optimally-tuned prompts would. The cost of more iteration before use is that the agent system sits idle while being polished for a use case it hasn't encountered yet. The reviews have already demonstrated that the agents produce useful, differentiated output even with current prompts. Real use will generate the self-evaluation data needed to make targeted improvements. More desk-review of prompts without dispatch experience is diminishing returns.

---

## Self-Evaluation

- **What worked well:** Reading all 12 review reports gave a comprehensive picture of what was found and what was fixed. The git history provided clear sequencing evidence. Focusing on "what blocks what" rather than "what could be better" kept the assessment grounded in feasibility rather than drifting into the Critic's or Prompt Engineer's territory.

- **What you struggled with:** Assessing whether the single-session delivery model is a genuine risk or just an unfamiliar workflow. Traditional project management would flag "spec, design, and implementation in one session" as a red flag. But in this context — a solo developer with a capable AI agent — the compressed timeline may be appropriate. The review cycle compensated for the compressed phases. I flagged it as advisory rather than blocking, but I'm not confident in my calibration here.

- **Prompt improvement suggestions:** My agent prompt says to ask "How long would this realistically take for one person?" but provides no calibration for what counts as realistic for AI-assisted solo development. Traditional time estimates do not apply. A framing like "how many distinct decision points require human judgment?" would be more useful than wall-clock time estimates for this context. The "(student)" label in my Project Context section was flagged by the prompt engineer review — I agree it should be removed, as it may have biased my assessment toward overcaution.
