---
name: consult-team
description: Multi-perspective consultation on the same work. Dispatch specialist agents for parallel review (Mode 2) or persistent collaborative teams (Mode 3). Different from dispatching-parallel-agents which splits independent tasks — this skill gets multiple viewpoints on the SAME topic.
---

# Agent Consultation

This skill provides guidance for dispatching multiple specialist agents to review, critique, or contribute perspectives on your current work. Use it when a single perspective isn't enough.

**Mode 1 (single expert consult) is not covered here** — for a quick single-agent opinion, dispatch directly from the Tier 1 pointer in your command. This skill covers Modes 2 and 3.

## Available Agents

Praxisity agents are registered as native Claude Code subagents in `.claude/agents/`. When loaded, they appear in your available agent types with their descriptions. Use those descriptions to select the right agents for the task.

If agents don't appear in your available types, run `/agents` to register them.

For a human-readable overview of the roster and planned future agents, see `.claude/agents/README.md`.

## The Decision Gate: Snapshot vs. Delta

Before dispatching, decide which mode fits your situation.

**Snapshot (Mode 2 — parallel subagents):** Each agent gets the current state of the work, evaluates independently, returns results, and shuts down. They don't see each other's work. They don't see changes you make after dispatch. Good for:
- Review gates before finalizing a spec, design, or DIP
- Getting multiple perspectives on a draft
- Quick multi-agent sanity check

**Delta (Mode 3 — collaborative team):** Agents persist as teammates for the full work session. They see changes as they happen. They can message each other and the user directly. When a fix from one perspective breaks something from another, a persistent teammate catches it because they saw the change. Good for:
- Sustained work sessions spanning multiple edits or DIPs
- Work where perspectives interact — a design decision that satisfies the Critic might alarm the Skeptic
- Framework rework or other large-scope changes where context accumulates

**The question to ask:** Will the agents need to see how the work changes during this session, or is a snapshot of the current state sufficient?

When in doubt, start with Mode 2. You can always escalate to Mode 3 if the work turns out to need sustained collaboration. The reverse is harder.

## Mode 2: Parallel Perspectives

Select agents from the index based on what the work needs. Not every review needs all 8 — pick the perspectives that matter for this topic.

**Dispatch each agent using the Agent tool:**
- `subagent_type`: the agent's name (e.g., `"critic"`)
- `prompt`: the context block describing the task

The platform loads the agent's file as the system prompt. Your context block becomes the task. Use the context block template at `.claude/skills/consult-team/templates/context-block.md` for structure — fill in the phase, topic, focus, and materials.

Each agent writes its own report to `.plans/reviews/` — this is the source of truth for what they found. They also return results directly for quick synthesis.

After all agents return, write a lead review to `.plans/reviews/[ARTIFACT-ID]-lead-review.md` synthesizing findings: areas of agreement, disagreement, and unresolved tensions. Use the session report template at `.claude/skills/consult-team/templates/session-report.md` for format.

## Mode 3: Collaborative Team

Mode 3 uses Claude Code's experimental agent teams feature. This requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` to be enabled and Claude Code v2.1.32+. If unavailable, fall back to Mode 2.

**Setting up the team:**
- Create a team with `TeamCreate` — give it a descriptive name and purpose
- Spawn each teammate with the `Agent` tool, including `team_name` and `name` parameters
- For each teammate's `prompt`, include the collab-mode content from `.claude/skills/consult-team/templates/collab-mode.md` followed by the context block
- The platform loads the agent file as the system prompt; the collab-mode + context block become the task

**Working with the team:**
- Teammates maintain context across the session — they accumulate understanding as the work evolves
- Teammates can message each other directly and share a task list
- The user can interact with any teammate directly via Shift+Down
- Let teammates finish their work and write their own reports before shutting them down

**Team lifecycle:**
- The user decides when the team shuts down, not the lead agent. Never shut down teammates without the user's explicit request.
- Initial reports are the beginning of Mode 3 work, not the end. After reports are in, present findings and ask the user what's next. The team should persist through the full iteration cycle — review, implement, re-review — so teammates can see changes and react.
- When the user requests shutdown: each teammate writes their final report to `.plans/reviews/`, the lead writes a review synthesizing all findings with reconstitution notes, then teammates are shut down gracefully.

## Session Management and Output Preservation

**Reports:** Every dispatched agent writes its own report to `.plans/reviews/` using the naming convention `[ARTIFACT-ID]-[agent-name]-report.md`. The lead review uses `[ARTIFACT-ID]-lead-review.md`. The session report template at `.claude/skills/consult-team/templates/session-report.md` defines the format.

**The report is the source of truth.** The direct return from an agent is for quick synthesis. The written report persists beyond context compression and enables verification — you can compare what you sent (the context block) against what the agent says it received (in its "Instructions received" section).

**Cross-session continuity (Mode 3):** When ending a Mode 3 session, the lead review should include reconstitution notes — team composition, what each teammate was working on, open concerns, and a context summary. Planning artifacts (specs, designs, DIPs) should reference these notes so the next session can reconstitute the same team with accumulated knowledge.

**Proportional engagement:** Read agent reports proportionally to the stakes. A quick Mode 2 sanity check may only need a glance at the synthesis. A Mode 3 framework rework warrants reading every teammate's full report.
