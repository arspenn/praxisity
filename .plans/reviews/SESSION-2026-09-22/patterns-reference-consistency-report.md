# Patterns Reference Consistency Review

**Reviewer:** consistency-reviewer (one-shot) · **Date:** 2026-10-08
**Subject:** `.claude/skills/skill-forge/references/praxisity-patterns.md` vs. the five workflow skills, `gather`, and the design template header.

**Status:** Issues Found (10 mismatches; none block use of the reference, but each will mislead a skill author who copies the stated shape)

## Verified consistent

- Phase sequences: the four document-producing skills and `/do` have exactly the headings the patterns file lists, in order.
- PLANNING.md contract line: verbatim in charter, describe, design, detail, do.
- Status lifecycle: every string `/do` writes (`In Progress`, `In Progress — Step N passed|skipped`, `Halted — Step N: …`, `Halted — Acceptance: AC-n …`, `Halted — Verification: …`, `Done`) and reads (plus `Ready`, bare `In Progress`, no-Status-row) matches; `/detail` sets `Ready` and writes "resume at Step K" / "resume at Acceptance".
- Gate rules for describe, design, detail match the skills' Rules bullets.
- Tokens `NNN` / `MMM` / `DDD` and the `-slug` stem rule match describe, design, detail, and the templates.
- No workflow skill carries an Agent Consultation section (only `consult-team/SKILL.md`'s H1 uses that title).
- Naming: artifact paths and the spec (OBJ, REQ-F, REQ-N, UC, AC, Q) and design (COMP, INT, DATA, DEC, DQ) ID lists match.
- Reference Conventions table matches the design template header line for line; all four document templates carry the identical block and the two-markers note; `adr.template.md` is parked in `.praxisity/templates/`; all four named support skills and all four named review agents exist.
- Compound pacing examples ("Two prompts: In, then Out", "Drafted, then one prompt", "Drafted outline, then one at a time") each appear verbatim in a skill table.

## Mismatches

| # | Patterns file passage | Skill passage | Should change |
|---|---|---|---|
| 1 | §Skeleton, Frontmatter: every document-producing skill has "an `argument-hint`"; §Opening: "two bold lines: **Template** … and **Argument**", template "declared once". | `charter/SKILL.md` frontmatter has no `argument-hint`; its opening has **Templates:** (plural, five files) and no **Argument** line. | Patterns: note charter takes no argument and bundles project-file templates. |
| 2 | §Skeleton, Frontmatter: description is "one sentence". | charter, describe, design, do descriptions are two sentences each. | Patterns: drop "one sentence" or say "one or two". |
| 3 | §Skeleton, Rules: "Five to seven bullets … the ID rule; the gate rule; the cite rule; the one-parent rule." | charter has 3 bullets and none of the four named rules; describe has 4 bullets, ID and gate only; detail has no one-parent rule (it has "One DIP, one element, one sitting"). Only design carries all four. | Patterns: "three to six bullets" and mark the four rules "as applicable (design has all four)". |
| 4 | §The PLANNING.md Contract: "Nothing in PLANNING.md survives the next skill's step 2". | design step 5, detail step 5b, and do step 3 all read PLANNING.md's Next Steps as the default *after* their own step 2 has written. Next Steps survives until the completion gate. | Patterns: "survives the next skill's completion gate". |
| 5 | §Gather Terms: "exactly these words from the gather skill … **Drafted by you**". | `gather/SKILL.md` §The Rule defines the term as **Drafted**; the four skill tables write "Drafted by you". | gather: rename the term to "Drafted by you" so the claim holds (four skills already use it). |
| 6 | §Gather Terms, Checklist: "unanswered ones are marked N/A at generate time (a sub-headed empty table is N/A on its own)". | charter Rule 3: each unanswered category gets its own marker, "N/A unless the user said TBD". describe Rule 2: an unanswered category "simply produces no row"; only an empty subsection is N/A. Two different behaviours; patterns states only the second. Also no table uses bare "Checklist"; they write "One prompt, categories as a checklist". | Patterns: describe both behaviours (list sections mark per category; table sections drop the row) and show the compound form used in tables. |
| 7 | §Markers, IDs, and Gates: a gate "names its exits in the confirm message"; §Skeleton, Review and Confirm: "the gate's exits named instead". | `describe/SKILL.md` §Review and Confirm: "while any MUST is uncovered, offer only edit or cancel". The exits (add a criterion, lower the priority, TBD with a milestone) appear only in the Rules bullet. design and detail do name theirs at confirm. | describe: name the three exits at Review and Confirm, matching design and detail. |
| 8 | §Agent Consultation: "The success message's next steps mention `consult-team` when it is installed and name the agent whose perspective fits". | charter mentions `consult-team` but names no agent; detail and do never mention `consult-team`. | Patterns: scope the claim to charter (no agent named), describe, and design. |
| 9 | §Naming, commit messages: "each naming the artifact ID". | charter commits `charter: create project charter` / `charter: update project charter`; no ID exists. | Patterns: "each naming the artifact ID where one exists". |
| 10 | §Markers: "Update flows use TBD markers as their target list." | `gather/SKILL.md` §Skips: "Update flows use these markers [both N/A and TBD] as their target list." The four skills walk every TBD section and only flag N/A in the index, so the skills agree with patterns, not gather. | gather: change to "TBD markers" (N/A sections are flagged, not walked). |

## Advisory (do not block)

- §Skeleton lists Review and Confirm as a peer phase; in all four skills it is an H3 under Gather. Say so, or a new skill will promote it to H2.
- `do` Completion Gate 4 writes `Halted — Step N: cancelled by user`; it fits the listed `Halted — Step N: [reason]` form, but the lifecycle paragraph could name it since it is the only Halted string not produced by a Verify failure.
- design Generate step 4 says "`MMM` with the spec number and slug"; detail step 4 states the `MMM` / `MMM-slug` distinction precisely. Aligning design's wording with detail's would make the token rule in §Markers trivially true in both skills.
- §Skeleton Pre-Flight "read the charter if present": charter reads CLAUDE.md instead. Obvious, but worth a parenthetical.

## Self-Evaluation

- **Most frequent type:** over-generalisation. The patterns file describes the design skill (the fullest instance) as if all four document-producing skills had the same frontmatter, rule set, and gate wording; charter is the outlier in six of ten rows.
- **Unable to assess:** whether the naming rationale for "detail" and the Mode 2 review checklist claim are accurate; neither is recorded in the skills.
- **Structure quality:** easy to cross-reference. Headings in the patterns file map one-to-one onto skill headings, and the skills share identical sentences where the patterns file quotes them.
- **Prompt improvement:** the task's "which one should change" column needs a stated tie-break. I used the patterns file's own line 3 (the skill is newer) except where three skills agreed against one file (rows 5, 7, 10).