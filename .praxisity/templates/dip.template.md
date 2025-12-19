# DIP-[NNN]: [Task Title]

> **For AI Agent:** This is a Detailed Implementation Prompt. Follow these instructions precisely.
> Read all referenced documents before beginning implementation.
>
> **TodoWrite Integration:** Use Claude's TodoWrite tool to track progress through this DIP.
> Create todos from the Implementation Steps below and mark them complete as you progress.

## Context

| Field | Value |
|-------|-------|
| DIP ID | DIP-[NNN] |
| Task | [Brief task description] |
| Spec | [SPEC-NNN](../../.plans/specs/NNN-name.md) |
| Design | [DESIGN-NNN](../../.plans/designs/NNN-name.md) |
| Todoist Task | [Task ID or link] |
| Created | [YYYY-MM-DD] |

## Objective

[One clear sentence: What must be accomplished when this DIP is complete.]

## Required Reading

Before implementation, read and understand these sections:

### From Specification (SPEC-[NNN])
- [ ] Section 3.1: REQ-[F/N][N] - [Requirement title]
- [ ] Section 3.1: REQ-[F/N][N] - [Requirement title]
- [ ] Section 4: UC-[N] - [Use case title]
- [ ] Section 5: AC-[N] - [Acceptance criterion]

### From Design (DESIGN-[NNN])
- [ ] Section 3: COMP-[N] - [Component name]
- [ ] Section 4: INT-[N] - [Interface name]
- [ ] Section 5: DATA-[N] - [Data entity name]
- [ ] Section 6: DEC-[N] - [Relevant design decision]

### From Charter
- [ ] Principles: [Relevant principle that applies]
- [ ] Constraints: [Relevant constraint that applies]

## Implementation Instructions

> **Agent Action:** Before starting, use TodoWrite to create todos from these steps:
> ```
> TodoWrite([
>   { content: "Read required spec/design sections", status: "pending", activeForm: "Reading documentation" },
>   { content: "Step 1: [First Action]", status: "pending", activeForm: "[First Action active form]" },
>   { content: "Step 2: [Second Action]", status: "pending", activeForm: "[Second Action active form]" },
>   { content: "Verify acceptance criteria", status: "pending", activeForm: "Verifying acceptance criteria" },
>   { content: "Complete safety checklist and commit", status: "pending", activeForm: "Completing safety checklist" }
> ])
> ```
> Mark each todo in_progress when starting, completed when done.

### Step 1: [First Action]

[Specific instruction for what to do first]

**Input:** [What you're working with]
**Output:** [What should exist after this step]
**Verify:** [How to confirm this step succeeded]

**TodoWrite:** Mark "Step 1" as `in_progress` before starting, `completed` when done.

### Step 2: [Second Action]

[Specific instruction]

**Input:** [What you're working with]
**Output:** [What should exist after this step]
**Verify:** [How to confirm this step succeeded]

**TodoWrite:** Mark "Step 2" as `in_progress` before starting, `completed` when done.

### Step 3: [Third Action]

[Continue as needed...]

**TodoWrite:** Mark "Step 3" as `in_progress` before starting, `completed` when done.

## Technical Requirements

### Must Implement
- [ ] [Specific technical requirement from spec/design]
- [ ] [Specific technical requirement from spec/design]
- [ ] [Specific technical requirement from spec/design]

### Must Satisfy
| Requirement | How to Satisfy |
|-------------|----------------|
| REQ-[F/N][N] | [Specific implementation approach] |
| REQ-[F/N][N] | [Specific implementation approach] |

### Interfaces to Implement/Use
| Interface | Role | Contract Reference |
|-----------|------|-------------------|
| INT-[N] | [Implement/Consume] | DESIGN-[NNN] Section 4 |

### Data Entities to Create/Modify
| Entity | Action | Schema Reference |
|--------|--------|-----------------|
| DATA-[N] | [Create/Modify/Use] | DESIGN-[NNN] Section 5 |

## Scope Boundaries

### DO (In Scope)
- [Explicit action that IS part of this task]
- [Explicit action that IS part of this task]
- [Explicit action that IS part of this task]

### DO NOT (Out of Scope)
- [Explicit action that is NOT part of this task]
- [Explicit action that is NOT part of this task]
- [Explicit action that is NOT part of this task]
- Do not refactor unrelated code
- Do not add features not specified
- Do not modify files outside the scope listed below

### Files in Scope
```
[path/to/file1.ext]
[path/to/file2.ext]
[path/to/directory/]
```

### Files Out of Scope
```
[path/to/protected/file.ext]
[Do not modify these]
```

## Acceptance Criteria

All criteria must pass for this DIP to be considered complete.

| ID | Criterion | Test |
|----|-----------|------|
| AC-[N] | Given [context], when [action], then [result] | [How to verify] |
| AC-[N] | Given [context], when [action], then [result] | [How to verify] |
| AC-[N] | Given [context], when [action], then [result] | [How to verify] |

### Verification Commands
```bash
# Run these to verify implementation
[command to run tests]
[command to verify behavior]
[command to check output]
```

## Safety Checklist

Before committing, verify:

- [ ] No secrets, keys, or credentials in code
- [ ] No `git add .` or `git add -A` used
- [ ] All new files explicitly added
- [ ] Conventional commit message prepared
- [ ] No unrelated changes included
- [ ] Tests pass (if applicable)

## Commit Instructions

When implementation is complete:

```bash
# Stage only files in scope
git add [specific files]

# Commit with conventional format
git commit -m "[type]([scope]): [description]

Implements [DIP-NNN]: [task title]
Satisfies: REQ-[N], REQ-[N]

Todoist: [task ID]"
```

**Commit type:** [feat|fix|refactor|test|docs]
**Scope:** [component or area affected]

## Completion Checklist

> **Agent Action:** Work through this checklist, marking each item in your TodoWrite as you go.

- [ ] All implementation steps completed (all step todos marked `completed`)
- [ ] All acceptance criteria verified (verification commands passed)
- [ ] Safety checklist passed (no secrets, explicit git adds)
- [ ] Code committed with proper message
- [ ] Todoist task marked complete: `mcp__todoist__complete-tasks`
- [ ] PLANNING.md updated with completion status
- [ ] TodoWrite cleared or marked all complete

## Notes

[Any additional context, warnings, or guidance for the implementing agent]

---

**End of DIP-[NNN]**

> **Final Agent Actions:**
> 1. Ensure all TodoWrite items are marked `completed`
> 2. Mark Todoist task complete: `mcp__todoist__complete-tasks({ ids: ["[TASK_ID]"] })`
> 3. Update PLANNING.md with:
>    - DIP completion status
>    - Any deviations or decisions made
>    - Next suggested action
