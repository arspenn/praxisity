## Prompt Engineer Review

**Artifact:** `/describe` skill — `.claude/skills/describe/SKILL.md`, `templates/spec.template.md`; pattern: final `charter/SKILL.md`; protocol: `gather/SKILL.md`
**Date:** 2026-09-22
**Dispatch Mode:** Mode 3 (team teammate, lead-directed)

## Instructions Received

Review the first clone of the charter pattern using the workflow-skill checklist. Focus: pacing-table consistency with gather's four terms, clarity of ID assignment and stable-ID rules, restatement of template or gather, signal-to-noise, and spec-template comments that would mislead an instructional design student.

## Findings

### HIGH — Generate step ID assignment has no update-mode branch and would renumber
**Location:** SKILL.md line 79, "number OBJ, REQ-F, REQ-N, UC, AC, and Q sequentially in the order gathered".
**Problem for AI:** The stable-ID rule lives in the Gather section (line 61). At generate time the agent is reading step 4, which says to number sequentially in gathered order. In update mode that renumbers everything, which is the exact outcome the rule exists to prevent. The reason ("designs and DIPs may already cite them") is not in view where the numbering happens.
**Fix, replace line 79:** "**ID assignment.** New spec: number each series in the order gathered. Update: every existing ID keeps its number; new items take the next unused number in their series; a removed item's row is deleted and its number is never reused, because designs and implementation prompts may already cite it. Fill each AC's Validates column with the requirement ID it traces to."

### MEDIUM — ID timing rule conflicts with drafting acceptance criteria during gather
**Location:** Rule line 19 ("assigned by you, sequentially, at generate time"), row 51 ("assign IDs later"), row 54 (AC "each traced to its requirement", table presented for approval), line 65 (MUST without AC check).
**Problem for AI:** The AC table and the MUST-coverage check both need to name requirements before generate time, but the rule says IDs do not exist yet. An agent either invents a workaround (quoting requirement text in the Validates column) or assigns IDs and believes it broke a rule.
**Fix, replace line 19:** "IDs (OBJ-n, REQ-Fn, REQ-Nn, UC-n, AC-n, Q-n) are yours to assign. Give each item its ID in conversation as soon as the user approves it, in approval order; those IDs become final at generate time. The user never needs to type one." Delete "assign IDs later" from row 51.

### MEDIUM — Metadata field is never gathered or derived
**Location:** Template line 28, `[CHARTER.md](../../CHARTER.md) — [principles this spec serves]`; SKILL.md generate step 5 sets Status, dates, Author, Revision History only.
**Problem for AI:** The placeholder survives to the finished spec, or the agent invents the list. Fix, append to step 5: "Charter Reference: list the charter principles the Problem Statement and MUST requirements invoke; derive it, do not prompt."

### MEDIUM — Gather's own example contradicts both skills' Scope pacing
**Location:** gather line 50 lists "scope items" as one-at-a-time; charter row 46 and describe row 57 gather Scope and Out of Scope as one prompt each.
**Problem for AI:** The protocol says the workflow skill decides, then gives an example that disagrees with the two workflow skills. An agent that weights the protocol will split Out of Scope item by item. Fix: gather line 50 example becomes "(principles, requirements)".

### MEDIUM — Constraints pacing is a fifth term and silently overrides the preference rule
**Location:** Row 55, "Drafted inherited half, then one prompt".
**Problem for AI:** Gather's "Drafted" means derived from earlier answers; the inherited half is copied from a loaded document, which under `guided` style should be prompted, not drafted. The row intends the copy regardless of style but does not say so. Fix: "Two prompts: 6.1 is drafted from the charter's constraints regardless of gathering style, since it is a citation rather than a decision; 6.2 is one prompt." Charter row 50 uses this "regardless of mode" phrasing already; match it.

### MEDIUM — Two template comments steer an instructional design student toward the wrong artifact
**Location:** Template line 67 (Objectives: "By [when], [who] will be able to [do what], measured by [how]") and lines 117–118 (Use Case ID example: "A [learner] encountering [situation] will [action] and demonstrate [outcome]").
**Problem for humans:** Both formulas are the shape of a learning or performance objective, which an ID student already has a name for. They will fill Objectives with the module's learning objectives and Use Cases with performance statements, and the spec loses its project-level view. Fixes: append to line 67, "These are project objectives, what the work achieves; the deliverable's own learning objectives belong in requirements." Replace lines 117–118 with "Instructional design: 'A [learner or facilitator] in [setting] uses [the deliverable] to [do what], and [what results].'"

### LOW — Exit that skips the gate
**Location:** Pre-flight step 5, "offer to continue or to run `/charter` first". If the user chooses `/charter`, this run ends without a Status. Append: "If they choose `/charter` first, set Status to `cancelled` and stop; they re-run `/describe` afterward."

