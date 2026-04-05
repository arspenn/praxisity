# Design: DESIGN-005 Command Behavioral Fixes and Pattern Standards

## Metadata

| Field | Value |
|-------|-------|
| Design ID | DESIGN-005 |
| Title | Command Behavioral Fixes and Pattern Standards |
| Status | Draft |
| Author | Designer Agent (Mode 3 collaborative team) + Lead Agent |
| Created | 2026-04-03 |
| Last Updated | 2026-04-04 |

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

This design transforms 5 Praxisity workflow commands from prototype `.claude/commands/*.md` files into self-contained, directory-based skills under `.claude/skills/`. Each skill bundles its own template and applies codified behavioral standards extracted from the v0.5.0 bug report.

Behavioral standards are delivered in two ways: 4 mechanical standards (F1, F2, F4, F5) are embedded inline at phase boundaries within each skill. The 1 judgment standard (F3 gathering protocol) is implemented as a standalone auto-invokable support skill (`/gather`) — because inline F3 was already present in prototypes and was defeated (BUG-018), and the gathering protocol benefits every development session, not just workflow skill execution. A development template (`.praxisity/templates/skill-standards.template.md`) documents all standards for UC-2 (new skill authoring) but is never loaded during skill execution.

**Workflow skills** (user-invoked, `disable-model-invocation: true`):
- **`/charter`** — create or update project charter (pattern-setter, built first)
- **`/describe`** (née `/spec`) — create a specification document
- **`/design`** (née `/architect`) — create a design document for a specification
- **`/plan`** (née `/define`) — generate implementation prompts (DIPs) from a design
- **`/do`** (née `/build`) — execute a DIP with step verification

**Support skills** (auto-invokable, used by the agent during workflow execution):
- **`/gather`** — structured one-at-a-time gathering protocol for user input (REQ-F3). Built first for immediate bootstrapping benefit.
- **`/consult-team`** — multi-perspective agent consultation (existing)
- **`/agent-authoring`** — agent definition file creation (existing)

### 1.2 Design Principles

- **Self-contained skills:** Each skill bundles its template and everything it needs. No reaching across the repo to distant directories. Aligns with Anthropic's skill format examples and distribution model.
- **Inline mechanical standards, skill-based judgment standards:** Mechanical standards (F1, F2, F5) are embedded inline. The gathering protocol (F3) is a standalone support skill (`/gather`) — auto-invokable, reusable across all workflow skills and development sessions. This eliminates both inline duplication and cross-file references.
- **Phase-gated placement:** Standards appear at the phase boundary where they apply, not at the top of the file.
- **Bootstrapping:** `/charter` is built first as the pattern-setter. It validates the standards approach before the remaining 4 skills are written. Then each subsequent skill can be specified using `/describe` — the framework building itself.

### 1.3 Requirements Coverage

| Requirement | Design Section | Approach |
|-------------|----------------|----------|
| REQ-F1 | COMP-3, DEC-4 | Copy-then-edit protocol with 6 permitted operations, inline at Generate phase |
| REQ-F1a | COMP-3 | N/A marking as permitted operation #4 |
| REQ-F2 | COMP-4 | Sequential execution constraint inline at Pre-Flight phase |
| REQ-F3 | COMP-5 | `/gather` support skill — auto-invokable, loaded by platform during gathering phases |
| REQ-F4 | COMP-6 | Per-skill success message checklist (each skill defines its own elements) |
| REQ-F5 | COMP-6 | One-line imperative between Post-Save and Success Message (Completion Gate) |
| REQ-F7 | DEC-4, COMP-3 | Resolved by operation #6 (table row adjustment) — template example counts are illustrative, not prescriptive |
| REQ-N1 | DEC-1, DEC-6 | Full rewrites as skills; charter first as pattern-setter; bootstrapping approach |
| REQ-N2 | COMP-3 (note) | Bug disposition table in bug report complete (26 bugs + 1 issue in scope) |

---

