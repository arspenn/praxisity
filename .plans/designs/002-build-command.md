# Design: DESIGN-002 Build Command

## Metadata

| Field | Value |
|-------|-------|
| Design ID | DESIGN-002 |
| Title | Build Command Design |
| Status | Draft |
| Author | Andrew Robert Spenn |
| Created | 2026-03-21 |
| Last Updated | 2026-03-21 |

### Specification References

| Spec ID | Title | Requirements Addressed |
|---------|-------|------------------------|
| [SPEC-002](../specs/002-build-command.md) | Build Command | REQ-F1 through REQ-F9, REQ-N1, REQ-N2 |

### Related Documents

| Document | Relationship |
|----------|--------------|
| [Foundation Plan](../../praxisity-foundation-plan.md) | Depends on — Git Safety section |
| [DIP Template](../../.praxisity/templates/dip.template.md) | Depends on — defines format /build consumes |
| [DESIGN-001](001-claude-md-minimization.md) | Related to — CLAUDE.md minimization principles apply to command prompt design |

---

## 1. Overview

### 1.1 Design Summary

The `/build` command is a Claude Code command (`.claude/commands/build.md`) that orchestrates DIP execution through three phases: pre-flight (DIP selection, git state check, step parsing), execution (sequential step processing with per-step verification), and completion (acceptance criteria verification, git safety, commit, state updates). The command itself is a markdown prompt — all intelligence comes from Claude interpreting the instructions, not from executable code.

The command handles both software and non-software DIPs through a verification duality pattern: automatable checks (commands, file existence) are run directly, while subjective or descriptive checks are presented to the user for manual pass/fail confirmation.

### 1.2 Design Principles

- **Stop, don't guess** — When a step fails or is unclear, halt and ask rather than improvising
- **Evidence before assertions** — Never claim completion without running verification
- **Domain-agnostic by default** — No code-specific assumptions; verification can be manual confirmation
- **Instructions, not explanations** — The command file is imperative and concise; rationale lives in this design doc

### 1.3 Requirements Coverage

| Requirement | Design Section | Approach |
|-------------|----------------|----------|
| REQ-F1 | COMP-1 | List DIPs from `.plans/prompts/` or accept path argument |
| REQ-F2 | COMP-1 | Parse DIP markdown by section headers |
| REQ-F3 | COMP-2 | Sequential loop with verification after each step |
| REQ-F4 | COMP-2 | Halt on failure, surface step and reason, ask user |
| REQ-F5 | COMP-3 | Reject blanket adds, scan sensitive files, verify scope |
| REQ-F6 | COMP-3 | Conventional commit with DIP ID and REQ references |
| REQ-F7 | COMP-3 | Run each AC from DIP before declaring complete |
| REQ-F8 | COMP-3 | Write execution status to PLANNING.md |
| REQ-F9 | COMP-3 | Call Todoist MCP complete-tasks if available |
| REQ-N1 | COMP-2, DEC-4 | Verification duality — automatable or manual |
| REQ-N2 | COMP-1, COMP-2 | TodoWrite progress tracking, step status display |

---

## 2. Architecture

### 2.1 System Context

```
┌─────────────┐     ┌─────────────┐     ┌──────────────┐
│  Pre-Flight │────▶│  Execution  │────▶│  Completion  │
│             │     │   Loop      │     │              │
│ - DIP select│     │ - Step N    │     │ - AC verify  │
│ - Git check │     │ - Verify    │     │ - Git safety │
│ - Parse     │     │ - Progress  │     │ - Commit     │
│ - Resume?   │     │ - Halt?     │     │ - State      │
└─────────────┘     └─────────────┘     └──────────────┘
                         │
                         ▼ (on failure)
                    ┌──────────┐
                    │  HALT    │
                    │ Ask user │
                    └──────────┘
```

### 2.2 Architecture Pattern

**Pattern:** Sequential pipeline — three phases executed in order within a single markdown command.

