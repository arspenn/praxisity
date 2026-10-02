## Cross-Document Consistency Review: DIP-006 consult-team Skill

**Documents reviewed:**
- `/home/arspenn/Dev/praxisity/.claude/skills/consult-team/SKILL.md`
- `/home/arspenn/Dev/praxisity/.plans/prompts/006-consult-team-skill.md` (DIP-006)
- `/home/arspenn/Dev/praxisity/.plans/designs/004-agent-consultation-system.md` (INT-1, INT-2, INT-3, COMP-3)
- `/home/arspenn/Dev/praxisity/.claude/agents/README.md` (referenced by skill)

**Status:** Issues Found

---

## Issues

### Issue 1 — AC-1 Mismatch: Skill Defers to Platform Listing; AC Requires Embedded Index

**Location:** DIP-006 AC-1 vs. SKILL.md "Available Agents" section

**What AC-1 requires:**
> "Given the skill is loaded, then it provides an index of all 8 agents with name, description, and category"

**What the skill actually does:**
> "Praxisity agents are registered as native Claude Code subagents in `.claude/agents/`. When loaded, they appear in your available agent types with their descriptions. Use those descriptions to select the right agents for the task."

The skill provides 0 agents by name in the index section. It defers entirely to the platform's native agent listing.

**Root cause:** The design was updated. The INT-2 contract now reads:
> "Agent names and descriptions are visible in the Agent tool's available types when properly registered. See `.claude/agents/README.md` for the full roster."

The skill's implementation is **fully consistent with the updated INT-2 design**. The problem is that AC-1 in DIP-006 was not updated when INT-2 was revised. The DIP still says "verify index covers all 8 agents" — but the new design intent is to defer to native platform listing instead of duplicating it.

**Why it matters for implementation:** No implementation impact — the skill works as designed. But AC-1 as written is a false negative: a correct implementation fails the written test. If DIP-006 is later audited against its ACs, this will create confusion about whether the DIP is complete.

**Fix needed:** Update DIP-006 AC-1 to reflect the new approach:
> "Given the skill is loaded, then it provides guidance for selecting agents via the platform's native agent listing, with a reference to `.claude/agents/README.md` for a human-readable roster overview"

---

## AC-by-AC Assessment

### AC-1 — FAIL (as written; see Issue 1)

Skill does not embed an index table. Defers to native platform listing. AC not updated to match design change.

### AC-2 — PASS

The Decision Gate section presents a clear snapshot vs. delta framework:
- Snapshot (Mode 2): independent agents, current state, good for review gates
- Delta (Mode 3): persistent teammates, see changes over time, good for sustained work
- Explicit key question: "Will the agents need to see how the work changes during this session, or is a snapshot of the current state sufficient?"
- Concrete tie-breaker: "When in doubt, start with Mode 2. You can always escalate to Mode 3 if the work turns out to need sustained collaboration. The reverse is harder."

Both modes' appropriate-use cases are concrete and differentiable.

### AC-3 — PASS

Mode 2 instructions match INT-1 contract exactly:
- `subagent_type`: the agent's name — contract: `Agent(subagent_type: "[agent-name]", ...)`
- `prompt`: the context block — contract: `prompt: [context block]`
- Platform loads agent file as system prompt — stated explicitly
- Context block template reference: `.claude/skills/consult-team/templates/context-block.md` — correct path
- Each agent writes own report to `.plans/reviews/` — matches INT-3
- Lead review instruction present: `.plans/reviews/[ARTIFACT-ID]-lead-review.md` — matches INT-3
- Session report template reference: `.claude/skills/consult-team/templates/session-report.md` — correct path

### AC-4 — PASS

