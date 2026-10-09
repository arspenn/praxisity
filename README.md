# Praxisity Framework

**Design-first workflow framework for AI-assisted planning and execution**

## What is Praxisity?

*Praxis* (theory into practice) + *-ity* (quality/state of being) = the quality of putting theory into practice.

Praxisity is a skills-based framework for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that structures complex, multi-disciplinary projects through specification, design, and implementation phases. It supports software development, public health program design, academic research, instructional design, and other domains where structured thinking improves outcomes.

Most AI workflows optimize for output. Praxisity optimizes for understanding. Each phase asks you to articulate decisions you'd otherwise skip — why this scope, why this design, why these trade-offs — and the structure ensures those decisions are recorded, reviewable, and buildable. You don't just get a deliverable; you get better at the process of making one.

## Workflow

Every project follows four phases, each driven by a skill, with the charter as the entry point:

```
/charter        Establish the project constitution (mission, principles, scope, constraints)
    ↓
/describe       Specify what to build (requirements, use cases, acceptance criteria)
    ↓
/design         Decide how it works (components, interfaces, decisions)
    ↓
/detail         Turn one design element into a DIP (a self-contained implementation prompt)
    ↓
/do             Execute a DIP step by step, with verification and git safety
```

Each phase cites the previous one by ID, so a requirement can be traced from the spec through the design to the step that implements it.

## Skills

Skills are instructions Claude Code follows when you invoke them. Each is a self-contained directory with its prompt and templates. Two kinds:

**Workflow skills** are user-invoked and drive one phase of work. Each bundles its own templates.

| Skill | Purpose |
|-------|---------|
| `/charter` | Create or update the project constitution, and set up CLAUDE.md, README, CHANGELOG, and .gitignore |
| `/describe` | Write a specification (SPEC-NNN) |
| `/design` | Write a design for a specification (DESIGN-NNN) |
| `/detail` | Turn one design element into a Detailed Implementation Prompt (DIP-NNN) |
| `/do` | Execute a DIP with verification after every step and git safety before commit |

**Support skills** load automatically when the conversation matches, or can be called directly.

| Skill | Purpose |
|-------|---------|
| `/gather` | The one-section-at-a-time protocol every workflow skill uses to collect input |
| `/consult-team` | Multi-perspective review by the agent roster |
| `/agent-authoring` | Install the agent roster into a project, or author a new agent |
| `/skill-forge` | Create and refine skills |

## Agent Roster

Nine specialist agents give multi-perspective review of work products:

**critic** · **skeptic** · **user-advocate** · **stakeholder** · **designer** · **project-manager** · **prompt-engineer** · **consistency-reviewer** · **spot**

They are installed into a project with `/agent-authoring` rather than bundled in the plugin, because agents inside a plugin cannot keep memory, and these are built to accumulate project-specific review knowledge across sessions. `/consult-team` dispatches them in three modes: a single opinion, parallel independent reviews, or a persistent team that follows the work as it changes.

## Getting Started

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 2.1.275 or later
- Git

### Install the plugin

From a local clone, for development or trial, run this from inside your project directory:

```bash
claude --plugin-dir /path/to/praxisity
```

Do not add `--add-dir /path/to/praxisity`: that makes the framework's own `.claude/` load as if it belonged to your project, so every support skill appears twice and the nine review agents appear uninstalled, keeping their memory in the wrong repository. If Claude needs to read a framework file, it will ask. To confirm the plugin is loaded, look for `praxisity:gather` in the available skills; the workflow skills are hidden from that list by design and appear only as `/praxisity:charter` and so on.

From GitHub, in one step (Claude Code 2.1.275 or later):

```
/plugin install praxisity --marketplace arspenn/praxisity
```

Or add the repository as a marketplace first: `/plugin marketplace add https://github.com/arspenn/praxisity.git`, then `/plugin install praxisity@arspenn`.

Skills from the plugin are namespaced: `/praxisity:charter`, `/praxisity:describe`, and so on.

### Start a project

1. In your project directory, run `/praxisity:charter`. It walks you through the charter one section at a time and offers to set up CLAUDE.md, README, CHANGELOG, and .gitignore.
2. Run `/praxisity:agent-authoring` to install the agent roster. If this creates `.claude/agents/` for the first time, restart the session so Claude Code loads it.
3. Follow the phases: `/praxisity:describe`, `/praxisity:design`, `/praxisity:detail`, `/praxisity:do`.

## Directory Structure

```
.claude-plugin/      Plugin and marketplace manifests
.claude/
  skills/            Skill definitions, each with its bundled templates and references
  agents/            Installed copy of the agent roster (source: skills/agent-authoring/templates/roster/)
.plans/
  specs/             Specifications
  designs/           Designs
  prompts/           Detailed Implementation Prompts
  decisions/         Architecture Decision Records
  reviews/           Agent review reports
  references/        Source material
  archive/           Earlier planning state and reviews
.praxisity/
  templates/         Templates awaiting a skill (currently the ADR template)
```

## Principles

1. **Design before implementation** — Specification and design precede building
2. **Bootstrapping** — Use the system to build the system, the system to build the user, the user to build the system; every session generates experience that becomes skills, agents, or templates
3. **Minimal cognitive overhead** — One thing at a time; structured workflows reduce mental burden
4. **Self-documenting** — The work IS the documentation; specs, designs, and plans are git-versioned artifacts
5. **Safety-first** — Git safety controls prevent accidental commits; integrations follow the lethal trifecta security model
6. **Dual-use design** — All outputs are written for both human understanding and AI consumption
7. **Reliability** — Operations are referenced, reviewed, reproducible, and rigorous

See [CHARTER.md](CHARTER.md) for the full project constitution.

## Status

**Version:** 0.7.0 (pre-alpha)

All five workflow skills and the four support skills are built and reviewed; the plugin packaging is validated. The end-to-end live test on a real project is the next step before the first release. Praxisity is built with itself: its own specs, designs, and reviews are in `.plans/`.

Praxisity is a solo project. Contributions will be welcomed once the core workflow is stable.

## License

[License to be determined]

---

*Praxisity: Putting theory into practice*