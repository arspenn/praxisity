# DIP-007: Tier 1 Command Pointers

> **For AI Agent:** This is a Detailed Implementation Prompt. Follow these instructions precisely.
> Read all referenced documents before beginning implementation.
>
> **TodoWrite Integration:** Use Claude's TodoWrite tool to track progress through this DIP.
> Create todos from the Implementation Steps below and mark them complete as you progress.

## Context

| Field | Value |
|-------|-------|
| DIP ID | DIP-007 |
| Task | Add compact agent consultation pointers to 3 thinking commands |
| Spec | [SPEC-005](../specs/005-agent-consultation-system.md) |
| Design | [DESIGN-004](../designs/004-agent-consultation-system.md) |
| Todoist Task | N/A |
| Created | 2026-03-29 |

## Objective

Add a compact Tier 1 agent consultation pointer to the three thinking commands (`/spec`, `/architect`, `/charter`) following the INT-2 contract format, and verify the four doing commands (`/build`, `/deliver`, `/breakdown`, `/define`) have no agent pointers.

## Required Reading

Before implementation, read and understand these sections:

### From Specification (SPEC-005)
- [ ] Section 3.1: REQ-F5 - Thinking commands include compact Tier 1 pointer
- [ ] Section 3.1: REQ-F6 - Doing commands have no agent pointers
- [ ] Section 3.2: REQ-N3 - Consultation always optional

### From Design (DESIGN-004)
- [ ] Section 3: COMP-4 - Tier 1 Command Pointers (responsibilities, natural-fit agents per command)
- [ ] Section 4: INT-2 - Command Pointer Interface (the authoritative format)
- [ ] Section 6: DEC-1 - Three-Mode Dispatch with Decision Gate (Mode 1 inline, Modes 2 & 3 via skill)

### Reference Files (must exist before this DIP)
- [ ] `.claude/skills/consult-team/SKILL.md` (DIP-006 output — skill must exist to reference)

## Implementation Instructions

### Step 1: Read the INT-2 Contract Format

The authoritative pointer format from DESIGN-004 INT-2:

```markdown
## Agent Consultation

For a quick single perspective, dispatch: [agent name], [agent name], or [agent name].
For multi-agent input (parallel or collaborative), invoke the consult-team skill.
```

Mode 1 (single consult): main agent dispatches directly using Agent tool with `subagent_type`.
Modes 2 & 3: main agent invokes consult-team skill via Skill tool, then follows loaded guidance including the decision gate.

**Verify:** You understand the format and the Mode 1 vs. Modes 2 & 3 split

### Step 2: Add Pointer to `/spec`

**Input:** `.claude/commands/spec.md`
**Output:** Same file with pointer appended (or inserted at an appropriate location)

Natural-fit agents for `/spec`: **Critic, User Advocate, Skeptic**

Rationale: Spec work benefits from adversarial review (Critic), user perspective (User Advocate), and scope challenge (Skeptic).

Add the pointer section using the INT-2 format with these three agents listed.

**Verify:** Pointer is present, lists the correct 3 agents, references the consult-team skill

### Step 3: Add Pointer to `/architect`

**Input:** `.claude/commands/architect.md`
**Output:** Same file with pointer added

Natural-fit agents for `/architect`: **Designer, Prompt Engineer, Critic**

Rationale: Design work benefits from architecture review (Designer), dual-consumption quality check (Prompt Engineer), and weakness finding (Critic).

**Verify:** Pointer is present, lists the correct 3 agents, references the consult-team skill

### Step 4: Add Pointer to `/charter`

**Input:** `.claude/commands/charter.md`
**Output:** Same file with pointer added

Natural-fit agents for `/charter`: **Stakeholder, Project Manager**

Rationale: Charter work benefits from audience perspective (Stakeholder) and feasibility check (Project Manager).

**Verify:** Pointer is present, lists the correct 2 agents, references the consult-team skill

### Step 5: Verify Doing Commands Have No Pointers

Check that `/build`, `/deliver`, `/breakdown`, `/define` do NOT contain agent consultation pointers.

**Input:** `.claude/commands/build.md`, `.claude/commands/deliver.md`, `.claude/commands/breakdown.md`, `.claude/commands/define.md`
**Output:** Confirmation that none contain "Agent Consultation" sections or references to consult-team skill

