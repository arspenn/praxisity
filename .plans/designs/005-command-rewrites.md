# Design: DESIGN-005 Command Behavioral Fixes and Pattern Standards

## Metadata

| Field | Value |
|-------|-------|
| Design ID | DESIGN-005 |
| Title | Command Behavioral Fixes and Pattern Standards |
| Status | Draft |
| Author | Designer Agent (Mode 3 collaborative team) |
| Created | 2026-04-03 |
| Last Updated | 2026-04-03 |

### Specification References

| Spec ID | Title | Requirements Addressed |
|---------|-------|------------------------|
| [SPEC-004](../specs/004-command-fixes-and-patterns.md) | Command Behavioral Fixes and Pattern Standards | REQ-F1, REQ-F1a, REQ-F2, REQ-F3, REQ-F4, REQ-F5, REQ-F7, REQ-N1, REQ-N2 |

### Related Documents

| Document | Relationship |
|----------|--------------|
| [Bug Report](../references/new-project-bug-report.md) | Depends on — primary evidence base (46 bugs, 3 issues) |
| [SESSION-4-1-26 reviews](../reviews/SESSION-4-1-26/) | Depends on — 9-agent parallel review informing design |
| [SESSION-4-3-26 reviews](../reviews/SESSION-4-3-26/) | Depends on — Mode 3 collaborative design session |
| [consult-team skill](../../.claude/skills/consult-team/) | Reference — proven skill directory structure |

---

## 1. Overview

### 1.1 Design Summary

This design transforms 6 Praxisity workflow commands from prototype `.claude/commands/*.md` files into directory-based skills under `.claude/skills/`, applying codified behavioral standards extracted from the v0.5.0 bug report. All 5 behavioral standards are embedded inline at phase boundaries within each skill — no shared files are read by AI at runtime. A human-only authoring reference (`command-standards.md`) documents the standards for UC-2 (new skill creation) but is never loaded during skill execution. Each skill is a full rewrite treating the existing command as prototype and semantic inspiration, not a base to patch.

The 6 commands fall into two structural families — template-producing skills (spec, charter, architect, define) that share a common Pre-Flight → Gather → Generate → Post-Save → Success Message skeleton, and execution skills (build, new-project) that diverge structurally. The design accommodates both families while maintaining a unified standards approach.

### 1.2 Design Principles

- **Inline over indirection:** All behavioral standards are embedded at the point of application within each skill. AI agents reliably follow inline imperatives; they unreliably follow cross-references. Zero shared files read at runtime.
- **Phase-gated placement:** Standards appear at the phase boundary where they apply, not at the top of the file. The agent reads template handling rules right before Generate, not 200 lines earlier.
- **Minimal coupling surface:** Each skill is fully self-contained — no skill depends on another skill's internals, and no shared files are loaded during execution. The only external references are to `.praxisity/templates/` for output generation.
- **Compression over explanation:** Standards are compressed to the minimum lines that address the documented bug patterns. Operational context (the "why") is embedded in the phrasing of the rule itself, not in a separate explanation.

### 1.3 Requirements Coverage

| Requirement | Design Section | Approach |
|-------------|----------------|----------|
| REQ-F1 | COMP-3, DEC-4 | Copy-then-edit protocol with 6 permitted operations, inline at Generate phase |
| REQ-F1a | COMP-3 | N/A marking as permitted operation #4 |
| REQ-F2 | COMP-4 | Sequential execution constraint inline at Pre-Flight phase |
| REQ-F3 | COMP-5 | Compressed 4-line inline standard at Gather phase boundary |
| REQ-F4 | COMP-6 | Per-skill success message checklist (each skill defines its own elements) |
| REQ-F5 | COMP-6 | One-line imperative between Post-Save and Success Message |
| REQ-F7 | DEC-4, COMP-3 | Resolved by operation #6 (table row adjustment) — "template example counts are illustrative, not prescriptive" |
| REQ-N1 | DEC-1, DEC-5 | Full rewrites as skills with Mode 3 team; implementation order: charter first |
| REQ-N2 | COMP-3 (note) | Bug disposition table in bug report is complete (35+1 in scope); design maps each to components |

---

## 2. Architecture

### 2.1 System Context

```
.claude/
├── skills/
│   ├── _shared/
│   │   └── command-standards.md        ← human authoring reference (UC-2, never read at runtime)
│   ├── spec/
│   │   └── SKILL.md                    ← full rewrite of /spec command
│   ├── charter/
│   │   └── SKILL.md                    ← full rewrite of /charter command
│   ├── architect/
│   │   └── SKILL.md                    ← full rewrite of /architect command
│   ├── define/
│   │   └── SKILL.md                    ← full rewrite of /define command
│   ├── build/
│   │   └── SKILL.md                    ← full rewrite of /build command
│   └── new-project/
│       └── SKILL.md                    ← full rewrite of /new-project command
│
├── commands/                           ← existing prototypes (retained as reference during rewrites)
│
.praxisity/
└── templates/                          ← template files referenced by REQ-F1
    ├── spec.template.md
    ├── charter.template.md
    ├── design.template.md
    ├── dip.template.md
    ├── claude.template.md
    ├── readme.template.md
    └── changelog.template.md
```

