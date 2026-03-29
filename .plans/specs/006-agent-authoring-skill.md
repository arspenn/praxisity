# Specification: SPEC-006 Agent Authoring Skill

## Metadata

| Field | Value |
|-------|-------|
| Spec ID | SPEC-006 |
| Title | Agent Authoring Skill |
| Status | Draft |
| Author | Andrew Robert Spenn |
| Created | 2026-03-29 |
| Last Updated | 2026-03-29 |
| Charter Reference | [CHARTER.md](../../CHARTER.md) |

### Related Documents

| Document | Relationship |
|----------|--------------|
| [SPEC-005](005-agent-consultation-system.md) | Depends on — agents built by this skill follow the format SPEC-005 established |
| [DESIGN-004](../designs/004-agent-consultation-system.md) | Reference — DATA-1 defines the agent file schema |
| [Claude Code Sub-agents docs](https://code.claude.com/docs/en/sub-agents) | Reference — native subagent format and capabilities |

---

## 1. Problem Statement

During SPEC-005 implementation, we discovered that writing effective agent definition files requires balancing multiple concerns: native Claude Code subagent format compliance, dual-consumption quality (human + AI), prompt engineering best practices (positive scoping, avoiding elephants, calibrated output formats), proper frontmatter configuration, and integration with the Praxisity consultation system. This knowledge was gained through iterative creation of 9 agents, 3 rounds of prompt engineer review, and a cross-review cycle that surfaced systemic prompt issues. Without a skill to capture this process, each new agent will rediscover these lessons from scratch.

---

## 2. Goals and Objectives

### 2.1 Primary Goal

Provide a reusable Praxisity skill that guides the creation of new native Claude Code subagent files following the patterns, format, and prompt engineering principles established during SPEC-005.

### 2.2 Objectives

| ID | Objective | Success Metric |
|----|-----------|----------------|
| OBJ-1 | Codify the agent file format and frontmatter requirements discovered during SPEC-005 | New agents conform to DATA-1 schema without referencing the design document |
| OBJ-2 | Embed prompt engineering lessons (elephants avoidance, positive scoping, calibrated severity, dual consumption) into the authoring process | New agent files pass spot-check (haiku clarity gate) on first draft |
| OBJ-3 | Guide the agent through interactive persona development — identity, reasoning approach, output format, self-evaluation | Authored agents produce differentiated output when dispatched alongside existing roster |

---

## 3. Requirements

### 3.1 Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-F1 | The skill shall guide creation of agent files in native Claude Code subagent format (YAML frontmatter + markdown body) | MUST | Ensures platform compatibility and progressive loading |
| REQ-F2 | The skill shall prompt for each frontmatter field with defaults and explanations (name, description, category, tools, model, memory) | MUST | Prevents misconfiguration; distinguishes required Claude Code fields from Praxisity custom fields |
| REQ-F3 | The skill shall guide authoring of each body section (Identity, Reasoning Approach, Output Format, Self-Evaluation) with prompt engineering principles | MUST | Captures lessons from SPEC-005: positive scoping, avoid cross-agent priming, calibrated output taxonomies |
| REQ-F4 | The skill shall include a spot-check validation step — dispatch the authored agent on a test task and dispatch spot to evaluate the output for clarity | SHOULD | Built-in quality gate using the haiku clarity test |
| REQ-F5 | The skill shall register the new agent via `/agents` or note that session restart is needed for standalone dispatch | SHOULD | Addresses the registration discovery from SPEC-005 (team dispatch works mid-session, standalone does not) |
| REQ-F6 | The skill shall update `.claude/agents/README.md` roster when a new agent is added | SHOULD | Single source of truth for the agent index |

### 3.2 Non-Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-N1 | The skill shall be guidance, not control flow — consistent with SPEC-005 DEC-5 | MUST | Skills are loaded context; the main agent makes authoring decisions |
| REQ-N2 | The skill shall reference existing agents as examples without duplicating their content | MUST | Progressive loading — point to files, don't embed them |

---

## 4. User Stories / Use Cases

### UC-1: Developer Creates a New Domain Expert Agent

**Actor:** Developer extending the Praxisity agent roster

**Preconditions:**
- Agent authoring skill exists and is invocable
- `.claude/agents/` directory exists with existing agents as reference

**Flow:**
1. Developer invokes the agent authoring skill
2. Skill guides through frontmatter configuration (name, description, category, tools, model, memory)
3. Skill guides through persona authoring (Identity, Reasoning Approach, Output Format, Self-Evaluation) with prompt engineering principles embedded
4. Agent file written to `.claude/agents/`
5. Optional: spot-check dispatched on a test artifact to validate clarity
6. README.md updated with new agent entry
7. Developer advised to run `/agents` or restart for standalone dispatch registration

**Postconditions:**
- New agent file exists, conforms to format, passes clarity gate

---

## 5. Acceptance Criteria

| ID | Criterion | Validates |
|----|-----------|-----------|
| AC-1 | Given the skill is invoked, when the developer follows the guidance, then the resulting agent file conforms to DATA-1 schema from DESIGN-004 | REQ-F1 |
| AC-2 | Given the skill's prompt engineering guidance, when a new agent's "What you ignore" section is authored, then it uses positive scope boundaries without cross-agent references | REQ-F3 |
| AC-3 | Given the spot-check validation step, when the new agent is dispatched on a test task, then spot can parse the agent's output without confusion | REQ-F4 |

---

## 6. Constraints

### 6.1 Inherited from Charter

- Solo developer — skill must be usable without team coordination
- Claude Code compatibility required

### 6.2 Spec-Specific Constraints

- Must not duplicate agent file content inline — reference existing agents by path
- Must capture lessons from SPEC-005 session without requiring the user to read 18 review reports

---

## 7. Dependencies

### 7.1 Depends On

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| SPEC-005 agent file format | Spec | Implemented | DATA-1 schema is the target format |
| spot agent | Resource | Available | Used for clarity validation step |
| `.claude/agents/` directory | Resource | Available | Target location for new agents |

### 7.2 Enables

| Dependent | Relationship |
|-----------|--------------|
| Future agent roster expansion | Standardized authoring process for new agents |
| Framework rework | New domain-specific agents can be created as needed |

---

## 8. Out of Scope

- Modifying existing agents (that's manual editing informed by self-evaluation data)
- Agent dispatch or team management (that's the consult-team skill)
- Agent testing beyond the spot-check gate (real validation comes from use)

---

## 9. Open Questions

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| Q-1 | Should the skill auto-dispatch the prompt-engineer agent to review the new agent file? | Open | Could be valuable but adds complexity and token cost |
| Q-2 | Should there be a "quick agent" mode that skips the full guided flow for experienced users? | Deferred | Wait for usage data on how often new agents are created |

---

## 10. References

- [SPEC-005: Agent Consultation System](005-agent-consultation-system.md)
- [DESIGN-004: Agent Consultation System Design](../designs/004-agent-consultation-system.md)
- [SPEC-005 Prompt Engineer Report](../reviews/SPEC-005-prompt-engineer-report.md) — 9 prompt engineering findings
- [SPEC-005 Prompt Engineer Elephants Experiment](../reviews/SPEC-005-prompt-engineer-elephants-experiment.md)
- [SPEC-005 Lead Review](../reviews/SPEC-005-lead-review.md) — synthesized lessons
- [Claude Code Sub-agents docs](https://code.claude.com/docs/en/sub-agents)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-03-29 | Andrew Robert Spenn | Initial draft from SPEC-005 session learnings |

---
