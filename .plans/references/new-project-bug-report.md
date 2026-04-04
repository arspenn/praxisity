# /new-project Command Bug Report

**Date:** 2026-03-21
**Tested on:** Praxisity framework v0.5.0
**Test project:** Interview Question Set (public-health)

---

## Summary

First live run of `/new-project` revealed several categories of Praxisity framework development artifacts that the command does not clean up, plus a fundamental process flaw in how templates are applied. The command spec needs to be updated to handle these.

---

## Root Cause: BUG-009

### BUG-009: Templates interpreted instead of copied

**Severity:** Critical
**Status:** Open (command-level fix needed)

The command read templates and then wrote entirely new files using the Write tool, treating templates as *guides* rather than *sources*. This is non-deterministic — the agent interprets, summarizes, and restructures content based on its understanding rather than preserving the template verbatim.

**What happened:**
- Templates were read with the Read tool
- New files were created with the Write tool, authored from scratch
- Content was paraphrased, comments were selectively dropped, placeholder counts changed
- This is the root cause of BUG-007 (README.md drift) and BUG-008 (CHARTER.md comment stripping)

**Expected behavior:**
1. Copy template file directly to destination (e.g., `cp .praxisity/templates/charter.template.md CHARTER.md`)
2. Read the fresh copy
3. Use the Edit tool to make only targeted changes: replace placeholders, remove non-applicable domain sections
4. Everything not explicitly edited remains identical to the template

**Why this matters:** The entire point of having templates is determinism. The same inputs should always produce the same output. When an agent rewrites from memory of a template, every run will produce slightly different results — missing comments, reworded sections, different placeholder counts.

**Fix needed in command:** The command spec should explicitly instruct:
- Use `cp` (Bash) to copy templates to their destinations
- Use Read + Edit for placeholder replacement and section removal
- Never use Write to generate template-derived files from scratch
- Exception: if the user explicitly requests using prior project context to inform a new iteration (the re-run use case), the agent may read existing content first and adapt

---

## Bugs Found

### BUG-001: PLANNING.md not reset

**Severity:** High
**Status:** Fixed (artifact only)

PLANNING.md retained framework development state after project initialization:
- Referenced version 0.5.0 (framework version, not new project)
- Contained framework-specific next steps ("end-to-end workflow test", "command-to-skill migration")

**Expected:** PLANNING.md should be reset to a clean template with empty active context.

**Fix needed in command:** Add PLANNING.md reset to Step 1, generating a clean version with the new project name and version.

---

### BUG-002: docs/examples/ not cleared

**Severity:** Medium
**Status:** Fixed (artifact only)

Two framework development research documents were left behind:
- `docs/examples/Claude Code slash commands Opus best practices.md`
- `docs/examples/praxisity-command-evaluation.md`

These are internal Praxisity research artifacts with no value to end-user projects.

**Fix needed in command:** Add `docs/examples/` to the list of directories cleared in Step 1. Preserve the `docs/` directory and its `.gitkeep`.

---

### BUG-003: .plans/references/ not cleared

**Severity:** Medium
**Status:** Fixed (artifact only)

Three framework-specific reference files were left behind:
- `praxisity-reportlab-template-scope.md` (ReportLab scoping for PDF template)
- `IEEE Editorial Style Manual for Authors.docx` (used for `/deliver` PDF styling)
- `IEEE Reference Style Guide for Authors.docx` (used for `/deliver` PDF styling)

The IEEE documents support the `/deliver` command's PDF template but are framework development artifacts. The `/deliver` command's style module (`.praxisity/praxisity_style.py`) already encodes the necessary styles — the source documents are not needed at runtime.

**Fix needed in command:** Add `.plans/references/` contents to the list cleared in Step 1.

---

### BUG-004: \_\_pycache\_\_ committed to initial repo

**Severity:** Low
**Status:** Fixed (artifact only)

`.praxisity/__pycache__/praxisity_style.cpython-312.pyc` was committed in the initial commit despite `.gitignore` containing `__pycache__/`. This happened because `git add -A` was run after `git init`, and the file existed on disk.

**Fix needed in command:** Add a `find . -type d -name __pycache__ -exec rm -rf {} +` step before `git add -A` in Step 7, or use `git rm -r --cached` patterns.

---

### BUG-005: Missing .gitkeep files for directory consistency

**Severity:** Low
**Status:** Fixed (artifact only)

Two directories referenced by the framework lack `.gitkeep` files:
- `.plans/decisions/` — had content removed but no `.gitkeep` preserved
- `.plans/archive/` — referenced by PLANNING.md archival workflow but directory not guaranteed to exist

**Fix needed in command:** Ensure all `.plans/` subdirectories have `.gitkeep` files after clearing. Add `.plans/archive/.gitkeep` creation to Step 1.

---

### BUG-006: Framework files tracked in git

**Severity:** High
**Status:** Fixed (artifact only)

Framework runtime files (`.praxisity/` and `.claude/commands/*.md`) were committed to the project repository. End users should not be tracking framework files — only their own project artifacts. If a user modifies framework files, those changes would show up as noise in their git history.

**What was done:**
- Added `.praxisity/` to `.gitignore`
- Added each Praxisity command file individually to `.gitignore` (not the whole `.claude/commands/` folder, so users can add their own commands)
- Removed `.praxisity/safety/.gitkeep` since the entire directory is now ignored (no `.gitkeep` needed — the folder auto-hides from git)
- Ran `git rm --cached` to untrack already-committed framework files

**Fix needed in command:** Update `.gitignore` generation in Step 7 to include `.praxisity/` and individual command file entries. Do not add `.gitkeep` to `.praxisity/` subdirectories. The `git add -A` in Step 7 will naturally exclude these via `.gitignore`.

**Note:** Commands listed individually so `git status` doesn't hide user-created command files in `.claude/commands/`.

---

### BUG-007: README.md not fully adapted for project type

**Severity:** Medium
**Status:** Open (command-level fix needed)

Two issues with the generated README.md:
1. `[LICENSE_TYPE]` placeholder on line 68 was not replaced — should either be substituted or removed.
2. The "Development Workflow" section is software-centric (references "git safety", "implementation prompts"). For a public-health project, this framing is incongruous. The command should adapt or simplify this section based on project type.

**Fix needed in command:** Add `[LICENSE_TYPE]` to the placeholder replacement list in Step 4. Consider project-type-aware section adaptation for README.md (similar to how CHARTER.md removes non-applicable domain sections).

