## Critic Review: /do skill (execution skill, consumer of the DIP contract)

**Artifact:** `.claude/skills/do/SKILL.md`; producer side `.claude/skills/detail/SKILL.md` and `templates/dip.template.md`; prototype `.claude/commands/build.md`
**Date:** 2026-10-02 | **Dispatch Mode:** Mode 1 (team-lead consult) | **Reviewer:** critic

## Instructions Received

Check the DIP contract end to end: every Status value handled and set at the right moment, legacy no-Status DIPs, the resume point after a Halted revision, In Progress after an interrupted session, scope check and bookkeeping exemption, whether skip leaves DIP, PLANNING.md, and commit consistent, deferred acceptance rows, the no-git path, the extra sentence in the PLANNING.md contract, and anything wrongly dropped from build.md.

## Findings

### Important — The resume point is lost the moment a Halted DIP is revised
**Location:** Pre-Flight 4 (**Ready:** proceed); `/detail` Generate 5 ("a Halted DIP returns to Ready") and its Completion Gate (Next Steps names "the DIP file and the element").
**Problem:** The halt lives in the Status row, which `/detail` resets to Ready, and in PLANNING.md Next Steps, which `/detail`'s Completion Gate overwrites. After the user fixes step 3 with `/detail`, `/do` sees Ready and starts at step 1, re-running steps whose Outputs exist ("Create the migration file" against a file that is there). The Success Message's own advice, "`/detail DIP-NNN` to revise the step," leads straight into this.
**Fix:** In `/detail`, the Revision History row for a Halted-to-Ready revision reads "revised after halt at Step N; resume at Step K." In `/do` Pre-Flight 4, Ready: "if the last Revision History row names a resume step, offer resume at K with the Outputs check from the Halted branch, or restart."

### Important — The commit ships the DIP as In Progress and PLANNING.md as in progress, then dirties the tree
**Location:** Safety and Commit 4 and 6 (stage DIP file and PLANNING.md, commit); Completion Gate (set Done, set PLANNING.md `complete`) runs after.
**Problem:** Both bookkeeping files are staged and committed before their final values are written. Every DIP commit records `Status | In Progress`, and the Completion Gate's edits immediately leave two modified files, so the next `/do` run's dirty-tree check fires on the framework's own bookkeeping.
**Fix:** Move the Status `Done` write and the PLANNING.md update ahead of staging (the hard gate is still "before the success message"). Keep the commit hash out of PLANNING.md; the Success Message shows it and `git log` keeps it. On a halt nothing is committed, which is correct, and the dirty-tree prompt then explains itself.

### Important — The In Progress step pointer lives only in a line any other skill overwrites
**Location:** Execute 4 ("record `DIP-NNN at step N` in PLANNING.md's Next Steps"); Pre-Flight 4 **In Progress** ("resume from the step PLANNING.md's Next Steps last recorded"); Rules 4 ("The DIP's Status row is the durable record").
**Problem:** If any skill runs between the interruption and the resume, its Completion Gate replaces Next Steps and the In Progress branch has no step to offer. The rule says the DIP is the durable record; the step pointer is not in it.
**Fix:** Status row `In Progress — Step N` rewritten at each pass; Execute 4's PLANNING.md line becomes a pointer only, and "record" should say "replace the line," since Next Steps is a list.

### Medium — Legacy DIPs have none of the headings /do parses
**Location:** Pre-Flight 4 **No Status row** ("treat the answer as Done or Ready"); Pre-Flight 7 ("Set the DIP's Status row"); Safety 2 ("Artifacts in Scope").
**Problem:** DIP-001 to 007 have `Implementation Instructions`, `Files in Scope`, `Verification Commands`, a `Must Implement` checklist, no Status row to set, and a TodoWrite header. Answering "Ready" sends `/do` into a file where the scope block it looks for does not exist, so every changed file is out of scope.
**Fix:** "A DIP with no Status row is run only after `/detail DIP-NNN` has brought it to the current template; stop and say so." That reuses the update flow's "structure differs from the template" walk and keeps `/do` parsing one shape.

