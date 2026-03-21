# DIP-002: Implement /build Command

> **For AI Agent:** This is a Detailed Implementation Prompt. Follow these instructions precisely.
> Read all referenced documents before beginning implementation.
>
> **TodoWrite Integration:** Use Claude's TodoWrite tool to track progress through this DIP.
> Create todos from the Implementation Steps below and mark them complete as you progress.

## Context

| Field | Value |
|-------|-------|
| DIP ID | DIP-002 |
| Task | Implement the /build command for DIP execution |
| Spec | [SPEC-002](../../.plans/specs/002-build-command.md) |
| Design | [DESIGN-002](../../.plans/designs/002-build-command.md) |
| Todoist Task | N/A |
| Created | 2026-03-21 |

## Objective

Create the `/build` command (`.claude/commands/build.md`) that executes DIPs through sequential step verification, git safety checks, and state management.

## Required Reading

Before implementation, read and understand these sections:

### From Specification (SPEC-002)
- [ ] Section 3.1: REQ-F1 - DIP selection/path input
- [ ] Section 3.1: REQ-F2 - Parse DIP implementation steps
- [ ] Section 3.1: REQ-F3 - Sequential execution with verification
- [ ] Section 3.1: REQ-F4 - Halt on failure with clear message
- [ ] Section 3.1: REQ-F5 - Git safety checks
- [ ] Section 3.1: REQ-F6 - Conventional commit with traceability
- [ ] Section 3.1: REQ-F7 - Acceptance criteria verification
- [ ] Section 3.1: REQ-F8 - PLANNING.md update
- [ ] Section 3.1: REQ-F9 - Todoist task completion
- [ ] Section 3.2: REQ-N1 - Works for non-software DIPs
- [ ] Section 3.2: REQ-N2 - Clear progress indication
- [ ] Section 4: UC-1 - Execute a Software DIP
- [ ] Section 4: UC-2 - Execute a Non-Software DIP
- [ ] Section 4: UC-3 - Resume After a Blocker
- [ ] Section 5: AC-1 through AC-7

### From Design (DESIGN-002)
- [ ] Section 3: COMP-1 - Pre-Flight
- [ ] Section 3: COMP-2 - Execution Loop
- [ ] Section 3: COMP-3 - Completion
- [ ] Section 4: INT-1 - DIP File Interface
- [ ] Section 4: INT-2 - Git CLI Interface
- [ ] Section 4: INT-3 - PLANNING.md Interface
- [ ] Section 4: INT-4 - Todoist MCP Interface
- [ ] Section 5: DATA-1 - DIP Document
- [ ] Section 5: DATA-2 - Step
- [ ] Section 5: DATA-3 - Execution State
- [ ] Section 6: DEC-1 - Command as Markdown Prompt
- [ ] Section 6: DEC-2 - Halt-and-Ask Over Retry-and-Guess
- [ ] Section 6: DEC-3 - Resume via PLANNING.md Context with User Confirmation
- [ ] Section 6: DEC-4 - Verification Duality

### From Charter
- [ ] Principle 1: Design before implementation
- [ ] Principle 5: Safety-first (git safety controls)
- [ ] Principle 6: Dual-use design (optimized for human and AI consumption)

## Implementation Instructions

> **Agent Action:** Before starting, use TodoWrite to create todos from these steps:
> ```
> TodoWrite([
>   { content: "Read required spec/design sections", status: "pending", activeForm: "Reading documentation" },
>   { content: "Step 1: Write COMP-1 (Pre-Flight)", status: "pending", activeForm: "Writing pre-flight section" },
>   { content: "Step 2: Write COMP-2 (Execution Loop)", status: "pending", activeForm: "Writing execution loop section" },
>   { content: "Step 3: Write COMP-3 (Completion)", status: "pending", activeForm: "Writing completion section" },
>   { content: "Step 4: Review and test", status: "pending", activeForm: "Reviewing and testing command" },
>   { content: "Verify acceptance criteria", status: "pending", activeForm: "Verifying acceptance criteria" },
>   { content: "Complete safety checklist and commit", status: "pending", activeForm: "Completing safety checklist" }
> ])
> ```
> Mark each todo in_progress when starting, completed when done.

### Step 1: Write COMP-1 (Pre-Flight) section of build.md

Write the pre-flight section of `.claude/commands/build.md` covering:

- Read PLANNING.md for session context and previous halt state
- If halted build detected, present resume context (DIP ID, step number, halt reason), ask user to confirm resume point or override
- List DIPs from `.plans/prompts/` or accept path argument
- Check git status — warn if dirty, require user approval to proceed
- Parse selected DIP: extract objective, implementation steps, verification checks, acceptance criteria, scope boundaries, commit instructions
- Display objective and step summary to user
- Create TodoWrite entries from parsed steps

