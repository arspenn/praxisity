## Prompt Engineer Review

**Artifact:** `/charter` skill — `.claude/skills/charter/SKILL.md`, `templates/charter.template.md`, with `.claude/skills/gather/SKILL.md` as dependency
**Date:** 2026-09-22
**Dispatch Mode:** Mode 3 (team teammate, lead-directed)

## Instructions Received

Evaluate the charter skill and template as prompts against Fable 5.1 / Claude Code 2.1.280 guidance, before it is cloned to describe/design/plan/do and packaged as a plugin. Focus: signal-to-noise, elephants, bare imperatives needing reasons, template-comment redundancy, cloning/plugin hazards, Agent Consultation section.

## Findings

### HIGH — Two competing gathering guides that have already drifted
**Location:** SKILL.md line 27 ("the HTML comments are your guide for what to gather") vs. SKILL.md lines 39–84 (Sections 1–9 restating the guidance); template comments.
**Problem for AI:** The agent loads both. Where they disagree it must pick one silently. They already disagree: template Constraints comment (lines 148–154) lists six categories (Timeline, Budget, Technical, Regulatory, Organizational, Domain); the template fields and SKILL.md Section 6 list five different ones (Timeline, Resources, Technical, Regulatory/Compliance, Other). Template Stakeholders comment (lines 97–102) gives five roles (Primary users, Secondary users, Contributors, Beneficiaries, Affected parties); the fields and SKILL.md Section 4 give four others. This is ~45 lines of SKILL.md context spent restating a template that is in context anyway.
**Problem for humans:** Maintainers edit one and forget the other. Five clones make this ten places to keep in sync.
**Fix:** One owner. Recommend the template's comments own per-section guidance (they already carry the examples), and SKILL.md's "Gather Charter Content" becomes an ordered list with only the exceptions:
```
Gather sections in template order, one at a time, following the gather protocol. The template comments say what each section needs. Exceptions:
- Mission: if CLAUDE.md or the conversation already states it, present it as a draft.
- Domain Context: detect project type from CLAUDE.md or ask; gather only the matching domain block.
- Glossary: gather last. Draft it yourself from terms used in earlier sections that a reader without project context would not know, then present for approval.
```
Then reconcile the template comments to the fields (or delete the category lists in the comments, since the fields already enumerate them).

### HIGH — Cancel paths strand PLANNING.md in "in progress"
**Location:** Pre-flight step 3 "(c)ancel"; Review and Confirm "(c)ancel"; Completion Gate (line 116).
**Problem for AI:** Step 2 sets PLANNING.md to "/charter in progress" before any cancel option exists. Both cancel branches exit without reaching the Completion Gate, and nothing tells the agent to reset. Next session reads a stale in-progress state. This propagates to all five clones.
**Fix:** Add one line after the Completion Gate: "If the user cancels at any point, update PLANNING.md to note the cancellation before ending, for the same reason as the gate: the next session reads PLANNING.md first."

### MEDIUM — Dependency on /gather auto-invocation is untested and plugin-fragile
**Location:** SKILL.md line 37 "follow the gathering protocol (see /gather)"; meta-review QG-2 (2026-04-04) still open.
**Problem for AI:** "(see /gather)" is a reference, not a load instruction. If gather has not auto-invoked, the agent has only the charter skill's inline "one at a time" phrasing, which is the exact class of instruction that failed in BUG-018. Inside a plugin, cross-skill auto-invocation is unverified.
**Fix:** Make loading explicit in pre-flight: "6. Invoke the `gather` skill so its protocol is in context before the first section." Testable, and the same line works in every clone.

### MEDIUM — Load-bearing rules stated without their reasons
**Location:** Line 21 (sequential pre-flight), line 24 ("This must complete before step 3" restates line 21), line 92 ("Never use Write for template-derived files"), line 116 ("hard gate").
**Problem for AI:** These held in the April live run and should keep their structure. But Fable follows a rule more consistently when it knows what the rule protects, and the reasons are cheap to state. The duplicate on line 24 is pure noise.
**Fix (keeps the same instruction class, adds the why):**
- Line 21: "Run these steps in order and finish each before starting the next. Step 2 must land first so an interrupted run still leaves PLANNING.md accurate; step 3's outcome changes what steps 4–5 mean." Delete the restatement on line 24.
- Line 92: "Copy the template, then Edit the copy. Edit keeps the template's structure as ground truth; regenerating the file with Write reproduces it from memory and drifts (renamed headers, dropped sections, half-stripped comments)."
- Line 116: keep, append "because the next session reads PLANNING.md before anything else."

