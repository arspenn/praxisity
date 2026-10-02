## Critic Review: /detail skill (fourth clone of the pattern)

**Artifact:** `.claude/skills/detail/SKILL.md`, `templates/dip.template.md`; pattern `/design`, `/describe`; protocol `/gather`; prototype `.claude/commands/define.md`; consumer `.claude/commands/build.md`; example output DIP-006
**Date:** 2026-10-02 | **Dispatch Mode:** Mode 1 (team-lead consult) | **Reviewer:** critic

## Instructions Received

Review /detail against its siblings and the old /define, with attention to the argument grammar and revise gate in pre-flight 4 and 5, the Ready-only revision rule, the NNN/DDD/MMM tokens, the two save gates, "cites not restates" for a fresh session, what was dropped from /define, and what /do will need from a DIP.

## Findings

### High — The revise gate reads a Status field that no existing DIP has, and silently falls through to "new"
**Location:** Pre-Flight 4: "If its Status is Ready ... If its Status is In Progress, Done, or Halted ... Otherwise continue to step 5."
**Problem:** Grep for `Status |` in `.plans/prompts/` returns nothing; all seven DIPs predate the field. `/detail DIP-006` reads the file, matches neither branch, and continues to step 5 as a new DIP with no message. The same hole is in step 5's "If a Ready DIP for this element already exists."
**Fix:** "If the DIP has no Status field, it predates this template: ask once whether it was executed. Executed means follow-up; not executed means revise, and the update flow adds the Status row." Treat a missing field as unknown, never as "otherwise."

### High — A Halted DIP cannot be fixed, only replaced
**Location:** Rules bullet 6; template Status comment; `/build` Execution 6 (halt → "fix and retry this step, skip, or abort") and Pre-Flight 3 (resume).
**Problem:** The commonest reason a step fails is that the step is wrong: a bad path, a missing input, a Verify that cannot pass. `/build` offers resume from the halted step, which only helps if the DIP text can change. The rule forbids revising anything past Ready, so the user must write a follow-up DIP that re-executes steps k..N against artifacts half-built by a DIP frozen as Halted. No one asked for the strict freeze; the rationale given ("nothing outside the DIP cites a step") argues for renumbering freedom, not for the freeze.
**Fix:** Freeze Done and In Progress. A Halted DIP may be revised: the update flow lists the halted step and reason from PLANNING.md first, the revision resets Status to Ready and bumps the version, and `/do` resumes at the step the user names. Who sets Status must be stated once, in the template comment, as `/do`; and the Success Message's "any agent can be handed the file" path leaves Status at Ready forever, so say that too.

### High — The MUST gate has no named exit, and the DIP cannot show which rows are MUST
**Location:** Rules bullet 5; Review and Confirm ("offer only edit or cancel"); template Must Satisfy table (no Priority column).
**Problem:** Design and describe name every escape from their gates. Here "edit" is the only one, and two cases have no in-DIP edit: the spec's Acceptance Criteria is `TBD` for that MUST (describe allows it with a milestone), or the AC is only testable once a sibling element exists (REQ-F1 satisfied by COMP-1 and COMP-3 jointly, this DIP builds COMP-3). Separately, the Must Satisfy table drops priority, so neither the reviewer nor the executing agent can tell a MUST row from a SHOULD, and the gate is checked only in the skill's head.
**Fix:** Add a Priority column to Must Satisfy. Name three exits: write the Test here; mark the row "verified in the DIP for COMP-x" when the criterion needs a sibling, carried into Next Steps; or cancel (Status `cancelled`) to add the criterion with `/describe`.

