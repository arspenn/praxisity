## User Advocate Review

**Artifact:** `/charter` skill (SKILL.md, charter.template.md, /gather dependency, live CHARTER.md)
**Date:** 2026-09-22
**Dispatch Mode:** Mode 2 (parallel perspectives, dispatched as teammates alongside critic and prompt-engineer)

## Instructions Received

Walk the first-run and update flows as a doctoral student in instructional design starting a course project; judge whether the ~25 prompts earn their place, whether the skill teaches or just collects, what "Other" domain costs, and whether next steps fit coursework.

## First-Run Walkthrough (doctoral student, week 1, no CHARTER.md)

I type `/charter`. Before anything is explained, a PLANNING.md appears in my repo. If I have no CLAUDE.md (likely in a fresh course folder), step 4 has no instruction for that case, so what happens next depends on the agent's mood. Then I get the intro sentence, which tells me what a charter *is* but not why I'd want one for a 15-week course or how long this will take. Then two calibration questions about gathering style, which I can't answer meaningfully because I've never gathered anything. I pick draft-first because it sounds faster. It isn't: there's nothing to draft from, so I get guided mode anyway.

Mission goes fine. Principles asks me one at a time for "core values that guide decisions." In brief mode I see no examples. I have a syllabus, not values. I write two things that sound like values and say done. Scope in/out is the first moment I learn something: the out-of-scope prompt tells me *why* (scope creep), and I realize I'd been planning to build a full course when the assignment is one module.

Then it turns into a form. Four stakeholder prompts for two lines of content (learners; me; my instructor). Three success-criteria prompts asking for "measurable outcomes" I can't know in week 1, because the learners of my module don't exist yet. Five constraint prompts, of which I answer one (due dates) and skip four, though "regulatory" should have nudged me toward accessibility, which is a real obligation in my field. Domain Context asks my project type; none of Software, Public Health, or Research is mine. I pick Other and get two blank boxes. Maintenance asks who approves amendments to a document only I will read. Glossary is drafted for me and is genuinely nice.

Then a full structured summary of everything I just approved, roughly the entire charter, which is exactly the dense output I struggle with. I say yes. Success message tells me to share with stakeholders (there are none) and run `/describe`, which does not exist in the skills directory. About 27 exchanges in, I have a good document and a mild sense that the framework was built for someone else.

## Findings

### Friction — Day-one draft-first has nothing to draft from
**What a new user encounters:** Draft-first preference selected, but no documents loaded, so every section is a cold prompt.
**Why it's a problem:** The user's stated preference is defeated silently. A course project always has source material (syllabus, assignment brief, rubric).
**Suggested improvement:** In the Introduction, before gathering: "If you have a syllabus, assignment brief, rubric, or proposal, share it now and I'll draft each section from it for your approval." This is the single biggest lever for the first-run experience and is already permitted by /gather's loaded-documents rule.

### Friction — Sub-category prompts are form-filling, not pedagogy
**What a new user encounters:** 12 separate prompts across Stakeholders (4), Success Criteria (3), Constraints (5) for content that fits in ten lines.
**Why it's a problem:** The one-at-a-time pacing earns its keep on Mission, Principles, and Scope, where each answer changes how the user thinks. It does not on "Secondary stakeholders" or "Other constraints." The user experiences it as a form with one field per page.
**Suggested improvement:** Keep sub-categories as *template formatting* but make each of these three a single gathering section: show the categories as a checklist, ask for whatever applies, draft from loaded docs where possible. /gather's rule is honored because the skill, not /gather, defines what counts as a section. Prompt count drops from ~27 to ~12 with no loss of learning.

### Friction — Asks for things the user cannot know in week 1, with no legitimate "not yet" answer
**What a new user encounters:** "Primary success metrics (measurable outcomes)", "Quality indicators", "Amendment process." Skip produces "N/A — reason", which reads as *permanently* not applicable.
**Why it's a problem:** The honest state is "unknown until week 4," and the skill has no vocabulary for it. Users either fabricate metrics or mark N/A and never revisit.
**Suggested improvement:** Add a second skip state: "TBD — revisit at [milestone]." Say in the intro that this is expected on a first pass. The update flow then has a target list, and the user learns that deferring a decision explicitly is a skill, not a failure.