## 2. Architecture

### 2.1 System Context

```
.claude/
├── skills/
│   ├── _shared/
│   │   └── (reserved for future cross-skill resources if needed)
│   ├── gather/
│   │   └── SKILL.md                   ← support skill: structured gathering protocol (REQ-F3)
│   ├── charter/
│   │   ├── SKILL.md                   ← full rewrite of /charter command
│   │   └── templates/
│   │       └── charter.template.md    ← bundled template
│   ├── describe/
│   │   ├── SKILL.md                   ← full rewrite of /spec command
│   │   └── templates/
│   │       └── spec.template.md       ← bundled template
│   ├── design/
│   │   ├── SKILL.md                   ← full rewrite of /architect command
│   │   └── templates/
│   │       └── design.template.md     ← bundled template
│   ├── plan/
│   │   ├── SKILL.md                   ← full rewrite of /define command
│   │   └── templates/
│   │       └── dip.template.md        ← bundled template
│   ├── do/
│   │   └── SKILL.md                   ← full rewrite of /build command (no template)
│   ├── consult-team/                  ← existing (unchanged)
│   └── agent-authoring/               ← existing (unchanged)
│
├── commands/                          ← existing prototypes (retained as reference during rewrites)
```

### 2.2 Architecture Pattern

**Pattern:** Self-contained skill-per-command with bundled templates and shared behavioral constraints.

**Rationale:** Each workflow command becomes a self-contained skill directory bundling its SKILL.md and its output template. Skills are the platform's documented extension format — `/init` creates skills, not commands. Bundling templates eliminates cross-repo indirection and supports distribution (individual skills can be installed independently). Behavioral standards are delivered at phase boundaries, with the gathering protocol (F3) implemented as an auto-invokable support skill (`/gather`).

**Trade-offs:**
- Pros: Fully self-contained, distributable, no distant path references, platform-aligned
- Cons: Templates are duplicated from `.praxisity/templates/` (one-time copy during migration). ~8-12 lines of inline standard text duplicated across 5 skills.

### 2.3 Two Structural Families

The 5 skills divide into two families based on their phase structure:

**Template-producing skills** (charter, describe, design, plan):
```
Pre-Flight → Gather → Generate-from-template → Post-Save → Completion Gate → Success Message
```
All 5 behavioral standards apply. These skills share the full skeleton and differ in gathering content and template.

**Execution skill** (do):
```
Pre-Flight → DIP-Execution → Completion Gate → Success Message
```
Standards apply selectively:

| Standard | charter | describe | design | plan | do |
|----------|---------|----------|--------|------|-----|
| REQ-F1 (template handling) | yes | yes | yes | yes | N/A |
| REQ-F2 (sequential pre-flight) | yes | yes | yes | yes | yes |
| REQ-F3 (gathering) | yes | yes | yes | yes | N/A |
| REQ-F4 (success message) | yes | yes | yes | yes | yes |
| REQ-F5 (PLANNING.md gate) | yes | yes | yes | yes | yes |

---

## 3. Components

### COMP-1: Standards Delivery System

**Purpose:** Deliver behavioral standards to each skill at the right phase with maximum AI reliability.

**Satisfies:** REQ-F1, REQ-F2, REQ-F3, REQ-F4, REQ-F5 (delivery mechanism for all)

**Responsibilities:**
- Classify standards as mechanical (inline) or judgment (support skill)
- Embed mechanical standards at phase boundaries in each SKILL.md
- Provide support skill (`/gather`) for the judgment standard (F3 gathering protocol)
- Provide human-readable authoring reference for UC-2 (new skill creation)

**Dependencies:**
- `.claude/skills/gather/SKILL.md` (support skill for REQ-F3, auto-invokable)
- `.praxisity/templates/skill-standards.template.md` (human authoring reference template for UC-2)

