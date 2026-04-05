# Specification: SPEC-006 Gather Support Skill

## Metadata

| Field | Value |
|-------|-------|
| Spec ID | SPEC-006 |
| Title | Gather Support Skill |
| Status | Draft |
| Author | Andrew Robert Spenn |
| Created | 2026-04-04 |
| Last Updated | 2026-04-04 |
| Charter Reference | [CHARTER.md](../../CHARTER.md) — Principles: Minimal cognitive overhead, Bootstrapping |
| Parent Spec | [SPEC-004](004-command-fixes-and-patterns.md) — REQ-F3 (gathering protocol) |

### Related Documents

| Document | Relationship |
|----------|--------------|
| [SPEC-004](004-command-fixes-and-patterns.md) | Parent — this skill implements REQ-F3 |
| [DESIGN-005](../designs/005-command-rewrites.md) | Design context — COMP-5 (Gathering Protocol) |
| [Bug Report](../references/new-project-bug-report.md) | Evidence base — BUG-012, BUG-018 (BUG-034 is /do execution batching, not user gathering — out of scope) |

---

## 1. Problem Statement

The Praxisity framework requires structured input gathering across multiple sections in workflow skills (/charter, /describe, /design, /plan) and in general development sessions. Testing at v0.5.0 revealed that agents consistently batch gathering — presenting all sections at once or drafting entire documents without per-section user confirmation (BUG-012, BUG-018). Inline constraints ("one section at a time") were already present in prototype commands and were defeated. The gathering protocol needs to be codified as a reusable, auto-invokable support skill that provides operational context beyond what a terse inline rule can deliver.

---

## 2. Goals and Objectives

### 2.1 Primary Goal

Codify the one-at-a-time gathering protocol as a standalone support skill that auto-invokes whenever structured input is needed, providing immediate benefit across all development sessions.

### 2.2 Objectives

| ID | Objective | Success Metric |
|----|-----------|----------------|
| OBJ-1 | Prevent batched gathering across all workflow skills | No instances of multiple sections presented in a single message during gathering phases |
| OBJ-2 | Support draft-for-approval when context is sufficient | Agent presents drafts with clear approval prompts; user retains per-section control |
| OBJ-3 | Auto-invoke reliably during workflow skill execution and general sessions | Skill loads without explicit cross-references from consuming skills |
| OBJ-4 | Handle edge cases (sub-categories, skip requests, "fill in the rest") | Agent responds correctly to each without breaking the one-at-a-time protocol |

---

## 3. Requirements

