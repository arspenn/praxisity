---
name: agent-authoring
description: Guide the creation of new Praxisity agent definition files. Ensures native Claude Code subagent format, prompt engineering best practices, and integration with the consultation system. Use when creating a new agent for the roster.
---

# Agent Authoring

This skill guides the creation of new native Claude Code subagent files. It encodes prompt engineering best practices for agent definition files.

## Before You Start

1. Check if an agent with this name already exists in `.claude/agents/`. If so, offer to (r)eview and update or (s)tart fresh, unless the user says otherwise.
2. Read an existing agent file as a reference — any file in `.claude/agents/` works. Note the structure: YAML frontmatter + markdown body with consistent sections.

## Frontmatter

Every agent file starts with YAML frontmatter. Required and optional fields:

**Required by Claude Code:**
- `name` — lowercase with hyphens (e.g., `domain-expert`). This is how the agent is dispatched.
- `description` — one sentence describing when to use this agent. This is a routing hint the platform uses to decide when to delegate. Keep it concise — don't embed usage examples or multi-paragraph scripts.

**Optional Claude Code fields:**
- `tools` — restrict what the agent can do (note: this is the agent equivalent of `allowed-tools` in skill frontmatter — different systems, same concept). Default for review agents: `Read, Grep, Glob, Write`. Broader agents: omit to inherit all tools, unless the user says otherwise.
- `model` — `inherit` (uses session model), `sonnet`, `opus`, or `haiku`. Default to `inherit` unless you have a specific reason. Use `haiku` for lightweight agents like clarity-gate checkers, unless the user says otherwise.
- `memory` — `project` recommended by default. Enables cross-session learning in `.claude/agent-memory/<name>/`. Note: agents may not write to memory unless the platform injects memory instructions at runtime. Omit for lightweight agents that don't need persistence, unless the user says otherwise.

**Required by Praxisity:**
- `category` — one of: `evaluative`, `perspective`, `structural`, `meta`. Used by the consult-team skill for grouping. Claude Code ignores this field.

## Body Sections

The markdown body defines the agent's persona. Four sections, consistent across all agents:

**Identity** — Who this agent is. 2-3 sentences establishing perspective and a core question. This is the attention anchor the agent returns to throughout its work. Example patterns: "You are the [Role]. You ask: '[Core Question]?'"

**Reasoning Approach** — How the agent thinks. A numbered checklist of what to do when reviewing, plus scope boundaries. Keep scope boundaries as simple negative statements ("What you ignore:") — do NOT reference other agents by name in these boundaries, as that primes team-roster awareness that's irrelevant for Mode 1 dispatch.

**Output Format** — Structure for the agent's reports. Include: metadata (artifact, date, dispatch mode), Instructions Received section, findings section (with a domain-specific taxonomy), strengths section, and self-evaluation. Tell the agent to write its report to `.plans/reviews/` with naming convention `[ARTIFACT-ID]-[agent-name]-report.md`.

**Self-Evaluation** — Embedded in the Output Format template. Three prompts: what worked well, what you struggled with, and how YOUR OWN agent prompt could be improved.

## Prompt Engineering Principles

Lessons from building and reviewing agents:

- **Positive scoping over negation.** "What you ignore" lists are fine for simple boundary statements. Do NOT add cross-agent references ("that's the Critic's job") — this primes the agent with team awareness that dilutes its focus.
- **No elephants.** Don't describe capabilities or behaviors you want the agent to avoid. Describing them activates them.
- **Focused and concise.** Agent files should default to ~50-100 lines. If an agent is 150+ lines, it's probably over-specified — consider moving detail to the task prompt instead, unless the user says otherwise.
- **Standalone operation.** The agent file must work without assuming anything will be appended. Customization comes via the task prompt, not by editing the file.
- **Dual consumption.** Every line must be useful to both a human reading the file AND an AI agent receiving it as a system prompt.
- **Calibrated output taxonomies.** If you define severity levels (Critical/Important/Minor), define what they mean. Undefined taxonomies drift between sessions.

## After Writing

1. Save the file to `.claude/agents/[name].md`
2. Update `.claude/agents/README.md` with the new agent's entry, unless the user says otherwise
3. Run `/agents` to register the agent for standalone dispatch, OR use team dispatch (`team_name` parameter) which loads mid-session agents without registration
4. Test: dispatch the agent on a real artifact. Optionally dispatch spot to check whether the output is clear.
5. If the agent will be part of the formal roster, update the roster documentation as needed