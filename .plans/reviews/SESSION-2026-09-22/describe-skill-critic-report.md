## Critic Review: /describe skill (first clone of the charter pattern)

**Artifact:** `.claude/skills/describe/SKILL.md`, `templates/spec.template.md`; pattern `.claude/skills/charter/SKILL.md`; protocol `.claude/skills/gather/SKILL.md`; prototype `.claude/commands/spec.md`; example output SPEC-009
**Date:** 2026-09-22 | **Dispatch Mode:** Mode 1 (team-lead consult) | **Reviewer:** critic

## Instructions Received

Review the new /describe skill against the charter pattern and gather protocol, with attention to new-vs-revise parsing, ID stability on revise, the charter-missing branch, MUST/AC enforcement, path and numbering in a fresh plugin project, the template's relative links, and anything dropped from the old command.

## Findings

### High — ID assignment rules contradict each other, and the Generate step follows the wrong one
**Location:** Rules bullet 4 ("assigned by you, sequentially, at generate time"); Gather FR row ("assign IDs later"); Generate 4 ID assignment ("sequentially in the order gathered"); Update flow ("Keep existing IDs stable ... removed items leave a gap").
**Problem:** The stability rule lives only in the Gather update paragraph. The step that actually writes IDs has no update branch and says "sequential in the order gathered," which renumbers. Generate 1 notes kept content but not kept IDs. The same defect exists in new mode: the AC table is drafted mid-gather with a Validates column, so IDs already exist when the user sees it; if the user then deletes a requirement at (e)dit, generate-time renumbering shifts every AC's Validates to the wrong requirement.
**Impact:** Designs cite requirement and AC IDs 128 times across seven design documents in this repo. A revise that renumbers silently breaks every one.
**Fix:** One rule for both modes: an item receives its ID the moment the user approves it, in approval order, and never changes. Deleted IDs are not reused. Delete Rules bullet 4's "at generate time"; make Generate 4 "write the IDs already assigned." Add to Generate 1: "note every existing ID and its text."

### Medium — New-vs-revise decision has no rule for ambiguous arguments, and "next number" is undefined
**Location:** Pre-Flight 4.
**Problem:** "If the argument names an existing spec by ID or title" gives no rule for a partial or near match. `/describe gather skill` could mean a new spec or SPEC-006 gather-skill. The skill also never says how the argument reaches it (`$ARGUMENTS` substitution in skills is not in the verified-capabilities table). "Take the next number" is undefined: `.plans/specs/` already holds two files numbered 006, so max-plus-one gives 010 and count-plus-one gives 011.
**Impact:** Duplicate numbers (already happened once under the old command) or a silent revise of the wrong spec.
**Fix:** Exact `SPEC-NNN` or `NNN` means revise. Any other argument that loosely matches an existing title or slug triggers one question: "SPEC-006 gather-skill exists. Revise it, or create a new spec?" Define next number as the highest existing NNN plus one. State the argument mechanism once and verify it in work-plan step 8.

### Medium — "Every MUST has an AC" collides with "Acceptance Criteria may be skipped," and "flag" has no consequence
**Location:** Rules bullets 2 and 5; Review and Confirm; template AC comment ("Every MUST requirement needs at least one").
**Problem:** Bullet 2 lets the AC section be TBD. Bullet 5 requires an AC per MUST. On a first pass with TBD ACs, every MUST is uncovered and the flag fires for all of them, with no stated outcome: the user can save anyway. The template comment reads as a hard rule; the skill treats it as a warning. Nothing checks at generate time.
**Fix:** Decide once and say it: AC may be TBD only with a milestone, in which case Review shows "N MUSTs uncovered until [milestone]" and the Completion Gate carries it into Next Steps. If ACs are present, a MUST without one blocks save until the user adds one or downgrades the priority.

### Medium — The charter-missing branch is a cancel path with no PLANNING.md reset, and the template hard-codes charter links
**Location:** Pre-Flight 5; template Metadata "Charter Reference," References line 215, Constraints 6.1; Gather Constraints row.
**Problem:** "Offer to continue or to run `/charter` first": the skill cannot invoke /charter (it is `disable-model-invocation: true`), so choosing it means the user leaves, and PLANNING.md stays `in progress`. If they continue, the two literal `[CHARTER.md](../../CHARTER.md)` links and the "Draft inherited half" instruction have no no-charter branch; the permitted operations cannot mark a non-placeholder link N/A.
**Fix:** "If they choose /charter first, set Status `cancelled`, stop, and tell them to run /charter then /describe again." Wrap the two links in placeholders (`[Charter reference or N/A]`) and add "N/A — no charter" to the Constraints row.

### Medium — Revise flow leaves three things undefined that designs depend on
**Location:** Update flow; Generate 1, 2, 5; template Metadata Status.
**Problem:** (a) A removed item "leaves a gap," but a design citing that ID now dangles silently. (b) The cp resets Status to `Draft`; Generate 1 does not note Status, so revising an Approved spec silently un-approves it. (c) The file name is never declared stable; if the title changes, does `NNN-[slug].md` change? Designs link to the path.
**Fix:** Before removing or rewording an item, grep `.plans/designs` and `.plans/dips` for its ID and list hits in the Revision History row; prefer keeping the row struck through as "Removed in v0.2" over deletion. Note Status in Generate 1 and either restore it or say it reverts to Draft on revise. State that the file name never changes after creation.

