# PLANNING.md

## Active Context

**Branch:** `consolidate` (off main at 758f13a — if this goes badly, delete the branch and start over)
**Last Command:** agent pass: roster into agent-authoring (step 8b)
**Status:** Steps 1–8b complete; next is step 9 (README, charter, changelog to 0.7.0, merge) then the live test
**Date:** 2026-10-08
**Version:** 0.6.0 → targeting 0.7.0 at end of consolidation

## Goal of This Branch

Get Praxisity to a state where it can be installed into a real school project and used for the core workflow. Two objectives only:

1. **Core workflow complete** — `/charter` → `/describe` → `/design` → `/detail` → `/do` all exist as skills with bundled templates, in markdown.
2. **Portable** — the framework packages as a Claude Code plugin installable per project.

Everything else is deferred. SPEC-009 is shelved (see its header note). `/deliver`, `/breakdown`, HTML output, consolidation protocol, and the ISD-specific agents/charter changes wait until the core is in use.

## Context Change

Andrew completed the MPH and started a doctorate of education in instructional systems design and technology (September 2026). Expect new theories and techniques to feed into the framework soon — new agents, charter revisions, possibly an ISD project domain. None of that is blocking; it is the reason the core needs to be clean first.

## Work Plan

| Step | Task | Status |
|------|------|--------|
| 1 | Commit SPEC-009 as shelved, create `consolidate` branch | Done |
| 1b | Re-review `/charter` before it becomes the pattern (4-agent Mode 2, two rounds); rewrite charter skill, template, and gather skill | Done — see `.plans/reviews/SESSION-2026-09-22/charter-skill-lead-review.md` |
| 2 | Build `/describe` skill from `/spec` command, bundle spec template | Done — two-round Mode 2 review; see `describe-skill-lead-review.md`. Not yet live-tested. |
| 3 | Build `/design` skill from `/architect` command, bundle design template | Done 2026-09-23 — two-round Mode 2 review; reference convention adopted; see `design-skill-lead-review.md`. Not yet live-tested. |
| 4 | Build `/detail` skill from `/define` command, bundle DIP template | Done 2026-10-02 — two-round Mode 2 review; see `detail-skill-lead-review.md`. Not yet live-tested. |
| 5 | Build `/do` skill from `/build` command (no template) | Done 2026-10-02 — two-round Mode 2 review; see `do-skill-lead-review.md`. Not yet live-tested. |
| 6 | Delete `.claude/commands/`; bundle or park remaining templates; archive pre-September reviews and references | In progress 2026-10-02 — commands deleted; reviews and references archived; claude/readme/changelog/gitignore templates rewritten and bundled in `/charter` (Post-Save checklist), `/do` appends to CHANGELOG.md; `adr.template.md` parked in `.praxisity/templates/` for a future `/decide` skill. Awaiting a one-round review of the charter extension. |
| 7 | Refresh skill-forge platform reference and praxisity-patterns | Done 2026-10-08 — both rewritten; prompt-engineer and consistency-reviewer passes applied (tested-vs-documented split, skeleton self-contained, patterns no longer over-generalize from /design; describe gate exits named; gather term "Drafted by you") |
| 8a | Package skills as a plugin: `.claude-plugin/plugin.json` pointing `skills` at `./.claude/skills/`, marketplace.json (`arspenn`, `source: "."`); validate; test `--plugin-dir` | Done 2026-10-08 — `claude plugin validate .` passes; headless `/praxisity:charter` in `~/Dev/praxisity-test` ran full pre-flight (PLANNING.md to contract, gather defaults, intro, Mission prompt). Verified: namespaced load, `${CLAUDE_SKILL_DIR}` in plugin. Plugin ships agentless. Watch in live test: source-material invite and Mission prompt landed in one message. |
| 8b | Agent pass: roster as templates in `agent-authoring/templates/roster/` (single source; this repo's `.claude/agents/` is an installed, gitignored copy); checklists harvested from agent memory into critic, prompt-engineer, user-advocate, consistency-reviewer; severity levels defined in every roster file; `agent-authoring` rebuilt with Install and Author flows | Done 2026-10-08 — PE + critic review applied (checklists as conditional checks, diff-before-overwrite, default install all nine, roster promotion only in the source repo, gitignore narrowed to roster names). |
| 9 | Update README, CHARTER scope/milestones, CHANGELOG to 0.7.0; merge to main | Not started |

Build order for steps 2–5 follows the pattern set by the revised `/charter` (2026-09-22): inline PLANNING.md contract, sequential pre-flight with reasons, explicit gather invocation, template owns section guidance, pacing table using gather's four terms, copy-then-edit with a closed operations list, cancel paths reset PLANNING.md, offer-only post-save, completion gate, honest success message. Review each clone with prompt-engineer + critic + spot in Mode 2 (they hold checklists in agent memory from the charter review). No Mode 3.

Decisions made 2026-09-22: Domain Context is generic (three transferable questions, examples per field in the template comment); Stakeholders/Success Criteria/Constraints are checklist prompts; `TBD — revisit at [milestone]` is a marker distinct from N/A; source material conventionally lives in `.plans/references/`.

Verified 2026-10-08 in the plugin-dir run: `${CLAUDE_SKILL_DIR}` inside a plugin; namespaced skill load; gather hand-off (defaults saved). Still to verify in the interactive live test: `@CHARTER.md` import actually loads; `$ARGUMENTS` inside a skill; whether a marketplace-installed plugin's directory is readable without a prompt; `/agent-authoring` install → `/agents` → dispatch picks up the new definition in the same session (the critic reviewing the roster reported running on the pre-pass definition, so registration timing is unproven). Test project: `~/Dev/praxisity-test` (sibling repo, kept for repeated use; run with `claude --plugin-dir ~/Dev/praxisity --add-dir ~/Dev/praxisity`).

ID pattern for /detail (from the /describe and /design reviews): IDs assigned on approval, highest-ever-plus-one, never renumbered; removed items kept with the ID struck; coverage gates withhold the save option and name their exits; `MMM` for a parent document's number; one parent per child.

Reference convention (2026-09-23, canonical block in every template header and in skill-forge's praxisity-patterns): `REQ-F1 (short label)` for cross-document elements; `§7.4 Title` for sections; relative link with ID text for documents; `~~REQ-F3~~ (removed v0.2)` for removals.

## Skills Status

### Workflow Skills (user-invoked)
| Skill | Status | Notes |
|-------|--------|-------|
| /charter | Rewritten 2026-09-22, not yet live-tested | Pattern-setter. Live test on the Praxisity charter update (step 9) or a school project. |
| /describe | Built 2026-09-22, not yet live-tested | IDs assigned on approval, never renumbered; revise flow with struck rows; MUST→AC coverage gate |
| /design | Built 2026-09-23, not yet live-tested | Generic Architecture (context, approach, key choices); coverage gate with design-wide and deliberate-gap escapes; spec-diff on revise |
| /detail | Built 2026-10-02, not yet live-tested | Cite-only reference sections, full-text steps; Status lifecycle shared with /do; artifacts may be locations inside a file |
| /do | Built 2026-10-02, not yet live-tested | Status row is the durable record; user-performed steps; completion gate before commit; legacy DIPs refused |

### Support Skills (auto-invokable)
| Skill | Status | Notes |
|-------|--------|-------|
| /gather | Rewritten 2026-09-22 | Defaults instead of calibration questions; four pacing terms; TBD/N/A skip states; owns drafting rule |
| /skill-forge | Built | Platform reference stale (step 7) |
| /consult-team | Built; audit deferred | Points at /agent-authoring when the roster is absent. Audit later: named agents report twice (SendMessage + idle notice); dispatch guidance should ask for one short final line. |
| /agent-authoring | Rebuilt 2026-10-08 | Install the roster (nine templates, single source) or author a new agent; roster reference replaces the old agents README |

### Legacy Commands (delete in step 6)
spec, architect, define, build, new-project, deliver, breakdown, _prototype-charter

## Verified Platform Capabilities

See `reference_skill_platform_capabilities.md` in project memory. Re-checked 2026-09-22 against Claude Code 2.1.280 docs: plugins available, commands deprecated, agent teams still experimental, plugin agents cannot use memory.

## Next Steps

1. Step 6: delete `.claude/commands/` (8 files) and `.praxisity/templates/` (now bundled in skills; keep `claude.template.md`, `readme.template.md`, `gitignore.template`, `changelog.template.md`, `adr.template.md` somewhere or decide they go too); move `.plans/reviews/` pre-2026-09 reports and stale `.plans/references/` into `.plans/archive/`; update `/consult-team` paths.
2. Step 7: refresh skill-forge (`when_to_use` now supported; `model`, `effort`, `context: fork`; plugin notes) and praxisity-patterns (PLANNING.md contract, pacing terms, gates, Status lifecycle, `context: fork` prohibition for interactive skills).
3. Step 8: plugin packaging and the verification list.
4. Live-test the full chain on a real project, ending with a `/do` run that halts on purpose, is revised with `/detail`, and resumes.

## First skill after consolidation

`/decide` — decision-support skill producing an ADR from `.praxisity/templates/adr.template.md` into `.plans/decisions/`. Cross-cutting decisions that would already be ADRs: shelving SPEC-009, the reference convention, naming the fourth phase `detail`, tracking in Status row + task list + commit body rather than ticks. Write them when the skill exists.

## Developer scratch pad (out of session notes)
- Consider adding an 'ex nihilo' pattern for the skill forge. Consider using this pattern to create new deep research skill. Consider adding that to the 'ex nihilo' pattern we used to create it.
- ISD/EdD integration: new theories may need dedicated agents and charter changes. Templates currently branch on Software / Public Health / Research domains — an Instructional Design domain will likely be needed. Keep domain sections generic during the rebuild so adding one later is cheap.