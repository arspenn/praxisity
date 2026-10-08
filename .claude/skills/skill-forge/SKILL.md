---
name: skill-forge
description: Guide the creation of well-structured Claude Code skills. Covers directory layout, frontmatter configuration, prompt engineering for dual-use skill files, template bundling, plugin packaging, and testing strategy. Use when creating a new skill, restructuring an existing one, or deciding how a new capability should be packaged.
---

# Skill Forge

Guide the creation of a new Claude Code skill. A skill is a directory-based prompt specification that the platform loads as agent instructions: it shapes how Claude works, not what Claude knows.

## Before You Start

1. **Clarify the skill's purpose.** What does this skill help the agent do? A skill is instructions for behavior, not a knowledge document.
2. **Determine the skill type:**
   - **Workflow skill** (`disable-model-invocation: true`): user-invoked via `/name`. Drives a process the user initiates and usually converses with them throughout. Examples: producing a document, executing a plan.
   - **Support skill** (default, auto-invokable): the agent loads it when the conversation matches its description. Examples: a gathering protocol, consultation dispatch, review patterns.
3. **Check for Praxisity-specific patterns.** If the skill will live in the Praxisity framework or in a project managed by it, read `${CLAUDE_SKILL_DIR}/references/praxisity-patterns.md` before proceeding; it holds the skeleton every Praxisity skill follows and the conventions that bind them.

## Progressive Loading Model

Skills load in three levels:

1. **Metadata** (name + description) is always in context, about 100 words. The platform uses it to decide auto-invocation.
2. **SKILL.md body** loads when the skill triggers. Keep it under 500 lines; the Praxisity workflow skills run about 100. If a skill is approaching the limit, move reference material to `references/` with a clear pointer about when to read it.
3. **Bundled resources** (`templates/`, `references/`, `scripts/`) load only when the skill instructs the agent to read them. Unlimited size.

## Skill Directory Structure

```
.claude/skills/[skill-name]/
├── SKILL.md                    ← required: frontmatter + the behavioral specification
├── templates/                  ← optional: output templates the skill copies and fills
│   └── [name].template.md
└── references/                 ← optional: documents the skill reads at specific phases
    └── [name].md
```

Bundle everything a skill uses inside its directory. A skill that reaches for a path elsewhere in the repo cannot be installed on its own and will break inside a plugin.

## Frontmatter

The YAML frontmatter configures how the platform handles the skill. Two columns matter: what has been tested in this repository, and what the Claude Code documentation (read 2026-09-22, version 2.1.280) says exists. Treat the second as true but untested; the project's platform-capabilities memory tracks which is which.

| Field | Purpose | Status |
|-------|---------|--------|
| `name` | Becomes the `/slash-command`. Lowercase, hyphens. Defaults to the directory name. | Tested here |
| `description` | What the skill does and when to use it. The platform matches conversation context against it for auto-invocation. Required. | Tested here (loading); auto-invocation itself untested |
| `disable-model-invocation` | `true` prevents auto-invocation. Use for workflow skills the user must trigger. Default `false`. | Tested here (skill loaded only on explicit call) |
| `user-invocable` | `false` hides the skill from the `/` menu. Use for background-knowledge skills. Default `true`. | Documented |
| `argument-hint` | Shown during autocomplete. Spell out the accepted argument forms. | Documented |
| `when_to_use` | Additional triggering context, separate from the description. | Documented as of 2.1.280; an IDE diagnostic rejected it in April 2026, so test before relying on it |
| `allowed-tools` / `disallowed-tools` | Restrict the tools available while the skill runs. | Documented |
| `model`, `effort` | Pin a model or an effort level (`low` to `max`) for the skill. | Documented |
| `context: fork` | Run the skill in an isolated subagent context, optionally with `agent` and `background`. **Never set this on a skill that converses with the user**; a forked context cannot ask them anything. | Documented |
| `hooks`, `paths`, `shell`, `metadata`, `license`, `compatibility` | Available; rarely needed. | Documented |

**Path variables.** `${CLAUDE_SKILL_DIR}` resolves to the skill's own directory; tested here for repo-local skills. Use it for every bundled file, declared once near the top of the skill. Inside a plugin, `${CLAUDE_PLUGIN_ROOT}` is the documented variable for bundled files; whether `${CLAUDE_SKILL_DIR}` also resolves there is untested. Declaring the path once per skill makes the swap a one-line edit.

**Arguments.** The text the user types after the slash command is available as `$ARGUMENTS` (documented for skills; untested here). Say in the skill what each accepted form means.

**Skill-from-skill loading.** A skill can tell the agent to invoke another skill with the Skill tool (the Praxisity workflow skills load `gather` this way). Untested as of this writing; it is on the plugin verification list.

