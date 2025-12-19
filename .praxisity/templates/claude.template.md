# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

<!--
This template is part of the Praxisity framework.
Fill in [BRACKETED] sections and remove comments before use.
Keep this file under 300 lines - minimize length but don't exclude critical information.
Focus on high-level architecture and workflow rules that require multiple files to understand.
-->

## Project Identity

**Name:** [PROJECT_NAME]
**Domain:** [software | public-health | research | other]
**Version:** [SEMVER]
**Status:** [planning | active-development | maintenance | archived]

**Mission:** [One sentence - what does this project accomplish?]

## Framework

**Praxisity Version:** [X.Y.Z]
**Commands Location:** `.claude/commands/`
**Task Management:** Todoist via MCP

## Current Focus

<!-- Update this section frequently to guide AI attention -->

**Active Phase:** [specification | design | implementation | delivery | maintenance]

**Priority Tasks:**
<!-- Link to specific Todoist tasks or .plans/ documents -->
- [Current sprint/milestone focus]
- [Key blockers or decisions needed]

**Recent Context:**
<!-- 2-3 sentences about recent work to provide continuity -->
[What was just completed? What's the current state?]

## Workflow Rules

### Design-First Mandate
1. Always create specifications before designs
2. Always create designs before implementation
3. Use `/spec` → `/architect` → `/breakdown` → `/define` → `/build` flow
4. Never skip directly to code without documentation

### Task Management
- All tasks tracked in Todoist project: "[TODOIST_PROJECT_NAME]"
- Use `/breakdown` to create micro-chunked tasks (<30min each)
- Use `/define` to generate DIPs before implementing complex tasks
- Mark Todoist tasks complete when work is done

### Documentation Requirements
- Update CHARTER.md when scope/principles change
- Create ADRs in `.plans/decisions/` for architectural choices
- Use `/deliver` to generate PDF deliverables for stakeholders

## Architecture Overview

<!-- Describe the big-picture structure that requires reading multiple files to understand.
     Do NOT list every file - focus on conceptual architecture.
     Remove domain sections below that don't apply to your project. -->

### [Domain-Specific Architecture Section]

<!-- For software projects: -->
**System Architecture:**
[Monolith? Microservices? Client-server? Key components?]

**Tech Stack:**
- [Language/framework]
- [Database/storage]
- [Key dependencies]

**Code Organization:**
```
[High-level directory structure with brief explanations]
```

<!-- For public health projects: -->
**Program Model:**
[Theory of change? Intervention framework? Logic model?]

**Stakeholder Map:**
[Who are the key actors? How do they interact?]

**Data Architecture:**
[What data flows through the system? How is it collected/analyzed?]

<!-- For research projects: -->
**Research Design:**
[Methodology? Study design? Analysis approach?]

**Theoretical Framework:**
[What theories/models guide this research?]

**Data Pipeline:**
[How does data flow from collection to analysis to publication?]

### Key Patterns

<!-- Project-specific patterns that Claude should follow -->

**[Pattern Name]:**
[When to use it, how it works, example location]

**[Pattern Name]:**
[When to use it, how it works, example location]

## Development Commands

<!-- Customize based on project type -->

**Build/Test:**
```bash
[How to build the project]
[How to run tests]
[How to run linter/formatter]
```

**Development Server:**
```bash
[How to run locally]
[How to access/test]
```

**Database/Data:**
```bash
[How to set up database]
[How to run migrations]
[How to seed test data]
```

## Domain Conventions

<!-- Customize based on domain.
     Remove domain sections below that don't apply to your project. -->

### [Domain-Specific Section]

<!-- For software projects: -->
**Code Style:**
- [Naming conventions]
- [File organization rules]
- [Comment/documentation standards]

**Testing Requirements:**
- [When to write tests]
- [Coverage expectations]
- [Testing patterns to follow]

<!-- For public health projects: -->
**Terminology:**
- [Key terms and their project-specific meanings]

**Compliance:**
- [IRB requirements]
- [HIPAA/privacy considerations]
- [Regulatory frameworks]

<!-- For research projects: -->
**Citation Style:**
[APA/Chicago/MLA/Domain-specific]

**Reproducibility:**
- [Code organization for reproducible research]
- [Data versioning approach]
- [Environment management]

## Git Safety

**Never:**
- Use `git add .` or `git add -A` (stage files explicitly)
- Commit sensitive data (.env files, credentials, PII, PHI)
- Force push to main/master branch
- Skip pre-commit safety checks

**Always:**
- Use conventional commit format: `type(scope): description`
- Review diffs before committing
- Reference Todoist task IDs in commit messages
- Run tests before pushing (if applicable)

**Commit Types:**
feat, fix, docs, style, refactor, test, chore, data (for data updates)

## Critical Context

<!-- Project-specific knowledge that Claude must know to work effectively -->

### Important Files

**[File/Directory Path]:**
[Why it's important, when Claude should read/modify it]

**[File/Directory Path]:**
[Why it's important, when Claude should read/modify it]

### Known Constraints

<!-- Technical debt, limitations, things that seem wrong but are intentional -->

**[Constraint Name]:**
[What it is, why it exists, what to avoid]

### Domain-Specific Notes

<!-- Context that's unique to this project's domain -->

[Critical knowledge that Claude needs to work effectively in this domain]

## References

- **Governance:** See `CHARTER.md` for mission, principles, and scope
- **Tasks:** Todoist project "[TODOIST_PROJECT_NAME]"
- **Planning:** See `.plans/` for specifications, designs, and DIPs
- **Decisions:** See `.plans/decisions/` for ADRs
- **Dependencies:** [Package manager file, requirements.txt, etc.]

---

<!-- Keep this file updated as the project evolves.
     When architecture changes significantly, update the Architecture Overview.
     When workflow rules need adjustment, update Workflow Rules.
     When starting new work phases, update Current Focus. -->

*Last updated: [DATE]*
