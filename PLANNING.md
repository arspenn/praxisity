# PLANNING.md

## Active Context

**Branch:** `consolidate` (off main at 758f13a — if this goes badly, delete the branch and start over)
**Last Command:** none — session restarted after 4-month gap, framework re-evaluated
**Status:** Consolidation plan agreed, work not yet started
**Date:** 2026-09-22
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
| 2 | Build `/describe` skill from `/spec` command, bundle spec template | Not started |
| 3 | Build `/design` skill from `/architect` command, bundle design template | Not started |
| 4 | Build `/plan` skill from `/define` command, bundle DIP template | Not started |
| 5 | Build `/do` skill from `/build` command (no template) | Not started |
| 6 | Delete `.claude/commands/` and `.praxisity/templates/`; move review reports and stale references to `.plans/archive/` | Not started |
| 7 | Refresh skill-forge platform reference (frontmatter fields changed: `when_to_use` now supported, plus `model`, `effort`, `context: fork`) | Not started |
| 8 | Package as plugin (`.claude-plugin/plugin.json`, `skills/`, `agents/`), test install into a scratch project with `--plugin-dir` | Not started |
| 9 | Update README, CHARTER scope/milestones, CHANGELOG to 0.7.0; merge to main | Not started |

Build order for steps 2–5 follows the pattern set by `/charter`: sequential pre-flight with PLANNING.md gate, gather via `/gather`, copy-then-edit template, completion gate, per-skill success message. Use at most one or two Mode 2 agent reviews per skill (prompt-engineer and spot are the cheap defaults). No Mode 3.

## Skills Status

### Workflow Skills (user-invoked)
| Skill | Status | Notes |
|-------|--------|-------|
| /charter | Built + validated | Pattern-setter |
| /describe | Not started | From `/spec` command |
| /design | Not started | From `/architect` command |
| /plan | Not started | From `/define` command |
| /do | Not started | From `/build` command |

### Support Skills (auto-invokable)
| Skill | Status | Notes |
|-------|--------|-------|
| /gather | Built | Memory-as-settings still untested empirically |
| /skill-forge | Built | Platform reference stale (step 7) |
| /consult-team | Built | References `.plans/reviews/` paths — update in step 6 |
| /agent-authoring | Built | Plugin agents cannot use `memory:` — note in step 8 |

### Legacy Commands (delete in step 6)
spec, architect, define, build, new-project, deliver, breakdown, _prototype-charter

## Verified Platform Capabilities

See `reference_skill_platform_capabilities.md` in project memory. Re-checked 2026-09-22 against Claude Code 2.1.280 docs: plugins available, commands deprecated, agent teams still experimental, plugin agents cannot use memory.

## Next Steps

1. Start step 2: `/describe` skill
2. Live-test it by writing a real spec (a school project or the plugin packaging itself)

## Developer scratch pad (out of session notes)
- Consider adding an 'ex nihilo' pattern for the skill forge. Consider using this pattern to create new deep research skill. Consider adding that to the 'ex nihilo' pattern we used to create it.
- ISD/EdD integration: new theories may need dedicated agents and charter changes. Templates currently branch on Software / Public Health / Research domains — an Instructional Design domain will likely be needed. Keep domain sections generic during the rebuild so adding one later is cheap.