### Low — Checklist-to-N/A rule does not fit table-shaped sections
**Location:** Rules bullet 3; NFR and Dependencies rows.
**Problem:** Copied from charter, where categories are bold labels. Here NFR categories are prompts, not rows; an "N/A" row in a requirements table is nonsense.
**Fix:** "For table sections, unanswered categories are simply omitted; mark the section N/A only if empty."

### Low — Dropped from the old command
Slug rule (lowercase, hyphens) is gone; add it to the Title row. Everything else dropped (Todoist, agent block, WON'T priority, second UC block) was right to drop.

### Low — Link convention unstated
SPEC-009 shows the convention (same-dir for specs, `../designs/` for designs, `../references/` for sources). Put it in the Related Documents comment so drafted links are consistent.

## Unstated Assumptions
- Working directory is the project root, so `.plans/specs/` and `../../CHARTER.md` line up.
- Skill-tool invocation of `gather` from inside a skill works (unverified, same as charter).
- Author defaults to git; in a non-git project the "ask" lands after Review and Confirm, an odd moment. Gather it with Title instead.
- One user creates specs sequentially; no concurrent numbering.

## Ranked Top 5
1. Assign IDs on approval, never at generate time, in both modes.
2. Define "next number" and the ambiguous-argument question; this repo already has a duplicate 006.
3. Resolve MUST/AC against skippable AC; say whether the flag blocks.
4. Make "/charter first" a proper cancel; give the charter links a no-charter branch.
5. Declare file name and Status behavior on revise; check designs before removing an ID.

## Strengths
The clone carried forward every Round 2 charter fix: re-read before cp, structural-drift walk in update mode, cancel resets, offer-only git, conditional next steps. Deriving ACs from MUSTs and surfacing uncovered MUSTs at Review is the right shape; the enforcement just needs a stated outcome. The template's four-domain examples and the relative-link fix over the old template are both correct.

## Self-Evaluation
- **What worked well:** Checking the specs directory and grepping designs for ID citations turned two rules from theoretical into evidenced.
- **What you struggled with:** Cannot test argument substitution or the numbering step live.
- **Prompt improvement suggestions:** Add "when a skill has an update flow, trace every ID and path it emits to the documents that cite them" to my checklist.

---

## Round 2 — 2026-09-22 (delta pass on the revision)

### Resolved
- **ID assignment (High):** Rules bullet 3 assigns on approval in both modes, every gather row says "assign on approval," Review says an edit leaves the ID unused, Generate 4 writes already-assigned IDs. Resolved. One wording risk: "the next unused number in their series" can be read as filling a gap left by a removed item, which the same bullet forbids. Say "one higher than the highest number ever used in that series."
- **New-vs-revise and numbering:** exact `SPEC-NNN` revises, a loose title match asks once, next number is highest plus one, `$ARGUMENTS` is named. Resolved. Two edge cases remain, both low: a bare `006` is neither an exact ID nor a title and would become a new spec titled "006"; and this repo has two files numbered 006, so an exact match can hit two files. Add "or a bare number" and "if two files share the number, ask which."
- **MUST without AC:** Rules bullet 4 now states the block and the TBD-with-milestone exception. Resolved. Review and Confirm still only lists uncovered MUSTs; add "do not offer (y)es while any MUST is uncovered and AC is not TBD" so the block is enforced where the save decision is made.
- **No-charter branch:** step 5 offers continue-with-N/A or cancel with Status reset; Generate 4 marks Charter Reference and inherited constraints and removes the References link. Resolved.
- **Revise flow:** struck-row rule with a search of `.plans/designs/` and `.plans/prompts/` (verified: DIPs live in `.plans/prompts/`), filename and Status stable, Status noted in Generate 1 and kept in Generate 5. Resolved.
- **Checklist over tables, slug rule, link convention:** all resolved.

### New gaps
- **Low-Medium — Struck rows can be lost at the cp.** Generate 1 notes "the content of every section the user kept." A removed-but-cited item is by definition not kept, and the template has no struck-row placeholder, so the row exists only if the agent treats it as section content. Add "including any struck rows" to Generate 1.
- **Low — Struck rows and the coverage block.** A struck MUST still reads as MUST; the rule should exclude struck rows from AC coverage, or the block fires on a requirement the user just removed.
- **Low — Reworded items are invisible.** Generate 5's "one-line summary of what changed" need not name IDs whose text changed under a stable ID. Designs cite the ID, not the text. Require the changed IDs in the Revision History row.
- **Low — Author "or ask" still lands after Review and Confirm** in a non-git project. Gather it with Title.

### Round 2 verdict
The high finding and all four mediums are closed. The remaining items are one-clause edits. This skill is fit to serve as the ID-bearing pattern for /design and /plan once the "next unused number" wording and the struck-row clause in Generate 1 are fixed, because both would otherwise be copied verbatim.
