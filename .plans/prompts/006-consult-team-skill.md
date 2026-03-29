# DIP-006: consult-team Skill

> **For AI Agent:** This is a Detailed Implementation Prompt. Follow these instructions precisely.
> Read all referenced documents before beginning implementation.
>
> **TodoWrite Integration:** Use Claude's TodoWrite tool to track progress through this DIP.
> Create todos from the Implementation Steps below and mark them complete as you progress.

## Context

| Field | Value |
|-------|-------|
| DIP ID | DIP-006 |
| Task | Create the consult-team skill — the on-demand guidance document for multi-agent dispatch |
| Spec | [SPEC-005](../specs/005-agent-consultation-system.md) |
| Design | [DESIGN-004](../designs/004-agent-consultation-system.md) |
| Todoist Task | N/A |
| Created | 2026-03-29 |

## Objective

Create the `consult-team` skill file that provides the main agent with on-demand guidance for multi-agent dispatch — the agent index, the snapshot vs. delta decision gate, dispatch instructions for Modes 2 and 3, session management, and output preservation. This skill is the Tier 2 load in the progressive loading architecture.

## Required Reading

Before implementation, read and understand these sections:

### From Specification (SPEC-005)
- [ ] Section 3.1: REQ-F3 - What the skill shall provide (index, dispatch guidance, synthesis, preservation)
- [ ] Section 3.1: REQ-F10 - Naming differentiation from Superpowers' dispatching-parallel-agents
- [ ] Section 3.1: REQ-F11 - Three dispatch modes with decision gate between Mode 2 and Mode 3
- [ ] Section 3.2: REQ-N2 - Skills are guidance, not control flow
- [ ] Section 3.2: REQ-N3 - Consultation always optional

### From Design (DESIGN-004)
- [ ] Section 2.2: Architecture Pattern - Three-mode dispatch, snapshot vs. delta, trade-offs table
- [ ] Section 2.3: Technology Choices - Agent tool, TeamCreate, SendMessage
- [ ] Section 3: COMP-3 - consult-team Skill (purpose, responsibilities, dependencies, key design decisions)
- [ ] Section 4: INT-1 - Agent Dispatch Interface (dispatch contract for all three modes)
- [ ] Section 4: INT-2 - Command Pointer Interface (how commands reference this skill)
- [ ] Section 4: INT-3 - Session Report Interface (reporting contract)
- [ ] Section 6: DEC-1 - Three-Mode Dispatch with Decision Gate
- [ ] Section 6: DEC-5 - Skills as Guidance, Not Control Flow

### Reference Files (must exist before this DIP)
- [ ] `.claude/agents/*.md` - All 8 agent files (DIP-005 output — needed for index)
- [ ] `.claude/skills/consult-team/templates/context-block.md` (DIP-004 output)
- [ ] `.claude/skills/consult-team/templates/session-report.md` (DIP-004 output)
- [ ] `.claude/skills/consult-team/templates/collab-mode.md` (DIP-004 output)

