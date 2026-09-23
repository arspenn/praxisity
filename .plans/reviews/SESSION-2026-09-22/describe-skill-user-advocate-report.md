## User Advocate Review

**Artifact:** `/describe` skill (SKILL.md, spec.template.md) with /gather as protocol
**Date:** 2026-09-22
**Dispatch Mode:** Mode 2 (parallel perspectives, dispatched as teammates)

## Instructions Received

Walk `/describe` as the doctoral student two weeks into a course, charter done, assignment brief and rubric in hand, writing the spec for one self-paced training module. Count exchanges, judge the requirements loop, Given/When/Then for a non-software deliverable, template examples, and next steps.

## Walkthrough

I type `/describe "Volunteer intake module"`. PLANNING.md already exists, so nothing new appears. The intro is short and ends with the question I can answer: do I have source material? I give it the brief and the rubric. Problem Statement comes back drafted from the brief and the charter mission, with a sentence on why it matters. Goal and Objectives follow, and the objective format ("By when, who will be able to do what, measured by how") is one I already know from writing learning objectives. That familiarity is also the first confusion: I start listing the module's learning objectives and nothing tells me whether those are project objectives or requirements.

Functional Requirements come one at a time as drafts from the brief. Each shows the requirement, MUST or SHOULD, and a rationale citing the brief. I approve most with one word. The loop is bearable and it is where I learn the most: deciding MUST vs SHOULD is a judgment I have never been asked to make explicitly about a course deliverable. Non-functional is one checklist and the accessibility nudge lands. Use cases arrive as "A learner encountering X will Y and demonstrate Z," which reads naturally, but then the block asks for Preconditions, Flow, Postconditions, and Alternative Flows. I work out that Alternative Flow means the remediation path. Acceptance criteria are drafted for me in Given/When/Then; they map to rubric rows more cleanly than the requirements did, which makes me wonder if I put the rubric in the wrong section. Constraints takes two turns. Dependencies is mostly N/A. Out of Scope is drafted from the charter plus two things I ruled out mid-loop, which feels earned. Open Questions lists three things I hedged on. Compact outline, yes, commit.

**Exchange count:** 24.

| Stage | Exchanges |
|-------|-----------|
| Intro with source-material invite | 1 |
| Problem, Goal, Objectives | 3 |
| Functional Requirements (6 drafts + done) | ~7 |
| Non-Functional checklist | 1 |
| Use Cases (2 + done) | ~3 |
| Acceptance Criteria draft | 1 |
| Constraints (inherited draft, then prompt) | 2 |
| Dependencies, Out of Scope, Open Questions | 3 |
| Related Documents / References draft | 1 |
| Review and confirm, git offer | 2 |

Roughly 13 of the 24 are one-word approvals of drafts when a brief and rubric are loaded. Without source material this would be a hard run, and the requirements loop would be the stall.

## Findings

### Friction — Brief and rubric are treated as one input; they map to different sections
**What a new user encounters:** The intro says "a rubric or brief usually yields the requirements and acceptance criteria almost directly." Nothing says which yields which. Rubric rows are judgment criteria, so drafted from a rubric the requirements come out as qualities ("the module shall demonstrate objective-assessment alignment") rather than functions.
**Why it's a problem:** The student ends up with requirements that restate the rubric and acceptance criteria that restate the requirements, and never learns the distinction the spec is built to teach.
**Suggested improvement:** One sentence in the Functional Requirements row and the AC row: the brief says what the deliverable must do (requirements); the rubric says how it will be judged (acceptance criteria and quality indicators). When drafting an AC from a rubric row, cite the row.

### Friction — Acceptance Criteria is the one section with no domain examples, and the one the student never writes
**What a new user encounters:** Every other section's comment carries a Software / Public health / Research / Instructional design example. AC has only the bare format. It is also drafted entirely by the agent, so the student approves a table they have never tried to write.
**Why it's a problem:** Given/When/Then does work for a module ("Given a learner has finished section 3, when they take the practice quiz, then they receive item-level feedback") but the student has no evidence of that until the draft arrives, and no practice at making a criterion testable.
**Suggested improvement:** Add two examples to the template comment, one instructional design ("Given a screen-reader user, when they navigate the module, then every image and video has a text alternative") and one that visibly bridges a rubric row. When presenting the draft, say in one sentence what makes a criterion pass/fail, and invite the user to write one for a SHOULD requirement. Show the requirement text next to each Validates ID; the user has never seen the IDs before this point.

### Friction — "Objectives" collides with learning objectives
**What a new user encounters:** The objective format is nearly the ABCD learning-objective format the student already uses. They fill 2.2 with the module's learning objectives, then meet Functional Requirements and cannot tell where "the module shall teach X" belongs.
**Suggested improvement:** One clarifying line in the Objectives comment for training deliverables: project objectives describe what the deliverable achieves (completion, pass rate, error reduction); the module's own learning objectives become requirements ("the module shall enable learners to...") or design content.

### Minor — Use case block labels are software vocabulary
**What a new user encounters:** The one-line framing is in the field's words; the block below is Actor, Preconditions, Postconditions, Alternative Flows.
**Suggested improvement:** Extend the instructional design line in the comment: preconditions are prior knowledge and access; alternative flows are remediation and retry paths. The structure fits a learning scenario well once named.

### Minor — Requirements examples say "the solution shall"
**Suggested improvement:** Add one instructional design row to the REQ-F and REQ-N example tables, for example an application-level practice activity (MUST, brief) and WCAG 2.1 AA captioning (MUST, accessibility policy). Examples are strong at the top of the template and thin in the middle, where the student spends most of the run.

### Minor — Charter Reference "principles this spec serves" is never gathered
The metadata field asks which charter principles the spec serves, but no pacing row covers it. Draft it alongside the Problem Statement; it is a good moment to make the student re-read their own principles.

### Minor — Constraints takes two turns for one section
Present the inherited draft and the spec-specific prompt in the same message; the inherited half is an approval, not a decision.

## What Works Well for Users

- **The requirements loop is bearable with a rubric loaded** and is the section that teaches most: priority plus rationale, one at a time, is the right pacing.
- **Out of Scope is required and drafts from what the user ruled out mid-loop.** The student sees their own decisions reflected back.
- **Open Questions drafts from earlier hedging.** Uncertainty becomes a tracked item instead of a vague feeling.
- **The success message's first step** ("every MUST is something you would refuse to ship without") is the best single teaching sentence in either skill. "Submit" would land better than "ship" for coursework.
- **The MUST-without-AC check** before saving is a quiet quality gate the student will come to rely on and then internalize.
- **Next steps fit:** review as reviewer, resolve open questions, optional critic pass, design gated on installation.

## Ranked Top 3

1. **Say which source maps to which section:** brief to requirements, rubric to acceptance criteria.
2. **Give Acceptance Criteria the examples every other section has**, and let the student try writing one.
3. **Disambiguate objectives from learning objectives** in the template comment.

## Self-Evaluation

- **What worked well:** Walking with two specific documents in hand exposed the brief/rubric mapping gap, which reading the skill alone would not have.
- **What you struggled with:** Whether learning objectives belong in Objectives or Requirements is a genuine judgment call; my suggestion is one defensible answer, not the only one.
- **Prompt improvement suggestions:** Ask me to check example coverage per section, not per template, since gaps cluster in the sections users find hardest.
