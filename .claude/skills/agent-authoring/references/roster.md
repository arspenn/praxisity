# Praxisity Agent Roster

Nine review agents, installed into a project's `.claude/agents/` by the agent-authoring skill and dispatched through consult-team. Each holds one perspective and one question.

| Agent | Category | Core question | Notes |
|-------|----------|---------------|-------|
| critic | Evaluative | What's wrong with this, and what breaks if it is? | Reads a process's live output alongside the process. |
| skeptic | Evaluative | Do we even need this? | The YAGNI enforcer; challenges scope, not quality. |
| user-advocate | Perspective | Would a new user understand this and grow from it? | Walks one concrete scenario per review, including a non-software one. |
| stakeholder | Perspective | Does the output serve the person it's for? | Reads as the professor, client, or reviewer who never sees the framework. |
| designer | Structural | How do the pieces fit together, with the least surface area? | Boundaries, interfaces, composition. |
| project-manager | Structural | What's realistic, and what blocks what? | Sequencing and feasibility for a solo practitioner. |
| prompt-engineer | Meta | Is this optimized for both humans and AI? | Signal-to-noise, elephants, state-string tracing. |
| consistency-reviewer | Meta | Does what's written here match what's written elsewhere? | IDs, counts, names, and references across documents. |
| spot | Meta | Can someone with no context understand this? | Haiku model; a cold clarity read, cheap and fast. |

**Default review set for a skill or template:** prompt-engineer, critic, user-advocate, spot, in parallel (Mode 2), two rounds: a cold read, then a delta pass on the revision. Add consistency-reviewer when a reference makes claims about other files; designer and skeptic for a design; stakeholder for anything a reader outside the project will receive.

**Memory.** Agents with `memory: project` keep notes under `.claude/agent-memory/<name>/`, which should be gitignored. The Checklist section in each agent file is the baseline those notes grow from; when a pattern recurs across projects, it belongs in the roster file.

## Not Yet Built

- **domain-expert** — a configurable specialist, spawned with a field (public health, software, instructional design) to judge whether content is technically sound there.
- **editor** — writing quality: clarity and concision without changing meaning. Distinct from prompt-engineer (AI-effectiveness) and consistency-reviewer (cross-document agreement).
- **devil's-advocate** — argues the opposing position on a decision outright; stronger than the skeptic, who only questions necessity.
- **integrator** — looks at how new work connects to the existing whole; catches what component-level reviewers miss.