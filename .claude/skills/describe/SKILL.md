---
name: describe
description: Create or revise a specification (SPEC-NNN) that defines what will be built and how you will know it is done. Produces requirements, use cases, and acceptance criteria with IDs that designs and implementation prompts cite.
disable-model-invocation: true
argument-hint: "[title, or an existing SPEC-NNN to revise]"
---

# Describe

Create or revise a specification. A spec defines WHAT will be built and how you will know it is done; the HOW comes later in a design. Every objective, requirement, use case, acceptance criterion, and open question carries an ID so the design and the Detailed Implementation Prompts (DIPs) that follow can cite it exactly.

**Template:** `${CLAUDE_SKILL_DIR}/templates/spec.template.md`. The template is read-only input shared by every future run; all edits target the spec file in `.plans/specs/`.

**Argument:** the text the user typed after `/describe`, if any, available as `$ARGUMENTS`.

## Rules

- Gather only what fills the template. The template defines the spec's shape; the skill does not add sections.
- Problem Statement and Out of Scope are required. Every other section may be skipped, marked rather than deleted so a reader sees it was considered: `N/A — [reason]` when it does not apply, `TBD — revisit at [milestone]` when it cannot be known yet. Tell the user both markers exist. In a checklist over a table section, an unanswered category simply produces no row. When a section has subsections that are each a table (Dependencies has 7.1 Depends On and 7.2 Enables), a subsection with no rows is marked N/A on its own; the whole section is N/A only when nothing applies.
- **IDs are assigned the moment the user approves an item and are never renumbered.** OBJ-n, REQ-Fn, REQ-Nn, UC-n, AC-n, Q-n take the highest number ever assigned in their series plus one, in both new and revise mode; a removed item's number is never reissued. This is the rule that lets designs and DIPs cite a requirement and trust the citation next month.
- Every MUST requirement needs at least one acceptance criterion. The Acceptance Criteria section may be TBD only with a milestone, carried into Next Steps; otherwise an uncovered MUST blocks saving until the user adds a criterion or lowers the priority.

<!-- Maintainer note: this skill converses with the user throughout, so it must not be given `context: fork` in frontmatter. -->

**PLANNING.md contract.** PLANNING.md has an `## Active Context` block with **Last Command**, **Status**, and **Date**, and a `## Next Steps` list. Skills set Status to `in progress`, `complete`, or `cancelled`.

## Pre-Flight

Run these steps in order and finish each before starting the next. Step 2 lands first so that an interrupted run still leaves PLANNING.md accurate, and step 4's outcome changes what the later steps mean.

1. Read PLANNING.md. If it is missing, create it per the contract above and tell the user you keep it as a session log.
2. Update PLANNING.md: Last Command `/describe`, Status `in progress`, Date today.
3. Invoke the `gather` skill with the Skill tool so its protocol is in context before the first section is presented.
4. Decide new or revise. List `.plans/specs/` with `ls` in Bash (create the directory if missing). If the argument is an existing spec number (`SPEC-006` or bare `006`), or the user asks to revise a spec, read that spec in full and run the update flow; if two files share the number, ask which. If the argument loosely matches an existing spec's title, ask once: revise that one, or start a new spec? Otherwise this is a new spec: its number is the highest existing NNN plus one, and the argument, if any, is the working title. To cancel here, set PLANNING.md Status to `cancelled` and stop.
5. Read CHARTER.md if it exists: the mission, principles, constraints, and Out of Scope feed the spec's Problem Statement, Charter Reference, Constraints, and Out of Scope. If it does not exist, say so once and offer two choices: continue without it (the charter-derived fields are marked `N/A — no charter`), or stop now with Status `cancelled` so the user can run `/charter` and come back.
6. Read the template. Its HTML comments define what each section needs and carry the examples.

## Introduction

Keep this under five sentences. Say what a spec is (what, not how), that you will go one section at a time, and that skipping and TBD are allowed. Then invite source material as the gather protocol describes. Say which source feeds what: an assignment brief or proposal yields requirements; a rubric yields acceptance criteria, and each criterion drafted from a rubric cites its rubric row. Read what the user provides before gathering begins.

## Gather

Gather in the order of the table below, which follows the template except that derived sections come last. Follow the gather protocol, including its purpose sentence before each prompt; the template comment for each section says what it needs. Use the vocabulary of the project's field, taken from the charter's Domain Context or asked once. Pacing uses the gather protocol's terms:

| Section | Pacing | Spec-specific notes |
|---------|--------|---------------------|
| Title | One prompt | Skip if given as the argument. Author defaults to `git config user.name`; if that is unavailable, ask for it here. |
| Problem Statement | One prompt | Required. Source material and the charter mission count as loaded documents for the gather drafting rule. |
| Primary Goal | One prompt | One sentence. |
| Objectives | One prompt | A short list, each with its metric. Project objectives, not a course's learning objectives; the template comment explains the difference. Assign OBJ-n on approval. |
| Functional Requirements | One at a time until the user says done | Each is a decision: the requirement, its priority, and why. Assign REQ-Fn on approval. |
| Non-Functional Requirements | One prompt, categories as a checklist | Performance · Security · Usability/Accessibility · Compliance · Maintainability. Nudge toward accessibility for anything learners or the public will use. Assign REQ-Nn on approval. |
| Use Cases | One at a time until the user says done | Frame each in the field's vocabulary per the template comment. One well-drawn scenario beats three thin ones. Assign UC-n on approval. |
| Acceptance Criteria | Drafted by you | At least one per MUST, Given/When/Then, each citing the requirement ID it validates and the rubric row if one exists. Invite the user to write one themselves for a SHOULD; it is the skill they will need most. Assign AC-n on approval. |
| Constraints | Drafted, then one prompt | 6.1 Inherited is drafted regardless of gathering style because it is a citation of the charter. Then prompt once for spec-specific constraints. |
| Dependencies | One prompt, two categories as a checklist | Depends On · Enables. N/A is common for a first spec. |
| Out of Scope | One prompt | Required, at least one item. Draft from the charter's Out of Scope plus anything the user ruled out while discussing requirements. |
| Open Questions | One prompt | Optional. Anything the user hedged on earlier is a candidate; list those as a draft. Assign Q-n on approval. |
| Charter Reference, Related Documents, References | Drafted by you | Charter Reference names the charter principles this spec serves. Related Documents come from Dependencies, as relative links from `.plans/specs/`. References come from source material plus the charter. Present together for approval. |