**How auto-invocation works.** The platform matches conversation context against skill descriptions. Claude consults skills only for tasks it cannot easily handle on its own, so a simple one-step request may not trigger a matching skill. Write support-skill descriptions to name the specific situations where the skill adds value, and make them a little pushy ("use it whenever the task means walking a user through several sections, even if they do not call it a form"), because the platform currently under-triggers.

## Writing the SKILL.md Body

The body is both a human-readable document and the prompt the AI follows. Write for both.

### Structure

1. **Title and purpose**: one paragraph saying what the skill produces and who reads it.
2. **Rules**: behavioral limits with their reasons. Short and specific.
3. **Phases**: the steps the agent follows, in order, each under its own heading.
4. **Success criteria**: what done looks like, as a checklist the agent can verify.

### Prompt Engineering Principles

**Explain the why.** An instruction that carries its reason is followed more reliably than a bare imperative, and the reason lets the agent handle the cases the instruction did not foresee. ALWAYS and NEVER in capitals are a sign the reason is missing. Mechanical, binary rules can stay imperative; judgment calls need the reasoning.

**Positive framing over prohibitions.** A list of what not to do teaches the failure mode. Prefer a verification check ("before sending, confirm these three things") or a bounded positive rule ("ask when two readings would produce different outputs; otherwise decide").

**Observable gates over self-assessment.** "When you have sufficient context" is always true to the agent. "When the user has provided direct input on this topic" or "when loaded documents cover this section" can be checked.

**Phase-boundary placement.** An instruction is most effective immediately before the phase it governs. A rule stated under Gather is out of view by Generate; if Generate depends on it, say it again there or move it.

**Imperative sequencing.** Numbered lists alone do not prevent parallelization. Add "run these steps in order and finish each before starting the next" with the reason step order matters.

**One owner per fact.** When a template and a skill both describe a section, they drift. Put per-section guidance in the template's comments and keep only skill-specific notes in the skill.

**Trace every state string.** If a skill writes a value another skill or a later run reads (a Status row, a resume pointer), list each value with its writer and its reader. Values with no reader and readers with no writer are the bugs reviewers find.

**Compression.** Keep instructions minimal. Reference material belongs in `references/`, read at the moment it is needed.

### Template Bundling

If the skill produces output from a template:

1. Bundle the template under `templates/` and reference it by `${CLAUDE_SKILL_DIR}` once.
2. In the Generate phase, instruct: copy with `cp`, read the copy, modify with Edit only, strip HTML comments.
3. Define the permitted Edit operations as a closed list.
4. Put per-section guidance and examples in the template's HTML comments; they are the gathering guide and are stripped on output.
5. Mark placeholder counts as illustrative so the agent does not anchor on them.

### Update Flow

Design the update flow from the start; it is used more than the create flow. Pre-flight checks whether the output exists; the update path asks what changed since the last date, walks only those sections plus any marked TBD, presents existing content as drafts, keeps identifiers stable, and preserves original dates.

## Plugin Packaging

A plugin bundles skills, agents, and hooks for installation into any project. Layout, verified against the documentation on 2026-09-22:

```
my-plugin/
├── .claude-plugin/plugin.json
├── skills/<name>/SKILL.md (+ templates/, references/)
├── agents/<name>.md
└── hooks/
```

Install from a local directory for development with `claude --plugin-dir ./my-plugin`, or add a local path or git repository as a marketplace and install from it; plugins can be enabled per project or user-wide. Plugin agents appear as `plugin-name:agent-name` and cannot use the `memory` field. Skills that reach outside their own directory, rely on `${CLAUDE_SKILL_DIR}` resolving inside a plugin, or invoke other skills with the Skill tool should be tested under `--plugin-dir` before the plugin is relied on.

## Testing Strategy

1. **Review before testing.** Have specialist reviewers read the skill as a prompt before anyone runs it; a prompt-engineering read, an adversarial read, a target-user walkthrough, and a cold clarity read catch different things. The Praxisity patterns reference names the roster it uses.
2. **Live test before trusting.** Reviews catch structure; a live run catches interaction problems: awkward flows, an update path that loses state, a verification that cannot be run. Both are needed.
3. **Test in a fresh session** when the skill relies on auto-invocation, so the platform's matching is what is tested rather than the conversation's memory.
4. **Verify template integrity** after a run: the bundled template must be unchanged.
5. **Walk one non-software scenario.** A skill written with code in mind quietly assumes files, paths, and an agent that does the work. Walk it once as someone building a lesson in an authoring tool.
6. **Read the output cold.** Does it make sense without project context? If it uses undefined terms, the template needs a glossary.