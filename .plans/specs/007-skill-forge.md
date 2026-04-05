# Specification: SPEC-007 Skill Forge Support Skill

## Metadata

| Field | Value |
|-------|-------|
| Spec ID | SPEC-007 |
| Title | Skill Forge Support Skill |
| Status | Draft |
| Author | Andrew Robert Spenn |
| Created | 2026-04-04 |
| Last Updated | 2026-04-04 |
| Charter Reference | [CHARTER.md](../../CHARTER.md) — Principles: Bootstrapping, Dual-use design, Reliability |
| Parent Spec | [SPEC-004](004-command-fixes-and-patterns.md) — supports skill rewrite process |

### Related Documents

| Document | Relationship |
|----------|--------------|
| [SPEC-004](004-command-fixes-and-patterns.md) | Parent — skill-forge supports the skill rewrite effort |
| [SPEC-006](006-gather-skill.md) | Sibling — first support skill built, informs skill-forge patterns |
| [DESIGN-005](../designs/005-command-rewrites.md) | Design context — DEC-1 (skills format), DEC-2 (standards delivery) |
| [Charter skill meta-review](../reviews/SESSION-4-4-26/charter-skill-meta-review.md) | Lessons learned from first live skill test |

---

## 1. Problem Statement

Building Claude Code skills requires knowledge of platform-specific conventions (frontmatter fields, directory structure, path variables), prompt engineering best practices (positive framing, observable gates, phase-boundary placement), and testing strategies (live testing, fresh-session validation, template integrity). This knowledge currently lives scattered across memory files, review reports, and session experience. Without a codified skill-building protocol, each new skill risks repeating mistakes that have already been identified and solved — wrong frontmatter fields, self-assessed gates, negative prohibition lists, missing update flows. A support skill that encodes this knowledge and auto-invokes during skill creation ensures every skill benefits from accumulated experience.

---

## 2. Goals and Objectives

### 2.1 Primary Goal

Codify the skill-building process as a reusable, auto-invokable support skill that ensures every new skill follows verified platform conventions and prompt engineering best practices.

### 2.2 Objectives

| ID | Objective | Success Metric |
|----|-----------|----------------|
| OBJ-1 | Encode verified platform knowledge (frontmatter fields, path variables, directory structure) so skill authors don't need to research it each time | New skills use correct frontmatter on first draft without consulting external documentation |
| OBJ-2 | Encode prompt engineering patterns (positive framing, observable gates, phase-boundary placement) from empirical testing | New skills avoid the failure patterns identified in testing and subsequent reviews |
| OBJ-3 | Support both general Claude Code skills and Praxisity-specific framework skills through a layered reference architecture | General guidance in SKILL.md, framework conventions in a reference file — the skill serves both audiences |
| OBJ-4 | Auto-invoke during skill creation to provide guidance without explicit invocation | Skill-forge loads automatically when the agent is building a new skill |

---

## 3. Requirements

### 3.1 Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-SF1 | The skill shall document all verified Claude Code skill frontmatter fields with their purpose, defaults, and supported values | MUST | Prevents use of unsupported fields (e.g., `when_to_use` — discovered invalid during SPEC-006 work) |
| REQ-SF2 | The skill shall document the standard skill directory structure (SKILL.md, templates/, references/) with guidance on when each component is needed | MUST | Self-contained skills require consistent structure |
| REQ-SF3 | The skill shall encode prompt engineering principles derived from empirical testing: positive framing, observable gates, phase-boundary placement, imperative sequencing | MUST | These patterns were validated through charter and gather skill development — they prevent specific failure modes |
| REQ-SF4 | The skill shall distinguish workflow skills (user-invoked, `disable-model-invocation: true`) from support skills (auto-invokable) and guide the author in choosing the right type | MUST | The two types have different frontmatter, invocation patterns, and design considerations |
| REQ-SF5 | The skill shall provide template bundling guidance: how to bundle, reference via `${CLAUDE_SKILL_DIR}`, implement copy-then-edit, and define permitted operations | MUST | Template handling is the most error-prone phase — the copy-then-edit pattern prevents non-deterministic output |
| REQ-SF6 | The skill shall provide a testing strategy: live testing, fresh-session testing, template integrity verification, dual-use clarity check | MUST | Reviews are necessary but not sufficient — live testing reveals interaction issues reviews miss |
| REQ-SF7 | The skill shall provide update-flow guidance: detecting existing output, presenting current content as drafts, preserving metadata dates | SHOULD | The update flow was underspecified in /charter and needed mid-run fixes |
| REQ-SF8 | The skill shall support a layered reference architecture: general guidance in SKILL.md, framework-specific patterns in a references/ file | MUST | Serves both general Claude Code users and Praxisity-specific development |
| REQ-SF9 | The skill shall auto-invoke via platform description-based context matching when the agent is creating or restructuring a skill | SHOULD | Reduces friction — the guidance loads when needed without explicit invocation |
| REQ-SF10 | The Praxisity reference file shall document behavioral standards (inline mechanical, skill-based judgment), PLANNING.md integration, memory-as-settings pattern, agent consultation, and dual-use output conventions | MUST | These are the framework patterns every Praxisity skill must follow |

---

## 4. Acceptance Criteria

