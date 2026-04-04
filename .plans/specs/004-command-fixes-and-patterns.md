# Specification: SPEC-004 Command Behavioral Fixes and Pattern Standards

## Metadata

| Field | Value |
|-------|-------|
| Spec ID | SPEC-004 |
| Title | Command Behavioral Fixes and Pattern Standards |
| Status | Ready for Design |
| Author | Andrew Robert Spenn |
| Created | 2026-03-22 |
| Last Updated | 2026-04-01 |
| Charter Reference | [CHARTER.md](../../CHARTER.md) — Principles: Dual-use design, Minimal cognitive overhead |

### Related Documents

| Document | Relationship |
|----------|--------------|
| [`.plans/references/new-project-bug-report.md`](../references/new-project-bug-report.md) | Depends on — primary evidence base |
| [`.plans/reviews/SESSION-4-1-26/`](../reviews/SESSION-4-1-26/) | 9-agent parallel review (2026-04-01) |

---

## 1. Problem Statement

Praxisity's workflow commands (`/spec`, `/charter`, `/architect`, `/new-project`, `/breakdown`, `/define`, `/build`, `/deliver`) were tested end-to-end for the first time at v0.5.0. The run revealed 46 bugs and 3 framework issues across 7 tested commands (8 total; `/breakdown` had no bugs), documented in `.plans/references/new-project-bug-report.md`. The failures share identifiable root causes: templates were read then rewritten from memory instead of copied verbatim (BUG-009, Critical), gathering steps were batched instead of one-at-a-time, pre-flight steps were reordered, PLANNING.md updates were consistently deferred, and required success message elements were dropped. These patterns repeat across commands, indicating that the existing command files should be treated as prototypes rather than finished implementations. This spec codifies the behavioral standards that emerged from testing and defines the requirements for full command rewrites that apply them. `/deliver` and `/breakdown` are excluded from this scope — `/deliver` is a fundamentally different process (Python-based PDF generation) and `/breakdown` is tightly coupled to task management service integration, both of which require their own dedicated specs.

---

## 2. Goals and Objectives

### 2.1 Primary Goal

Extract the recurring behavioral patterns from the full bug report into codified command standards, use those standards to guide full rewrites of all workflow commands (treating existing commands as prototypes), and leave a clear tracking record for what is addressed vs. deferred.

### 2.2 Objectives

| ID | Objective | Success Metric |
|----|-----------|----------------|
| OBJ-1 | Codify cross-cutting behavioral standards from the recurring bug patterns | Standards documented in a form that all commands can reference (delivery mechanism TBD in design) |
| OBJ-2 | Rewrite all workflow commands (excluding `/deliver`) using the codified standards, treating existing commands as prototypes | Re-run of the test scenario shows pattern classes eliminated |
| OBJ-3 | Address command-specific bugs within the rewrite scope | Bug disposition table shows each in-scope bug addressed |
| OBJ-4 | Document all bug dispositions (addressed, deferred, or won't fix) with rationale | All 46 bugs have a disposition in the bug disposition table (the bug report's disposition table) |

---

## 3. Requirements

### 3.1 Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-F1 | All commands that use templates shall copy the template file via `cp`, then use Edit for placeholder substitution — never Write from scratch | MUST | Root cause of BUG-020 (/spec), BUG-009 (original discovery in /new-project, now deferred) |
| REQ-F1a | When a template section does not apply, commands shall mark it "N/A — [reason]" rather than removing it | MUST | BUG-031 — sections were silently removed instead of marked; distinct from the copy-then-edit root cause |
| REQ-F2 | All commands shall execute pre-flight steps sequentially in specified order; PLANNING.md update shall be step 2 before any other checks. Each step must complete before the next begins — do not batch or parallelize pre-flight steps | MUST | BUG-016, BUG-017 — numbered lists alone did not prevent parallelization |
| REQ-F3 | All commands that gather user input shall prompt one section at a time by default, waiting for the user's response before presenting the next section. When the agent has sufficient context to draft a section, it may present a draft for approval rather than prompting from scratch, but must still pause between sections for user confirmation. Do not draft content for sections the user has not yet been prompted for | MUST | BUG-012, BUG-018, BUG-034 — affects /spec, /charter, /architect, /define, /build |
| REQ-F4 | All commands shall emit every element listed in their own Success Message section, including all required fields and next steps. Each command's "complete" is defined by its own spec, not a uniform template | MUST | BUG-014, BUG-021, BUG-032, BUG-037, BUG-043, BUG-044 — 6 instances across commands |
| REQ-F5 | All commands shall update PLANNING.md as a hard gate before showing the success message | MUST | BUG-036, BUG-042 — PLANNING.md updates consistently deferred or skipped |
| REQ-F6 | ~~Removed~~ — `/breakdown` is now fully out of scope; Todoist coupling concern deferred with it | — | — |
| REQ-F7 | Framework CLAUDE.md template shall include a template-anchoring behavioral note clarifying that example counts are illustrative, not prescriptive (verify existing CLAUDE.md hint is sufficient before adding a second instance) | SHOULD | ISSUE-001 — agent output count anchors to template example count; existing "Hints from the developer" section may already address this |