---

### BUG-008: CHARTER.md guidance comments stripped

**Severity:** Low
**Status:** Open (command-level fix needed)

The command spec says "Copy charter template to CHARTER.md (user will fill via /charter)". However, the generated CHARTER.md had most inline `<!-- -->` guidance comments removed from sections like Scope, Stakeholders, Success Criteria, and Constraints. These comments help users understand how to fill in each section.

The non-applicable domain sections (Software, Research, Other) were correctly removed, and the Public Health section was correctly kept. Dates were correctly populated.

**Fix needed in command:** The spec says to copy the template. Guidance comments should be preserved — only remove domain sections that don't match the project type. Clarify in the command spec that "copy" means preserve comments.

---

---

# /charter Command Bugs

The following bugs were found during post-execution review of the `/charter` command.

---

### BUG-010: Domain context fields not fully gathered (public-health)

**Severity:** Medium (reduced from High — see notes)
**Status:** Open (command-level fix needed)

The spec defines 5 fields for public-health domain context: theoretical framework, target population, intervention model, evidence base, and evaluation approach. Only 2 of 5 were explicitly prompted (theoretical framework and target population). Intervention Model was inferred from context and filled without asking. Evidence Base and Evaluation Approach were silently dropped.

**Mitigating factors:** This project is an academic interview question assignment, not a deployed public health intervention. "Evidence Base" and "Evaluation Approach" map awkwardly to this use case, so the agent likely skipped them as contextually irrelevant rather than forgetting them. Additionally, 3 of 5 fields were filled in the output (1 by inference). The shortcut was reasonable but unauthorized — the agent should still prompt for each field and let the user decide to skip.

**Fix needed in command:** The gather flow for Section 7 should explicitly prompt for each domain-specific field defined in the spec, with the option to skip each one. The command spec could also note that fields may be skipped if the user confirms they don't apply.

---

### BUG-011: Success Criteria quality indicators not gathered

**Severity:** Medium
**Status:** Open (command-level fix needed)

The spec lists three subsections for Success Criteria: primary success metrics, milestones, and quality indicators. Only metrics and milestones were asked about. Quality Indicators were never prompted.

**Fix needed in command:** Add a prompt for Quality Indicators in Section 5 gathering.

---

### BUG-012: Constraints gathered as single combined prompt

**Severity:** Medium
**Status:** Open (command-level fix needed)

The spec says "Prompt by category, allow skipping" with categories: timeline, resources, technical, regulatory. The execution used a single multi-select question, collapsing all categories into one pass. This removes the per-category skip affordance and makes it harder for users to think through each constraint type.

**Fix needed in command:** Prompt for each constraint category individually, allowing the user to skip categories that don't apply.

---

### BUG-013: Charter dates incomplete

**Severity:** Low
**Status:** Open (command-level fix needed)

The template has three date fields: "Charter established", "Last reviewed", and "Next review". Only "Charter established" was set in the output. "Last reviewed" was dropped entirely and "Next review" was dropped. For a short project this is cosmetic, but the spec says to "Add dates (established, last reviewed, next review)" in the Generate step.

**Fix needed in command:** Set all three dates during generation. "Last reviewed" should match "established" on first creation. "Next review" should be derived from the maintenance schedule or left as a placeholder if the user skipped that section.

---

### BUG-014: Success message incomplete

**Severity:** Low
**Status:** Open (command-level fix needed)

The spec requires the success message to suggest four next steps: share with stakeholders, reference when making decisions, create first spec with /spec, update charter as understanding evolves. Only /spec was mentioned. The other three were omitted or replaced with project-specific suggestions (/architect, generate questions).

**Fix needed in command:** Include all four spec-defined suggestions in the success message. Project-specific suggestions can be added but should not replace the spec-defined ones.

---

### BUG-015: Charter maintenance amendment process not prompted

**Severity:** Low
**Status:** Open (command-level fix needed)

The spec lists two items for Section 8: "Review schedule (default: Quarterly)" and "Amendment process (optional)". Only review schedule was asked. The amendment process should be prompted even if optional.

**Fix needed in command:** Add a prompt for amendment process in Section 8, making it clear it's optional.

---

### BUG-016: Pre-flight step ordering

**Severity:** Low
**Status:** Open (command-level fix needed)

The spec defines a specific order for pre-flight: (1) read PLANNING.md, (2) update PLANNING.md with active command, (3) check CHARTER.md, (4) read CLAUDE.md, (5) verify template. The actual execution updated PLANNING.md as step 5 instead of step 2. While the outcome was the same, the ordering matters if a failure occurs mid-flight — PLANNING.md should reflect the active command before other checks.

**Fix needed in command:** This is more of a behavioral note. The command spec ordering is correct; the agent just needs to follow it strictly. Consider adding a note in the spec that step ordering is significant.

---

# /spec Command Bugs

The following bugs were found during post-execution review of the `/spec` command.

---

### BUG-017: Pre-flight step ordering (same pattern as BUG-016)

**Severity:** Low
**Status:** Open (command-level fix needed)

The spec defines pre-flight as: (1) Read PLANNING.md, (2) Update PLANNING.md with /spec active, (3) Check CHARTER.md, (4) Load charter, (5) Verify template, (6) Determine next spec number, (7) Create directory.

Actual execution: Steps 1, 3, 4, 5, and 6 were all run in parallel, then step 2 (PLANNING.md update) and step 7 ran together after. Same pattern as BUG-016 — PLANNING.md should reflect the active command before other checks begin, in case a failure occurs mid-flight.

**Note:** This is the same behavioral pattern as BUG-016. May warrant a general "pre-flight ordering is significant" note across all commands rather than per-command fixes.

---

### BUG-018: Sections gathered in batches, not one at a time

**Severity:** Medium
**Status:** Open (command-level fix needed)

The spec constraint says: "Keep each prompt focused on one section at a time." The gather instructions say: "For each section, briefly explain what's needed, show a domain-relevant example, and prompt for input."

**What happened:**
- Section 1 (Problem Statement) and Section 2 (Goals) were bundled into the first prompt
- Sections 3-10 were all drafted by the agent and presented in a single batch for approval
- No domain-relevant examples were shown for any section
- The user was not prompted individually for requirements, use cases, acceptance criteria, constraints, dependencies, out of scope, open questions, or references