**Rationale:** The command orchestrates a linear workflow (select → execute → complete). No concurrency, no branching architecture needed. The pipeline maps directly to how a human would manually follow a DIP.

**Trade-offs:**
- Pros: Simple to understand, easy to write as a prompt, matches DIP's sequential step structure
- Cons: No parallelism — but parallelism is explicitly out of scope (post-MVP)

### 2.3 Technology Choices

| Layer/Concern | Technology | Rationale |
|---------------|------------|-----------|
| Command format | Markdown (`.claude/commands/build.md`) | Framework standard — all Praxisity commands are markdown prompts |
| Task tracking | TodoWrite | Claude Code native, per-session progress tracking |
| Git operations | Git CLI via Claude | Direct shell commands with safety rules |
| Todoist integration | Todoist MCP | Optional — already available in framework |

---

## 3. Components

### COMP-1: Pre-Flight

**Purpose:** Prepare for DIP execution — select DIP, check preconditions, parse steps.

**Satisfies:** REQ-F1, REQ-F2, REQ-N2

**Responsibilities:**
- Read PLANNING.md for session context
- Check for previous halted `/build` execution — if found, present resume context and ask user to confirm or override
- List available DIPs from `.plans/prompts/` or accept path argument
- Check git status — warn if dirty, require user approval to proceed
- Parse DIP to extract: objective, implementation steps, verification checks, acceptance criteria, scope boundaries, commit instructions
- Display objective and step summary to user
- Create TodoWrite entries from parsed steps

**Dependencies:**
- `.plans/prompts/` directory with DIP files
- Git CLI
- PLANNING.md

---

### COMP-2: Execution Loop

**Purpose:** Execute DIP steps sequentially with verification and progress tracking.

**Satisfies:** REQ-F3, REQ-F4, REQ-N1, REQ-N2

**Responsibilities:**
- For each step: mark in-progress, execute, run verification
- If verification is automatable (command, file check): run it and check result
- If verification is not automatable: present criterion to user, ask for manual pass/fail confirmation
- On verification pass: mark step complete, show progress, continue
- On verification fail: halt execution, report which step failed and why, ask user how to proceed
- On ambiguity: halt and ask rather than interpreting

**Dependencies:**
- COMP-1 (parsed step list)
- TodoWrite (progress tracking)

---

### COMP-3: Completion

**Purpose:** Verify acceptance criteria, perform git safety, commit, and update state.

**Satisfies:** REQ-F5, REQ-F6, REQ-F7, REQ-F8, REQ-F9

**Responsibilities:**
- Run each acceptance criterion from the DIP — same automatable/manual logic as step verification
- Enforce git safety: reject blanket adds, scan for sensitive files, verify files are within DIP scope
- Generate conventional commit message with DIP ID and REQ IDs
- Show diff to user before committing
- Update PLANNING.md with completion status (or halt status if stopped)
- Optionally mark Todoist task complete via MCP

**Dependencies:**
- COMP-2 (all steps completed)
- Git CLI
- PLANNING.md
- Todoist MCP (optional)

---

## 4. Interfaces

### INT-1: DIP File Interface

**Connects:** COMP-1 ↔ DIP files (`.plans/prompts/`)

**Type:** File

**Direction:** Read

**Contract:**
- Command reads DIP markdown and parses by section headers
- Expected sections: Context table, Implementation Steps (`### Step N:`), Acceptance Criteria, Scope Boundaries, Commit Instructions
- Steps must have `**Verify:**` sub-blocks to enable per-step verification

---

### INT-2: Git CLI Interface

**Connects:** COMP-1, COMP-3 ↔ Git

**Type:** CLI

**Direction:** Bidirectional

**Contract:**
- `git status` — check working tree state (COMP-1 pre-flight)
- `git diff` — show changes before commit (COMP-3)
- `git add [specific files]` — stage only scoped files (never `-A` or `.`)
- `git commit -m "type(scope): description\n\nImplements DIP-NNN\nSatisfies: REQ-N, REQ-N"` — conventional format with traceability

