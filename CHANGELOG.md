# Changelog

All notable changes to the Praxisity framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.0] - 2026-03-29

### Added

**Agent Consultation System (SPEC-005, DESIGN-004, DIP-004 through DIP-007):**
- 9 native Claude Code subagent definitions in `.claude/agents/`:
  - Evaluative: critic, skeptic
  - Perspective: user-advocate, stakeholder
  - Structural: designer, project-manager
  - Meta: prompt-engineer, consistency-reviewer, spot (haiku-based document clarity gate)
- `consult-team` skill in `.claude/skills/consult-team/` — on-demand guidance for multi-agent dispatch with snapshot vs. delta decision gate
- Templates in `.claude/skills/consult-team/templates/`:
  - `context-block.md` — standardized task prompt structure for agent dispatch
  - `session-report.md` — flexible report format for agent findings and lead reviews
  - `collab-mode.md` — Mode 3 persistent teammate awareness extension
- Tier 1 consultation pointers in `/spec`, `/architect`, `/charter` commands with Mode 1 dispatch examples
- `.plans/reviews/` directory for agent consultation outputs
- `.praxisity/templates/gitignore.template` with `.claude/agent-memory/` exclusion

**Three Dispatch Modes:**
- Mode 1: Single expert consult (Agent tool, snapshot, inline in commands)
- Mode 2: Parallel perspectives (Agent tool, snapshot, via consult-team skill)
- Mode 3: Collaborative team (TeamCreate + Agent tool, delta-aware, persistent sessions with direct inter-agent and user messaging)

**Platform Discoveries:**
- Native subagent dispatch works for custom agents after `/agents` registration
- Team dispatch (`team_name` parameter) loads mid-session agents without registration
- Agent files cached at session start; edits require restart or `/agents` reload
- `memory: project` injects ~130 lines of platform boilerplate at runtime

**Bootstrapping Validation:**
- 9-agent team reviewed its own implementation across 2 rounds + cross-reviews
- 18 review reports produced with differentiated, non-redundant findings
- spot (haiku) validated as document clarity gate — caught 7 issues primed agents missed
- Mode 3 collaborative teams validated; inter-agent messaging untested (collab-mode not prepended)

### Changed

- `.gitignore` — added `.claude/agent-memory/` exclusion
- PLANNING.md — updated with SPEC-005 completion and next steps
- `/spec`, `/architect`, `/charter` — added Agent Consultation sections

### Planning Artifacts

- SPEC-005: Agent Consultation System (12 functional + 4 non-functional requirements)
- DESIGN-004: Agent Consultation System Design (4 components, 3 interfaces, 4 data entities, 5 design decisions)
- DIP-004: Templates, extensions, and directory structure
- DIP-005: 8 agent definition files (+ spot added outside DIP scope)
- DIP-006: consult-team skill
- DIP-007: Tier 1 command pointers
- ISSUE-006: DIP template duplicates requirement satisfaction (deferred to SPEC-004)

---

## [0.5.0] - 2026-03-21

### Added

**Commands:**
- `/build` - Execute DIPs with sequential step verification, git safety controls, and state tracking (SPEC-002, DESIGN-002, DIP-002)
  - Verification duality: automatable checks run automatically, subjective checks prompt user
  - Halt-and-ask on failure — never retries or guesses
  - Resume support via PLANNING.md halt state detection
  - Context-aware reading: skips re-reading documents already in current session
- `/deliver` - Generate professional PDFs from markdown documents using ReportLab (SPEC-003, DESIGN-003, DIP-003)
  - Uses `praxisity_style.py` for consistent IEEE-inspired formatting
  - Sans-serif body (Liberation Sans), left-aligned, 1" margins, minimal table rules
  - No external dependencies (no Pandoc, no LaTeX)

**Style Module:**
- `.praxisity/praxisity_style.py` - ReportLab style definitions for PDF output
  - Font registration with Liberation Sans/Mono (Helvetica/Courier fallback)
  - 10 paragraph styles (Title, Subtitle, Heading1-3, BodyText, BulletItem, CodeBlock, Caption, Metadata)
  - IEEE-inspired table style (minimal horizontal rules, no vertical lines)
  - Builder functions: `create_document()`, `build_table()`, `code_block()`, `title_block()`

**Planning Artifacts:**
- SPEC-002: Build Command specification (11 requirements, 3 use cases, 7 acceptance criteria)
- SPEC-003: Deliver Command specification (10 requirements, 2 use cases, 4 acceptance criteria)
- DESIGN-002: Build Command design (3 components, 4 interfaces, 3 data entities, 4 design decisions)
- DESIGN-003: Deliver Command design (2 components, 2 interfaces, 1 data entity, 4 design decisions)
- DIP-002: Build Command implementation prompt
- DIP-003: Deliver Command implementation prompt
- `.plans/references/` directory for external reference documents

### Changed

- PLANNING.md archived and refreshed for Week 3
- CLAUDE.md updated with `/build` dependency chain and developer hints

### Deprecated

- `.praxisity/templates/pandoc/` directory — replaced by ReportLab approach via `praxisity_style.py`

---

## [0.4.0] - 2026-03-20

### Changed

**CLAUDE.md Minimization (SPEC-001, DESIGN-001, DIP-001):**

Reduced CLAUDE.md from 373 to 44 lines (88% reduction) based on research showing comprehensive context files increase agent costs by 20%+ with marginal benefit (Gloaguen et al., 2026).

