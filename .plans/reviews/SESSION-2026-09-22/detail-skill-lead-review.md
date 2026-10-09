# Lead Review: /detail skill (and the naming decision)

**Date:** 2026-10-02
**Mode:** 2 (parallel snapshot), two rounds — prompt-engineer, critic, user-advocate, spot. Naming consult beforehand with user-advocate and prompt-engineer.
**Subject:** `.claude/skills/detail/SKILL.md` + `templates/dip.template.md`; replaces `.claude/commands/define.md` and `.praxisity/templates/dip.template.md`.

## Naming

The fourth phase was `/plan` in the April design. Dropped because Claude Code has a built-in plan mode and the word recurs in PLANNING.md. Candidates: define (original), detail, devise. Both consulted agents ranked detail > devise > define. Detail names the behaviour (add resolution to one element) and shares a stem with the artifact; devise points semantically at "plan"; define overlaps describe for an agent choosing a skill and, in instructional design vocabulary, names the up-front scoping stage. Workflow is now Describe → Design → Detail → Do. Rename committed separately (769d499).

## Verdict

The DIP is different in kind from the three documents: a prompt for an executor, not a document for a reviewer. The pattern still cloned, and the reviewers found the problems at the seams: Status lifecycle shared with the unwritten `/do`, the cite rule applied to step bodies, and assumptions that the executor is an agent working on files. Both rounds closed. The user-advocate calls "read it once as someone with no memory of this conversation; anything you had to remember belongs in the DIP" the strongest teaching line in the skill.

## Round 1 findings and fixes

| Sev | Finding | Raised by | Fix |
|-----|---------|-----------|-----|
| High | Status-based revise gate fell through to "new DIP" for every existing DIP: none of the seven legacy DIPs has a Status row | critic | Missing Status is treated as unknown and asked. |
| High | Halted DIPs could not be revised, yet the executor's fix-and-retry assumes step text can change | critic | Ready or Halted may be revised; Halted returns to Ready on save; In Progress or Done gets a follow-up DIP. |
| High | MUST gate had no exits and Must Satisfy showed no priorities | critic | Priority column; exits: write the test, TBD with milestone, or "tested in the DIP for COMP-n". |
| Med | "Cites, does not restate" was global, so steps would read "implement COMP-2 per §3" | PE | Scoped to the four reference sections; step bodies and scope written in full in the executor's terms. |
| Med | Acceptance Criteria restated the spec | PE | User's decision: follow the rule, no exception. AC table cites AC-n and REQ-n; the Test column is what the DIP adds. Both reviewers judged this sound in round 2. |
| Med | Argument grammar made bare `DESIGN-004` or `005` a custom DIP | critic | DESIGN-NNN selects a design; bare number asks which kind. |
| Med | Element grep unqualified (COMP-3 matches three designs) | critic | Grep design ID, then element ID. |
| Med | Step drafts had no stated source; agent would invent paths and Verifies | PE | Action and Output drafted from the design; Input and Verify prompted. |
| Med | "Human judgment" Verify was a draftable escape | PE | Must name who looks at what; judge shown in the Review outline. |
| Med | DIP described as "for an agent in a fresh session"; the target user builds in an authoring tool | advocate | "Whoever executes it, person or agent, with no memory of this conversation." |
| Med | Artifacts as paths cannot scope six components in one authoring file | advocate | An artifact may be a named location inside a file. |
| Med | Safety Checklist git-shaped and fixed | advocate | Three tool-neutral items always; two git items only under version control. |
| Low | `.plans/prompts/` never created; custom DIP shape undefined; DDD/MMM with -slug suffix ambiguous; "the list below" had two lists; N/A checkboxes; pre-flight 5 monolithic; Verify as "criterion for done"; Input/Output may fold into step text; abbreviations undefined for a cold reader | all | All applied. |

## Round 2

PE: 7 of 8 resolved; cite-only AC table sound with the condition that every cited AC is under Required Reading (added to the Review outline); three template contradictions (DO NOT vs bookkeeping exception, who sets Ready, Ready-only wording) fixed. Critic: all eight resolved; deferral wording changed to "tested in the DIP for COMP-n" since the sibling has no number yet, with a grep for deferrals in step 5c and a Next Steps carry; the DIP's Status row is the durable halt record (`Halted — Step N: [reason]`) since `/detail` step 2 overwrites PLANNING.md's Active Context; Follows row added; revise path no longer skips the charter step; custom DIP serves only the requirements the user names.

## What /do needs from a DIP (from the critic's list, for step 5)

- Status row values: Ready (set by /detail), In Progress, Done, `Halted — Step N: [reason]` (set by the executor). Legacy DIPs have no Status row; treat as unknown.
- Resume point after a Halted revision: the DIP returns to Ready; /do starts from step 1 unless the user says otherwise.
- Step block shape: `### Step N: [Action]`, body, then bold Input / Output / Verify labels; Verify always present.
- Three Verify forms, shared with AC Test and Verification: command, observable check, named human judgment.
- Artifacts in Scope is the git safety list; entries may be paths, directories, or "file, named location". The DIP's own Status row and PLANNING.md are exempt from the scope check.
- Decide whether bookkeeping edits are committed with the work (recommend yes, same commit).
- The old build.md says "Files in Scope"; the template says Artifacts.

## Sources

- `detail-skill-prompt-engineer-report.md`
- `detail-skill-critic-report.md`
- `detail-skill-user-advocate-report.md`
- `detail-skill-spot-report.md`