---

### INT-3: PLANNING.md Interface

**Connects:** COMP-1, COMP-3 ↔ PLANNING.md

**Type:** File

**Direction:** Bidirectional

**Contract:**
- Read: session context, active artifacts, previous halt state
- Write: execution status, halt point and reason, completion record, next steps

---

### INT-4: Todoist MCP Interface

**Connects:** COMP-3 ↔ Todoist

**Type:** MCP

**Direction:** Write

**Contract:**
- `mcp__todoist__complete-tasks({ ids: ["TASK_ID"] })` — mark task done
- Task ID sourced from DIP context table
- Optional — command checks MCP availability before attempting

---

## 5. Data Model

### 5.1 Entity Overview

```
┌──────────────┐
│  DIP (DATA-1)│
│              │
│  Objective   │
│  Spec ref    │──────────▶ .plans/specs/
│  Design ref  │──────────▶ .plans/designs/
│  Scope       │
│  Commit info │
│              │
│  ┌─────────┐ │
│  │Steps    │ │     ┌───────────────────┐
│  │(DATA-2) │─┼────▶│ Execution State   │
│  │ 1..N    │ │     │ (DATA-3)          │
│  └─────────┘ │     │                   │
│              │     │ Step statuses     │
│  ┌─────────┐ │     │ AC results        │
│  │ACs      │─┼────▶│ Completion status  │
│  │ 1..N    │ │     └───────────────────┘
│  └─────────┘ │              │
└──────────────┘              ▼
                       PLANNING.md
```

### DATA-1: DIP Document

**Purpose:** The input artifact that drives execution — contains everything `/build` needs.

**Used by:** COMP-1, COMP-2, COMP-3

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| DIP ID | String (DIP-NNN) | Yes | Unique identifier |
| Objective | Text | Yes | What this DIP accomplishes |
| Spec Reference | Path (SPEC-NNN) | Yes | Linked specification |
| Design Reference | Path (DESIGN-NNN) | Yes | Linked design |
| Todoist Task ID | String | No | External task reference |
| Implementation Steps | Ordered list | Yes | Sequential steps with verification |
| Acceptance Criteria | Table (AC-N) | Yes | Given/when/then with test method |
| Scope Boundaries | Lists (DO/DO NOT) | Yes | Files and actions in/out of scope |
| Commit Instructions | Template | Yes | Type, scope, files to stage |

**Constraints:**
- Steps must be ordered — execution depends on sequence
- Each step must include a verification method (automatable or manual)

---

### DATA-2: Step

**Purpose:** A single unit of work within a DIP — the atomic element of execution.

**Used by:** COMP-2

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Step Number | Integer | Yes | Position in sequence |
| Title | Text | Yes | Brief action description |
| Instructions | Text | Yes | What to do |
| Input | Text | No | What you're working with |
| Output | Text | No | What should exist after |
| Verification | Text | Yes | How to confirm success |
| Verification Type | Enum | Inferred | Automatable (command/file check) or Manual (user confirmation) |
| Status | Enum | Yes | Pending → In Progress → Complete → Failed |

**Constraints:**
- Status transitions are one-directional during normal flow (Pending → In Progress → Complete)
- Failed status triggers halt — cannot proceed to next step

---

### DATA-3: Execution State

**Purpose:** Tracks progress through a `/build` run — exists in TodoWrite during session, persisted to PLANNING.md on completion or halt.

**Used by:** COMP-1, COMP-2, COMP-3

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| DIP ID | String | Yes | Which DIP is being executed |
| Current Step | Integer | Yes | Which step is active |
| Step Statuses | Map (step → status) | Yes | Progress through all steps |
| Started At | Timestamp | Yes | When execution began |
| Halted At Step | Integer | No | Where execution stopped (if halted) |
| Halt Reason | Text | No | Why execution stopped |
| AC Results | Map (AC-N → pass/fail) | No | Acceptance criteria verification results |
| Completion Status | Enum | Yes | In Progress → Completed → Halted |