**Why this matters:** The one-at-a-time approach exists so the user can think through each section without being overwhelmed. Batching everything means the user is reviewing the agent's drafts rather than providing their own input. This is a significant departure from the specified flow.

**Mitigating factors:** The charter provided strong context, and the user's argument was to keep things in one spec — so the agent's instinct to move quickly was responsive to implicit time pressure. The user approved the output.

**Fix needed in command:** The "one section at a time" constraint needs stronger emphasis, or the spec needs to acknowledge a "fast mode" where the agent can draft from charter context and present for review. Currently the spec says one thing and the natural execution pressure pushes toward another.

---

### BUG-019: Review and Confirm step skipped

**Severity:** Medium
**Status:** Open (command-level fix needed)

The spec says: "Show summary with counts (requirements, use cases, acceptance criteria). Offer to (y)es save, (e)dit a section, or (c)ancel."

**What happened:** After presenting all sections, the agent asked "Does this all look right? Anything you'd add, change, or remove? If it looks good I'll generate the spec file." — which is close in spirit but doesn't match the specified format. No structured summary with counts was shown, and the y/e/c options weren't offered.

**Fix needed in command:** Either enforce the specific format, or relax the spec to allow natural-language confirmation. The current spec is prescriptive but the agent defaulted to conversational.

---

### BUG-020: Template written from scratch (same root cause as BUG-009)

**Severity:** Medium
**Status:** Open (command-level fix needed)

The Generate step says: "1. Read the spec template, 2. Fill metadata table... 3. Populate each section..." This implies using the template as a structural base. Instead, the agent wrote the file from scratch using the Write tool, same as BUG-009.

The output is structurally faithful to the template, so the impact is low here — but it's the same non-deterministic pattern. The template's exact formatting, section ordering, and any nuances could drift.

**Same fix as BUG-009:** Copy template, then Edit to fill sections.

---

### BUG-021: Success message missing two of four suggested next steps

**Severity:** Low
**Status:** Open (command-level fix needed)

The spec requires four next steps: (1) Review for completeness, (2) Get stakeholder alignment if needed, (3) Create design document with /architect, (4) Section IDs will be referenced by designs and DIPs.

**What happened:** Only steps 1 and 3 were included. "Get stakeholder alignment" and the section ID traceability note were omitted.

**Fix needed in command:** Include all four. Same pattern as BUG-014 from /charter.

---

### BUG-022: Post-save Todoist option not offered

**Severity:** Low
**Status:** Open (command-level fix needed)

The spec says: "Optionally create Todoist task for spec review (if MCP available)." This was not offered. Git commit was offered.

**Fix needed in command:** Prompt for Todoist task creation if MCP is available, or note its absence.

---

### /spec: Things That Worked Well

- Pre-flight checks were thorough (PLANNING.md, CHARTER.md, template, existing specs, directory creation)
- Charter context was effectively used to draft relevant content
- Section IDs were correctly generated (REQ-F1-F5, REQ-N1-N4, UC-1-2, AC-1-6, OBJ-1-4)
- PLANNING.md was updated with completion, active artifacts, and next steps
- The slug was correctly generated from the title
- Out of scope was populated (required by spec)
- HTML comments were removed from the output
- User correction (REQ-F2 rationale notes are process, not deliverable) was incorporated promptly and accurately

---

---

# /architect Command Bugs

The following bugs were found during post-execution review of the `/architect` command.

**Recurring patterns (not re-logged as new bugs):**
- BUG-017 pattern (pre-flight ordering): Steps ran in parallel, PLANNING.md update came after other checks
- BUG-020/BUG-009 pattern (template written from scratch): File not yet generated but will follow same Write-from-scratch pattern
- BUG-018 pattern (batched sections): Some sections batched together, though notably improved over /spec — most sections got individual turns

---

### BUG-023: Metadata not gathered

**Severity:** Low
**Status:** Open (command-level fix needed)

The spec says to gather title (default to "[Spec Title] Design") and author (default to git user.name), then generate slug.

**What happened:** Metadata gathering was skipped entirely. No title was proposed, no author confirmed, no slug generated during the gather phase. These will presumably be filled at generation time, but the user had no opportunity to customize them.

**Fix needed in command:** Prompt for title and author before gathering content, even if defaulting. Same pattern as /spec where metadata was bundled with Section 1.

---

### BUG-024: Spec auto-selected without listing available specs

**Severity:** Low
**Status:** Open (command-level fix needed)

Pre-flight step 4 says: "List available specs and prompt user to select one." The user provided "spec 1" as an argument, and there was only one spec, so the agent correctly used SPEC-001. However, it never listed the available specs or confirmed the selection — it just proceeded.

**Mitigating factors:** The user explicitly specified which spec in the arguments, and there was only one. Listing and re-asking would have been redundant. The behavior note says "may auto-select spec if one is active," which partially covers this.

**Fix needed in command:** When the user provides a spec argument, confirm the selection rather than silently proceeding. When auto-selecting, state which spec was selected. E.g., "Designing for SPEC-001: Healthcare Risk Management Interview Question Set. Correct?"

---

### BUG-025: MUST requirement coverage check not explicitly performed

**Severity:** Medium
**Status:** Open (command-level fix needed)

The spec says for Section 3 (Components): "After all components, check that MUST requirements are covered (warn if gaps)."

**What happened:** After presenting the three components, the agent stated "All MUST requirements covered" but did not show a requirement-by-component matrix or explicitly walk through each MUST requirement to verify coverage. The user has to trust the claim rather than verify it.

**Fix needed in command:** After components are gathered, show a traceability matrix mapping each MUST requirement to its covering component(s). This makes gaps visible and gives the user something concrete to validate.

---

### BUG-026: No domain-relevant examples shown

**Severity:** Low
**Status:** Open (command-level fix needed)

The spec says: "For each section, explain what's needed, show domain-relevant examples, and prompt for input."

**What happened:** No domain-relevant examples were shown for any section. The agent explained what was needed and drafted content, but never showed illustrative examples from the public-health domain to help the user understand what kind of input was expected.

**Same pattern as BUG-018** from /spec. Agents consistently skip the example-showing step, likely because they're drafting content directly rather than prompting for user input.

**Fix needed in command:** Stronger emphasis on showing examples before drafting. Or, acknowledge that when the agent drafts from context, examples serve a different purpose and may be unnecessary.

---

### BUG-027: Introduction step incomplete

