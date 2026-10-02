## User Advocate Review

**Artifact:** `.claude/skills/do/SKILL.md`, run against `.claude/skills/detail/templates/dip.template.md`
**Date:** 2026-10-02
**Dispatch Mode:** Mode 1 (subagent consult)

## Instructions Received

Walk `/do` as the doctoral student in instructional design in two scenarios. One: a DIP whose artifacts are a markdown job aid and a JSON quiz, five steps, two human-judged Verifies. Two: a DIP whose artifacts are scenes in an authoring-tool file the agent cannot open, so the student executes and `/do` is a checklist runner. Count interactions. Judge halt messages, the fix/skip/stop choice, progress signals, the git phase for a non-coder, and the success message.

## Interaction Count

| Scenario | Interactions | Where |
|----------|-------------|-------|
| 1. Agent-editable files | 6 | confirm DIP default, 2 human Verifies, 1 human AC test, look at diff, commit yes |
| 2. Authoring-tool scenes, as written | undefined | halts at step 1; the skill has no branch for a step the agent cannot perform |
| 2. With a user-performed step branch | 10 to 15 | 5 "done" reports, 5 Verify pass/fail (foldable into the done report), 3 AC judgments, 2 commit |

Scenario 1 is light and the interactions are all real decisions. Scenario 2 is the problem.

## User Experience Assessment

### Blocking — The skill assumes the agent performs every step; the student-as-executor case has no path
**What a new user encounters:** Execute step 2 says "Do the step, touching only Artifacts in Scope." Step 1 of their DIP is "Build Scene 3 screens in Storyline." The agent cannot open the file. Nothing in the skill says what happens next. The likeliest outcome is a halt at step 1 with a reason that is not a failure, or the agent asking an open question with no framing.
**Why it's a problem:** This is the one phase where the charter's "not automation" stance is tested directly, and the student finds the skill was built for the agent to do the work. The intro's "this skill is that someone" confirms their suspicion. They stop using `/do` for their actual deliverables.
**Suggested improvement:** Add a third form to the Verify rule's list, and a branch to Execute step 2: a user-performed step. When the artifact is one the agent cannot edit, or the user says they will do the step, the agent presents the step's instruction, Input, and expected Output, waits for "done", then runs the Verify as normal (usually a human judgment: "look at X, pass or fail?"). Everything else in the skill, including halts, Status bookkeeping, and the acceptance table, works unchanged once that branch exists. One sentence in the intro: "When a step is work only you can do, this skill presents it, waits, and verifies."

### Blocking — Halt next step points at `/detail DIP-NNN`, which refuses halted DIPs
**What a new user encounters:** The success message after a halt says "`/detail DIP-NNN` to revise the step." Execute step 6 says the same for a scope halt. The `/detail` pre-flight (step 4) reads a Halted status and says the DIP has been executed, offering only a follow-up DIP or cancel.
**Why it's a problem:** The student follows the instruction they were given and is turned away. That is a dead end at the moment they are already dealing with a failure.
**Suggested improvement:** Either `/do` says "write a follow-up DIP with `/detail`, referencing DIP-NNN," matching what `/detail` actually offers, or `/detail` allows revising a Halted DIP at or after the halted step. The first is the smaller change and matches the "once executed, not revised" rule.

### Friction — "Fix and retry, skip, or stop" is offered without the consequence of each
**What a new user encounters:** The halt reports step, Verify, and result clearly. Then three options. The student does not know when skipping is safe or what stopping leaves behind.
**Why it's a problem:** Skip is dangerous when a later step depends on this Output, and the skill knows the step list but does not say so. Stop is the right choice when they need to think, but it sounds like giving up.
**Suggested improvement:** One line per option at the halt: retry when you know what went wrong; skip only if later steps do not need this step's Output, and name the steps that do; stop to leave the DIP Halted and resume later with `/do DIP-NNN`, nothing is lost.

### Friction — The git diff wait has nothing to show for binary artifacts
**What a new user encounters:** In scenario 2 with the module file under git, "show `git diff --staged` and wait for the user to look" prints "Binary files differ."
**Suggested improvement:** For binary artifacts, show the file list with sizes and say the diff is not readable; the Verifies already passed are the review. In scenario 1 the diff is readable and the wait is genuinely useful.

### Minor — "stashing" in pre-flight step 5 is unexplained
A non-coder sees "commit or stash first." Say "set the changes aside" once. The reason given ("cannot be separated later") is good and should stay.

### Minor — Success message step 3 promises something `/detail` does not do
"That sibling's `/detail` run will pick it up" (deferred criteria): `/detail` gathers acceptance criteria from the element's Must Satisfy, not from sibling DIPs' deferred rows. In practice the criterion usually lands there anyway, but the sentence reads as a mechanism that does not exist. Either add a check in `/detail` or soften to "belongs in the sibling's DIP."

## What Works Well for Users

- **The intro closes the loop with `/detail`'s "read it cold" line.** "`/detail` wrote it so someone with no memory could carry it out; this skill is that someone" tells the student why the DIP was so pedantic. That is the framework teaching its own design.
- **Halt messages are specific.** "Halted — Step N: what the Verify expected and what happened," recorded in the DIP file, means the next session opens with the reason in front of them. Resume checks that earlier Outputs still exist, which is exactly the question a returning student would forget to ask.
- **"Step N of M passed" is progress, not ceremony.** In scenario 1 it is the only thing between the student and silence while commands run. The acceptance table is the first time they see the spec's criteria tested, and pass/fail/deferred in one view is worth the space.
- **The git phase is proportionate for scenario 1.** Markdown and JSON diffs are readable, the secret scan is silent unless it matches, and "never commit without a yes" keeps the student in control. For a non-git project it is skipped with a sentence.
- **Required Reading is read in order and ticked.** The reason given ("skipping them is how an executor builds the wrong thing confidently") is the kind of sentence that survives into the student's own practice.

## Self-Evaluation

- **What worked well:** Running the second scenario literally, step by step, found the missing branch in the first minute; cross-reading `/detail`'s pre-flight found the dead end.
- **What you struggled with:** The scenario 2 count is an estimate of a branch that does not exist yet.
- **Prompt improvement suggestions:** Add "check that every next step named in a success message is accepted by the skill it points at" to the reasoning approach; this is the second skill in this session where it caught a dead end.