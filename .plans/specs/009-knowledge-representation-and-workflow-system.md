# Specification: SPEC-009 Knowledge Representation and Workflow System

## Metadata

| Field | Value |
|-------|-------|
| Spec ID | SPEC-009 |
| Title | Knowledge Representation and Workflow System |
| Status | Shelved |
| Author | Andrew Robert Spenn |
| Created | 2026-05-18 |
| Last Updated | 2026-09-22 |

> **Shelved 2026-09-22.** The diagnosis holds (four workflow skills unbuilt, review output never consolidated), but the remedy — HTML output, a spec-centric folder hierarchy, a provenance-tracked consolidation protocol, and Mode 3 review per skill — is a research program that would delay actual use of the framework by months. Superseded in practice by a narrower plan: build `/describe`, `/design`, `/plan`, `/do` as markdown skills with bundled templates, archive review sprawl without synthesis, and package the framework as a Claude Code plugin for portability. OBJ-1 and OBJ-6 carry forward into that work; OBJ-2 through OBJ-5 and OBJ-7 are deferred indefinitely. SPEC-004 remains the behavioral-standards reference.
| Charter Reference | [CHARTER.md](../../CHARTER.md) — Principles: Dual-use design, Minimal cognitive overhead, Self-documenting, Bootstrapping |

### Related Documents

| Document | Relationship |
|----------|--------------|
| [SPEC-004: Command Behavioral Fixes and Pattern Standards](004-command-fixes-and-patterns.md) | Supersedes — behavioral standards inherited, scope expanded |
| [DESIGN-005: Command Rewrites](../designs/005-command-rewrites.md) | Related to — design decisions carried forward where applicable |
| [Bug Report: v0.5.0 test results](../references/new-project-bug-report.md) | Depends on — primary evidence base |

---

## 1. Problem Statement

Praxisity's workflow produces growing volumes of project artifacts — specifications, designs, DIPs, reviews, and references — currently stored as flat markdown files in type-segregated directories (`.plans/specs/`, `.plans/designs/`, `.plans/reviews/`). At 17,400+ lines across 90+ files, this system has hit three scaling limits:

**Information overload without consolidation.** Mode 3 agent teams produce multiple independent review reports (38% of all content — 6,600 lines across 41 files) that are never distilled into authoritative syntheses. Each new session must re-read and re-synthesize raw reports, burning context on work the AI has already done. Knowledge is re-derived on every query rather than compiled once and kept current.

**Flat markdown limits comprehension.** Markdown provides no information hiding — a 250-line spec must be read linearly. There are no collapsible sections, no visual hierarchy beyond headers, no semantic metadata for agents to efficiently skip irrelevant content. The framework's creator — a power user comfortable with dense text — reports being at their comprehension limit, particularly with Mode 3 output. Less experienced users would struggle far sooner.

**File structure obscures relationships.** Specs, designs, and DIPs are numbered independently in separate directories, causing mismatched numbering (SPEC-005 maps to DESIGN-004; SPEC-004 has seven DIPs). A single spec cannot naturally own multiple designs or DIPs. Reviews are associated with specs only by naming convention. The structure makes it hard to answer "show me everything related to SPEC-005."

Meanwhile, SPEC-004 defined behavioral standards for skill rewrites (pre-flight sequencing, template handling, gathering protocol, success messages) but none of the workflow skills beyond `/charter` have been built. Building them against the current flat-markdown, type-segregated structure would require rebuilding them when the structure changes.

This spec supersedes SPEC-004, inheriting its behavioral standards and combining them with the structural and representational changes needed to build the workflow system right the first time.

---

## 2. Goals and Objectives

### 2.1 Primary Goal

Rebuild Praxisity's workflow system with codified behavioral standards, HTML-based knowledge representation for complex documents, a hierarchical project structure, and a consolidation protocol — designed together so skills are built right the first time.

### 2.2 Objectives