**Key Design Decisions:**
- Mechanical standards inline, judgment standard as support skill (DEC-2)
- Phase-gated placement — inline standards appear at the boundary where they apply
- The architectural distinction: mechanical = "do X, not Y" (survives as terse imperative). Judgment = "apply X considering Y and Z" (needs operational context as a reusable skill). REQ-F3 is the only judgment standard.
- Two skill types: workflow skills (user-invoked, `disable-model-invocation: true`) and support skills (auto-invokable, agent uses as tools)

**Standard locations:**

| Standard | Delivery | Location |
|----------|----------|----------|
| REQ-F2 | Inline | Top of Pre-Flight section (~2 lines) |
| REQ-F1 | Inline | Top of Generate section (~3 lines) |
| REQ-F3 | Support skill | `/gather` skill auto-invoked during gathering phases |
| REQ-F5 | Inline | Between Post-Save and Success Message (~1 line) |
| REQ-F4 | Per-skill | Within Success Message section (unique per skill) |

---

### COMP-2: Skill File Structure

**Purpose:** Define the directory layout and file structure for each rewritten skill.

**Satisfies:** REQ-N1 (full rewrites as skills)

**Responsibilities:**
- Each skill is a directory under `.claude/skills/` containing a `SKILL.md` and bundled template(s)
- SKILL.md contains YAML frontmatter followed by structured sections
- Templates bundled in `templates/` subdirectory within each skill
- Shared resources live under `_shared/`
- Existing `.claude/commands/*.md` files retained during transition as prototype reference

**Dependencies:**
- Claude Code skills platform (directory-based loading)
- Existing `consult-team` skill as proven structural reference

**Skill frontmatter:**

```yaml
---
name: [skill-name]
description: [one-line description]
# Additional capabilities leveraged per-skill:
# allowed-tools: [restrict tools for safety — e.g., /do may need Bash, /charter may not]
# disable-model-invocation: true  # for destructive skills only
# argument-hint: [describe expected arguments]
---
```

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
[The /gather support skill auto-invokes here via platform context matching]
[Section-by-section gathering — one at a time per /gather protocol]

### Review and Confirm
[Structured review with y/e/c options]

## Generate [Output Type]
[REQ-F1 inline standard]
1. Copy template via cp...
2. Read the copy...
3. Edit to populate...

## Post-Save
[Optional: task manager integration, git commit]

## Completion Gate
[REQ-F5 inline standard — PLANNING.md hard gate]

## Success Message
[REQ-F4 per-skill checklist]