**Severity:** Low
**Status:** Open (command-level fix needed)

The spec says: "Show which spec is being designed for, list the requirements to address, and explain that designs define HOW to implement what the spec defined."

**What happened:** The spec being designed for was shown, and requirements were listed in a table. However, the explanation that "designs define HOW to implement what the spec defined" was not stated. The agent jumped from the requirements table to "Let's start with Section 1."

**Fix needed in command:** Include the framing explanation. Same pattern as BUG-014/BUG-021 where prescribed messaging is partially omitted.

---

### /architect: Things That Worked Well

- Correctly identified project type as public-health from CLAUDE.md
- Used the public-health architecture template (logic model + delivery model) rather than software architecture
- Section-by-section gathering was notably better than /spec — most sections got individual turns
- Skippable sections (Interfaces, Data Model) were offered as skippable per spec
- User's design decisions were accepted without over-validating (constraint respected)
- Components correctly traced to requirements
- Conversation was responsive to user tangents (template anchoring discussion, professor instructions, course context) without losing the design thread
- The user's personal interest in pushback to risk management was captured as design context while respecting their desire to stay neutral in the interview

---

---

# /define Command Bugs

The following bugs were found during post-execution review of the `/define` command.

**Recurring patterns (not re-logged as new bugs):**
- BUG-017 pattern (pre-flight ordering): PLANNING.md not updated with /define as active command at start — only updated at end after all DIPs generated
- BUG-009 pattern (template written from scratch): All 3 DIP files written with Write tool from scratch rather than copying template then editing
- BUG-018 pattern (batched sections): Content for all 3 DIPs summarized and presented in a single batch rather than gathered individually
- BUG-019 pattern (informal review): Summaries shown with "These look right?" rather than structured summary with y/e/c options

---

### BUG-028: Task selection step skipped

**Severity:** Low
**Status:** Open (command-level fix needed)

The spec says to prompt user to select what to create a DIP for: design component, interface, data entity, Todoist task, or custom. The user should select from these options.

**What happened:** The user said "create our DIPs" and the agent auto-generated DIPs for all 3 components without presenting the selection menu or confirming which components to create DIPs for.

**Mitigating factors:** User's intent was clear ("lets go ahead and create our DIPs"), and the design only has 3 components with no interfaces or data entities. Presenting a selection menu would have been redundant.

**Fix needed in command:** When user requests all DIPs, confirm the selection list ("I'll create DIPs for COMP-1, COMP-2, and COMP-3. Correct?") rather than silently proceeding. The command spec assumes one DIP per run — it may need a batch mode.

---

### BUG-029: Multiple DIPs generated in single run

**Severity:** Low
**Status:** Open (command-level fix needed)

The behavior notes say: "Each run creates a NEW DIP with incremented number." This implies one DIP per invocation.

**What happened:** Three DIPs were generated in a single run. Content gathering, review, and file generation were all batched across all three.

**Why this matters:** The one-per-run assumption means the command's gather/review/confirm flow is designed for a single element. Batching 3 means the user reviews summaries of all 3 at once rather than thoroughly reviewing each. For this project it worked fine (small, simple components), but for larger designs the batch approach could miss issues.

**Fix needed in command:** Either add explicit batch mode support (with per-DIP confirmation) or enforce one-per-run and let the user invoke multiple times. The current spec is ambiguous.

---

### BUG-030: Git commit not offered post-save

**Severity:** Low
**Status:** Open (command-level fix needed)

The spec says: "Optionally commit to git: `dip([element]): add DIP-[N] for [ELEMENT]`"

**What happened:** After generating all 3 DIPs and updating PLANNING.md, no git commit was offered. The user was not asked if they wanted to commit the new files.

**Same pattern as BUG-022** from /spec where the Todoist option was not offered.

**Fix needed in command:** After saving DIPs, offer git commit. When batching multiple DIPs, offer a single combined commit or per-DIP commits.

---

### BUG-031: Template sections silently removed instead of marked N/A

**Severity:** Low
**Status:** Open (command-level fix needed)

The DIP template includes sections for "Interfaces to Implement/Use" and "Data Entities to Create/Modify." These were removed entirely from the generated DIPs rather than being marked N/A.

**What happened:** Since DESIGN-001 has no interfaces or data entities, these sections were omitted. The omission is correct in substance but not traceable — someone reading the DIP can't tell if interfaces were considered and excluded, or if the section was accidentally dropped.

**Fix needed in command:** When a template section doesn't apply, include it with "N/A — [reason]" rather than removing it. This preserves traceability and makes the omission explicit. E.g., "N/A — DESIGN-001 has no interfaces."

---

### BUG-032: Success message not shown

**Severity:** Low
**Status:** Open (command-level fix needed)

The spec says: "Confirm DIP was generated, summarize what it provides (reading sections, steps, criteria), and suggest next steps: 1. Review the DIP for completeness, 2. Execute by reading and following instructions, 3. Or run /build for guided execution, 4. On completion, all acceptance criteria should pass."

**What happened:** After generating the files, the agent showed a brief summary ("All 3 DIPs generated and PLANNING.md updated") with abbreviated next steps. The full prescribed success message format was not followed — no counts of reading sections, steps, or criteria were shown, and only 3 of 4 next steps were included.

**Same pattern as BUG-021** from /spec and BUG-014 from /charter.

**Fix needed in command:** Include the full success message format. This is a recurring pattern across all commands — agents consistently abbreviate prescribed messaging.

---

### /define: Things That Worked Well

- Pre-flight checks ran correctly (template verified, designs found, prompts directory created, next number determined)
- Auto-generation from design was effective — most DIP content was correctly derived from COMP-1/2/3 responsibilities, linked requirements, and design decisions
- Dependency chain correctly represented (DIP-001 output feeds DIP-002, DIP-002 output feeds DIP-003)
- Scope boundaries were clear and precise — each DIP explicitly says what belongs to other DIPs
- User feedback incorporated immediately (textbook-first reordering of DIP-001 steps)
- Acceptance criteria correctly mapped to spec ACs where applicable (DIP-003 uses AC-1, AC-3, AC-4, AC-5 from SPEC-001)
- Notes sections captured important context (pushback interest, essay implications, student voice, mid-semester status)
- Commit instructions included conventional commit format with requirement traceability

---

### /breakdown Command Notes