### Platform Documentation
- [ ] [Claude Code Sub-agents](https://code.claude.com/docs/en/sub-agents) - Agent tool dispatch, subagent_type, native format
- [ ] [Claude Code Agent Teams](https://code.claude.com/docs/en/agent-teams) - TeamCreate, team workflow, limitations

## Implementation Instructions

### Step 1: Build the Agent Index

Read the frontmatter of all 8 agent files in `.claude/agents/`. Extract name, description, and category for each. Organize by category.

**Input:** 8 agent files
**Output:** Index table for the skill, grouped by category:
- Evaluative: Critic, Skeptic
- Perspective: User Advocate, Stakeholder
- Structural: Designer, Project Manager
- Meta: Prompt Engineer, Consistency Reviewer

The index should contain just enough for the main agent to select agents without loading full files — name, one-line description, category.

**Verify:** Index covers all 8 agents, descriptions match frontmatter, categories are correct

### Step 2: Write the Decision Gate

This is the core value of the skill. The main agent must explicitly consider whether it needs snapshot or delta dispatch before choosing a mode.

**Input:** DEC-1 rationale, Section 2.2 trade-offs table
**Output:** Decision gate section in the skill

The decision gate should present:
- **Snapshot (Mode 2):** Multiple viewpoints on a point-in-time state. Agents evaluate independently, return results, shut down. Good for review gates, sanity checks, multi-perspective feedback on a draft.
- **Delta (Mode 3):** Persistent teammates who see changes over time. They detect when a fix from one perspective breaks something from another. Good for sustained work, multi-DIP implementation, framework rework.
- **Key question:** "Will the agents need to see how the work changes over the session, or is a snapshot of the current state sufficient?"

Do NOT write this as a flowchart or control flow. Write it as a decision framework the main agent considers.

**Verify:** An agent reading the gate would understand when Mode 2 is sufficient and when Mode 3 is worth the cost

### Step 3: Write Mode 2 Dispatch Guidance

How the main agent dispatches parallel subagents.

**Input:** INT-1 Mode 2 contract, INT-3 reporting contract
**Output:** Mode 2 section in the skill

Cover:
- Select agents from the index based on the topic
- Dispatch via Agent tool: `subagent_type: "[agent-name]"`, `prompt: [context block]`
- Platform loads the agent file as system prompt; context block is the task
- Read the context block template (`templates/context-block.md`) for structure
- Each agent writes its own report to `.plans/reviews/`
- Main agent writes a lead review synthesizing findings
- Read the session report template (`templates/session-report.md`) for format and naming

**Verify:** Instructions are clear enough that a main agent could dispatch 3 agents in parallel following this section alone

### Step 4: Write Mode 3 Dispatch Guidance

How the main agent creates a collaborative team.

**Input:** INT-1 Mode 3 contract, TeamCreate tool, INT-3 reporting contract, collab-mode.md
**Output:** Mode 3 section in the skill

**Important:** The items below describe the knowledge to convey in the skill, not a procedural structure to impose. The skill should explain these concepts as guidance the main agent can draw on, not as a step-by-step sequence to follow. See AC-6: the skill must contain no execution sequences or control flow.

Cover:
- Create team: `TeamCreate(team_name: "[name]", description: "[purpose]")`
- Spawn each teammate: `Agent(subagent_type: "[agent-name]", team_name: "[name]", name: "[agent-name]", prompt: [collab-mode content] + [context block])`
- Read collab-mode.md (`templates/collab-mode.md`) and include its content in each teammate's task prompt
- Teammates maintain context across the session — they see deltas, not just snapshots
- Teammates can message each other directly and share a task list
- User can interact directly with teammates via Shift+Down
- Don't shut down teammates prematurely — let them write their own reports first
- Each teammate writes their own report; main agent writes lead review
- Clean up: shut down teammates, then have the lead clean up the team
- **Prerequisites:** Agent teams require `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` enabled and Claude Code v2.1.32+
- **Fallback:** If agent teams are unavailable, fall back to Mode 2 (parallel subagents)

**Verify:** Instructions cover the full lifecycle: create → spawn → work → report → shutdown → cleanup

### Step 5: Write Session Management and Output Preservation

How to handle outputs and cross-session continuity.

**Input:** INT-3 contract, DATA-4 schema, REQ-N4
**Output:** Session management section in the skill

Cover:
- Every dispatched agent (all modes) writes its own report — this is the source of truth
- Main agent writes lead review for Modes 2 & 3
- Naming: `[ARTIFACT-ID]-[agent-name]-report.md`, `[ARTIFACT-ID]-lead-review.md`
- All reports go to `.plans/reviews/`
- Lead review includes reconstitution notes (Mode 3) — team composition, open concerns, context summary
- Planning artifacts (specs, designs, DIPs) should reference session reports for cross-session continuity
- The main agent should read reports proportionally to the stakes of the decision being informed

**Verify:** An agent could follow these instructions to preserve outputs and reconstitute a team in a later session

### Step 6: Write Skill Frontmatter and Description

The skill needs a name and description that are clearly differentiated from Superpowers' `dispatching-parallel-agents`.

**Input:** REQ-F10
**Output:** Skill frontmatter

- Name: `consult-team`
- Description: Must emphasize multi-perspective consultation on the same topic, not independent parallel tasks. The Superpowers skill is about splitting independent work; this skill is about getting different viewpoints on the same work.

**Verify:** Name and description would not be confused with `dispatching-parallel-agents` if both are installed

### Step 7: Assemble and Write the Skill File

Combine all sections into a single skill file.

**Input:** Steps 1-6 outputs
**Output:** `.claude/skills/consult-team/SKILL.md`

Structure:
1. Frontmatter (name, description)
2. Agent Index (from Step 1)
3. Decision Gate (from Step 2)
4. Mode 2 Guidance (from Step 3)
5. Mode 3 Guidance (from Step 4)
6. Session Management (from Step 5)

Keep the skill focused and readable. Remember: this is loaded context, not a manual. The main agent reads this and makes its own decisions. No control flow, no deterministic sequences.

**Verify:** Read the complete skill as a cold reader — could a main agent follow it to run a consultation session?

## Technical Requirements

### Must Implement
- [ ] Agent index with all 8 agents grouped by category
- [ ] Snapshot vs. delta decision gate
- [ ] Mode 2 dispatch instructions referencing Agent tool and context block template
- [ ] Mode 3 dispatch instructions referencing TeamCreate, Agent tool with team_name, and collab-mode.md
- [ ] Session report preservation instructions with naming conventions
- [ ] Mode 3 fallback guidance when agent teams are unavailable
- [ ] Clear differentiation from Superpowers' dispatching-parallel-agents

### Must Satisfy
| Requirement | How to Satisfy |
|-------------|----------------|
| REQ-N1 | Skill file optimized for dual consumption — human-readable AND effective when loaded into AI context |
| REQ-F3 | Skill provides: agent index, dispatch guidance, synthesis approach, output preservation |
| REQ-F10 | Name and description clearly distinct from Superpowers skill |
| REQ-F11 | Covers Mode 2 and Mode 3 with decision gate (Mode 1 is in command pointers) |
| REQ-N2 | Written as guidance, not control flow |
| REQ-N3 | Framed as optional — the main agent chooses whether to follow |

### Interfaces to Implement/Use
| Interface | Role | Contract Reference |
|-----------|------|-------------------|
| INT-1 | Skill guides dispatch per this contract | DESIGN-004 Section 4 |
| INT-2 | Commands reference this skill per this format | DESIGN-004 Section 4 |
| INT-3 | Skill guides reporting per this contract | DESIGN-004 Section 4 |

## Scope Boundaries

### DO (In Scope)
- Create the consult-team skill file at `.claude/skills/consult-team/SKILL.md`
- Reference all 8 agent files by name in the index
- Reference all 3 template files by path
- Document the three dispatch modes and decision gate
- Document session management and output preservation

### DO NOT (Out of Scope)
- Do not create or modify agent files (DIP-005)
- Do not create or modify templates (DIP-004)
- Do not modify command files (DIP-007)
- Do not implement hooks or quality gates
- Do not embed agent personas in the skill — index only

### Files in Scope
```
.claude/skills/consult-team/SKILL.md
```

### Files Out of Scope
```
.claude/agents/ (DIP-005)
.claude/skills/consult-team/templates/ (DIP-004)
.claude/commands/ (DIP-007)
```

## Acceptance Criteria

All criteria must pass for this DIP to be considered complete.

| ID | Criterion | Test |
|----|-----------|------|
| AC-1 | Given the skill is loaded, then it provides an index of all 8 agents with name, description, and category | Read skill; verify index covers all 8 agents |
| AC-2 | Given the skill is loaded, then it presents a decision gate between snapshot (Mode 2) and delta (Mode 3) dispatch | Read skill; verify the gate explains when each mode is appropriate |
| AC-3 | Given the skill is loaded, then it provides dispatch instructions for Mode 2 (Agent tool with subagent_type and prompt) | Read skill; verify Mode 2 instructions match INT-1 contract |
| AC-4 | Given the skill is loaded, then it provides dispatch instructions for Mode 3 (TeamCreate + Agent tool with team_name, collab-mode in prompt) | Read skill; verify Mode 3 instructions match INT-1 contract |
| AC-5 | Given the skill name and description, when compared to Superpowers' dispatching-parallel-agents, then they are clearly distinguishable | Compare descriptions; verify different emphasis |
| AC-6 | Given the skill content, then it contains no execution sequences or control flow — only guidance and decision frameworks | Read skill; verify no "then do X, then do Y" deterministic flows |

### Verification Commands
```bash
# Verify skill file exists
ls .claude/skills/consult-team/SKILL.md

# Verify all 8 agents referenced in index
grep -c "critic\|skeptic\|user-advocate\|stakeholder\|designer\|project-manager\|prompt-engineer\|consistency-reviewer" .claude/skills/consult-team/SKILL.md
# Expected: >= 8 matches

# Verify decision gate keywords present
grep -c "snapshot\|delta\|decision" .claude/skills/consult-team/SKILL.md
# Expected: multiple matches

# Verify template references
grep -c "context-block\|session-report\|collab-mode" .claude/skills/consult-team/SKILL.md
# Expected: >= 3 matches
```

## Safety Checklist

Before committing, verify:

- [ ] No secrets, keys, or credentials in code
- [ ] No `git add .` or `git add -A` used
- [ ] All new files explicitly added
- [ ] Conventional commit message prepared
- [ ] No unrelated changes included

## Commit Instructions

When implementation is complete:

```bash
# Stage only the skill file
git add .claude/skills/consult-team/SKILL.md

# Commit with conventional format
git commit -m "feat(agents): add consult-team skill (DIP-006)

Implements DIP-006: agent index, snapshot/delta decision gate,
Mode 2 and Mode 3 dispatch guidance, session management.
Satisfies: REQ-F3, REQ-F10, REQ-F11, REQ-N1, REQ-N2, REQ-N3"
```

**Commit type:** feat
**Scope:** agents

## Completion Checklist

- [ ] All implementation steps completed
- [ ] All acceptance criteria verified
- [ ] Safety checklist passed
- [ ] Code committed with proper message
- [ ] PLANNING.md updated with completion status

## Notes

- This skill is the linchpin of the consultation system — it's what makes the difference between "user remembers to tell the agent about teams" and "the guidance is loaded and available"
- The decision gate is the most important section. If the agent reads nothing else, the gate should help it choose correctly between Mode 2 and Mode 3
- Keep it concise. The theory-of-change skill's problem was embedding ~90 lines of methodology that could have been loaded on demand. This skill should be tight enough that loading it doesn't bloat the context significantly
- The skill should feel like advice from an experienced colleague, not a manual to follow step by step
- AC-6 is the quality gate: if the skill reads like control flow, it needs to be rewritten as guidance

---

**End of DIP-006**