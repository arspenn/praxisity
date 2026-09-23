# Lead Review: /charter skill re-evaluation

**Date:** 2026-09-22
**Mode:** 2 (parallel snapshot) — prompt-engineer, critic, user-advocate, spot
**Subject:** `.claude/skills/charter/SKILL.md` + `templates/charter.template.md` + dependency on `/gather`
**Why:** Skill written April 2026 on Opus / Claude Code ~2.1.32. About to become the pattern for /describe, /design, /plan, /do and be packaged as a plugin.

## Verdict

The output document is good; the skill that produces it has structural defects that would be cloned five times. Nothing blocks, but the skill should be revised before it is used as the pattern. Reviewers converged independently on the same top items.

## Consolidated findings

### A. Structural — propagate to every clone

| # | Finding | Raised by | Fix |
|---|---------|-----------|-----|
| A1 | Both cancel paths (pre-flight step 3, Review and Confirm) exit before the Completion Gate; PLANNING.md stays "in progress" with no reset | PE, critic | Add a cancel branch that resets PLANNING.md status |
| A2 | PLANNING.md contract undefined — "create if missing" has no schema, skills write fields the real file lacks; CLAUDE.md is auto-edited and assumed to exist | critic, advocate | Define one minimal PLANNING.md block format shared by all skills; CLAUDE.md edits become offer-only and skip if absent |
| A3 | SKILL.md sections 1–9 restate the template's HTML comments and have already drifted (Constraints: 6 categories in comment, 5 in fields and skill; Stakeholders similar) | PE, critic | Template owns per-section guidance; SKILL.md keeps an ordered list plus charter-specific exceptions (Mission required, domain detection, Glossary derived last) |
| A4 | `${CLAUDE_SKILL_DIR}` repeated three times; unverified inside plugins | PE, critic, lead | Declare template path once at top of Generate; plugin swap becomes one edit |
| A5 | `/gather` is referenced ("see /gather") not loaded; relies on untested auto-invocation | PE, spot | Explicit "load the gather skill" pre-flight step |
| A6 | Draft-for-approval ownership: charter drafts unconditionally in three places, gather gates it on the guided/draft-first preference | critic | Gather owns the rule; charter says only "existing content is always shown as a draft" |
| A7 | Dead text: Post-Save "task management service" (Todoist is out of scope); Agent Consultation section is unreachable, uses pseudo-syntax, and agent names will be namespaced in a plugin | all four | Delete both; fold "get a review" into next steps |
| A8 | Load-bearing rules (sequential pre-flight, copy-then-edit, gate) stated as bare imperatives; "byte-for-byte unchanged" verify has no mechanism | PE | Attach one-line reasons; replace verify with a git-diff command or a read-only statement |

### B. Charter-specific

| # | Finding | Raised by | Fix |
|---|---------|-----------|-----|
| B1 | "Domain section removal" contradicts "never remove a section"; live CHARTER.md dropped the H3 heading (not a permitted op); hard-coded 3 domains + Other gives the framework's own author a blank box | critic, advocate, spot, lead | Generalize now: one Domain Context section with three transferable prompts (frameworks/theories that guide the work, tools/methods that deliver it, how quality is judged in this field). Domain-specific examples live in the HTML comment. Removal operation deleted. Adding ISD later costs one comment paragraph. |
| B2 | Update flow: `cp` overwrites CHARTER.md before the "preserve established date" step reads it; "skip" is undefined in update mode (gather says move on, generate says write N/A) — approving by saying "skip" can erase content; the (r)eview path replays all ~25 prompts to change three sections | critic, advocate | Read existing charter fully before cp; define skip-in-update as "keep existing"; on review ask "what changed since [date]?" and walk only those sections plus any TBDs |
| B3 | ~27 exchanges for a first run. Stakeholders (4), Success Criteria (3), Constraints (5) yield ~10 lines of content. Day-one students cannot know measurable outcomes | advocate | Collapse those three to one prompt each with sub-categories as a checklist (Mission, Principles, Scope stay one-at-a-time); add "TBD — revisit at [milestone]" as a state distinct from N/A; invite the user to share a syllabus/brief/rubric before gathering so draft-first has a source |
| B4 | Only one "why this matters" sentence in the flow (scope creep). Brief mode suppresses purpose along with examples | advocate | One purpose sentence per section that survives brief mode |
| B5 | Success message: points to `/describe` (does not exist yet), "share with stakeholders" (solo user), never states the important effect (CLAUDE.md now routes Claude to the charter every session) | advocate | Rewrite next steps for the actual user |
| B6 | Template: five numbered principle slots (count anchoring); "dual-use design principle" cited in both files, defined in neither | PE | Two slots + "add as needed"; define or drop the term |

## Tensions

- **B3 vs the gather protocol.** The gather skill's "prompt each sub-category individually" rule came from batching bugs in the March test (BUG-012/018/034). The advocate's proposal to collapse Stakeholders/Success/Constraints into one prompt each is a deliberate relaxation of that rule. The bugs were about batching *sections*; sub-category batching within one section with a checklist was not the failure mode. Recommend: allow it, and say so in gather.
- **Generalizing domains now vs deferring ISD work.** The user asked to defer ISD-specific changes unless critical. B1 is not ISD-specific: the contradiction exists today and the fix removes a permitted-operation bug. Generalizing is cheaper than keeping three domains and adding a fourth. Recommend: do it now.

## Preserved as the pattern

Sequential pre-flight → gather → copy-then-edit with a closed operations list → post-save → completion gate → success message. Explicit update flow with new-vs-update date branching. Agent-derived glossary as last gather step. Good/bad examples in template comments. Delegation to gather.

## Round 2 (same day)

All three files rewritten; all four reviewers re-read fresh. Every round-1 high finding closed. Decisions taken with the user: generalize Domain Context now; collapse Stakeholders, Success Criteria, Constraints to checklist prompts; add the TBD marker and the source-material invitation; source material conventionally lives in `.plans/references/` with an ask as fallback.

Round-2 items fixed: unanswered checklist categories get N/A at generate time; CLAUDE.md link is an `@CHARTER.md` import (offer-only) and the success-message claim is conditional on acceptance; re-read the old charter immediately before the cp; update mode walks any section whose template shape changed and always re-derives the Glossary; start-fresh resets the established date; template title carries the project name; gather names its four pacing terms with an example checklist prompt and updates preferences mid-session; Domain Context shows field examples even in brief mode; Principles offers a first draft from the Mission on a stall; Post-Save offers are one message.

Accepted knowingly: the PLANNING.md contract is inline in each workflow skill (one line, five copies) because the plugin cannot rely on skill-forge being installed.

Left for work-plan step 8 (plugin test): skill-from-skill invocation via the Skill tool; `${CLAUDE_SKILL_DIR}` inside a plugin; `@CHARTER.md` import actually loading.

Result: charter SKILL.md 133 → 96 lines; template 287 → 204; gather 85 → 88. First-run exchange count estimated ~27 → ~17 (user-advocate). Reviewers judge the pacing table copyable as the pattern for /describe, /design, /plan.

## Sources

- `charter-skill-prompt-engineer-report.md`
- `charter-skill-critic-report.md`
- `charter-skill-user-advocate-report.md`
- `charter-skill-spot-report.md`
