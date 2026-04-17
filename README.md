# Praxisity Framework

**Design-first workflow framework for AI-assisted planning and execution**

## What is Praxisity?

*Praxis* (theory into practice) + *-ity* (quality/state of being) = the quality of putting theory into practice.

Praxisity is a skills-based framework for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that structures complex, multi-disciplinary projects through specification, design, and implementation phases. It supports software development, public health program design, academic research, and other domains where structured thinking improves outcomes.

Most AI workflows optimize for output. Praxisity optimizes for understanding. Each phase forces you to articulate decisions you'd otherwise skip — why this scope, why this design, why these trade-offs — and the structure ensures those decisions are recorded, reviewable, and buildable. You don't just get a deliverable; you get better at the process of making one.

## Workflow

Every project follows four phases, each driven by a skill:

```
/charter        Establish project constitution (scope, principles, constraints)
    ↓
/describe       Specify what to build (requirements, acceptance criteria)
    ↓
/design         Architect how it works (structure, interfaces, trade-offs)
    ↓
/plan           Generate implementation prompts (DIPs — self-contained build instructions)
    ↓
/do             Execute with git safety
```

## Skills

Skills are specialized instructions that Claude Code follows when you invoke them. Each skill is a self-contained directory with its own prompt and templates — type `/charter` and Claude knows what to do, what to ask, and what to produce. There are two types:

**Workflow skills** are user-invoked and drive a specific phase of work. Each bundles its own templates.

| Skill | Purpose |
|-------|---------|
| `/charter` | Create or update project constitution |
| `/describe` | Write specification documents |
| `/design` | Create design documents from specs |
| `/plan` | Generate Detailed Implementation Prompts (DIPs) |
| `/do` | Execute DIPs with git safety controls |

**Support skills** are invoked automatically when the context matches, or called directly when needed.

| Skill | Purpose |
|-------|---------|
| `/gather` | Structured input collection across multi-part forms |
| `/skill-forge` | Create and refine skills |
| `/consult-team` | Multi-perspective agent consultation |
| `/agent-authoring` | Create new agent definitions |

## Agent Consultation

Praxisity includes a roster of 9 specialist agents that provide multi-perspective review on work products:

**critic** · **designer** · **project-manager** · **prompt-engineer** · **skeptic** · **spot** · **stakeholder** · **user-advocate** · **consistency-reviewer**

Agents are consulted in three modes via `/consult-team`:

- **Mode 1** — Quick gut-check from one specialist
- **Mode 2** — Multiple independent reviews in parallel, for broad coverage before a decision
- **Mode 3** — Persistent team that stays active through an iteration cycle, reacting to changes as you make them

## Getting Started

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- Git

### Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd praxisity
   ```

2. Start with `/charter` to establish your project's scope and principles, then follow the workflow phases.

## Directory Structure

```
.claude/
  skills/          Skill definitions (bundled templates + instructions)
  agents/          Agent persona definitions (9-agent roster)
  commands/        Legacy prototype commands (being sunset)
.plans/
  specs/           Specification documents
  designs/         Design documents
  reviews/         Agent consultation reports
  decisions/       Architecture Decision Records
  prompts/         Detailed Implementation Prompts
  references/      Research artifacts and external material
.praxisity/
  templates/       Shared framework templates
  safety/          Git safety logic
```

## Principles

1. **Design before implementation** — Specification and design precede building
2. **Bootstrapping** — Use the system to build the system, the system to build the user, the user to build the system — a virtuous cycle where every session generates experience that becomes skills, agents, or templates
3. **Minimal cognitive overhead** — One thing at a time; structured workflows reduce mental burden
4. **Self-documenting** — The work IS the documentation; specs, designs, and plans are git-versioned artifacts
5. **Safety-first** — Git safety controls prevent accidental commits; integrations follow the lethal trifecta security model
6. **Dual-use design** — All outputs optimized for both human understanding and AI agent consumption
7. **Reliability** — Operations are referenced, reviewed, reproducible, and rigorous

See [CHARTER.md](CHARTER.md) for the full project constitution.

## Status

**Version:** 0.6.0 (pre-alpha)

The framework is under active development. `/charter` is built and validated. The remaining workflow skills (`/describe`, `/design`, `/plan`, `/do`) are being built using the framework itself — bootstrapping in practice.

Praxisity is currently a solo project. Contributions will be welcomed after the core workflow is stable.

## License

[License to be determined]

---

*Praxisity: Putting theory into practice*