### 2.2 Architecture Pattern

**Pattern:** Skill-per-command with shared behavioral constraints

**Rationale:** Each workflow command becomes a self-contained skill directory. Skills are the unit of loading — when invoked, the platform loads the SKILL.md as the agent's instructions. Behavioral standards are delivered at phase boundaries within each SKILL.md, with one shared file for the gathering protocol. This matches the existing `consult-team` skill pattern proven in the codebase.

**Trade-offs:**
- Pros: Fully self-contained skills, no hidden dependencies, no cross-references, maximum AI reliability
- Cons: ~8-12 lines of inline standard text duplicated across 6 skills (acceptable — total duplication is small and each instance is adapted to its phase context)

### 2.3 Two Structural Families

The 6 skills divide into two families based on their phase structure:

**Template-producing skills** (spec, charter, architect, define):
```
Pre-Flight → Gather → Generate-from-template → Post-Save → Success Message
```
All 5 behavioral standards apply. These skills share the full skeleton and differ only in gathering content and template.

**Execution skills** (build, new-project):
```
/build:       Pre-Flight → DIP-Execution → Completion → Success Message
/new-project: Pre-Flight → Parameter-Gathering → Execution-Steps → Success Message
```
Standards apply selectively:

| Standard | spec | charter | architect | define | build | new-project |
|----------|------|---------|-----------|--------|-------|-------------|
| REQ-F1 (template handling) | yes | yes | yes | yes | N/A | adapted (multi-template) |
| REQ-F2 (sequential pre-flight) | yes | yes | yes | yes | yes | yes |
| REQ-F3 (gathering) | yes | yes | yes | yes | N/A | yes (parameter gathering) |
| REQ-F4 (success message) | yes | yes | yes | yes | yes | yes |
| REQ-F5 (PLANNING.md gate) | yes | yes | yes | yes | yes | yes |

---

## 3. Components

### COMP-1: Standards Delivery System

**Purpose:** Deliver behavioral standards to each skill at the right phase with maximum AI reliability.

**Satisfies:** REQ-F1, REQ-F2, REQ-F3, REQ-F4, REQ-F5 (delivery mechanism for all)

**Responsibilities:**
- Classify standards as mechanical (inline) or judgment (shared file)
- Embed mechanical standards at phase boundaries in each SKILL.md
- Provide shared file for judgment standards with imperative loading instructions
- Provide human-readable authoring reference for UC-2 (new skill creation)

**Dependencies:**
- `.claude/skills/_shared/gathering-standards.md` (the one shared runtime file)
- `.claude/skills/_shared/command-standards.md` (human authoring reference, never read at runtime)

**Key Design Decisions:**
- Mechanical standards inline, judgment standards in shared file (DEC-2)
- Phase-gated loading — standards are read at the boundary where they apply, not at the top
- The architectural distinction: mechanical = "do X, not Y" (survives as terse imperative). Judgment = "apply X considering Y and Z" (needs operational context). REQ-F3 is the only judgment standard.

**Inline standard locations per SKILL.md:**

| Standard | Location in SKILL.md | Approximate text |
|----------|---------------------|------------------|
| REQ-F2 | Top of Pre-Flight section | "Execute steps sequentially. Do not begin step N+1 until step N completes. PLANNING.md update must be step 2." (~2 lines) |
| REQ-F1 | Top of Generate section | "Copy template to destination via `cp`. Read the copy. Use Edit for permitted modifications only. Never use Write for template-derived files." (~3 lines) |
| REQ-F3 | Top of Gather section | Imperative: "Before gathering, read `.claude/skills/_shared/gathering-standards.md` and apply its rules to each section below." (~1 line) |
| REQ-F5 | Between Post-Save and Success Message | "Update PLANNING.md with completion status. This is a hard gate — do not show the success message until PLANNING.md is updated." (~1 line) |
| REQ-F4 | Within Success Message section | Per-skill checklist of required elements (unique per skill, not duplicated) |

---

### COMP-2: Skill File Structure

**Purpose:** Define the directory layout and file structure for each rewritten command.

**Satisfies:** REQ-N1 (full rewrites as skills)

**Responsibilities:**
- Each skill is a directory under `.claude/skills/` containing at minimum a `SKILL.md`
- SKILL.md contains YAML frontmatter (name, description), followed by structured sections
- Shared resources live under `_shared/`
- Existing `.claude/commands/*.md` files retained during transition as prototype reference

**Dependencies:**
- Claude Code skills platform (directory-based loading)
- Existing `consult-team` skill as proven structural reference