### Friction — Update flow replays all ~25 prompts to change three sections
**What a new user encounters:** Two months in, the course shifted. (r)eview walks every section and sub-category as a draft for re-approval.
**Why it's a problem:** Approving 20 unchanged drafts to reach the 3 that changed is exactly the "gathering feels slow" complaint. It also misses the learning moment: nothing asks what changed or what was learned.
**Suggested improvement:** On (r), first ask "What has changed since [last reviewed date]?" and show a one-line index of sections with any TBD markers flagged. Walk only the sections the user names plus the TBDs, then offer "quick pass on the rest?" Preserve the full walk as an option.

### Friction — "Other" domain hands the framework's own target user a blank box
**What a new user encounters:** Three richly scaffolded domains that aren't theirs, then "Domain name and key context."
**Why it's a problem:** The cost is two-fold. They get none of the guiding questions the other domains get (which frameworks, which methods, how quality is judged), and they get the message that this tool was designed for someone else. For instructional design the missing scaffold is real: ID model, learning theory, learner analysis, delivery modality, evaluation model.
**Suggested improvement:** Replace the fixed domain list with three domain-agnostic questions that all four current variants already reduce to: (1) What frameworks, models, or theories guide the work? (2) What tools, platforms, or methods deliver it? (3) How is quality judged in this field? Let the agent tailor examples to the stated project type. This transfers across every project the student will ever do, which is the point.

### Friction — The skill collects but teaches only once
**What a new user encounters:** One "why" sentence in the whole flow (scope creep). The template's genuinely good teaching comments ("If we face a tough choice, what values guide us?") are stripped from the output and, in brief mode, never shown.
**Why it's a problem:** A user who completes this learns what a charter contains, not why each part exists. That builds compliance, not capability.
**Suggested improvement:** Give each of the nine sections one "why this matters" sentence shown regardless of prompt-detail preference. Brief mode should suppress *examples*, not *purpose*. Move the template's best comment lines into the skill so they survive.

### Friction — Success message points to a dead end and the wrong audience
**What a new user encounters:** "Share with stakeholders" (solo student), "Create your first specification with /describe" (skill does not exist yet), "Reference when making project decisions" (how?).
**Why it's a problem:** The first thing the user tries after success fails. And nobody has told them the one thing that makes the charter matter to AI collaboration: CLAUDE.md now points at it, so Claude reads it every session.
**Suggested improvement:** Say explicitly: "Claude will read CHARTER.md at the start of each session via CLAUDE.md; when it makes a judgment call, this is what it consults." Rewrite next steps for a solo user: (1) skim it once as a reader, not the author; (2) share with your instructor or advisor if useful; (3) next skill, only if installed; (4) revisit at each TBD milestone. Gate the /describe line on the skill actually being available.

### Minor — Silent file creation and missing-CLAUDE.md case
**What a new user encounters:** PLANNING.md appears unannounced; step 4 and Post-Save assume CLAUDE.md exists; step 3 of Post-Save assumes git.
**Suggested improvement:** One intro line: "I'll keep PLANNING.md as a session log." Add "create if missing" to CLAUDE.md handling, and "if this is a git repo" to the commit step.

### Minor — Calibration questions come before the user can answer them
**What a new user encounters:** Asked to choose gathering style before experiencing gathering; re-asked in every new course project.
**Suggested improvement:** Default to draft-first with brief prompts, say so, and let the user change it mid-flow ("say 'more detail' anytime"). Consider a user-level default with project override.

## What Works Well for Users

- **Mission and Scope pacing is right.** One-at-a-time here genuinely changes how the user thinks about the project. Keep it.
- **The out-of-scope prompt is the model.** One sentence of "why" attached to a prompt. Every section should look like this.
- **Glossary is drafted, not prompted.** The agent does the work, the user approves. This is the correct division of labor and it quietly teaches the dual-use idea.
- **The (r)eview path exists and presents drafts.** The concept is right; only the granularity is wrong.
- **Constraints as agent rules are humane.** "Accept brief answers," "all sections except Mission can be skipped." Just tell the *user* those rules too.

## Ranked Top 5

1. **Invite source documents in the intro** so draft-first actually drafts on day one.
2. **Collapse Stakeholders, Success Criteria, and Constraints to one prompt each.** ~27 exchanges become ~12; pedagogy is preserved where it lives.
3. **Add a "TBD — revisit at" state** distinct from N/A, and make the update flow target it.
4. **Replace the domain list with three transferable questions** so an instructional design student gets scaffolding instead of a blank box.
5. **Fix the success message:** explain that CLAUDE.md now points Claude at the charter, and don't recommend a skill that isn't installed.

