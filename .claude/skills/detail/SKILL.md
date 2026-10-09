---
name: detail
description: Turn one design element into a DIP (DIP-NNN), a Detailed Implementation Prompt with exact steps, verification, scope boundaries, and acceptance criteria that whoever executes it, a person or an agent, can follow with no memory of the design conversation.
disable-model-invocation: true
argument-hint: "[DESIGN-NNN COMP-n, or DIP-NNN to revise, or a task description]"
---

# Detail

Turn one design element into a Detailed Implementation Prompt. A DIP is the bridge from a design to work: it names exactly what to build, in what order, how each step is verified, what is in and out of scope, and which acceptance criteria must pass. It is written for whoever executes it, the user in an authoring tool or an agent through `/do`, with no memory of this conversation, and for the person who reviews it before and after.

**Template:** `${CLAUDE_SKILL_DIR}/templates/dip.template.md`. The template is read-only input shared by every future run; all edits target the DIP file in `.plans/prompts/`.

**Argument:** the text the user typed after `/detail`, if any, available as `$ARGUMENTS`. `DIP-NNN` means revise that DIP. `DESIGN-NNN` selects a design, with an element ID after it (`DESIGN-004 COMP-2`) selecting the element directly. A bare number is ambiguous between a DIP, a design, and a spec; ask which. Any other text is a task description for a custom DIP.

## Rules

- Gather only what fills the template. The template defines the DIP's shape; the skill does not add sections.
- Objective, Required Reading, Implementation Steps, Scope Boundaries, and Acceptance Criteria are required. Every other section may be marked `N/A — [reason]` or `TBD — revisit at [milestone]` rather than deleted. A DIP that cannot state its artifacts in scope is not ready to execute; an artifact may be a path or a named location inside a file.
- **One DIP, one element, one sitting.** If the drafted steps run past about ten, or the work touches more than one component, say so and offer to split before continuing.
- **Reference sections cite; step bodies stand alone.** Required Reading, Must Satisfy, Interfaces and Data Touched, and Acceptance Criteria point at the design and spec by ID with a short label, so the executor reads the sources and the DIP stays correct when they change. What the DIP adds to each citation is specific to this work: the approach, the role, the test. Implementation Steps and Scope Boundaries are written in full, in the executor's terms, never as "implement COMP-2 per §3".
- **Every step has a Verify. Every MUST requirement under Must Satisfy has an acceptance criterion with a test.** A Verify is a command, an observable check, or a named human judgment (who looks at what). A step without one, or a MUST without a tested criterion, withholds the save option. The exits: write the test, mark the criterion `TBD — revisit at [milestone]` when the spec's own criterion is TBD, or write "tested in the DIP for COMP-n" when it can only be verified once a sibling element exists; that deferral is carried into PLANNING.md's Next Steps and picked up when the sibling is detailed.
- A DIP's number is assigned once and never reused. Steps are numbered sequentially within the DIP and may be renumbered freely while the DIP is Ready or Halted, because nothing outside the DIP cites a step. `/do` sets Status to In Progress, Done, or Halted. A Done or In Progress DIP is not revised; a follow-up DIP is written instead.

<!-- Maintainer note: this skill converses with the user throughout, so it must not be given `context: fork` in frontmatter. -->

**PLANNING.md contract.** PLANNING.md has an `## Active Context` block with **Last Command**, **Status**, and **Date**, and a `## Next Steps` list. Skills set Status to `in progress`, `complete`, or `cancelled`.

## Pre-Flight

Run these steps in order and finish each before starting the next. Step 2 lands first so that an interrupted run still leaves PLANNING.md accurate, and steps 4 and 5 decide what the rest of the run is about.

