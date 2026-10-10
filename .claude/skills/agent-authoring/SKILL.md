---
name: agent-authoring
description: Install the Praxisity review agents (critic, skeptic, designer, project-manager, prompt-engineer, consistency-reviewer, spot, stakeholder, user-advocate) into a project, or author a new native Claude Code subagent definition. Use whenever a project needs the agent roster, when consult-team reports that no Praxisity agents are available, or when the user wants a new agent perspective.
---

# Agent Authoring

Two jobs. **Install** puts the Praxisity agent roster, or the part of it the user wants, into the project's `.claude/agents/`. **Author** creates a new agent definition that follows the same conventions. Both end with the agents registered and usable by `consult-team`.

**Roster:** `${CLAUDE_SKILL_DIR}/templates/roster/` holds one ready-to-install file per agent; `${CLAUDE_SKILL_DIR}/references/roster.md` describes them. The roster files are the single source for the agents: this framework's own `.claude/agents/` is an installed copy, like any other project's.

## Why the agents are installed, not bundled

Agents inside a plugin cannot use the `memory` field, and these agents are built to accumulate project-specific review knowledge (recurring weakness patterns, naming conventions, usability friction) across sessions. An agent file copied into a project's `.claude/agents/` is a project agent, where `memory: project` works. So the plugin ships the roster as templates and this skill installs them.

## Install the Roster

1. List the roster from `references/roster.md`: each agent's name, category, and core question, one line each. For each that already exists in `.claude/agents/`, run `diff` against the roster file and mark it "installed, matches the roster" or "installed, differs from the roster", showing the diff (usually a few lines). Nothing records which roster version was installed, so the diff is how the user tells a local edit from a roster update.
2. Ask once which to install, as a checklist. The default is all nine; the workflow skills recommend specific agents by name, and a missing one is a dead end. For an agent that differs from the roster, ask whether to replace it with the roster version, pointing at the diff so the user knows what would be lost; one that matches is simply refreshed. Agent memory is untouched either way, whichever scope it uses.
3. For each chosen agent, copy the roster file with `cp` in Bash to `.claude/agents/[name].md`, creating the directory if it is missing. These are complete files: there are no placeholders to fill and no comments to strip.
4. Memory scope. The roster files declare `memory: local` (`.claude/agent-memory-local/`, never versioned), which is right for a solo project. Ask once: keep it local (the default), or version agent memory with the project (`memory: project`, `.claude/agent-memory/`, shared through git, for a team or for a project that wants the record)? On "version", change the field in the installed copies with `sed -i 's/^memory: local$/memory: project/'` so the field and the repository say the same thing. Note that memory is inert if auto memory is disabled in Claude Code settings. Recurring patterns are promoted to the roster file's Checklist section, which is the versioned form either way.
5. Say when the agents become dispatchable. Claude Code watches `.claude/agents/` and picks up new files within seconds, but only in directories that existed when the session started. So: if `.claude/agents/` already existed, the agents are usable now; if this install created it, the session must be restarted before `consult-team` can dispatch them. (There is no registration command; `/agents` was removed in Claude Code 2.1.2xx.)

## Author a New Agent

1. If an agent with this name already exists in `.claude/agents/`, offer to (r)eview and update it or (s)tart fresh.
2. Read `${CLAUDE_SKILL_DIR}/templates/roster/critic.md` as the structural reference (spot is the one roster file that does not follow the full shape). The sections, in order: YAML frontmatter, Identity, Project Context, Reasoning Approach, Checklist (optional; it grows from experience), Critical Rules, Output Format with a self-evaluation block, and a closing line about memory.
3. Gather, one at a time: the agent's role and core question; the perspective it holds that no existing agent holds; what it ignores; the output taxonomy it reports in, with each level defined in a line. Draft from the conversation when the user has already described the agent.
4. Write the file to `.claude/agents/[name].md`. Write is correct here: an agent file is authored, not derived from a placeholder template, so there is no template ground truth to drift from. Before saving, confirm the headings match the roster file you read. If `.gitignore` excludes `.claude/agents/` wholesale, say so, because the new agent would be unversioned; the Praxisity source repo ignores only the nine roster names.
5. If this project is the Praxisity framework repository (the roster directory is tracked here), offer to add the new agent to the roster as well when it is general enough to belong in every project. In any project, finish as Install does: the agent is dispatchable within seconds if `.claude/agents/` already existed, after a restart if this file created it; then test by dispatching it on a real artifact, optionally with spot reading its report.

## Frontmatter

Required by Claude Code: `name` (lowercase, hyphens; this is how the agent is dispatched) and `description` (one sentence saying when to use the agent; the platform routes on it).

Common optional fields: `tools` (allowlist; review agents use `Read, Grep, Glob, Write`), `model` (`inherit`, `sonnet`, `opus`, `haiku`, or a full model ID; `inherit` unless there is a reason, as spot's `haiku` is), `memory` (`project` for agents meant to learn across sessions; omit for lightweight ones). `category` (`evaluative`, `perspective`, `structural`, `meta`) is Praxisity's own grouping field; Claude Code ignores it. The full field list and platform behaviours are in `${CLAUDE_SKILL_DIR}/references/platform-reference.md`.

## Writing the Body

- **Identity** is the attention anchor: who the agent is and the one question it keeps asking. Two or three sentences.
- **Project Context** states the workflow (Describe → Devise → Detail → Do, charter as entry) and where artifacts and IDs live. It is the same paragraph across the roster, varied only where the agent's focus needs a different emphasis.
- **Reasoning Approach** is a numbered procedure plus "What you ignore" as plain boundary statements. Do not name other agents in those boundaries; it primes team awareness that is irrelevant when the agent is dispatched alone.
- **Checklist** holds the recurring patterns the agent has learned to check, phrased as questions with observable answers, never as findings (a finding stated as a fact gets re-reported in every session, fixed or not). A new agent has no Checklist section; one is added when a pattern has recurred in the agent's memory, and it is kept to about a dozen items, retiring the rest to memory.
- **Critical Rules** are a few calibration rules, always ending with "if the work is sound, say so".
- **Output Format** names the report path (`.plans/reviews/[ARTIFACT-ID]-[name]-report.md`), the metadata, an Instructions Received section, findings in the agent's own taxonomy with each level defined, a strengths section, and a self-evaluation asking what worked, what the agent struggled with, and how its own prompt could improve.

Principles, learned the hard way: describe what to do, not what to avoid, because describing a behaviour activates it; keep files near 100 lines, since detail beyond that belongs in the task prompt; make the file standalone, with customization coming from the task prompt rather than edits; design for single-level dispatch, since subagents cannot spawn subagents; define every taxonomy level, because undefined ones drift between sessions.