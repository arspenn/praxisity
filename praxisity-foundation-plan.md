# Praxisity Framework - Foundation Plan

**Date:** December 2025  
**Status:** Draft for Review  
**Scope:** MVP Foundation + 1-Month Timeline

---

## Executive Summary

Praxisity is a design-first workflow framework for AI-assisted planning and execution. It handles software development, public health program design, academic research, and other multi-disciplinary projects through structured specification, design, and implementation phases.

**Name Origin:** Praxis (theory into practice) + -ity (quality/state of being) = the quality of putting theory into practice.

**Core Philosophy:**
- Design-first thinking (proven from Bootstrap V1)
- External task management via Todoist MCP (not text files)
- Self-bootstrapping (use Praxisity to build Praxisity)
- Git-versioned documents with Pandoc output
- Minimal cognitive overhead (ADHD-informed design)
- Detailed Implementation Prompts (DIPs) for consistent AI output

**Differentiation:**
- Multi-disciplinary focus (software + public health + research)
- Integrated external task management via MCP
- Document-centric with version control
- Git safety controls (unique feature)
- DIP generation for reduced AI variability

---

## Foundational vs. Desired Features

### Foundational (MVP - Must Have)

| Feature | Rationale |
|---------|-----------|
| Project Constitution | Governance doc that guides AI behavior for the project |
| Specification Command | Design-first workflow entry point |
| Design Command | Architecture/intervention modeling |
| Breakdown Command | Decompose designs into Todoist tasks via MCP |
| Define Command | Generate DIPs for each task |
| Build Command | Execute DIPs with git safety |
| Todoist MCP Integration | External task store (ADHD requirement) |
| Document Templates | Consistent output structure |
| Pandoc PDF Generation | Deliverable output |
| New-Project Command | Initialize clean project from framework |
| Self-Bootstrapping | Use Praxisity to build Praxisity |

### Desired (Post-MVP)

| Feature | Rationale |
|---------|-----------|
| Multiple domain templates | Public health, research, software variants |
| Advanced git workflows | Branching strategies, PR templates |
| Notion/other MCP integrations | Alternative task systems |
| Collaboration features | Multi-user workflows |
| GitLab migration option | Alternative to GitHub |
| Analytics/metrics | Track productivity patterns |

---

## Command Architecture

### Command Location
All commands in `.claude/commands/` for Claude Code compatibility.

### Command Set

| Command | Purpose | Output |
|---------|---------|--------|
| `/new-project` | Initialize fresh project from framework | Clean project structure |
| `/charter` | Create/update project constitution | `CHARTER.md` |
| `/spec` | Specify what we're building | `.plans/specs/NNN-name.md` |
| `/architect` | Design how it works | `.plans/designs/NNN-name.md` |
| `/breakdown` | Decompose design into Todoist tasks | Tasks created in Todoist |
| `/define` | Generate DIP for specific task | `.plans/prompts/NNN-task-name.md` |
| `/build` | Execute DIP with git safety | Code/documents created |
| `/deliver` | Generate PDF/output from markdown | `deliverables/*.pdf` |

### Command Flow

```
/new-project (once per project)
       |
       v
   /charter (establish constitution)
       |
       v
   /spec --> /architect --> /breakdown --> /define --> /build
     ^                          |             |
     |                          v             v
     |                      (Todoist)       (DIP)
     |_______________________________________________|
              (cycle for each feature)
       |
       v
   /deliver (when ready for output)
```

### DIP (Detailed Implementation Prompt) Purpose

The `/define` command generates a task-specific prompt that:
- References the relevant specification
- References the relevant design
- Includes specific acceptance criteria
- Embeds safety checks
- Provides clear scope boundaries

This reduces AI variability by giving consistent, detailed context for each implementation task rather than relying on generic commands.

---

## Directory Structure

```
project/
├── CLAUDE.md                 # Minimal AI config (~50 lines)
├── CHARTER.md                # Project constitution
├── CHANGELOG.md              # Version history
├── README.md                 # Project overview
|
├── .claude/                  # Claude Code configuration
│   └── commands/             # Slash commands
│       ├── new-project.md
│       ├── charter.md
│       ├── spec.md
│       ├── architect.md
│       ├── breakdown.md
│       ├── define.md
│       ├── build.md
│       └── deliver.md
|
├── .praxisity/               # Framework resources
│   ├── templates/            # Document templates
│   │   ├── charter.template.md
│   │   ├── spec.template.md
│   │   ├── design.template.md
│   │   ├── dip.template.md
│   │   └── pandoc/           # PDF output templates
│   └── safety/               # Git safety logic (referenced by /build)
|
├── .plans/                   # Planning artifacts
│   ├── specs/                # Specifications
│   ├── designs/              # Design documents
│   ├── prompts/              # DIPs (Detailed Implementation Prompts)
│   └── decisions/            # ADRs (Architecture Decision Records)
|
├── deliverables/             # Generated outputs (PDF, etc.)
|
├── src/                      # Source code (if software project)
│   └── ...
|
└── docs/                     # Project documentation
    └── ...
```

