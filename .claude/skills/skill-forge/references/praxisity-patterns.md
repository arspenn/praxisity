# Praxisity Skill Patterns

Read this reference when building or revising a skill for the Praxisity framework. It extends the general skill-building guidance in skill-forge's SKILL.md with the conventions every Praxisity skill follows. The five workflow skills (`charter`, `describe`, `design`, `detail`, `do`) are the worked examples; when this reference and a skill disagree, the skill is probably newer, and this file should be fixed.

Last rebuilt 2026-10-08 after the consolidation rewrite.

## Two Skill Types

**Workflow skills** drive one phase of Describe → Devise → Detail → Do, with `/charter` as the entry point. They are user-invoked only (`disable-model-invocation: true`) and converse with the user throughout, so they must never be given `context: fork`. Four produce a document from a template:

```
Pre-Flight → Introduction → Gather → Review and Confirm → Generate → Post-Save → Completion Gate → Success Message
```

`/do` executes a DIP instead and has its own shape:

```
Pre-Flight → Execute → Acceptance → Completion Gate → Safety and Commit → Success Message
```

**Support skills** provide cross-cutting capabilities the agent uses in any session and auto-invoke when context matches: `gather` (the input protocol), `consult-team` (agent dispatch), `agent-authoring`, `skill-forge` (this skill).

## Skeleton of a Document-Producing Workflow Skill

Each heading below names what the five skills have in common. Copy the shape; write the content for the new skill.

**Frontmatter.** `name`, a `description` that says what the skill produces and when to run it (one sentence; for a support skill, make it pushy so the platform triggers it), `disable-model-invocation: true`, and, when the skill takes an argument, an `argument-hint` showing the accepted forms (`charter` takes none).

**Opening.** One paragraph: what the artifact is and who reads it. Then a bold **Template** line (the `${CLAUDE_SKILL_DIR}/templates/...` path, declared once and called "the template" after that, "read-only input shared by every future run"; `charter` lists five) and, when the skill takes an argument, a bold **Argument** line (what the text after the slash command means, available as `$ARGUMENTS`, with each accepted form spelled out and a rule for ambiguous forms such as bare numbers).

**Rules.** A handful of bullets, each carrying its reason: gather only what fills the template (the template defines the artifact's shape); which sections are required and that the rest are marked, not deleted (so a reader sees they were considered); and, for skills whose artifact carries IDs or has a parent, the ID rule, the gate rule, the cite rule, and the one-parent rule (`charter` has none of those and runs three bullets). Then a maintainer note in an HTML comment that the skill must not be forked, and the PLANNING.md contract line (below), verbatim.

**Pre-Flight.** Numbered, with the sentence "Run these steps in order and finish each before starting the next" and the reason (step 2 lands first so an interrupted run leaves PLANNING.md accurate). Steps 1 and 2 are always PLANNING.md read and write; step 3 invokes `gather` with the Skill tool; then the skill-specific steps: decide new or revise, select the parent document, read parents in full, read the charter if present, read the template last. Every branch that stops sets PLANNING.md Status to `cancelled`.

**Introduction.** "Keep this under five sentences." What the artifact is, one-section-at-a-time, skipping and TBD allowed, then the source-material invitation as gather describes.

**Gather.** One sentence pointing at gather and the template comments, then a pacing table: Section | Pacing | Skill-specific notes. Pacing uses gather's four terms and their compounds. Derived sections come last. Below the table, the update flow paragraph.

**Review and Confirm.** Compact outline, counts, markers, and the gate result. `(y)es save`, `(e)dit a section`, `(c)ancel`, with the save option withheld while a gate is open and the gate's exits named instead.

**Generate.** Open with the copy-then-edit rule and its reason: copy the template, then Edit the copy, because Edit keeps the template's structure as ground truth while regenerating the file with Write reproduces it from memory and drifts (renamed headers, dropped sections, half-stripped comments, renumbered IDs). Then numbered steps: in update mode, re-read the existing artifact immediately before the copy overwrites it; `cp` in Bash to the destination; read the copy; apply only the four permitted Edit operations, named as a closed list: **placeholder substitution** (bracketed placeholders and number tokens), **comment stripping** (all HTML comments), **marking** (N/A or TBD in place of a skipped section's content, section kept), **row and block adjustment** (table rows and repeated blocks to fit the content); set metadata (dates, author, status, revision row).

**Post-Save.** Offers only, in one message, nothing done without a yes. Commit offers use a conventional message naming the artifact ID where there is one (`charter: create project charter` has none).

