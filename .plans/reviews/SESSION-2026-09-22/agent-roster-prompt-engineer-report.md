## Prompt Engineer Review

**Artifact:** `.claude/skills/agent-authoring/SKILL.md`, `references/roster.md`, and the nine files in `templates/roster/`
**Date:** 2026-10-08 · **Dispatch Mode:** Mode 2

## Instructions Received
Evaluate the rebuilt skill and roster as prompts: do the four new Checklist sections read as checks or as findings the agent will re-report; do any items plant failure modes; are the checklists holdable alongside a task; is "cp, nothing is edited" consistent with copy-then-edit; does the Author flow's Write need explaining; signal-to-noise on the skill.

## Findings

### HIGH — Findings stated as facts will be re-reported (user-advocate, consistency-reviewer Checklists)
A checklist item written as a property of the world ("brief modes suppress examples exactly where first-timers need them", "non-functional requirements assigned to 'all' fall through every DIP's Must Satisfy table", "use-case postconditions omit outputs the design later requires", "risk sections re-open decisions a component already closed") is read by a fresh session as a known defect of this project, not as a check. The agent reports it again whether or not it is present. The gather skill already fixed the brief-mode case ("brief suppresses examples, not purpose"), so that item now primes a false finding. Critic's and prompt-engineer's lists mostly escape this because they are phrased as conditionals or principles.
**Rewrite each as a conditional check with an observable test.** User-advocate: "Check whether the default mode shows at least one example per section; note which sections a brief mode leaves bare." Consistency-reviewer items 1 to 6: "For each NFR assigned to 'all', find the DIP whose Must Satisfy table carries it." "For each use case, compare its postconditions against the outputs the design requires of it." "For each risk, confirm it references the decision that governs it rather than restating the choice." Same pattern for the AC-priority, interface-count, and coverage-table items.

### MEDIUM — Items that prescribe a feature rather than check for one (user-advocate Checklist)
"One 'try writing one yourself' invitation keeps the skill" and "next steps must say how the AI will use the artifact from now on" are design positions. Loaded as a checklist, the agent flags their absence in every artifact, including an execution skill where neither fits. **Scope them:** "In a skill that drafts a section the user will later need to write unaided, look for one invitation to try it themselves." Bundled items also need splitting: the second user-advocate bullet carries three separate checks (a "not yet" marker, a source-material invite, a purpose sentence), which is three places to miss.

### MEDIUM — Holding load: checklist plus Reasoning Approach double up (critic, prompt-engineer)
Each list is 12 or 13 one-line items, which is holdable on its own. The load problem is that each sits beside a Reasoning Approach whose generic sub-bullets ("Are directives unambiguous?", "Assumptions that aren't explicitly validated") are the vague form of the same checks. Prompt-engineer now carries about 25 prompts to apply per review; the generic ones dilute the specific ones. **Trim the Reasoning Approach sub-bullets in the four agents that gained a checklist to the ones the checklist does not cover**, and give the skill a bound the author can act on: "when a checklist passes about a dozen items, retire the ones that have not fired in recent reviews to agent memory." Without a bound, "grows from memory" only grows.

### MEDIUM — Author flow reproduces structure from memory, which is the drift the Write rule guards against (SKILL.md Author step 2 and 4)
The one-line reason for Write ("authored, not derived from a placeholder template") is sufficient: there is no template ground truth to drift from, so the copy-then-edit reason does not apply. But step 2 ("note the shape") then has the agent reproduce seven section headings from memory, which is exactly how headings get renamed and the self-evaluation block gets dropped. **Add an observable gate after step 4:** "Confirm the new file's section headings match the roster file you read." Also name the reference file: `spot.md` has none of the sections, so "read one roster file" can land on the wrong shape. Say "read critic.md as the structural reference."

### LOW — "cp, nothing is edited" is consistent but needs its contrast stated (SKILL.md Install step 3)
The copy-then-edit rule's reason is that Write regenerates and drifts; a bare `cp` is strictly safer, so there is no contradiction. The risk is association: the directory is named `templates/`, and every other template in the framework is copied, edited, and comment-stripped. An agent with a workflow skill's Generate rules in context may go looking for comments to strip. **Rewrite:** "These are finished files, not placeholder templates: copy with `cp` and leave them unedited; there are no placeholders to fill and no comments to strip."

### LOW — Small clarity items
- Author step 5 says "step 5 of Install applies" then lists two things Install step 5 does not say (dispatch on a real artifact, spot on the report). State the three actions inline.
- "Checklist ... starts empty for a new agent" leaves it unclear whether the author writes an empty heading. Say "omit the heading until the first item exists."
- The rule against naming other agents is scoped to "What you ignore", but its reason (team awareness when dispatched alone) applies to the whole body. Skeptic's Identity opens "Where the Critic asks..." Either scope the rule to the body or accept the contrast in Identity and say so.
- Install step 5 asserts consult-team dispatches the agents; the description allows for consult-team being absent. Add "if installed."
- Project Context: the first sentence is identical across all nine files, which is the right design. Tell the author to copy that sentence verbatim rather than "it is the same paragraph", which invites paraphrase.
- Prompt-engineer item "if the dependency is the fix for an instruction that already failed" depends on Praxisity history a fresh project lacks. Rewrite: "if the dependency carries a protocol the inline text cannot reproduce."

## What's Well-Engineered
"Why the agents are installed, not bundled" earns its three lines: it stops a future author from "fixing" the design by moving agents into the plugin. The `category` note ("Claude Code ignores it") prevents a platform-field misread. The skill states the right rule for checklists ("phrased as checks, not findings"); the roster files are what need to catch up to it. Critic's checklist is the model: nearly every item is a conditional with a test. The closing principles paragraph carries a reason per principle. Roster.md's default review set and its "when to add which agent" line give consult-team's caller a decision rule, not a list.

## Self-Evaluation
Reading each checklist as a fresh session in a different project exposed the re-report items; reading them as their author would not have. Blind spot: I did not check whether the checklist items are still true of the current skills (whether the fixed brief-mode case is the only stale one); consistency-reviewer's seat covers that. Prompt improvement: my own roster file should say that a checklist item is only a check if a reviewer could answer it with "present" or "absent" for the artifact in hand.