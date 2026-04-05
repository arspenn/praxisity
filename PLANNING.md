# PLANNING.md

## Active Context

**Last Command:** /charter (updating project charter)
**Status:** In progress — first live test of the /charter skill
**Date:** 2026-04-04
**Version:** 0.6.0

## Completed This Session

1. Mechanical updates to SPEC-004 and bug report (/new-project dropped, counts updated, BUG-009 citation adjusted)
2. DESIGN-005 updated to v0.5 (templates bundled, /new-project dropped, renames, DEC-8 memory-as-settings, stale references fixed)
3. SPEC-006 written for /gather skill — gathered using the gather skill prototype itself (bootstrapping)
4. /gather SKILL.md prototype built
5. 5-agent Mode 2 review of SPEC-006 + prototype (critic, PE, designer, consistency-reviewer, spot)
6. SKILL.md iterated based on review:
   - Positive framing (Before You Send) replaced negative prohibitions (elephants fix)
   - Observable drafting gate replaced self-assessed "sufficient context"
   - Explicit "fill in the rest" example added
   - Memory-as-settings implemented (REQ-G8/G9) with two fixed calibration questions
   - Removed unsupported `when_to_use` frontmatter field
7. DESIGN-006 written for /gather skill (5 design decisions, 3 components, 2 interfaces)
8. Consistency pass: 8 stale `when_to_use` references fixed across SPEC-006 and DESIGN-005
9. Discovered: `when_to_use` is not a supported skill frontmatter field — auto-invocation uses `description` field for context matching

## Key Decisions This Session

1. **Templates bundled in skill directories** — end-user templates with skills, development templates in `.praxisity/`
2. **Charter first** as pattern-setter (not /describe) — simplest, immediate utility, bootstrapping
3. **/new-project dropped** from SPEC-004 scope (sunset candidate) — 5 skills: describe, charter, design, plan, do
4. **/gather as support skill** — auto-invokable, not a shared file. Eliminates cross-references.
5. **Memory-as-settings pattern** — skills check project memory for preferences on every invocation, calibrate on first run. Framework-wide pattern.
6. **Positive framing over prohibitions** — "Before You Send" verification checks instead of "What You Must Not Do" lists
7. **Observable gates over self-assessment** — drafting requires pointing to specific prior input, not judgment calls
8. **Skill frontmatter** — `when_to_use` not supported; `description` drives auto-invocation. `disable-model-invocation` and `user-invocable` both default correctly for support skills.

## Documents Updated/Created

- SPEC-004 v0.3 — /new-project dropped, Q-3/Q-4 resolved, scope narrowed to 5 skills
- SPEC-006 v0.2 — gather skill spec (BUG-034 removed, REQ-G3 exception, QG-1 resolved)
- DESIGN-005 v0.5 — templates bundled, DEC-8 memory-as-settings, stale refs fixed, DATA-2 updated
- DESIGN-006 v0.1 — gather skill design (DEC-G1 through DEC-G5)
- /gather SKILL.md — iterated prototype with all review fixes applied
- Bug report disposition table — /new-project bugs deferred (26+1 in scope)
- Session reviews in `.plans/reviews/SESSION-4-4-26/`

## Next Steps

1. **Build `/charter` skill** — pattern-setter, first workflow skill
   - Create `.claude/skills/charter/` directory
   - Bundle charter template from `.praxisity/templates/`
   - Write SKILL.md applying inline standards (F1, F2, F5), per-skill F4
   - /gather auto-invokes during Gather phase (test QG-2 empirically)
   - Address BUG-010 through BUG-016
   - Set `disable-model-invocation: true` (workflow skill)
2. **Use `/charter` to update the project charter** — security principles, skills-first direction, drop Todoist mandate
3. **Build `/describe` skill** — then use it to specify remaining skills (bootstrapping)
4. **Build remaining skills:** design → plan → do
5. **Deferred:** Q-5 agent prompt fixes (4 agents), skill-standards development template