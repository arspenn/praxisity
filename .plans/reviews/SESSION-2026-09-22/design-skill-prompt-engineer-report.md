## Prompt Engineer Review

**Artifact:** `/design` skill — `.claude/skills/design/SKILL.md`, `templates/design.template.md`; pattern: final `describe/SKILL.md`; protocol: `gather/SKILL.md`
**Date:** 2026-09-22
**Dispatch Mode:** Mode 3 (team teammate, lead-directed)

## Instructions Received

Review the third clone with the nine-item workflow-skill checklist. Specific attention: "Three prompts" pacing versus gather's terms; the coverage gate's third escape (deliberate gap as Open Question); agreement between "cites, does not restate" and the Satisfies generate instruction; the update flow's spec-diff step; signal-to-noise at 115 lines; template comments for an instructional design student.

## Findings

### MEDIUM — The Satisfies label rule and the template disagree
**Location:** Rule line 22 ("only as an ID with a short label"), generate line 81 ("requirement IDs with short labels"), versus template line 147 `**Satisfies:** [REQ-F1, REQ-N1]`, line 81 `| REQ-F1 | COMP-1, INT-1 |`, and line 40 `[REQ-F1, REQ-F2, REQ-N1...]`.
**Problem for AI:** The two skill passages agree with each other, but at Edit time the agent is looking at template placeholders that show bare IDs, and the placeholder wins. "Short label" is also undefined: a truncation of the requirement text restates it; a paraphrase does not.
**Fix:** Define once in rule 22: "an ID followed by a two-to-four-word paraphrase in parentheses, e.g. `REQ-F3 (offline access)`." Change the three template placeholders to that form. Drop the restatement from line 81; "already-assigned ID" is enough once the template shows the format.

### MEDIUM — The deliberate-gap escape can be drafted by the agent, has no file form, and is announced before it exists
**Location:** Rule line 21; row 58 ("this is the gate"); row 64 ("plus any deliberate coverage gap"); Review and Confirm line 71.
**Problem for AI:** Row 64 tells the agent to draft Open Questions from "any deliberate coverage gap". In draft-first mode the agent therefore turns every uncovered MUST into a drafted DQ, and the escape becomes the default path through the gate. Nothing says what the coverage-matrix row for a gapped MUST contains, so the agent invents it. "Revises the spec" is a third escape with no mechanics inside this skill. Row 58 calls itself the gate, but Open Questions comes six rows later, so at row 58 the escape is not yet available and the actual gate is at Review and Confirm.
**Fix:** Rule 21 becomes: "an uncovered MUST withholds the save option until the user adds an element or declares a deliberate gap. A gap is declared by the user, never drafted from an uncovered requirement; it is recorded as a DQ-n naming the requirement, the reason, and the milestone, and the matrix row lists that DQ-n under Design Elements with 'deliberate gap' as the Approach. If the requirement itself is wrong, cancel and revise the spec with `/describe`." Row 64 drops "plus any deliberate coverage gap" in favor of "plus any gap the user declared". Row 58 becomes "Show any MUST still uncovered and say the save option stays withheld until each is covered or declared a gap in Open Questions."

### MEDIUM — The spec-diff step asks for a comparison its inputs cannot support
**Location:** Update flow line 67, "diff its requirements against the coverage matrix first and show what is new, changed, or removed."
**Problem for AI:** New and removed are derivable (IDs present in one and not the other; struck-through rows in the spec). "Changed" is not: the matrix holds IDs and labels, not requirement text or priority, so a reworded or repriorited MUST looks unchanged. The agent will either skip "changed" or guess.
**Fix:** "New: requirement IDs in the spec absent from the matrix. Removed: struck through in the spec but present in the matrix. Changed: any ID named in a spec Revision History row dated after the design's Last Updated, including priority changes; a SHOULD raised to MUST is a new coverage obligation." This works because describe's generate step 5 already requires revision rows to name the IDs added, changed, or removed.

### LOW — Bare-number argument is ambiguous between spec and design
**Location:** Step 4 accepts `DESIGN-004` or bare `004` as a design; step 5 accepts an argument that "names a spec". If both SPEC-004 and DESIGN-004 exist and the user typed `004` meaning the spec, step 4 silently runs the update flow on the design. Fix: "A bare number matches a design only if no spec has that number; otherwise ask which."

### LOW — Small clarity items
- Step 5 last sentence: if the user chooses "revise it", say "read that design in full and run the update flow", since step 4 already decided "new".
- Row 58: "from every live element's Satisfies list"; line 71 excludes struck-through elements but the matrix is drafted before Review.
- Row 54 names three of the five COMP block fields; say "per the template block: purpose, satisfies, responsibilities, dependencies, local decisions".
- Rule 21 second sentence ("Coverage is shown after every component and in the coverage matrix") restates rows 54 and 58. Cut.
- Row 56 "Nudge toward retention when the data is about people" and template line 193 say the same thing; keep the skill's copy, since it governs behavior.

## Answers to the specific questions

**"Three prompts" and gather's terms.** Not one of gather's four terms, but the same compound the charter's "Two prompts: In, then Out" and describe's "Drafted, then one prompt" already use: named subsections, each One prompt. It is unambiguous. Add one line to gather after the four terms so the compounds are sanctioned rather than tolerated: "Skills may combine terms per subsection, for example 'Two prompts: In, then Out' or 'Drafted, then one prompt'."

**Coverage gate third escape.** Followable but abusable as written; see the second finding. The fix keeps the escape and makes it user-declared with a defined file form.