**Update flow (revising an existing spec).** Ask "What has changed since [Last Updated date]?" and show a one-line index of sections with any TBD, N/A, or Open question flagged. Walk the sections the user's answer touches, every TBD section, every Open question, and any section whose structure differs between the existing spec and the current template (present the old content mapped into the new fields as a draft). Then offer a quick pass over the rest. A removed item keeps its row with the ID struck through and the version, per the template's reference conventions, so any design or DIP that cites the ID still resolves. Re-derive acceptance criteria coverage for any changed MUST. The filename and Status stay as they are unless the user changes them. In update mode, "skip" means keep the existing content unchanged.

### Review and Confirm

Show a compact outline: each section header with a one-line summary, the counts of requirements (MUST / SHOULD / COULD), use cases, acceptance criteria, and open questions, the count of TBD and N/A markers, and any MUST without an acceptance criterion. Not the full text; the user just approved it section by section. Offer **(y)es save**, **(e)dit a section**, or **(c)ancel**. While any MUST is uncovered, offer instead: write a criterion for it, mark the Acceptance Criteria section TBD with a milestone, lower the requirement to SHOULD, or cancel. An edit that removes an item retires its ID; nothing renumbers. Struck-through items do not count toward coverage. On cancel, set PLANNING.md Status to `cancelled` and stop.

## Generate the Spec File

Copy the template, then Edit the copy, one section at a time. Edit's guarantee is that everything outside `old_string` survives verbatim; a whole-body replacement leaves nothing outside it and is a Write under another name, which is how templates drift (renamed headers, dropped sections, half-stripped comments, renumbered IDs).

1. In update mode, re-read the existing spec now, immediately before the copy overwrites it, and note its Created date, Author, Status, Revision History, the content of every section the user kept, and every struck-through row.
2. New spec: derive the slug from the title (lowercase, hyphens, no punctuation) and copy the template to `.plans/specs/NNN-[slug].md` with `cp` in Bash, NNN zero-padded to three digits. Update: copy the template over the existing file with `cp` in Bash.
3. Read the fresh copy.
4. Edit one H2 section per call: `old_string` runs from the section's heading to the line before the next heading, never across one. Within a section, apply only these operations:
   - **Placeholder substitution:** replace `[bracketed placeholders]` and `NNN` with gathered content, writing each item's already-assigned ID and every reference per the template's reference conventions.
   - **Comment stripping:** remove all `<!-- ... -->` blocks.
   - **Marking:** for a skipped section, replace its placeholder content with `N/A — [reason]` or `TBD — revisit at [milestone]`. The section stays. With no charter, Charter Reference and the inherited constraints are `N/A — no charter` and the charter link in References is removed.
   - **Row and block adjustment:** add or remove table rows and repeat the UC block once per use case, to fit the content. Template counts are illustrative.
5. Set metadata. New spec: Status `Draft`, Created and Last Updated today, Author as gathered, Revision History row `0.1 — Initial draft`. Update: keep Created, Author, and Status, set Last Updated today, and append a Revision History row with the next minor version (0.1 → 0.2) and a one-line summary naming the IDs added, changed, or removed.
6. Run the structure check and show its output: `bash ${CLAUDE_SKILL_DIR}/scripts/check-template-structure.sh ${CLAUDE_SKILL_DIR}/templates/spec.template.md .plans/specs/NNN-[slug].md --repeat` (`--repeat` because use-case blocks and table rows legitimately repeat). Proceed only on `STRUCTURE CHECK OK`; on a failure, fix the named sections with further single-section Edits and run it again. The check's output is the evidence; do not assert the structure matches without it.

## Post-Save

If the project is a git repository, offer to commit the spec with `spec([slug]): add SPEC-NNN` or `spec([slug]): revise SPEC-NNN to v[version]`. Do nothing without a yes.

## Completion Gate

Update PLANNING.md: Status `complete`, and Next Steps naming the spec file, any TBD milestones, and any Open questions. This is a hard gate: do not show the success message until PLANNING.md is updated, because the next session reads PLANNING.md before anything else.

If the user cancelled at any earlier point, PLANNING.md must already read `cancelled` for the same reason.

## Success Message

Show all of the following:
- The spec file path and ID, and whether it was created or revised.
- Counts: requirements (MUST / SHOULD / COULD), use cases, acceptance criteria, open questions, TBD markers.
- Next steps:
  1. Read the spec once as a reviewer rather than its author; check that every MUST is something you would refuse to submit or ship without.
  2. Resolve or explicitly defer each Open question before design.
  3. If the Praxisity agent roster is installed in this project, a critic or skeptic pass through `consult-team` catches scope creep and weak requirements before they harden into a design. If it is not, `/agent-authoring` installs it.
  4. If the `devise` skill is installed, start the design with `/devise`; it will cite these IDs.
