# Specification: SPEC-004 Command Behavioral Fixes and Pattern Standards

## Metadata

| Field | Value |
|-------|-------|
| Spec ID | SPEC-004 |
| Title | Command Behavioral Fixes and Pattern Standards |
| Status | Draft |
| Author | Andrew Robert Spenn |
| Created | 2026-03-22 |
| Last Updated | 2026-03-22 |
| Charter Reference | [CHARTER.md](../../CHARTER.md) — Principles: Dual-use design, Minimal cognitive overhead |

### Related Documents

| Document | Relationship |
|----------|--------------|
| [`.plans/references/new-project-bug-report.md`](../references/new-project-bug-report.md) | Depends on — primary evidence base |

---

## 1. Problem Statement

Praxisity's workflow commands (`/spec`, `/charter`, `/architect`, `/new-project`, `/breakdown`, `/define`, `/build`, `/deliver`) were tested end-to-end for the first time at v0.5.0. The run revealed 46 bugs and 3 framework issues across all 7 tested commands, documented in `.plans/references/new-project-bug-report.md`. The failures share identifiable root causes: templates were read then rewritten from memory instead of copied verbatim (BUG-009, Critical), gathering steps were batched instead of one-at-a-time, pre-flight steps were reordered, PLANNING.md updates were consistently deferred, and required success message elements were dropped. These patterns repeat across commands — fixing them per-command in isolation misses the opportunity to establish consistent behavioral standards that all current and future commands follow. This spec defines those standards and the command-level fixes that apply them.

---

## 2. Goals and Objectives

### 2.1 Primary Goal

Extract the recurring behavioral patterns from the full bug report into codified command standards, apply them as fixes to the highest-impact and most cross-cutting bugs, and leave a clear tracking record for what is fixed vs. deferred.

### 2.2 Objectives

| ID | Objective | Success Metric |
|----|-----------|----------------|
| OBJ-1 | Codify cross-cutting behavioral standards from the recurring bug patterns | Standards documented in a reference that all commands can cite |
| OBJ-2 | Fix all bugs tied to the recurring pattern classes (BUG-009, BUG-016/017, BUG-018, success-message family) across all affected commands | Re-run of the test scenario shows these pattern classes eliminated |
| OBJ-3 | Fix command-specific bugs where the fix is a low-effort targeted edit | Bug tracking table updated with command-updated status |
| OBJ-4 | Document deferred bugs with rationale for deferral | All 46 bugs have a disposition: fixed, deferred, or won't fix |

---

## 3. Requirements

### 3.1 Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-F1 | All commands that use templates shall copy the template file via `cp`, then use Edit for placeholder substitution — never Write from scratch | MUST | Root cause of BUG-009, BUG-007, BUG-008, BUG-020, BUG-031 |
| REQ-F2 | All commands shall execute pre-flight steps sequentially in specified order; PLANNING.md update shall be step 2 before any other checks | MUST | BUG-016, BUG-017 — recurring across all commands |
| REQ-F3 | All commands that gather user input shall prompt one section or item at a time with an explicit stop between each | MUST | BUG-018, BUG-034 — affects /spec, /charter, /architect, /define, /build |
| REQ-F4 | All commands shall emit the complete prescribed success message including all required fields and next steps | MUST | BUG-014, BUG-021, BUG-032, BUG-037, BUG-043, BUG-044 — 6 instances across commands |
| REQ-F5 | All commands shall update PLANNING.md as a hard gate before showing the success message | MUST | BUG-036, BUG-042 — PLANNING.md updates consistently deferred or skipped |
| REQ-F6 | Commands shall avoid deepening Todoist-specific coupling pending task management service replacement evaluation | SHOULD | /breakdown Todoist dependency under review |
| REQ-F7 | Framework CLAUDE.md template shall include a template-anchoring behavioral note clarifying that example counts are illustrative, not prescriptive | SHOULD | ISSUE-001 — agent output count anchors to template example count |
| REQ-F8 | The template-anchoring note shall also be added to individual command specs that populate templates | COULD | Belt-and-suspenders enforcement for ISSUE-001 |

