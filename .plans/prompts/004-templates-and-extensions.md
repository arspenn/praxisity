# DIP-004: Templates, Extensions, and Directory Structure

> **For AI Agent:** This is a Detailed Implementation Prompt. Follow these instructions precisely.
> Read all referenced documents before beginning implementation.
>
> **TodoWrite Integration:** Use Claude's TodoWrite tool to track progress through this DIP.
> Create todos from the Implementation Steps below and mark them complete as you progress.

## Context

| Field | Value |
|-------|-------|
| DIP ID | DIP-004 |
| Task | Create directory structure, context block template, session report template, and collaborative mode extension |
| Spec | [SPEC-005](../specs/005-agent-consultation-system.md) |
| Design | [DESIGN-004](../designs/004-agent-consultation-system.md) |
| Todoist Task | N/A |
| Created | 2026-03-28 |

## Objective

Create the foundational directory structure and three template/extension files (context block template, session report template, collab-mode.md) that all other SPEC-005 components depend on.

## Required Reading

Before implementation, read and understand these sections:

### From Specification (SPEC-005)
- [ ] Section 3.1: REQ-F2 - Agent files immutable; customization appended as context block
- [ ] Section 3.1: REQ-F8 - Every dispatched agent writes its own report to `.plans/reviews/`
- [ ] Section 3.1: REQ-F12 - Mode 3 teammates are full parallel sessions with self-authored reports
- [ ] Section 3.2: REQ-N4 - Team composition documented in session reports and referenced by planning artifacts

### From Design (DESIGN-004)
- [ ] Section 3: COMP-2 - Templates and Extensions (responsibilities, key design decisions)
- [ ] Section 4: INT-1 - Agent Dispatch Interface (prompt assembly contract)
- [ ] Section 4: INT-3 - Session Report Interface (reporting contract, naming conventions)
- [ ] Section 5: DATA-2 - Collaborative Mode Extension (schema)
- [ ] Section 5: DATA-3 - Context Block (schema)
- [ ] Section 5: DATA-4 - Session Report (schema for agent report and lead review)
- [ ] Section 6: DEC-2 - Layered Prompt Assembly (agent + collab + customization)
- [ ] Section 6: DEC-3 - Every Agent Writes Its Own Report

### From Charter
- [ ] Principles: Dual-use design (human-readable AND AI-consumable)
- [ ] Principles: Minimal cognitive overhead

## Implementation Instructions

### Step 1: Create Directory Structure

Create the directories needed by the agent consultation system.

**Input:** Current repo structure
**Output:** New directories exist:
- `.plans/reviews/` (with `.gitkeep`)
- `.claude/skills/consult-team/` (home for the skill, created now for DIP-006)
- `.claude/skills/consult-team/templates/` (home for context block and session report templates)
- `.claude/agents/` (should already exist from fresh-eyes-reviewer work)

**Verify:** `ls -la` each directory confirms it exists

### Step 2: Create Context Block Template

Create the standardized structure that the main agent fills and uses as the task prompt when dispatching agents.

**Input:** DATA-3 schema from DESIGN-004, INT-1 dispatch contract
**Output:** `.claude/skills/consult-team/templates/context-block.md`

In all modes, the platform loads the agent file as the system prompt. The context block becomes the task prompt (`prompt` parameter in the Agent tool):
- **Modes 1 & 2:** `Agent(subagent_type: "[name]", prompt: [context block])`
- **Mode 3:** `Agent(subagent_type: "[name]", team_name: "...", prompt: [collab-mode content] + [context block])` — collab-mode.md content is prepended to the context block in the task prompt
- **Fallback:** `Agent(subagent_type: "general-purpose", prompt: [agent file content] + [context block])`

The template provides structure but the main agent writes naturally within it. It is NOT a rigid form — it's a guide. The template should note these delivery mechanisms so the consult-team skill (DIP-006) can reference them.

**Content per DATA-3 schema:**
- Section identifier (main agent writes a heading marking this as the context/task section)
- Phase: current workflow phase (specifying, designing, reviewing, etc.)
- Topic: what's being evaluated
- Focus: (optional) specific aspects to pay attention to
- Materials: file paths or inline content to review

**Verify:** File exists, is human-readable, follows the schema, and documents the three delivery mechanisms

### Step 3: Create Session Report Template

Create the flexible template used by all agents (all modes) for writing their reports, and by the main agent for lead reviews.

**Input:** DATA-4 schema from DESIGN-004
**Output:** `.claude/skills/consult-team/templates/session-report.md`

One flexible template covers both agent reports and lead reviews. Sections are left empty when not applicable.

**Agent report sections (every dispatched agent, all modes):**
- Metadata: artifact ID, date, agent name, dispatch mode
- Instructions received: the customization block they were given
- Findings: analysis and recommendations
- Self-evaluation: what worked, what they struggled with, prompt improvement suggestions

**Lead review sections (main agent, Modes 2 & 3):**
- Metadata: artifact ID, date, team composition, dispatch mode
- Per-agent assessment: quality of work, instruction fidelity, context retention
- Synthesis: cross-perspective analysis, areas of agreement/disagreement
- Reconstitution notes (Mode 3 only): team composition, open concerns, context summary for next session

**Naming convention (document in template header):**
- Agent reports: `[ARTIFACT-ID]-[agent-name]-report.md`
- Lead reviews: `[ARTIFACT-ID]-lead-review.md`
- All reports go to `.plans/reviews/`

**Verify:** Template is clear enough that an agent reading it cold could produce a well-structured report

### Step 4: Create Collaborative Mode Extension

Create `collab-mode.md` — the single shared file that adds Mode 3 awareness to any agent when appended between the agent file and the customization block.

