---
name: skill-forge
description: Guide the creation of well-structured Claude Code skills. Covers directory layout, frontmatter configuration, prompt engineering for dual-use skill files, template bundling, and testing strategy. Use when creating a new skill or restructuring an existing one.
---

# Skill Forge

Guide the creation of a new Claude Code skill. A skill is a directory-based prompt specification that the platform loads as agent instructions — it shapes how Claude works, not what Claude knows.

## Before You Start

1. **Clarify the skill's purpose.** What does this skill help the agent do? A skill is instructions for behavior, not a knowledge document.
2. **Determine the skill type:**
   - **Workflow skill** (`disable-model-invocation: true`): User-invoked via `/name`. Drives a specific process the user initiates. Examples: creating a document, running a pipeline, executing a plan.
   - **Support skill** (default, auto-invokable): The agent loads it automatically when the context matches the skill's description. Examples: gathering protocols, consultation dispatch, code review patterns.
3. **Check for Praxisity-specific patterns.** If building a skill for the Praxisity framework, read `${CLAUDE_SKILL_DIR}/references/praxisity-patterns.md` for framework conventions before proceeding.

## Progressive Loading Model

Skills use a three-level loading system:

1. **Metadata** (name + description) — always in context, ~100 words. This is what the platform uses for auto-invocation decisions.
2. **SKILL.md body** — loaded when the skill triggers. Keep under 500 lines. If approaching this limit, move detailed reference material to files in `references/` with clear pointers about when to read them.
3. **Bundled resources** (templates/, references/, scripts/) — loaded on demand when the skill instructs the agent to read them. Unlimited size.

The key principle: metadata is always visible, the skill body is loaded on trigger, and resources are read only when needed at the right phase.

## Skill Directory Structure

Every skill is a directory under `.claude/skills/`:

```
.claude/skills/[skill-name]/
├── SKILL.md                    ← required: the skill's instructions
├── templates/                  ← optional: output templates bundled with the skill
│   └── [name].template.md
└── references/                 ← optional: supporting documents the skill reads at specific phases
    └── [name].md
```

- **SKILL.md** is the only required file. It contains frontmatter + the full behavioral specification.
- **templates/** holds output templates the skill copies and fills. Bundle templates with the skill for self-containment — don't reference distant paths.
- **references/** holds supporting documents the skill reads at specific phases. Use `${CLAUDE_SKILL_DIR}/references/[name].md` to reference them.

## Frontmatter

The YAML frontmatter configures how the platform handles the skill.

**Supported fields (verified):**

| Field | Purpose | Default |
|-------|---------|---------|
| `name` | Display name, becomes the `/slash-command`. Lowercase, hyphens, max 64 chars. | Directory name |
| `description` | What the skill does and when to use it. The platform uses this for auto-invocation context matching. Front-load the key use case. Max ~250 chars before truncation. | Required |
| `disable-model-invocation` | Set `true` to prevent auto-invocation. Use for workflow skills the user must explicitly trigger. | `false` |
| `user-invocable` | Set `false` to hide from the `/` menu. Use for background knowledge skills. | `true` |
| `allowed-tools` | Restrict which tools the agent can use during this skill. Space-separated or YAML list. | All tools |
| `argument-hint` | Hint shown during autocomplete for expected arguments. | None |

**Not supported (do not use):**
- `when_to_use` — not a valid field. Auto-invocation uses the `description` field.
- `tags` — command-era field, not supported in skills.

**How auto-invocation works:** The platform matches conversation context against skill descriptions to decide which skills to load. Important: Claude only consults skills for tasks it can't easily handle on its own. Simple, one-step queries may not trigger a skill even if the description matches — the agent handles them directly with basic tools. Complex, multi-step, or specialized queries trigger skills reliably. Design descriptions accordingly — front-load the key use case and include specific contexts where the skill adds value.

**Path variable:**
- `${CLAUDE_SKILL_DIR}` — resolves to the skill's directory at runtime. Use for referencing bundled files. Verified working.

## Writing the SKILL.md Body

The body of SKILL.md is the agent's instructions. It is both a human-readable document and a prompt the AI follows. Write with both audiences in mind.

### Structure

1. **Title and purpose** — one line explaining what this skill does.
2. **Constraints** — behavioral limits. What the skill must NOT do. Keep this short and specific.
3. **Phases** — the steps the agent follows, in order. Name them clearly (Pre-Flight, Gather, Generate, etc.).
4. **Success criteria** — what "done" looks like. A checklist the agent can verify.

### Prompt Engineering Principles

**Positive framing over prohibitions.** Instead of listing what not to do (which teaches the failure mode), use verification checks: "Before sending, verify: [checklist]." Negative lists activate the exact representation they're trying to suppress.

**Observable gates over self-assessment.** Don't say "when you have sufficient context" — the agent always thinks it does. Say "when the user has already provided direct input on this topic" or "when loaded documents explicitly cover this section." Gates must be verifiable, not judgment calls.

**Phase-boundary placement.** Instructions are most effective when they appear immediately before the phase they govern. An instruction at line 5 may be forgotten by line 100. Place behavioral rules at the top of the section they apply to.

**Imperative language for sequencing.** Numbered lists alone don't prevent parallelization. Add explicit: "Execute sequentially. Do not begin step N+1 until step N is complete."

**Explain the why, not just the what.** When instructing behavior, explain the reasoning behind the instruction. AI agents with good theory of mind follow reasoned instructions more reliably than rigid directives. If you find yourself writing ALWAYS or NEVER in all caps, consider reframing with the reasoning instead. That said, some rules ARE mechanical and benefit from imperative framing — the balance is: explain the why for judgment calls, use imperatives for binary rules.

**Compression over explanation.** Keep instructions minimal. If context is needed for a judgment call, consider whether it belongs in the skill body or in a reference file read at the right moment.

### Template Bundling

If the skill produces output from a template:

1. Bundle the template in the skill's `templates/` directory.
2. Reference it with `${CLAUDE_SKILL_DIR}/templates/[name].template.md`.
3. In the Generate phase, instruct: copy via `cp`, read the copy, modify with Edit only.
4. Define permitted Edit operations explicitly — a closed list of what the agent may change.
5. Verify the original template is unchanged after generation.

Template HTML comments serve as gathering guides — the agent reads them during the Gather phase to understand what each section needs, then strips them during Generation.

### Update Flow

If the skill can be run on existing output (updating a document rather than creating from scratch):

1. Pre-Flight checks if the output already exists.
2. Offer the user options: review and update, start fresh, or cancel.
3. The update flow reads existing content and presents each section's current content as a draft for approval or revision.
4. Preserve metadata from the original (e.g., "established" dates) while updating "last reviewed" dates.

Design the update flow explicitly from the start — it's as important as the creation flow.

## Testing Strategy

1. **Live test before validation.** Agent reviews catch structural and consistency issues. Live testing catches interaction issues — missing sections, awkward flows, underspecified update paths. Both are needed.
2. **Test in a fresh session.** If the skill relies on auto-invocation, test it in a session where the agent hasn't been discussing the skill's topic. This validates that the platform's context matching works, not just that the agent remembers the conversation.
3. **Verify template integrity.** After generation, confirm the bundled template is unchanged. This is the fundamental test for copy-then-edit compliance.
4. **Check dual-use.** Read the output document cold. Does it make sense without project context? If it references terms without defining them, add a glossary.