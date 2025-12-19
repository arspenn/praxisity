# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Identity

**Name:** Praxisity Framework
**Type:** Development Framework / Tooling
**Version:** 0.2.0
**Status:** Active Development - Week 1 Complete

**Mission:** Build a design-first workflow framework enabling consistent, structured planning and execution for multi-disciplinary projects through AI-assisted tooling.

## Framework Development Context

**Critical:** This repository IS the Praxisity framework itself. We are building the tool, not using it (yet). Commands and templates created here will be used by future projects. Quality and thoughtfulness in design are paramount.

**Self-Bootstrapping:** Once core commands exist, we'll use Praxisity to build Praxisity (eating our own dog food). The `.plans/` directory will contain our own specifications and designs.

## Current Focus

**Active Phase:** Foundation (Week 1 of 4)
**Priority:** Template design and core command implementation

**Current Tasks:**
- ✅ Directory structure
- ✅ CLAUDE.md and CHARTER.md templates
- ✅ /new-project and /charter commands
- ✅ ADR documentation (4 ADRs)
- ⏳ Todoist MCP integration (user setup required)

**Next Steps:**
1. Create remaining templates (spec, design, DIP)
2. Implement `/spec`, `/architect`, `/breakdown`, `/define` commands
3. Test full workflow: spec → architect → breakdown → define

## Architecture Overview

### Framework Structure

```
.claude/commands/         - Slash command implementations (markdown)
.praxisity/              - Framework resources (user-facing)
  templates/             - Document templates
    claude.template.md   - CLAUDE.md for new projects
    charter.template.md  - CHARTER.md for new projects
    spec.template.md     - Specification template
    design.template.md   - Design document template
    dip.template.md      - Detailed Implementation Prompt template
    pandoc/              - LaTeX templates for PDF generation
  safety/                - Git safety validation scripts/logic
.plans/                  - Praxisity's own planning docs
  specs/                 - Framework specifications
  designs/               - Framework designs
  prompts/               - DIPs for framework features
  decisions/             - ADRs for framework architecture
```

### Command Architecture

Commands are markdown files in `.claude/commands/` that Claude Code interprets as slash commands.

**Command Pattern:**
```markdown
---
description: Brief command description
tags: [relevant, tags]
---

# Command Name

[Command implementation with clear sections:
 1. Parameter gathering (with validation)
 2. Action execution
 3. User feedback
]
```

**Command Design Principles:**
1. **Guided prompting** - Ask questions to gather parameters, don't assume
2. **Safe defaults** - Prefer safety over convenience
3. **Clear feedback** - Tell users what happened and what to do next
4. **Idempotent** - Running twice should be safe
5. **Template-driven** - Commands generate from templates
6. **Error handling** - Graceful failures with helpful messages

### Template Design Principles

Templates in `.praxisity/templates/` guide users in creating project artifacts.

**Template Requirements:**
1. **Self-documenting** - HTML comments explain what goes where
2. **Placeholder clarity** - Use [BRACKETS] for required fills
3. **Example-driven** - Show examples in comments
4. **Domain-flexible** - Support software/public health/research use cases
5. **Remove guidance** - Comments should be removed in final docs
6. **Opinionated but adaptable** - Strong defaults, clear override points

**Template Testing:**
- Can a new user understand what to fill in?
- Are examples relevant to multiple domains?
- Is guidance text clearly marked for removal?
- Does the template enforce the framework philosophy?

## Development Workflow

### For Framework Development

Since we're building the framework, NOT using it yet:

1. **Read the foundation plan** - `praxisity-foundation-plan.md` is our spec
2. **Track tasks in Todoist** - "Praxisity Development" project
3. **Use conventional commits** - Even before `/build` command exists
4. **Test commands manually** - Create test projects to validate
5. **Document decisions** - ADRs in `.plans/decisions/`

### For Command Implementation

When creating a new command:

1. **Design first** - Sketch the command flow in `.plans/designs/`
2. **Identify templates** - What templates does it use/create?
3. **Define parameters** - What input does it need?
4. **Write the command** - Markdown in `.claude/commands/`
5. **Test thoroughly** - Create test scenarios
6. **Document** - Add to README and CHANGELOG

### For Template Creation

When creating a new template:

1. **Identify use cases** - Who uses this? For what?
2. **Design sections** - What information is needed?
3. **Write guidance** - Clear comments explaining each part
4. **Add examples** - Show good examples in comments
5. **Test with novices** - Can someone unfamiliar understand it?
6. **Iterate** - Refine based on actual use

## Core Framework Concepts

### Design-First Philosophy

Every Praxisity project follows: **Specify → Design → Breakdown → Implement**

