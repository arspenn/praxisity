## User Advocate Review

**Artifact:** `/design` skill (SKILL.md, design.template.md) with /gather as protocol
**Date:** 2026-09-22
**Dispatch Mode:** Mode 2 (parallel perspectives, dispatched as teammates)

## Instructions Received

Walk `/design` as the doctoral student with a charter, a spec for a self-paced training module (5 MUST, 3 SHOULD, 2 use cases), and a rough storyboard. Count exchanges; judge Architecture scaffolding, component/interface/data translation, the coverage display and gate, the ask-first questions, and next steps.

## Walkthrough

I type `/design SPEC-001`. The intro names my spec and says it holds 5 MUST and 3 SHOULD requirements, which orients me immediately. I hand over the storyboard. Title default, accepted. Summary and Principles arrive drafted; the principles are my charter's principles applied to this module, which is the first time I have seen the charter do work for me. Architecture is three prompts and, because the examples show even in brief mode, each one is in my vocabulary: Context is the learning ecosystem and the LMS, Approach is scenario-based with a rationale and trade-offs, Key Choices is modality, media, authoring tool, assessment instruments. This does not feel like software in disguise. It feels like the design rationale section of an ID project, with a structure I did not have to invent.

Components come one at a time, drafted from my storyboard scenes: orientation, three scenario lessons, practice activity, assessment, job aid. After each one, the skill shows me which MUSTs are still uncovered. I watch REQ-F3 and REQ-F5 disappear from the list as I approve the practice activity and the job aid. That display is the moment the spec and the design become one thing in my head. Interfaces asks first whether components interact; I say the assessment score goes to the instructor and lessons unlock in order, so two interfaces. Data Model asks first whether anything is stored; I say the LMS tracks completion and scores, and I get a Field/Type table for something I do not build. Design Decisions are drafted from choices I made in Architecture, each with alternatives, which is the first time I have seen my own choices framed as decisions I could have made differently.

Then the tail: coverage matrix, implementation order, risks, validation, non-functional approach, out of scope in two turns, open questions, glossary group. Nine approvals after the real thinking is done. Compact outline, all five MUSTs covered, save, commit.

**Exchange count:** about 33 with two interfaces and one data entity; about 27 if both are N/A.

| Stage | Exchanges |
|-------|-----------|
| Intro, Title, Summary, Principles | 4 |
| Architecture (Context, Approach, Key Choices) | 3 |
| Components (6 drafts + done) | ~7 |
| Interfaces (ask, 2, done), Data Model (ask, 1, done) | ~6 |
| Design Decisions (2 + done) | ~3 |
| Coverage, Impl Order, Risks, Validation, NFR, Out of Scope (2), Open Q, Glossary group | 9 |
| Review and confirm, git | 2 |

## Findings

### Friction — Nine approvals after the thinking is done
**What a new user encounters:** After Design Decisions, every remaining section is derived or drafted. The student approves nine messages in a row containing no decisions.
**Why it's a problem:** This is the "gathering feels slow" complaint relocated to the tail, where attention is lowest. The one derived section that matters, coverage, is buried among citations.
**Suggested improvement:** Keep Coverage on its own because it is the gate. Present Implementation Order, Non-Functional Approach, and the Glossary group as one derived-sections approval; /gather lets the skill define the section, and these are citations, not decisions. Fold Title acceptance into the intro. Present the inherited Out of Scope and the spec-specific prompt in one message, as recommended for /describe. That brings the run to about 27.

### Friction — Cross-cutting MUSTs have no element to satisfy them
**What a new user encounters:** The spec has an accessibility MUST (REQ-N1) and a "completable in 90 minutes" MUST. No single component satisfies either. The student either writes REQ-N1 on every component or leaves it uncovered and hits the gate.
**Why it's a problem:** The rule says coverage comes from components, interfaces, or data entities, but the template already has the right home for these: the Non-Functional Approach table. The gate will bite on exactly the requirements a learning deliverable is most likely to have.
**Suggested improvement:** Let a REQ-N MUST be covered by its Non-Functional Approach row, and say so in the Components purpose sentence: "quality requirements that apply to everything are covered in 7.4, not per component." Show that in the coverage matrix as "design-wide (7.4)."

### Friction — The gate withholds save but does not present the exits
**What a new user encounters:** At Review and Confirm with a MUST uncovered, the options shrink to edit or cancel.
**Why it's a problem:** The three legitimate resolutions (add an element, record a deliberate gap with a milestone, revise the spec) are in the Rules, which the user never sees. Withholding a button without naming the way out is where a first-timer gives up.
**Suggested improvement:** When a MUST is uncovered at confirm, list the three exits as the options in that message. The gate then helps: it teaches that a design is not done until every promise has an owner, and it shows how to keep that promise honestly.

### Minor — Data Model asks for a schema of something the LMS owns
**What a new user encounters:** "Does the design manage persistent information?" Yes, completion and scores, in the LMS. Then a Field/Type/Required table.
**Suggested improvement:** In the ask, distinguish "you design the storage" from "a platform stores it." For the latter, the entity block records the platform, what it captures, who can see it, and retention. The retention nudge for data about people is good and should stay; it is a real FERPA moment.

### Minor — The ask-first questions need a recognition cue
Both asks are the right move; they turn two loops the student might not understand into one question each. But "do the components interact?" is abstract. Add the cue: "for example, does a score go anywhere, does one lesson unlock another, does a facilitator step in?" Same for data: "is anything recorded about the learner?"

### Minor — Component block vocabulary
"Responsibilities" and Interface type "API / Event / File / Protocol / Handoff" are software-first. Add "what the learner does or learns in it" as a gloss on Responsibilities, and "Transition" to the interface types. The template's instructional design lines for each section are otherwise good.

### Minor — Coverage display shows only MUSTs
After the last MUST closes, the student may think the SHOULDs are done too. One line, "SHOULDs not yet covered: REQ-F7," once the MUST list is empty, keeps them honest without adding a gate.

## What Works Well for Users

- **Architecture gives real scaffolding.** Context, Approach, Key Choices map onto learning ecosystem, instructional strategy, and media/tool selection with no translation effort. Showing examples even in brief mode was the right call.
- **The closing-coverage display is the best teaching mechanic in the three skills.** The student watches requirements become parts. Traceability stops being a word.
- **Design Decisions drafted from the user's own choices** with alternatives named. That is architecture-decision-record thinking, transferable to any field.
- **Design Principles derived from the charter.** The first time the charter visibly pays off.
- **Next steps fit.** "Every component should be something you could start tomorrow" is in the student's vocabulary; marking the spec Approved teaches lifecycle; `/plan` is gated on installation.
- **Pre-flight refuses to design without a spec** and points to `/describe`. A student cannot skip the step that makes the coverage matrix possible.

## Ranked Top 3

1. **Let non-functional MUSTs be covered design-wide** via the Non-Functional Approach table, or the gate bites on accessibility every time.
2. **Name the three exits at the gate**, not just in the Rules.
3. **Collapse the tail** to about six approvals by grouping derived sections.

## Self-Evaluation

- **What worked well:** Walking with a concrete spec (5 MUST including one non-functional) exposed the cross-cutting coverage gap that reading the rule alone would not.
- **What you struggled with:** The 33 count assumes six components from a storyboard; a sparser storyboard gives fewer, and the tail dominates either way.
- **Prompt improvement suggestions:** Ask me to check any gate for whether the user-facing message names the way through it.