**Input:** DESIGN-002 COMP-1 specification, existing command patterns from other `.claude/commands/` files
**Output:** Pre-flight section of `build.md`
**Verify:** Section covers all COMP-1 responsibilities listed in DESIGN-002

**TodoWrite:** Mark "Step 1" as `in_progress` before starting, `completed` when done.

### Step 2: Write COMP-2 (Execution Loop) section of build.md

Write the execution loop section covering:

- For each step: mark in-progress in TodoWrite, execute the step, run verification
- Verification duality (DEC-4): if verification looks like a command or file check, run it automatically; if subjective or descriptive, present criterion to user and ask for manual pass/fail confirmation
- On verification pass: mark step complete, show progress, continue to next step
- On verification fail: halt execution, report which step failed and why, ask user how to proceed (DEC-2)
- On ambiguity: halt and ask rather than interpreting

**Input:** DESIGN-002 COMP-2 specification, DEC-2 (halt-and-ask), DEC-4 (verification duality)
**Output:** Execution loop section of `build.md`
**Verify:** Section handles both automatable and manual verification; halts on failure

**TodoWrite:** Mark "Step 2" as `in_progress` before starting, `completed` when done.

### Step 3: Write COMP-3 (Completion) section of build.md

Write the completion section covering:

- Run each acceptance criterion from the DIP (same automatable/manual duality as step verification)
- Git safety: reject `git add .` and `git add -A`, scan for sensitive files (.env, credentials, keys), verify staged files are within DIP's scope boundaries
- Show diff to user before committing
- Generate conventional commit message: `type(scope): description` with DIP ID and REQ IDs in body
- Update PLANNING.md with completion status (or halt status if stopped during AC verification)
- Optionally mark Todoist task complete via MCP if task ID exists in DIP context

**Input:** DESIGN-002 COMP-3 specification, INT-2 (Git CLI), INT-3 (PLANNING.md), INT-4 (Todoist MCP)
**Output:** Completion section of `build.md`
**Verify:** Section covers git safety, commit format, PLANNING.md update, and optional Todoist completion

**TodoWrite:** Mark "Step 3" as `in_progress` before starting, `completed` when done.

### Step 4: Review and test

- Read the complete `build.md` file for consistency and clarity
- Verify it follows DEC-1: instructions only, no rationale or explanations — keep it concise per DQ-1 resolution
- Check that the command follows the same structural patterns as existing commands (frontmatter, constraints, pre-flight, flow, behavior notes)
- Review against all 11 requirements for coverage
- Dry-run mentally against DIP-001 to validate the flow makes sense

**Input:** Complete `build.md`, existing commands for pattern reference
**Output:** Reviewed and potentially revised `build.md`
**Verify:** Command is concise, imperative, covers all requirements, follows existing patterns

**TodoWrite:** Mark "Step 4" as `in_progress` before starting, `completed` when done.

## Technical Requirements

### Must Implement
- [ ] DIP selection from `.plans/prompts/` or path argument (REQ-F1)
- [ ] DIP parsing to extract steps, verification, acceptance criteria (REQ-F2)
- [ ] Sequential step execution with per-step verification (REQ-F3)
- [ ] Halt-and-ask on failure or ambiguity (REQ-F4)
- [ ] Git safety checks: no blanket adds, sensitive file scan, scope verification (REQ-F5)
- [ ] Conventional commit with DIP/REQ traceability (REQ-F6)
- [ ] Acceptance criteria verification before completion (REQ-F7)
- [ ] PLANNING.md state update (REQ-F8)
- [ ] Optional Todoist task completion (REQ-F9)
- [ ] Verification duality for non-software DIPs (REQ-N1)
- [ ] Progress indication via TodoWrite (REQ-N2)

### Must Satisfy
| Requirement | How to Satisfy |
|-------------|----------------|
| REQ-F1 | List `.plans/prompts/*.md` files or accept path argument |
| REQ-F3 | Loop through steps sequentially, verify each before proceeding |
| REQ-F4 | On failure: stop, report step/reason, ask user |
| REQ-F5 | Before commit: reject blanket adds, scan for secrets, check scope |
| REQ-F6 | Commit format: `type(scope): desc` + `Implements DIP-NNN` + `Satisfies: REQ-N` |
| REQ-F7 | After all steps: run each AC from DIP before declaring complete |
| REQ-N1 | Infer verification type — run commands automatically, present subjective checks to user |