### 3.2 Non-Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-N1 | Each command fix shall be a targeted edit — no unrelated refactoring of surrounding content | MUST | Solo developer; minimize regression surface |
| REQ-N2 | All 46 bugs shall have a documented disposition (fixed / deferred / won't fix) in the bug report fix tracking table | MUST | Traceability — know what has and has not been addressed |

---

## 4. User Stories / Use Cases

### UC-1: Developer Runs a Fixed Command

**Actor:** Developer invoking a Praxisity workflow command

**Preconditions:**
- Command spec has been updated with pattern-class fixes applied

**Flow:**
1. Developer invokes command (e.g., `/spec`)
2. Pre-flight executes sequentially; PLANNING.md updated as step 2 before any other checks
3. Gathering prompts one section at a time; waits for response before proceeding
4. Template is copied via `cp` to destination, then filled using Edit
5. PLANNING.md updated as a hard gate before success message
6. Complete prescribed success message shown with all required fields and next steps

**Postconditions:**
- Command completes without exhibiting any of the pattern-class bug behaviors

---

### UC-2: Developer Authors a New Command Using Codified Standards

**Actor:** Developer writing a new Praxisity command

**Preconditions:**
- Behavioral standards reference document exists

**Flow:**
1. Developer reads the standards reference
2. Structures new command with sequential pre-flight, one-at-a-time gathering, copy-then-edit template handling, hard-gated PLANNING.md update, and complete success message

**Postconditions:**
- New command is pattern-compliant without rediscovering the bug patterns from the v0.5.0 test run

---

## 5. Acceptance Criteria

| ID | Criterion | Validates |
|----|-----------|-----------|
| AC-1 | Given a command that uses a template, when it generates output, then the template file is copied via `cp` and the original template is byte-for-byte unchanged | REQ-F1 |
| AC-2 | Given any command invocation, when pre-flight runs, then PLANNING.md is updated as the second step before any other checks complete | REQ-F2 |
| AC-3 | Given a command with a gather phase, when prompting for section N, then section N+1 is not presented until the user has responded to section N | REQ-F3 |
| AC-4 | Given any completed command, when the success message is shown, then all fields and next steps prescribed in the command spec are present | REQ-F4 |
| AC-5 | Given any completed command, when the success message appears, then PLANNING.md has already been updated in that same run | REQ-F5 |
| AC-6 | Given the bug report fix tracking table, when this spec is implemented, then every bug from BUG-001 through BUG-046 has a disposition of fixed, deferred, or won't fix | REQ-N2 |

---

## 6. Constraints

<!--
What limits the solution? Pull relevant constraints from CHARTER.md
and add any spec-specific constraints.

Categories:
- Technical: Platform, integration, performance limits
- Timeline: Deadlines affecting this spec
- Resources: Budget, team, tools available
- Regulatory: Compliance requirements
- Dependencies: External systems, other specs
-->

### 6.1 Inherited from Charter

- Solo developer — changes must be manageable without team coordination
- Strict MVP discipline — no scope creep beyond what bugs require
- Claude Code compatibility required for all command behavior

### 6.2 Spec-Specific Constraints

- Todoist MCP coupling in `/breakdown` shall not be deepened — fixes must remain service-agnostic pending replacement evaluation
- Fixes are targeted edits only; no command may be structurally refactored as part of this work
- Long-term plugin/skill format migration is explicitly out of scope for this spec

---

## 7. Dependencies

<!--
What must exist or happen for this spec to be implementable?
What does this spec enable?
-->

### 7.1 Depends On

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| `.plans/references/new-project-bug-report.md` | Resource | Available | Primary evidence base — all 46 bugs and 3 framework issues |
| All 8 command files in `.claude/commands/` | Resource | Available | Files receiving targeted fixes |
| `.praxisity/templates/` | Resource | Available | Template files referenced by REQ-F1 |

### 7.2 Enables

| Dependent | Relationship |
|-----------|--------------|
| Plugin/skill format migration (long-term) | Stable, well-specified commands are a prerequisite for migration |
| Todoist service replacement evaluation | REQ-F6 keeps `/breakdown` loosely coupled so the dependency can be swapped |

---

## 8. Out of Scope

<!--
CRITICAL SECTION: Explicitly state what this spec does NOT cover.
This prevents scope creep and sets clear boundaries.

Include things that:
- Users might reasonably expect but won't be delivered
- Will be addressed in future specs
- Are explicitly excluded by charter
- Are adjacent features you're intentionally not building
-->

The following are explicitly NOT part of this specification:

- Plugin or skill format migration
- Structural refactoring of any command file
- New commands or command features not required to fix a documented bug
- Todoist service replacement (REQ-F6 only prevents deepening the dependency)
- ISSUE-002 (smart quotes in PDF output) and ISSUE-003 (Word Title border) — cosmetic output issues, separate concern
- Bugs discovered during fix implementation that are not in the original BUG-001 through BUG-046 scope

---

## 9. Open Questions

<!--
What needs to be resolved before or during implementation?
Track questions and their resolutions.

Questions should be resolved before moving to design phase,
or explicitly deferred with rationale.
-->

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| Q-1 | Which service replaces Todoist in `/breakdown`? | Deferred | To be decided separately; REQ-F6 keeps the door open |
| Q-2 | Should deferred bugs be logged as tasks in the replacement task manager or tracked in the bug report itself? | Open | Depends on Q-1 outcome |

---

## 10. References

<!--
External documents, research, or resources that inform this spec.
-->

- [Bug Report: v0.5.0 end-to-end test results](../references/new-project-bug-report.md)
- [CHARTER.md](../../CHARTER.md)
- [`.claude/commands/`](../../.claude/commands/) — all 8 command files under fix

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-03-22 | Andrew Robert Spenn | Initial draft |

---