**Completion Gate.** PLANNING.md Status `complete` and Next Steps naming the artifact. State that it is a hard gate and why: the success message waits for it because the next session reads PLANNING.md before anything else. One line stating what a cancellation must already have written.

**Success Message.** "Show all of the following:" the artifact, the counts, and next steps that are gated on the next skill being installed.

## The PLANNING.md Contract

Every skill carries this line verbatim under Rules, because a plugin cannot assume a shared reference file is installed:

> **PLANNING.md contract.** PLANNING.md has an `## Active Context` block with **Last Command**, **Status**, and **Date**, and a `## Next Steps` list. Skills set Status to `in progress`, `complete`, or `cancelled`.

A skill touches PLANNING.md three times: read in pre-flight step 1 (create per the contract if missing, and say so), write `in progress` in step 2, write `complete` or `cancelled` at the gate. Active Context is overwritten by the next skill's step 2; Next Steps survives until the next completion gate rewrites it, which is why skills read it for defaults (the active spec, design, or DIP) but never as a record. Durable state that another skill must read later lives in the artifact itself (a DIP's Status row, a design's Revision History), with Next Steps as a pointer only.

## Gather Terms

The `gather` skill owns the pacing vocabulary and defines it; a workflow skill's pacing table uses its four terms by name (**One prompt**, **Checklist**, **One at a time**, **Drafted by you**) and their compounds ("Two prompts: In, then Out", "Drafted, then one prompt", "Drafted outline, then one at a time"), so all skills render the same way. Two Praxisity-specific additions: a derived section that is a citation of a parent (inherited constraints, inherited out-of-scope) is drafted regardless of the user's gathering-style preference, because there is nothing to decide; and an unanswered checklist category is marked N/A in a prose section, produces no row in a table section, and leaves a sub-headed empty table N/A on its own.

## Markers, IDs, and Gates

**Two markers** stand in for content and are never a reason to delete a section: `N/A — [reason]` when it does not apply, `TBD — revisit at [milestone]` when it cannot be known yet. Update flows use TBD markers as their target list.

**IDs** are assigned the moment the user approves an item, take the highest number ever used in that series plus one, and are never renumbered; a removed item keeps its row or block header with the ID struck through and the version. Steps inside a DIP are the exception: nothing outside the DIP cites a step, so they renumber freely while the DIP is Ready or Halted.

**Gates** are coverage rules checked at Review and Confirm: every MUST requirement has an acceptance criterion (`describe`), every MUST is covered by an element, design-wide, or a declared gap (`design`), every step has a Verify and every MUST a tested criterion (`detail`). A gate withholds the save option and names its exits in the confirm message; it never says "flag" and never lets the agent draft its own escape.

**One parent per child.** One spec per design, one design per DIP. Split or merge rather than cite two. Placeholder tokens for a parent's number are distinct from the child's (`NNN` for the document, `MMM` for the spec, `DDD` for the design), and a token followed by `-slug` is the filename stem.

## Reference Conventions

Every Praxisity document uses the same four reference forms. The canonical text is the block below; every template carries it verbatim in its header comment (it is stripped from output, so finished documents do not restate it), and skills apply the forms at generate time. Copy it from here or from any template; do not paraphrase it.

```
Reference conventions, identical in every Praxisity template:
- An element with an ID from another document: the ID plus a short label in parentheses,
  always in tables and Satisfies lists, and on first mention under each heading in prose:
  REQ-F1 (search latency). The label is two to four words, coined by the first document
  that cites the element and reused verbatim after that. Qualify with the document ID when
  more than one parent is in play: SPEC-003 REQ-F2. IDs from this same document are never
  labeled.
- A section: section sign, then number or name, then title: §7.4 Non-Functional Approach,
  §Scope. When the section is in another document, link the document first:
  [CHARTER.md](../../CHARTER.md) §Scope.
- Another document: a relative markdown link, from this file, whose text is the document
  ID or file name: [SPEC-005](../specs/005-agent-consultation-system.md).
- A removed item: its ID struck through, with the version, wherever it appears:
  ~~REQ-F3~~ (removed v0.2).
```

**The cite rule has no exceptions.** A child document cites its parents by ID with a label and adds only what is specific to itself (a design's approach, a DIP's test). Text is never copied from a parent, because a parent revision would leave the copy stale. Step bodies in a DIP are the one place that is written in full, because the executor acts on them directly.

## Template Conventions

