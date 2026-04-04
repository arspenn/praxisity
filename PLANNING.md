# PLANNING.md

## Active Context

**Last Command:** SPEC-004 /architect (Mode 3 team session)
**Status:** Design phase in progress — paused by user
**Date:** 2026-04-03
**Version:** 0.6.0

## Decisions Made This Session

1. **Q-3: Skills format** — commands migrate to `.claude/skills/[name]/SKILL.md`. Platform evidence: commands are legacy, not listed as extension point, `/init` creates skills.
2. **Q-4: Standards delivery** — inline mechanical standards (F1, F2, F5) at phase boundaries, shared file for F3 (judgment standard), per-skill for F4. Human-only authoring guide for UC-2. (Note: PE briefly reversed F3 to inline then back to shared — final position is shared file for F3.)
3. **Scope: 5 skills** — `/new-project` dropped (sunset candidate). Final list: `/describe`, `/charter`, `/design`, `/plan`, `/do`.
4. **Full renames:** spec→describe, architect→design, define→plan, build→do. Charter unchanged.
5. **Todoist:** Abstract to generic "task management service" in all skills.
6. **REQ-F1 permitted operations:** 6 allowed (placeholder sub, domain section removal, comment stripping, N/A marking, content population, table row adjustment). 4 not allowed (rewriting prose, adding sections, restructuring, paraphrasing).
7. **Bootstrapping approach:** Build `/describe` first, then use it to specify remaining skills.
8. **Templates:** Open question — designer recommends keeping in `.praxisity/templates/` (option C), user leaned toward bundling in skill directories. Unresolved at pause.

## In Progress at Pause

- **Designer** wrote DESIGN-005 v0.2 at `.plans/designs/005-command-rewrites.md` — needs DQ-4 (skill frontmatter) and template location decision to complete
- **Consistency-reviewer** produced full impact analysis of /new-project drop and renames — SPEC-004 and bug report need updates
- **PM** has pipeline plan at `.plans/reviews/SESSION-4-3-26/SPEC-004-pipeline-plan.md`
- **Q-5 agent prompt fixes** (4 agents: critic, designer, prompt-engineer, spot) — identified but not applied

## Documents Needing Updates Before Build

1. **SPEC-004** — remove /new-project from scope, update counts (26 bugs + 1 issue), adjust BUG-009 citation in REQ-F1 (lead with BUG-020), update status
2. **Bug report disposition table** — change BUG-001–009 to "Deferred: /new-project sunset"
3. **Design document** — resolve template location (DQ-5), skill frontmatter (DQ-4)

## Session Reviews

All reports in `.plans/reviews/SESSION-4-3-26/`:
- SPEC-004-project-manager-report.md (sequencing + pipeline)
- SPEC-004-pipeline-plan.md
- SPEC-004-consistency-reviewer-report.md
- SPEC-004-prompt-engineer-report.md
- DESIGN-005 at `.plans/designs/005-command-rewrites.md`

## Mode 3 Team: command-rewrite

**Status:** Paused. 5 teammates (designer, critic, prompt-engineer, project-manager, consistency-reviewer).

**UX feedback:** Teammate messages flood the terminal, pushing lead output out of frame. User couldn't read summaries or decision points. Captured in memory.

## Next Steps (When Resuming)

1. Resolve template location question (bundle vs `.praxisity/`)
2. Complete DESIGN-005 (skill frontmatter, template location)
3. Update SPEC-004 and bug report for /new-project removal and renames
4. Apply 4 agent prompt fixes (Q-5)
5. Build `/describe` skill (bootstrap)
6. Use `/describe` to specify remaining 4 skills
7. Build remaining skills: charter → design → plan → do