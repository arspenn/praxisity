# PLANNING.md

## Active Context

**Branch:** `consolidate` (off main at 758f13a — if this goes badly, delete the branch and start over)
**Last Command:** /design skill built and reviewed (manual, Mode 2 team); reference convention adopted
**Status:** Step 3 complete; next is step 4 (/plan)
**Date:** 2026-09-23
**Version:** 0.6.0 → targeting 0.7.0 at end of consolidation

## Goal of This Branch

Get Praxisity to a state where it can be installed into a real school project and used for the core workflow. Two objectives only:

1. **Core workflow complete** — `/charter` → `/describe` → `/design` → `/plan` → `/do` all exist as skills with bundled templates, in markdown.
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
| 4 | Build `/plan` skill from `/define` command, bundle DIP template | Not started |
| 5 | Build `/do` skill from `/build` command (no template) | Not started |
| 6 | Delete `.claude/commands/` and `.praxisity/templates/`; move review reports and stale references to `.plans/archive/` | Not started |
| 7 | Refresh skill-forge platform reference (frontmatter fields changed: `when_to_use` now supported, plus `model`, `effort`, `context: fork`) | Not started |
| 8 | Package as plugin (`.claude-plugin/plugin.json`, `skills/`, `agents/`), test install into a scratch project with `--plugin-dir` | Not started |
| 9 | Update README, CHARTER scope/milestones, CHANGELOG to 0.7.0; merge to main | Not started |

Build order for steps 2–5 follows the pattern set by the revised `/charter` (2026-09-22): inline PLANNING.md contract, sequential pre-flight with reasons, explicit gather invocation, template owns section guidance, pacing table using gather's four terms, copy-then-edit with a closed operations list, cancel paths reset PLANNING.md, offer-only post-save, completion gate, honest success message. Review each clone with prompt-engineer + critic + spot in Mode 2 (they hold checklists in agent memory from the charter review). No Mode 3.

Decisions made 2026-09-22: Domain Context is generic (three transferable questions, examples per field in the template comment); Stakeholders/Success Criteria/Constraints are checklist prompts; `TBD — revisit at [milestone]` is a marker distinct from N/A; source material conventionally lives in `.plans/references/`.

To verify in step 8: skill invoking `gather` via the Skill tool; `${CLAUDE_SKILL_DIR}` inside a plugin; `@CHARTER.md` import in CLAUDE.md actually loads; `$ARGUMENTS` inside a skill.

ID pattern for /plan (from the /describe and /design reviews): IDs assigned on approval, highest-ever-plus-one, never renumbered; removed items kept with the ID struck; coverage gates withhold the save option and name their exits; `MMM` for a parent document's number; one parent per child.

Reference convention (2026-09-23, canonical block in every template header and in skill-forge's praxisity-patterns): `REQ-F1 (short label)` for cross-document elements; `§7.4 Title` for sections; relative link with ID text for documents; `~~REQ-F3~~ (removed v0.2)` for removals.

## Skills Status

### Workflow Skills (user-invoked)
| Skill | Status | Notes |
|-------|--------|-------|
| /charter | Rewritten 2026-09-22, not yet live-tested | Pattern-setter. Live test on the Praxisity charter update (step 9) or a school project. |
| /describe | Built 2026-09-22, not yet live-tested | IDs assigned on approval, never renumbered; revise flow with struck rows; MUST→AC coverage gate |
| /design | Built 2026-09-23, not yet live-tested | Generic Architecture (context, approach, key choices); coverage gate with design-wide and deliberate-gap escapes; spec-diff on revise |
| /plan | Not started | From `/define` command |
| /do | Not started | From `/build` command |

### Support Skills (auto-invokable)
| Skill | Status | Notes |
|-------|--------|-------|
| /gather | Rewritten 2026-09-22 | Defaults instead of calibration questions; four pacing terms; TBD/N/A skip states; owns drafting rule |
| /skill-forge | Built | Platform reference stale (step 7) |
| /consult-team | Built | References `.plans/reviews/` paths — update in step 6 |
| /agent-authoring | Built | Plugin agents cannot use `memory:` — note in step 8 |

### Legacy Commands (delete in step 6)
spec, architect, define, build, new-project, deliver, breakdown, _prototype-charter

## Verified Platform Capabilities

See `reference_skill_platform_capabilities.md` in project memory. Re-checked 2026-09-22 against Claude Code 2.1.280 docs: plugins available, commands deprecated, agent teams still experimental, plugin agents cannot use memory.

## Next Steps

1. Step 4: `/plan` skill from `/define` command, bundle DIP template (210 lines). DIP links to both a design and a spec; needs the design's IDs and the spec's acceptance criteria.
2. Step 5: `/do` skill from `/build` command (execution skill, different phase structure, no template)
3. Live-test the chain on a real project once `/plan` exists

## Developer scratch pad (out of session notes)
- Consider adding an 'ex nihilo' pattern for the skill forge. Consider using this pattern to create new deep research skill. Consider adding that to the 'ex nihilo' pattern we used to create it.
- ISD/EdD integration: new theories may need dedicated agents and charter changes. Templates currently branch on Software / Public Health / Research domains — an Instructional Design domain will likely be needed. Keep domain sections generic during the rebuild so adding one later is cheap.