| ID | Objective | Success Metric |
|----|-----------|----------------|
| OBJ-1 | Codify cross-cutting behavioral standards: template copy-then-edit (`cp` then `Edit`, never `Write` from scratch), sequential pre-flight with PLANNING.md as step 2, one-section-at-a-time gathering with draft-for-approval, inapplicable sections marked "N/A — [reason]" not removed, PLANNING.md update as hard gate before success message, complete success messages per each skill's own definition | Standards documented in a form all skills can reference; re-run of v0.5.0 test scenario shows pattern-class bugs eliminated |
| OBJ-2 | Establish HTML with shared CSS as the output format for complex project documents (specs, designs, consolidated reviews), with collapsible sections, semantic metadata, and machine-readable headers | Complex documents open in any browser with zero dependencies; agents can target-read specific sections via metadata |
| OBJ-3 | Consolidate all framework-generated artifacts under `.praxisity/` in a spec-centric hierarchy, with skill templates bundled in their skill directories rather than a separate templates folder. Root-level files (CLAUDE.md, CHARTER.md) placement to be resolved in design. | All framework artifacts live under `.praxisity/` (plus any root files decided in design); a project can gitignore `.praxisity/` to exclude framework output |
| OBJ-4 | Define a consolidation protocol that synthesizes multi-output processes (Mode 3 reviews, research rounds) into authoritative documents with git-based provenance tracking, explicit contradiction preservation, and detectable staleness | Consolidated documents carry source paths and commit hashes; a freshness check can identify stale syntheses |
| OBJ-5 | Define the markdown/HTML boundary — which document types stay markdown (skills, CLAUDE.md, memory, ADRs, DIPs) and which become HTML | Every document type has an explicit format assignment with rationale |
| OBJ-6 | Rewrite all workflow skills (`/describe`, `/design`, `/plan`, `/do`) applying both the behavioral standards and the representational standards simultaneously | All 5 workflow skills built and validated |
| OBJ-7 | Resolve all 46 bugs from the v0.5.0 test run with documented dispositions | Every bug BUG-001 through BUG-046 has a disposition of addressed, deferred, or won't fix |

---

## 3. Requirements

### 3.1 Functional Requirements

**Behavioral Standards**

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-F1 | All skills that use templates shall copy the template file via `cp`, then use Edit for placeholder substitution — never Write from scratch | MUST | Root cause of BUG-020, BUG-009; templates must survive skill execution byte-for-byte |
| REQ-F2 | When a template section does not apply, skills shall mark it "N/A — [reason]" rather than removing it | MUST | BUG-031 — sections silently removed; structure must be preserved for traceability |
| REQ-F3 | All skills shall execute pre-flight steps sequentially in specified order; PLANNING.md update shall be step 2 before any other checks. Steps must not be batched or parallelized | MUST | BUG-016, BUG-017 — numbered lists alone did not prevent parallelization |
| REQ-F4 | All skills that gather user input shall prompt one section at a time, waiting for the user's response before presenting the next. When the agent has sufficient context, it may present a draft for approval rather than prompting from scratch, but must still pause between sections | MUST | BUG-012, BUG-018, BUG-034 — batched gathering across multiple skills |
| REQ-F5 | All skills shall emit every element listed in their own Success Message section. Each skill's "complete" is defined by its own spec, not a uniform template | MUST | BUG-014, BUG-021, BUG-032, BUG-037, BUG-043, BUG-044 — 6 instances |
| REQ-F6 | All skills shall update PLANNING.md as a hard gate before showing the success message | MUST | BUG-036, BUG-042 — updates consistently deferred or skipped |

**HTML Document Format**

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-F7 | Workflow skills that produce complex documents (specs, designs, consolidated reviews) shall output HTML files referencing a shared `praxisity.css` stylesheet | MUST | Core format change — enables collapsibility, visual hierarchy, semantic structure |
| REQ-F8 | HTML documents shall use `<details>/<summary>` elements for section-level collapsibility | MUST | Information hiding — both humans and agents see structure first, drill into detail on demand |
| REQ-F9 | HTML documents shall include machine-readable metadata (`<meta>` tags) for document type, status, ID, and dependencies | MUST | Enables agent pre-flight checks to assess document relevance without reading full content |
| REQ-F10 | Core HTML document viewing shall require no JavaScript. CSS-only styling and interaction (collapsible sections, layout, color coding) | MUST | Zero-dependency constraint — any browser, no build step, no server |
| REQ-F11 | A single shared `praxisity.css` file shall provide consistent styling across all HTML documents including status badges, section layout, and print-friendly rendering | MUST | Design system consistency without per-document styling |

