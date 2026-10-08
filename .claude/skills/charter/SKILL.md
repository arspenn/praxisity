---
name: charter
description: Create or update CHARTER.md, the project constitution that states mission, principles, scope, and constraints. Claude reads it every session, so it governs both the user's decisions and the AI's.
disable-model-invocation: true
---

# Charter

Create or update the project's charter. The charter is the project's constitution: it states the mission, principles, scope, and constraints. When CLAUDE.md points to it, Claude reads it at the start of every session, so it shapes the AI's judgment calls as much as the user's.

**Templates:** `${CLAUDE_SKILL_DIR}/templates/charter.template.md` for the charter, and in the same directory `claude.template.md`, `readme.template.md`, `changelog.template.md`, and `gitignore.template` for the project files offered after saving. Templates are read-only input shared by every future run; all edits target the project's own files.

## Rules

- Gather only what fills the template. The template defines the charter's shape; the skill does not add sections.
- Every section except Mission may be skipped. A skipped section is marked, not deleted, so a reader sees it was considered: `N/A — [reason]` when it does not apply, `TBD — revisit at [milestone]` when it cannot be known yet. Tell the user both markers exist; TBD is normal on a first pass.
- Unanswered categories inside a checklist section get their own marker at generate time: `N/A` unless the user said TBD.

<!-- Maintainer note: this skill converses with the user throughout, so it must not be given `context: fork` in frontmatter. -->

**PLANNING.md contract.** PLANNING.md has an `## Active Context` block with **Last Command**, **Status**, and **Date**, and a `## Next Steps` list. Skills set Status to `in progress`, `complete`, or `cancelled`.

## Pre-Flight

Run these steps in order and finish each before starting the next. Step 2 lands first so that an interrupted run still leaves PLANNING.md accurate, and step 4's outcome changes what the later steps mean.

1. Read PLANNING.md. If it is missing, create it per the contract above and tell the user you keep it as a session log.
2. Update PLANNING.md: Last Command `/charter`, Status `in progress`, Date today.
3. Invoke the `gather` skill with the Skill tool so its protocol is in context before the first section is presented.
4. If CHARTER.md exists, read it in full and offer three options: **(r)eview and update**, **(s)tart fresh** (a new charter; the established date resets to today), or **(c)ancel**. On cancel, set PLANNING.md Status to `cancelled` and stop.
5. If CLAUDE.md exists, read it for the project name, domain, and mission as defaults. If it does not exist, gather the project name along with the Mission.
6. Read the template. Its HTML comments define what each section needs and carry the examples.

## Introduction

Keep this under five sentences. Say what a charter is, that you will go one section at a time, and that skipping and TBD are allowed. Then invite source material as the gather protocol describes (a syllabus, assignment brief, rubric, proposal, or existing plan); if the project's references folder already holds files, list them and ask which apply. Read what the user provides before gathering begins.

## Gather

Gather in template order, one section at a time, following the gather protocol, including its purpose sentence before each prompt. The template comment for each section says what it needs. Pacing uses the gather protocol's terms:

| Section | Pacing | Charter-specific notes |
|---------|--------|------------------------|
| Mission | One prompt | Required. CLAUDE.md and source material count as loaded documents for the gather drafting rule. |
| Principles | One at a time until the user says done | Pacing matters here: each principle changes how the user thinks about the project. Source material rarely states values, so if the user stalls, offer to draft a first principle from the Mission. |
| Scope | Two prompts: In, then Out | Say why Out of Scope matters: it is what prevents scope creep. |
| Stakeholders | One prompt, categories as a checklist | Short answers; a solo project may name one person in two roles. |
| Success Criteria | One prompt, categories as a checklist | TBD is expected on a first pass; ask for the milestone at which it will be known. |
| Constraints | One prompt, categories as a checklist | Nudge toward the regulatory category if the field has obligations (accessibility, IRB, FERPA). |
| Domain Context | One prompt: the field, the three template questions, and any key context | Name the field first. Show the template comment's examples for that field even in brief mode; this is the one section where a newcomer to the field needs scaffolding more than speed. |
| Charter Maintenance | One prompt | For a solo project, "update via /charter" is a complete amendment process. |
| Glossary | Drafted by you, last | Scan everything gathered for terms a reader without project context would not know. Present the table for approval. Skip only if no such terms exist. |

