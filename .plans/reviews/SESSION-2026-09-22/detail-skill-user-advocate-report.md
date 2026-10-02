## User Advocate Review

**Artifact:** `.claude/skills/detail/SKILL.md` and `templates/dip.template.md`, with `gather/SKILL.md` as protocol
**Date:** 2026-10-02
**Dispatch Mode:** Mode 1 (subagent consult)

## Instructions Received

Walk the skill as a doctoral student in instructional design. Charter, spec, and design exist for a self-paced training module; the design has six components, one interface (assessment results to the LMS), one data entity (completion record). They run `/detail` on the practice scenario component. Count exchanges and judge: intro clarity, artifacts and Verify for authoring-tool work, step pacing, Safety Checklist and Commit noise, success message fit.

## Exchange Count

Typing bare `/detail` with the design named in PLANNING.md Next Steps, five implementation steps, project in git:

| Phase | Exchanges |
|-------|-----------|
| Pre-flight (confirm design default, pick element) | 2 |
| Intro and source-material invitation | 1 |
| Title/Objective, Required Reading | 2 |
| Steps (outline, then 5 steps) | 6 |
| Must Satisfy, Interfaces/Data, Scope (2), AC, Verification, Commit, Notes | 8 |
| Review and Confirm, commit offer | 2 |
| **Total** | **21** |

Bearable for a one-sitting artifact because the intro promises "mostly approvals" and that promise holds: 14 of 21 are yes/edit on a draft. Eight steps pushes it to 24, which is the top of comfortable.

## User Experience Assessment

### Friction — The DIP assumes an agent executes it; for this student, the executor is often themselves
**What a new user encounters:** The intro says a DIP is "an instruction set for an agent in a fresh session." The template header says the same. The student is going to build the practice scenario in Articulate Storyline, which no agent can open. Their first thought is "so what is this for?"
**Why it's a problem:** It contradicts the charter's "not automation" stance at the moment the student most needs to see the framework working for human-executed work. They may conclude the fourth phase is for coders only.
**Suggested improvement:** Intro and template header: "written for whoever executes it in a fresh sitting, you or an agent, with no memory of this conversation." The success message's "any agent can be handed the file" becomes "you, or any agent, can follow it cold." Keep `/do` as the agent path.

### Friction — "Artifacts in scope" expects file paths; a Storyline module is one file holding all six components
**What a new user encounters:** The prompt asks for paths in and out of scope. The student has `module.story`. All six components live inside it. They cannot name the intro lesson as an out-of-scope path, and "Do not change artifacts outside the list below" becomes meaningless.
**Why it's a problem:** The rule "a DIP that cannot state its artifacts in scope is not ready" would withhold save on perfectly scoped work, or the student writes a path that does not protect anything.
**Suggested improvement:** Template comment and gather note: an artifact is a path, or a named location inside a file when the tool does not expose files: "module.story, Scene 3 (Practice Scenario)"; out of scope "module.story, Scenes 1, 2, 4, 5, 6." Add this as the instructional-design example alongside the existing step examples.

### Friction — Safety Checklist is git-shaped, fixed, and absent from the gather table
**What a new user encounters:** After their branching-scenario steps, the DIP ends with "No secrets, keys, or credentials" and "no `git add .`". The checklist is marked "fixed list" in the template and never appears in the skill's gather table or generate rules, so the agent leaves it verbatim even when Commit Instructions is N/A.
**Why it's a problem:** Three of five items read as someone else's document. That is the moment the student decides the framework was built for software and tolerates them rather than trusting them.
**Suggested improvement:** Keep three tool-neutral items always (only in-scope artifacts changed, no unrelated changes, verification passed). Drop the two git items when Commit Instructions is N/A. Add a Safety Checklist row to the gather table ("Drafted by you; git items follow Commit Instructions") so the agent knows it may adjust.

### Minor — Verify is the best teaching moment and the purpose sentence does not name the connection
**What a new user encounters:** Per-step Verify with the instruction "prefer an observable check, name human judgment as such." This student already knows criterion-referenced objectives (condition, behaviour, criterion). Nobody tells them Verify is the criterion.
**Suggested improvement:** The purpose sentence for Steps: "Verify is each step's criterion for done, the same move as the criterion in a learning objective." One sentence, transfers an existing skill into the new context.

### Minor — Input and Output on every step will feel redundant on simple steps
Five steps each showing Input, Output, Verify is fine when drafted. For "Build Scene 3 screens" the Input (storyboard) and Output (screens) restate the title. Allow the agent to fold Input/Output into the step text when they add nothing, keeping Verify always separate.

## What Works Well for Users

- **The intro is five sentences and tells the student where their judgment matters** (steps, verification, artifact paths). That focuses attention exactly where the drafts will be weakest.
- **Verify and the Verification section already accommodate non-code work.** The template's instructional-design step example ("scenario launches from the module menu and the three branches resolve") is the right register, and "describe the manual check and who performs it" makes human judgment legitimate rather than a fallback.
- **The outline-then-one-at-a-time pacing teaches.** Approving the outline is where the student sees the shape of the work and where a split is raised; walking each step is where they learn to define done. Both are transferable habits.
- **Success message step 1 is the strongest line in the skill.** "Read it as someone with no memory of this conversation; anything you had to remember belongs in the DIP" teaches cold-reader writing, which an ID student recognises from facilitator guides and learner instructions. It should survive every revision. Step 3 correctly points at the design's Implementation Order, which exists at §7.1 of the design template.
- **The element picker shows Satisfies lists and existing DIPs**, so the student can see progress across the six components without opening anything.
- **`content` is in the commit type list.** Small, but it signals the framework expected non-code deliverables.

## Self-Evaluation

- **What worked well:** Walking a concrete authoring-tool build exposed the single-file artifact problem and the executor assumption, which a generic read would have missed.
- **What you struggled with:** I estimated exchange count from the table; a live run could differ by a few depending on how the agent batches the design and element questions.
- **Prompt improvement suggestions:** Add "walk one concrete non-software scenario end to end" to the reasoning approach. It is the most productive move I have, and it is currently implicit.