### Medium — Without git, the three tool-neutral safety items are skipped too
**Location:** Safety and Commit ("Skip this phase when the project is not under git"); template Safety Checklist comment ("The first three apply to any work").
**Fix:** "Walk the first three checklist items always; without git, skip items 2 to 6 of this phase and the last two checklist lines."

### Medium — Two Status forms are set but never handled, and deviations have no durable home
**Location:** Acceptance 4 (`Halted — Acceptance: AC-n`); Completion Gate (`Halted — Step N: cancelled by user`); Execute 5 ("skip it and record the deviation ... the DIP itself is not edited"); Execute 6 ("widening scope with the user's explicit yes"); line 55 (only fix-and-retry clears Halted).
**Problem:** Pre-Flight 4 resumes only `Halted — Step N`; an acceptance halt offers no path to "all steps done, rerun acceptance." A skip leaves the row at `Halted — Step N` while the run continues, so a second failure overwrites the first reason, and the deviation is recorded only in PLANNING.md (overwritten later) and the commit body (absent without git). In-run scope widening edits the DIP's Artifacts in Scope while In Progress, which `/detail` forbids and Execute 5 says `/do` never does. "Returns to the step that owns the failing behaviour" assumes a mapping the DIP does not hold.
**Fix:** Add an **Acceptance** halt branch to Pre-Flight 4 (resume at the Acceptance phase). Clear to In Progress on skip as well as retry. Record every deviation (skipped step, widened scope, acceptance override) as a dated line in the DIP's Notes section; that is the bookkeeping edit the exemption already covers. Drop in-run widening; a scope-blocked halt is already Halted and therefore revisable with `/detail`. Let the user name the step to return to.

### Low — PLANNING.md contract sentence and cancel-after-a-step
The added sentence is consistent with the closed set (`complete` for a halted run), but it makes this the one copy of the contract that differs from the other four, and the same fact is already in Rules 4. Move it out of the bold paragraph so the five copies stay identical. Completion Gate says what the DIP reads after a cancel-after-a-step but not what PLANNING.md reads; say `complete` with the halt in Next Steps.

### Dropped from build.md
Nothing that should return. Dirty-tree approval (Pre-Flight 5), verification duality (Rules 2), resume (now via the DIP row plus Next Steps, better once the fixes above land), deviations in the commit body, and the "Files in Scope" check (renamed) all survive. Todoist is gone, correct for this branch. Build's "skip re-reading documents you saw earlier this session" is reversed to "do not skip," the right call for a skill whose premise is a fresh session.

## Unstated Assumptions
- Only one DIP is In Progress at a time; the Next Steps pointer and the Status row both assume it.
- The DIP file's own edits (ticks, Status) are small enough that staging them with feature work is acceptable; a repo with a `.plans/`-free history policy would want a separate `dip(...)` commit.
- Step Outputs are inspectable artifacts, so "confirm the Outputs of steps 1 to N−1 still exist" is a check and not a memory test; for human-judged Outputs it is a question to the user.

## Ranked Top 5
1. Carry the resume step through a Halted-to-Ready revision via the Revision History row, and have Ready check for it.
2. Write Done and PLANNING.md `complete` before staging, so the commit holds final state and the tree is clean after.
3. Keep the step pointer in the Status row (`In Progress — Step N`), not only in Next Steps.
4. Refuse legacy no-Status DIPs until `/detail` has rebuilt them on the current template.
5. Handle the Acceptance halt, clear Halted on skip, and record deviations in the DIP's Notes.

