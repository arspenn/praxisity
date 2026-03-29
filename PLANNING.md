# PLANNING.md

## Active Context

**Last Command:** /build
**Status:** In Progress — executing DIP-007: Tier 1 Command Pointers
**Date:** 2026-03-28
**Version:** 0.5.0

## Active Artifacts

- **DIP-004**: `.plans/prompts/004-templates-and-extensions.md` — ready for build
- **DIP-005**: `.plans/prompts/005-agent-definition-files.md` — ready for build (depends on DIP-004)
- **DIP-006**: `.plans/prompts/006-consult-team-skill.md` — ready for build (depends on DIP-004, DIP-005)
- **DIP-007**: `.plans/prompts/007-tier1-command-pointers.md` — ready for build (depends on DIP-006)
- **DESIGN-004**: `.plans/designs/004-agent-consultation-system.md` — approved
- **SPEC-005**: `.plans/specs/005-agent-consultation-system.md` — approved
- **SPEC-004**: `.plans/specs/004-command-fixes-and-patterns.md` — approved, paused (resumes after SPEC-005 implementation)

## Session Notes

- SPEC-005 designed via brainstorming session — 8-agent consultation system with 3-tier progressive loading
- Bootstrapping approach: build agents to help write the framework rework spec, then formalize as a feature
- Key design decisions: skills are loaded context not control flow; agent files immutable at dispatch; persistence via documents not terminal sessions

## Next Steps

1. `/build` DIP-004 — templates, extensions, directory structure
2. `/build` DIP-005 — 8 agent definition files
3. `/build` DIP-006 — consult-team skill
4. `/build` DIP-007 — Tier 1 command pointers
5. Bootstrapping test — use agents on real framework rework spec work
6. Resume SPEC-004 — `/architect` and implementation