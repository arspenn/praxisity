## Prompt Engineer Review

**Artifact:** `.claude/skills/do/SKILL.md` (consuming `.claude/skills/detail/templates/dip.template.md`; replacing `.claude/commands/build.md`)
**Date:** 2026-10-02
**Dispatch Mode:** Mode 1 (subagent consult)

## Instructions Received

Review /do as a prompt for an agent running real commands against a real repo. Specific questions: elephants around "do not improvise" and git; dispatch of the three Verify forms; followability of halt/resume/restart in Pre-Flight 4 and Execute 5; cost of the per-step PLANNING.md write; whether "fix and retry" has a shape; signal-to-noise. Under 100 lines.

## Dual-Consumption Assessment

### Elephants — "Do not improvise" is bounded on one side only
**Location:** lines 10, 16, 17, 49
**Problem for AI:** The file says stop-and-ask four ways (does not improvise, not a judgment call, cannot tell which form, resolved by guessing) and never says what is not a question. An execution agent primed this hard will ask about indentation, variable names, and which of two equivalent commands to run, and the user will answer twenty questions for a ten-step DIP. The prototype had the same unbounded form. The git negations ("never `git add .`") are fine: the forbidden command is more checkable than "stage by name" alone, and it appears once in Rules and once in the checklist the DIP carries.
**Suggested fix:** One sentence after line 49: "An ambiguity is two readings that would produce different Outputs; a choice that leaves the Output the same is yours to make."

### Ambiguity — The observable check has no decider
**Location:** Rule line 17; Execute step 3-4
**Problem for AI:** Command: run it. Human judgment: ask pass or fail. Observable check: "perform it and report what you saw." Who declares pass? Step 4 says "Pass: mark complete" without a subject. One session will self-certify every observable check, collapsing it into the command form; another will ask the user, collapsing it into the human form. The dispatch signal is also unstated: the DIP template defines the human form as naming who looks at what, which is a usable test.
**Suggested fix:** "Identify the form from the text: a command is runnable as written; a human judgment names who judges; anything else is an observable check, which you perform and decide against what the Verify states, reporting what you saw and the verdict."

### Ambiguity — "At step N" means two different things
**Location:** Execute step 4 (line 51); Pre-Flight 4 In Progress branch (line 36); Halted branch (line 35)
**Problem for AI:** On pass, the record is `DIP-NNN at step N`, meaning N finished. A halt reads `Halted — Step N`, meaning N failed. The In Progress branch says resume "from the step last recorded", and the agent cannot tell whether that is N again or N+1. If the session died between Pre-Flight 7 and the first pass, nothing is recorded and the branch has no answer.
**Suggested fix:** Record `DIP-NNN: step N passed` and have the In Progress branch say "resume at the step after the last one recorded as passed, or step 1 if none."

### Noise — The per-step PLANNING.md write serves one branch and the wrong file
**Location:** Execute step 4; Rule line 19
**Problem for AI:** Rule 19 names the DIP's Status row as the durable record. The per-step write goes to PLANNING.md's Next Steps instead, which is a list any skill overwrites and which an Edit must find by text. Cost is one tool call per step plus the diff clutter; the only reader is the In Progress branch. The task tracker already holds within-session state.
**Suggested fix:** Keep one write per step but make it the Status cell: `In Progress — step N passed`. Drop the PLANNING.md write from Execute; PLANNING.md is written in Pre-Flight 2 and at the gate. The In Progress branch then reads the same row it already reads to dispatch.

### Clarity — Fix-and-retry has no shape
**Location:** Execute step 5 (line 52); line 55
**Problem for AI:** "Fix and retry this step (the user supplies the fix or tells you how)" leaves open: may the agent propose the fix; is the fix bounded by Artifacts in Scope; does retry re-run the Verify or redo the step from its Input; is there a retry limit. The parenthetical also forbids the agent proposing, which it will do anyway because it is what a user expects, so behaviour differs by session.
**Suggested fix:** "Fix and retry: you may propose a fix, the user approves it, you apply it within Artifacts in Scope, then re-run the step's Verify (redo the whole step only if the user says so). A second fail on the same step is a stop; the step needs `/detail`."

### Drift — Halt states that no branch resumes
**Location:** Acceptance step 4; Pre-Flight 4
**Problem for AI:** Acceptance writes `Halted — Acceptance: AC-n`, but Pre-Flight 4 only dispatches `Halted — Step N`. A session resuming from an acceptance halt matches no branch. Line 55 clears Halted only for fix-and-retry; after a skip the Status stays Halted while execution continues, and the gate then cannot tell a skipped step from a run that ended in a halt. A Verification-block failure (Acceptance step 2) has no status string at all.
**Suggested fix:** Add a Halted — Acceptance branch (resume at Acceptance, all steps done). Make line 55 cover skip as well as fix-and-retry. Give the Verification block the same fail path as a row.

### Ambiguity — Deferred-criterion string does not match the template
**Location:** Acceptance step 1 (line 61); template Acceptance Criteria comment
**Problem for AI:** /do matches "tested in the DIP for COMP-n"; /detail writes "tested in DIP-NNN". A literal match fails and the row is run as a test.
**Suggested fix:** Match on the prefix "tested in".

