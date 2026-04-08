---
name: agent-authoring
description: Guide the creation of new Praxisity agent definition files. Ensures native Claude Code subagent format, prompt engineering best practices, and integration with the consultation system. Use when creating a new agent for the roster.
---

# Agent Authoring

This skill guides the creation of new native Claude Code subagent files. It encodes prompt engineering best practices for agent definition files.

## Before You Start

1. Check if an agent with this name already exists in `.claude/agents/`. If so, offer to (r)eview and update or (s)tart fresh, unless the user says otherwise.
2. Read an existing agent file as a reference — any file in `.claude/agents/` works. Note the structure: YAML frontmatter + markdown body. Minimal example:

```markdown
---
name: example-agent
description: Brief description of when to use this agent.
tools: Read, Grep, Glob, Write
model: inherit
memory: project
---

## Identity
You are the [Role]. Your core question: "[What do you ask?]"

## Reasoning Approach
1. [First step]
2. [Second step]

## Output Format
Write your report to `.plans/reviews/` with findings and self-evaluation.
```

## Frontmatter

Every agent file starts with YAML frontmatter. The most common fields are listed here. For the full list of all 16+ supported fields (including advanced options like `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `isolation`, and more), read `${CLAUDE_SKILL_DIR}/references/platform-reference.md` — it complements this skill with reference tables and official documentation links.

**Required by Claude Code:**
- `name` — lowercase with hyphens (e.g., `domain-expert`). This is how the agent is dispatched.
- `description` — one sentence describing when to use this agent. This is a routing hint the platform uses to decide when to delegate. Keep it concise.

**Common optional fields:**
- `tools` — allowlist of tools the agent can use (agent equivalent of `allowed-tools` in skill frontmatter). Default for review agents: `Read, Grep, Glob, Write`. Use `disallowedTools` for a denylist instead. Omit both to inherit all session tools, unless the user says otherwise.
- `model` — `inherit` (uses session model), `sonnet`, `opus`, `haiku`, or a full model ID. Default to `inherit` unless you have a specific reason, unless the user says otherwise.
- `memory` — `project` recommended by default. Options: `project` (shared via git, per-project), `user` (personal, across all projects), `local` (per-project, not shared via git). When enabled, the platform automatically injects memory instructions AND enables Read/Write/Edit tools for the memory directory. Omit for lightweight agents that don't need persistence, unless the user says otherwise.

**Praxisity-specific (not part of Claude Code):**
- `category` — one of: `evaluative`, `perspective`, `structural`, `meta`. Claude Code ignores this field. Used by Praxisity's consult-team skill for dispatch grouping.

## Body Sections

The markdown body defines the agent's persona. Four sections, consistent across all agents:

**Identity** — Who this agent is. 2-3 sentences establishing perspective and a core question. This is the attention anchor the agent returns to throughout its work. Example patterns: "You are the [Role]. You ask: '[Core Question]?'"

**Reasoning Approach** — How the agent thinks. A numbered checklist of what to do when reviewing, plus scope boundaries. Keep scope boundaries as simple negative statements ("What you ignore:") — do NOT reference other agents by name in these boundaries, as that primes team-roster awareness that's irrelevant for single-agent dispatch (Mode 1 — one agent consulted in isolation).

**Output Format** — Structure for the agent's reports. Include: metadata (artifact, date, dispatch mode), Instructions Received section, findings section (with a domain-specific taxonomy), strengths section, and self-evaluation. Tell the agent to write its report to `.plans/reviews/` with naming convention `[ARTIFACT-ID]-[agent-name]-report.md`.

**Self-Evaluation** — Part of the Output Format (included in the agent's report output, not as a separate section in the agent file). Three prompts for the agent to answer in its report: what worked well, what you struggled with, and how YOUR OWN agent prompt could be improved.

## Prompt Engineering Principles

Lessons from building and reviewing agents:

- **Positive scoping over negation.** "What you ignore" lists are fine for simple boundary statements. Do NOT add cross-agent references ("that's the Critic's job") — this primes the agent with team awareness that dilutes its focus.
- **No elephants.** Don't describe capabilities or behaviors you want the agent to avoid. Describing them activates them.
- **Focused and concise.** Agent files should default to ~50-100 lines. If an agent is 150+ lines, it's probably over-specified — consider moving detail to the task prompt instead, unless the user says otherwise.
- **Standalone operation.** The agent file must work without assuming anything will be appended. Customization comes via the task prompt, not by editing the file.
- **Single-level dispatch.** Subagents cannot spawn other subagents. The lead agent coordinates all dispatch. Design agents to do their work and report back — not to delegate further.
- **Dual consumption.** Every line must be useful to both a human reading the file AND an AI agent receiving it as a system prompt.
- **Calibrated output taxonomies.** If you define severity levels (Critical/Important/Minor), define what they mean. Undefined taxonomies drift between sessions.

## After Writing

1. Save the file to `.claude/agents/[name].md`
2. Update `.claude/agents/README.md` with the new agent's entry, unless the user says otherwise
3. Register the agent: run `/agents` in Claude Code to add it to the session registry for standalone dispatch. Alternatively, team dispatch (using the `team_name` parameter when spawning) scans the agents directory fresh and can load agents created during the current session without registration.
4. Test: dispatch the agent on a real artifact. Optionally dispatch spot to check whether the output is clear.
5. If the agent will be part of the formal roster, update the roster documentation as needed