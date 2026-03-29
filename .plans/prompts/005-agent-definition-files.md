# DIP-005: Agent Definition Files (8 Agents)

> **For AI Agent:** This is a Detailed Implementation Prompt. Follow these instructions precisely.
> Read all referenced documents before beginning implementation.
>
> **TodoWrite Integration:** Use Claude's TodoWrite tool to track progress through this DIP.
> Create todos from the Implementation Steps below and mark them complete as you progress.

## Context

| Field | Value |
|-------|-------|
| DIP ID | DIP-005 |
| Task | Create 8 native Claude Code subagent files in `.claude/agents/` |
| Spec | [SPEC-005](../specs/005-agent-consultation-system.md) |
| Design | [DESIGN-004](../designs/004-agent-consultation-system.md) |
| Todoist Task | N/A |
| Created | 2026-03-29 |

## Objective

Create the 8 agent persona files as native Claude Code subagents, each following the standardized format (YAML frontmatter + markdown body with Identity, Reasoning Approach, Output Format, Self-Evaluation sections). The consistency-reviewer.md already exists and serves as the reference implementation — write the remaining 7 agents to match its quality and structure.

## Required Reading

Before implementation, read and understand these sections:

### From Specification (SPEC-005)
- [ ] Section 3.1: REQ-F1 - Native Claude Code subagent format with required/optional fields
- [ ] Section 3.1: REQ-F2 - Agent files immutable at dispatch; customization is the task prompt
- [ ] Section 3.1: REQ-F4 - 8 agents across 4 categories
- [ ] Section 3.1: REQ-F7 - Self-evaluation in every agent output
- [ ] Section 3.1: REQ-F8 - Every agent writes its own report to `.plans/reviews/`
- [ ] Section 3.2: REQ-N1 - Dual consumption (human-readable AND AI-effective)

### From Design (DESIGN-004)
- [ ] Section 3: COMP-1 - Agent Definition Files (roster, format, key design decisions)
- [ ] Section 5: DATA-1 - Agent Definition File schema (frontmatter fields, markdown body sections)
- [ ] Section 6: DEC-4 - Native Claude Code Subagent Format rationale

### Reference Implementation
- [ ] `.claude/agents/consistency-reviewer.md` - The existing agent file; use as the pattern for structure, tone, and length