## Self-Evaluation

- **What worked well:** Walking the flow with a concrete artifact in hand (a syllabus) exposed the draft-first gap immediately; counting prompts against lines of resulting content made the form-filling finding concrete.
- **What you struggled with:** I cannot observe the live run, so the CLAUDE.md-missing and no-git cases are inferences from the text, not observed failures. I also can't tell whether calibration re-asking per project is annoying or reassuring without a second project.
- **Prompt improvement suggestions:** My prompt should tell me to check whether every skill or command a success message references actually exists in the repo. It should also ask me to count prompts against resulting content lines as a standard overhead check.

---

## Round 2 (2026-09-22, after rewrite of SKILL.md, template, and /gather)

**Exchange count, first run, same student (no CHARTER.md, no CLAUDE.md, no memory, has a syllabus):**

| Stage | Exchanges |
|-------|-----------|
| Intro + defaults notice + source-material invite (one message, user shares syllabus) | 1 |
| Mission with project name | 1 |
| Principles, one at a time (assume 3 + "done") | ~4 |
| Scope In, Scope Out | 2 |
| Stakeholders, Success Criteria, Constraints, Domain, Maintenance (one each) | 5 |
| Glossary draft | 1 |
| Review and confirm (compact outline) | 1 |
| Post-save offers: CLAUDE.md, git commit | 2 |
| **Total** | **~17** (was ~27) |

With a syllabus loaded, most of the middle five are approvals of drafts rather than cold prompts. The pedagogical pacing survives exactly where I asked for it: Mission, Principles, Scope.

**Resolved (8 of 9):** source-document invitation; sub-category collapse with /gather now stating the section-vs-checklist rule and its reason; TBD marker, surfaced to the user, counted in the success message, and carried into PLANNING.md next steps; update flow asks "what changed?" and walks only named sections plus TBDs; "Other" replaced by three transferable questions with instructional design examples inline; a purpose sentence per section that survives brief mode; success message explains the CLAUDE.md link, fits a solo user, and gates `/describe` on it being installed; PLANNING.md announced, CLAUDE.md create-if-missing offered, git conditional and consent-gated. Calibration questions replaced by stated defaults with change-anytime.

**Not resolved, or new:**

- **Domain scaffolding exists only in detailed mode.** The ADDIE, SAM, Kirkpatrick, and LMS hints live in a template comment, and /gather says brief suppresses examples. The charter's pacing row says "tailor examples to the field," which reads as an exception but does not say so. For the default brief-mode student, Domain Context risks being three well-labelled blanks plus a fourth, "Key Context," that the skill's "three questions" never mentions. Fix: say in the Domain row "show the field's examples from the template comment regardless of prompt-detail," and either drop Key Context or fold it into the prompt.
- **Principles is now the cold-start stall.** A syllabus has no values to draft from, and brief mode hides the one instructional design example. The student can say "more detail," but a first-timer does not know they need to. Fix: on the first Principles prompt, offer to draft one starting principle from the Mission, or show two field examples once.
- **The intro can become a wall.** PLANNING.md notice, what a charter is, one-at-a-time, skip and TBD, preference defaults, source-material invite, and a file list from `.plans/references/` (a directory the student has never heard of). Every sentence is load-bearing, but the agent has no length cap. Fix: cap at roughly five lines, end on the single question ("any source material?"), and leave the markers explanation for the first prompt where skipping matters.
- **Three consecutive yes/no gates at the tail.** Confirm, then CLAUDE.md, then git. Each is a real permission, but a one-message offer with two items would feel less like a checkout flow.

**Does anything read as a form again?** No. The pacing table is agent-facing and the user never sees it. A single checklist prompt for five constraint categories is one page, not five, and the purpose sentence in front of it keeps it a decision rather than a field.

**Round 2 verdict:** the first run now reads as a guided conversation with a document at the end rather than a form with a conversation wrapped around it. The four residuals are small and mostly one-line fixes. Ready to serve as the pattern for the other four skills, with the Domain-examples ambiguity fixed first since it is the one that hits the target user directly.