The /breakdown command was invoked but could not fully execute because Todoist MCP was unavailable. A markdown task breakdown was generated as a fallback at `deliverables/task-breakdown-DESIGN-001.md`. No bugs are logged for /breakdown since it correctly identified the missing dependency and offered alternatives. The fallback deliverable is not part of the command spec but was a reasonable adaptation.

---

---

# /build Command Bugs (DIP-001 Execution)

The following bugs were found during post-execution review of the `/build` command executing DIP-001.

**Recurring patterns (not re-logged as new bugs):**
- BUG-017 pattern (pre-flight ordering): PLANNING.md not updated with /build as active command at start

---

### BUG-033: Objective and step summary not displayed at start

**Severity:** Low
**Status:** Open (command-level fix needed)

The spec says: "Display objective and step summary to user" before beginning execution.

**What happened:** TodoWrite entries were created (which implicitly shows the steps), but the DIP objective was never explicitly stated to the user. The agent jumped directly into reading the textbook without framing the task.

**Fix needed in command:** Before starting Step 1, show the objective from the DIP and a numbered list of steps. This gives the user a clear picture of what's about to happen.

---

### BUG-034: Steps 2-6 batched into single execution

**Severity:** Medium
**Status:** Open (command-level fix needed)

The /build command spec says: "For each implementation step in the DIP, in order: 1. Mark step as in_progress, 2. Show step title and instructions, 3. Execute, 4. Run verification."

**What happened:** Steps 2-6 in DIP-001 (fill gaps via research on field overview, regulatory environment, risk areas, career pathways, current challenges) were all executed in a single batch of 3 web searches. All 5 steps were marked complete at once without individual verification for each.

**Mitigating factors:** The web research results covered all 5 topics simultaneously, and the textbook had already covered most of the content. Doing 5 separate web searches for content that overlaps heavily would have been inefficient. The DIP itself anticipated this by framing Steps 2-6 as "fill gaps" — if the textbook covered a topic well, that step might be trivially complete.

**Fix needed in command:** The command spec's step-by-step execution model assumes each step is a discrete, independent action. When DIP steps are designed as conditional ("if gaps exist, fill them"), the build command should acknowledge when steps are trivially satisfied and mark them accordingly, rather than silently batching.

---

### BUG-035: Git diff not shown before commit

**Severity:** Medium
**Status:** Open (command-level fix needed)

The spec says: "Show diff to user before committing (git diff --staged)."

**What happened:** The agent ran `git status` and `git diff --stat` (showing file-level changes) but never showed the actual content diff. The user was asked "Does the research brief look right to you?" based on having already read the file — but the prescribed diff step was skipped.

**Mitigating factors:** The user had already reviewed the research brief content directly and approved it. Showing the diff would have been redundant in this case. However, skipping the step means the user doesn't see if anything unexpected was staged.

**Fix needed in command:** Always run `git diff --staged` and show it to the user, even if they've already reviewed the content. It's a safety check, not a content review.

---

### BUG-036: PLANNING.md not updated with DIP-001 completion

**Severity:** Medium
**Status:** Open (command-level fix needed)

The spec says: "Update PLANNING.md: Record DIP completion status, note any deviations or decisions made during execution, suggest next action."

**What happened:** PLANNING.md was never updated after DIP-001 completed. It still shows /define as the last command.

**Fix needed in command:** This is a recurring pattern — PLANNING.md updates are consistently skipped or deferred. The command spec should make this a hard requirement before the success message.

---

### BUG-037: Success message abbreviated

**Severity:** Low
**Status:** Open (command-level fix needed)

The spec says to show: "DIP ID and objective accomplished, steps completed count, acceptance criteria results, commit hash, suggested next action from PLANNING.md."

**What happened:** The agent showed DIP ID, step count, AC pass status, and commit hash — but didn't restate the objective or suggest the next action from PLANNING.md. The format was informal rather than structured.

**Same pattern as BUG-021, BUG-032** — agents consistently abbreviate prescribed success messages.

---

### /build (DIP-001): Things That Worked Well

- DIP argument was correctly parsed from the command args
- Git status check caught the untracked textbook files and correctly warned the user
- Required reading check correctly identified that spec/design/charter were already in context from earlier in the session
- TodoWrite was used throughout to track step progress
- Textbook reading was thorough — read the entire book (~220K words) across multiple chunks
- Gap assessment after textbook review was clear and actionable — identified exactly what remained
- Web research was targeted and efficient — 3 searches filled all remaining gaps
- Research brief correctly cites sources (textbook chapters vs. web sources) as DIP-001 Step 7 required
- Acceptance criteria were explicitly verified before committing
- Git safety was followed — only the research brief was staged, textbook files correctly excluded
- Commit message followed the DIP's prescribed format with REQ traceability

---

---

# Framework-Level Issues

Issues that are not bugs in a specific command but systemic patterns that affect multiple commands and templates.

---

### ISSUE-001: Template example counts anchor agent output

**Severity:** Medium
**Status:** Open (framework-level fix needed for next version)
**Affects:** All templates (spec, design, charter, and any future templates)

Templates include a fixed number of example items (e.g., 3 components in the design template, 2 use cases in the spec template). The agent tends to anchor on this count and produce the same number of items in its output, rather than deriving the correct number from the problem.

**Observed during:** /architect execution for SPEC-001. The design template has 2 component placeholders (COMP-1, COMP-2). The agent produced 3 components, which happened to be correct for this project — but the user flagged the general pattern as a concern. The anchoring effect applies across all templates: requirements tables, use cases, acceptance criteria, interfaces, data entities, etc.

**Why this matters:** The purpose of templates is to provide structure, not to prescribe quantity. When agents match template counts instead of problem counts, the output is either padded (splitting things that should be one item) or truncated (combining things that should be separate). Both reduce quality.

**Fix needed in framework:**
1. Add a behavioral note to the Praxisity CLAUDE.md template (inherited by all projects): "Template anchoring: Templates show example counts for illustration only. Derive the number of items from the problem, not from the template. More or fewer items than shown is expected and correct."
2. Consider also adding this note to individual command specs where templates are populated (spec, architect, charter, define).

---

### ISSUE-002: Typography — straight quotes and apostrophes in PDF output

**Severity:** Medium
**Status:** Open (framework-level design decision needed)
**Affects:** /deliver (all PDF output)