## Behavior Notes
[Skill-specific behavioral guidance]
```

---

### COMP-3: Template Handling Protocol

**Purpose:** Define how skills interact with their bundled template files to produce deterministic output.

**Satisfies:** REQ-F1, REQ-F1a, REQ-F7

**Responsibilities:**
- Enforce copy-then-edit pattern for all template-derived output
- Define permitted Edit operations (closed list — anything not listed is not permitted)
- Handle dual-use template lifecycle (read for gathering context, copy for generation)

**Dependencies:**
- Each skill's `templates/` subdirectory
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
| 6 | Table row adjustment | Add or remove rows in ID-tracked tables to match gathered content count exactly. Template example row counts are illustrative, not prescriptive. Generate sequential IDs. |

**NOT permitted:**
- Rewriting existing template prose
- Adding sections not present in the template
- Restructuring section order
- Paraphrasing or summarizing template language

**Dual-use template lifecycle:**
1. **During Gather phase:** Read the bundled template (with HTML comments intact) as a reference for section structure, examples, and domain-specific prompts. The comments are the gathering guide.
2. **During Generate phase:** `cp` the template from the skill's `templates/` directory to the destination path. Read the fresh copy. Apply permitted Edit operations. The bundled template is never modified.

---

### COMP-4: Pre-Flight Protocol

**Purpose:** Ensure consistent pre-flight behavior across all skills.

**Satisfies:** REQ-F2

**Common pre-flight steps (all skills):**

| Step | Action | Notes |
|------|--------|-------|
| 1 | Read PLANNING.md for session context; create if missing | First step, always |
| 2 | Update PLANNING.md with this skill as active command | Hard gate — must complete before step 3 |
| 3+ | Skill-specific checks | Varies per skill |

**Inline standard text (embedded at top of each Pre-Flight section):**

> Execute these steps sequentially in the order listed. Do not begin step N+1 until step N is complete. Do not batch or parallelize pre-flight steps.

---

### COMP-5: Gathering Protocol (Support Skill)

**Purpose:** Prevent batched gathering by codifying the one-at-a-time prompting protocol as a reusable, auto-invokable support skill.

**Satisfies:** REQ-F3

**Implementation:** `.claude/skills/gather/SKILL.md` — a standalone support skill. Auto-invocation via platform `description`-based context matching.

**Why a skill, not inline or a shared file:**
- Inline "one section at a time" was already present in prototype commands and was defeated (BUG-018). A terse inline rule is the pattern that already failed.
- A shared file requires cross-references, which we've established are unreliable.
- A support skill is auto-invoked by the platform based on context matching — no cross-reference needed. The agent loads the gathering protocol when it needs it, the same way it loads consult-team when it needs multi-agent review.
- Building it as a skill gives immediate benefit — every session from this point forward uses the protocol, not just workflow skill executions.
- The gathering protocol can be developed, tested, and improved independently from the workflow skills.

**Skill type:** Support skill (auto-invokable). Workflow skills are `disable-model-invocation: true` (user-invoked only). Support skills like `/gather`, `/consult-team`, and `/agent-authoring` are auto-invokable — the agent uses them as tools.

**Applicability:** Any session where structured input is gathered from the user across multiple sections or categories. This includes workflow skill execution (charter, describe, design, plan) and general development work. Does NOT apply to `/do` — its DIP execution steps are agent-driven, not user-input gathering.

---

### COMP-6: Completion Protocol

**Purpose:** Ensure consistent completion behavior — PLANNING.md gating and complete success messages.

**Satisfies:** REQ-F4, REQ-F5

**REQ-F5 inline standard (Completion Gate — between Post-Save and Success Message):**

> Update PLANNING.md with completion status, active artifacts, and next steps. This is a hard gate — do not display the success message until PLANNING.md has been updated in this run.

**REQ-F4 approach:** Each skill defines its own success message checklist. The design specifies the structure, not the content:

```markdown
## Success Message

Show all of the following:
- [ ] [Element 1 specific to this skill]
- [ ] [Element 2 specific to this skill]
- [ ] Next steps:
  1. [Step 1]
  2. [Step 2]
```

**Post-Save section restructuring:** In prototype commands, PLANNING.md update was buried as step 3-4 inside Post-Save, after optional Todoist/git steps. The Completion Gate is a new structural element that physically separates Post-Save from Success Message:

```
## Post-Save
1. Optional: create task in project task management service (if available)
2. Optional: commit to git with conventional format

## Completion Gate
Update PLANNING.md with completion status. Do not proceed until this is done.

