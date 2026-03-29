# Praxisity Agent Roster

## Active Agents (9)

| Agent | Category | Core Question |
|-------|----------|---------------|
| consistency-reviewer | Meta | Does what's written match what's written elsewhere? |
| critic | Evaluative | What's wrong with this? |
| skeptic | Evaluative | Do we even need this? |
| user-advocate | Perspective | Would a new user understand and benefit? |
| stakeholder | Perspective | Does the output serve its audience? |
| designer | Structural | How do the pieces fit together? |
| project-manager | Structural | What's realistic and what blocks what? |
| prompt-engineer | Meta | Is this optimized for both humans and AI? |
| spot | Meta | Can someone with no context understand this? (haiku model — document clarity gate) |

## Future Agents (Not Yet Built)

- **domain-expert** — Configurable domain specialist. Spawn with a specific domain (public health, software, research) to evaluate whether content is technically sound in that field.
- **editor** — Writing quality reviewer. Checks clarity, conciseness, and readability without changing meaning. Distinct from prompt-engineer (which checks AI-effectiveness) and consistency-reviewer (which checks cross-document agreement).
- **devil's-advocate** — Takes the opposing position on any decision or design choice. Stronger than the skeptic — doesn't just question necessity, actively argues the other side to stress-test reasoning.
- **integrator** — Looks at how new work connects to the existing codebase and framework. Catches integration issues that component-level reviewers miss because they focus on the piece, not the whole.