**Constraints:**
- Only one DIP can be actively executing per session
- Halted state is persisted to PLANNING.md so resume can detect it

---

## 6. Design Decisions

### DEC-1: Command as Markdown Prompt, Not Executable Script

**Context:** `/build` could be implemented as a shell script, Python tool, or a markdown prompt that Claude interprets.

**Decision:** Implement as a markdown command file (`.claude/commands/build.md`), consistent with all other Praxisity commands.

**Rationale:** The framework's commands are instructions for Claude, not standalone tools. Claude reads the DIP, understands the steps, executes them, and makes judgment calls (like whether a verification is automatable). A script can't do that. Consistency with the rest of the framework matters more than hypothetical performance gains.

**Alternatives Considered:**
- Shell script wrapper: Would require parsing DIP markdown programmatically, couldn't handle ambiguity or manual verification
- Hybrid (script + prompt): Added complexity with no clear benefit at MVP

**Consequences:**
- Command intelligence depends entirely on Claude's interpretation of the prompt
- No programmatic guarantees — the prompt must be clear enough to produce consistent behavior

---

### DEC-2: Halt-and-Ask Over Retry-and-Guess

**Context:** When a step verification fails, the command could retry, attempt to fix the issue, or stop and ask the user.

**Decision:** Always halt and surface the failure. Never retry or attempt automatic recovery.

**Rationale:** Guessing causes cascading errors that are harder to fix than pausing. The user has context the command doesn't — letting them decide how to proceed produces better outcomes. Particularly important for non-software DIPs where "fixing" may not be meaningful.

**Alternatives Considered:**
- Retry with backoff: Inappropriate — if a step fails, retrying the same action rarely helps
- Automatic fix attempt: Would require domain-specific knowledge the command shouldn't assume (REQ-N1)

**Consequences:**
- Execution is slower (requires human in the loop on failure)
- But correctness is higher — no silent failures or wrong fixes

---

### DEC-3: Resume via PLANNING.md Context with User Confirmation

**Context:** When a user returns after a halt, the command needs to know where to pick up.

**Decision:** COMP-1 reads PLANNING.md, detects if a previous `/build` was halted (DIP ID, step number, halt reason are recorded there by COMP-3). The command presents this context and asks the user to confirm the resume point or provide a different one. User arguments can override if the situation has changed.

**Rationale:** PLANNING.md already serves as session state. The halt information written by COMP-3 gives COMP-1 enough to suggest a resume point. The user confirmation step keeps the human in the loop without requiring them to remember or look up the step number themselves.

**Alternatives Considered:**
- Separate checkpoint file: Redundant — PLANNING.md already carries this information
- Fully automatic resume with no confirmation: Risky — user may have manually completed steps or changed approach between sessions

**Consequences:**
- Resume is mostly automatic (command suggests, user confirms)
- No new state mechanism needed — leverages existing PLANNING.md pattern
- User can still override if they've done work outside the command

---

### DEC-4: Verification Duality — Automatable vs Manual

**Context:** Some DIP steps have verification that can be run as a command (`npm test`, `ls file.md`). Others require human judgment ("does this document section read clearly?").

**Decision:** The command infers verification type from the DIP. If the verification looks like a command or file check, run it automatically. If it's subjective or descriptive, present it to the user and ask for pass/fail confirmation.

**Rationale:** This is what makes `/build` work for non-software DIPs (REQ-N1). A research DIP's verification might be "confirm the literature review covers all three theoretical frameworks" — that can't be automated, but it can be presented as a checklist item.

**Alternatives Considered:**
- All manual: Too tedious for software DIPs with runnable tests
- All automatic: Impossible for non-software DIPs
- Explicit markup in DIP template: Would require DIP template changes and add author burden

**Consequences:**
- Inference may occasionally miscategorize — but the user is watching and can correct

---

## 7. Implementation Considerations

