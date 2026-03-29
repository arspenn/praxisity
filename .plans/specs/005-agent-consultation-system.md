# Specification: SPEC-005 Agent Consultation System

## Metadata

| Field | Value |
|-------|-------|
| Spec ID | SPEC-005 |
| Title | Agent Consultation System |
| Status | Draft |
| Author | Andrew Robert Spenn |
| Created | 2026-03-28 |
| Last Updated | 2026-03-28 |
| Charter Reference | [CHARTER.md](../../CHARTER.md) — Principles: Dual-use design, Minimal cognitive overhead |

### Related Documents

| Document | Relationship |
|----------|--------------|
| [SPEC-004: Command Behavioral Fixes](004-command-fixes-and-patterns.md) | Related to — SPEC-004 paused; resumes after SPEC-005 implementation |
| [D4C Bug Report: ISSUE-004](../references/d4c-praxisity-bug-report.md) | Depends on — identified need for persistent agent teams across DIPs |
| [Superpowers subagent-driven-development](https://github.com/anthropics/claude-code-plugins) | Reference — pattern source for agent dispatch (not a dependency) |

---

## 1. Problem Statement

Praxisity's workflow commands operate through a single agent session, which means specifications, designs, and other thinking-phase artifacts reflect only one perspective at a time. The v0.5.0 end-to-end test (46 bugs) and the D4C-ARS project (ISSUE-004) demonstrated that blind spots — missed requirements, unstated assumptions, scope creep, prompt quality issues — consistently survive single-agent review. The D4C project's ad-hoc 3-agent review team (Evidence Auditor, Claim Reviewer, Construct Analyst) caught issues that the primary agent missed, but the team was managed through improvised DIP notes ("Do NOT shut down the agent team") because the framework has no concept of agent teams.

Separately, Praxisity's skills currently embed all behavioral guidance inline, which bloats agent context with instructions irrelevant to the current task. The theory-of-change skill duplicates ~90 lines of reference-verification and claim-validation methodology rather than loading it on demand. This "everything in context" approach conflicts with the framework's goal of minimal cognitive overhead and creates "don't think about elephants" problems where loaded-but-irrelevant instructions interfere with the agent's focus.

This spec addresses both problems by defining a structured agent consultation system with progressive loading — specialized agent perspectives available on demand without bloating the default context of any command.

---

## 2. Goals and Objectives

### 2.1 Primary Goal

Provide Praxisity with a reusable, progressively-loaded agent consultation system that enables multi-perspective review during thinking-phase commands without bloating the default context of any session.

### 2.2 Objectives

| ID | Objective | Success Metric |
|----|-----------|----------------|
| OBJ-1 | Define a standardized agent definition format that separates stable persona from per-invocation context | Agent files are immutable at dispatch time; customization is appended, never edited into the file |
| OBJ-2 | Create a consultation skill that the main agent can load on demand for team dispatch guidance | Skill can be invoked manually or referenced by thinking commands without being loaded by default |
| OBJ-3 | Implement a 3-tier progressive loading architecture (pointers, skill, agent files) that keeps irrelevant content out of context | A simple `/build` session loads zero agent content; a `/spec` session with team input loads only the agents dispatched |
| OBJ-4 | Build the initial agent roster and use it to stress-test the framework rework spec (bootstrapping) | Agents produce usable feedback on real spec work and generate self-evaluation data for prompt refinement |

---

## 3. Requirements

### 3.1 Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-F1 | Each agent shall be defined as a native Claude Code subagent file (YAML frontmatter + markdown body) in `.claude/agents/`, with required Claude Code fields (name, description), optional Claude Code fields (tools, model, memory), required Praxisity field (category — used by consult-team skill for grouping, ignored by Claude Code), and a markdown body containing Identity, Reasoning Approach, Output Format, and Self-Evaluation sections | MUST | Native format gives platform capabilities for free (tool restrictions, persistent memory, @-mention, --agent mode); enables progressive loading — only dispatched agents enter context |
| REQ-F2 | Agent files shall be immutable at dispatch time; per-invocation customization shall be appended as a context block following a standardized template, never edited into the agent file | MUST | Prevents prompt drift across sessions; separates stable persona from variable context |
| REQ-F3 | A `consult-team` skill shall provide the main agent with guidance on: available agents (index from frontmatter), when to use single consult vs. team session, how to manage parallel agent sessions, how to synthesize feedback, and what to preserve from sessions | MUST | Without this loaded guidance, the user must manually instruct the agent on team management every session |
| REQ-F4 | The initial agent roster shall include 8 agents across 4 categories: Evaluative (Critic, Skeptic), Perspective (User Advocate, Stakeholder), Structural (Designer, Project Manager), Meta (Prompt Engineer, Fresh Eyes Reviewer) | MUST | These perspectives cover the range needed for spec/design review; roster designed during brainstorming and expanded during design when cross-document consistency review proved its value |
| REQ-F5 | Thinking commands (`/spec`, `/architect`, `/charter`) shall include a Tier 1 pointer (~4 lines: heading + guidance) referencing the consult-team skill and listing natural-fit agents for that command's phase | SHOULD | Reminds the main agent that consultation is available without loading the full skill; reduces user burden of remembering to invoke |
| REQ-F6 | Doing commands (`/build`, `/deliver`, `/breakdown`, `/define`) shall not include agent consultation pointers by default | SHOULD | Keeps doing-command context lean; user can still manually invoke the skill when needed (e.g., when a DIP involves writing skills) |
| REQ-F7 | Each agent's output shall include a self-evaluation section covering: what was useful about their perspective, what they struggled with, and suggestions for prompt improvement | SHOULD | Generates improvement data as a byproduct of normal work; enables iterative refinement without separate overhead |
| REQ-F8 | Every dispatched agent (all modes) shall write its own report directly to `.plans/reviews/` including findings, instructions received, and self-evaluation — independent of what it returns to the main agent | MUST | Agent-authored reports are the source of truth; prevents telephone-game summarization loss; enables verification of what the agent actually found vs. what the main agent reported; persists beyond context window compression |
| REQ-F9 | Agent definitions shall use Claude Code's native `memory: project` feature for persistent cross-session knowledge accumulation, stored in `.claude/agent-memory/<name>/` | COULD | Platform-native Tier 3 — agents accumulate knowledge across sessions without custom infrastructure; starts empty and grows through use |
| REQ-F10 | The `consult-team` skill name and description shall be clearly differentiated from Superpowers' `dispatching-parallel-agents` skill to prevent main agent confusion when both are installed | MUST | Different purpose (multi-perspective on same topic vs. independent parallel tasks); ambiguous naming would cause incorrect skill selection |
| REQ-F11 | The agent consultation system shall support three dispatch modes: single expert consult (Mode 1, one subagent via Agent tool, guided by Tier 1 command pointers), parallel perspectives (Mode 2, multiple subagents via Agent tool, guided by consult-team skill), and collaborative team (Mode 3, persistent teammates via TeamCreate with shared task list, direct messaging, and direct user interaction, guided by consult-team skill with decision gate between Mode 2 and Mode 3) | MUST | Each mode serves different needs: Mode 1 for quick checks (snapshot), Mode 2 for multi-perspective review (snapshot), Mode 3 for sustained work where context accumulation and delta-awareness matter |
| REQ-F12 | Mode 3 collaborative teammates shall be full parallel sessions that write their own reports directly, maintain their own perspective, and can interact with the user either via main agent relay or direct terminal access | MUST | Teammates are independent professionals, not subordinate funnels; self-authored reports capture nuance lost in summarization; direct user access enables in-depth interaction when relay is insufficient |

### 3.2 Non-Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-N1 | All agent files and skill content shall be optimized for dual consumption: human-readable AND effective as AI prompts | MUST | Every file in Praxisity is both prompt output and prompt input; quality matters for both readability and promptability |
| REQ-N2 | The consult-team skill shall be guidance and context, not control flow — the main agent always coordinates; the skill provides knowledge of how to coordinate | MUST | Skills are loaded instructions, not functions; the main agent makes all dispatch and synthesis decisions |
| REQ-N3 | Agent consultation shall not be required by any command — it is always optional, invocable by user choice or command suggestion | MUST | Preserves the framework's flexibility; a quick task shouldn't be gated on agent review |
| REQ-N4 | Team composition for multi-session work shall be documented in planning artifacts (specs, designs, DIPs) so teams can be reconstituted across terminal sessions | SHOULD | Terminal sessions can end unexpectedly; persistence lives in documents, not connections |

---

## 4. User Stories / Use Cases

### UC-1: Multi-Perspective Spec Review via Command Suggestion

**Actor:** Developer running `/spec` for a new feature

**Preconditions:**
- Thinking command includes Tier 1 pointer to consult-team skill
- Agent definition files exist in `.claude/agents/`

**Flow:**
1. Developer runs `/spec` and completes the gathering phase
2. Before finalizing, the main agent notes the Tier 1 pointer suggesting agent consultation
3. Main agent asks the developer if they'd like multi-perspective review before finalizing
4. Developer agrees; main agent invokes the consult-team skill (Tier 2 loads)
5. Main agent reads the agent index, selects relevant agents (e.g., Critic, User Advocate, Skeptic)
6. Main agent loads each selected agent's file and appends a context block with the current spec draft
7. Agents are dispatched in parallel; each returns structured findings and self-evaluation
8. Main agent synthesizes the feedback, presents areas of agreement and disagreement to the developer
9. Developer decides which feedback to incorporate
10. Agent outputs and self-evaluations are saved to `.plans/reviews/`

**Postconditions:**
- Spec reflects multi-perspective input before moving to design phase
- Agent self-evaluations are persisted for future prompt refinement

**Alternative Flows:**
- Developer declines consultation at step 3 — command proceeds normally with no agent content loaded
- An agent returns BLOCKED or unhelpful output — main agent notes this and proceeds with remaining agents

---

### UC-2: Manual Team Invocation During Build

**Actor:** Developer running `/build` on a DIP that involves writing a skill

**Preconditions:**
- `/build` has no Tier 1 pointer (doing command)
- Developer recognizes the task would benefit from perspectives (e.g., Prompt Engineer review)

**Flow:**
1. Developer is mid-build and realizes the skill content being written would benefit from review
2. Developer tells the main agent to invoke the consult-team skill
3. Main agent loads the skill (Tier 2), reads agent index
4. Developer requests specific agents (e.g., "get the Prompt Engineer and Critic to look at this")
5. Main agent dispatches the requested agents with current work-in-progress as context
6. Feedback is returned, developer incorporates what's useful, build continues

**Postconditions:**
- Build benefits from consultation without the command needing built-in agent support

---

### UC-3: Team Reconstitution Across Sessions

**Actor:** Developer resuming multi-session work documented in a DIP

**Preconditions:**
- Previous session's DIP or spec includes team composition notes (which agents, what they found, open concerns)
- Session report from previous consultation exists in `.plans/reviews/`

**Flow:**
1. Developer starts new session, runs command that loads relevant DIP
2. DIP references the team composition and previous session report
3. Developer invokes consult-team skill and requests the same team
4. Main agent dispatches agents with context including previous session's findings
5. Agents build on prior work rather than starting from scratch

**Postconditions:**
- Continuity of perspective across terminal sessions via document persistence

---

## 5. Acceptance Criteria

| ID | Criterion | Validates |
|----|-----------|-----------|
| AC-1 | Given an agent definition file in `.claude/agents/`, when inspected, then it uses native Claude Code subagent format with YAML frontmatter containing required Claude Code fields (name, description), applicable optional Claude Code fields (tools, model, memory), required Praxisity field (category), and a markdown body containing Identity, Reasoning Approach, Output Format, and Self-Evaluation sections | REQ-F1 |
| AC-2 | Given a dispatched agent, when the dispatch prompt is constructed, then the agent file content is included verbatim and the context block is appended after it — the agent file is not modified | REQ-F2 |
| AC-3 | Given the consult-team skill is invoked, when loaded, then it provides an agent index (names, categories, purposes), dispatch guidance for single consult and team sessions, session management instructions, and output preservation instructions | REQ-F3 |
| AC-4 | Given the `.claude/agents/` directory, when listed, then it contains exactly 8 agent files: critic.md, skeptic.md, user-advocate.md, stakeholder.md, designer.md, project-manager.md, prompt-engineer.md, fresh-eyes-reviewer.md | REQ-F4 |
| AC-5 | Given a thinking command (`/spec`, `/architect`, `/charter`), when its command file is inspected, then it contains a Tier 1 pointer of ~4 lines (heading + guidance) referencing the consult-team skill and listing natural-fit agents | REQ-F5 |
| AC-6 | Given a doing command (`/build`, `/deliver`, `/breakdown`, `/define`), when its skill file is inspected, then it contains no agent consultation pointers | REQ-F6 |
| AC-7 | Given an agent that has completed its review, when its output is inspected, then it includes a self-evaluation section | REQ-F7 |
| AC-8 | Given any dispatched agent (Mode 1, 2, or 3), when it completes its work, then it has written its own report to `.plans/reviews/` including findings, instructions received, and self-evaluation | REQ-F8 |
| AC-9 | Given the consult-team skill name and description, when compared to Superpowers' dispatching-parallel-agents, then the names and descriptions are clearly distinguishable in purpose | REQ-F10 |
| AC-10 | Given an agent definition file, when its frontmatter is inspected, then it includes `memory: project` enabling persistent knowledge accumulation in `.claude/agent-memory/<name>/` | REQ-F9 |
| AC-11 | Given the consult-team skill, when loaded, then it provides guidance for Mode 2 (parallel subagents) and Mode 3 (collaborative team via TeamCreate) including a decision gate for choosing between snapshot and delta dispatch. Mode 1 guidance is provided by Tier 1 command pointers (COMP-4), not the skill. | REQ-F11 |
| AC-12 | Given a Mode 3 collaborative team session, when a teammate completes their work, then they have written their own report to `.plans/reviews/` including findings, instructions received, and self-evaluation — independent of the lead's report | REQ-F12 |

---

## 6. Constraints

### 6.1 Inherited from Charter

- Solo developer — agent system must be manageable without team coordination
- Strict MVP discipline — build what's needed now, expand from experience
- Claude Code compatibility required for all skill and agent behavior

### 6.2 Spec-Specific Constraints

- Agent system shall not depend on Superpowers plugin functionality — use Superpowers patterns as reference but implement independently for eventual standalone operation
- Skills are loaded context and guidance, not control flow — the main agent always coordinates; skills provide knowledge of how to coordinate, not execution logic
- Terminal sessions cannot persist agent connections — all cross-session continuity must be document-based
- Agent roster is designed for the current framework rework use case — roster expansion happens through use and self-evaluation, not speculative design

---

## 7. Dependencies

### 7.1 Depends On

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| Claude Code Agent tool | External | Available | Required for dispatching subagents; available in current Claude Code version |
| `.claude/skills/` directory convention | Resource | Available | Standard location for Claude Code skills |
| D4C bug report (ISSUE-004) | Resource | Available | Evidence base for agent team need |

### 7.2 Enables

| Dependent | Relationship |
|-----------|--------------|
| Framework rework spec (future) | Agent system provides the multi-perspective review needed to flesh out the comprehensive rework |
| SPEC-004 implementation | Agent consultation available during command behavioral fixes |
| Future skill development | Agent files (especially Prompt Engineer) provide review capability for new skill authoring |

---

## 8. Out of Scope

The following are explicitly NOT part of this specification:

- Auto-invocation of the consult-team skill by commands — commands include pointers but the skill is invoked by user choice or explicit agent suggestion, never automatically
- Custom agent-to-agent communication protocols — the platform's built-in SendMessage capability exists and agents may use it; this spec does not build additional communication infrastructure on top of it
- Agents modifying project files — agents return analysis and recommendations for project artifacts; the main agent or user acts on them. All dispatched agents (every mode) write their own reports to `.plans/reviews/`, but do not modify other project files
- Code review agents — covered by Superpowers for now; Praxisity will develop its own when scope expands to cover implementation phases
- Automated agent prompt refinement — self-evaluation generates data; humans decide when and how to revise prompts
- Populating Tier 3 agent-specific resources — directory structure is created but content grows through use, not upfront design
- Todoist integration for agent task tracking — task management service is under separate evaluation (SPEC-004 Q-1)

---

## 9. Open Questions

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| Q-1 | How reliably does Claude Code auto-invoke skills when it recognizes the need? | Deferred | No data as of 2026-03-28; designed around explicit chains for now with structure compatible with auto-invocation later |
| Q-2 | What is the optimal synthesis approach for multi-agent feedback — automated summary, raw responses, or both? | Deferred | Will be informed by experience using the agents during the framework rework spec work |
| Q-3 | Should the session report template be structured differently for single consult vs. team sessions? | Resolved | DESIGN-004 DATA-4: one flexible template covers all modes; sections left empty when not applicable |

---

## 10. References

- [D4C-ARS Bug Report](../references/d4c-praxisity-bug-report.md) — ISSUE-004 identified need for persistent agent teams
- [v0.5.0 Bug Report](../references/new-project-bug-report.md) — 46 bugs demonstrating single-perspective blind spots
- [CHARTER.md](../../CHARTER.md)
- [Claude Code Sub-agents documentation](https://code.claude.com/docs/en/sub-agents) — native subagent file format, tool restrictions, persistent memory
- [Claude Code Agent Teams documentation](https://code.claude.com/docs/en/agent-teams) — Mode 3 team creation and coordination
- Superpowers plugin skills (subagent-driven-development, dispatching-parallel-agents, brainstorming) — pattern reference for agent dispatch approaches

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-03-28 | Andrew Robert Spenn | Initial draft from brainstorming session |

---
