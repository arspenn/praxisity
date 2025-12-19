# Project Charter

## Mission
Build a design-first workflow framework that enables consistent, structured planning and execution for multi-disciplinary projects through AI-assisted tooling.

## Principles
1. **Design before implementation** - Specification and architecture precede coding
2. **External accountability** - Tasks managed in Todoist, not text files
3. **Minimal cognitive overhead** - ADHD-informed design with micro-chunked tasks
4. **Self-documenting** - Git-versioned documents with professional PDF outputs
5. **Safety-first** - Git safety controls prevent accidental commits

## Scope

### In Scope
- Command-driven workflow for spec → design → breakdown → implementation
- Todoist MCP integration for task management
- Document templates (charter, spec, design, DIP)
- Pandoc PDF generation for deliverables
- Git safety controls
- Multi-disciplinary support (software, public health, research)
- Self-bootstrapping capability

### Out of Scope
- Collaboration/multi-user features (post-MVP)
- Multiple domain-specific templates (post-MVP)
- Advanced git workflows beyond safety basics (post-MVP)
- Alternative MCP integrations beyond Todoist (post-MVP)
- Analytics and metrics (post-MVP)

## Stakeholders
- **Primary User**: Solo developer/researcher with ADHD requiring structured workflows
- **Contributors**: Future open-source contributors
- **Beneficiaries**: Multi-disciplinary practitioners needing consistent project management

## Success Criteria
- Complete MVP in 4 weeks
- Successfully self-bootstrap (use Praxisity to build Praxisity)
- End-to-end workflow tested: `/spec` → `/architect` → `/breakdown` → `/define` → `/build` → `/deliver`
- `/new-project` cleanly initializes new projects from framework
- Portfolio-ready documentation

## Constraints
- **Timeline**: 4 weeks to MVP
- **Technical**: Claude Code compatibility, Todoist MCP availability
- **Resources**: Solo developer, no budget constraints
- **Scope**: Strict MVP discipline to avoid feature creep

## Domain Context

**Framework Type**: AI-assisted workflow management
**Primary Technologies**: Claude Code, Todoist MCP, Pandoc, Git
**Methodology**: Design-first, specification-driven development
**Target Domains**: Software engineering, public health program design, academic research

**Key Concepts**:
- **DIP (Detailed Implementation Prompt)**: Task-specific prompts with full context to reduce AI variability
- **ADHD-Informed Design**: Micro-chunking (<30min tasks), external accountability, visible progress
- **Constitution (Charter)**: Governance document guiding AI behavior for the project

---
*Charter established: December 2025*
*Last reviewed: December 2025*
