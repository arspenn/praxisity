---
name: do
description: Execute one DIP (DIP-NNN) step by step with verification after every step, acceptance checks at the end, and git safety before commit. Records progress and halts in the DIP so an interrupted run resumes where it stopped.
disable-model-invocation: true
argument-hint: "[DIP-NNN]"
---

# Do

Execute a Detailed Implementation Prompt. `/detail` wrote the DIP so that someone with no memory of the design conversation could carry it out; this skill is that someone. It follows the DIP as written, verifies each step before the next, checks the acceptance criteria, and commits only what the DIP put in scope. Some steps the agent performs; some the user performs in tools the agent cannot open; the skill runs both the same way. When something fails or is unclear, it stops and asks; it does not improvise.

**Argument:** the text the user typed after `/do`, if any, available as `$ARGUMENTS`: a DIP ID (`DIP-012` or bare `012`).

## Rules

- Do what the DIP says and nothing adjacent. If a step needs a change outside Artifacts in Scope, that is a halt, not a judgment call.
- Ask when a step has two readings that would produce different Outputs. A choice that leaves the Output the same is yours to make; asking about it is noise.
- Verify every step before starting the next. Read the Verify text to decide its form: runnable as written is a **command** (run it, check the result); text naming who judges is a **human judgment** (show the judge what to look at and ask pass or fail); anything else is an **observable check** (perform it, report what you saw, and decide against the Verify text).
- One DIP per run. A DIP is sized for one sitting; chaining them hides where things went wrong.
- The DIP's Status row is the durable record of progress: `In Progress — Step N passed` after each step, `Halted — Step N: [reason]` when stopped, `Done` at the end. Deviations are recorded as dated lines under the DIP's Notes. Live progress is tracked in your task list (TodoWrite in Claude Code); nothing else in the DIP is edited. Edits to the DIP's Status and Notes, to PLANNING.md, and to CHANGELOG.md are bookkeeping, outside the scope check, and are committed with the work.
- Git safety: stage every artifact by name, never `git add .` or `git add -A`; do not stage anything matching secret patterns (`.env`, keys, tokens, credentials) unless the user names the file and says to include it; show the staged changes before committing; never commit without a yes.

<!-- Maintainer note: this skill converses with the user throughout (human-judged verifications, user-performed steps, halts), so it must not be given `context: fork` in frontmatter. -->

**PLANNING.md contract.** PLANNING.md has an `## Active Context` block with **Last Command**, **Status**, and **Date**, and a `## Next Steps` list. Skills set Status to `in progress`, `complete`, or `cancelled`.

## Pre-Flight

Run these steps in order and finish each before starting the next. Step 2 lands first so that an interrupted run still leaves PLANNING.md accurate, and steps 3 and 4 decide whether this is a fresh run or a resume.

1. Read PLANNING.md. If it is missing, create it per the contract above and tell the user you keep it as a session log.
2. Update PLANNING.md: Last Command `/do`, Status `in progress`, Date today.
3. Select the DIP. List `.plans/prompts/` with `ls` in Bash. If it is empty or missing, say there is nothing to execute, set PLANNING.md Status to `cancelled`, and stop with the suggestion to run `/detail` first. If the argument names a DIP, use it; if PLANNING.md's Next Steps names a DIP to execute or resume, offer it as the default; otherwise show the DIPs with their Status rows and ask once. Read the chosen DIP in full.
4. Act on its Status row:
   - **Ready:** proceed from step 1, unless the latest Revision History row says "resume at Step K" or "resume at Acceptance" (a revised halt), in which case offer to resume there after confirming the Outputs of the earlier steps still exist.
   - **In Progress — Step N passed** or **skipped:** a previous session was interrupted. Offer resume at step N+1 (after confirming earlier Outputs exist), restart, or cancel. Bare **In Progress** means it was interrupted during step 1; offer resume at step 1 or cancel.
   - **Halted — Step N:** show the reason and offer: resume at step N, restart from step 1, or cancel. On resume, confirm the Outputs of steps 1 through N−1 still exist; if any is missing, recommend restart.
   - **Halted — Acceptance** or **Halted — Verification:** all steps passed; offer to resume at the Acceptance phase, restart, or cancel.
   - **Done:** say so and stop unless the user explicitly asks to run it again.
   - **No Status row, or headings that do not match the current DIP template** (Files in Scope, Implementation Instructions, Verification Commands): the DIP predates the template. Say this skill executes DIPs in the current shape and point to `/detail DIP-NNN`, whose update flow maps the old sections into the new ones. Set PLANNING.md Status to `cancelled` and stop.
   To cancel at this step, set PLANNING.md Status to `cancelled` and stop; the DIP's Status is unchanged.
5. Check the working tree. If the project is a git repository, run `git status`. On a resume, changes to this DIP's file, to PLANNING.md, to CHANGELOG.md, and to the DIP's own Artifacts in Scope from the previous run are expected and do not count as dirty. If anything else is uncommitted, list it and ask for explicit approval to proceed, or suggest committing or setting it aside with `git stash` first; uncommitted work mixed into this run cannot be separated later. If it is not a git repository, note that the git items of the Safety Checklist and the Commit Instructions are N/A for this run.
6. Read every item under the DIP's Required Reading, in the order listed. These are the sources the steps are written against; skipping them is how an executor builds the wrong thing confidently. Do not skip items you believe you remember from an earlier session. Track them in your task list, not in the DIP.
7. Set the DIP's Status row to `In Progress`. Show the user the Objective and the list of step titles, and say which steps you expect the user to perform (any whose artifacts you cannot open, or any they claim). Create one task-list entry per step, plus one each for acceptance and for safety and commit.