**Update flow (option r).** Ask "What has changed since [Last reviewed date]?" and show a one-line index of sections with any TBD or N/A markers flagged. Walk the sections the user's answer touches, every TBD section, and any section whose structure differs between the existing charter and the current template (present the old content mapped into the new fields as a draft). Then offer a quick pass over the rest. The Glossary is always re-derived, since other sections changed. In update mode, "skip" means keep the existing content unchanged.

### Review and Confirm

Show a compact outline: each section header with a one-line summary, and the count of TBD and N/A markers. Not the full text; the user just approved it section by section. Offer **(y)es save**, **(e)dit a section**, or **(c)ancel**. On cancel, set PLANNING.md Status to `cancelled` and stop.

## Generate CHARTER.md

Copy the template, then Edit the copy. Edit keeps the template's structure as ground truth; regenerating the file with Write reproduces it from memory and drifts (renamed headers, dropped sections, half-stripped comments).

1. In update mode, re-read CHARTER.md now, immediately before the copy overwrites it, and note its "Charter established" date and the content of every section the user kept.
2. Copy the template to `CHARTER.md` with `cp` in Bash.
3. Read the fresh copy.
4. Apply only these operations with Edit:
   - **Placeholder substitution:** replace `[bracketed placeholders]` with gathered content.
   - **Comment stripping:** remove all `<!-- ... -->` blocks.
   - **Marking:** for a skipped section, replace its placeholder content with `N/A — [reason]` or `TBD — revisit at [milestone]`. The section stays.
   - **Row adjustment:** add or remove list rows and table rows to fit the content. Template row counts are illustrative.
5. Set dates. New charter: established and last reviewed are today. Update: keep the original established date, set last reviewed to today. In both cases, next review is today plus the interval when the review schedule names one (quarterly, monthly); when it names an event instead ("after the pilot"), write that event in place of a date.

## Post-Save

A charter is the first document in a project, so this is where the other project files get offered. Present the checklist below in one message, listing only the items that apply, so the user answers once; create nothing without a yes. Each file is made the same way as the charter: copy its template with `cp` in Bash, read the copy, substitute placeholders from the charter with Edit, strip the HTML comments (the gitignore's `#` lines are its content and stay).

1. **CLAUDE.md.** If missing, create it from `claude.template.md`: name, domain, mission, and the `@CHARTER.md` import line that loads the charter into every session. If present and it does not import the charter, offer to add that line under a "Project Constitution" heading.
2. **README.md.** If missing, create it from `readme.template.md`. Show the drafted Overview (from the mission and scope) before creating the file; later sections stay as placeholders or N/A.
3. **CHANGELOG.md.** If missing, create it from `changelog.template.md`; the first entry records the charter. `/do` appends to it as work completes.
4. **.gitignore.** If the project is a git repository and has none, create it from `gitignore.template`.

Then, if the project is a git repository, offer to commit CHARTER.md and any files just created, with `charter: create project charter` or `charter: update project charter`. Never commit without an explicit yes.

## Completion Gate

Update PLANNING.md: Status `complete`, and Next Steps naming CHARTER.md and any TBD milestones. This is a hard gate: do not show the success message until PLANNING.md is updated, because the next session reads PLANNING.md before anything else.

If the user cancelled at any earlier point, PLANNING.md must already read `cancelled` for the same reason.

## Success Message

Show all of the following:
- CHARTER.md was created or updated, and how many TBD items it holds.
- If CLAUDE.md now imports the charter: Claude will load CHARTER.md each session, and when it faces a judgment call about scope or priorities this is what it consults. If the user declined the import, say the charter is only consulted when they point Claude at it.
- Next steps:
  1. Read the charter once as a reader rather than its author.
  2. Share it with an instructor, advisor, or collaborator if that would help alignment.
  3. Revisit at each TBD milestone; `/charter` will walk only what changed.
  4. If the `describe` skill is installed, start the first specification with `/describe`. If the Praxisity agent roster is installed in this project, `consult-team` can run a multi-perspective review of the charter first; `/agent-authoring` installs the roster.