**Key Design Decisions:**
- Skills format chosen over commands (DEC-1) — directory-based, supports supporting files, progressive loading
- No supporting files needed per-skill beyond SKILL.md (unlike consult-team which has templates/)
- The `_shared/` directory holds cross-skill resources

**Standard SKILL.md section order for template-producing skills:**

```
---
name: [skill-name]
description: [one-line description]
---

# [Skill Name]

[Brief purpose statement]

## Constraints
[Skill-specific behavioral constraints]

## Pre-Flight
[REQ-F2 inline standard]
1. Read PLANNING.md...
2. Update PLANNING.md...
[remaining pre-flight steps]

## [Skill-Specific] Flow

### Introduction
[Framing for the user]

### Gather [Content Type]
[REQ-F3 imperative loading instruction]
[Section-by-section gathering]

### Review and Confirm
[Structured review with y/e/c options]

## Generate [Output Type]
[REQ-F1 inline standard]
1. Copy template via cp...
2. Read the copy...
3. Edit to populate...

## Post-Save
[Optional: task manager integration, git commit]

[REQ-F5 inline standard — PLANNING.md hard gate]

## Success Message
[REQ-F4 per-skill checklist]

## Behavior Notes
[Skill-specific behavioral guidance]
```

---

### COMP-3: Template Handling Protocol

**Purpose:** Define how skills interact with `.praxisity/templates/` files to produce deterministic output.

**Satisfies:** REQ-F1, REQ-F1a, REQ-F7

**Responsibilities:**
- Enforce copy-then-edit pattern for all template-derived output
- Define permitted Edit operations (closed list — anything not listed is not permitted)
- Handle dual-use template lifecycle (read for gathering context, copy for generation)
- Handle `/new-project`'s multi-template variant

**Dependencies:**
- `.praxisity/templates/*.md` (7 template files)
- Bash `cp` command for file copying
- Edit tool for modifications

**Permitted Edit Operations:**

| # | Operation | Description |
|---|-----------|-------------|
| 1 | Placeholder substitution | Replace bracketed placeholders (e.g., `[PROJECT_NAME]`, `SPEC-NNN`) with actual values |
| 2 | Domain section removal | Delete template sections that don't apply to the detected project type |
| 3 | HTML comment stripping | Remove `<!-- ... -->` guidance comments |
| 4 | N/A marking | Replace content of inapplicable sections with "N/A — [reason]" (REQ-F1a) |
| 5 | Content population | Fill gathered user input into the appropriate template sections |
| 6 | Table row adjustment | Add or remove rows in ID-tracked tables to match gathered content count exactly. If gathered content has fewer entries than template example rows, remove excess rows. If more, add rows. Preserve table format and header. Generate sequential IDs. Template example row counts are illustrative, not prescriptive. |

**NOT permitted:**
- Rewriting existing template prose
- Adding sections not present in the template
- Restructuring section order
- Paraphrasing or summarizing template language

**Dual-use template lifecycle:**
1. **During Gather phase:** Read the original template (with HTML comments intact) as a reference for section structure, examples, and domain-specific prompts. The comments are the gathering guide.
2. **During Generate phase:** `cp` the template to the destination path. Read the fresh copy. Apply permitted Edit operations. The original template is never modified.

**`/new-project` per-template operation matrix:**

| Template | Destination | cp | Placeholder sub | Domain removal | Comment strip | Content population |
|----------|-------------|----|-----------------|----|---|---|
| claude.template.md | CLAUDE.md | yes | yes | yes | yes | no |
| charter.template.md | CHARTER.md | yes | no | no | no | no |
| readme.template.md | README.md | yes | yes | no | no | no |
| changelog.template.md | CHANGELOG.md | yes | yes | no | yes | no |

---

### COMP-4: Pre-Flight Protocol

**Purpose:** Ensure consistent pre-flight behavior across all skills.

**Satisfies:** REQ-F2

**Responsibilities:**
- Enforce sequential step execution (no parallelization, no batching)
- Ensure PLANNING.md update is step 2 in every skill's pre-flight
- Provide skill-specific pre-flight steps after the common first two

**Dependencies:**
- PLANNING.md (read and write)
- Skill-specific resources (CHARTER.md, specs, designs, templates, etc.)

**Common pre-flight steps (all skills):**

| Step | Action | Notes |
|------|--------|-------|
| 1 | Read PLANNING.md for session context; create if missing | First step, always |
| 2 | Update PLANNING.md with this skill as active command | Hard gate — must complete before step 3 |
| 3+ | Skill-specific checks | Varies per skill |

**Inline standard text (embedded at top of each Pre-Flight section):**

> Execute these steps sequentially in the order listed. Do not begin step N+1 until step N is complete. Do not batch or parallelize pre-flight steps.

**Why this is inline, not shared:** The sequential execution rule is a mechanical constraint — "do not parallelize" — that was defeated when phrased as a numbered list alone (BUG-016, BUG-017). The explicit prohibition needs to be directly above the numbered steps, not in a separate file read beforehand.

