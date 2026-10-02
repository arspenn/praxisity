## Critic Review: /charter Post-Save project files and /do changelog line

**Artifact:** `.claude/skills/charter/SKILL.md` (Templates line, Post-Save, update flow); `templates/claude.template.md`, `readme.template.md`, `changelog.template.md`, `gitignore.template`; `.claude/skills/do/SKILL.md` Completion Gate 3, Safety and Commit 3 and 5; `dip.template.md` bookkeeping lines
**Date:** 2026-10-02 | **Dispatch Mode:** Mode 1 (team-lead consult) | **Reviewer:** critic

## Instructions Received

One-round check of the four project files offered after a charter save and the changelog line /do appends: re-offers in update mode, the CLAUDE.md Type field against pre-flight 5, the @CHARTER.md import timing, README link assumptions, /do's behaviour when Unreleased is absent, whether the changelog section is decidable from an Objective, and plugin-layout path risk.

## Findings

### Medium — /do has no fallback when `## [Unreleased]` is absent or the file is not Keep a Changelog
**Location:** do Completion Gate 3 ("append one line under `## [Unreleased]`"); changelog template comment ("rename Unreleased to the version ... start a fresh Unreleased block").
**Problem:** The template tells the user to recreate Unreleased by hand after a cut; the first time they forget, /do has no heading to append under. A project adopting Praxisity with an existing CHANGELOG may have no bracketed Unreleased or no Added/Changed sections at all.
**Fix:** "If there is no `## [Unreleased]` heading, insert one above the newest version with the four sections. If the file does not follow Keep a Changelog, append nothing and tell the user where the line would have gone."

### Medium — The changelog section is not decidable from the Objective; the commit type is
**Location:** do Completion Gate 3 ("in the section that fits ... from the DIP's Objective").
**Problem:** An Objective states what is true when the DIP is done ("the export runs in under two seconds"). That reads as Added or Changed or Fixed depending on history the DIP does not hold. Fixed in particular needs knowledge of a prior defect. The Objective is also declarative; the template demands imperative mood.
**Fix:** Derive the section from the DIP's Commit Instructions type: feat is Added, fix is Fixed, refactor, docs, content, and test are Changed; Removed when the Objective or DO list says remove. Rephrase the Objective in imperative mood. Ask only when the type is absent.

### Medium — "Type" flows from nowhere
**Location:** charter Pre-Flight 5 ("read it for the project name, type, and mission as defaults"); claude.template line 17 (**Type:** "the field this project belongs to"); Post-Save 1 ("substitute placeholders from the charter").
**Problem:** The charter template has no Type; its nearest field is Domain Context's **Domain**, which is exactly what claude.template's Type describes. Pre-flight 5 reads a type that no gather row consumes, and Post-Save fills Type from a charter field that does not carry that name. Praxisity's own CLAUDE.md has "Type: Development Framework / Tooling", a project kind, not a field, so the two readings already diverge in the one live example.
**Fix:** Rename claude.template's field to **Domain:** and say in pre-flight 5 that it is the default for Domain Context. Or keep Type and define it as the charter's Domain, in both places.

### Low-Medium — Template content that is Praxisity's, not the user's
**Location:** claude.template Bootstrapping Principle ("should become a skill, agent, or template"); readme.template line 46 (`.plans/decisions/`) and line 50 (`[YOUR-USERNAME]`); gitignore comment ("used by some Praxisity tooling").
**Problem:** The Bootstrapping section is framework-author language pasted into every user project, and contradicts the template's own "start minimal" comment. No skill in this workflow creates `.plans/decisions/`. `[YOUR-USERNAME]` is a bracketed placeholder with no source in the charter, so Post-Save's substitution rule either leaves it or guesses. The Python-cache comment names tooling that a fresh plugin install does not have.
**Fix:** Drop Bootstrapping or reword it toward the user's learning ("what did you learn that should change the charter"). Remove the decisions line. Hardcode the real repository URL or drop the link. Make the gitignore comments generic.

### Low — Platform claims and plugin paths
The Success Message states that Claude will load CHARTER.md each session; the `@` import is documented but untested here, and Praxisity's own CLAUDE.md uses a pointer, not an import. Say "should" until the first fresh-session check, then record it. `${CLAUDE_SKILL_DIR}` is verified for a project skill and unverified inside a plugin; this change adds four more paths to that single dependency, so the plugin packaging step should test it before anything else. The import itself has no timing problem: CHARTER.md is on disk before Post-Save runs, and the import reads the filesystem, not git.

### Low — Template and flow nits
The changelog seed entry "Project charter established" is past tense beside a comment demanding imperative mood. Charter updates never reach CHANGELOG, though the template promises the file "maintains itself"; append "Change: update project charter" in update mode when the file exists, or say charter history lives in its own dates. In update mode with every file present the checklist is empty; say to skip the message rather than show an empty list.

### Confirmed sound
Re-offers: each item is guarded by "If missing," so an update run offers nothing that exists and only the import line if CLAUDE.md lacks it. README links: CHARTER.md and CHANGELOG.md are written to the same directory as README.md, so the links hold wherever that directory sits. Bookkeeping: do Rules, Completion Gate 3, Safety 3 and 5, and the three dip.template lines all name CHANGELOG.md consistently, and staging it "if it was appended" is correct.

## Ranked Top 3
1. Give /do a fallback for a missing Unreleased heading and a non-conforming file.
2. Derive the changelog section from the commit type, not the Objective.
3. Resolve Type versus Domain so pre-flight 5, the charter, and claude.template agree.

## Self-Evaluation
- **What worked well:** Reading the live CLAUDE.md beside claude.template exposed the Type divergence as observed, not reasoned.
- **What you struggled with:** Cannot test the `@` import or the plugin variable; both findings are pointers to tests, not defects.
- **Prompt improvement suggestions:** Add to the checklist: "for every placeholder in a secondary template, name the field in the primary artifact that fills it."