### What `/new-project` Does

When a user clones Praxisity to start their own project:

1. Prompts for project name and type
2. Removes Praxisity development artifacts:
   - `.plans/` contents (Praxisity's own planning docs)
   - `deliverables/` (Praxisity's outputs)
   - Development-specific ADRs
   - This planning document
3. Resets to templates:
   - `CLAUDE.md` - populated with project name
   - `CHARTER.md` - empty template ready to fill
   - `README.md` - project template
4. Preserves:
   - `.claude/commands/` (the framework commands)
   - `.praxisity/templates/` (document templates)
   - Git history (user can choose to squash later)
5. Creates initial Todoist project (if MCP connected)

---

## CLAUDE.md Design

Minimal configuration (~50 lines max):

```markdown
# Project Configuration

## Identity
Project: [NAME]
Type: [software | public-health | research | other]
Version: [X.Y.Z]

## Framework
Praxisity Version: 1.0.0
Commands: .claude/commands/

## Conventions
- Design before implementation
- Tasks managed in Todoist (not text files)
- All planning docs in .plans/
- DIPs generated for each implementation task
- Deliverables generated via /deliver

## Git Safety
- Never use `git add .` or `git add -A`
- Review changes before commit
- Use conventional commit format
- Protect main branch

## Current Focus
See CHARTER.md for project constitution
See Todoist for active tasks

@.praxisity/templates/
```

---

## CHARTER.md (Constitution) Design

```markdown
# Project Charter

## Mission
[One sentence: What does this project exist to accomplish?]

## Principles
[3-5 guiding principles that inform all decisions]

## Scope

### In Scope
- [What this project WILL do]

### Out of Scope
- [What this project will NOT do]

## Stakeholders
- [Who benefits from this project]
- [Who contributes to this project]

## Success Criteria
- [How do we know when we've succeeded?]

## Constraints
- [Timeline, budget, technical, regulatory limitations]

## Domain Context
[Project-specific context - theoretical frameworks, tech stack, methodology, etc.]

---
*Charter established: [DATE]*
*Last reviewed: [DATE]*
```

---

## Todoist Integration Architecture

### Why Todoist (Not Text Files)

1. **External accountability** - Tasks exist outside the AI conversation
2. **ADHD-appropriate** - Reminders, due dates, mobile access
3. **Micro-chunking** - AI breaks down tasks, Todoist stores them
4. **Progress visibility** - See what's done without parsing markdown
5. **No context pollution** - Tasks don't consume AI token budget

### MCP Setup

Using the official Todoist MCP server:

```json
{
  "mcpServers": {
    "todoist": {
      "command": "npx",
      "args": ["mcp-remote", "https://ai.todoist.net/mcp"]
    }
  }
}
```

### Todoist Structure (One Project Per Praxisity Project)

```
Todoist Project: [Project Name]
├── Section: Specifications
│   └── Tasks from /spec
├── Section: Design
│   └── Tasks from /architect
├── Section: Implementation
│   └── Tasks from /breakdown (micro-chunked)
└── Section: Delivery
    └── Tasks from /deliver
```

### /breakdown Command Behavior

1. Read the design document
2. Identify implementation steps
3. Apply ADHD-friendly micro-chunking:
   - Each task completable in <30 minutes
   - Clear, concrete action verbs
   - No ambiguous "figure out" tasks
4. Create tasks in Todoist with:
   - Project assignment
   - Section assignment
   - Priority levels
   - Dependencies noted in task descriptions
5. Report summary back to user

### /define Command Behavior

1. Accept task reference (from Todoist or by name)
2. Locate relevant spec and design documents
3. Generate DIP that includes:
   - Task objective
   - Relevant spec sections
   - Relevant design sections
   - Acceptance criteria
   - Git safety reminders
   - Scope boundaries (what NOT to do)
4. Save to `.plans/prompts/NNN-task-name.md`
5. Optionally update Todoist task with link to DIP

---

## Pandoc Integration

### Template Structure

```
.praxisity/templates/pandoc/
├── academic.latex        # For papers, theses
├── report.latex          # For program plans, evaluations
├── memo.latex            # For short deliverables
└── defaults.yaml         # Shared Pandoc settings
```

### /deliver Command Behavior

1. Identify source markdown file(s)
2. Select appropriate template based on document type
3. Run Pandoc with template
4. Output to `deliverables/[name].pdf`
5. Optionally git add the deliverable

### Academic Features

- Citation management via BibTeX
- Automatic bibliography generation
- Figure/table numbering
- Cross-references
- APA/Chicago/custom citation styles

---

## Git Safety (Embedded in /build)

### Pre-Commit Checks

1. **No blanket adds** - Reject `git add .` and `git add -A`
2. **Sensitive file scan** - Warn on .env, credentials, keys
3. **Large file warning** - Flag files >1MB
4. **Uncommitted changes** - Show diff before commit

### Commit Format

```
type(scope): description

[optional body]

[optional footer: references Todoist task]
```

Types: feat, fix, docs, style, refactor, test, chore

### Safety Messaging

```
⚠️  Git Safety Check
-------------------
Detected: [issue]
Risk: [explanation]
Recommendation: [what to do instead]

Proceed anyway? (requires explicit confirmation)
```

---

## MVP Timeline (4 Weeks)

### Week 1: Foundation
- [ ] Create new repository: `praxisity`
- [ ] Set up directory structure
- [ ] Write CLAUDE.md template
- [ ] Write CHARTER.md template
- [ ] Create /new-project command
- [ ] Create /charter command
- [ ] Set up Todoist MCP connection
- [ ] Create Todoist project "Praxisity Development"
- [ ] Document architecture decisions (ADR-001)

### Week 2: Core Workflow
- [ ] Create /spec command + template
- [ ] Create /architect command + template
- [ ] Create /breakdown command
- [ ] Create /define command + DIP template
- [ ] Test spec -> architect -> breakdown -> define flow
- [ ] Populate Praxisity development tasks in Todoist

### Week 3: Execution & Output
- [ ] Create /build command with git safety
- [ ] Set up Pandoc templates (start with one generic)
- [ ] Create /deliver command
- [ ] Test full workflow end-to-end
- [ ] Refine based on actual use
- [ ] Use /define to create DIPs for remaining work

### Week 4: Polish & Documentation
- [ ] Use framework to document itself
- [ ] Create README for public/portfolio
- [ ] Portfolio documentation
- [ ] Validate /new-project cleans properly
- [ ] Buffer for issues/refinement

---

## Todoist Account Recommendation

**Premium ($4/month) - Recommended:**
- Reminders (critical for ADHD)
- Labels (for categorization)
- Filters (custom views)
- Comments on tasks
- Task duration estimates

Business tier not needed for solo use.

---

## Risk Assessment

### Technical Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Todoist MCP issues | Medium | Test early in Week 1, have manual fallback |
| Pandoc template complexity | Medium | Start with one simple template, iterate |
| Git safety too restrictive | Low | Make confirmable, not blocking |
| DIP generation inconsistent | Medium | Iterate on template, test with real tasks |

### Process Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Scope creep | High | Strict MVP definition, backlog everything else |
| Perfectionism | High | "Working" beats "perfect" |
| Abandonment mid-project | Medium | Use framework's own task management |

### ADHD-Specific Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Getting stuck on decisions | High | Timebox decisions, default to simpler option |
| Hyperfocus on wrong thing | Medium | Daily check: "Is this MVP?" |
| Losing momentum | Medium | External accountability (Todoist), visible progress |

---

## Next Steps

1. **Create repository** - `praxisity` on GitHub
2. **Set up Todoist** - Sign up for Premium, create "Praxisity Development" project
3. **Initialize structure** - Create directory skeleton
4. **Write CHARTER.md** - For Praxisity itself (self-bootstrap begins)
5. **Begin Week 1 tasks** - Track in Todoist

---

## Open Items Resolved

| Decision | Resolution |
|----------|------------|
| Framework name | Praxisity |
| Command location | `.claude/commands/` |
| DIP generation | Restored as `/define` command |
| Todoist structure | One project per Praxisity project |
| Templates | Start generic, add domain-specific later |
| First target | Build framework MVP first, then alpha test |

---

*This document will be removed by /new-project when Praxisity is used to start end-user projects.*
