# PLANNING.md

## Active Context

**Last Command:** /define (DESIGN-002)
**Status:** In Progress
**Date:** 2026-03-20

## Current Task

Creating SPEC-002 (/build) and SPEC-003 (/deliver) — Week 3 execution & output commands.

Context: Extensive evaluation of superpowers, commit-commands, and skill-creator plugins completed. Decision made to finish MVP as commands first, incorporating key concepts (verification-before-completion, systematic execution, stop-when-blocked) directly into /build rather than creating separate skills. Plugin-to-skills migration deferred to post-MVP.

## Key Decisions This Session

- Plugin evaluation: superpowers (14 skills), commit-commands (3 commands), skill-creator (1 skill + 3 agents)
- Identified 3 future skills (TDD, systematic-debugging, verification-before-completion) for post-MVP
- Finish MVP commands first, iterate after end-to-end testing
- Commands will migrate to skills (disable-model-invocation: true) post-MVP
- Superpowers concepts absorbed into /build design, not as separate skills
- commit-commands plugin stays as-is (orthogonal utility)

## Active Artifacts

- `.plans/specs/001-claude-md-minimization.md` — SPEC-001 Complete
- `.plans/designs/001-claude-md-minimization.md` — DESIGN-001 Complete
- `.plans/prompts/001-claude-md-minimization.md` — DIP-001 Executed
- `.plans/specs/002-build-command.md` — SPEC-002 Draft
- `.plans/specs/003-deliver-command.md` — SPEC-003 Draft
- `.plans/designs/002-build-command.md` — DESIGN-002 Draft
- `.plans/designs/003-deliver-command.md` — DESIGN-003 Draft
- `.plans/prompts/002-build-command.md` — DIP-002 Ready
- `.plans/prompts/003-deliver-command.md` — DIP-003 Ready

## Next Steps

1. Execute DIP-002: implement /build command
2. Execute DIP-003: implement /deliver command and style module
3. End-to-end workflow test
4. Implement via /build (manually for the first one, then self-hosting)
5. End-to-end workflow test