| ID | Criterion | Validates |
|----|-----------|-----------|
| AC-SF1 | Given a developer creating a new skill, then the skill-forge provides correct frontmatter field names, defaults, and supported values — no unsupported fields recommended | REQ-SF1 |
| AC-SF2 | Given a new skill being created, then the output follows the standard directory structure (SKILL.md required, templates/ and references/ as needed) | REQ-SF2 |
| AC-SF3 | Given a skill draft, then it uses positive framing (verification checks, not prohibition lists), observable gates (not self-assessed), and phase-boundary placement for behavioral instructions | REQ-SF3 |
| AC-SF4 | Given a new skill, then the developer has explicitly chosen workflow or support type and the frontmatter reflects that choice correctly | REQ-SF4 |
| AC-SF5 | Given a skill that produces template-based output, then the skill includes copy-then-edit instructions with `${CLAUDE_SKILL_DIR}` paths, a closed list of permitted operations, and template integrity verification | REQ-SF5 |
| AC-SF6 | Given a completed skill, then it has been live-tested (not just reviewed) before being marked as validated | REQ-SF6 |
| AC-SF7 | Given a skill that can update existing output, then the update flow is explicitly defined with current-content-as-drafts and metadata preservation | REQ-SF7 |
| AC-SF8 | Given a Praxisity skill being built, then the developer has been directed to read the Praxisity patterns reference file before proceeding | REQ-SF8 |
| AC-SF9 | Given an agent building a new skill in a session, then skill-forge auto-invokes without explicit `/skill-forge` invocation | REQ-SF9 |
| AC-SF10 | Given a new Praxisity workflow skill, then it includes inline mechanical standards (F1, F2, F5), references /gather for gathering phases, defines per-skill success message, and integrates with PLANNING.md at 3 touchpoints | REQ-SF10 |

---

## 5. Constraints

- The main SKILL.md must be platform-general — no Praxisity-specific content in the core skill file. Framework conventions belong in the references file only.
- All platform claims in the skill must be verified empirically or marked as unverified with a testing note. Reference `reference_skill_platform_capabilities.md` for current verification status.
- The skill must not generate code or files itself — it guides the developer/agent through the process. The developer writes the skill file.
- The Praxisity patterns reference must stay in sync with DESIGN-005 and the charter as they evolve. When a framework pattern changes, this reference must be updated.

---

## 6. Out of Scope

- Skill performance measurement and benchmarking (the `skill-creator` plugin handles this)
- Agent definition file creation (the `/agent-authoring` skill handles this)
- Modifying or updating existing skills after creation — skill-forge guides initial creation and restructuring, not incremental edits
- Platform documentation — the skill encodes what's been verified, not a comprehensive Claude Code reference
- Enforcing patterns at runtime — skill-forge provides guidance at authoring time, not runtime validation

---

## 7. Open Questions

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| QSF-1 | Should skill-forge include a baseline testing pattern (run with and without skill)? | Deferred | Useful concept from the skill-creator plugin but outside MVP scope. Note prototype commit hash for manual comparison if needed. |
| QSF-2 | Should skill-forge auto-invoke reliably when agents are building skills, or is explicit `/skill-forge` invocation sufficient? | Open | Depends on platform auto-invocation behavior (QG-2 from SPEC-006 still untested). The description is crafted for auto-invocation but needs empirical validation. |
| QSF-3 | Should skill-forge include a description optimization workflow? | Deferred | The skill-creator plugin has an automated trigger-testing loop. Valuable but heavy infrastructure — defer until we have enough skills to warrant it. |
| QSF-4 | Should the Praxisity patterns reference replace the agent-authoring skill, or do they coexist? | Open | Agent-authoring covers agent definition files specifically. Skill-forge covers skills. They're adjacent but serve different artifact types. Likely coexist, but should cross-reference. |

---

## 8. Dependencies

### 8.1 Depends On

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| Claude Code skills platform | Platform | Available | |
| `${CLAUDE_SKILL_DIR}` path variable | Platform | Verified (2026-04-04) | |
| Supported frontmatter fields documentation | Platform | Verified | See reference_skill_platform_capabilities.md |
| Skill `description`-based auto-invocation | Platform | Needs empirical testing (QSF-2) | |

### 8.2 Enables

| Dependent | Relationship |
|-----------|--------------|
| All future Praxisity workflow skills (/describe, /design, /plan, /do) | Skill-forge guides their creation using verified patterns |
| All future support skills | Same guidance applies |
| Agent prompt revision (Q-5) | Praxisity patterns reference provides vocabulary and conventions for agent updates |
| DQ-3 (skill-standards development template) | The Praxisity patterns reference file fulfills this need — DQ-3 can be closed |

---

## 9. References

- [SPEC-004: Command Behavioral Fixes and Pattern Standards](004-command-fixes-and-patterns.md)
- [SPEC-006: Gather Support Skill](006-gather-skill.md)
- [DESIGN-005: Command Rewrites](../designs/005-command-rewrites.md)
- [Charter skill meta-review](../reviews/SESSION-4-4-26/charter-skill-meta-review.md)
- [skill-creator plugin](~/.claude/plugins/cache/claude-plugins-official/skill-creator/) — reviewed for concepts to incorporate

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-04-04 | Andrew Robert Spenn | Initial draft — gathered using /gather protocol. Incorporates lessons from /charter and /gather skill development, plus concepts from skill-creator plugin review. |

---