- Every template lives in its skill's `templates/` directory; nothing a skill uses lives anywhere else. A template with no owning skill is parked in `.praxisity/templates/` and does not ship in the plugin (currently `adr.template.md`, awaiting `/decide`).
- The template owns per-section guidance in HTML comments: what the section needs and examples from several fields, including instructional design. The skill's pacing table carries only skill-specific notes, so the two cannot drift.
- Domain-specific content is generalized into transferable questions with per-field examples in the comment (the charter's Domain Context, the design's Architecture), never into parallel per-domain blocks.
- Placeholder rows and blocks are illustrative; the header comment says so, and the Generate operations include row and block adjustment.
- The reference-conventions block and the two-markers note appear in every template header.
- Copy-then-edit is absolute: `cp`, read, then one Edit per H2 section (an `old_string` never crosses a heading, so a whole-body replacement is impossible by construction) with a closed list of operations, strip HTML comments (a gitignore's `#` lines are content). Never Write a template-derived file.
- The Generate phase ends by running `scripts/check-template-structure.sh` (bash, awk, grep, sed only; no Python) (template, output, `--repeat` for templates with repeating blocks) and showing its output; `STRUCTURE CHECK OK` is the acceptance condition, not the agent's assertion. Identical copies of the script live in every template skill; edit all of them together.

## The Status Lifecycle of a DIP

Needed only when editing `/detail` or `/do`, which write and read these values; other skills do not touch them. `/detail` sets `Ready`. `/do` sets `In Progress` at start, `In Progress — Step N passed` (or `skipped`) after each step, `Halted — Step N: [reason]`, `Halted — Acceptance: AC-n [reason]`, or `Halted — Verification: [reason]` when stopped, and `Done` at the end. A Ready or Halted DIP may be revised (`/detail` returns it to Ready and writes "resume at Step K" or "resume at Acceptance" in the Revision History row); an In Progress or Done DIP gets a follow-up DIP that names it under Follows. Bookkeeping edits (a DIP's Status and Notes, PLANNING.md, CHANGELOG.md) are outside the scope check and are committed with the work. Nothing in a DIP is ticked; live progress is the task list, the permanent record is the commit body.

## Memory-as-Settings

A skill that needs per-project preferences checks project memory for a named file on every run and applies it silently. On first use it applies stated defaults, tells the user in one line how to change them mid-session, saves the defaults, and updates the file whenever the user changes a preference. No calibration questionnaire: `gather` is the worked example.

## Agent Consultation

Workflow skills do not carry an Agent Consultation section; it was unreachable where it sat. Where a review is worth suggesting (after a charter, spec, or design), the success message's next steps mention `consult-team` when it is installed and name the agent whose perspective fits (critic or skeptic after a spec, designer or skeptic after a design); `detail` and `do` do not suggest one. Reviewing a new skill before it ships: dispatch prompt-engineer, critic, user-advocate, and spot in Mode 2, two rounds; they hold checklists in agent memory from the consolidation reviews.

## Dual-Use Output

Every produced document is read by people and by the AI, so it must stand alone: every specialized term is defined in a glossary or self-evident; governance documents state principles, not bug IDs; a reader with no project context can follow it.

## Naming

- Workflow skills are named for the verb of their phase: charter, describe, devise, detail, do. The artifact keeps its own name (`/devise` writes a design, `/detail` writes a DIP).
- **Before naming any skill, check the built-in command list** at https://code.claude.com/docs/en/commands (and type `/` in a session on the current version). A bare plugin skill name resolves only when no built-in uses it, so a collision sends the user to Anthropic's command, not ours. Two collisions found so far by accident: `plan` (plan mode) and `design` (the bundled mockup skill added in 2.1.265). Also avoid near-synonyms of an existing phase.
- Support skills are named for what they enable: gather, consult-team, skill-forge, agent-authoring.
- Artifacts: `SPEC-NNN`, `DESIGN-NNN`, `DIP-NNN`, with files `.plans/specs/NNN-slug.md`, `.plans/designs/NNN-slug.md`, `.plans/prompts/NNN-slug.md`. Element IDs within them: OBJ, REQ-F, REQ-N, UC, AC, Q (spec); COMP, INT, DATA, DEC, DQ (design).
- Commit messages: `charter:`, `spec(slug):`, `design(slug):`, `dip(slug):`, each naming the artifact ID.

## What to Carry Into the Next Skill

`/decide` is the first skill after consolidation (an ADR from the parked template). It should follow the document-producing skeleton above, treat the ADR as a child of nothing (no parent, no coverage gate), and cite the designs or specs whose decisions it records by the reference convention.