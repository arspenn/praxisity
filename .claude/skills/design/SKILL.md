---
name: design
description: Create or revise a design document (DESIGN-NNN) that defines how a specification will be built. Produces components, interfaces, data entities, and decisions with IDs, each traced to the spec requirements it satisfies.
disable-model-invocation: true
argument-hint: "[SPEC-NNN to design for, or DESIGN-NNN to revise]"
---

# Design

Create or revise a design. A design defines HOW the work a specification described will be built: the parts, how they connect, what information they handle, and the decisions that shaped them. Every component, interface, data entity, decision, and open question carries an ID so the Detailed Implementation Prompts (DIPs) that follow can cite it exactly, and every element cites the spec requirements it satisfies.

**Template:** `${CLAUDE_SKILL_DIR}/templates/design.template.md`. The template is read-only input shared by every future run; all edits target the design file in `.plans/designs/`.

**Argument:** the text the user typed after `/design`, if any, available as `$ARGUMENTS`. `DESIGN-NNN` means revise that design. `SPEC-NNN` or a bare number means design for that spec.

## Rules

- Gather only what fills the template. The template defines the design's shape; the skill does not add sections.
- Overview, Architecture, Components, and Requirements Coverage are required. Every other section may be skipped, marked rather than deleted so a reader sees it was considered: `N/A — [reason]` when it does not apply, `TBD — revisit at [milestone]` when it cannot be known yet. Tell the user both markers exist. A subsection that is a table with no rows is marked N/A on its own.
- **IDs are assigned the moment the user approves an element and are never renumbered.** COMP-n, INT-n, DATA-n, DEC-n, DQ-n take the highest number ever assigned in their series plus one, in both new and revise mode; a removed element's number is never reissued. DIPs will cite these IDs and must be able to trust them.
- **Coverage.** Every MUST requirement in the spec must be covered in one of three ways: by at least one component, interface, or data entity that lists it under Satisfies; for a non-functional requirement no single element can own, by its row in Non-Functional Approach, shown in the matrix as design-wide; or, only when the user declares it, by a deliberate gap recorded as an Open Question naming the requirement, the reason, and the milestone at which it will be designed for. You never draft a deliberate gap; the user chooses it. An uncovered MUST withholds the save option.
- One spec per design. If the work spans two specs, split the design or merge the specs first; the spec number, the coverage total, and the commit message all assume one.
- The design cites the spec; it does not restate it. References follow the conventions in the template header: a requirement appears as its ID with a short label, `REQ-F1 (search latency)`, so the design reads without the spec open; a section is `§7.4 Non-Functional Approach`; another document is a relative link; a removed item is its ID struck through with the version.

<!-- Maintainer note: this skill converses with the user throughout, so it must not be given `context: fork` in frontmatter. -->

**PLANNING.md contract.** PLANNING.md has an `## Active Context` block with **Last Command**, **Status**, and **Date**, and a `## Next Steps` list. Skills set Status to `in progress`, `complete`, or `cancelled`.

## Pre-Flight

Run these steps in order and finish each before starting the next. Step 2 lands first so that an interrupted run still leaves PLANNING.md accurate, and steps 4 and 5 decide what the rest of the run is about.