## Strengths
The contract listed in the detail report is honoured almost line for line: Status values, the three Verify forms shared by steps, AC Tests, and the Verification block, deferred rows treated as deferred, the bookkeeping exemption with named files, the Outputs check on resume, and the refusal to skip Required Reading from memory. "An ambiguity resolved by guessing becomes a defect two steps later" is the right one-line reason for the halt rule. The scope-blocked halt (Execute 6) is a case build.md never named.

## Self-Evaluation
- **What worked well:** Walking the order of writes in Safety and Commit against the Completion Gate exposed the commit-ordering defect, which no single section shows.
- **What you struggled with:** The legacy-DIP finding is partly a policy question (alias old headings or refuse); I recommended refuse because it keeps one parse shape, but the user may want to run DIP-007 as is.
- **Prompt improvement suggestions:** Add to the checklist: "when a skill commits its own bookkeeping, check that the final status writes land before the stage, not after."

---

## Round 2 — 2026-10-02 (delta pass on the rewrite)

### Resolved
Completion Gate runs before staging and the hash stays out of PLANNING.md. Progress lives in the Status row. Halted-to-Ready carries "resume at Step K" in the Revision History row (detail Generate 5) and the Ready branch reads it. Acceptance and Verification halts have a resume branch. Skip clears Halted and writes a dated Notes line. Scope is never widened mid-run. The three tool-neutral safety items run without git. Legacy DIPs are refused. The PLANNING.md contract paragraph is byte-identical to the other four again. Cancel-after-a-step now states both files' values.

### Status strings, writer to reader
| String | Writer | Reader | Result |
|---|---|---|---|
| `Ready` | detail Generate 5 | do PF4; detail step 4, 5e | OK |
| `In Progress` (bare) | do PF7 | none in PF4 | **Gap:** a session interrupted during step 1 matches no branch. Add: "bare In Progress: interrupted before any step passed; offer restart or cancel." |
| `In Progress — Step N passed` | do Execute 4, retry pass | do PF4 | OK |
| `In Progress — Step N skipped` | do Execute 5 Skip | none in PF4 | **Gap:** the resume branch names only "passed." Widen it to "passed or skipped: resume at N+1." Also warn on resume that step N+1 may be partly done; the Outputs check covers only 1 to N. |
| `Halted — Step N: [reason]` | do Execute 5, 6; Gate 3 | do PF4; detail step 4, update flow | OK |
| `Halted — Acceptance: AC-n` | do Acceptance 4 | do PF4 | OK in do. **Gap in detail:** Generate 5 writes only "resume at Step K"; for a revised Acceptance or Verification halt it should write "resume at Acceptance," and do's Ready branch should read that form too. The update flow's "the halted step is the likely target" has no step here; say "or the failing criterion." |
| `Halted — Verification: [..]` | do Acceptance 2 | do PF4 | OK, but Acceptance 4's three choices are stated only for criterion failures; say "any fail in 1 or 2." |
| `Done` | do Gate 1; template blockquote | do PF4; detail step 4 | OK |

### Partly or not resolved
- **Halt then commit is undefined.** Safety and Commit has no halt guard; the Gate says "leave the Halted status" and continues into staging, while the Success Message lists "halted" as a reason for "not committed." Say which: on a halt, skip Safety and Commit and leave the tree as it is. Then PF5's dirty-tree exemption must also cover Artifacts in Scope of the DIP being resumed, or every resume trips on its own partial work.
- **Two migration paths for a legacy DIP.** do PF4 says rebuild "as a custom DIP referencing the same elements" (new number, old file orphaned); detail step 4 revises a no-Status DIP in place through the update flow (number kept, structure mapped to the template). Pick in place and have do point to `/detail DIP-NNN`.
- **"The step that owns the failing behaviour"** (Acceptance 4) still assumes a mapping the DIP does not hold; let the user name the step.

### Round 2 verdict
The rewrite closes every Round 1 finding. The remaining holes are two unread Status strings (bare In Progress, skipped), the undefined commit-on-halt, and the Acceptance form of "resume at." All are one-line fixes.