### 3.2 Non-Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-N1 | Commands shall be fully rewritten using the codified behavioral standards, treating existing command files as prototypes and semantic inspiration rather than code to patch. Each rewrite shall be developed with a Mode 3 collaborative agent team reviewing in real time | MUST | Existing commands are prototypes; targeted edits cannot achieve the behavioral consistency needed. Agent team review during authoring catches cross-cutting issues between perspectives |
| REQ-N2 | All 46 bugs shall have a documented disposition (addressed / deferred / won't fix) in the bug disposition table (the bug report's disposition table) | MUST | Traceability — know what has and has not been addressed |

---

## 4. User Stories / Use Cases

### UC-1: Developer Runs a Rewritten Command

**Actor:** Developer invoking a Praxisity workflow command

**Preconditions:**
- Command has been rewritten using the codified behavioral standards

**Flow:**
1. Developer invokes command (e.g., `/spec`)
2. Pre-flight executes sequentially; PLANNING.md updated as step 2 before any other checks
3. Gathering prompts one section at a time; waits for response before proceeding (may present drafts for approval when context is sufficient)
4. Template is copied via `cp` to destination, then filled using Edit; inapplicable sections marked N/A
5. PLANNING.md updated as a hard gate before success message
6. Complete prescribed success message shown with all elements defined in that command's spec

**Postconditions:**
- Command completes without exhibiting any of the pattern-class bug behaviors

---

### UC-2: Developer Authors a New Command Using Codified Standards

**Actor:** Developer writing a new Praxisity command

**Preconditions:**
- Behavioral standards are accessible (delivery mechanism TBD in design — could be a reference document, context block, skill, or template)

**Flow:**
1. Developer reads the standards
2. Structures new command with sequential pre-flight, one-at-a-time gathering, copy-then-edit template handling, hard-gated PLANNING.md update, and complete success message

**Postconditions:**
- New command is pattern-compliant without rediscovering the bug patterns from the v0.5.0 test run

---

## 5. Acceptance Criteria

| ID | Criterion | Validates |
|----|-----------|-----------|
| AC-1 | Given a command that uses a template, when it generates output, then the template file is copied via `cp` and the original template is byte-for-byte unchanged, and the output was produced by applying only Edit-based modifications to the copy | REQ-F1 |
| AC-1a | Given a command output where a template section does not apply, then that section is present and marked "N/A — [reason]" rather than removed | REQ-F1a |
| AC-2 | Given any command invocation, when pre-flight runs, then PLANNING.md is updated as the second step before any other checks complete | REQ-F2 |
| AC-3 | Given a command with a gather phase, when prompting for section N, then section N+1 is not presented until the user has responded to section N | REQ-F3 |
| AC-4 | Given any completed command, when the success message is shown, then all elements defined in that command's Success Message section are present | REQ-F4 |
| AC-5 | Given any completed command, when the success message appears, then PLANNING.md has already been updated in that same run | REQ-F5 |
| AC-6 | Given the bug report's disposition table, when this spec is implemented, then every bug from BUG-001 through BUG-046 has a disposition of addressed, deferred, or won't fix | REQ-N2 |
| AC-7 | Given any rewritten command, then it was developed using a Mode 3 collaborative agent team and the existing command was used as prototype/inspiration, not as a base to patch | REQ-N1 |

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

- `/breakdown` is entirely out of scope — tightly coupled to task management service integration, requires its own spec
- `/deliver` is excluded — separate Python-based process, will be addressed independently
- Commands are fully rewritten, not patched — existing commands serve as prototypes and semantic inspiration
- The command-vs-skill format migration question is deferred to the `/architect` phase for research and design decision
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
| 5 command files in `.claude/commands/` (`/charter`, `/spec`, `/architect`, `/define`, `/build`) | Resource | Available | Prototypes for skill rewrites (`/deliver`, `/breakdown`, `/new-project` excluded) |
| `.praxisity/templates/` | Resource | Available | Template files referenced by REQ-F1 |

### 7.2 Enables