## Success Message
[per-skill checklist]
```

---

## 4. Interfaces
### INT-1: Workflow Skill ↔ Gather Support Skill

**Connects:** Workflow skills with gathering phases (COMP-2) ↔ `/gather` skill (COMP-5)

**Type:** Platform auto-invocation via `description`-based context matching

**Contract:**
- **Trigger:** Agent is gathering structured input from the user across multiple sections — the `/gather` skill's `description` matches this context
- **Mechanism:** Platform loads the gathering skill's instructions automatically, not via explicit cross-reference
- **Failure mode:** If auto-invocation doesn't fire, the agent falls back to its default gathering behavior (which may batch). Bounded downside — same as current state. Workflow skills can also reference `/gather` explicitly as a fallback.
- **Applicability:** Workflow skills with user-input gathering (charter, describe, design, plan). Not `/do`.

### INT-2: Skill ↔ Bundled Templates

**Connects:** Each template-producing SKILL.md (COMP-2) ↔ its `templates/*.template.md` (COMP-3)

**Type:** File read + file copy + file edit

**Contract:**
```
Phase 1 (Gather): Read bundled template → extract section structure, examples, prompts
Phase 2 (Generate):
  1. cp templates/[name].template.md → destination    (Bash cp)
  2. Read destination                                  (Read tool)
  3. Edit destination                                  (Edit tool, permitted operations only)
  4. Verify: bundled template unchanged                (implicit — cp creates the copy)
```

### INT-3: Skill ↔ PLANNING.md

**Connects:** Each SKILL.md (COMP-2) ↔ PLANNING.md

**Contract:**
```
Pre-Flight Step 1: Read PLANNING.md (or create if missing)
Pre-Flight Step 2: Write — set active skill
Completion Gate:   Write — set completion status, artifacts, next steps
                   MUST complete before Success Message is displayed
```

**Touchpoints per skill execution:** Exactly 3 — read at start, write at step 2, write at completion gate.

---

## 5. Data Model

### DATA-1: Skill Directory

| Component | Required | Description |
|-----------|----------|-------------|
| `SKILL.md` | Yes | The complete behavioral specification |
| `templates/` | Template-producing skills only | Bundled output template(s) |

### DATA-2: Gather Support Skill (SKILL.md)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| YAML frontmatter | metadata | Yes | `name`, `description` (platform uses description for auto-invocation context matching) |
| Preferences | section | Yes | Memory check + first-run calibration (REQ-G8/G9) |
| The Rule | section | Yes | Core one-at-a-time rule |
| How to Gather Each Section | section | Yes | Step-by-step gathering procedure |
| When Drafting is Permitted | section | Yes | Observable drafting gate |
| Before You Send | section | Yes | Pre-send verification checklist (replaces prohibitions) |
| Handling Sub-Sections | section | Yes | Per-sub-category prompting |
| Handling Skip Requests | section | Yes | Skip and "fill in the rest" behavior with explicit example |

Self-contained skill — no cross-references to other files. See DESIGN-006 for full component breakdown.

### DATA-3: Skill Standards Template (Human Authoring Guide)

`.praxisity/templates/skill-standards.template.md` — a Praxisity template documenting the behavioral standards (F1-F5), mechanical vs. judgment classification, phase-gate placement rules, and permitted edit operations. For human developers writing new skills. Not read by AI at runtime.

---

## 6. Design Decisions

### DEC-1: Skills Format Over Commands

**Decision:** Migrate to skills under `.claude/skills/[name]/SKILL.md`.

**Rationale:** Platform evidence confirms commands are legacy — not listed as extension point, `/init` creates skills, skills support `allowed-tools`, `disable-model-invocation`, named arguments, and per-step success criteria. Skills are directory-based, enabling bundled templates and supporting files.

### DEC-2: Standards Delivery — Inline Mechanical, Skill-Based Judgment

**Decision:** Inline mechanical standards (F1, F2, F5) at phase boundaries. Judgment standard (F3 gathering protocol) implemented as a standalone auto-invokable support skill (`/gather`). Per-skill for F4 success messages.

**Rationale:**
- **Mechanical standards** (F1, F2, F5): 2-4 lines each, "do X not Y" rules that survive as inline imperatives.
- **Judgment standard** (F3): Inline "one section at a time" was already in prototypes and was defeated (BUG-018). A support skill provides the operational context AND is reusable across all sessions — not just workflow skill execution. The gathering protocol benefits every development session, making it a natural skill rather than embedded documentation.
- **Per-skill standard** (F4): Each skill's success message is unique.
- **Two skill types:** Workflow skills are user-invoked (`disable-model-invocation: true`). Support skills (gather, consult-team, agent-authoring) are auto-invokable — the agent uses them as tools.

### DEC-3: Todoist Abstraction to Generic Task Manager

**Decision:** Abstract all Todoist references to generic "project task management service (if available)." Remove hardcoded MCP tool names.

**Rationale:** Three coupling types identified:
1. **Post-save convenience** (charter, describe, design): abstract to generic
2. **Input source** (plan): abstract to "task from project task manager"
3. **Completion signal** (do): abstract to "mark task complete in project task management service"

### DEC-4: Permitted Edit Operations (Closed List)

**Decision:** 6 permitted operations. Anything not listed is not permitted.

**The 6 operations:** Placeholder substitution, domain section removal, HTML comment stripping, N/A marking, content population, table row adjustment. (Full definitions in COMP-3.)

**NOT permitted:** Rewriting prose, adding sections, restructuring order, paraphrasing.

### DEC-5: Templates Bundled in Skill Directories

**Decision:** Each skill bundles its own template in a `templates/` subdirectory. Templates are copied from `.praxisity/templates/` during the migration.

**Rationale:**
- Skills should be self-contained — bundling matches Anthropic's skill examples and the consult-team skill pattern
- Eliminates cross-repo indirection (no distant `.praxisity/templates/` references)
- Supports distribution model — individual skills can be installed with their templates
- Reduces conceptual cross-referencing before Obsidian support is developed
- `/new-project` (which shared `charter.template.md`) is dropped from scope, so the sharing concern is moot

**Two template locations by audience:**
- **`.praxisity/templates/`** — development templates (framework infrastructure, consumed by developers building the framework). E.g., `skill-standards.template.md`.
- **`.claude/skills/[name]/templates/`** — end-user templates (output structure, consumed by the skill during execution). E.g., `charter.template.md` bundled with the `/charter` skill.

**Consequences:**
- Each skill references its template via a short relative path: `templates/charter.template.md`
- `.praxisity/templates/` retains development-facing templates and remains the canonical source for `/new-project` if it's ever revived

### DEC-6: Implementation Order — Charter First, Bootstrapping Approach

**Decision:** Build `/charter` first as the pattern-setter. Then use `/describe` to formally specify remaining skills through the framework's own workflow.

**Order:** charter → describe → design → plan → do

**Rationale:**
- `/charter` is the simplest gathering flow (8 sections, no traceability IDs) and validates the standards approach
- Building `/charter` first gives immediate utility — it can be used to update the project charter
- `/describe` is built second, then used to specify the remaining 3 skills (bootstrapping principle: use the system to build the system)
- `/do` has a unique execution model (DIP runner) and comes last

### DEC-7: Skill Frontmatter Capabilities

**Decision:** Leverage skill-specific frontmatter fields where they add safety or clarity.

| Skill | `allowed-tools` | `disable-model-invocation` | `argument-hint` |
|-------|-----------------|---------------------------|-----------------|
| charter | Read, Write, Edit, Glob, Grep | no | — |
| describe | Read, Write, Edit, Glob, Grep | no | — |
| design | Read, Write, Edit, Glob, Grep | no | `<spec-number>` |
| plan | Read, Write, Edit, Glob, Grep | no | `<design-component or task>` |
| do | Read, Write, Edit, Glob, Grep, Bash | no | `<dip-path>` |

Note: `allowed-tools` and other advanced frontmatter fields need empirical testing during the `/charter` build to verify platform behavior.

---

### DEC-8: Memory-as-Settings Pattern

**Decision:** Skills that need per-project configuration use the Claude Code agent SDK main project memory system as their settings store, following the official memory tool documentation.

**Pattern:**
1. On every invocation, check project memory for relevant preferences
2. If found → load and apply silently
3. If not found → first invocation; run calibration as a natural part of the workflow flow, store results to project memory via MEMORY.md
4. Preferences persist across sessions, subagent calls, and skill invocations

**Rationale:** Solves the "settings and config files for prompt-based systems" problem without custom infrastructure. The agent memory system is platform-provided, always loaded into sessions, and follows a documented format. First identified during SPEC-006 (`/gather` skill calibration) but applicable to any skill needing per-project configuration.

**First consumer:** `/gather` skill (REQ-G8, REQ-G9) — calibrates gathering strictness and user experience level on first use, loads preferences on subsequent runs.

**Consequences:**
- No config files, settings panels, or custom persistence backends
- Preferences are transparent (stored as readable markdown in project memory)
- Other skills can read gathering preferences to adapt their own behavior (e.g., `/charter` adjusting example verbosity based on user experience level)
- Pattern should be documented in the skill-standards development template for UC-2

---

## 7. Implementation Considerations

### 7.1 Implementation Order

| Order | Skill | Notes |
|-------|-------|-------|
| 0 | `/gather` (support skill) | Build first — immediate bootstrapping benefit for all sessions |
| 0 | `.praxisity/templates/skill-standards.template.md` | Human authoring reference template (deferrable — DQ-3) |
| 1 | `/charter` | Pattern-setter; simplest; validates approach; uses `/gather` |
| 2 | `/describe` | Adds traceability IDs; then used to specify remaining skills |
| 3 | `/design` | Most complex gathering; domain-aware sections |
| 4 | `/plan` | Depends on design output format; BUG-029 batch question |
| 5 | `/do` | Unique execution model; only F2/F4/F5 apply |

### 7.2 Migration Steps

1. Build `/gather` support skill (already created as prototype — iterate based on review)
2. For each workflow skill in order: create directory, bundle template from `.praxisity/templates/`, write SKILL.md
3. Retain `.claude/commands/` originals as reference during transition
4. After all 5 workflow skills validated end-to-end, remove old command files

### 7.3 Risk Areas

| Risk | Impact | Mitigation |
|------|--------|------------|
| Gathering standards file not read by agent | F3 violations — same as current state | Bounded downside; imperative phrasing proven in consult-team |
| Inline standards ignored despite explicit phrasing | Behavioral violations for F1/F2/F5 | Explicit prohibition language is the upgrade over numbered lists. If this also fails, enforcement via tooling needed |
| BUG-029 batch mode question unresolved for /plan | Design gap during /plan rewrite | Flag during /plan design — design decision, not just a bug fix |
| Skill frontmatter fields don't work as expected | Features like `allowed-tools` may not behave as documented | Test during /charter build before relying on them |
| Template drift between bundled copies and .praxisity/ originals | Inconsistency if both are maintained | `.praxisity/templates/` is canonical source for `/new-project` only; skill-bundled copies are authoritative for their skill |

### 7.4 Testing Strategy

| Level | Approach | Covers |
|-------|----------|--------|
| Per-skill | Run each rewritten skill end-to-end in a test project | AC-1 through AC-5 for that skill |
| Cross-skill | Run the full Describe → Design → Plan → Do workflow | Skill-to-skill handoffs |
| Regression | Compare against bug disposition table | AC-6 — all 26 in-scope bugs addressed |
| Pattern validation | Run `/charter` first, verify standards hold, then proceed | AC-7 — charter as pattern-setter validates approach |

---

## 8. Out of Scope

**From Specification (inherited):**
- `/new-project` command — sunset candidate pending distribution model decision
- `/deliver` command — separate Python-based process
- `/breakdown` command — task management service integration
- All deferred bugs (BUG-001–009, BUG-038–039, BUG-040–041, BUG-044–046)
- New features not required to address a documented bug

**Design-Specific Exclusions:**
- Agent prompt revision (Q-5) — separate workstream, does not block skill rewrites
- Todoist replacement selection — abstracted away
- Template standardization ("template for templates") — valid future concern, deferred
- `consult-team` and `agent-authoring` skills — existing skills, not in scope for rewrite

---

## 9. Open Questions

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| DQ-1 | Should `/plan` support batch DIP creation? | Open | BUG-029 flagged this. Current spec says one-per-run. Design decision during `/plan` rewrite. |
| DQ-2 | Should existing `.claude/commands/` files be deleted after skills are validated? | Open | Recommend retaining during transition, removing after full workflow validation. |
| DQ-3 | Does the `command-standards.md` authoring reference need to exist at MVP? | Open | Could be deferred until someone writes a new skill. |
| DQ-4 | Do skill frontmatter capabilities work as documented? | Open | `allowed-tools`, `disable-model-invocation`, named arguments need empirical testing during `/charter` build. |

---

## 10. Appendices

### A. Glossary

| Term | Definition |
|------|------------|
| Skill | A directory-based prompt specification under `.claude/skills/` containing a SKILL.md and optional supporting files |
| Command | The prototype format under `.claude/commands/` — flat markdown files, being replaced by skills |
| Mechanical standard | A behavioral rule stated as a terse imperative ("do X, not Y") — survives inline |
| Judgment standard | A behavioral rule requiring operational context ("apply X considering Y and Z") — needs shared reference |
| Phase boundary | The point where a new phase begins (Pre-Flight → Gather → Generate → etc.) |
| Template-producing skill | A skill that gathers user input and generates output from a bundled template |
| Execution skill | A skill that runs a process (DIP execution) rather than producing template-based output |
| Completion gate | Structural element between Post-Save and Success Message enforcing PLANNING.md update |

### B. Bug-to-Component Mapping

| Bug Range | Skill | Component(s) | Notes |
|-----------|-------|---------------|-------|
| BUG-010–011, 013, 015 | /charter | COMP-2 | Command-specific gathering items |
| BUG-012 | /charter | COMP-5 | REQ-F3 pattern class |
| BUG-014 | /charter | COMP-6 | REQ-F4 pattern class |
| BUG-016 | /charter | COMP-4 | REQ-F2 pattern class |
| BUG-017 | /describe | COMP-4 | REQ-F2 pattern class |
| BUG-018 | /describe | COMP-5 | REQ-F3 pattern class |
| BUG-019, 022 | /describe | COMP-2 | Command-specific |
| BUG-020 | /describe | COMP-3 | REQ-F1 pattern class |
| BUG-021 | /describe | COMP-6 | REQ-F4 pattern class |
| BUG-023–027 | /design | COMP-2 | All command-specific |
| BUG-028–030 | /plan | COMP-2 | Command-specific |
| BUG-031 | /plan | COMP-3 | REQ-F1a pattern class |
| BUG-032 | /plan | COMP-6 | REQ-F4 pattern class |
| BUG-033, 035 | /do | COMP-2 | Command-specific |
| BUG-034 | /do | COMP-5 | REQ-F3 pattern class (execution variant) |
| BUG-036, 042 | /do | COMP-6 | REQ-F5 pattern class |
| BUG-037, 043 | /do | COMP-6 | REQ-F4 pattern class |
| ISSUE-001 | framework | COMP-3, DEC-4 | Resolved by table row adjustment operation #6 |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-04-03 | Designer Agent | Initial draft — Mode 3 collaborative team session |
| 0.2 | 2026-04-03 | Designer Agent | Added DEC-5 (template location), DQ-4 (skill frontmatter), DQ-5 (template standardization) |
| 0.3 | 2026-04-04 | Lead Agent | Comprehensive update: templates bundled in skill directories (DEC-5 reversed); /new-project dropped (5 skills); renames applied (describe, charter, design, plan, do); charter first with bootstrapping (DEC-6); DEC-7 added (skill frontmatter); bug counts updated (26+1) |
| 0.4 | 2026-04-04 | Lead Agent | F3 gathering protocol elevated from shared file to standalone support skill (`/gather`). Two skill types introduced: workflow (user-invoked) and support (auto-invokable). `/gather` built first for immediate bootstrapping benefit. Shared `_shared/gathering-standards.md` removed from architecture. |
| 0.5 | 2026-04-04 | Lead Agent | Post-review propagation: all stale "shared file" references updated to "support skill"; DATA-2 updated from file schema to SKILL.md schema; DEC-8 added (memory-as-settings pattern); migration steps updated; BUG-034 removed from gather scope |

---