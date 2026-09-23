# Lead Review: /describe skill (first clone of the charter pattern)

**Date:** 2026-09-22
**Mode:** 2 (parallel snapshot), two rounds — prompt-engineer, critic, user-advocate, spot (same agents as the charter review, carrying their checklists)
**Subject:** `.claude/skills/describe/SKILL.md` + `templates/spec.template.md`; replaces `.claude/commands/spec.md` and `.praxisity/templates/spec.template.md`

## Verdict

The charter pattern cloned cleanly; every round-2 charter fix carried forward. The problems were all spec-specific, and one was serious enough that it would have propagated into `/design` and `/plan`. Both rounds closed; reviewers judge the skill fit to be the ID-bearing pattern for the next two skills.

## Round 1 findings and fixes

| Sev | Finding | Raised by | Fix |
|-----|---------|-----------|-----|
| High | ID rules contradicted: "assign at generate time, sequentially in the order gathered" vs "keep IDs stable on revise". Any revision, or an edit at Review, would renumber every requirement and shift every AC's Validates column. Designs in this repo cite spec IDs 128 times. | PE, critic | IDs assigned the moment the user approves an item, never renumbered, in both modes. Generate writes already-assigned IDs and numbers nothing. Rule visible from Rules, the pacing rows, Review and Confirm, and Generate. |
| Med | New-vs-revise had no rule for a loose title match; "next number" undefined (repo has two 006 specs); argument mechanism unnamed | critic, spot | Exact number (with or without `SPEC-`) → revise, ask if duplicated; loose title match → ask once; otherwise new with highest NNN + 1. `$ARGUMENTS` named (unverified in skills; test in step 8). |
| Med | "Every MUST has an AC" collided with "AC may be TBD" and "flag" had no consequence | critic | AC may be TBD only with a milestone carried to Next Steps; otherwise an uncovered MUST withholds the save option. |
| Med | "Run /charter first" was a cancel the skill cannot perform; PLANNING.md left in progress; template's charter links had no no-charter branch | critic, PE | Offer continue-without or stop with Status `cancelled`; charter-derived fields marked `N/A — no charter` at generate. |
| Med | Revise flow: filename and Status not declared stable; removed IDs could dangle in designs | critic | Filename and Status stable; removed rows kept struck through with "removed in vX" so citations resolve. |
| Med | Brief and rubric treated as one input; rubric rows are judgment criteria, so requirements drafted from a rubric came out as qualities and ACs restated them | advocate | Intro says brief → requirements, rubric → acceptance criteria, and each rubric-derived AC cites its row. |
| Med | Objectives formula and the ID use-case example both read as learning objectives; a student would fill both with the module's learning objectives | advocate, PE | Template comments distinguish project objectives from learning objectives (which become requirements, assessed by ACs); use-case example reframed as a scenario with ID glosses for Preconditions and Alternative Flows. |
| Med | Charter Reference field never gathered | PE, advocate, spot | Drafted with Related Documents and References. |
| Med | Gather's own one-at-a-time example listed "scope items", contradicting both skills | PE | Gather example now says use cases. |
| Med | Constraints pacing was an unnamed fifth term overriding the drafting preference | PE | 6.1 stated as drafted regardless of style because it is a citation. |
| Low | AC section had no examples and the student never writes one; NFR category list differed between skill and template; slug rule dropped; link convention unstated; "DIPs" unexpanded; version increment unspecified | all | All addressed in template comments or one clause. |

## Round 2

PE: all round-1 items resolved; new medium on "next unused number" being readable as gap-filling and uncited removed rows being deleted. Critic: high and all mediums resolved; same wording risk; struck rows could be lost at the cp; five low edges. All applied: next ID is highest ever assigned plus one, removed rows always kept struck, struck rows preserved through the copy and excluded from coverage, bare numeric argument handled, save withheld while a MUST is uncovered, Author gathered with the title, revision row names affected IDs.

## Pattern notes for /design and /plan

- IDs on approval, never renumbered, highest-ever-plus-one: copy verbatim.
- Struck rows for removed cited items: copy verbatim.
- Coverage gates (every MUST → AC here; every MUST → component in design) withhold the save option rather than "flag".
- Checklist-over-table rule: a subsection with no rows is N/A on its own.
- Reviewer agent memories now hold nine (PE) and several (critic, advocate) checklist items from these two reviews; dispatch the same three agents for the next clones.

## Unverified platform items added to the step-8 list

`$ARGUMENTS` inside a skill; `ls`/`cp` in Bash from within a skill flow is assumed fine.

## Sources

- `describe-skill-prompt-engineer-report.md`
- `describe-skill-critic-report.md`
- `describe-skill-user-advocate-report.md`
- `describe-skill-spot-report.md`
