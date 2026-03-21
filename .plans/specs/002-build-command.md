# Specification: SPEC-002 Build Command

## Metadata

| Field | Value |
|-------|-------|
| Spec ID | SPEC-002 |
| Title | Build Command |
| Status | Draft |
| Author | Andrew Robert Spenn |
| Created | 2026-03-21 |
| Last Updated | 2026-03-21 |
| Charter Reference | [CHARTER.md](../../CHARTER.md) — Principles 1, 2, 5 |

### Related Documents

| Document | Relationship |
|----------|--------------|
| [SPEC-001](001-claude-md-minimization.md) | Related to — CLAUDE.md references git safety |
| [Foundation Plan](../../praxisity-foundation-plan.md) | Depends on — Git Safety section defines commit controls |
| [DIP Template](../../.praxisity/templates/dip.template.md) | Depends on — defines the format /build consumes |

---

## 1. Problem Statement

The Praxisity framework can generate DIPs (Detailed Implementation Prompts) but has no command to execute them. Users must manually follow DIP instructions, manage git safety checks, track step completion, and verify acceptance criteria. This breaks the design-first workflow at its most critical point — the transition from planning to execution — and eliminates the consistency benefits DIPs were designed to provide.

---

## 2. Goals and Objectives

### 2.1 Primary Goal

Provide guided, safe execution of DIPs with step-by-step verification and git safety controls.

### 2.2 Objectives

| ID | Objective | Success Metric |
|----|-----------|----------------|
| OBJ-1 | Execute any DIP through its implementation steps with verification | All DIP steps completed with verification checks passing |
| OBJ-2 | Prevent unsafe git operations during implementation | No accidental commits of secrets, blanket adds, or unscoped files |
| OBJ-3 | Stop and surface blockers rather than guessing | Execution halts with clear message when a step fails or is ambiguous |

---

## 3. Requirements

### 3.1 Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-F1 | The command shall accept a DIP file path or present available DIPs from `.plans/prompts/` for selection | MUST | Entry point to execution |
| REQ-F2 | The command shall read and parse the selected DIP's implementation steps | MUST | Steps drive the execution flow |
| REQ-F3 | The command shall execute steps sequentially, verifying each before proceeding | MUST | Prevents cascading errors from unverified steps |
| REQ-F4 | The command shall halt execution and surface a clear message when a step fails or is ambiguous | MUST | Stop-when-blocked principle — guessing causes more damage than pausing |
| REQ-F5 | The command shall enforce git safety checks before any commit (no blanket adds, sensitive file scan, scoped file verification) | MUST | Charter principle: safety-first |
| REQ-F6 | The command shall use conventional commit format with DIP/REQ traceability in commit messages | MUST | Links implementation back to spec |
| REQ-F7 | The command shall verify acceptance criteria from the DIP before marking execution complete | MUST | Verification-before-completion — evidence before assertions |
| REQ-F8 | The command shall update PLANNING.md with execution status on completion | SHOULD | Session state continuity |
| REQ-F9 | The command shall optionally mark the associated Todoist task complete via MCP | SHOULD | External accountability loop |

### 3.2 Non-Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-N1 | The command shall work for non-software DIPs (documents, research tasks) without assuming code-specific tooling | MUST | Multi-disciplinary framework |
| REQ-N2 | The command shall provide clear progress indication for each step | SHOULD | ADHD-informed: visible progress reduces abandonment |

---

## 4. User Stories / Use Cases

### UC-1: Execute a Software DIP

**Actor:** Developer with a generated DIP

**Preconditions:**
- DIP exists in `.plans/prompts/`
- Spec and design documents referenced by DIP exist
- Git repository is initialized

**Flow:**
1. User invokes `/build`
2. Command presents available DIPs for selection
3. User selects a DIP
4. Command reads DIP, displays objective and step summary
5. Command executes steps sequentially, showing progress
6. After each step, command runs the step's verification check
7. On final step, command runs acceptance criteria verification
8. Command performs git safety checks and commits with traceability
9. Command updates PLANNING.md and optionally completes Todoist task

**Postconditions:**
- All DIP steps completed and verified
- Code/documents committed with conventional format
- PLANNING.md reflects completion

**Alternative Flows:**
- Step verification fails: command halts, reports which step failed and why, asks user how to proceed
- Git working tree is dirty: command warns and requires user approval before proceeding

---