### Interfaces to Implement/Use
| Interface | Role | Contract Reference |
|-----------|------|-------------------|
| INT-1 | Consume | Read DIP files, parse by section headers |
| INT-2 | Use | Git status, diff, add (specific files), commit |
| INT-3 | Use | Read/write PLANNING.md for state |
| INT-4 | Use | Optional Todoist complete-tasks call |

### Data Entities to Create/Modify
| Entity | Action | Schema Reference |
|--------|--------|-----------------|
| DATA-3 (Execution State) | Create/Update | Tracked via TodoWrite during session, persisted to PLANNING.md |

## Scope Boundaries

### DO (In Scope)
- Write the complete `/build` command as a single markdown file
- Include frontmatter (description, tags) consistent with other commands
- Cover all three components (pre-flight, execution loop, completion)
- Follow existing command patterns for structure
- Keep instructions concise and imperative (DEC-1, DQ-1)

### DO NOT (Out of Scope)
- Do not modify the DIP template
- Do not modify other commands
- Do not modify CLAUDE.md
- Do not implement git worktree support
- Do not implement subagent dispatch
- Do not implement TDD enforcement
- Do not implement automatic code review
- Do not add rollback/undo capability
- Do not add explanations or rationale in the command — that belongs in the design doc

### Files in Scope
```
.claude/commands/build.md
```

### Files Out of Scope
```
.praxisity/templates/dip.template.md
.claude/commands/charter.md
.claude/commands/spec.md
.claude/commands/architect.md
.claude/commands/breakdown.md
.claude/commands/define.md
.claude/commands/new-project.md
CLAUDE.md
```

## Acceptance Criteria

All criteria must pass for this DIP to be considered complete.

| ID | Criterion | Test |
|----|-----------|------|
| AC-1 | Given DIPs in `.plans/prompts/`, when `/build` is invoked, then available DIPs are listed for selection | Invoke `/build`, verify DIP list appears |
| AC-2 | Given a selected DIP, when execution begins, then steps are executed sequentially with verification after each | Run `/build` on a DIP, observe step-by-step execution |
| AC-3 | Given a step whose verification fails, when the failure is detected, then execution halts with a clear message identifying the step and failure reason | Deliberately fail a step, verify halt behavior |
| AC-4 | Given completed implementation, when committing, then no `git add .` or `git add -A` is used and sensitive files are flagged | Review commit commands in the output |
| AC-5 | Given a successful commit, when the message is generated, then it follows conventional format and includes DIP ID and satisfied REQ IDs | Check commit message format |
| AC-6 | Given all steps completed, when acceptance criteria are checked, then each criterion from the DIP is verified before declaring completion | Observe AC verification at end of run |
| AC-7 | Given a DIP with non-automatable verification, when that step is reached, then the user is prompted to manually confirm pass/fail | Test with a subjective verification step |

### Verification Commands
```bash
# Verify command file exists
ls -la .claude/commands/build.md

# Verify frontmatter is present
head -5 .claude/commands/build.md

# Verify file follows command pattern (has description in frontmatter)
grep -c "description:" .claude/commands/build.md
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
git add .claude/commands/build.md

# Commit with conventional format
git commit -m "feat(commands): add /build command for DIP execution

Implements DIP-002: /build command
Satisfies: REQ-F1, REQ-F2, REQ-F3, REQ-F4, REQ-F5, REQ-F6, REQ-F7, REQ-F8, REQ-F9, REQ-N1, REQ-N2"
```

**Commit type:** feat
**Scope:** commands

## Completion Checklist

> **Agent Action:** Work through this checklist, marking each item in your TodoWrite as you go.

- [ ] All implementation steps completed (all step todos marked `completed`)
- [ ] All acceptance criteria verified (verification commands passed)
- [ ] Safety checklist passed (no secrets, explicit git adds)
- [ ] Code committed with proper message
- [ ] PLANNING.md updated with completion status
- [ ] TodoWrite cleared or marked all complete

## Notes

- Reference existing commands (e.g., `define.md`, `spec.md`) for structural patterns and frontmatter format
- The command should be concise — design rationale lives in DESIGN-002, not in the command file
- This is the first command that will be tested against itself (self-hosting): once `/build` exists, future DIPs can be executed via `/build`

---

**End of DIP-002**

> **Final Agent Actions:**
> 1. Ensure all TodoWrite items are marked `completed`
> 2. Update PLANNING.md with:
>    - DIP completion status
>    - Any deviations or decisions made
>    - Next suggested action