### Medium — Argument grammar contradicts step 5 and makes bare numbers into task titles
**Location:** Argument paragraph: "`DESIGN-NNN` with an element ID selects the element. Anything else is treated as a task description." Pre-Flight 5: "If no element was given, show the design's components ..."
**Problem:** By the paragraph, `/detail DESIGN-004` is "anything else" and becomes a custom DIP titled "DESIGN-004"; step 5 assumes it selects the design. `/detail 005` becomes a custom DIP titled "005"; in this repo 005 is a DIP, a design, and a spec. Three independent series make the collision routine.
**Fix:** "`DESIGN-NNN` alone selects the design and asks for the element. A bare number is ambiguous across DIPs, designs, and specs: ask which. Anything else that is not an ID is a task description."

### Medium — The "already has a DIP" check greps the element ID without the design
**Location:** Pre-Flight 5: "search `.plans/prompts/` for the element ID with Grep."
**Problem:** `COMP-3` matches DIP-001 (DESIGN-001), DIP-002 (DESIGN-002), and DIP-006 (DESIGN-004) today. Every design has a COMP-1.
**Fix:** Grep for the design's file name or `DESIGN-DDD` first, then for the element within those files; for new-template DIPs read the Context table's Element and Design rows.

### Medium — The custom DIP has no shape
**Location:** Argument paragraph; Pre-Flight 5 last sentences; template Element row ("custom task"); Gather rows for Must Satisfy, Required Reading, Acceptance Criteria, which all start from "the element's Satisfies list."
**Problem:** With no element there is no Satisfies list, so Must Satisfy and Acceptance Criteria (required) have no source, the MUST gate is vacuous, and "cites, does not restate" has nothing to cite, so the steps must carry everything. The Design and Specification rows are single-valued while "which design elements it relates to" may span designs. Also the no-argument path has no way to reach custom; /define offered it from its menu.
**Fix:** One paragraph: a custom DIP names one design in Context, lists related elements in Required Reading, draws Must Satisfy from those elements' Satisfies lists or marks it `N/A — no requirement owns this`, and then Acceptance Criteria must hold at least one DIP-local criterion with a Test. Offer custom in step 5's element prompt as the last option.

### Medium — `.plans/prompts/` is never created
**Location:** Pre-Flight 4 and 5 (`ls`), Generate 2 (`cp` to `.plans/prompts/NNN-[slug].md`). /define step 6 created it; describe says "(create the directory if missing)".
**Fix:** Add the parenthetical to step 4's `ls`.

### Low — Revise path skips the charter read; step 5's "revise it" skips reading the DIP
Step 4 Ready → "go to step 7" bypasses step 6, so the charter block cannot be re-derived in update mode (design routes revise through its charter step). Step 5's "revise it (go to step 7)" never reads the existing DIP in full. Fix: "read it in full and continue as step 4's Ready path," and route both through step 6.

### Low — Template details
Required Reading and Must Satisfy show only `REQ-Fn`; REQ-N MUSTs are in spec §3.2 and are the ones most often design-wide. Generate 4 says DDD and MMM carry "number and slug," but `slug` in `DDD-slug.md` is an unbracketed literal no listed operation replaces; same wording in design. The commit template `DESIGN-DDD COMP-n` has no custom form. The template header says the conventions are "identical in every Praxisity template" and here they are, verbatim against design.

### Dropped from /define
Todoist path: dropped, correct for the consolidate branch; `/build` still has a Todoist completion step that `/do` should drop in step. Auto-generation: kept as "Drafted by you" rows. Custom task: kept only via free text (see above). Directory creation: dropped, should return. TodoWrite header and Completion Checklist: dropped from the template; `/build` owns both, correct.

### What /do will need
The template renamed Files in Scope to Artifacts in Scope; `/build` Completion 2 says "Files in Scope," so `/do` must be written against the new heading. `/do` must set the DIP's Status (Ready → In Progress → Done/Halted), which is an edit to a file outside Artifacts in Scope; the Safety Checklist line "Only artifacts in scope were changed" and the staged-file check will flag it, along with PLANNING.md. Decide now whether `/do` commits the Status change with the work (and exempts `.plans/` and PLANNING.md from the scope check) or leaves it unstaged. Step structure (`### Step N:`, `**Verify:**`), the AC Test column, and the Commit block survive unchanged from what `/build` parses.