### Clarity — Dirty-tree check will flag the previous run's own bookkeeping
**Location:** Pre-Flight 5
**Problem for AI:** A halt leaves the DIP's Status edit and partial outputs uncommitted. The next run's `git status` lists them as foreign uncommitted work and asks the user to stash their own half-done DIP.
**Suggested fix:** "On a resume, changes to the DIP file, PLANNING.md, and Artifacts in Scope are the previous run's work and are expected; list anything else."

## Answers to the Remaining Questions

- **Halt/resume/restart in Pre-Flight 4:** followable for Ready, Halted — Step N, Done, and no-Status. The In Progress branch is the weak one, per the "at step N" finding. Restart from step 1 is followable but will hit the dirty-tree check with the old outputs, which the Pre-Flight 5 fix handles.
- **Signal-to-noise:** good for 93 lines. "Never commit without a yes" and "stage by name" each appear in Rules and in Safety; that is tolerable because Rules primes and Safety executes. Completion Gate line 79 packs six things to write into one sentence and should be a list. Line 41's refusal to skip Required Reading from memory is a deliberate reversal of the prototype and earns its place.

## What's Well-Engineered

- The three-form Verify with "if you cannot tell, ask" is a clear improvement on the prototype's two-way duality; it only needs the decider named.
- Required Reading ticked in the DIP file makes the executor's reading auditable in the diff.
- Blocked-by-scope is its own branch with its own status string, separate from a Verify failure. That is the right distinction.
- The success message carries "not committed" with a reason, so an optional outcome is never asserted.
- Bookkeeping edits are named as outside the scope check, closing the contradiction Round 2 found in the DIP template.

## Self-Evaluation

- **What worked well:** Tracing each status string from where it is written to where it is read exposed three gaps (N vs N+1, acceptance halt, skip) that a section-by-section read would not.
- **What you struggled with:** Without a real run I cannot say how often the observable-check ambiguity bites; it may be rare if most Verifies are commands.
- **Prompt improvement suggestions:** My prompt should list "trace every state string from writer to reader" as a check for execution skills, alongside the gather checks it already implies.

## Round 2 (2026-10-02, delta pass on the rewrite)

**Resolved (6 of 8):** the ambiguity bound (Rule 17, with "asking about it is noise" as the positive side); the Verify-form decider (Rule 18, form read from the text, agent decides observable checks); the per-step write moved to the Status row with "Step N passed" so N+1 is derivable; fix-and-retry has a shape with a second-fail stop; the deferred-test string now matches the template on both sides; the Completion Gate is a list and runs before staging, with the reason given for not recording the hash.

**Partly resolved: halt states without a reader.** Acceptance and Verification halts now have a Pre-Flight branch, skip resets Status, and the dirty-tree check excludes the previous run's bookkeeping. Two strings still have no reader:
- Bare `In Progress`, written at Pre-Flight 7 before any step passes. A session interrupted there matches no branch at Pre-Flight 4. Add: "bare In Progress: resume at step 1."
- `In Progress — Step N skipped`, written at Execute 5. The Pre-Flight branch matches "passed" only. Widen it to "passed or skipped".

**Partly resolved: dirty tree.** The exclusion covers the DIP file and PLANNING.md but not the previous run's partial Artifacts in Scope, which are the most likely uncommitted changes on a resume. Add them to the expected list.

**User-performed step branch (Execute 2):** reads as a clean fork, not a second loop. It sits inside step 2, is bold-marked, and ends with an explicit rejoin sentence; steps 3 to 6 need no change for it. One nit: step 1 already shows "the step title and what it will do", so the user-performed presentation shows the step twice. Let step 1 show the title and step 2's fork add Input and expected Output.

**Three-choice halt menu:** the right length. Each choice is one or two sentences and the skip choice carries the only inference the agent must do (name dependent later steps), which is the most valuable line in the menu. Acceptance step 4 reuses the menu by name without repeating it, which is the correct pattern. Do not trim it.

**Reintroduced elephant: checkboxes nobody ticks.** The user decided the record goes in the commit body, so the skill says "nothing is ticked" and the template comment says the same. But the comment is stripped, and the finished DIP still shows `- [ ]` under Required Reading and Safety Checklist. An executor, person or agent, sees a checkbox and a preamble that says to read every item; ticking is the natural act and now contradicts the skill. Convert both lists to plain bullets. This is the one place the rewrite says "do not do X" while the artifact invites X.

**New, minor:**
- Acceptance opens "After the last step passes". A skipped final step is not a pass. Say "after the last step passes or is skipped".
- Template preamble: "When every step and criterion has passed, set Status to Done" cannot be satisfied after a skip, which the skill allows. Say "when the run completes".
- Rule 20 names TodoWrite in parentheses. Harmless as a hint; it is the only platform-specific name in the file.

Nothing remaining blocks use. The skill now reads consistently from the executor's seat in both the agent-performed and user-performed paths.