## Execute

For each step, in order, starting at step 1 or the resume point:

1. Mark the step in progress in your task list. Show the user the step title.
2. Perform the step, touching only Artifacts in Scope. **If the user performs the step** (the artifact is one you cannot open, or they say they will do it): add the instruction, the Input, and the expected Output, then wait for them to say it is done. The rest of the loop is identical.
3. Run the step's Verify in whichever form it takes.
4. **Pass:** mark the step complete, tell the user "Step N of M passed", and set the DIP's Status row to `In Progress — Step N passed`.
5. **Fail:** set the Status row to `Halted — Step N: [what the Verify expected and what happened]`. Report the step, the Verify, and the result. Offer three choices, each with its consequence:
   - **Fix and retry.** You may propose a fix; the user approves it; apply it within scope; re-run only this step's Verify. On pass, set Status back to `In Progress — Step N passed` and continue. A second fail stops the run with the halt standing.
   - **Skip.** Name the later steps whose Input depends on this step's Output, so the user sees what a skip puts at risk. On a yes, record a dated line under the DIP's Notes ("Step N skipped: [reason]"), set Status back to `In Progress — Step N skipped`, and continue.
   - **Stop.** Nothing is lost: the halt is recorded in the DIP and `/do DIP-NNN` resumes here, or `/detail DIP-NNN` revises the step.
6. **Blocked by scope:** if completing the step would change something outside Artifacts in Scope, do not make the change. Set Status to `Halted — Step N: requires change to [artifact] outside scope`, report it, and point to `/detail DIP-NNN` to revise the scope. Scope is not widened mid-run.

## Acceptance

After the last step passes or is skipped:

1. For each row of the DIP's Acceptance Criteria, run its Test in whichever form it takes, the same way as a step Verify. Rows whose Test begins "TBD" or "tested in the DIP for" are deferred, not failed.
2. Run the DIP's Verification block, if present. A failure there is `Halted — Verification: [what happened]`.
3. Show a table: criterion, result (pass, fail, deferred).
4. Any fail: set Status to `Halted — Acceptance: AC-n [what happened]`, report, and offer fix-and-retry (ask the user which step owns the failing behaviour, return there, then re-run acceptance), skip with a dated Notes line, or stop.

## Completion Gate

This runs before anything is staged, so the commit carries the final state.

1. Set the DIP's Status row to `Done`, or leave the Halted status if the run ended in a halt.
2. Update PLANNING.md: Status `complete`; Next Steps naming the DIP and its outcome (done, or halted at step N with "resume with `/do DIP-NNN`"), any deviations, any deferred criteria, and the next element to detail per the design's §7.1 Implementation Order. Do not record the commit hash; it does not exist yet.
3. If the run ended Done and CHANGELOG.md exists, append one line under `## [Unreleased]`. The section comes from the DIP's commit type: `feat` → Added, `fix` → Fixed, a removal → Removed, anything else → Changed. The line is one imperative sentence from the Objective, ending with `(DIP-NNN)`. If the file has no Unreleased heading, insert one with the four sections above the newest version first. The changelog then maintains itself as work completes.
4. Cancellations: before any step ran, PLANNING.md reads `cancelled` and the DIP is unchanged. After a step ran, PLANNING.md reads `complete` with the outcome, and the DIP reads `Halted — Step N: cancelled by user`.

This is a hard gate: do not proceed to commit or show the success message until these files are updated, because the next session reads them before anything else.

## Safety and Commit

Skip this phase when the run ended in a halt; the work is not committed, and the success message says so. Otherwise:

1. Walk the DIP's Safety Checklist and confirm each item to the user. The three tool-neutral items apply to every run; the two git items only under version control. Nothing is ticked in the DIP; the confirmation goes in the commit body.
2. If the project is not a git repository, stop here and say the work is not committed because there is no repository.
3. Run `git status` and compare every changed path against Artifacts in Scope. The DIP file, PLANNING.md, and CHANGELOG.md are bookkeeping and pass. Anything else outside scope is shown to the user and needs an explicit yes to be staged.
4. Scan the changed content for secret patterns. A match is shown and is not staged unless the user names it and says to include it.
5. Stage by name: the artifacts in scope that changed, the DIP file, PLANNING.md, and CHANGELOG.md if it was appended.
6. Show the staged changes: `git diff --staged` for text artifacts; for binary artifacts show the file list and say the Verifies already passed are the review. Wait for the user to look.
7. Commit per the DIP's Commit Instructions. In the body: acceptance results, deviations, and "safety checklist confirmed". Never commit without a yes.

## Success Message

Show all of the following:
- The DIP ID and Objective, and the outcome: done, or halted at step N.
- Steps completed out of total; acceptance criteria passed, failed, deferred.
- The commit hash, or "not committed" with the reason (no repository, user declined, halted).
- Any deviations recorded.
- Next steps:
  1. If halted: fix the cause, then `/do DIP-NNN` to resume, or `/detail DIP-NNN` to revise the step or scope.
  2. If done: `/detail` the next element in the design's Implementation Order, or `/do` the next Ready DIP if one exists.
  3. If any criterion was deferred to a sibling's DIP, `/detail` picks it up when that element is detailed.