### 3.1 Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-G1 | The skill shall prompt one section at a time, waiting for the user's explicit response before presenting the next section | MUST | Core protocol — BUG-018 root failure was batching all sections |
| REQ-G2 | When the agent has sufficient context, it may present a draft for approval rather than prompting from scratch, but must still pause between sections | MUST | Balances UX for experienced users with the one-at-a-time constraint |
| REQ-G3 | The skill shall not draft content for sections the user has not yet been prompted for, unless the user explicitly requests it (see REQ-G5) | MUST | Prevents the "draft everything then present for batch approval" pattern (BUG-018). The explicit user request exception (REQ-G5) is the only override. |
| REQ-G4 | When a section has sub-categories, each sub-category shall be prompted individually with the option to skip | MUST | BUG-012 — constraints were combined into a single prompt instead of per-category |
| REQ-G5 | When the user requests "fill in the rest" or similar, the skill may draft remaining sections but shall still present each individually for confirmation | SHOULD | Flexibility for experienced users without abandoning the protocol |
| REQ-G6 | The skill shall auto-invoke via platform `description`-based context matching during structured gathering without requiring explicit cross-references from workflow skills | MUST | Eliminates the cross-reference reliability problem; gathering protocol loads automatically |
| REQ-G7 | The skill shall be usable in any session context, not only during workflow skill execution | SHOULD | Bootstrapping benefit — every development session gets the gathering protocol |
| REQ-G8 | On every invocation, the skill shall first check agent memory for gathering preferences. If preferences exist, load and apply them silently. If not, run calibration as a natural part of the gathering flow before proceeding | MUST | Memory is the settings store. First invocation calibrates; subsequent invocations load. This fires naturally during /charter (the framework's true entry point) |
| REQ-G9 | Calibration and preference storage shall use the Claude Code agent SDK main project memory system, writing to MEMORY.md per the official documentation | MUST | Uses the platform's memory system, not a custom implementation. Project memory is loaded into every session — any agent, subagent, or skill invocation sees preferences automatically |

---

## 4. Acceptance Criteria

| ID | Criterion | Validates |
|----|-----------|-----------|
| AC-G1 | Given a gathering flow with N sections, then each section is presented in a separate message and section N+1 does not appear until the user responds to section N | REQ-G1 |
| AC-G2 | Given sufficient context for a section, when the agent drafts it, then the draft is presented with an explicit approval prompt and the agent waits for response | REQ-G2 |
| AC-G3 | Given a section with sub-categories (e.g., constraint types), then each sub-category is prompted individually with the option to skip | REQ-G4 |
| AC-G4 | Given the first invocation in a project (no gathering preferences in memory), then the skill runs calibration questions as part of the natural gathering flow and stores results to main project memory | REQ-G8, REQ-G9 |
| AC-G5 | Given a subsequent invocation (preferences exist in memory), then the skill loads preferences silently and applies them without re-prompting | REQ-G8, REQ-G9 |
| AC-G6 | Given the user says "fill in the rest," then the agent drafts remaining sections but presents each individually for confirmation | REQ-G5 |
| AC-G7 | Given the skill is invoked during a workflow skill execution (e.g., /charter), then it auto-invokes via platform `description`-based context matching without explicit cross-references | REQ-G6 |
| AC-G8 | Given the skill is invoked outside of a workflow skill (e.g., during a general development session), then the gathering protocol still applies when structured multi-section input is needed | REQ-G7 |

---

## 5. Constraints

- The skill must use the Claude Code agent SDK memory system (main project memory, MEMORY.md) — no custom persistence backends or framework-specific memory implementations
- Calibration must feel natural, not like a configuration wizard — questions should be conversational and brief
- The skill must not assume it is being invoked from a specific workflow skill — it works in any gathering context
- The skill must not make any file changes — it only governs the conversation pattern for gathering. File operations (template copying, editing) belong to the consuming workflow skill
- Stored preferences must use the standard memory frontmatter format so any agent or subagent can parse them reliably

---

## 6. Dependencies

### 6.1 Depends On

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| Claude Code agent SDK memory system | Platform | Available | Main project memory, MEMORY.md |
| Skill `description`-based auto-invocation | Platform | Available | Platform matches conversation context against skill descriptions; needs empirical testing (QG-2) |
| MEMORY.md project memory (official format) | Platform | Available | Standard frontmatter + markdown |

### 6.2 Enables

| Dependent | Relationship |
|-----------|--------------|
| `/charter` skill | First consumer — calibration happens here |
| `/describe`, `/design`, `/plan` skills | All gathering phases use this protocol |
| Future skills with structured gathering | Any skill needing multi-section user input |
| Per-project settings pattern | Establishes memory-as-settings for other skills to follow |

---

## 7. Out of Scope

- Template handling (REQ-F1 copy-then-edit) — separate concern, inline in each workflow skill's Generate phase
- What sections to gather — defined by the consuming workflow skill, not by this skill
- File creation or modification of any kind — this skill governs conversation, not output
- User authentication or permissions — the skill trusts the invoking context
- Advanced preference UI (sliders, config files, settings panels) — preferences live in agent memory, period
- Enforcing preferences across other agents' behavior — the skill stores preferences; other skills read them if they choose to

---

## 8. Open Questions

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| QG-1 | What specific calibration questions should be asked on first run? | Resolved | Two fixed binary questions: (1) gathering-style: guided vs draft-first, (2) prompt-detail: detailed vs brief. See DESIGN-006 DEC-G4. |
| QG-2 | How does `description`-based auto-invocation interact with a workflow skill already in progress? | Open | Need empirical testing — does the platform layer the gather skill's instructions on top of the active skill, or does it require explicit invocation? Fallback: workflow skills reference /gather explicitly |
| QG-3 | Should preferences be stored in the main agent's memory or in a gather-specific agent memory path? | Resolved | Main project memory (`~/.claude/projects/[path]/memory/`), written to MEMORY.md per the official Claude Code memory tool documentation. Project memory is loaded into every session — any agent, subagent, or skill invocation sees preferences automatically. No separate skill-specific memory paths. |
| QG-4 | Can other skills read gathering preferences to adapt their own behavior? | Open | E.g., /charter might adjust how many examples it shows based on the user experience level stored by /gather. This is the "shared settings via memory" pattern — validate during /charter build |

---

## 9. References

- [SPEC-004: Command Behavioral Fixes and Pattern Standards](004-command-fixes-and-patterns.md)
- [DESIGN-005: Command Rewrites](../designs/005-command-rewrites.md) — COMP-5
- [Bug Report: v0.5.0 end-to-end test results](../references/new-project-bug-report.md) — BUG-012, BUG-018
- [Claude Code Memory Tool Documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-04-04 | Andrew Robert Spenn | Initial draft — gathered using /gather skill prototype (bootstrapping) |
| 0.2 | 2026-04-04 | Andrew Robert Spenn | Post-review fixes: removed BUG-034 (out of scope — /do execution, not user gathering); added exception clause to REQ-G3 for REQ-G5 override; added AC-G8 for REQ-G7 |

---

## Framework Pattern: Memory-as-Settings

**Pattern identified during this spec:** Skills can use the agent memory system as a per-project settings store. Any skill needing configuration that varies between projects can: (1) check memory on invocation, (2) calibrate on first run, (3) store structured preferences, (4) load and apply on subsequent runs. This pattern should be documented in the skill-standards development template (`.praxisity/templates/skill-standards.template.md`) for UC-2.