Mode 3 instructions match INT-1 contract:
- TeamCreate with team_name and description — matches contract step 1
- Agent tool with subagent_type, team_name, name parameters — matches contract step 2
- collab-mode.md content included in each teammate's task prompt — matches contract: `prompt: [collab-mode.md content] + [context block]`
- collab-mode reference: `.claude/skills/consult-team/templates/collab-mode.md` — correct path
- Prerequisite noted: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` and Claude Code v2.1.32+
- Fallback to Mode 2 if unavailable — explicitly stated

### AC-5 — PASS

Skill description: "Multi-perspective consultation on the same work. Dispatch specialist agents for parallel review (Mode 2) or persistent collaborative teams (Mode 3). **Different from dispatching-parallel-agents which splits independent tasks — this skill gets multiple viewpoints on the SAME topic.**"

The description explicitly names and differentiates from `dispatching-parallel-agents`. The distinction (same topic vs. independent tasks) is unambiguous.

### AC-6 — PASS

The skill contains no execution sequences or control flow. Assessment by section:

**Decision Gate:** Frames two options with "Good for:" use cases. No "if X then do Y."

**Mode 2:** Describes what to do in guidance form: "Select agents... Dispatch each agent using the Agent tool... Each agent writes its own report... After all agents return, write a lead review..." This reads as advice from a colleague, not a state machine. No mandatory sequencing operators.

**Mode 3:** Uses a sub-heading structure ("Setting up the team", "Working with the team", "Wrapping up") with bullet points describing concepts. The bullets describe knowledge to have, not steps to execute. Example: "Teammates maintain context across the session — they accumulate understanding as the work evolves" is explanation, not instruction. The only imperative bullets describe the API parameters to use, which is appropriate technical guidance.

**Session Management:** All descriptive. "Every dispatched agent writes its own report... The report is the source of truth." Explanatory framing throughout.

The tone consistently aligns with DIP-006 Note: "The skill should feel like advice from an experienced colleague, not a manual to follow step by step." AC-6 passes.

---

## Additional Checks

### Template references — all correct

All three template files are referenced by path:
- `.claude/skills/consult-team/templates/context-block.md` (Mode 2 section, line 46)
- `.claude/skills/consult-team/templates/session-report.md` (Mode 2 line 50, Session Management line 75)
- `.claude/skills/consult-team/templates/collab-mode.md` (Mode 3 section, line 59)

All three files exist (created by DIP-004).

### INT-2 consistency — consistent

The updated INT-2 contract:
> "Agent names and descriptions are visible in the Agent tool's available types when properly registered. See `.claude/agents/README.md` for the full roster."

SKILL.md "Available Agents" section:
> "When loaded, they appear in your available agent types with their descriptions. Use those descriptions to select the right agents for the task. [...] For a human-readable overview of the roster and planned future agents, see `.claude/agents/README.md`."

The skill's approach is consistent with the updated INT-2 design. No mismatch between skill and design. The mismatch is between the DIP AC (not updated) and both the design and implementation.

### README.md reference — file exists, scope gap noted

The skill references `.claude/agents/README.md`. The file exists and contains a correct 8-agent roster table plus planned future agents. However, no DIP explicitly claims creating this file as in-scope. It was created as part of DIP-006 implementation work but appears nowhere in DIP-006's Files in Scope list (which only lists `SKILL.md`). This is not a breaking issue — the file exists, its content is correct, and the skill's reference to it is valid. Worth noting as an undocumented deliverable.

### Decision gate clarity assessment

The gate is clear. The "key question" formulation ("Will the agents need to see how the work changes during this session...") is concrete and answers-its-own-question: if changes matter, Mode 3; if current state is sufficient, Mode 2. The tie-breaker heuristic (start with Mode 2, escalate if needed) provides actionable guidance when the question is ambiguous. The reasoning ("The reverse is harder") explains why the heuristic points that direction.

One minor gap: the skill describes Mode 3 costs as "high (full session per agent)" in abstract but doesn't surface this cost in the decision gate section itself. A main agent reading the gate gets the use-case framing but not the cost signal. This may lead to over-use of Mode 3. The trade-offs table in DESIGN-004 Section 2.2 is more explicit. Advisory only.

---

## Recommendations (advisory, do not block approval)

- **Update DIP-006 AC-1** to match the implemented approach: deferred index via platform native listing + README.md pointer. This is a documentation fix, not an implementation fix. The skill is correct; the AC is stale.

- **README.md scope** — the `README.md` file is referenced by the skill but was not in any DIP's scope. Its creation should be acknowledged in PLANNING.md or DIP-006's completion notes, so future reviewers don't wonder which DIP owned it.

- **Decision gate cost signal** — Consider adding a one-line cost note to the gate section, e.g., "Mode 3 costs significantly more (full session per agent vs. one subagent call)." This would surface the cost/benefit tradeoff without requiring the main agent to find the trade-offs table elsewhere.

---

## Self-Evaluation

- **Most frequent inconsistency type:** Design update not propagated to DIP acceptance criteria. The INT-2 revision was clean in the design and clean in the implementation — but the DIP AC was never updated to match. This is the same pattern as Round 2 of the DIP consistency review (commit message Satisfies lines not updated when Must Satisfy tables changed).

- **Unable to assess:** Whether the native platform listing actually makes agents discoverable in the Agent tool's UI — this requires runtime testing. The assumption that agents "appear in your available agent types when properly registered" is correct per the design's DQ-3 resolution, but that runtime behavior is outside what I can verify from documents alone.

- **Document structure quality:** The DIP's AC section was easy to test against: each AC has a clear criterion and a stated test method. The challenge was identifying that the design had changed (INT-2 updated) while the DIP's AC had not — this required reading both documents and comparing their expectations for the same deliverable.

- **Prompt improvement suggestions:** The review request asked "Does the 'Available Agents' section appropriately defer to the platform's native agent listing rather than duplicating the index?" — this framing already signals the expected answer and implies the design changed. My instructions say to read what is written, not what was discussed. In this case, the framing was accurate and useful. No change needed to the review prompt.