- CLAUDE.md now contains only corrective/non-obvious content: project identity, framework development context, PLANNING.md state management, design-first workflow constraint, and non-obvious file pointers
- Relocated human-facing content (template principles, design decisions, development workflow, testing commands, roadmap) to README.md
- Rewrote `claude.template.md` with "corrections only" philosophy — template now guides users toward minimal behavioral corrections instead of comprehensive codebase descriptions
- Fixed `/architect` command: changed "domain" to "type" for field name consistency with CLAUDE.md and template

---

## [0.3.0] - 2025-12-19

### Added

**Templates:**
- `spec.template.md` - Specification template with section IDs (REQ-F/N, UC, AC, OBJ)
- `design.template.md` - Design document template with section IDs (COMP, INT, DATA, DEC)
- `dip.template.md` - Detailed Implementation Prompt template with TodoWrite integration
- `changelog.template.md` - Keep a Changelog format template for new projects

**Commands:**
- `/spec` - Create specification documents defining WHAT to build
- `/architect` - Create design documents defining HOW to implement specs
- `/breakdown` - Decompose designs into Todoist tasks with ADHD-friendly sizing
- `/define` - Generate DIPs from design elements or Todoist tasks

**Architecture Decision Records:**
- ADR-005: PLANNING.md for session state persistence

**Documentation:**
- `docs/examples/praxisity-command-evaluation.md` - Opus 4.5 compatibility analysis
- `docs/examples/Claude Code slash commands Opus best practices.md` - Command authoring guide

### Changed

**Command Refactoring for Opus 4.5:**

All 6 commands refactored following Opus 4.5 best practices (~80% size reduction):

| Command | Before | After |
|---------|--------|-------|
| /charter | ~627 lines | ~110 lines |
| /spec | ~740 lines | ~123 lines |
| /architect | ~845 lines | ~137 lines |
| /breakdown | ~546 lines | ~107 lines |
| /define | ~686 lines | ~103 lines |
| /new-project | ~353 lines | ~93 lines |

Changes applied:
- Added explicit "Constraints" section with simplicity guardrails
- Removed aggressive language (MUST/CRITICAL/REQUIRED)
- Condensed pre-flight checks from subsections to numbered lists
- Reduced step granularity - let Opus 4.5 infer intermediate steps

**CLAUDE.md Updates:**
- Added "Command Authoring for Opus 4.5" section
- Added PLANNING.md state management documentation
- Added "dual-use design" principle for templates
- Converted MVP Timeline to static MVP Structure
- Added changelog.template.md to framework structure

**Command Updates:**
- `/charter` - Added PLANNING.md integration
- `/new-project` - Now references changelog template

---

## [0.2.0] - 2025-12-18

### Added

**Templates:**
- `claude.template.md` - CLAUDE.md template for new projects (230 lines, domain-flexible)
- `charter.template.md` - CHARTER.md template for new projects (266 lines, comprehensive governance)
- `readme.template.md` - README.md template for new projects (108 lines)
- `adr.template.md` - Architecture Decision Record template (145 lines)

**Commands:**
- `/new-project` - Initialize fresh project from framework (360 lines)
  - Pre-flight safety checks
  - Parameter gathering with validation
  - Removes Praxisity dev artifacts
  - Generates project files from templates
  - Resets git history to fresh repository
  - Optional Todoist project creation
  - Optional git remote configuration
- `/charter` - Create/update project charter (460 lines)
  - Interactive guided questionnaire (8 sections)
  - Domain-specific questions for software/public-health/research
  - Create and update modes
  - Review & edit before saving
  - Updates CLAUDE.md with mission
  - Optional Todoist review reminders
  - Optional git commit

**Architecture Decision Records:**
- ADR-001: Template-based documents over AI generation
- ADR-002: Git history reset in /new-project command
- ADR-003: Todoist MCP for external task management
- ADR-004: Framework directory structure (.praxisity/ namespace)

**Documentation:**
- Comprehensive CLAUDE.md for framework development (341 lines)
- CHARTER.md documenting Praxisity's governance (80 lines)
- Updated README.md with framework overview (146 lines)

**Infrastructure:**
- `.gitkeep` files in all empty directories (8 directories)
- Complete directory structure:
  - `.claude/commands/` - Slash command implementations
  - `.praxisity/templates/` - Document templates
  - `.praxisity/safety/` - Git safety logic (placeholder for Week 3)
  - `.plans/specs/` - Specifications (placeholder for Week 2)
  - `.plans/designs/` - Design documents (placeholder for Week 2)
  - `.plans/prompts/` - DIPs (placeholder for Week 2)
  - `.plans/decisions/` - Architecture Decision Records
  - `deliverables/` - Generated outputs
  - `src/` - Source code
  - `docs/` - Documentation

### Changed

- CLAUDE.md template guidance: Updated line limit from 200 to 300 lines
- Template philosophy: Clarified multi-domain support with removal guidance

## [0.1.0] - 2025-12-18

### Added

- Project initialization
- Foundation planning document (`praxisity-foundation-plan.md`)
- Core directory structure (`.claude`, `.praxisity`, `.plans`, `deliverables`, `src`, `docs`)
- Initial CLAUDE.md configuration
- Initial CHARTER.md constitution
- Initial README.md