### MEDIUM — `${CLAUDE_SKILL_DIR}` appears three times; plugin resolution unverified
**Location:** Lines 27, 94, 106.
**Problem for AI/maintainers:** If the variable does not resolve inside a plugin, `cp` gets the literal string and fails loudly (good), but the fix is then three edits per skill, fifteen across the set.
**Fix:** Declare the path once near the top ("Template: `${CLAUDE_SKILL_DIR}/templates/charter.template.md`") and refer to "the template" elsewhere. Note the variable as unverified-in-plugin in the skill-forge platform reference until tested.

### MEDIUM — "Byte-for-byte unchanged" verify has no mechanism
**Location:** Line 106.
**Problem for AI:** No instruction on how to verify, so the agent asserts it rather than checks. In a plugin the template lives in a directory the agent should never touch anyway.
**Fix:** Replace with a scope statement: "All edits target the project's CHARTER.md. The template path is read-only input shared by every future run." If a check is wanted, give the command: `git diff --quiet -- <template path>`.

### MEDIUM — Constraints block duplicates gather and buries its one unique rule
**Location:** Lines 11–17.
**Problem for AI:** Three of five bullets restate gather ("Accept brief answers", "ask rather than assume", scope-to-template). The unique rule, "all sections except Mission can be skipped", is disconnected from the N/A instruction on line 100 that gives it teeth.
**Fix:** Compress to two lines: "Gather only what fills the template; the template defines the charter's shape. Every section except Mission may be skipped. Mark skipped sections `N/A — [reason]` rather than deleting them, so a reader sees the section was considered." Delete the rest.

### LOW — Agent Consultation section is dead text where it sits
**Location:** Lines 129–134.
**Problem for AI:** It follows the Success Message, so the skill has already ended when the agent reads it. No trigger says when to use it. `Agent(subagent_type: "stakeholder", prompt: ...)` is pseudo-syntax, and the canned prompt gives the stakeholder no pointer to the charter. Cloned five times this is 20+ lines of unreachable instructions.
**Fix:** Either cut it and add "Run /consult-team for a multi-perspective review" to the Success Message next steps, or make it actionable where a review helps: a fourth Review-and-Confirm option, "(a)sk the stakeholder agent for a read before saving", with the prompt pointing at the drafted content.

### LOW — Template count anchoring survived the April fix
**Location:** Template lines 41–45 (five numbered principle rows, two marked optional), Success Criteria and Scope rows.
**Problem for AI:** The Principles comment now says "no fixed count" but the five slots still anchor output toward five. SKILL.md line 102 counters this, but the placeholder rows are what the agent sees while editing.
**Fix:** Two rows per list, with the second reading "[add or remove rows to match the project]". Apply the same rule when writing the spec/design/DIP templates.

### LOW — Undefined term used as justification in both files
**Location:** SKILL.md line 84 and template line 250, "the dual-use design principle".
**Problem for AI/humans:** Referenced as if defined; defined nowhere in the skill, template, or gather. In a plugin used outside Praxisity it is meaningless.
**Fix:** Inline the definition once: "the charter is read by both humans and AI, so it must be self-contained".

### LOW — Small ambiguities
- Line 33 scripts the introduction verbatim and duplicates line 9; a `brief` gather preference gets the long version anyway. Replace with "Open with a sentence on what a charter is and that you will go one section at a time."
- Line 74 says "prompt each field individually" only for Public Health, implying other domains may batch. Delete the clause; gather's sub-section rule already covers it.
- Line 111 references an undefined "task management service". Cut. Line 112 "Optionally commit": say "Offer to commit" so the agent asks rather than decides.
- Template line 272 is a choice list inside a placeholder; an agent may substitute it literally. Make it a comment.

## What's Well-Engineered (preserve as the pattern)

- **Structure enforces order** (Post-Save → Completion Gate → Success Message). This is a different instruction class from prohibition and it held in the live run. Clone this shape exactly.
- **Closed list of permitted Edit operations** (lines 97–102). Specific, enumerable, and it names counts as illustrative with the reason attached.
- **Explicit update flow** in step 3 and new-vs-update date branching (lines 103–105). Both came from live failures and are correctly specified.
- **Delegation to /gather** instead of restating the protocol. Right call; just make the load explicit.
- **Frontmatter** `disable-model-invocation: true` is correct for a user-initiated workflow. No `when_to_use` needed for that reason.
- **Template examples** (Mission good/bad pairs, Scope examples) are the Input/Output style current guidance asks for. Keep them in the template, where they are stripped from the output.

## Top 5 Changes, Ranked

