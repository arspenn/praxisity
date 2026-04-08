# Claude Code Agent Definition — Platform Reference

Official documentation: https://code.claude.com/docs/en/sub-agents.md

## All Supported Frontmatter Fields

### Required

| Field | Purpose |
|-------|---------|
| `name` | Agent identifier, lowercase with hyphens. Used for dispatch. |
| `description` | When to use this agent. Platform uses this as a routing hint. |

### Optional — Common

| Field | Purpose | Default |
|-------|---------|---------|
| `tools` | Allowlist of tools the agent can use. | Inherits all session tools |
| `disallowedTools` | Denylist of tools the agent cannot use. Opposite of `tools`. | None |
| `model` | Model to use. Options: `inherit`, `sonnet`, `opus`, `haiku`, or a full model ID. | `inherit` |
| `memory` | Enable persistent memory. Options: `project`, `user`, `local`. | Disabled |
| `permissionMode` | Permission behavior. Options: `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`. | `default` |

### Optional — Advanced

| Field | Purpose | Default |
|-------|---------|---------|
| `maxTurns` | Maximum agentic turns before the agent stops. | Platform default |
| `skills` | Preload specific skills into the agent's context. | None |
| `mcpServers` | Configure MCP servers available to the agent. | Inherits session MCP |
| `hooks` | Lifecycle hooks scoped to this agent. | None |
| `background` | Run agent as a background task. | `false` |
| `effort` | Override effort level. Options: `low`, `medium`, `high`, `max`. | Inherits session |
| `isolation` | Run in a temporary git worktree. | Disabled |
| `color` | Display color in task list UI. | Auto-assigned |
| `initialPrompt` | Auto-submitted first turn — agent starts working immediately on this prompt. | None |

### Praxisity-Specific (not part of Claude Code)

| Field | Purpose | Notes |
|-------|---------|-------|
| `category` | Agent grouping for consult-team skill. Options: `evaluative`, `perspective`, `structural`, `meta`. | Claude Code ignores this field. Used by Praxisity's consult-team skill for dispatch grouping. |

## Key Platform Behaviors

### Memory

When `memory` is set (e.g., `memory: project`), the platform automatically:
- Injects ~150 lines of memory instructions into the agent's system prompt
- Includes the first 200 lines / 25KB of the agent's `MEMORY.md`
- Enables Read, Write, and Edit tools for the memory directory
- Memory path: `.claude/agent-memory/<agent-name>/` (project scope)

Reference: https://code.claude.com/docs/en/sub-agents.md#enable-persistent-memory

### Dispatch

- **Standalone dispatch** (`Agent(subagent_type: "name")`): requires agent to be in session registry (loaded at startup or via `/agents`)
- **Team dispatch** (`Agent(subagent_type: "name", team_name: "...", name: "...")`): scans `.claude/agents/` fresh at spawn time — can load agents created mid-session
- **CLI dispatch** (`--agents` flag): agents can be defined as JSON objects at launch time

Reference: https://code.claude.com/docs/en/sub-agents.md

### Scope Priority

When multiple agents share the same name, scope determines which loads:
1. Project agents (`.claude/agents/` in project directory) — highest priority
2. User agents (`~/.claude/agents/`)
3. Plugin agents — lowest priority

Reference: https://code.claude.com/docs/en/sub-agents.md (scope priority section)

### Constraints

- **Subagents cannot spawn other subagents.** An agent dispatched via the Agent tool cannot itself dispatch further agents. Design agents as single-level — the lead coordinates.
- **Agents receive CLAUDE.md** but NOT the lead's conversation history.
- **Team teammates** load CLAUDE.md, MCP servers, and skills from project/user settings.
- **Plugin agents** cannot use `hooks`, `mcpServers`, or `permissionMode`.

Reference: https://code.claude.com/docs/en/sub-agents.md, https://code.claude.com/docs/en/agent-teams.md