**File Structure**

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-F12 | All framework-generated artifacts shall be organized under `.praxisity/` in a spec-centric hierarchy where each spec folder owns its designs, DIPs, reviews, and references | MUST | Co-location answers "show me everything for SPEC-X" with one directory listing |
| REQ-F13 | Skill templates shall be bundled within their respective skill directories (`.claude/skills/<skill>/`), not in a separate templates folder | MUST | Templates travel with the skill that uses them; eliminates orphaned template problem |
| REQ-F14 | Document numbering within a spec folder shall be independent — a spec may have multiple designs and multiple DIPs without requiring cross-type number alignment | MUST | Current flat numbering forces artificial 1:1 mapping between specs, designs, and DIPs |

**Consolidation Protocol**

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-F15 | Multi-output processes (Mode 3 reviews, research rounds) shall produce a consolidated synthesis document in addition to individual raw outputs | MUST | 41 review files (6,600 lines) exist with no synthesis; knowledge re-derived every session |
| REQ-F16 | Consolidated syntheses shall preserve contradictions and disagreements explicitly, surfacing them as named tensions rather than smoothing into consensus | MUST | Engineering-says-12-weeks / sales-says-8 problem — resolved contradictions lose strategic signal |
| REQ-F17 | Consolidated syntheses shall include provenance metadata: source file paths, git commit hash at compilation time, and compilation date | MUST | Enables staleness detection without external tooling |
| REQ-F18 | A freshness check shall be possible by comparing source file state against the recorded commit hash, identifying when a synthesis may be stale | SHOULD | Git-based: `git diff <recorded-hash> HEAD -- <source-files>` — zero new dependencies |
| REQ-F19 | Raw individual outputs (review reports, research notes) shall be retained as archival sources, not deleted upon consolidation | MUST | Karpathy's architecture: raw sources immutable, synthesis is a compiled view |

**Format Boundary**

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-F20 | Each document type in the framework shall have an explicit format assignment (markdown or HTML) with rationale documented | MUST | Prevents ad-hoc format decisions; establishes when each format is appropriate |
| REQ-F21 | Skills, CLAUDE.md, memory files, and PLANNING.md shall remain markdown | MUST | Platform requirements (skills), frequent quick edits (PLANNING.md, memory), and clean diffs |