### From Claude Code Documentation
- [ ] [Sub-agents](https://code.claude.com/docs/en/sub-agents) - Supported frontmatter fields, tool restrictions, memory feature

## Implementation Instructions

### Step 1: Review the Reference Implementation

Read `.claude/agents/consistency-reviewer.md` carefully. Note:
- Frontmatter structure (name, description, category, tools, model, memory)
- How Identity establishes perspective in 2-3 sentences
- How Reasoning Approach provides a concrete checklist without being exhaustive
- How Output Format gives structure without being rigid
- How Self-Evaluation prompts specific reflection
- The overall length and density — focused, not bloated
- The Project Context section that orients the agent to Praxisity
- The Critical Rules section that prevents specific failure modes

This is the bar. Each agent should match this quality and conciseness.

**Verify:** You can articulate what makes consistency-reviewer effective before writing others

### Step 2: Write Evaluative Agents (Critic, Skeptic)

Create two agents that stress-test work from different angles.

**Critic** (`critic.md`):
- Category: evaluative
- Core question: "What's wrong with this?"
- Finds weaknesses, contradictions, unstated assumptions, scope creep
- Naturally adversarial but constructive — strengthen the work, not reject it
- Tools: Read, Grep, Glob, Write (review-focused)

**Skeptic** (`skeptic.md`):
- Category: evaluative
- Core question: "Do we even need this?"
- Challenges whether something is necessary at all
- The YAGNI enforcer — questions scope, not quality
- Tools: Read, Grep, Glob, Write (review-focused)

**Input:** COMP-1 roster descriptions, consistency-reviewer as structural reference
**Output:** `.claude/agents/critic.md`, `.claude/agents/skeptic.md`
**Verify:** Each file has correct frontmatter, all 4 body sections, focused identity, and would produce differentiated output from the other evaluative agent

### Step 3: Write Perspective Agents (User Advocate, Stakeholder)

Create two agents that represent viewpoints the author can't easily hold.

**User Advocate** (`user-advocate.md`):
- Category: perspective
- Core question: "Would a new user understand and benefit?"
- Represents the solo practitioner being onboarded into structured AI workflows
- Connected to the framework's "build the user" philosophy — does this help someone learn, not just produce output?
- Tools: Read, Grep, Glob, Write (review-focused)

**Stakeholder** (`stakeholder.md`):
- Category: perspective
- Core question: "Does the output serve its audience?"
- Represents someone consuming the outputs (professor, client, collaborator)
- Evaluates whether the process produces things that are useful to the people they're for
- Tools: Read, Grep, Glob, Write (review-focused)

**Input:** COMP-1 roster descriptions, consistency-reviewer as structural reference
**Output:** `.claude/agents/user-advocate.md`, `.claude/agents/stakeholder.md`
**Verify:** Each perspective is distinct and represents a viewpoint the author genuinely can't hold while writing

### Step 4: Write Structural Agents (Designer, Project Manager)

Create two agents that ensure the design holds together.

**Designer** (`designer.md`):
- Category: structural
- Core question: "How do the pieces fit together?"
- Thinks about architecture, interfaces, component boundaries, progressive loading tradeoffs
- Evaluates whether pieces compose well and have minimal surface area
- Tools: Read, Grep, Glob, Write (review-focused)

**Project Manager** (`project-manager.md`):
- Category: structural
- Core question: "What's realistic and what blocks what?"
- Tracks scope, dependencies, sequencing, what's realistic for a solo developer
- Guards against redesigning everything at once
- Tools: Read, Grep, Glob, Write (review-focused)

**Input:** COMP-1 roster descriptions, consistency-reviewer as structural reference
**Output:** `.claude/agents/designer.md`, `.claude/agents/project-manager.md`
**Verify:** Designer focuses on how things fit; PM focuses on whether they're achievable — distinct concerns

### Step 5: Write Prompt Engineer Agent

**Prompt Engineer** (`prompt-engineer.md`):
- Category: meta
- Core question: "Is this optimized for both humans and AI?"
- Evaluates dual-consumption quality of files that are both prompt output and prompt input
- Checks for: clear/unambiguous instructions, good signal-to-noise ratio, "don't think about elephants" problems, consistent behavior across sessions
- Tools: Read, Grep, Glob, Write (review-focused)

**Input:** COMP-1 roster descriptions, consistency-reviewer as structural reference
**Output:** `.claude/agents/prompt-engineer.md`
**Verify:** This agent's perspective is distinct from Consistency Reviewer — Prompt Engineer evaluates prompt quality, Consistency Reviewer checks cross-document consistency

### Step 6: Verify All 8 Agents

Run verification across all agent files.

**Input:** All 8 files in `.claude/agents/`
**Output:** Verification results
**Verify:**
- All 8 files exist with correct names
- All frontmatter has: name, description, category, tools, model, memory
- All bodies have: Identity (or equivalent), Reasoning Approach, Output Format, Self-Evaluation
- No two agents have overlapping core questions or would produce redundant output
- All agents reference `.plans/reviews/` for report writing
- All agents include Project Context section for Praxisity orientation
- All agents include Critical Rules section

## Technical Requirements

### Must Implement
- [ ] All 8 agents use native Claude Code subagent format (YAML frontmatter + markdown body)
- [ ] All agents have `tools: Read, Grep, Glob, Write` (restricted, per SPEC-005 Section 8)
- [ ] All agents have `model: inherit`
- [ ] All agents have `memory: project` (COULD priority — include it)
- [ ] All agents have `category` custom field for consult-team skill grouping
- [ ] All agent descriptions are concise routing hints (one sentence), not multi-paragraph scripts
- [ ] All agents are standalone-functional (no assumption of appended content)

### Must Satisfy
| Requirement | How to Satisfy |
|-------------|----------------|
| REQ-F1 | Native Claude Code subagent format with correct field classification |
| REQ-F4 | 8 files: critic, skeptic, user-advocate, stakeholder, designer, project-manager, prompt-engineer, consistency-reviewer |
| REQ-F7 | Self-Evaluation section in each agent's body instructs reflection |
| REQ-F8 | Output Format section instructs agents to write reports to `.plans/reviews/` |
| REQ-N1 | All files optimized for dual consumption |

### Data Entities to Create/Modify
| Entity | Action | Schema Reference |
|--------|--------|-----------------|
| DATA-1 | Create (7 new agent files; consistency-reviewer already exists) | DESIGN-004 Section 5 |

## Scope Boundaries

### DO (In Scope)
- Write 7 new agent definition files in `.claude/agents/`
- Verify consistency-reviewer.md conforms to the same standard
- Ensure all 8 agents are differentiated in perspective

### DO NOT (Out of Scope)
- Do not create the consult-team skill (DIP-006)
- Do not modify command files (DIP-007)
- Do not create or modify templates (DIP-004)
- Do not write collab-mode.md (DIP-004)
- Do not populate agent memory directories
- Do not test dispatch mechanisms (bootstrapping test is separate)

### Files in Scope
```
.claude/agents/critic.md
.claude/agents/skeptic.md
.claude/agents/user-advocate.md
.claude/agents/stakeholder.md
.claude/agents/designer.md
.claude/agents/project-manager.md
.claude/agents/prompt-engineer.md
.claude/agents/consistency-reviewer.md (verify only, already exists)
```

### Files Out of Scope
```
.claude/skills/ (DIP-006)
.claude/commands/ (DIP-007)
.claude/skills/consult-team/templates/ (DIP-004)
```

## Acceptance Criteria

All criteria must pass for this DIP to be considered complete.

| ID | Criterion | Test |
|----|-----------|------|
| AC-1 | Given `.claude/agents/`, when listed, then it contains exactly 8 `.md` files matching the roster | `ls .claude/agents/*.md \| wc -l` returns 8 |
| AC-2 | Given any agent file, when its frontmatter is inspected, then it contains name, description, category, tools, model, and memory fields | Inspect each file's frontmatter |
| AC-3 | Given any agent file, when its body is inspected, then it contains Identity, Reasoning Approach, Output Format, and Self-Evaluation sections | Grep for section headers across all files |
| AC-4 | Given any two agents, when their core questions are compared, then they are distinct and would produce non-redundant output | Read all agents; confirm no two overlap in what they evaluate |
| AC-5 | Given any agent file, when its Output Format section is inspected, then it instructs the agent to write a report to `.plans/reviews/` | Grep for `.plans/reviews/` across all agent files |

### Verification Commands
```bash
# Count agent files
ls .claude/agents/*.md | wc -l
# Expected: 8 (plus any -old/-generated variants from testing)

# Verify all have category field
grep -l "^category:" .claude/agents/critic.md .claude/agents/skeptic.md .claude/agents/user-advocate.md .claude/agents/stakeholder.md .claude/agents/designer.md .claude/agents/project-manager.md .claude/agents/prompt-engineer.md .claude/agents/consistency-reviewer.md
# Expected: 8 files listed

# Verify all reference .plans/reviews/
grep -l "plans/reviews" .claude/agents/*.md
# Expected: 8 files listed

# Verify all have Self-Evaluation section
grep -l "Self-Evaluation\|Self Evaluation" .claude/agents/*.md
# Expected: 8 files listed
```

## Safety Checklist

Before committing, verify:

- [ ] No secrets, keys, or credentials in agent files
- [ ] No `git add .` or `git add -A` used
- [ ] All new files explicitly added
- [ ] Conventional commit message prepared
- [ ] No unrelated changes included

## Commit Instructions

When implementation is complete:

```bash
# Stage only agent files
git add .claude/agents/critic.md \
  .claude/agents/skeptic.md \
  .claude/agents/user-advocate.md \
  .claude/agents/stakeholder.md \
  .claude/agents/designer.md \
  .claude/agents/project-manager.md \
  .claude/agents/prompt-engineer.md

# Commit with conventional format
git commit -m "feat(agents): add 7 agent definition files (DIP-005)

Implements DIP-005: Critic, Skeptic, User Advocate, Stakeholder,
Designer, Project Manager, Prompt Engineer
Satisfies: REQ-F1, REQ-F4, REQ-F7, REQ-F8, REQ-N1"
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

- Write the Critic first — it's the most natural counterpart to the Consistency Reviewer and will help calibrate the style for the remaining agents
- Each agent should feel like a distinct professional with a clear lens, not a generic reviewer with a different label
- Resist the urge to make agents exhaustive — the consistency-reviewer is the right density
- The `description` field is a routing hint for the platform — keep it one sentence
- Agents will accumulate project-specific knowledge via `memory: project` over time; don't try to frontload domain knowledge

---

**End of DIP-005**