1. Read PLANNING.md. If it is missing, create it per the contract above and tell the user you keep it as a session log.
2. Update PLANNING.md: Last Command `/detail`, Status `in progress`, Date today.
3. Invoke the `gather` skill with the Skill tool so its protocol is in context before the first section is presented.
4. Revise, if asked. If the argument is `DIP-NNN` or the user asks to revise a DIP, list `.plans/prompts/` with `ls` in Bash and read that DIP in full. Read its Status: Ready or Halted means revise (read the design and spec it links, then continue at step 6; the update flow runs in Gather, and a Halted DIP returns to Ready on save). In Progress or Done means the DIP has been executed; offer a follow-up DIP that references it, or cancel. A DIP with no Status field predates this skill; ask whether it has been executed and proceed accordingly. If not revising, continue to step 5. To cancel here, set PLANNING.md Status to `cancelled` and stop.
5. Select the design and element for a new DIP:
   a. List `.plans/designs/` with `ls` in Bash. If it is empty or missing, say a DIP needs a design element to detail, set PLANNING.md Status to `cancelled`, and stop with the suggestion to run `/design` first.
   b. Choose the design: from the argument if it names one; else offer the design named in PLANNING.md's Next Steps as the default; else ask once. Read the design in full, then read the spec it references in full.
   c. Choose the element: from the argument if given; else show the design's components, interfaces, and data entities with their Satisfies lists, mark any that already has a DIP (search `.plans/prompts/` with Grep for the design ID and then the element ID, since element IDs repeat across designs), add "a custom task" as the last option, and ask once. Then hold the element's block (Purpose, Responsibilities, Dependencies, Satisfies), the requirement text and acceptance criteria for every ID it satisfies, the decisions that constrain it, and both documents' Out of Scope. Also search `.plans/prompts/` for "tested in the DIP for [this element]"; any hit is a deferred criterion this DIP must carry.
   d. Custom DIP (a task description with no element, or the last option above): ask once which design elements it relates to, then which of their requirements this task actually serves; Required Reading, Must Satisfy, and Acceptance Criteria are drawn from those. If it serves none, Must Satisfy and Acceptance Criteria are `N/A — custom task with no requirement` and the MUST gate has nothing to check.
   e. If a Ready or Halted DIP for this element already exists, ask once: revise it (read it, then continue at step 6 with the update flow) or write another.
6. Read CHARTER.md if it exists, for the principles and constraints that bear on this element. If it does not exist, Required Reading's charter block is `N/A — no charter`.
7. Read the template. Its HTML comments define what each section needs and carry the examples. Create `.plans/prompts/` if it is missing. A new DIP's number is the highest existing NNN in `.plans/prompts/` plus one.

## Introduction

Keep this under five sentences. Name the element being detailed, the design and spec it comes from, and how many requirements and acceptance criteria it carries. Say a DIP is an instruction set for whoever executes it, the user or an agent, with no memory of this conversation; that most of it will be drafted from the design for approval; and that the user's judgment matters most on the steps, each step's criterion for done, and the artifact locations. Invite source material as the gather protocol describes: an existing codebase, a storyboard, a file tree, or notes from a prior attempt tell you what the artifacts are.

## Gather

Gather in the order of the table below, which follows the template except that derived sections come last. Follow the gather protocol, including its purpose sentence before each prompt; the template comment for each section says what it needs. Most sections are drafted from the design, so the run is mostly approvals; the exceptions are where the user knows something the design does not. Pacing uses the gather protocol's terms:

| Section | Pacing | DIP-specific notes |
|---------|--------|--------------------|
| Task Title and Objective | One prompt | Title from the element name; Objective from the element's Purpose. Author defaults to `git config user.name`; if unavailable, ask alongside. |
| Required Reading | Drafted by you | Element, its Satisfies requirements, the use cases and acceptance criteria that cite them, the decisions that name it, the charter principles and constraints that apply. Every entry as ID with label and section. A block with nothing in it is one line reading N/A. |
| Implementation Steps | Drafted outline, then one at a time | First draft the ordered list of step titles from the element's Responsibilities and Dependencies and present it for approval; raise a split here if it runs long. Then walk each step. Draft the action and Output from the design; prompt for Input (what the executor starts from, including locations) and Verify, because those are what the user knows and the design does not. Verify is the step's criterion for done. Input and Output may fold into the step text when they would only restate the title. |
| Must Satisfy | Drafted by you | One row per requirement in the element's Satisfies list with its priority, approach from the design's coverage matrix. |
| Interfaces and Data Touched | Drafted by you | From the element's Dependencies and the design's interfaces and data entities that name it. N/A is common. |
| Scope Boundaries | Two prompts: DO and DO NOT, then Artifacts | DO from Responsibilities; DO NOT from the design's and spec's Out of Scope and the neighbouring elements. Then artifacts in and out of scope: paths, or named locations inside a file when several elements share one (an authoring-tool project, a slide deck). Source material or a file listing helps. |
| Acceptance Criteria | Drafted by you | Every spec AC that validates a requirement under Must Satisfy, cited by ID, with the Test this DIP uses for each. Show any MUST without a tested criterion and the three exits; this is the gate. |
| Verification | One prompt | Commands or checks for the whole DIP after the last step. Draft from the step Verifies and the AC tests. |
| Safety Checklist and Commit Instructions | Drafted by you | The three tool-neutral checklist items always; the two git items and the commit block only when the project is under version control, otherwise N/A. Type and scope from the element; artifacts by name from scope. |
| Notes | One prompt | Optional. Pitfalls, environment setup, decisions deferred to execution. |

