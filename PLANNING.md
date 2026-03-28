# PLANNING.md

## Active Context

**Last Command:** brainstorming / spec authoring
**Status:** In Progress — SPEC-005: Agent Consultation System (draft written, pending review)
**Date:** 2026-03-28
**Version:** 0.5.0

## Active Artifacts

- **SPEC-005**: `.plans/specs/005-agent-consultation-system.md` — draft, pending spec review
- **SPEC-004**: `.plans/specs/004-command-fixes-and-patterns.md` — approved, paused (resumes after SPEC-005 implementation)

## Session Notes

- SPEC-005 designed via brainstorming session — 7-agent consultation system with 3-tier progressive loading
- Bootstrapping approach: build agents to help write the framework rework spec, then formalize as a feature
- Key design decisions: skills are loaded context not control flow; agent files immutable at dispatch; persistence via documents not terminal sessions

## Next Steps

1. Spec review loop for SPEC-005 — dispatch reviewer, iterate if needed
2. User review of SPEC-005
3. `/architect` — design SPEC-005
4. Implement SPEC-005 (agent files, consult-team skill, directory structure, Tier 1 pointers)
5. Use SPEC-005 agents to work on framework rework spec
6. Resume SPEC-004 — `/architect` and implementation