| Dependent | Relationship |
|-----------|--------------|
| `/new-project` rewrite or sunset (future) | Behavioral standards apply if /new-project is retained; distribution model decision comes first |
| `/breakdown` rewrite (future) | Stable behavioral standards apply when `/breakdown` gets its own spec |
| `/deliver` rewrite (future) | Stable commands are a prerequisite for the full delivery pipeline |

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

- `/new-project` command — sunset candidate pending framework distribution model decision; all 9 bugs (BUG-001 through BUG-009) deferred
- `/deliver` command — fundamentally different process (Python-based PDF generation), will be addressed separately
- `/breakdown` command — tightly coupled to task management service integration (currently Todoist), which requires its own spec once the service question (Q-1) is resolved
- All `/deliver`-specific bugs (BUG-038, BUG-039, BUG-045, BUG-046) — deferred with `/deliver`
- All `/breakdown`-specific bugs — deferred with `/breakdown`
- Plugin or skill format migration (the command-vs-skill question is deferred to `/architect` for research)
- New commands or command features not required to address a documented bug
- Todoist service replacement (deferred with `/breakdown`; Todoist optional steps in remaining commands are a design decision for `/architect`)
- BUG-040/BUG-041 (context compaction during long sessions) — platform limitation, not addressable by command rewrites
- ISSUE-002 (smart quotes in PDF output) and ISSUE-003 (Word Title border) — cosmetic output issues, separate concern
- Bugs discovered during implementation that are not in the original BUG-001 through BUG-046 scope

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
| Q-1 | Which service replaces Todoist in `/breakdown`? | Deferred | `/breakdown` is out of scope for this spec; to be decided in its own spec |
| Q-2 | Should deferred bugs be logged as tasks in the replacement task manager or tracked in the bug report itself? | Resolved | Bug dispositions tracked in the bug report's disposition table (REQ-N2). Whether deferred bugs also become tasks elsewhere is a future concern |
| Q-3 | Should commands remain as commands or migrate to skills? | Resolved | Migrate to skills. Platform evidence: commands not listed as extension point, `/init` creates skills, skills support allowed-tools/disable-model-invocation/named args. See DESIGN-005 DEC-1. |
| Q-4 | What is the best mechanism for cross-command behavioral standards? | Resolved | Minimal hybrid: inline mechanical standards (F1, F2, F5) at phase boundaries + shared file for F3 gathering protocol (judgment standard, inline already failed per BUG-018) + per-skill F4 success messages. See DESIGN-005 DEC-2. |
| Q-5 | Do agent prompts need revision before Mode 3 command rewrites? | Open | Two concerns: (1) Agents flagged prompt gaps in SPEC-004 self-evaluations (critic: draft vs. wrong distinction; designer: progressive loading lens unhelpful for flat files; prompt-engineer: needs prompt-infrastructure evaluation guidance). (2) Agent prompts reference the current framework vocabulary (commands, workflow names). After the command-vs-skill decision (Q-3) and any renames, agent descriptions must be updated to match the new terminology. Address during `/architect` |

---

## 10. References

<!--
External documents, research, or resources that inform this spec.
-->

- [Bug Report: v0.5.0 end-to-end test results](../references/new-project-bug-report.md) — primary evidence base, disposition table appended here
- [CHARTER.md](../../CHARTER.md)
- [`.claude/commands/`](../../.claude/commands/) — 6 command files in scope for rewrite
- [Session reviews](../reviews/SESSION-4-1-26/) — 9-agent parallel review (2026-04-01)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-03-22 | Andrew Robert Spenn | Initial draft |
| 0.2 | 2026-04-01 | Andrew Robert Spenn | Post-review revision: reframed from targeted fixes to full command rewrites; excluded `/deliver` and `/breakdown` from scope; split REQ-F1/BUG-031 into REQ-F1a; added BUG-012 to REQ-F3; strengthened REQ-F2 and REQ-F3 language for AI consumption; added flexibility clause to REQ-F3; removed REQ-F6 (moot with `/breakdown` excluded) and REQ-F8; added AC-1a, AC-7; deferred command-vs-skill and standards delivery mechanism to `/architect`; added Q-3, Q-4; resolved Q-2 |
| 0.3 | 2026-04-03 | Andrew Robert Spenn | Design phase updates: dropped `/new-project` from scope (sunset candidate, 9 bugs deferred); scope now 5 skills; adjusted BUG-009 citation in REQ-F1 to lead with BUG-020; Q-3 resolved (skills format); Q-4 resolved (inline mechanical + shared F3); renames confirmed (describe, charter, design, plan, do) |

---
