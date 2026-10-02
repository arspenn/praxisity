# Praxisity Skill Patterns

Read this reference when building a skill for the Praxisity framework. These patterns extend the general skill-building guidance in the main SKILL.md with framework-specific conventions.

## Two Skill Types

Praxisity distinguishes workflow skills from support skills:

**Workflow skills** drive a specific phase of the design-first workflow (Describe → Design → Detail → Do). They are user-invoked only (`disable-model-invocation: true`). Each workflow skill follows a standard phase structure:

```
Pre-Flight → Gather → Generate-from-template → Post-Save → Completion Gate → Success Message
```

Exception: `/do` is an execution skill with a different structure (Pre-Flight → DIP Execution → Completion Gate → Success Message).

**Support skills** provide cross-cutting capabilities that the agent uses during any session. They auto-invoke when context matches. Examples: `/gather` (structured input protocol), `/consult-team` (agent dispatch), `/skill-forge` (this skill).

## Behavioral Standards

Praxisity workflow skills embed behavioral standards at phase boundaries. These standards were codified from empirical testing and address specific failure patterns.

### Inline Mechanical Standards

These appear at the top of the phase they govern, directly in the SKILL.md:

**Pre-Flight (REQ-F2):**
> Execute these steps sequentially in the order listed. Do not begin step N+1 until step N is complete. Do not batch or parallelize pre-flight steps.
>
> 1. Read PLANNING.md for session context. Create if missing.
> 2. Update PLANNING.md: set active skill to `/[name]`, status to "in progress". This must complete before step 3.
> 3. [Skill-specific steps...]

**Generate (REQ-F1):**
> Copy the template to the destination, then use Edit for all modifications. Never use Write for template-derived files.
>
> Permitted operations: placeholder substitution, domain section removal, HTML comment stripping, N/A marking, content population, table row adjustment. Nothing else.

**Completion Gate (REQ-F5):**
> Update PLANNING.md with completion status, active artifacts, and suggested next steps. This is a hard gate — do not display the success message until PLANNING.md has been updated in this run.

### Support Skill for Judgment Standards

The gathering protocol (REQ-F3) is implemented as the `/gather` support skill rather than inline text. It auto-invokes during gathering phases. Workflow skills reference it as a fallback: "follow the gathering protocol (see /gather)."

### Per-Skill Success Messages (REQ-F4)

Each skill defines its own success message checklist. The standard structure:

```markdown
## Success Message

Show all of the following:
- [Confirmation of what was saved/done]
- [What the output guides/enables]
- Next steps:
  1. [First suggested action]
  2. [Second suggested action]
```

## Template Conventions

- End-user templates (output structure) are bundled with skills in `templates/`
- Development templates (framework infrastructure for building the framework) stay in `.praxisity/templates/`
- Templates use HTML comments as gathering guides — the agent reads them during the Gather phase
- Template example counts are illustrative, not prescriptive — never anchor output quantity to template examples

## Memory-as-Settings Pattern

Skills that need per-project configuration use the Claude Code agent SDK memory system:

1. On every invocation, check project memory for relevant preferences
2. If found → load and apply silently
3. If not found → first invocation; run calibration as a natural part of the flow
4. Store preferences in main project memory (MEMORY.md) per official documentation
5. Preferences persist across sessions, subagent calls, and skill invocations

Calibration questions should be fixed (not improvised), binary, and conversational — not a configuration wizard.

## PLANNING.md Integration

Every workflow skill touches PLANNING.md exactly 3 times:
1. **Pre-Flight step 1:** Read for session context
2. **Pre-Flight step 2:** Write active skill status (hard gate before proceeding)
3. **Completion Gate:** Write completion status (hard gate before success message)

## Agent Consultation

Workflow skills include an Agent Consultation section at the end, pointing users to the agent roster for review:

```markdown
## Agent Consultation

For a quick perspective, dispatch a Praxisity agent:
`Agent(subagent_type: "[relevant-agent]", prompt: "[relevant question]")`

For multi-perspective review, use the consult-team skill.
```

## Dual-Use Output

All output documents follow the dual-use design principle — they are both human governance AND AI prompt context. This means:
- Every specialized term must be defined (glossary section) or self-evident
- Don't reference implementation evidence (bug IDs, version numbers) in governance documents — state principles conceptually
- The document must make sense to a reader with no project context

## Reference Conventions (2026-09-23)

Every Praxisity document uses the same four reference forms. Each template carries the identical block in its header comment (copy it verbatim into any new template; it is stripped from output, so finished documents do not restate it); skills apply the forms at generate time.

| Referring to | Form | Example |
|--------------|------|---------|
| An element with an ID from another document | ID plus a short label in parentheses, always in tables and Satisfies lists, and on first mention under each heading in prose. Label is two to four words, coined by the first citing document, reused verbatim downstream. Qualify by document when more than one parent is in play. Same-document IDs are never labeled. | `REQ-F1 (search latency)`, `SPEC-003 REQ-F2` |
| A section | Section sign, then number or name, then title; link the document first when it is elsewhere | `§7.4 Non-Functional Approach`, `[CHARTER.md](../../CHARTER.md) §Scope` |
| Another document | Relative markdown link, from the citing file, whose text is the document ID or file name | `[SPEC-005](../specs/005-agent-consultation-system.md)` |
| A removed item | Its ID struck through, with the version, wherever it appears | `~~REQ-F3~~ (removed v0.2)` |

IDs are assigned when the user approves an item, take the highest number ever used in their series plus one, and are never renumbered. One parent document per child (one spec per design, one design per DIP); split or merge rather than cite two.

## Naming Conventions

- Workflow skills: named for the verb of the phase (charter, describe, design, detail, do). "Detail" was chosen over "plan" (collides with Claude Code's plan mode) and "define" (overlaps with describe, and names the scoping stage in instructional design vocabulary).
- Support skills: named for what they enable (gather, consult-team, skill-forge)
- Prototype commands (being sunset): prefixed with `_prototype-` in `.claude/commands/`