**Verify:** Grep returns no matches

## Technical Requirements

### Must Implement
- [ ] Pointer in `/spec` with Critic, User Advocate, Skeptic
- [ ] Pointer in `/architect` with Designer, Prompt Engineer, Critic
- [ ] Pointer in `/charter` with Stakeholder, Project Manager
- [ ] All pointers follow INT-2 contract format exactly
- [ ] No pointers in `/build`, `/deliver`, `/breakdown`, `/define`

### Must Satisfy
| Requirement | How to Satisfy |
|-------------|----------------|
| REQ-F5 | Compact pointer in 3 thinking commands, per INT-2 format |
| REQ-F6 | No pointers in 4 doing commands |
| REQ-N3 | Pointers suggest consultation, never require it |

## Scope Boundaries

### DO (In Scope)
- Add pointer section to `/spec`, `/architect`, `/charter` command files
- Verify doing commands have no pointers

### DO NOT (Out of Scope)
- Do not modify agent files (DIP-005)
- Do not modify the consult-team skill (DIP-006)
- Do not modify templates (DIP-004)
- Do not change any other part of the command files — targeted addition only
- Do not add pointers to doing commands

### Files in Scope
```
.claude/commands/spec.md
.claude/commands/architect.md
.claude/commands/charter.md
```

### Files Out of Scope
```
.claude/commands/build.md (verify only — no changes)
.claude/commands/deliver.md (verify only — no changes)
.claude/commands/breakdown.md (verify only — no changes)
.claude/commands/define.md (verify only — no changes)
.claude/agents/ (DIP-005)
.claude/skills/ (DIP-006)
```

## Acceptance Criteria

All criteria must pass for this DIP to be considered complete.

| ID | Criterion | Test |
|----|-----------|------|
| AC-1 | Given `/spec` command file, when inspected, then it contains a Tier 1 pointer listing Critic, User Advocate, Skeptic and referencing consult-team skill | Grep for "Agent Consultation" in spec.md |
| AC-2 | Given `/architect` command file, when inspected, then it contains a Tier 1 pointer listing Designer, Prompt Engineer, Critic and referencing consult-team skill | Grep for "Agent Consultation" in architect.md |
| AC-3 | Given `/charter` command file, when inspected, then it contains a Tier 1 pointer listing Stakeholder, Project Manager and referencing consult-team skill | Grep for "Agent Consultation" in charter.md |
| AC-4 | Given all doing command files, when inspected, then none contain "Agent Consultation" or "consult-team" | Grep returns no matches across 4 doing commands |

### Verification Commands
```bash
# Verify pointers exist in thinking commands
grep -l "Agent Consultation" .claude/commands/spec.md .claude/commands/architect.md .claude/commands/charter.md
# Expected: 3 files listed

# Verify consult-team referenced
grep -l "consult-team" .claude/commands/spec.md .claude/commands/architect.md .claude/commands/charter.md
# Expected: 3 files listed

# Verify NO pointers in doing commands
grep -l "Agent Consultation\|consult-team" .claude/commands/build.md .claude/commands/deliver.md .claude/commands/breakdown.md .claude/commands/define.md
# Expected: no output (exit code 1)
```

## Safety Checklist

Before committing, verify:

- [ ] No secrets, keys, or credentials in code
- [ ] No `git add .` or `git add -A` used
- [ ] All modified files explicitly added
- [ ] Conventional commit message prepared
- [ ] No unrelated changes to command files — pointer addition only

## Commit Instructions

When implementation is complete:

```bash
# Stage only modified command files
git add .claude/commands/spec.md \
  .claude/commands/architect.md \
  .claude/commands/charter.md

# Commit with conventional format
git commit -m "feat(agents): add Tier 1 consultation pointers to thinking commands (DIP-007)

Implements DIP-007: /spec, /architect, /charter get agent consultation pointers.
/build, /deliver, /breakdown, /define confirmed clean.
Satisfies: REQ-F5, REQ-F6, REQ-N3"
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

- This is the lightest DIP in the set — 3 targeted edits to existing files
- The pointer is an addition, not a replacement — don't change any other part of the command files
- The pointer text is suggestive, not directive — "For a quick single perspective, dispatch..." not "You must dispatch..."
- After this DIP, the full agent consultation system is implemented and ready for bootstrapping test

---

**End of DIP-007**
