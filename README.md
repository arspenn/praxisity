# Praxisity Framework

**Design-first workflow framework for AI-assisted planning and execution**

Praxisity handles software development, public health program design, academic research, and other multi-disciplinary projects through structured specification, design, and implementation phases.

## What is Praxisity?

**Name Origin**: *Praxis* (theory into practice) + *-ity* (quality/state of being) = the quality of putting theory into practice.

## Core Philosophy

- **Design-first thinking** - Specify and architect before implementing
- **External task management** - Todoist MCP integration (not text files)
- **Self-bootstrapping** - Use Praxisity to build Praxisity
- **Git-versioned documents** - Professional PDF outputs via Pandoc
- **Minimal cognitive overhead** - ADHD-informed design
- **Detailed Implementation Prompts (DIPs)** - Reduce AI variability with task-specific context

## Quick Start

### Prerequisites

- [Claude Code](https://claude.ai/code) installed
- Git
- Todoist account (Premium recommended for reminders)
- Pandoc (for PDF generation)

### Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd praxisity
   ```

2. Configure Todoist MCP in Claude Code settings:
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

3. Start a new project:
   ```
   /new-project
   ```

## Workflow

```
/charter          Create project constitution
      ↓
   /spec          Specify what to build
      ↓
 /architect       Design how it works
      ↓
 /breakdown       Create Todoist tasks (micro-chunked)
      ↓
  /define         Generate Detailed Implementation Prompts
      ↓
  /build          Execute with git safety
      ↓
 /deliver         Generate PDF deliverables
```

## Directory Structure

```
.claude/commands/     - Slash commands for workflow
.praxisity/          - Framework resources
  templates/         - Document templates
  safety/            - Git safety logic
.plans/              - Planning artifacts
  specs/             - Specifications
  designs/           - Design documents
  prompts/           - DIPs
  decisions/         - Architecture Decision Records
deliverables/        - Generated PDF outputs
```

## Commands

- `/new-project` - Initialize fresh project from framework
- `/charter` - Create/update project constitution
- `/spec` - Create specification document
- `/architect` - Create design document
- `/breakdown` - Decompose design into Todoist tasks
- `/define` - Generate DIP for specific task
- `/build` - Execute DIP with git safety checks
- `/deliver` - Generate PDF from markdown

## Features

### ADHD-Informed Design
- Micro-chunked tasks (<30 minutes)
- External accountability via Todoist
- Visible progress tracking
- Clear action verbs (no ambiguous tasks)

### Git Safety
- No blanket `git add .` or `git add -A`
- Sensitive file scanning
- Pre-commit diff review
- Conventional commit format

### Multi-Disciplinary Support
- Software development
- Public health program design
- Academic research
- Cross-domain workflows

## Development Status

**Current Version**: 0.2.0
**Status**: Week 1 Foundation Complete

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Documentation

- [CLAUDE.md](CLAUDE.md) - Configuration for Claude Code
- [CHARTER.md](CHARTER.md) - Project constitution
- [Foundation Plan](praxisity-foundation-plan.md) - Detailed architecture and roadmap

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

### Command Authoring for Opus 4.5

Commands are optimized for Opus 4.5's improved instruction-following:

- **Explicit constraints section** - Every command includes a "Constraints" section with simplicity guardrails
- **Calmer language** - Avoid MUST/CRITICAL/REQUIRED; use normal prose
- **Condensed pre-flight** - Numbered lists, not verbose subsections
- **Let Claude infer** - Describe goals, not micro-steps; Opus 4.5 fills in intermediate steps
- **15,000 char budget** - Keep commands under ~300 lines to avoid truncation
- **Single outcome** - Each command produces one clear result

## Template Design Principles

Templates in `.praxisity/templates/` guide users in creating project artifacts.

1. **Self-documenting** - HTML comments explain what goes where
2. **Placeholder clarity** - Use [BRACKETS] for required fills
3. **Example-driven** - Show examples in comments
4. **Domain-flexible** - Support software/public health/research use cases
5. **Remove guidance** - Comments should be removed in final docs
6. **Opinionated but adaptable** - Strong defaults, clear override points
7. **Dual-use design** - Structured for both human readability and AI parsing (use section IDs like REQ-1, UC-1 for traceability)

**Template Testing:**
- Can a new user understand what to fill in?
- Are examples relevant to multiple domains?
- Is guidance text clearly marked for removal?
- Does the template enforce the framework philosophy?

## Design Decisions

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

## Testing Commands

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

## Roadmap

**Week 1: Foundation**
- Repository structure, CLAUDE.md, CHARTER.md templates
- `/new-project` and `/charter` commands
- ADR documentation

**Week 2: Core Workflow**
- `/spec`, `/architect`, `/breakdown`, `/define` commands
- Spec, design, and DIP templates
- PLANNING.md state management

**Week 3: Execution & Output**
- `/build` command with git safety
- Pandoc templates for PDF generation
- `/deliver` command

**Week 4: Polish**
- Self-documentation, portfolio documentation
- End-to-end testing and refinement

*For current progress, see PLANNING.md and Todoist.*

## Contributing

This project is currently in early development. Contributions will be welcomed after MVP release.

## License

[License to be determined]

## Contact

[Contact information to be added]

---

*Praxisity: Putting theory into practice*