---

### COMP-5: Gathering Protocol

**Purpose:** Prevent batched gathering by providing operational context for one-at-a-time prompting.

**Satisfies:** REQ-F3

**Responsibilities:**
- Define what "one section at a time" means operationally
- Define when draft-for-approval is permitted vs. prompting from scratch
- Define the boundary of "sufficient context" for drafting

**Dependencies:**
- `.claude/skills/_shared/gathering-standards.md` (the shared file)

**Why this is a shared file, not inline:** REQ-F3 is the only judgment standard. Inline "one section at a time" was already present in prototype commands and was defeated (BUG-018: agent drafted sections 3-10 in a single batch despite the constraint). The operational context — what "sufficient context" means, what "one at a time" means in practice, when drafting is OK — is ~15 lines and provides the behavioral anchoring that a terse rule cannot.

**`gathering-standards.md` content structure:**

```markdown
# Gathering Standards

## Rule
Prompt one section at a time. Wait for the user's response before presenting
the next section.

## When drafting is permitted
When the agent has sufficient context (prior conversation, loaded documents,
domain knowledge) to produce a reasonable draft for a section, it may present
a draft for approval rather than prompting from scratch. But:
- Still pause between sections for user confirmation
- Do not draft content for sections the user hasn't been prompted for yet
- "Sufficient context" means you can produce something the user would accept
  with minor edits, not that you can produce *something*

## What "one section at a time" means operationally
- Present section N's prompt or draft
- Wait for explicit user response (approval, edit, or new input)
- Only then present section N+1
- Never bundle multiple sections into a single message
- Never draft ahead of where the user has confirmed
```