**Input:** DATA-2 schema from DESIGN-004, INT-1 Mode 3 contract
**Output:** `.claude/skills/consult-team/templates/collab-mode.md`

This file contains ONLY what's different about being a persistent teammate vs. a one-shot subagent. It must not duplicate anything from agent definition files.

**Sections per DATA-2 schema:**
- Session awareness: you are a persistent teammate, not a subagent; you maintain context across the session
- Direct capabilities: can write files to `.plans/reviews/`, can request relay to user, user may interact directly via Shift+Down
- Reporting duties: write your own report including findings, the instructions you received, and self-evaluation
- Team dynamics: maintain your perspective even in disagreement; flag changes that affect your domain

**Verify:** File is focused, doesn't duplicate agent file content, and would make sense appended to any of the 8 agent definitions

## Technical Requirements

### Must Implement
- [ ] All three template files follow dual-consumption principle (human-readable AND AI-effective)
- [ ] Session report template uses one flexible format for all modes (not separate templates)
- [ ] Collab-mode.md is agent-agnostic (works with any of the 8 agents)
- [ ] Context block template is a guide, not a rigid form
- [ ] All files use markdown format

### Must Satisfy
| Requirement | How to Satisfy |
|-------------|----------------|
| REQ-F2 | Context block template provides the standardized structure for appended customization |
| REQ-F8 | Session report template defines the format agents use to write their own reports |
| REQ-F12 | Collab-mode.md provides Mode 3 awareness including self-authored reporting and direct user interaction |
| REQ-N4 | Session report template includes reconstitution notes section for Mode 3 lead reviews |

### Interfaces to Implement/Use
| Interface | Role | Contract Reference |
|-----------|------|-------------------|
| INT-1 | Context block template used in prompt assembly | DESIGN-004 Section 4 |
| INT-3 | Session report template defines output format | DESIGN-004 Section 4 |

### Data Entities to Create/Modify
| Entity | Action | Schema Reference |
|--------|--------|-----------------|
| DATA-2 | Create (collab-mode.md) | DESIGN-004 Section 5 |
| DATA-3 | Create (context block template) | DESIGN-004 Section 5 |
| DATA-4 | Create (session report template) | DESIGN-004 Section 5 |

## Scope Boundaries

### DO (In Scope)
- Create `.plans/reviews/` directory with `.gitkeep`
- Create `.claude/skills/consult-team/templates/` directory
- Create context block template
- Create session report template
- Create collab-mode.md

### DO NOT (Out of Scope)
- Do not create agent definition files (DIP-005)
- Do not create the consult-team skill (DIP-006)
- Do not modify existing command files (DIP-007)
- Do not write any agent persona content
- Do not modify files outside the scope listed below

### Files in Scope
```
.plans/reviews/.gitkeep
.claude/skills/consult-team/templates/context-block.md
.claude/skills/consult-team/templates/session-report.md
.claude/skills/consult-team/templates/collab-mode.md
```

### Files Out of Scope
```
.claude/agents/ (DIP-005)
.claude/skills/consult-team/SKILL.md (DIP-006)
.claude/commands/ (DIP-007)
```

## Acceptance Criteria

All criteria must pass for this DIP to be considered complete.

| ID | Criterion | Test |
|----|-----------|------|
| AC-1 | Given the context block template, when read by an agent, then it provides clear structure for phase, topic, focus, and materials fields | Read the template; confirm all DATA-3 fields are present and understandable |
| AC-2 | Given the session report template, when used by a dispatched agent, then it provides structure for metadata, instructions received, findings, and self-evaluation | Read the template; confirm all DATA-4 agent report fields are present |
| AC-3 | Given the session report template, when used by the main agent for a lead review, then it provides structure for metadata, per-agent assessment, synthesis, and reconstitution notes | Read the template; confirm all DATA-4 lead review fields are present |
| AC-4 | Given collab-mode.md, when appended to any agent file, then it adds session awareness, direct capabilities, reporting duties, and team dynamics without duplicating agent file content | Read collab-mode.md; confirm all DATA-2 sections present; confirm no overlap with agent Identity/Reasoning/Output/Self-Eval sections |
| AC-5 | Given the naming convention in the session report template, when an agent writes a report, then the filename follows `[ARTIFACT-ID]-[agent-name]-report.md` pattern | Read template header; confirm convention is documented |

### Verification Commands
```bash
# Verify directories exist
ls -la .plans/reviews/.gitkeep
ls -la .claude/skills/consult-team/templates/

# Verify all three template files exist
ls .claude/skills/consult-team/templates/context-block.md
ls .claude/skills/consult-team/templates/session-report.md
ls .claude/skills/consult-team/templates/collab-mode.md

# Verify collab-mode.md doesn't contain agent persona sections
grep -c "## Identity\|## Reasoning Approach\|## Output Format" .claude/skills/consult-team/templates/collab-mode.md
# Expected: 0
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
# Stage only files in scope
git add .plans/reviews/.gitkeep \
  .claude/skills/consult-team/templates/context-block.md \
  .claude/skills/consult-team/templates/session-report.md \
  .claude/skills/consult-team/templates/collab-mode.md

# Commit with conventional format
git commit -m "feat(agents): add templates, extensions, and directory structure (DIP-004)

Implements DIP-004: context block template, session report template, collab-mode.md
Satisfies: REQ-F2, REQ-F8, REQ-F12, REQ-N4"
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

- These templates will be referenced by DIP-005 (agent files), DIP-006 (consult-team skill), and DIP-007 (command pointers)
- The context block template should feel like a guide, not a form — agents should write naturally within its structure
- Collab-mode.md is the ONLY file that differs between Mode 1/2 and Mode 3 dispatch — keep it focused on that delta
- The session report template's flexibility is key — one template, not separate ones per mode

---

**End of DIP-004**