### 7.1 Implementation Order

| Order | Component | Dependencies | Notes |
|-------|-----------|--------------|-------|
| 1 | COMP-1 (Pre-Flight) | None | DIP selection and parsing must work before anything else |
| 2 | COMP-2 (Execution Loop) | COMP-1 | Core logic — step execution with verification duality |
| 3 | COMP-3 (Completion) | COMP-2 | Git safety, commit, state updates — ties everything together |

Since this is a single markdown command file, all three components exist in one file. They should be written and tested in this sequence.

### 7.2 Risk Areas

| Risk | Impact | Mitigation |
|------|--------|------------|
| DIP format inconsistency — steps may not follow the template exactly if `/define` output varies | COMP-1 fails to parse steps correctly, execution breaks | COMP-1 should be tolerant of minor format variations (step numbering style, header level) while requiring the essential elements (step title, verification) |
| Verification type inference — command misjudges whether verification is automatable or manual | Attempts to run descriptive text as a command, or asks user to confirm something trivially automatable | Bias toward manual confirmation when uncertain — safer to ask than to run a bad command |
| Git safety too restrictive — blocks legitimate commits | User frustration, workarounds that bypass safety | Safety checks warn and require approval rather than hard-blocking; user always has final say |
| Prompt length — command file becomes too long for Claude to follow reliably | Claude loses track of later sections, inconsistent behavior | Keep the command to instructions only — no rationale, no explanations. Reasoning lives in this design doc (DEC-1, DQ-1) |

### 7.3 Testing Strategy

| Level | Approach | Covers |
|-------|----------|--------|
| Manual walkthrough | Execute `/build` against DIP-001 (already completed manually) as a dry run | COMP-1, COMP-2, COMP-3 end-to-end |
| Software DIP | Create a small test DIP with automatable verification steps, run `/build` | COMP-2 automatic verification path |
| Non-software DIP | Create a document-focused test DIP with manual verification steps | COMP-2 manual verification path, REQ-N1 |
| Halt and resume | Deliberately fail a step mid-execution, restart with resume | COMP-2 halt behavior, DEC-3 resume flow |
| Git safety | Attempt to commit with dirty state, sensitive files, blanket adds | COMP-3 safety checks |

---

## 8. Out of Scope

**From Specification (inherited):**
- Git worktree creation or branch management
- Subagent dispatch for parallel task execution
- TDD enforcement as a separate discipline
- Automatic code review between steps
- Rollback/undo of partially completed builds

**Design-Specific Exclusions:**
- DIP template format changes — `/build` consumes the existing DIP format as-is
- Multi-DIP execution in a single `/build` invocation
- Step reordering or skipping (beyond resume)

---

## 9. Open Questions

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| DQ-1 | Should the command prompt length be a concern? | Resolved | Yes — keep the command file to instructions only. No rationale, no explanations of why. Design decisions and reasoning live in this design doc, not in the command. The command should be imperative and concise. This aligns with the CLAUDE.md minimization work from SPEC-001. |

---

## 10. Appendices

### A. Glossary

| Term | Definition |
|------|------------|
| DIP | Detailed Implementation Prompt — task-specific prompt with full context for implementation |
| Verification Duality | Pattern where verification is either run automatically (command/file check) or presented to user for manual confirmation |
| Halt-and-Ask | Behavior where execution stops on failure and asks user rather than retrying or guessing |

### B. References

- [SPEC-002: Build Command](../specs/002-build-command.md)
- [Foundation Plan](../../praxisity-foundation-plan.md) — Git Safety section
- [DIP Template](../../.praxisity/templates/dip.template.md)
- Superpowers plugin `executing-plans` — conceptual influence on sequential execution pattern
- Superpowers plugin `verification-before-completion` — conceptual influence on evidence-before-assertions principle
- Superpowers plugin `systematic-debugging` — conceptual influence on halt-and-ask principle

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-03-21 | Andrew Robert Spenn | Initial draft |