This framework enforces that workflow through command dependencies:
- `/spec` creates specifications
- `/architect` requires specs to exist (references them)
- `/breakdown` requires designs to exist
- `/define` requires both specs and designs
- `/build` requires DIPs to exist

### Todoist Integration

**Why Todoist (not text files):**
- External accountability (tasks exist outside conversation)
- ADHD-appropriate (reminders, due dates, mobile)
- No token consumption (tasks don't pollute context)
- Visual progress tracking

**MCP Implementation:**
Commands use Todoist MCP to create/update tasks. The framework doesn't manage task state internally.

### DIP (Detailed Implementation Prompt) Concept

DIPs solve AI variability by providing complete context for each task:
- Links to relevant spec sections
- Links to relevant design sections
- Acceptance criteria
- Scope boundaries (what NOT to do)
- Git safety reminders

This means instead of: "Implement user authentication"
You get: "Implement OAuth2 authentication per spec section 3.2 and design section 2.1, using PKCE flow, with explicit exclusions for password-based auth..."

### Git Safety

Framework commands enforce safety by:
- Rejecting `git add .` / `git add -A`
- Scanning for sensitive files
- Showing diffs before commits
- Requiring conventional commit format
- Prompting for confirmation on risky operations

This is implemented in `.praxisity/safety/` and used by `/build` command.

## Development Commands

### Setup Todoist MCP

Add to Claude Code settings:
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

Create Todoist project: "Praxisity Development"

### Testing Commands

```bash
# Test a command by invoking it
/command-name

# Test template generation
cat .praxisity/templates/[template].md

# Validate command markdown
# (commands should be valid markdown with frontmatter)
```

### Document Generation (Future)

```bash
# Once /deliver exists:
pandoc .plans/specs/001-spec.md \
  -o deliverables/spec.pdf \
  --template=.praxisity/templates/pandoc/report.latex
```

## Git Workflow

**Commit Format:**
```
type(scope): brief description

Longer explanation if needed.

Todoist: [task URL or ID]
```

**Types:** feat, fix, docs, style, refactor, test, chore, tmpl (for templates)

**Examples:**
```
feat(commands): add /charter command with template support

tmpl(charter): add comprehensive charter template with domain sections

docs(readme): update quick start with Todoist MCP setup
```

## Key Design Decisions

### Why Markdown Commands?

Claude Code interprets markdown files as commands. This gives us:
- Version control of command logic
- Easy to read/modify
- Natural documentation format
- No compilation/deployment step

### Why Templates Not Generators?

Templates are filled in by users (with AI assistance), not fully generated, because:
- Users need to think deeply about charter/specs
- Fills are more thoughtful than generations
- Templates are easier to customize
- Reduces AI hallucination risk

### Why Separate .praxisity/ Directory?

Framework resources in `.praxisity/` separate from project resources because:
- Clear ownership (framework vs. project)
- Easy to update framework without touching project
- Namespaced to avoid conflicts
- `.` prefix keeps it out of main workspace clutter

## Testing Strategy

**Command Testing:**
1. Create a test directory outside this repo
2. Run `/new-project` to initialize from framework
3. Verify templates are copied correctly
4. Test each command in sequence
5. Validate generated outputs

**Template Testing:**
1. Manually fill in templates
2. Check if guidance is clear
3. Verify placeholders are obvious
4. Test with different domains (software/health/research)

## MVP Timeline

**Week 1 (Complete):** Foundation
- ✅ Repository structure
- ✅ CLAUDE.md and CHARTER.md templates
- ✅ README and ADR templates
- ✅ `/new-project` command
- ✅ `/charter` command
- ✅ 4 Architecture Decision Records

**Week 2:** Core Workflow
- `/spec` command + template
- `/architect` command + template
- `/breakdown` command (Todoist integration)
- `/define` command + DIP template

**Week 3:** Execution & Output
- `/build` command with git safety
- Pandoc templates (basic)
- `/deliver` command
- End-to-end testing

**Week 4:** Polish
- Self-documentation (use framework for itself)
- Portfolio documentation
- Refinement and validation

## Important Files

**praxisity-foundation-plan.md**
- Our source of truth for MVP scope
- Reference when making decisions
- Will be removed by `/new-project` for end users

**CHARTER.md**
- Praxisity's own project charter
- Governs framework development decisions
- Example for end users

**.praxisity/templates/**
- User-facing templates
- Critical to get right - used by all projects
- Must be domain-flexible

## References

- **Foundation Plan:** `praxisity-foundation-plan.md`
- **Charter:** `CHARTER.md`
- **Tasks:** Todoist project "Praxisity Development"
- **Templates:** `.praxisity/templates/`

---

*Last updated: 2025-12-18*
*Current Phase: Week 1 Complete, Ready for Week 2*