1. Make the template the single owner of per-section gathering guidance; reduce SKILL.md sections to an ordered list plus three exceptions. Reconcile template comments to fields.
2. Add a cancel-path PLANNING.md instruction next to the Completion Gate. Cross-cutting for all five skills.
3. Add an explicit "invoke gather" pre-flight step instead of relying on auto-invocation.
4. Attach the reason to the three load-bearing rules, delete the duplicate on line 24, and centralize the template path to one declaration.
5. Cut or relocate Agent Consultation; fix the template's five-slot principle anchoring and the undefined "dual-use" reference.

---

## Round 2 — 2026-09-22 (delta pass on the rewrite)

### Resolved
All ten Round 1 findings are resolved. Specifically: the template now owns per-section guidance and its comments match its fields (Constraints, Stakeholders); both cancel branches set PLANNING.md `cancelled` (pre-flight 4, Review and Confirm) with the gate restating it; gather is loaded explicitly (pre-flight 3); the sequential, copy-then-edit, and gate rules each carry their reason and the line 24 duplicate is gone; the template path is declared once (line 11) with a read-only scope statement replacing the unverifiable byte-check; Rules is three lines with N/A and TBD tied to "may be skipped"; Agent Consultation is folded into next steps as a conditional; principle slots are two rows with "add or remove"; "dual-use" is defined inline in both files; the verbatim intro, the Public Health-only "each field individually", the task-management service, and the choice-list placeholder are all gone. Commit and CLAUDE.md edits now require a yes.

### Partly resolved or new

**MEDIUM — Checklist sections leave unanswered sub-categories undefined.** SKILL.md line 68 marks "a skipped section", but Stakeholders, Success Criteria, and Constraints are now one prompt with categories as a checklist (lines 45–47). When the user answers two of five categories, nothing says whether the other three get a marker, keep their placeholder, or lose their sub-heading. An agent will pick one silently. Fix, in Generate step 4 Marking: "In a checklist section, each unanswered category gets its own marker; assume `N/A` unless the user said it is TBD."

**MEDIUM — Success message asserts something that may be false.** Line 87 says Claude will read CHARTER.md each session via CLAUDE.md, but Post-Save step 1 is an offer the user can decline. Fix: "If CLAUDE.md points to it, Claude will read CHARTER.md each session..." or drop the bullet when the offer was declined. Same conditional applies to the frontmatter description's "Claude reads it every session", acceptable there as intent.

**MEDIUM (cloning) — PLANNING.md schema is now inline in the skill.** Pre-flight step 1 defines the `## Active Context` block (Last Command, Status, Date) and `## Next Steps`. Five clones means five copies of a schema, which is the same drift class as Round 1 finding 1. Fix: state the schema once in the skill-forge praxisity-patterns reference and have each skill cite it in one line, or accept the duplication knowingly and grep all five on any change.

**LOW — Source-material invitation is stated in two places.** Charter Introduction (line 32) and gather "Source material" (line 40) both say to invite files, list `.plans/references/`, and read what is provided. Since gather is loaded before the intro runs, the agent may invite twice. Fix: charter keeps only its domain-specific example list ("a syllabus, assignment brief, rubric, proposal") and defers the mechanics to gather.

**LOW — "Purpose sentence" rule appears three times.** Gather lines 12 and 50, charter line 36. The charter copy carries the best reason ("where the user learns the shape of a project plan"). Keep charter line 36, trim gather line 50 to the instruction alone.

**LOW — Rule line 17 addresses the wrong reader.** "Must run in the main conversation, not a forked context" is a constraint on the frontmatter (`context: fork`), which the running agent cannot act on. Move it to a maintainer comment or the plugin README. Enforcement is the absence of `context: fork`.

**LOW — Domain Context pacing omits Key Context.** Table line 48 says "the three template questions"; the template has Domain, three questions, and Key Context (lines 157–169). Say "the three questions plus Key Context" or drop the field.

**LOW — Preference changes mid-session.** Gather line 18 says "Save the defaults, or whatever the user chose", but at that point the user has chosen nothing. Add: "If the user changes a preference mid-session, update the memory file."

No regressions or new elephants found. Every prohibition that survived ("do not push for more detail", "never commit without a yes", "batching is the failure mode") is paired with a reason or a positive alternative.

### Pacing table as the pattern for a spec skill
Yes, it is copyable. It works because the Pacing column uses a small closed vocabulary (One prompt; One at a time until done; Two prompts; One prompt with checklist; Drafted by you, last) and gather line 46 gives the decision rule for choosing among them: "whether pacing changes the answer, not how the template is formatted." A spec-skill author can apply that rule to requirements (item by item) versus metadata (checklist) without guessing. Two additions before cloning: name that vocabulary as a fixed set in gather or the praxisity-patterns reference so all five tables use identical terms, and show one example checklist prompt (three lines) in gather so "categories as a checklist" renders the same way in every skill.