**Update flow (revising a Ready or Halted DIP).** Ask "What has changed since [last revision date]?" and show a one-line index of sections. If the DIP is Halted, show its Status row first; a step halt points at that step, an Acceptance or Verification halt at the criterion or check that failed and the step that produced it. If the design's or spec's Revision History has rows dated on or after the DIP's last revision, list them and show any Required Reading entry or Must Satisfy row that cites a struck ID. Walk the sections the user's answer touches, every section affected by a source change, and any section whose structure differs between the existing DIP and the current template. Then offer a quick pass over the rest. Steps may be reordered or renumbered. In update mode, "skip" means keep the existing content unchanged.

### Review and Confirm

Show a compact outline: the objective, the step titles with each one's Verify in a few words (naming the judge for human-judged steps), the counts of requirements by priority and acceptance criteria, confirmation that every cited criterion is also under Required Reading, the artifacts in scope, and any step without a Verify or MUST without a tested criterion. Not the full text. Offer **(y)es save**, **(e)dit a section**, or **(c)ancel**. While any step lacks a Verify or any MUST lacks a tested criterion, offer instead: write the test, mark it TBD with a milestone, note the sibling DIP that will test it, or cancel. On cancel, set PLANNING.md Status to `cancelled` and stop.

## Generate the DIP File

Copy the template, then Edit the copy, one section at a time. Edit's guarantee is that everything outside `old_string` survives verbatim; a whole-body replacement leaves nothing outside it and is a Write under another name, which is how templates drift (renamed headers, dropped sections, half-stripped comments, lost verifications).

1. In update mode, re-read the existing DIP now, immediately before the copy overwrites it, and note its Created date, Author, Status, Revision History, and the content of every section the user kept.
2. New DIP: derive the slug from the title (lowercase, hyphens, no punctuation) and copy the template to `.plans/prompts/NNN-[slug].md` with `cp` in Bash, NNN zero-padded to three digits. Update: copy the template over the existing file with `cp` in Bash.
3. Read the fresh copy.
4. Edit one H2 section per call: `old_string` runs from the section's heading to the line before the next heading, never across one. Within a section, apply only these operations:
   - **Placeholder substitution:** replace `[bracketed placeholders]` with gathered content. Tokens: `NNN` is the DIP number; `DDD` not followed by `-slug` is the design number and `DDD-slug` is the design's filename stem; likewise `MMM` and `MMM-slug` for the spec. A follow-up DIP names its predecessor under Follows. Write every reference per the template's reference conventions.
   - **Comment stripping:** remove all `<!-- ... -->` blocks.
   - **Marking:** for a skipped section, replace its placeholder content with `N/A — [reason]` or `TBD — revisit at [milestone]`. The section stays.
   - **Row and block adjustment:** add or remove table rows, checklist lines, and Step blocks to fit the content. Template counts are illustrative.
5. Set metadata. New DIP: Status `Ready`, Created today, Author as gathered, Revision History row `0.1 — Initial draft`. Update: keep Created and Author, set Status `Ready` (a Halted DIP returns to Ready), append a Revision History row with the next minor version and a one-line summary of what changed. Then run the structure check and show its output: `python3 ${CLAUDE_SKILL_DIR}/scripts/check-template-structure.py ${CLAUDE_SKILL_DIR}/templates/dip.template.md .plans/prompts/NNN-[slug].md --repeat` (`--repeat` because Step blocks repeat). Proceed only on `STRUCTURE CHECK OK`; on a failure, fix the named sections with further single-section Edits and run it again. When the DIP was Halted at step N and the earlier steps' Outputs still stand, end the row with "resume at Step K" (K is N, or the first renumbered step whose Output no longer exists); when it was Halted at Acceptance or Verification, end it with "resume at Acceptance". Either lets `/do` offer to pick up there instead of restarting.

## Post-Save

If the project is a git repository, offer to commit the DIP with `dip([slug]): add DIP-NNN for DESIGN-DDD COMP-n` or `dip([slug]): revise DIP-NNN to v[version]`. Do nothing without a yes.

## Completion Gate

Update PLANNING.md: Status `complete`, and Next Steps naming the DIP file, the element it details, and any criterion deferred to a sibling's DIP. This is a hard gate: do not show the success message until PLANNING.md is updated, because the next session reads PLANNING.md before anything else.

If the user cancelled at any earlier point, PLANNING.md must already read `cancelled` for the same reason.

## Success Message

Show all of the following:
- The DIP file path and ID, the element and design it details, and whether it was created or revised.
- Counts: steps, requirements satisfied by priority, acceptance criteria, artifacts in scope.
- Next steps:
  1. Read the DIP once as someone who will execute it with no memory of this conversation; anything you had to remember to understand it belongs in the DIP.
  2. If the `do` skill is installed, execute it with `/do DIP-NNN`. Without `/do`, follow the steps yourself or hand the file to any agent.
  3. Detail the next element with `/detail`; the design's §7.1 Implementation Order says which comes next.