1. Read PLANNING.md. If it is missing, create it per the contract above and tell the user you keep it as a session log.
2. Update PLANNING.md: Last Command `/design`, Status `in progress`, Date today.
3. Invoke the `gather` skill with the Skill tool so its protocol is in context before the first section is presented.
4. Revise, if asked. If the argument is `DESIGN-NNN` or the user asks to revise a design, list `.plans/designs/` with `ls` in Bash, read that design in full, read the spec named in its Specification References in full, and go to step 6 for the update flow. Otherwise continue to step 5 for a new design. To cancel here, set PLANNING.md Status to `cancelled` and stop.
5. Select the spec for a new design. List `.plans/specs/` with `ls` in Bash. If it is empty or missing, say a design needs a spec to design for, set PLANNING.md Status to `cancelled`, and stop with the suggestion to run `/describe` first. If the argument names a spec (`SPEC-NNN` or a bare number), use it; if PLANNING.md's Next Steps names a spec, offer it as the default; otherwise ask once. Read the selected spec in full and hold its requirements (REQ-F, REQ-N with priorities), use cases, acceptance criteria, constraints, Out of Scope, and Open Questions; the whole design is built against them. Then search `.plans/designs/` for the spec's ID with Grep. If a design already implements it, ask once: revise that design (read it and go to step 6 for the update flow) or create an alternative alongside it (the new design's Related Documents will list the existing one as "Alternative to"). A new design's number is the highest existing NNN in `.plans/designs/` plus one.
6. Read CHARTER.md if it exists, for its principles and Domain Context; the field's vocabulary for examples and section framing comes from there. If it does not exist, ask the field once.
7. Read the template. Its HTML comments define what each section needs and carry the examples.

## Introduction

Keep this under five sentences. Name the spec being designed for, how many MUST and SHOULD requirements it holds, and the default title "[Spec title] Design" (the user can change it in one word). Say a design answers how, that you will go one section at a time, and that skipping and TBD are allowed. Then invite source material as the gather protocol describes: an existing architecture, a storyboard, a logic model, a syllabus outline, or notes from a prior attempt all shorten the run. Read what the user provides before gathering begins.

## Gather

Gather in the order of the table below, which follows the template except that derived sections come last. Follow the gather protocol, including its purpose sentence before each prompt; the template comment for each section says what it needs. Use the field's vocabulary throughout. Pacing uses the gather protocol's terms, including compounds such as "three prompts":

| Section | Pacing | Design-specific notes |
|---------|--------|-----------------------|
| Design Summary | One prompt | Draft from the spec's problem and goal plus source material when they cover it. Author defaults to `git config user.name`; if unavailable, ask alongside this section. |
| Design Principles | One prompt | A short list. Draft from the charter's principles as they apply to this piece of work; the user edits. |
| Architecture | Three prompts: Context, Approach, Key Choices | Show the template comment's examples for the project's field even in brief mode; this is the section where a newcomer to design most needs scaffolding. A diagram is welcome, not required. |
| Components | One at a time until the user says done | Each is a decision: what it does, which requirements it satisfies, what it depends on, any decision local to it. Assign COMP-n on approval. After each, show the MUST requirements not yet covered so the user sees the gap close; once the MUST list is empty, show uncovered SHOULDs once. If the user is unsure where to start, offer a candidate list drawn from the spec's use cases. |
| Interfaces | One at a time until the user says done | Ask first, with the template comment's recognition cue: does a result go anywhere, does one part unlock another, does a person hand something to another person? N/A is a legitimate answer. Assign INT-n on approval. |
| Data Model | One at a time until the user says done | Ask first: does the design manage or capture persistent information, including anything a platform stores on its behalf? N/A is legitimate. Nudge toward retention when the data is about people. Assign DATA-n on approval. |
| Design Decisions | One at a time until the user says done | Draft candidates from choices the user made while discussing Architecture and Components; each becomes a DEC block with alternatives named. Assign DEC-n on approval. |
| Non-Functional Approach | Drafted by you | One row per REQ-N in the spec, stating how the design meets it. This is what covers a non-functional MUST no single element owns, so it comes before the gate. |
| Requirements Coverage | Drafted by you | Re-read the spec, then build the matrix from every live element's Satisfies list plus the Non-Functional Approach rows. Show any MUST still uncovered and the three ways to cover it. This is the gate; present it on its own. |
| Implementation Order | Drafted by you | Derive from component dependencies; the order is a decision, so it gets its own approval. |
| Risk Areas | One prompt | Draft from the spec's Open Questions and anything the user called hard. |
| Validation Strategy | One prompt | Levels in the field's terms per the template comment. Draft coverage from the spec's acceptance criteria. |
| Out of Scope | Drafted, then one prompt | Inherited half drafted from the spec's Out of Scope regardless of gathering style, because it is a citation; then prompt once for design-specific exclusions. |
| Open Questions | One prompt | Draft from the spec's still-open questions that the design did not settle. Deliberate coverage gaps appear here only if the user declared them at the gate. Assign DQ-n on approval. |
| Glossary, Specification References, Related Documents, References | Drafted by you, presented together | Glossary from terms used; Specification References with the requirement IDs addressed; Related Documents and References from the spec, source material, and dependencies, as relative links from `.plans/designs/`. One approval for the set. |

**Update flow (revising an existing design).** Ask "What has changed since [Last Updated date]?" and show a one-line index of sections with any TBD, N/A, or Open question flagged. If the spec's Revision History has rows dated on or after the design's Last Updated, list those rows first: they name the requirement IDs added, changed, or removed. A Satisfies entry that cites a removed requirement takes the struck form. For each removed requirement, show any element whose Satisfies list is now empty and ask whether to remove it or re-home it. Before striking an element, search `.plans/prompts/` for its ID with Grep and name any citing DIP in the Revision History row, so `/detail` can see what needs revisiting. Walk the sections the user's answer touches, every TBD section, every Open question, every element affected by a spec change, and any section whose structure differs between the existing design and the current template (present the old content mapped into the new fields as a draft). Then offer a quick pass over the rest. A removed element keeps its block header with the ID struck through and the version, per the reference conventions, so any DIP that cites the ID still resolves. Re-derive the coverage matrix from live elements and the spec's live requirements; struck requirements are not in the total. The filename and Status stay as they are unless the user changes them. In update mode, "skip" means keep the existing content unchanged.

### Review and Confirm

Show a compact outline: each section header with a one-line summary, the counts of components, interfaces, data entities, decisions, and open questions, the count of TBD and N/A markers, and the coverage result: MUSTs covered out of total, and any uncovered. Not the full text; the user just approved it section by section. Offer **(y)es save**, **(e)dit a section**, or **(c)ancel**. While any MUST is uncovered, offer instead: add an element, mark it design-wide if it is a non-functional requirement met by the whole design, record a deliberate gap with a milestone, or cancel (Status `cancelled`) to go revise the spec with `/describe`. An edit that removes an element retires its ID; nothing renumbers. Struck-through elements do not count toward coverage. On cancel, set PLANNING.md Status to `cancelled` and stop.

## Generate the Design File

Copy the template, then Edit the copy, one section at a time. Edit's guarantee is that everything outside `old_string` survives verbatim; a whole-body replacement leaves nothing outside it and is a Write under another name, which is how templates drift (renamed headers, dropped sections, half-stripped comments, renumbered IDs).

1. In update mode, re-read the existing design now, immediately before the copy overwrites it, and note its Created date, Author, Status, Revision History, the content of every section the user kept, and every struck-through element.
2. New design: derive the slug from the title (lowercase, hyphens, no punctuation) and copy the template to `.plans/designs/NNN-[slug].md` with `cp` in Bash, NNN zero-padded to three digits. Update: copy the template over the existing file with `cp` in Bash.
3. Read the fresh copy.
4. Edit one H2 section per call: `old_string` runs from the section's heading to the line before the next heading, never across one. Within a section, apply only these operations:
   - **Placeholder substitution:** replace `[bracketed placeholders]` with gathered content, `NNN` with the design number, and `MMM` with the spec number and slug. Write each element's already-assigned ID, and every reference per the template's reference conventions.
   - **Comment stripping:** remove all `<!-- ... -->` blocks.
   - **Marking:** for a skipped section or subsection, replace its placeholder content with `N/A — [reason]` or `TBD — revisit at [milestone]`. The section stays.
   - **Row and block adjustment:** add or remove table rows and repeat the COMP, INT, DATA, and DEC blocks once per element, to fit the content. In update mode, retained struck-through block headers are written as they were. Template counts are illustrative.
5. Set metadata. New design: Status `Draft`, Created and Last Updated today, Author as gathered, Revision History row `0.1 — Initial draft`. Update: keep Created, Author, and Status, set Last Updated today, and append a Revision History row with the next minor version (0.1 → 0.2) and a one-line summary naming the IDs added, changed, or removed.
6. Run the structure check and show its output: `python3 ${CLAUDE_SKILL_DIR}/scripts/check-template-structure.py ${CLAUDE_SKILL_DIR}/templates/design.template.md .plans/designs/NNN-[slug].md --repeat` (`--repeat` because COMP, INT, DATA, and DEC blocks repeat). Proceed only on `STRUCTURE CHECK OK`; on a failure, fix the named sections with further single-section Edits and run it again. The check's output is the evidence; do not assert the structure matches without it.

## Post-Save

If the project is a git repository, offer to commit the design with `design([slug]): add DESIGN-NNN for SPEC-MMM` or `design([slug]): revise DESIGN-NNN to v[version]`. Do nothing without a yes.

## Completion Gate

Update PLANNING.md: Status `complete`, and Next Steps naming the design file, the spec it implements, any TBD milestones, and any Open questions. This is a hard gate: do not show the success message until PLANNING.md is updated, because the next session reads PLANNING.md before anything else.

If the user cancelled at any earlier point, PLANNING.md must already read `cancelled` for the same reason.

## Success Message

Show all of the following:
- The design file path and ID, the spec it implements, and whether it was created or revised.
- Counts: components, interfaces, data entities, decisions, open questions, TBD markers, and MUST coverage (covered out of total, with any design-wide or deliberate-gap entries named).
- Next steps:
  1. Read the design once as the person who will build it; every component should be something you could start tomorrow.
  2. Resolve or explicitly defer each Open question before writing implementation prompts.
  3. If the spec's Status is still Draft, consider marking it Approved now that a design depends on it.
  4. If the Praxisity agent roster is installed in this project, a designer or skeptic pass through `consult-team` tests component boundaries and whether every part is needed. If it is not, `/agent-authoring` installs it.
  5. If the `detail` skill is installed, detail the first element with `/detail`; the resulting implementation prompt will cite these IDs.
