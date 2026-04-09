# PLANNING.md

## Active Context

**Last Command:** /architect for SPEC-008 (portable research prompt)
**Status:** Designing prompt architecture based on v0.2 prototype and PE review
**Date:** 2026-04-08
**Version:** 0.6.0

## Completed This Session

1. Mechanical updates to SPEC-004 and bug report (/new-project dropped, counts updated)
2. DESIGN-005 updated to v0.5 (templates bundled, renames, DEC-8 memory-as-settings)
3. SPEC-006 /gather skill — spec, prototype, 5-agent review, iterated
4. DESIGN-006 /gather skill design
5. /charter skill built — first workflow skill, pattern-setter
6. /charter run live — updated project charter v2 (7 principles, glossary, security)
7. Charter skill meta-review — 6 patterns for all future skills
8. CLAUDE.md overhauled — removed stale command names, minimized, points to charter
9. SPEC-007 /skill-forge — spec + prototype with Praxisity patterns reference
10. Reviewed skill-creator plugin — extracted 3 concepts (progressive loading, trigger mechanism, explain-the-why)

## Skills Status

### Support Skills (auto-invokable)
| Skill | Status | Spec | Notes |
|-------|--------|------|-------|
| /gather | Prototype iterated | SPEC-006 | Memory-as-settings not yet tested empirically |
| /skill-forge | Prototype | SPEC-007 | General + Praxisity patterns reference |
| /consult-team | Existing (pre-standards) | None | Needs audit against new standards |
| /agent-authoring | Existing (pre-standards) | None | Needs audit against new standards |

### Workflow Skills (user-invoked)
| Skill | Status | Spec | Notes |
|-------|--------|------|-------|
| /charter | Built + validated | SPEC-004 | Pattern-setter, live-tested, reviewed |
| /describe | Not started | SPEC-004 | Next workflow skill to build |
| /design | Not started | SPEC-004 | |
| /plan | Not started | SPEC-004 | |
| /do | Not started | SPEC-004 | |

### Prototype Commands (to sunset)
| Command | Status | Notes |
|---------|--------|-------|
| _prototype-charter | Renamed | Skill replacement validated |
| spec | Active (not yet replaced) | Will become /describe |
| architect | Active (not yet replaced) | Will become /design |
| define | Active (not yet replaced) | Will become /plan |
| build | Active (not yet replaced) | Will become /do |
| new-project | Active (sunset candidate) | |
| deliver | Active (deferred) | Separate spec needed |
| breakdown | Active (deferred) | Separate spec needed |

## Current Task

Audit existing skills (/consult-team, /agent-authoring) against the standards established by /skill-forge and /charter:
- Frontmatter (correct supported fields only)
- Directory structure
- Prompt engineering patterns (positive framing, observable gates, phase-boundary placement)
- Progressive loading model
- Dual-use clarity

## Verified Platform Capabilities

See `reference_skill_platform_capabilities.md` for full tracking. Key verifications this session:
- `${CLAUDE_SKILL_DIR}` — VERIFIED (resolved correctly during /charter run)
- `disable-model-invocation: true` — loaded correctly on /charter
- Auto-invocation via description — still needs fresh-session testing (QG-2/QSF-2)

## Next Steps

1. **Audit /consult-team and /agent-authoring** against skill-forge standards
2. **Build /describe skill** — use /skill-forge patterns, test with /gather
3. **Use /describe to specify remaining skills** (bootstrapping)
4. **Build remaining skills:** design → plan → do
5. **Deferred:** Q-5 agent prompt fixes (4 agents), /gather memory-as-settings testing, auto-invocation testing

## Developer scratch pad (out of session notes)
- Consider adding an 'ex nihilo' pattern for the skill forge. Consider using this pattern to create new deep research skill. Consider adding that to the 'ex nihilo' pattern we used to create it.