### UC-2: Execute a Non-Software DIP

**Actor:** Researcher or practitioner with a document-focused DIP

**Preconditions:**
- DIP exists with steps that produce documents rather than code
- Referenced spec and design exist

**Flow:**
1. User invokes `/build`
2. Selects DIP
3. Command executes document creation/modification steps
4. Verification checks confirm document sections exist and meet criteria
5. Command commits deliverables with traceability

**Postconditions:**
- Documents created per DIP specification
- Committed to version control

**Alternative Flows:**
- Verification check is not automatable: command presents the criterion and asks user to manually confirm pass/fail

---

### UC-3: Resume After a Blocker

**Actor:** User returning after `/build` halted on a failed step

**Preconditions:**
- A previous `/build` execution was halted
- User has resolved the blocking issue

**Flow:**
1. User invokes `/build` with arguments indicating resume point (step number, last artifact produced, or rough progress estimate)
2. Command loads the DIP and skips to the indicated step
3. Execution continues from that point

**Postconditions:**
- Remaining steps completed and verified

---

## 5. Acceptance Criteria

| ID | Criterion | Validates |
|----|-----------|-----------|
| AC-1 | Given a `.plans/prompts/` directory with DIPs, when `/build` is invoked, then available DIPs are listed for selection | REQ-F1 |
| AC-2 | Given a selected DIP, when execution begins, then steps are executed sequentially with verification after each | REQ-F2, REQ-F3 |
| AC-3 | Given a step whose verification fails, when the failure is detected, then execution halts with a clear message identifying the step and failure reason | REQ-F4 |
| AC-4 | Given completed implementation, when committing, then no `git add .` or `git add -A` is used and sensitive files are flagged | REQ-F5 |
| AC-5 | Given a successful commit, when the message is generated, then it follows conventional format and includes DIP ID and satisfied REQ IDs | REQ-F6 |
| AC-6 | Given all steps completed, when acceptance criteria are checked, then each criterion from the DIP is verified before declaring completion | REQ-F7 |
| AC-7 | Given a DIP with non-automatable verification, when that step is reached, then the user is prompted to manually confirm pass/fail | REQ-N1 |

---

## 6. Constraints

### 6.1 Inherited from Charter

- Timeline: 4 weeks to MVP
- Technical: Claude Code compatibility, Todoist MCP availability
- Scope: Strict MVP discipline to avoid feature creep

### 6.2 Spec-Specific Constraints

- Must work without any plugins installed (no superpowers or other plugin dependency)
- Git must be initialized in the project
- Resume functionality relies on user-provided arguments, not automatic state tracking

---

## 7. Dependencies

### 7.1 Depends On

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| `/define` command | Spec | Available | Produces the DIPs that `/build` consumes |
| DIP template | Resource | Available | `.praxisity/templates/dip.template.md` |
| Git | External | Available | Required for safety checks and commits |
| Todoist MCP | External | Available | Optional — for task completion |

### 7.2 Enables

| Dependent | Relationship |
|-----------|--------------|
| End-to-end workflow test | `/build` completes the spec-design-breakdown-define-build chain |
| `/deliver` command | `/build` produces artifacts that `/deliver` converts to PDF |

---

## 8. Out of Scope

The following are explicitly NOT part of this specification:

- Git worktree creation or branch management (post-MVP)
- Subagent dispatch for parallel task execution (post-MVP)
- TDD enforcement as a separate discipline (post-MVP)
- Automatic code review between steps (post-MVP)
- Rollback/undo of partially completed builds (post-MVP)
- Automatic resume detection without user arguments (post-MVP)

---

## 9. Open Questions

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| Q-1 | How should `/build` detect previously completed steps for resume? | Resolved | User provides resume point via command arguments: step number, last artifact path, or rough progress estimate |
| Q-2 | Should `/build` require a clean git state before starting? | Resolved | Warn if dirty, require user approval to proceed |

---

## 10. References

- [CHARTER.md](../../CHARTER.md)
- [Foundation Plan](../../praxisity-foundation-plan.md) — Git Safety section
- [DIP Template](../../.praxisity/templates/dip.template.md)
- Superpowers plugin `executing-plans` and `verification-before-completion` skills — conceptual influence (not a dependency)
- Superpowers plugin `subagent-driven-development` — future enhancement reference

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-03-21 | Andrew Robert Spenn | Initial draft |

