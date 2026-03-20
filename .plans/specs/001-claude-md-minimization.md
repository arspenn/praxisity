# Specification: SPEC-001 CLAUDE.md Minimization

## Metadata

| Field | Value |
|-------|-------|
| Spec ID | SPEC-001 |
| Title | CLAUDE.md Minimization |
| Status | Draft |
| Author | Andrew Robert Spenn |
| Created | 2026-03-20 |
| Last Updated | 2026-03-20 |
| Charter Reference | [CHARTER.md](../../CHARTER.md) |

### Related Documents

| Document | Relationship |
|----------|--------------|
| [Gloaguen et al., 2026 - "Evaluating AGENTS.md"](https://arxiv.org/pdf/2602.11988) | Informs |
| [claude.template.md](../../.praxisity/templates/claude.template.md) | Affected by |

---

## 1. Problem Statement

The current CLAUDE.md is ~300 lines containing architecture descriptions, file paths, template design principles, and conventions that are largely discoverable by the agent through normal codebase exploration. Research (Gloaguen et al., 2026 - "Evaluating AGENTS.md") demonstrates that comprehensive context files:

- Only marginally improve task success (+4% for developer-written, -3% for LLM-generated)
- Increase agent costs by 20%+ due to unnecessary exploration and reasoning
- Bias models toward mentioned patterns even when inappropriate
- Go stale as the codebase evolves, actively misleading agents

The framework also ships a `claude.template.md` for new projects, meaning this pattern propagates to every project initialized with Praxisity.

---

## 2. Goals and Objectives

### 2.1 Primary Goal

Reduce CLAUDE.md to only corrective, non-obvious content while ensuring no critical context is lost.

### 2.2 Objectives

| ID | Objective | Success Metric |
|----|-----------|----------------|
| OBJ-1 | Reduce CLAUDE.md to only content the agent cannot discover from the codebase | Line count reduction of 50%+ while retaining all non-obvious guidance |
| OBJ-2 | Ensure no information loss from removed content | All removed content is either discoverable from code or relocated to appropriate artifacts |
| OBJ-3 | Update `claude.template.md` to encourage minimal, corrective content | Template guides users toward behavioral corrections, not codebase descriptions |

---

## 3. Requirements

### 3.1 Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-F1 | Audit every section of current CLAUDE.md and classify each as: (a) non-obvious/corrective -- keep, (b) discoverable from code -- remove, (c) belongs elsewhere -- relocate | MUST | Core mechanism for minimization without information loss |
| REQ-F2 | Retain content that establishes mental model shifts the agent cannot infer (e.g., "this repo IS the framework, not a project using it") | MUST | Research shows corrective/non-obvious content is the only high-value type |
| REQ-F3 | Retain safety guardrails and workflow constraints that override default agent behavior | MUST | These are behavioral corrections -- exactly what agent MD files should contain |
| REQ-F4 | Relocate any removed content that isn't directly discoverable from code to appropriate project artifacts (README, inline comments, etc.) | MUST | Prevents information loss |
| REQ-F5 | Update `claude.template.md` to guide new projects toward minimal, corrective content rather than comprehensive descriptions | SHOULD | Prevents the anti-pattern from propagating to projects using Praxisity |
| REQ-F6 | Preserve PLANNING.md reference and dynamic state separation | MUST | This is a non-obvious behavioral instruction the agent needs |

### 3.2 Non-Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-N1 | Minimized CLAUDE.md should be readable in under 60 seconds | SHOULD | If it takes longer, it's too long -- same principle applies to agent token consumption |
| REQ-N2 | Changes must not break any existing slash command functionality | MUST | Commands may reference CLAUDE.md sections or assume certain content exists |

---

## 4. User Stories / Use Cases

### UC-1: Framework Developer Minimizes CLAUDE.md

**Actor:** Framework developer

**Preconditions:**
- Current CLAUDE.md exists with ~300 lines of content
- Research findings understood (paper + video context)

**Flow:**
1. Developer audits each CLAUDE.md section against REQ-F1 classification criteria
2. Developer removes content discoverable from codebase
3. Developer relocates content that belongs elsewhere
4. Developer verifies remaining content is corrective/non-obvious
5. Developer tests that slash commands still function correctly

**Postconditions:**
- CLAUDE.md contains only corrective, non-obvious content
- No information is permanently lost
- All commands work as before

---

### UC-2: New Project User Gets Minimal claude.template.md

**Actor:** Developer initializing a new Praxisity project

**Preconditions:**
- Praxisity framework installed
- User runs `/new-project`

**Flow:**
1. User runs `/new-project` which copies `claude.template.md`
2. Template guides user to add only behavioral corrections and non-obvious context
3. User fills in project-specific corrections as they discover agent misbehaviors over time

**Postconditions:**
- New project starts with a minimal CLAUDE.md
- Template discourages comprehensive codebase descriptions
- User understands the file is for corrections, not documentation

---

### UC-3: Agent Receives CLAUDE.md at Conversation Start

**Actor:** AI coding agent (Claude Code, sub-agents)

**Preconditions:**
- CLAUDE.md exists in project root
- Agent session starts (new conversation or sub-agent spawn)

**Flow:**
1. Agent receives CLAUDE.md content injected into context
2. Agent parses only corrective/non-obvious instructions
3. Agent proceeds to explore codebase normally for discoverable information
4. Agent behavior is steered away from known pitfalls without being biased toward irrelevant patterns

**Postconditions:**
- Agent context is not bloated with redundant information
- Agent is not biased toward mentioned-but-irrelevant patterns
- Agent spends fewer tokens on unnecessary exploration triggered by excessive context
- Agent still has all non-obvious guidance needed to work correctly in the project

---

## 5. Acceptance Criteria

| ID | Criterion | Validates |
|----|-----------|-----------|
| AC-1 | Given the minimized CLAUDE.md, when line count is measured, then it is at least 50% smaller than the current version | OBJ-1 |
| AC-2 | Given every removed section, when checked against the codebase, then the information is either discoverable from code or relocated to another artifact | REQ-F1, OBJ-2 |
| AC-3 | Given the minimized CLAUDE.md, when read by a developer, then every remaining line is either a behavioral correction, safety guardrail, or non-obvious context | REQ-F2, REQ-F3 |
| AC-4 | Given a new project initialized with `/new-project`, when the generated CLAUDE.md is reviewed, then it guides toward minimal corrective content | REQ-F5, OBJ-3 |
| AC-5 | Given the minimized CLAUDE.md, when all slash commands are invoked, then none fail due to missing context | REQ-N2 |
| AC-6 | Given an agent starting a session with the minimized CLAUDE.md, when it performs codebase tasks, then it is not biased toward patterns that are merely mentioned but not relevant to the task | UC-3 |

---

## 6. Constraints

### 6.1 Inherited from Charter

- Timeline: 4 weeks to MVP
- Technical: Claude Code compatibility
- Scope: Strict MVP discipline

### 6.2 Spec-Specific Constraints

- Must not break existing slash commands that may reference or depend on CLAUDE.md content
- Removal decisions must be validated -- no "just delete it and see what happens"
- The CLAUDE.md file itself must remain (it's a core framework concept), only its content is minimized

---

## 7. Dependencies

### 7.1 Depends On

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| Current CLAUDE.md | Resource | Available | The artifact being minimized |
| Research findings (Gloaguen et al.) | External | Available | Informs classification criteria |
| Existing slash commands | Resource | Available | Must verify no breakage |

### 7.2 Enables

| Dependent | Relationship |
|-----------|--------------|
| `claude.template.md` update | Template should reflect same minimization principles |
| Future progressive context expansion work | Clean minimal base to expand from |

---

## 8. Out of Scope

The following are explicitly NOT part of this specification:

- Progressive context expansion mechanisms (future work)
- Automated CLAUDE.md generation or `/init`-style tooling
- Changes to slash command logic (only verifying they still work)
- Changes to CHARTER.md or other framework documents beyond `claude.template.md`
- Benchmarking agent performance before/after (we trust the published research)

---

## 9. Open Questions

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| Q-1 | Do any slash commands parse CLAUDE.md content directly (vs. just benefiting from it being in context)? | Open | Need to grep commands for CLAUDE.md references before removing content |
| Q-2 | Should the "Important Files" section remain as a lightweight pointer, or is that also discoverable? | Open | Agent can find files, but pointers to non-obvious files like `praxisity-foundation-plan.md` may have value |
| Q-3 | Where should relocated content go -- README, inline comments, or somewhere else? | Open | Design phase decision |

---

## 10. References

- [Gloaguen et al., 2026 - "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?"](https://arxiv.org/pdf/2602.11988)
- Theo Browne video discussion on agent MD minimization (YouTube, March 2026)
- [CHARTER.md](../../CHARTER.md)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-03-20 | Andrew Robert Spenn | Initial draft |