**Imperative loading instruction (in each SKILL.md's Gather section):**

> Before gathering, read `.claude/skills/_shared/gathering-standards.md` and apply its rules to each section below.

**Applicability:** Template-producing skills (spec, charter, architect, define) and `/new-project` (parameter gathering). Does NOT apply to `/build` — its DIP execution steps are agent-driven with verification gates, not user-input gathering.

---

### COMP-6: Completion Protocol

**Purpose:** Ensure consistent completion behavior — PLANNING.md gating and complete success messages.

**Satisfies:** REQ-F4, REQ-F5

**Responsibilities:**
- Enforce PLANNING.md update as a hard gate before success message display
- Ensure each skill emits all elements defined in its own Success Message section

**Dependencies:**
- PLANNING.md (write)
- Per-skill success message element definitions

**REQ-F5 inline standard (between Post-Save and Success Message):**

> Update PLANNING.md with completion status, active artifacts, and next steps. This is a hard gate — do not display the success message until PLANNING.md has been updated in this run.

**REQ-F4 approach:** Each skill defines its own success message checklist. These are NOT standardized across skills because each skill's "complete" is different (SPEC-004 spec, Section 3.1, REQ-F4 note). The design specifies the structure, not the content:

```markdown
## Success Message

Show all of the following:
- [ ] [Element 1 specific to this skill]
- [ ] [Element 2 specific to this skill]
- [ ] Next steps:
  1. [Step 1]
  2. [Step 2]
```

**Post-Save section restructuring:** In prototype commands, PLANNING.md update was buried as step 3-4 inside Post-Save, after optional Todoist/git steps. This is the root cause of BUG-036 and BUG-042. The design restructures the section order:

```
## Post-Save
1. Optional: create task in project task management service (if available)
2. Optional: commit to git with conventional format

## Completion Gate
Update PLANNING.md with completion status. Do not proceed until this is done.

## Success Message
[per-skill checklist]
```

The "Completion Gate" is a new structural element that physically separates Post-Save from Success Message with the PLANNING.md requirement between them.

---

## 4. Interfaces

### INT-1: Skill ↔ Shared Standards

**Connects:** Each SKILL.md (COMP-2) ↔ `_shared/gathering-standards.md` (COMP-5)

**Type:** File read (imperative)

**Direction:** Unidirectional — SKILL.md reads from `_shared/`; never writes.

**Contract:**
- **Trigger:** Agent reaches the Gather phase boundary in a skill
- **Instruction:** Imperative "read this file now and apply" (not passive "see also")
- **Content:** The gathering protocol rules (~15 lines)
- **Failure mode:** If the agent doesn't read the file, behavior reverts to prototype-era failure mode (batched gathering). This is a bounded downside — no worse than current state.
- **Applicability filter:** Only skills with user-input gathering phases include the imperative. `/build` omits it.

### INT-2: Skill ↔ Templates

**Connects:** Each template-producing SKILL.md (COMP-2) ↔ `.praxisity/templates/*.md` (COMP-3)

**Type:** File read + file copy + file edit

**Direction:** Unidirectional — skill reads and copies templates; never modifies originals.

**Contract:**
```
Phase 1 (Gather): Read template original → extract section structure, examples, prompts
Phase 2 (Generate):
  1. cp template.md → destination.md    (Bash cp)
  2. Read destination.md                (Read tool)
  3. Edit destination.md                (Edit tool, permitted operations only)
  4. Verify: original template unchanged (implicit — cp creates the copy)
```

**Error handling:** If `cp` fails (permissions, missing file), halt and report. If Edit fails (old_string not found), halt and report — do not fall back to Write.

### INT-3: Skill ↔ PLANNING.md

**Connects:** Each SKILL.md (COMP-2) ↔ PLANNING.md

**Type:** File read + file write

**Direction:** Bidirectional — skill reads context and writes updates.

**Contract:**
```
Pre-Flight Step 1: Read PLANNING.md (or create if missing)
Pre-Flight Step 2: Write — set active command/skill
Completion Gate:   Write — set completion status, artifacts, next steps
                   MUST complete before Success Message is displayed
```

**Touchpoints per skill execution:** Exactly 3 — read at start, write at step 2, write at completion gate. No intermediate writes during Gather or Generate phases.

---

## 5. Data Model

### DATA-1: Skill File (SKILL.md)

**Purpose:** The complete behavioral specification for one workflow skill.

**Used by:** Claude Code platform (loaded as agent instructions when skill is invoked)

**Schema/Structure:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| YAML frontmatter | metadata | Yes | `name` and `description` fields |
| Constraints | section | Yes | Skill-specific behavioral limits |
| Pre-Flight | section | Yes | Sequential steps with REQ-F2 inline standard |
| Flow/Gather | section | Yes (template-producing) | Content gathering with REQ-F3 imperative |
| Generate | section | Yes (template-producing) | Template handling with REQ-F1 inline standard |
| Post-Save | section | Yes | Optional integrations (task manager, git) |
| Completion Gate | section | Yes | REQ-F5 PLANNING.md hard gate |
| Success Message | section | Yes | REQ-F4 per-skill element checklist |
| Behavior Notes | section | Optional | Skill-specific guidance |

### DATA-2: Gathering Standards File

**Purpose:** Shared operational context for the gathering protocol (REQ-F3).

**Used by:** COMP-5 (Gathering Protocol), loaded by template-producing skills + `/new-project`

**Schema/Structure:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Rule | section | Yes | Core one-at-a-time rule |
| When drafting is permitted | section | Yes | Exception conditions and boundaries |
| Operational definition | section | Yes | Step-by-step meaning of "one at a time" |

**Constraints:**
- Must be self-contained — no cross-references to other files
- Must be under 20 lines — loaded into context at a phase boundary, not at session start

### DATA-3: Command Standards Reference (Human Authoring Guide)

**Purpose:** Canonical reference for authors creating new skills (UC-2). Not read by AI at runtime.

**Used by:** Human developers writing new Praxisity skills

**Schema/Structure:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Per-standard sections | section | Yes | Each REQ-F standard with rule, rationale, and application guidance |
| Standard classification | metadata | Yes | Mechanical vs. judgment classification |
| Delivery instructions | section | Yes | Where and how to embed each standard in a new SKILL.md |

---

## 6. Design Decisions

### DEC-1: Skills Format Over Commands

**Context:** Q-3 — existing commands are `.claude/commands/*.md` files. Should rewrites remain as commands or migrate to directory-based skills?

**Decision:** Migrate to skills under `.claude/skills/[name]/SKILL.md`.

**Rationale:** Skills are directory-based (SKILL.md + supporting files), enabling progressive loading and shared resources. The `_shared/` directory provides a natural location for the gathering standards file. Skills also align with the framework's direction (SPEC-006, agent-authoring skill, consult-team precedent).

**Alternatives Considered:**
- Keep as commands: Simpler but flat — no directory structure for shared resources, no supporting files
- MCP tools: Overkill — these are prompt instructions, not programmatic interfaces

**Consequences:**
- Existing commands retained as prototypes during transition
- Each skill gets its own directory even if it only contains SKILL.md
- `_shared/` directory establishes the pattern for future shared resources

---

### DEC-2: Hybrid Standards Delivery — Mechanical Inline, Judgment Shared

**Context:** Q-4 — how do behavioral standards reach each skill? Options: shared reference doc, context block, extracted skill, inline duplication, or hybrid.

**Decision:** Inline mechanical standards at phase boundaries + one shared file for the judgment standard (REQ-F3 gathering protocol).

**Rationale:**
- **Mechanical standards** (F1, F2, F5): 2-4 lines each, "do X not Y" rules. These survive as inline imperatives. Cross-referencing adds indirection cost that exceeds the duplication cost (~7-8 lines total per skill).
- **Judgment standard** (F3): ~15 lines of operational context. Inline "one section at a time" was already present in prototypes and defeated (BUG-018). The "why" context provides behavioral anchoring that terse rules cannot.
- **Per-skill standard** (F4): Each skill's success message is unique. No duplication — each defines its own checklist.

**Alternatives Considered:**
- Pure shared reference: AI cross-referencing unreliable (skeptic's v0.1 review insight)
- Pure inline duplication: Would duplicate F3's 15 lines across 5 skills — unnecessary when a shared file works for this one standard
- Context block: No existing loading mechanism in skills, can't be section-targeted
- Extracted skill: Standards are constraints, not a skill — no invocation or flow

**Consequences:**
- One cross-reference in the entire system (`gathering-standards.md`)
- If the cross-reference fails, bounded downside — reverts to current failure mode
- Human authoring reference (`command-standards.md`) is documentation, not infrastructure

---

### DEC-3: Todoist Abstraction to Generic Task Manager

**Context:** Todoist is named in 4 of 6 in-scope commands as optional post-save integration. `/breakdown` (excluded) is deeply Todoist-coupled. Charter still mandates Todoist but replacement is deferred.

**Decision:** Abstract all Todoist references to generic "project task management service (if available)." Remove hardcoded MCP tool names.

**Rationale:** Three coupling types identified:
1. **Post-save convenience** (spec, charter, architect): "Optionally create task" — abstract to generic
2. **Input source** (define): "Task from Todoist" — abstract to "task from project task manager"
3. **Completion signal** (build): Hardcoded `mcp__todoist__complete-tasks` — abstract to "mark task complete in project task management service"

Hardcoding "Todoist" in 4 skills creates 4 update points when the service changes. The abstraction costs nothing — steps are already "if available" guarded.

**Alternatives Considered:**
- Remove entirely: Loses the integration point; would need re-adding when replacement lands
- Keep as-is: 4 unnecessary update points when service changes

**Consequences:**
- No service-specific MCP tool names in any skill file
- Task management integration remains as optional steps
- When replacement service is chosen, only the service-specific implementation changes — skill files stay generic

---

### DEC-4: Permitted Edit Operations (Closed List)

**Context:** REQ-F1 says "Edit-based modifications" but doesn't define what operations are permitted. The critic flagged this as under-specified.

**Decision:** Define a closed list of 6 permitted operations. Anything not listed is not permitted.

**Rationale:** A closed list prevents the agent from reinterpreting "Edit-based modifications" as license to rewrite template content. The operations were derived from analyzing what the 7 templates actually require and what the bug report documented as failures.

**The 6 operations:** Placeholder substitution, domain section removal, HTML comment stripping, N/A marking, content population, table row adjustment. (Full definitions in COMP-3.)

**Alternatives Considered:**
- Open-ended "use Edit tool appropriately": Too vague — the v0.5.0 test showed agents interpret liberally
- Positive-and-negative list: The NOT-permitted list supplements the positive list to close loopholes

**Consequences:**
- Table row adjustment (operation #6) resolves ISSUE-001 (template anchoring) at the design level
- `/new-project` applies a per-template subset of operations (matrix in COMP-3)

---

### DEC-5: Templates Remain in `.praxisity/templates/`

**Context:** Skills format supports bundled resources (e.g., `consult-team/templates/`). Should output templates move from `.praxisity/templates/` into each skill's directory?

**Decision:** Templates stay in `.praxisity/templates/`. Skills reference them by path.

**Rationale:** Templates and skill-internal resources serve different audiences:
- **Skill-internal resources** (like consult-team's `context-block.md`) are consumed by the skill during execution. They have no meaning outside the skill. Bundling is correct.
- **Output templates** (like `spec.template.md`) define what the user's output documents look like. They're the user's customization surface — a user might modify their spec template without touching skill logic. `.praxisity/` is framework configuration that `/new-project` preserves for the user. `.claude/` is agent infrastructure.

Additionally, `charter.template.md` is shared between `/charter` (fills it) and `/new-project` (copies it as placeholder). Bundling would require either a duplicate or a cross-skill reference — both worse than the current shared location.

**Alternatives Considered:**
- Bundle in skill directories, keep `.praxisity/` as meta-source: Two copies of each template, sync question
- Bundle in skill directories, eliminate `.praxisity/`: Conflates user customization with agent infrastructure; `charter.template.md` duplicated in two skills
- Symlinks: Fragile, platform-dependent, over-engineered for the problem

**Consequences:**
- Skills reference `.praxisity/templates/[name].template.md` — a distant but stable path
- Templates are the user's domain; skills are the framework's domain — clean separation
- Template standardization (consistent metadata tables, HTML comment style, section IDs) is a separate concern addressable by an authoring guide, not by moving files

---

### DEC-6: Implementation Order — Charter First, New-Project Last

**Context:** 6 skills to rewrite. The dependency chain matches the workflow the commands implement. PM analysis identified `/charter` as the simplest pattern-setter and `/new-project` as the most structurally different.

**Decision:** Implement in this order: charter -> spec -> architect -> define -> build -> new-project.

**Rationale:**
- `/charter` is the simplest gathering flow (8 sections, no traceability IDs), has the clearest bug-to-fix mapping, and its output (CHARTER.md) is referenced by `/spec`
- `/spec` adds traceability IDs, references charter — second validation of patterns
- `/architect` is the most complex gathering (domain-aware sections), adds requirement coverage
- `/define` depends on design output format, has the batch-mode design question (BUG-029)
- `/build` has unique execution model (DIP runner, not gatherer) — needs independent design
- `/new-project` is structurally different from all others, mostly cleanup bugs (BUG-001-006)

**Alternatives Considered:**
- Alphabetical: Ignores dependencies and pattern-setting opportunity
- By bug count: `/new-project` has 9 bugs but is the worst pattern-setter
- Parallel: Limited opportunity — each rewrite informs the next

**Consequences:**
- Design and implementation can overlap: once `/charter` is approved, its build can begin while `/spec` design proceeds
- The Mode 3 team accumulates pattern knowledge through the sequence
- `/new-project` benefits from all patterns established in earlier rewrites

---

## 7. Implementation Considerations

### 7.1 Implementation Order

| Order | Skill | Dependencies | Notes |
|-------|-------|--------------|-------|
| 0 | `_shared/gathering-standards.md` | None | Write the shared file first — all gathering skills reference it |
| 0 | `_shared/command-standards.md` | None | Write the authoring reference — informs all rewrites |
| 1 | charter | shared files | Pattern-setter; simplest gathering flow |
| 2 | spec | charter pattern | Adds traceability IDs; references charter output |
| 3 | architect | spec pattern | Most complex gathering; domain-aware sections |
| 4 | define | architect pattern | Depends on design output format; BUG-029 batch question |
| 5 | build | independent | Unique execution model; only F2/F4/F5 apply |
| 6 | new-project | all patterns | Structurally different; multi-template; mostly cleanup bugs |

### 7.2 Risk Areas

| Risk | Impact | Mitigation |
|------|--------|------------|
| Gathering standards file not read by agent | F3 violations (batched gathering) — same as current state | Bounded downside; imperative phrasing ("read this now") proven in consult-team |
| Inline standards ignored despite explicit phrasing | Behavioral violations for F1/F2/F5 | F2 already failed as numbered list — explicit prohibition language ("do not begin step N+1") is the upgrade. If this also fails, the standard needs enforcement via tooling, not prompt language |
| `/new-project` per-template variant creates confusion | Agent applies wrong operations to wrong template | Operation matrix (COMP-3) makes the mapping explicit and testable |
| BUG-029 batch mode question unresolved for /define | Design gap during /define rewrite | Flag during /define design — the current spec says "each run creates a NEW DIP" but users want batch creation. Design decision, not just a bug fix |
| Scope creep during individual rewrites | Each rewrite expands beyond its bug list | PM identified 4 scope creep risks — agent prompt revision (Q-5), command rename, BUG-029, and Todoist references. All are explicitly bounded or deferred |

### 7.3 Testing Strategy

| Level | Approach | Covers |
|-------|----------|--------|
| Per-skill | Run each rewritten skill end-to-end in a test project | AC-1 through AC-5 for that skill |
| Cross-skill | Run the full Specify → Design → Build workflow | Skill-to-skill handoffs, template output consumed by downstream skills |
| Regression | Compare against bug disposition table | AC-6 — all 35 in-scope bugs addressed |
| Pattern validation | Run `/charter` first, verify behavioral standards hold, then proceed | AC-7 — charter as pattern-setter validates the approach before scaling |

---

## 8. Out of Scope

**From Specification (inherited):**
- `/deliver` command — separate Python-based process, own spec later
- `/breakdown` command — task management service integration, own spec later
- All `/deliver`-specific bugs (BUG-038, BUG-039, BUG-044, BUG-045, BUG-046)
- Platform limitation bugs (BUG-040, BUG-041) — not addressable by skill rewrites
- Plugin/skill format long-term migration beyond the 6 in-scope rewrites
- New features not required to address a documented bug

**Design-Specific Exclusions:**
- Agent prompt revision (Q-5) — separate workstream, does not block skill rewrites
- Command rename (describe/design/do) — deferred to implementation phase, per-skill decision
- Todoist replacement selection — abstracted away; replacement is a future decision
- Template file modifications — templates are consumed, not rewritten, by this design
- `consult-team` and `agent-authoring` skills — existing skills, not in scope for rewrite

---

## 9. Open Questions

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| DQ-1 | Should `/define` support batch DIP creation? | Open | BUG-029 flagged this. Current spec says one-per-run. Users naturally want batch. Design decision needed during `/define` rewrite — not blocking other skills. |
| DQ-2 | Should existing `.claude/commands/` files be deleted after skills are validated? | Open | Recommend retaining during transition, removing after full workflow validation. |
| DQ-3 | Does the `command-standards.md` authoring reference need to exist at MVP? | Open | It's documentation for UC-2 (new skill authoring). Could be deferred until someone actually writes a new skill. The inline standards in each SKILL.md are the runtime source of truth. |
| DQ-4 | Which skill frontmatter capabilities should the rewrites leverage? | Open | Skills support fields beyond `name` and `description` — potentially `allowed-tools` (restrict tool access), named arguments, and per-step success criteria. Need PE input on what capabilities exist and which are relevant per skill. `/new-project` is the strongest candidate for `allowed-tools` restriction (destructive operations). Resolution will add a DEC-7 to this design. |
| DQ-5 | Should template standardization be addressed now or deferred? | Open | The user identified that templates themselves could benefit from standardization (consistent metadata tables, HTML comment style, section IDs). This is a valid concern but separate from SPEC-004's scope (which is about command behavior, not template structure). Recommend deferring to a future spec unless it blocks the rewrites. |

---

## 10. Appendices

### A. Glossary

| Term | Definition |
|------|------------|
| Skill | A directory-based prompt specification under `.claude/skills/` containing a SKILL.md and optional supporting files |
| Command | The prototype format under `.claude/commands/` — flat markdown files, being replaced by skills |
| Mechanical standard | A behavioral rule that can be stated as a terse imperative ("do X, not Y") and survives inline |
| Judgment standard | A behavioral rule requiring operational context ("apply X considering Y and Z") that needs a shared reference |
| Phase boundary | The point in a skill's execution where a new phase begins (Pre-Flight → Gather → Generate → etc.) |
| Template-producing skill | A skill that gathers user input and generates output from a `.praxisity/templates/` file |
| Execution skill | A skill that runs a process (DIP execution, project initialization) rather than producing template-based output |
| Permitted operation | One of the 6 defined Edit operations allowed on template copies (COMP-3) |
| Completion gate | The structural element between Post-Save and Success Message enforcing PLANNING.md update |

### B. References

- [SPEC-004: Command Behavioral Fixes and Pattern Standards](../specs/004-command-fixes-and-patterns.md)
- [Bug Report: v0.5.0 end-to-end test results](../references/new-project-bug-report.md)
- [SESSION-4-1-26 reviews](../reviews/SESSION-4-1-26/) — 9-agent parallel review
- [SESSION-4-3-26 reviews](../reviews/SESSION-4-3-26/) — Mode 3 collaborative design
- [consult-team skill](../../.claude/skills/consult-team/) — structural reference for skill directory pattern
- [CHARTER.md](../../CHARTER.md) — project governance

### C. Bug-to-Component Mapping

| Bug Range | Command | Component(s) | Notes |
|-----------|---------|---------------|-------|
| BUG-001–006 | /new-project | COMP-2 (skill structure) | Command-specific cleanup items |
| BUG-007–009 | /new-project | COMP-3 (template handling) | REQ-F1 pattern class |
| BUG-010–011, 013, 015 | /charter | COMP-2 (skill structure) | Command-specific gathering items |
| BUG-012 | /charter | COMP-5 (gathering protocol) | REQ-F3 pattern class |
| BUG-014 | /charter | COMP-6 (completion protocol) | REQ-F4 pattern class |
| BUG-016 | /charter | COMP-4 (pre-flight protocol) | REQ-F2 pattern class |
| BUG-017 | /spec | COMP-4 (pre-flight protocol) | REQ-F2 pattern class |
| BUG-018 | /spec | COMP-5 (gathering protocol) | REQ-F3 pattern class |
| BUG-019, 022 | /spec | COMP-2 (skill structure) | Command-specific |
| BUG-020 | /spec | COMP-3 (template handling) | REQ-F1 pattern class |
| BUG-021 | /spec | COMP-6 (completion protocol) | REQ-F4 pattern class |
| BUG-023–027 | /architect | COMP-2 (skill structure) | All command-specific |
| BUG-028–030 | /define | COMP-2 (skill structure) | Command-specific |
| BUG-031 | /define | COMP-3 (template handling) | REQ-F1a pattern class |
| BUG-032 | /define | COMP-6 (completion protocol) | REQ-F4 pattern class |
| BUG-033, 035 | /build | COMP-2 (skill structure) | Command-specific |
| BUG-034 | /build | COMP-5 (gathering protocol) | REQ-F3 pattern class (execution variant) |
| BUG-036, 042 | /build | COMP-6 (completion protocol) | REQ-F5 pattern class |
| BUG-037, 043 | /build | COMP-6 (completion protocol) | REQ-F4 pattern class |
| ISSUE-001 | framework | COMP-3, DEC-4 | Resolved by table row adjustment operation #6 |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-04-03 | Designer Agent | Initial draft — Mode 3 collaborative team session |
| 0.2 | 2026-04-03 | Designer Agent | Added DEC-5 (template location), DQ-4 (skill frontmatter), DQ-5 (template standardization). Renumbered DEC-5→DEC-6. Incorporated user feedback on template bundling. |

---
