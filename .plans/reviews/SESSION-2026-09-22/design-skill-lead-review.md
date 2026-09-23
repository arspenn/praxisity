# Lead Review: /design skill and the reference convention

**Date:** 2026-09-23
**Mode:** 2 (parallel snapshot), two rounds — prompt-engineer, critic, user-advocate, spot
**Subject:** `.claude/skills/design/SKILL.md` + `templates/design.template.md`; replaces `.claude/commands/architect.md` and `.praxisity/templates/design.template.md`. Also the reference convention adopted mid-review and applied to all three templates.

## Verdict

The describe pattern cloned cleanly; every describe round-2 fix carried forward. The new problems came from the one thing describe did not have: a parent document. One high finding (a shared placeholder that would have written the design number into the spec link) and a cluster of mediums around the coverage gate. Both rounds closed. The user-advocate rates the closing-coverage display after each component as the strongest teaching mechanic in the three skills.

## Round 1 findings and fixes

| Sev | Finding | Raised by | Fix |
|-----|---------|-----------|-----|
| High | Template used `NNN` for both the design number and the spec number in the Specification References link; Generate said replace globally. Independent numbering (SPEC-005 → DESIGN-004 here) means a literal run corrupts the link. | critic | Spec number is `MMM`; Generate names both tokens. |
| Med | Bare-number argument ambiguous between spec and design (005 exists as both here) | critic, PE, spot | `DESIGN-NNN` revises; `SPEC-NNN` or bare number selects a spec. |
| Med | Coverage counted interfaces and data entities but only COMP blocks had Satisfies | critic | Satisfies added to INT and DATA blocks. |
| Med | Cross-cutting non-functional MUSTs (accessibility, duration) had no element to satisfy them; the gate would bite on exactly what a learning deliverable always has | advocate, critic | Design-wide coverage via the Non-Functional Approach row, shown in the matrix; that table now drafted before the gate. |
| Med | Deliberate-gap escape was agent-draftable (Open Questions row said draft gaps), so in draft-first mode it became the default path; gap had no file form | PE | User-declared only; DQ names requirement, reason, milestone; matrix shows "deliberate gap, DQ-n". |
| Med | Gate withheld save but its exits lived only in Rules | advocate | Confirm message names the four options. |
| Med | "Revise the spec" escape was a cancel the skill cannot perform; PLANNING.md left in progress | critic | Cancel with Status `cancelled` and a pointer to `/describe`. |
| Med | Step 5 "revise it" had no route to the update flow; no detection of an existing design for the spec | critic, spot | Grep `.plans/designs/` for the spec ID; revise routes to step 6; alternative designs get "Alternative to". |
| Med | Spec-diff asked for "changed" requirements, undetectable from a matrix of IDs; orphaned components undefined | PE, critic | Diff via the spec's Revision History rows dated on or after the design's Last Updated; orphaned elements shown and re-homed or removed. |
| Med | "ID with short label" in the skill vs bare IDs in template placeholders; label undefined | PE | Became the reference convention (below). |
| Low | ~33 exchanges, nine of them approvals after the last decision; ask-first questions abstract; "Transition" missing from interface types; LMS-owned data vs designed storage; show SHOULDs after MUSTs empty; count anchor "two or three paragraphs"; struck blocks not a permitted op; re-read spec before matrix | advocate, PE, critic | All applied. Title folded into the intro; four reference lists batched; Implementation Order kept separate because it is a decision. |

## The reference convention

Adopted 2026-09-23 with the user. Prompted by "design-wide (7.4)" being a bare section number and the three templates mixing forms. Canonical block, identical in every template header comment (stripped from output) and in the skill-forge patterns reference:

- Element with an ID from another document: ID plus a two-to-four-word label in parentheses, always in tables and Satisfies lists, on first mention under each heading in prose; label coined by the first citing document and reused verbatim; qualify by document when more than one parent is in play; same-document IDs never labeled.
- Section: `§7.4 Non-Functional Approach`, `§Scope`; link the document first when it is elsewhere.
- Another document: relative markdown link whose text is the document ID or file name.
- Removed item: ID struck through with the version, wherever it appears.

Round-2 refinements from PE and critic: "first mention in a section" replaced by the decidable table/list/heading rule; label length and provenance defined; §Name allowed for unnumbered sections; document-plus-section form added; strike form unified on the ID (describe and design skills updated); one parent per child stated as policy (one spec per design, one design per DIP).

## Round 2 residue, accepted

- Convention lives only in stripped comments and the patterns reference; finished documents do not restate it. Acceptable: the plan template will carry the same block.
- Retention nudge appears in both the skill row and the template comment.

## Pattern notes for /plan

- `MMM` for the parent's number; DIPs link to both a design and a spec, so expect a third token.
- Struck elements: search `.plans/prompts/` before striking; name citing DIPs in the revision row. `/plan` should do the reverse: on revise, read the design's Revision History for struck elements it cites.
- Coverage-style gate for a DIP is different in kind: every step verifiable, every acceptance criterion cited. Same shape (withhold save, name the exits).

## Sources

- `design-skill-prompt-engineer-report.md`
- `design-skill-critic-report.md`
- `design-skill-user-advocate-report.md`
- `design-skill-spot-report.md`