### 3.2 Non-Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-N1 | HTML documents shall be viewable in any modern browser with zero external dependencies — no CDN links, no npm packages, no build step | MUST | Framework principle: minimal cognitive overhead extends to tooling |
| REQ-N2 | HTML output shall be structured with one-concept-per-block to keep git diffs meaningful for content review, even though tag-level noise is accepted | SHOULD | User actively reviews tone/content shifts via diff view; diffs must remain useful even if noisier than markdown |
| REQ-N3 | All workflow skills shall be fully rewritten treating existing commands as prototypes, not patched. Each rewrite developed with Mode 3 collaborative review | MUST | Existing commands are prototypes; targeted edits cannot achieve the behavioral consistency needed |
| REQ-N4 | All 46 bugs from the v0.5.0 test run shall have documented dispositions (addressed, deferred, or won't fix) in the bug report's disposition table | MUST | Traceability — know what has and has not been addressed |

---

## 4. User Stories / Use Cases

### UC-1: Developer Runs a Rewritten Workflow Skill

**Actor:** Developer invoking a Praxisity workflow skill (e.g., `/describe`)

**Preconditions:**
- Skill has been rewritten per behavioral and representational standards
- `.praxisity/` directory exists with shared CSS

**Flow:**
1. Developer invokes skill (e.g., `/describe`)
2. Pre-flight executes sequentially; PLANNING.md updated as step 2
3. Gathering prompts one section at a time, waiting for response (drafts for approval when context is sufficient)
4. HTML template is copied via `cp` to `.praxisity/SPEC-NNN/`, then filled using Edit; inapplicable sections marked N/A
5. PLANNING.md updated as hard gate
6. Complete success message shown per skill's own definition

**Postconditions:**
- HTML document exists in the correct spec-centric folder, references `praxisity.css`, includes machine-readable metadata
- No pattern-class bugs from v0.5.0 exhibited

---

### UC-2: Developer Reviews a Complex Document

**Actor:** Developer reading a spec, design, or consolidated review

**Preconditions:**
- HTML document exists under `.praxisity/`

**Flow:**
1. Developer opens HTML file in browser
2. Page renders with consistent styling via `praxisity.css` — status badges, section headers, visual hierarchy
3. All major sections are collapsible; developer sees structure at a glance
4. Developer expands only the sections relevant to their current task
5. Cross-references to related documents are clickable links

**Postconditions:**
- Developer comprehends document structure and targeted content without reading linearly through hundreds of lines

---

### UC-3: Agent Assesses Document Relevance

**Actor:** AI agent (main session or subagent) needing project context

**Preconditions:**
- HTML documents exist with machine-readable `<meta>` tags

**Flow:**
1. Agent reads the first ~10 lines of an HTML document, encountering `<meta>` tags (doc type, status, ID, dependencies)
2. Based on metadata, agent determines whether this document is relevant to the current task
3. If relevant, agent target-reads specific sections by scanning for `<details>` boundaries or section IDs
4. If not relevant, agent skips the document entirely

**Postconditions:**
- Agent spent minimal context on irrelevant documents; relevant documents read efficiently via structural navigation

---

### UC-4: Mode 3 Output Gets Consolidated

**Actor:** Lead agent (or developer) after a Mode 3 team review completes

**Preconditions:**
- Multiple individual review reports exist (e.g., critic, designer, stakeholder reports)

**Flow:**
1. Individual reports are collected from the spec's review subfolder
2. A consolidated synthesis is produced as an HTML document
3. Points of agreement are summarized; contradictions and disagreements are preserved as explicitly named tensions with attribution to the agents that raised them
4. Provenance metadata is recorded: source file paths, current git commit hash, compilation date
5. Raw individual reports are retained in an archive subfolder

**Postconditions:**
- Single authoritative synthesis exists as the primary reading document
- Raw reports preserved but clearly archived
- Provenance metadata enables future staleness checks

---

### UC-5: Developer Detects a Stale Synthesis

**Actor:** Developer or agent encountering a consolidated synthesis document

**Preconditions:**
- A consolidated synthesis exists with provenance metadata (source paths, commit hash)
- One or more source documents have changed since compilation

**Flow:**
1. Developer or agent reads provenance metadata from the synthesis
2. Compares recorded commit hash against current state of source files (e.g., `git diff <hash> HEAD -- <sources>`)
3. Diff is non-empty — synthesis is flagged as potentially stale
4. Developer decides whether to regenerate the synthesis or follow references to source documents to verify conclusions manually

**Postconditions:**
- Staleness is surfaced rather than silently trusted
- Developer has the information to decide whether to act on it

---

## 5. Acceptance Criteria

| ID | Criterion | Validates |
|----|-----------|-----------|
| AC-1 | Given a skill that uses a template, when it generates output, then the template file is copied via `cp` and the original template is byte-for-byte unchanged, and the output was produced by applying only Edit-based modifications to the copy | REQ-F1 |
| AC-2 | Given a skill output where a template section does not apply, then that section is present and marked "N/A — [reason]" rather than removed | REQ-F2 |
| AC-3 | Given any skill invocation, when pre-flight runs, then PLANNING.md is updated as the second step before any other checks complete | REQ-F3 |
| AC-4 | Given a skill with a gather phase, when prompting for section N, then section N+1 is not presented until the user has responded to section N | REQ-F4 |
| AC-5 | Given any completed skill, when the success message is shown, then all elements defined in that skill's Success Message section are present | REQ-F5 |
| AC-6 | Given any completed skill, when the success message appears, then PLANNING.md has already been updated in that same run | REQ-F6 |
| AC-7 | Given a workflow skill producing a spec, design, or consolidated review, when it completes, then the output is an HTML file that references `praxisity.css` via a relative path | REQ-F7 |
| AC-8 | Given any HTML document produced by the framework, when opened in a browser with JavaScript disabled, then all sections are collapsible via `<details>/<summary>` and all styling renders correctly | REQ-F8, REQ-F10 |
| AC-9 | Given any HTML document, when an agent reads the first 15 lines, then `<meta>` tags for document type, status, ID, and compilation date are present | REQ-F9 |
| AC-10 | Given the `.praxisity/` directory, when a new spec is created, then its artifacts are co-located under a spec-specific folder with related designs, DIPs, and reviews accessible within that folder's subtree | REQ-F12 |
| AC-11 | Given a spec with multiple designs, when listed, then each design has its own number within the spec folder without requiring alignment to a global numbering scheme | REQ-F14 |
| AC-12 | Given a Mode 3 team review that produced 3+ individual reports, when consolidation completes, then a single synthesis HTML document exists that names at least one explicit tension or contradiction (or states that none were found), and all individual reports are retained in an archive subfolder | REQ-F15, REQ-F16, REQ-F19 |
| AC-13 | Given a consolidated synthesis, when its provenance metadata is inspected, then it contains source file paths, a git commit hash, and a compilation date | REQ-F17 |
| AC-14 | Given a consolidated synthesis whose source files have been modified since compilation, when a freshness check is run, then the synthesis is identified as potentially stale | REQ-F18 |
| AC-15 | Given any document type in the framework, then a documented format assignment (markdown or HTML) exists with stated rationale | REQ-F20 |
| AC-16 | Given CLAUDE.md, PLANNING.md, skill files, and memory files, then they remain in markdown format | REQ-F21 |
| AC-17 | Given any rewritten skill, then it was developed as a full rewrite (not a patch of existing commands) with Mode 3 collaborative review | REQ-N3 |
| AC-18 | Given the v0.5.0 bug report disposition table, then every bug from BUG-001 through BUG-046 has a disposition of addressed, deferred, or won't fix | REQ-N4 |

---

## 6. Constraints

### 6.1 Inherited from Charter

- Solo developer — changes must be manageable without team coordination
- Claude Code platform — skills, agents, and memory system are the execution environment
- Platform capabilities must be empirically verified before relying on them
- No hard deadline — quality over speed

### 6.2 Spec-Specific Constraints

- Zero external dependencies for HTML viewing — no CDN links, no npm packages, no build tooling, no server
- CLAUDE.md must remain markdown (platform requirement)
- Skill files must remain markdown (platform requirement)
- This spec supersedes SPEC-004 — SPEC-004's behavioral requirements are inherited here, not duplicated in parallel. SPEC-004 should be marked "Superseded by SPEC-009" upon approval
- The `/charter` skill has already been built and validated against SPEC-004 standards. It does not need a full rewrite, but may need updates to conform to new file structure and output format decisions made in design
- `/deliver` and `/breakdown` remain excluded — each requires its own spec (unchanged from SPEC-004)
- File structure migration (moving existing `.plans/` content to `.praxisity/`) is a one-time operation whose scope and approach is a design decision, not a spec requirement

---

## 7. Dependencies

### 7.1 Depends On

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| `.plans/references/new-project-bug-report.md` | Resource | Available | Primary evidence base — all 46 bugs and 3 framework issues (inherited from SPEC-004) |
| 5 workflow skill slots (describe, design, plan, do, charter) | Resource | Charter built; 4 not started | Charter may need format/structure updates; 4 others are full rewrites |
| `.claude/skills/` directory structure | Resource | Available | Existing skills provide pattern; templates will be bundled here |
| Git repository | Resource | Available | Provenance tracking depends on git commit hashes |
| SPEC-004 and DESIGN-005 | Resource | Available | Behavioral standards analysis and design decisions carried forward |

### 7.2 Enables

| Dependent | Relationship |
|-----------|--------------|
| All future specs and designs | Produced in HTML format under the new file structure |
| `/consult-team` skill | Consolidation protocol defines what happens after Mode 3 output |
| `/deliver` pipeline (future) | Stable workflow system is prerequisite for delivery |
| `/breakdown` task decomposition (future) | Stable file structure needed before task management integration |
| Framework distribution / onboarding | Clean `.praxisity/` boundary makes the framework portable to new projects |
| Charter review | Charter may migrate to HTML and/or move under `.praxisity/` based on design decisions |

---

## 8. Out of Scope

The following are explicitly NOT part of this specification:

- `/deliver` command — fundamentally different process (Python-based PDF generation), requires its own spec
- `/breakdown` command — tightly coupled to task management service integration, requires its own spec
- `/new-project` scaffolding — sunset candidate pending framework distribution model decision
- JavaScript-based interactivity (sliders, live editors, copy-as-prompt buttons) — interesting future possibility but not required for core document viewing
- Database-backed knowledge storage (SQL, structured query systems) — our scale (~100 documents, solo user) doesn't warrant it; git + filesystem is sufficient
- Multi-user/team knowledge base features — charter out of scope (post-MVP)
- Automated scheduled recompilation of stale syntheses — staleness is detected, not auto-resolved; human decides when to regenerate
- Static site generator or build tooling for HTML — documents are hand-authored (by agents) HTML, not compiled from another source format
- Auditing and migrating existing `.plans/` content — the migration path is a design concern, but retroactively converting all 90+ existing files is not required by this spec
- BUG-040/BUG-041 (context compaction during long sessions) — platform limitation, not addressable by skill rewrites (unchanged from SPEC-004)
- ISSUE-002 (smart quotes in PDF) and ISSUE-003 (Word Title border) — cosmetic output issues, separate concern (unchanged from SPEC-004)

---

## 9. Open Questions

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| Q-1 | Should CHARTER.md remain a markdown file in the project root, move under `.praxisity/` as HTML, or both (root markdown for platform/git + HTML rendering for reading)? | Open | To be resolved in design |
| Q-2 | What is the exact folder structure under `.praxisity/`? Naming conventions for spec folders, subfolder organization for designs/DIPs/reviews, and where shared assets (CSS, base template) live | Open | To be resolved in design |
| Q-3 | How should the `/charter` skill be updated? It's already built and validated — does it need a full rewrite for HTML output, a targeted update, or can it remain markdown since charters are shorter documents? | Open | To be resolved in design |
| Q-4 | Should the consolidation protocol be embedded in the `/consult-team` skill, or exist as a separate support skill invoked after team completion? | Open | To be resolved in design |
| Q-5 | Do agent prompts need revision before Mode 3 skill rewrites? Agents flagged prompt gaps in SPEC-004 self-evaluations, and agent descriptions reference old vocabulary (commands vs skills) | Open | Carried forward from SPEC-004 Q-5 |
| Q-6 | What is the migration path for existing `.plans/` content? Move everything, move only active specs, or leave `.plans/` as a frozen archive? | Open | To be resolved in design |
| Q-7 | How should HTML templates handle the diff-readability concern? Specific formatting conventions (one-attribute-per-line, semantic line breaks) could keep diffs useful for content review | Open | To be resolved in design |

---

## 10. References

- [CHARTER.md](../../CHARTER.md) — Project constitution, principles, scope
- [SPEC-004: Command Behavioral Fixes and Pattern Standards](004-command-fixes-and-patterns.md) — Superseded by this spec; behavioral standards and bug analysis inherited
- [DESIGN-005: Command Rewrites](../designs/005-command-rewrites.md) — Design decisions from SPEC-004 carried forward where applicable
- [Bug Report: v0.5.0 end-to-end test results](../references/new-project-bug-report.md) — Primary evidence base, 46 bugs and 3 framework issues
- [Session reviews for SPEC-004](../reviews/SESSION-4-1-26/) — 9-agent parallel review (2026-04-01)
- [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — Wiki architecture: raw sources, maintained synthesis layer, schema governance
- [Thariq Shehata: HTML as agent output format](https://x.com/trq212/status/2052809885763747935) — Argument for HTML over markdown for AI-generated documents
- Nate (OpenBrain): Write-time vs query-time synthesis — Staleness risks in compiled knowledge, provenance tracking, contradiction preservation (video transcript, session context)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-05-18 | Andrew Robert Spenn | Initial draft — supersedes SPEC-004, adds HTML format, hierarchical file structure, consolidation protocol, provenance tracking |

---