**Cites versus Satisfies.** The two skill passages agree; the template does not; see the first finding.

**Spec-diff step.** Two of three comparisons are supported; see the third finding.

**Signal-to-noise.** Acceptable at 115 lines. The growth over describe is branches (spec selection, gate escapes, spec diff, alternative designs), not restatement. About four lines are cuttable (rule 21 second sentence, row 54 field list once it points to the template, line 81 label restatement, one retention nudge).

**Template comments for an instructional design student.** No misleading content found. The four-field examples are consistent across Architecture (learning ecosystem, instructional strategy, modality and tools), Components (modules, activities, assessments, job aids), Interfaces (transitions, facilitator handoffs, assessment result flow), Data Model (learner records, completion tracking, retention), and Validation (expert review, learner pilot, assessment validation). The Contract explanation for a handoff (trigger, what is passed, from whom to whom, by when) translates a software concept without forcing its shape. One small anchor: 1.1 "Two or three paragraphs" is a count; "as long as an outside stakeholder needs" avoids it.

## What's Well-Engineered

- Rule 20 carries the "highest ever assigned plus one" form and the reason; the update flow keeps struck-through headers so DIP citations resolve.
- Coverage feedback after each component (row 54, "so the user sees the gap close") is a teaching loop, not a check, and it is placed where the decision is made.
- Review and Confirm withholds save rather than warning; the structure enforces the rule.
- The Architecture section mirrors the charter's Domain Context "three questions that transfer across fields", so the framework teaches one shape twice.
- The Introduction names the spec and its MUST/SHOULD counts, which anchors every later prompt in what must be covered.

## Top 5 Changes, Ranked

1. Make the deliberate gap user-declared with a defined DQ and matrix form; fix row 58's "this is the gate".
2. Define the Satisfies label and change the three template placeholders to show it.
3. Define new, changed, and removed for the spec diff via IDs and Revision History.
4. Resolve bare-number argument ambiguity between spec and design.
5. Sanction compound pacing terms in gather with one line.

---

## Round 2 — 2026-09-23 (delta pass on the revision and the reference convention)

### Resolved
All three medium findings and the bare-number ambiguity are resolved. Rule 22 defines the label with an example and the template placeholders show it (lines 93, 159, 193, 218, 296). The deliberate gap is user-declared, never drafted (rule 21, row 61), has a defined matrix form (template lines 87–89), and the spec-revision escape is now a cancel with a pointer to `/describe`. The spec diff uses Revision History rows dated after the design's Last Updated and handles emptied Satisfies lists. The argument line and step 4 make `DESIGN-NNN` the only revise trigger. Row 57 builds from live elements; rule 21's restatement is gone; gather sanctions compounds; "A few paragraphs" replaces the count. Not resolved, and acceptable: the retention nudge still appears in both row 55 and template line 211.

### New

**MEDIUM — The design-wide escape is not available when the gate runs.** Row 57 builds the matrix "plus the Non-Functional Approach rows" and offers "the three ways to cover it", but Non-Functional Approach is drafted in row 62, five rows later. At the gate an uncovered REQ-N MUST has no design-wide row to point to. Fix: give Non-Functional Approach its own "Drafted by you" row immediately before Requirements Coverage.

**MEDIUM — Row 62 batches six sections into one approval, two of them substantive.** Implementation Order (the build sequence) and Non-Functional Approach (MUST coverage) are decisions; Glossary and the three reference lists are bookkeeping. One message for all six is the form-filling failure gather's "Why one at a time" names. Fix: Implementation Order gets its own row after Design Decisions, Non-Functional Approach moves as above, and the remaining four stay batched.

**LOW** — Template line 49 Requirements Addressed shows bare IDs; under "first mention in a section" every one would need a label. Say "(IDs only; this is an index)". Step 5 "go to step 6 for the update flow" reads as if step 6 were the update flow; say "continue from step 6, then run the update flow".

### The reference convention as a prompt

Three of the four forms will render identically across skills: section (§number title), document (relative link with ID text), and removed-item-as-citation. The element form will not, for two reasons, and the four copies already differ.

1. **"First mention in a section" is undefined for nested structure.** Is the section §3 Components or each COMP block? If REQ-F1 is satisfied by COMP-1 and COMP-3, one reading labels it once, the other twice. The template placeholders (line 159) imply per-block. Replace with a deterministic rule: "always labelled in tables and Satisfies lists; in prose, labelled on first mention under each heading, bare after."
2. **"Short label" has no length, source, or reuse rule.** One skill will write `(search latency)`, another `(return results within 2 seconds)`. Add: "two to four words, a paraphrase rather than the requirement text, coined by the first document that cites the ID and reused verbatim downstream."
3. **The source-document strike form differs from the citation form.** The convention strikes the ID, `~~REQ-F3~~ (removed v0.2)`; describe line 62 strikes the row text with "removed in v[version]"; design line 64 strikes the block title. Align all three on: strike the ID and the title or text, append `(removed v0.2)`.
4. **The four copies are not verbatim.** The charter template drops the removed form and the first-mention clause, reorders the bullets, and adds a name variant (`§Scope`) that the canonical table lacks. A spec citing the charter's unnumbered Constraints has no sanctioned form. Add "or name when unnumbered" to the canonical table, extend the qualify-by-document clause to sections (`DESIGN-002 §7.4`), and paste the canonical block into all three templates unchanged so a grep shows one text.

The convention lives in template comments, which are stripped, and in praxisity-patterns, which only skill-forge loads. Finished documents therefore carry no statement of their own conventions; the `/plan` template must carry the same block or DIPs will not learn it.
