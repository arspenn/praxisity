## Prompt Engineer Review

**Artifact:** `.claude/skills/charter/SKILL.md` Post-Save; `templates/claude.template.md`, `readme.template.md`, `changelog.template.md`, `gitignore.template`; `.claude/skills/do/SKILL.md` Completion Gate and Safety and Commit
**Date:** 2026-10-02
**Dispatch Mode:** Mode 1 (subagent consult)

## Instructions Received

One-round review of the charter Post-Save checklist, the four project-file templates, and the /do changelog append. Questions: checklist vs gather protocol; does the CLAUDE.md template follow its own start-minimal advice; are comments working or restating; is the changelog append unambiguous; what breaks outside Praxisity. Under 60 lines.

## Dual-Consumption Assessment

### Clarity — The checklist does not collide with gather
**Location:** charter SKILL.md Post-Save
The gather protocol's one-at-a-time rule is for sections where each item changes the user's thinking. Four yes/no offers are the protocol's own Checklist term, and the skill names it that. No collision. One soft spot: item 2 drafts the README Overview and creates the file on a bare yes, so the draft is never shown for approval. Acceptable because it is derived from two sections the user just approved; say "show the Overview draft in the created file" so the user knows to look.

### Ambiguity — "Strip the comments" will delete the gitignore
**Location:** Post-Save intro; `gitignore.template`
**Problem for AI:** The shared recipe says "strip the comments". Three templates use HTML comments; the gitignore uses `#` comments, which are its only documentation. A literal agent removes them.
**Suggested fix:** "strip the HTML comments".

### Noise — CLAUDE.md template does not take its own advice
**Location:** `claude.template.md` Workflow and Bootstrapping Principle
**Problem for AI:** The header says start minimal and add a line only after the same mistake twice. Identity, the import, Current Focus, and the two empty correction sections honour that. Workflow restates four skill descriptions the platform already loads, plus a rule. Bootstrapping Principle is Praxisity's own identity: in a public-health or instructional-design project it tells the agent, every session, to look for skills, agents, and templates to build. That is a standing directive the user never chose.
**Suggested fix:** Cut Bootstrapping Principle. Compress Workflow to one line: "Work follows /describe, /design, /detail, /do; each skill carries its own instructions."

### Drift — Comments that only survive in the template
**Location:** `claude.template.md` Behavioral Corrections and Non-Obvious Context
**Problem for humans:** The format and example for these sections live in comments, and comments are stripped. The person who adds the first entry months later sees an empty heading. The other comments are doing work: the claude header carries the rationale and the add-a-line criterion; the changelog comment carries the Unreleased lifecycle; the readme Getting Started comment carries field examples. The Constitution comment restates Post-Save item 1 and can go.
**Suggested fix:** Replace the two stripped comments with one visible italic line each: "Add an entry only after the same mistake twice; remove it when it stops."

### Ambiguity — Changelog append: section and wording are both judgment calls
**Location:** do SKILL.md Completion Gate step 3; `changelog.template.md`
**Problem for AI:** "The section that fits" asks the agent to choose among four headings with no key. "From the DIP's Objective" produces a state ("Users can reset passwords"), while the template comment demands imperative mood ("Add"), and the seeded entry is past participle ("Project charter established"). Three conventions in one file; sessions will differ. The citation form is also unstated.
**Suggested fix:** Map from the DIP's commit type: feat to Added, fix to Fixed, anything that removes to Removed, all else Changed. Wording: "one imperative line naming what was delivered, ending with (DIP-NNN)". Fix the seed to "Add project charter". Add: "create the heading if a version was cut and Unreleased is missing." The gate's "both files" is now three.

### Clarity — Things that break outside Praxisity
**Location:** `readme.template.md` lines 46 and 50; `gitignore.template` line 8
- The Praxisity link is `github.com/[YOUR-USERNAME]/praxisity`. The user is not the framework's author; this should be the canonical URL, not a placeholder.
- The Documentation list names `.plans/decisions/` for ADRs. No skill on this branch creates it, so every new project ships a dead pointer.
- The gitignore comment claims "Python caches (used by some Praxisity tooling)". The branch is markdown-only; the claim is stale and will outlive the comment's author. Keep the pattern, drop the reason.
- `.claude/agent-memory/` is ignored here but tracked in Praxisity's own repo. Right default for user projects; note it so the template is not applied to this repo.

## What's Well-Engineered

- The `@CHARTER.md` import is real platform syntax and the Success Message tells the user the consequence of declining it.
- The changelog lifecycle comment (rename Unreleased, start a fresh block) is the one instruction a future human needs and it is where they will look.
- Listing CHANGELOG.md as bookkeeping in both the scope check and the stage-by-name step keeps /do's git safety consistent with the new write.

## Self-Evaluation

- **What worked well:** Reading the shared recipe against the one template with a different comment syntax caught the gitignore deletion.
- **What you struggled with:** Whether the Workflow section earns its place depends on how reliably skill descriptions load in a plugin install, which I could not verify here.
- **Prompt improvement suggestions:** Add "when a template is for a project other than this one, check every pointer and claim against the receiving project, not against this repo."