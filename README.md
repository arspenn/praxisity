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

## Contributing

This project is currently in early development. Contributions will be welcomed after MVP release.

## License

[License to be determined]

## Contact

[Contact information to be added]

---

*Praxisity: Putting theory into practice*
