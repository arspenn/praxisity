# Lead Review: /do skill

**Date:** 2026-10-02
**Mode:** 2 (parallel snapshot), two rounds — prompt-engineer, critic, user-advocate, spot
**Subject:** `.claude/skills/do/SKILL.md`; replaces `.claude/commands/build.md`. No template; consumes the DIP produced by `/detail`.

## Verdict

The execution skill, and the last of the five. It honours the DIP contract from the detail review line for line (critic's words), and the reviews found the defects where an execution skill hides them: state that does not survive across runs, the order of the final writes, and the assumption that the agent does the work. Both rounds closed. Nothing from the old `/build` command was wrongly dropped; Todoist is gone on purpose.

## Decision taken with the user: tracking lives in three places

Raised by the user mid-review: should the agent tick the DIP or use its task list? Decision: the task list for live progress (session-local, free), the DIP's Status row for durable state (one write per step: `In Progress — Step N passed`), and the commit body for the permanent record (acceptance results, deviations, "safety checklist confirmed"). Required Reading and the Safety Checklist are not ticked in the DIP; the template's checkboxes became plain bullets so the finished DIP does not invite an act the skill forbids. Deviations are dated lines under the DIP's Notes, because `/detail` reads them when writing a follow-up.

## Round 1 findings and fixes

| Sev | Finding | Raised by | Fix |
|-----|---------|-----------|-----|
| High | Commit staged the DIP and PLANNING.md before the Completion Gate wrote Done, so every commit shipped "In Progress" and dirtied the tree for the next run | critic | Completion Gate runs before Safety and Commit; no hash in PLANNING.md. |
| High | Resume point lost after a revised halt: `/detail` resets Ready and overwrites Next Steps, so `/do` restarts at step 1 against existing Outputs | critic | `/detail` writes "resume at Step K" or "resume at Acceptance" in the Revision History row; `/do`'s Ready branch reads it. |
| High | In Progress pointer lived only in PLANNING.md Next Steps, which any intervening skill replaces | critic, PE | Status row carries `In Progress — Step N passed`; per-step PLANNING.md write dropped. |
| High | No branch for a step the user performs; for an authoring-tool artifact the skill was undefined | advocate | User-performed step form in Execute step 2: present instruction, Input, expected Output, wait for done, verify as usual. |
| Med | "Do not improvise" stated four ways with no bound; agent would over-ask | PE | Ambiguity is two readings that change the Output; otherwise the agent decides. |
| Med | Observable check had no decider; would collapse into command or judgment | PE | Verify form decided by its text: runnable, names a judge, or anything else. |
| Med | Fix-and-retry had no shape; skip and stop had no consequences | PE, advocate | Agent proposes, user approves, apply in scope, re-run only the Verify, second fail stops; skip names dependent steps; stop says how to resume. |
| Med | Legacy DIPs (001–007) have different headings and no Status row | critic | Refused with a pointer to `/detail DIP-NNN`, whose update flow maps old sections. |
| Med | No-git path skipped the three tool-neutral safety items | critic | Tool-neutral items always; git items only under version control. |
| Med | Acceptance halt never resumed; skip left Halted mid-run; in-run scope widening contradicted the no-edit rule | critic | Acceptance and Verification halt branches in pre-flight; skip and retry clear back to In Progress; scope never widened mid-run. |
| Low | `git diff --staged` useless on binaries; "stash" unexplained; completion gate as prose; contract sentence drifted from the other four copies | advocate, PE, critic | All applied. |

## Round 2

Critic: every round-1 item closed; Status trace found bare `In Progress` and `Step N skipped` with no reader (fixed in pre-flight 4), a revised Acceptance halt with no "resume at" form (both sides fixed), halt-then-commit undefined (Safety and Commit skipped on halt; dirty-tree exemption covers the resumed DIP's own artifacts), two legacy migration paths (now one, in place via `/detail`), and "the step that owns the failing behaviour" assumed a mapping the DIP lacks (user names it). PE: six of eight resolved, two overlapping the critic's; user-performed branch reads as a clean fork; halt menu is the right length and the skip line's dependent-steps sentence is its most valuable; checkboxes converted; "after the last step passes or is skipped".

## Status strings, writer to reader

| String | Written by | Read by |
|--------|-----------|---------|
| Ready | /detail generate | /do pre-flight 4 (checks Revision History for "resume at") |
| In Progress | /do pre-flight 7 | /do pre-flight 4 (interrupted during step 1) |
| In Progress — Step N passed / skipped | /do Execute 4, 5 | /do pre-flight 4 (resume at N+1) |
| Halted — Step N: reason | /do Execute 5, 6; cancel after a step | /do pre-flight 4; /detail update flow |
| Halted — Acceptance: AC-n / Halted — Verification | /do Acceptance | /do pre-flight 4; /detail update flow |
| Done | /do Completion Gate; manual executor | /do pre-flight 4; /detail step 4 (follow-up only) |
| none | legacy DIPs | /do refuses; /detail asks |

## Pattern notes for the plugin test (step 8)

- `/do` is the first skill that runs commands against the repo; it is where `$ARGUMENTS`, `ls` and `cp` in Bash, and the Skill tool for gather get exercised end to end.
- A full-chain live test should end with one `/do` run that halts on purpose, is revised with `/detail`, and resumes.

## Sources

- `do-skill-prompt-engineer-report.md`
- `do-skill-critic-report.md`
- `do-skill-user-advocate-report.md`
- `do-skill-spot-report.md`