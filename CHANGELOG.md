# Changelog

All notable changes to the Praxisity framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

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