### LOW — Small clarity items
- Line 61 "DIPs" is never expanded; line 10 says "implementation prompts". Write "design and implementation prompts (DIPs)" once.
- MUST-needs-AC is stated three times (rule 20, row 54, line 65) and the rule carries no reason. Keep rule 20 with "because an acceptance criterion is how done is verified" and drop it from row 54.
- Row 52 NFR list says "Usability/Accessibility"; template line 86 says "accessibility". Same drift class as charter Round 1; make one match the other.
- Line 43 "Gather in template order" while the table gathers Related Documents (top of template) last. Say "in the order below". Charter line 40 has the same wording.
- Line 39 restates gather's source-material mechanics (references folder, read before gathering), as charter line 36 does. Pattern-level; keep only the spec-specific example list and the rubric sentence.
- Row 51 "With source material, draft each one; approval is fast" restates gather's draft-first rule. Cut.

## Pacing table consistency

Consistent with gather's four terms and the charter's phrasing. Ten of thirteen rows use a term verbatim or the charter's "One prompt, categories as a checklist" variant. The exceptions are row 55 (above) and row 54/59 "Drafted by you", which matches gather's "Drafted". The Title row ("Skip if given as the argument") is a sensible new case that gather need not name.

## Signal-to-noise

Good at 100 lines. Every section is load-bearing and the reasons survive the clone (sequential pre-flight, copy-then-edit, gate, stable IDs). The only cuts are the three items above (row 51 second sentence, one MUST restatement, source-material mechanics), about six lines.

## What's Well-Engineered

- `argument-hint` and the step-4 new-or-revise decision are explicit and testable.
- Rule 18 (checklist marking) and the maintainer note as an HTML comment carried forward correctly from the charter fixes.
- The stable-ID rule states its reason. It only needs to be in view at generate time.
- Review and Confirm reports counts and the MUST-coverage gap, giving the user a real check before saving.
- Template Problem Statement examples are quantified across four domains, and the Status lifecycle comment is one line where it is needed.
- Success message next step 1 ("something you would refuse to ship without") teaches what MUST means.

## Top 5 Changes, Ranked

1. Add the update-mode branch to generate step 4 ID assignment.
2. Replace rule 19 with provisional-then-final ID assignment.
3. Derive the Charter Reference principles in generate step 5.
4. Fix gather's "scope items" example and the Constraints pacing row.
5. Rewrite the two ID-student template comments (Objectives, Use Case example).

---

## Round 2 — 2026-09-22 (delta pass on the revision)

### Resolved
All Round 1 findings are resolved except one partial. The high finding is closed: Generate step 4 no longer numbers anything and writes "each item's already-assigned ID" (line 76). The IDs-on-approval rule is visible from every place it matters: Rules line 20 (with its reason), pacing rows 52, 53, 54, 55, and 59 ("Assign X on approval"), Review and Confirm line 66 ("nothing renumbers"), and Generate line 76. Charter Reference is derived (row 60). Gather's one-at-a-time example now says use cases, which both skills pace that way. Constraints row 56 says 6.1 is drafted regardless of style and why. The Objectives comment explains project versus learning objectives and the Use Case ID example is a scenario. The `/charter`-first exit sets `cancelled`. DIPs is expanded. NFR lists match. "Order of the table below" replaces "template order". Source-material mechanics defer to gather, and the rubric-to-criteria mapping (line 40) is a good spec-specific addition.

**Partly resolved:** MUST-needs-AC still appears in three places (rule 21, row 55, line 66), but rule 21 now carries the reason and a blocking behavior with a TBD escape hatch, and each restatement has a distinct role. Acceptable as is.

### New

**MEDIUM — "Next unused number" can mean a gap.** Rule line 20: "take the next unused number in their series ... A removed item leaves a gap." If REQ-F3 was removed and deleted (uncited, per line 62), F3 is literally the next unused number, and an agent may refill it. Deleting the row also hides the series maximum, so a removed REQ-F5 gets reissued. Fix, two parts: rule 20 says "the highest number ever assigned in that series plus one; a gap is never refilled"; and line 62 drops the citation search and always keeps a removed row struck through with "removed in v[version]", which is what keeps the maximum visible. This also removes a grep step and matches the template's Revision History comment (line 249), which already says removed items keep their row.

**LOW — Objectives row lacks the "Assign OBJ-n on approval" note.** Row 51 is the only ID-bearing row without it. Rule 20 covers it, but since every other series is called out, the omission reads as intentional. Add the note.

**LOW — Checklist-over-table rule and sub-headed tables.** Rule 19 says an unanswered category "simply produces no row; the section is N/A only when nothing applies." Dependencies has two sub-headed tables (7.1, 7.2). If only Depends On is answered, it is unclear whether 7.2 Enables becomes N/A or an empty table. Add: "a sub-section with its own heading gets N/A when it has no rows."

**LOW — Template line 11 "IDs are assigned sequentially"** now understates the rule. Say "assigned in approval order and never renumbered."

**LOW — Confirm the DIP expansion.** Line 10 expands DIPs as "Detailed Implementation Prompts". The previous draft implied "design and implementation prompts". Whichever is canonical will be copied into three more skills; verify before cloning.

No regressions, no new elephants. The one near miss, "A scenario, not a learning objective" (template line 136), sits directly after the correct pattern and next to the Objectives comment that says where learning objectives go, so it orients rather than primes.