ReportLab renders text as-is and does not perform typographic substitution. Straight ASCII quotes (`"`, `'`) and apostrophes remain straight in the output PDF rather than being converted to typographic (curly) equivalents (`"`, `"`, `'`, `'`). Word processors like Microsoft Word do this automatically via "smart quotes" processing. The result is PDF output that looks noticeably less polished than a word-processed document — especially in prose-heavy deliverables.

**Observed during:** Review of interview-questions-final.pdf. Apostrophes in contractions (What's, can't, don't) and any straight-typed quotation marks render as vertical strokes rather than curved glyphs.

**Why this matters:** This is purely cosmetic but is immediately noticeable to anyone comparing the PDF to a Word-generated document. For professional deliverables, curly quotes are the expected standard. The issue affects every document rendered through /deliver.

**Scope of the problem:** Full typographic processing includes:
- Smart quotes: `"text"` → `"text"`, `'text'` → `'text'`
- Apostrophes in contractions: `it's` → `it's`
- Em dashes: ` -- ` → ` — `
- Ellipses: `...` → `…`

Each substitution is individually straightforward, but implementing all of them correctly (handling edge cases like `'90s`, possessives, nested quotes) is a non-trivial text processing problem.

**Options for the framework:**
1. **Preprocessing pass in /deliver**: Apply a `smartquotes()` function to all text before passing to ReportLab's `Paragraph()`. The Python `smartypants` library (port of the classic Perl SmartyPants) handles all the standard cases. Adds one dependency.
2. **Source discipline**: Require authors to use Unicode typographic characters in source markdown (copy-paste or keyboard shortcuts). No code change needed, but shifts burden to the author and is easy to miss.
3. **Accept as-is for now**: Acknowledge the limitation in /deliver documentation. Revisit when the framework matures.

**Recommended approach:** Option 1 (preprocessing in /deliver) is the cleanest solution. The `smartypants` library is lightweight and well-tested. The substitution should be applied per text node, after markdown parsing but before ReportLab rendering.

---

---

### ISSUE-003: Word (.docx) Title style has a default bottom border

**Severity:** Low
**Status:** Open (relevant to future /deliver Word output support)
**Affects:** Any future Word document generation via python-docx

Word's built-in `Title` paragraph style includes a bottom border by default. When python-docx applies the `Title` style to a document heading, a horizontal rule appears between the title and the first content section. This is immediately visible and looks like a formatting error to the reader.

**Observed during:** First generation of interview-questions-final.docx. The border appeared below "Interview Questions: Healthcare Risk Management Leader" before the "Warm-Up / Role Overview" heading.

**Fix:** Remove the border explicitly via python-docx XML manipulation on the style element after the document is created:
```python
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

pPr = title_style.element.get_or_add_pPr()
pBdr = OxmlElement('w:pBdr')
bottom = OxmlElement('w:bottom')
bottom.set(qn('w:val'), 'none')
pBdr.append(bottom)
pPr.append(pBdr)
```

This fix was applied in `_gen_interview_questions_docx.py`. It should be built into any future Word delivery skill as a standard style initialization step — the Title border removal should happen automatically, the same way the PDF deliver skill sets up the praxisity_style defaults on every run.

---

## Design Decision: Keep /new-project command

**Not a bug.** Initially flagged as a potential artifact to remove, but the user identified a valid use case: copying a mature project to a new folder and re-running `/new-project` to create an iteration that preserves lessons learned. Future enhancement could have the command read through existing project state and generate guidelines for the new iteration.

---

### BUG-038: /deliver does not handle numbered lists

**Severity:** Low
**Status:** Open (command-level fix needed)
**Affects:** /deliver

The deliver skill's markdown parser maps bullet lists to `styles["BulletItem"]` but does not have explicit handling for numbered (ordered) lists. Numbered list items fall through to `styles["BodyText"]`, rendering as plain paragraphs with the number prefix as literal text (e.g., "1. Question text").

**Observed during:** /deliver run on interview-questions-final.md. The document is entirely numbered lists, so this affects every content line.

**Why this matters:** The visual output is acceptable for this document (body text with number prefix reads fine), but it loses the semantic distinction. Numbered lists should render with consistent left-indent and spacing as a proper ordered list, not as flowing body paragraphs.

**Fix needed in command:** Add numbered list detection to the markdown parser in the deliver script generation step. Lines matching `^\d+\. ` should render with `styles["BulletItem"]` (or a new `NumberedItem` style with matching indent) rather than `styles["BodyText"]`.

---

### BUG-039: /deliver leaves generation script in deliverables/

**Severity:** Low
**Status:** Open (command-level fix needed)
**Affects:** /deliver

The deliver skill generates a Python script, executes it, then moves on — but does not clean up the script afterward. The script (e.g., `_gen_interview_questions.py`) ends up committed alongside the PDF in `deliverables/`, which is a build artifact, not a deliverable.

**Observed during:** /deliver run on interview-questions-final.md. Script was kept intentionally for framework testing, but in normal use it should be removed.

**Fix needed in command:** After successful PDF generation, delete the generation script. Alternatively, write the script to a temp directory (e.g., `/tmp/`) so it never lands in the project tree.

---

### BUG-040: Context compaction mid-DIP execution causes step state loss

**Severity:** High
**Status:** Open (framework-level issue, relevant to skill transition)
**Affects:** /build (and any long-running command)

When a conversation is compacted mid-execution (due to context window pressure), the agent loses granular step state. In DIP-003, the compaction occurred during Step 1 (question selection). The selection work happened in the compacted portion of the conversation and was not recoverable from the resumed context — the agent had to reconstruct what had been decided.

**Observed during:** /build DIP-003. The question selection and merge/cut decisions were made in the pre-compaction conversation. After compaction, the agent resumed at Step 2 (ordering) without a record of Step 1's output artifact (cut notes). The user noted the original decisions may be recoverable from their local conversation archive.

**Why this matters:** DIPs are designed as step-by-step processes with intermediate outputs. If compaction wipes intermediate outputs before they are written to files, the DIP cannot be reliably resumed. This is particularly risky for long DIPs (e.g., DIP-001 which read the entire textbook).

**Fix needed in framework:** As commands transition to real skills, each DIP step should write its intermediate output to a file before proceeding to the next step. This makes the state recoverable after compaction. Consider a `.plans/wip/` directory for in-progress step outputs that get cleaned up on DIP completion.

---

### BUG-041: DIP-003 cut notes not persisted as artifact

**Severity:** Low
**Status:** Open (command-level fix needed)
**Affects:** /build (DIP-003)

DIP-003 Step 1 specifies: "Document why each cut question was removed (brief note)." and lists the output as "Selected 15-20 questions with brief cut notes for removed candidates." The cut decisions were made in conversation but never written to a file. The rationale for the 8 dropped questions has no persistent record.

**Root cause:** Related to BUG-040 — context compaction disrupted the step. But even without compaction, Step 1 had no designated output file for cut notes. The DIP should have specified a file path for this intermediate output.

**Fix needed in command:** DIP-003 Step 1 should write cut notes to a file (e.g., `deliverables/candidate-questions.md` as an appended section, or a separate `deliverables/cut-notes-DIP-003.md`). Without a file path, agents will complete this step in memory only.

---

### BUG-042: PLANNING.md not updated after DIP-003 completion (recurrence of BUG-036)

**Severity:** Medium
**Status:** Open (command-level fix needed)
**Affects:** /build (DIP-003)

Same pattern as BUG-036. After DIP-003 execution completed (acceptance criteria verified, formatting done), PLANNING.md was never updated to record DIP-003 as complete. The session moved directly into cleanup and /deliver without the prescribed PLANNING.md update.

**What happened:** PLANNING.md went from showing "/build (DIP-003) In Progress" directly to "/deliver In Progress" — DIP-003 completion was never recorded.

**Pattern note:** This is now the third observed instance of this failure (DIP-001, DIP-002 implied, DIP-003 confirmed). The PLANNING.md update is consistently skipped or deferred. This should be a hard gate before the success message in the /build skill spec.

---

### BUG-043: DIP-003 success message not shown (recurrence of BUG-037)

**Severity:** Low
**Status:** Open (command-level fix needed)
**Affects:** /build (DIP-003)

Same pattern as BUG-037. After DIP-003 acceptance criteria were verified and the formatted deliverable was confirmed, no structured success message was shown. The session moved directly into the "clean up for delivery" review.

**Same pattern as BUG-021, BUG-032, BUG-037** — success messages are consistently skipped or abbreviated. Now confirmed across DIP-001, DIP-002, and DIP-003.

---

### BUG-044: /deliver success message not shown

**Severity:** Low
**Status:** Open (command-level fix needed)
**Affects:** /deliver

The deliver skill prescribes a success message showing: source file, output path, page count (if available), suggested next steps. After PDF generation, the agent reported the shell output (file size via `ls -lh`) but never presented the structured success message.

**Same pattern as BUG-021, BUG-032, BUG-037, BUG-043** — structured success messages are a persistent failure point across all commands.

---

### BUG-045: /deliver page count not obtained or communicated

**Severity:** Low
**Status:** Open (command-level fix needed)
**Affects:** /deliver

The deliver skill says to show "page count (if available)." The generation script attempted to get the page count via pypdf/PyPDF2 but neither was installed, so the count was silently skipped. The user was never told the page count was unavailable.

**What happened:** The `except ImportError: pass` block swallowed the failure silently. No fallback, no notification.

**Fix needed in command:** If page count cannot be determined, report it explicitly: "Page count: unavailable (pypdf not installed)." Optionally offer to install pypdf. Do not silently skip.

---

### BUG-046: /deliver parser does not handle `---` horizontal rules

**Severity:** Low
**Status:** Open (command-level fix needed)
**Affects:** /deliver

The deliver skill's markdown parser handles: title, headings, body paragraphs, tables, code blocks, and bullet lists. It does not handle `---` thematic breaks (horizontal rules). A `---` line would fall through to `styles["BodyText"]` and render as a literal "---" paragraph.

**Observed during:** /deliver run on interview-questions-final.md. The `---` was removed from the source markdown during review as a workaround. The parser gap remains for any future document that uses horizontal rules.

**Fix needed in command:** Add `---` detection to the parser. Either skip it (no output) or render a thin horizontal line using ReportLab's `HRFlowable`.

---

## Bug Disposition Table (SPEC-004)

**Updated:** 2026-04-01
**Scope:** SPEC-004 covers full rewrites of 5 commands as skills (`/charter`, `/describe` (née /spec), `/design` (née /architect), `/plan` (née /define), `/do` (née /build)). `/deliver`, `/breakdown`, and `/new-project` are excluded — they require their own specs or are sunset candidates.

### Disposition Key
- **Address in rewrite** — will be resolved during the skill rewrite (SPEC-004 scope)
- **Deferred: /deliver** — deferred until `/deliver` gets its own spec
- **Deferred: /breakdown** — deferred until `/breakdown` gets its own spec
- **Deferred: /new-project** — deferred; `/new-project` is a sunset candidate pending framework distribution model decision
- **Deferred: platform** — platform limitation, not addressable by skill rewrites
- **Already fixed** — artifact-only fix applied during v0.5.0 testing, no command change needed

### /new-project Command (DEFERRED — sunset candidate)

| Bug | Summary | Disposition | Pattern Class | Rationale |
|-----|---------|-------------|---------------|-----------|
| BUG-001 | PLANNING.md not reset | Deferred: /new-project | Command-specific | Sunset candidate pending distribution model |
| BUG-002 | docs/examples/ not cleared | Deferred: /new-project | Command-specific | Sunset candidate pending distribution model |
| BUG-003 | .plans/references/ not cleared | Deferred: /new-project | Command-specific | Sunset candidate pending distribution model |
| BUG-004 | \_\_pycache\_\_ committed | Deferred: /new-project | Command-specific | Sunset candidate pending distribution model |
| BUG-005 | Missing .gitkeep files | Deferred: /new-project | Command-specific | Sunset candidate pending distribution model |
| BUG-006 | Framework files tracked in git | Deferred: /new-project | Command-specific | Sunset candidate pending distribution model |
| BUG-007 | README.md not fully adapted | Deferred: /new-project | Template handling (REQ-F1) | Sunset candidate; pattern class still valid via BUG-020 |
| BUG-008 | CHARTER.md comments stripped | Deferred: /new-project | Template handling (REQ-F1) | Sunset candidate; pattern class still valid via BUG-020 |
| BUG-009 | Templates interpreted instead of copied | Deferred: /new-project | Template handling (REQ-F1) | Original discovery of pattern class; still valid via BUG-020 (/spec) |

### /charter Command

| Bug | Summary | Disposition | Pattern Class | Rationale |
|-----|---------|-------------|---------------|-----------|
| BUG-010 | Domain context fields not fully gathered | Address in rewrite | Command-specific | Prompt each field individually |
| BUG-011 | Success Criteria quality indicators not gathered | Address in rewrite | Command-specific | Add missing prompt |
| BUG-012 | Constraints gathered as single combined prompt | Address in rewrite | One-at-a-time gathering (REQ-F3) | Prompt per constraint category |
| BUG-013 | Charter dates incomplete | Address in rewrite | Command-specific | Set all three date fields |
| BUG-014 | Success message incomplete | Address in rewrite | Success messages (REQ-F4) | Include all prescribed elements |
| BUG-015 | Amendment process not prompted | Address in rewrite | Command-specific | Add optional prompt |
| BUG-016 | Pre-flight step ordering | Address in rewrite | Pre-flight ordering (REQ-F2) | PLANNING.md must be step 2 |

### /spec Command

| Bug | Summary | Disposition | Pattern Class | Rationale |
|-----|---------|-------------|---------------|-----------|
| BUG-017 | Pre-flight step ordering (same as BUG-016) | Address in rewrite | Pre-flight ordering (REQ-F2) | Same pattern |
| BUG-018 | Sections gathered in batches | Address in rewrite | One-at-a-time gathering (REQ-F3) | One section at a time with pause |
| BUG-019 | Review and Confirm step skipped | Address in rewrite | Command-specific | Enforce structured review format |
| BUG-020 | Template written from scratch | Address in rewrite | Template handling (REQ-F1) | Root cause: BUG-009 |
| BUG-021 | Success message missing next steps | Address in rewrite | Success messages (REQ-F4) | Include all prescribed elements |
| BUG-022 | Post-save Todoist option not offered | Address in rewrite | Command-specific | Offer post-save options as specified |

### /architect Command

| Bug | Summary | Disposition | Pattern Class | Rationale |
|-----|---------|-------------|---------------|-----------|
| BUG-023 | Metadata not gathered | Address in rewrite | Command-specific | Prompt for title/author before content |
| BUG-024 | Spec auto-selected without listing | Address in rewrite | Command-specific | Confirm selection even when argument provided |
| BUG-025 | MUST requirement coverage check not shown | Address in rewrite | Command-specific | Show traceability matrix |
| BUG-026 | No domain-relevant examples shown | Address in rewrite | Command-specific | Show examples before drafting |
| BUG-027 | Introduction step incomplete | Address in rewrite | Success messages (REQ-F4) | Include framing explanation |

### /define Command

| Bug | Summary | Disposition | Pattern Class | Rationale |
|-----|---------|-------------|---------------|-----------|
| BUG-028 | Task selection step skipped | Address in rewrite | Command-specific | Confirm DIP selection list |
| BUG-029 | Multiple DIPs generated in single run | Address in rewrite | Command-specific | Design decision: add batch mode or enforce one-per-run |
| BUG-030 | Git commit not offered post-save | Address in rewrite | Command-specific | Offer git commit after saving |
| BUG-031 | Template sections removed instead of N/A | Address in rewrite | Template handling (REQ-F1a) | Mark inapplicable sections N/A |
| BUG-032 | Success message not shown | Address in rewrite | Success messages (REQ-F4) | Include full prescribed format |

### /build Command

| Bug | Summary | Disposition | Pattern Class | Rationale |
|-----|---------|-------------|---------------|-----------|
| BUG-033 | Objective/step summary not displayed | Address in rewrite | Command-specific | Show objective and steps before starting |
| BUG-034 | Steps 2-6 batched into single execution | Address in rewrite | One-at-a-time gathering (REQ-F3) | Mark each step individually even if execution overlaps |
| BUG-035 | Git diff not shown before commit | Address in rewrite | Command-specific | Always show git diff --staged |
| BUG-036 | PLANNING.md not updated after DIP completion | Address in rewrite | PLANNING.md gating (REQ-F5) | Hard gate before success message |
| BUG-037 | Success message abbreviated | Address in rewrite | Success messages (REQ-F4) | Include all prescribed elements |

### /deliver Command (DEFERRED)

| Bug | Summary | Disposition | Pattern Class | Rationale |
|-----|---------|-------------|---------------|-----------|
| BUG-038 | Does not handle numbered lists | Deferred: /deliver | /deliver-specific | Python parser fix, separate process |
| BUG-039 | Leaves generation script in deliverables/ | Deferred: /deliver | /deliver-specific | Cleanup step needed |
| BUG-044 | Success message not shown | Deferred: /deliver | Success messages | Will adopt standard when rewritten |
| BUG-045 | Page count not obtained | Deferred: /deliver | /deliver-specific | pypdf dependency |
| BUG-046 | Parser does not handle horizontal rules | Deferred: /deliver | /deliver-specific | Parser gap |

### Platform / Cross-Cutting

| Bug | Summary | Disposition | Pattern Class | Rationale |
|-----|---------|-------------|---------------|-----------|
| BUG-040 | Context compaction causes step state loss | Deferred: platform | Platform limitation | Not fixable by command rewrites; relevant to future skill transition |
| BUG-041 | DIP-003 cut notes not persisted | Deferred: platform | Platform limitation | Related to BUG-040; DIP design issue, not command issue |
| BUG-042 | PLANNING.md not updated after DIP-003 | Address in rewrite | PLANNING.md gating (REQ-F5) | Third instance of same pattern — /build rewrite will enforce |
| BUG-043 | DIP-003 success message not shown | Address in rewrite | Success messages (REQ-F4) | Third instance — /build rewrite will enforce |

### Framework Issues

| Issue | Summary | Disposition | Rationale |
|-------|---------|-------------|-----------|
| ISSUE-001 | Template example counts anchor agent output | Address in rewrite | REQ-F7; verify existing CLAUDE.md hint sufficiency |
| ISSUE-002 | Smart quotes in PDF output | Deferred: /deliver | Cosmetic, /deliver-specific |
| ISSUE-003 | Word Title bottom border | Deferred: /deliver | Cosmetic, /deliver-specific |

### Summary

| Disposition | Count |
|-------------|-------|
| Address in rewrite (SPEC-004 scope) | 26 bugs + 1 issue |
| Deferred: /new-project (sunset candidate) | 9 bugs |
| Deferred: /deliver | 5 bugs + 2 issues |
| Deferred: /breakdown | 0 (no bugs logged) |
| Deferred: platform | 2 bugs |