## Unstated Assumptions
- Every DIP cites one design and one spec; the custom path and multi-element "relates to" break this.
- Design-wide REQ-N MUSTs (covered in design §7.4, in no element's Satisfies) never reach any DIP's Must Satisfy, so nothing tests them at implementation. Say where they are tested, or say they are not.
- The executing agent runs from the project root so `../designs/` resolves, and reads whole sections, not labels, when the DIP cites.

## Ranked Top 5
1. Treat a missing Status as unknown and ask; never fall through to "new."
2. Allow revising a Halted DIP with a version bump and Ready reset; say who sets Status.
3. Add Priority to Must Satisfy and name the three exits from the MUST gate.
4. Fix the argument grammar: `DESIGN-NNN` alone selects, bare numbers ask, directory gets created.
5. Qualify the existing-DIP grep by design and give the custom DIP a defined shape.

## Strengths
Every carried-forward fix from the design review landed first time: `DDD`/`MMM` tokens with no collision, `DESIGN-` prefix semantics, re-read before `cp`, Revision History dated "on or after," struck-ID surfacing in the update flow, save withheld at Review. The split from the old 300-line DIP to "cites, does not restate" is the right call for a document that must survive spec changes, and the Verify-per-step gate is enforceable from the DIP alone. The renumbering-while-Ready rule is correctly reasoned from "nothing cites a step."

## Self-Evaluation
- **What worked well:** Grepping the live prompts directory for `Status |` and `COMP-3` turned two reasoned risks into observed failures.
- **What you struggled with:** The Halted finding depends on how `/do` is built next; it is a design recommendation, not a defect in text already written.
- **Prompt improvement suggestions:** Add to the checklist: "when a gate or branch keys on a field, grep the existing artifacts for that field; legacy files without it fall into whichever branch is 'otherwise.'"

---

## Round 2 — 2026-10-02 (delta pass on the revision)

### Resolved
Missing Status asked, not fallen through (step 4). Halted revisable with Ready reset, `/do` named as the Status setter (Rules 6, step 4, Generate 5, template comment). Priority column on Must Satisfy; three gate exits in Rules 5, Review and Confirm, and the AC comment. Argument grammar: `DESIGN-NNN` alone selects, bare numbers ask. Element grep qualified by design ID (5c). Directory created (step 7). Custom task offered as the last option (5c) with a stated source (5d). Bookkeeping edits exempted in the Safety Checklist. `DDD`/`MMM` and `-slug` now named separately in Generate 4.

### Partly resolved
- **Custom DIP inherits obligations it does not own.** 5d draws Must Satisfy from the related elements' Satisfies lists, so a custom task "relating to" COMP-2 inherits COMP-2's MUSTs and the gate demands tests for requirements the task does not fulfil. And when no requirement applies, Must Satisfy is N/A and Acceptance Criteria (required) has no source. **Fix:** "Must Satisfy holds only the requirements the user affirms this task advances; the rest stay in Required Reading. With none, Must Satisfy is `N/A — no requirement owns this` and Acceptance Criteria holds at least one DIP-local criterion with a Test." Title for a custom DIP comes from the argument, not "the element name."
- **Charter skipped on revise.** Step 4 still routes to step 7 past step 6; 5e says "via step 4's revise path," so it inherits the skip. Route revise through step 6.
- **Manual execution never moves Status.** The success message allows following the steps by hand; Status stays Ready and the DIP remains revisable after the work exists. Add one line to the executor blockquote: "When finished, set Status to Done."

### New gaps
- **Medium — The sibling exit cites a number that does not exist yet.** "tested in DIP-NNN" (Rules 5, AC comment) assumes the sibling DIP has been written; Implementation Order usually puts the dependency's DIP first, so the sibling has no number. Nothing carries the deferral forward: the Completion Gate's Next Steps names only the file and element, and 5b does not look for deferrals aimed at the element it is about to detail. **Fix:** write "tested in the DIP for COMP-x"; Completion Gate adds "any criterion marked TBD or deferred to a sibling"; 5b greps `.plans/prompts/` for "tested in the DIP for [this element]" and seeds those criteria into the AC draft. Also say which cell carries the TBD marker when the spec's AC has no ID: the Criterion cell, with Validates still filled.
- **Medium — The halt note's PLANNING.md location does not survive to the revise.** The update flow reads "the halt note from PLANNING.md or the DIP's Status row," but `/detail` step 2 has already overwritten Active Context before the update flow runs, and `/build` writes its halt state nowhere else. **Fix:** the DIP's Status row is the durable place: `Halted — Step N: [reason]`; PLANNING.md Next Steps carries a pointer only. Say so here and in `/do`.
- **Low — A follow-up DIP has nowhere to cite its predecessor.** Step 4 and the Status comment promise a follow-up "that references it," but Context, Required Reading, and Notes have no field for a prior DIP. Add a `Follows` row to Context, `N/A` by default, and a Required Reading block "From [DIP-NNN](NNN-slug.md)" when set, including a Done DIP's artifacts as the starting Input.
- **Low — Order inside 5b.** "Hold the element's block" sits in 5b before the element is chosen in 5c; move it after 5c and phrase for the custom case as "the related elements' blocks."
- **Low — Stale lines.** Revision History comment (line 226) says "while the DIP is Ready"; now Ready or Halted. Template header (line 5) still names "the AI agent" as the executor while the blockquote says person or agent. Step 4's `ls` and 5c's Grep run on `.plans/prompts/` before step 7 creates it; harmless, but say "if it exists."
- **Cite-only AC table:** no gap. Join Must Satisfy.Requirement to AC.Validates and the MUST gate is checkable from the file alone, which it was not before; `/build` only ever consumed the Test column.

### What /do needs from a DIP
- **Status row** in the Context table. Values: `Ready`, `In Progress`, `Done`, `Halted — Step N: [reason]`. `/do` sets all but Ready; `/detail` resets Halted to Ready. A DIP with no Status row (DIP-001 to 007) is treated as Ready and the row is added on first run, or `/do` refuses and names `/detail`; pick one.
- **Resume point.** After a Halted DIP is revised, `/do` asks whether to resume at the previously halted step or restart; the Revision History row names the halted step, so that is where to read it.
- **Step blocks:** `### Step N: [Action]` under `## Implementation Steps`, body text, then bold `**Input:**`, `**Output:**`, `**Verify:**` lines. Input and Output may be absent (folded into the body); Verify is always present. Parse on the H3 and the bold label, not on line position.
- **Verify forms**, identical in step Verify, the AC Test cell, and the `### Verification` fenced block: a command (run it), an observable check (inspect and judge), a named human judgment "who looks at what" (present to that person, record pass/fail). A Test cell reading `TBD — revisit at` or `tested in the DIP for` is skipped with a note, not failed.
- **Required Reading:** three `### From` blocks of checkbox lines, or a single `N/A` line; `/do` reads each cited section and ticks the box.
- **Artifacts in Scope:** fenced block under `### Artifacts in Scope`; entries are a path, a directory with trailing slash, or `file, named location` (the file is the git-checkable unit). `### Artifacts Out of Scope` is the deny list. The DIP file itself and PLANNING.md are exempt from the scope check; decide whether they are staged with the work or in a separate `dip(...)` commit, because the Commit Instructions block lists only artifacts in scope.
- **Safety Checklist:** five checkbox lines, the last two absent when not under version control; `/do` confirms each before finishing, and the "Files in Scope" wording in `/build` must become "Artifacts in Scope."
- **Must Satisfy Priority** and **AC Validates** columns give `/do` the MUST list to report against; `/do` never appends to Revision History.

### Round 2 verdict
All eight named items landed; the remaining work is the forward reference for deferred criteria, the durable halt location, and tightening the custom path's obligations. Carry the `/do` list above into that skill before it is drafted.
