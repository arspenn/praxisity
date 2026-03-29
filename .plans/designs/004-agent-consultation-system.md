# Design: DESIGN-004 Agent Consultation System

## Metadata

| Field | Value |
|-------|-------|
| Design ID | DESIGN-004 |
| Title | Agent Consultation System Design |
| Status | Draft |
| Author | Andrew Robert Spenn |
| Created | 2026-03-28 |
| Last Updated | 2026-03-28 |

### Specification References

| Spec ID | Title | Requirements Addressed |
|---------|-------|------------------------|
| [SPEC-005](../specs/005-agent-consultation-system.md) | Agent Consultation System | REQ-F1 through REQ-F10, REQ-N1 through REQ-N4 |

### Related Documents

| Document | Relationship |
|----------|--------------|
| [D4C Bug Report: ISSUE-004](../references/d4c-praxisity-bug-report.md) | Depends on — identified need for persistent agent teams |
| [Claude Code Agent Teams docs](https://code.claude.com/docs/en/agent-teams) | Reference — platform capabilities for Mode 3 |

---

## 1. Overview

### 1.1 Design Summary

This design implements a prompt-based agent consultation system — no runtime code, no automation logic. The entire deliverable is authored files: 8 agent definition prompts, 1 skill document, 1 collaborative mode extension, 1 flexible report template, 1 context block template, a directory structure, and minor edits to 3 existing command files.

The architecture follows a 3-tier progressive loading model where content enters the agent's context only when needed. Tier 1 is 2 lines embedded in thinking commands. Tier 2 is the consult-team skill loaded on demand. Tier 3 is individual agent files loaded only when that specific agent is dispatched. Three dispatch modes (single expert consult, parallel perspectives, collaborative team) serve different needs, with a decision gate in the skill that forces explicit consideration of snapshot vs. delta tradeoffs.

The main agent is always the coordinator. The skill provides knowledge of how to coordinate but contains no control flow. Agent files are immutable at dispatch time — customization is appended, never edited in. For collaborative teams (Mode 3), agents are full parallel sessions that write their own reports, maintain their own perspective, and can interact directly with the user.

### 1.2 Design Principles

- **Progressive disclosure** — load only what's needed for the current task; never prime the agent with perspectives it shouldn't be thinking about yet
- **Immutable personas, mutable context** — agent identity is stable across sessions; what changes is what they're looking at
- **Document-based persistence** — all continuity lives in files, never in terminal state
- **Bootstrapping** — the agents are built to be useful immediately on the framework rework, then refined from that experience

### 1.3 Requirements Coverage

| Requirement | Design Section | Approach |
|-------------|----------------|----------|
| REQ-F1 | COMP-1, DATA-1 | Standardized agent files with frontmatter + 4 sections |
| REQ-F2 | COMP-1, COMP-2, DATA-2, DATA-3, INT-1 | Layered prompt assembly: agent file (immutable) + collab-mode (Mode 3) + context block (appended) |
| REQ-F3 | COMP-3 | consult-team skill with agent index, decision gate, dispatch guidance, session management |
| REQ-F4 | COMP-1 | 8 agent files across 4 categories |
| REQ-F5 | COMP-4 | 2-line pointers in /spec, /architect, /charter |
| REQ-F6 | COMP-4 | No pointers in /build, /deliver, /breakdown, /define |
| REQ-F7 | COMP-1, DATA-1 | Self-Evaluation section in every agent file's output instructions |
| REQ-F8 | COMP-2, DATA-4, INT-3 | Flexible session report template; reports saved to .plans/reviews/ |
| REQ-F9 | COMP-1 | agents/resources/ directory with per-agent subdirectories (empty initially) |
| REQ-F10 | COMP-3 | Skill name and description emphasize perspective consultation vs. independent parallel tasks |
| REQ-N1 | All | All files authored for dual consumption (human-readable + AI-effective) |
| REQ-N2 | COMP-3, DEC-4 | Skill provides guidance and decision frameworks, not execution sequences |
| REQ-N3 | COMP-3, COMP-4 | Consultation always optional; pointers suggest, never require |
| REQ-N4 | COMP-2, DATA-4, INT-3 | Team composition captured in session reports; lead review includes reconstitution notes |

---

## 2. Architecture

#### 2.1 System Context

```
┌─────────────┐     invokes      ┌──────────────────┐
│    User      │───────────────▶  │   Main Agent     │
└─────────────┘                   │   (Team Lead)    │
                                  └──────────────────┘
                                     │        │       │
                               Tier 1    Tier 2    Tier 3
                              (command   (skill    (agent
                               ptrs)     load)     files)
                                     │        │       │
                    ┌────────────────┴────────┴───────┴──────────┐
                    │                                             │
            Mode 1 & 2:                                   Mode 3:
            Agent tool                                    TeamCreate
            (subagents)                                   (agent teams)
                    │                                             │
        ┌───────────┼───────────┐              ┌─────────────────┼─────────────────┐
        ▼           ▼           ▼              ▼                 ▼                 ▼
  ┌──────────┐┌──────────┐┌──────────┐  ┌──────────┐     ┌──────────┐     ┌──────────┐
  │ Expert A ││ Expert B ││ Expert C │  │Teammate A│◄───▶│Teammate B│◄───▶│Teammate C│
  │(snapshot)││(snapshot)││(snapshot)│  │ (delta)  │     │ (delta)  │     │ (delta)  │
  └────┬─────┘└────┬─────┘└────┬─────┘  └────┬─────┘     └────┬─────┘     └────┬─────┘
       │           │           │              │                │                │
       └───────────┼───────────┘              └────────────────┼────────────────┘
                   ▼                                           ▼
            Results return                              Shared task list
            to main agent                               + direct messaging
                   │                                    + user can interact
                   │                                    directly (Shift+Down)
                   └──────────────┬────────────────────────────┘
                                  ▼
                           ┌──────────────┐
                           │ .plans/      │
                           │  reviews/    │
                           │  (reports)   │
                           └──────────────┘
```

**Key distinction:** Modes 1 & 2 (subagents) see a snapshot — they get the current state, evaluate, and return. Mode 3 (agent teams) see deltas — they maintain context across the full work session and can detect when a change in one area breaks assumptions in another.

#### 2.2 Architecture Pattern

**Pattern:** Three-mode progressive dispatch with file-based persona loading

**Rationale:** Each mode serves a different need. The skill must help the main agent choose correctly because the natural tendency is to default to the lightest-weight option even when the heavier option is what's needed.

**Three dispatch modes:**

| Mode | Mechanism | Context | Communication | When to Use |
|------|-----------|---------|---------------|-------------|
| **1. Single expert consult** | Agent tool (1 subagent) | Snapshot only | Returns to main agent | Quick second opinion on a focused question |
| **2. Parallel perspectives** | Agent tool (N subagents) | Snapshot only | Each returns to main agent independently | Multiple viewpoints needed, no inter-agent discussion required |
| **3. Collaborative team** | TeamCreate (agent teams) | Persistent delta-aware | Direct inter-agent messaging + shared task list + direct user interaction | Sustained work where context accumulation matters; where a fix from one perspective might break another |

**Trade-offs:**

| | Single Consult | Parallel Perspectives | Collaborative Team |
|---|---|---|---|
| Token cost | Low | Medium (scales with N) | High (full session per agent) |
| Context depth | None (cold read) | None (cold read) | Accumulates over session |
| Catches regressions | No | No | Yes (sees changes) |
| Setup overhead | Minimal | Minimal | Requires team creation + cleanup |
| User interaction | Via main agent only | Via main agent only | Direct interaction possible |
| Best for | Sanity checks | Spec/design review gates | Multi-DIP implementation, framework rework |

**Prompt assembly by mode:**

```
Mode 1: [agent.md] + [customization]
Mode 2: [agent.md] + [customization]  (×N in parallel)
Mode 3: [agent.md] + [collab-mode.md] + [customization]
```

#### 2.3 Technology Choices

| Layer/Concern | Technology | Rationale |
|---------------|------------|-----------|
| Snapshot dispatch (Modes 1 & 2) | Claude Code Agent tool | Built-in subagent capability; lightweight, results return to caller |
| Persistent dispatch (Mode 3) | Claude Code TeamCreate (experimental) | Full agent team with shared task list, messaging, persistent context |
| Inter-agent communication | Claude Code SendMessage / team mailbox | Platform-native; Mode 3 agents can challenge each other directly |
| Quality gates | Claude Code hooks (TeammateIdle, TaskCreated, TaskCompleted) | Available for future enforcement of standards on agent work |
| Skill loading | Claude Code Skill tool | Standard mechanism for on-demand context loading |
| File format | Markdown with YAML frontmatter | Human-readable, AI-parseable, consistent with rest of Praxisity |
| Persistence | `.plans/reviews/` directory + planning artifacts | Document-based; survives session termination |

**Note:** Agent teams require `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` enabled and Claude Code v2.1.32+. The skill should note this prerequisite and provide fallback guidance to use Mode 2 if teams are unavailable.

---

## 3. Components

### COMP-1: Agent Definition Files

**Purpose:** Define the 8 agent personas in a standardized, immutable format that supports progressive loading through frontmatter.

**Satisfies:** REQ-F1, REQ-F2, REQ-F4, REQ-F7, REQ-F9, REQ-N1

**Responsibilities:**
- Define each agent's identity, reasoning approach, output format, and self-evaluation instructions
- Provide frontmatter (name, category, purpose) readable without loading the full file
- Remain immutable at dispatch time — never edited, only appended to with additional layers
- Function standalone without assuming any content will be appended

**Dependencies:**
- None — standalone files

**Key Design Decisions:**
- 8 files, one per agent: `critic.md`, `skeptic.md`, `user-advocate.md`, `stakeholder.md`, `designer.md`, `project-manager.md`, `prompt-engineer.md`, `fresh-eyes-reviewer.md`
- Each file follows identical section structure (Identity, Reasoning Approach, Output Format, Self-Evaluation)
- `agents/resources/` subdirectories created per-agent but left empty initially (Tier 3 infrastructure)
- Self-evaluation section is part of the agent's instructions, not a separate mechanism
- Files must be focused and concise — establish perspective and expectations, not exhaustive instructions

**Agent Roster:**

| Agent | Category | Core Question |
|-------|----------|---------------|
| Critic | Evaluative | "What's wrong with this?" |
| Skeptic | Evaluative | "Do we even need this?" |
| User Advocate | Perspective | "Would a new user understand and benefit?" |
| Stakeholder | Perspective | "Does the output serve its audience?" |
| Designer | Structural | "How do the pieces fit together?" |
| Project Manager | Structural | "What's realistic and what blocks what?" |
| Prompt Engineer | Meta | "Is this optimized for both humans and AI?" |
| Fresh Eyes Reviewer | Meta | "Does what's written match what's written elsewhere?" |

---

### COMP-2: Templates and Extensions

**Purpose:** Provide standardized formats for per-dispatch customization, collaborative mode extension, and output persistence.

**Satisfies:** REQ-F2, REQ-F8, REQ-N4

**Responsibilities:**
- Context block template: standardized structure appended by the main agent at dispatch (phase, topic, focus, materials)
- Collaborative mode extension (`collab-mode.md`): single shared file adding Mode 3 awareness to any agent — session persistence, direct file writing, direct user interaction, self-authored reporting
- Session report template: flexible format for saving consultation outputs to `.plans/reviews/` — used by both Mode 2 (main agent writes) and Mode 3 (teammates and lead write separately)

**Dependencies:**
- COMP-1 (context block appended to agent files; collab-mode appended between agent file and context block)
- `.plans/reviews/` directory (report destination)

**Key Design Decisions:**
- Collab-mode.md is a single shared file, not per-agent — avoids 7x duplication; contains only what's different about being a persistent teammate vs. a one-shot subagent
- One flexible session report template covers all modes — sections left empty when not applicable rather than maintaining separate templates
- Context block provides structure but the main agent writes naturally within it; the main agent identifies the customization section explicitly when it writes it
- Report naming: `[ARTIFACT-ID]-agent-review.md` (Mode 2), `[ARTIFACT-ID]-[agent-name]-report.md` (Mode 3 teammates), `[ARTIFACT-ID]-lead-review.md` (Mode 3 lead)

---

### COMP-3: consult-team Skill

**Purpose:** Provide the main agent with on-demand guidance for multi-agent dispatch — the decision gate between Mode 2 (parallel perspectives) and Mode 3 (collaborative team), plus session management for both.

**Satisfies:** REQ-F3, REQ-F10, REQ-N2, REQ-N3

**Responsibilities:**
- Agent index: names, categories, purposes (from frontmatter — enough to select without loading full files)
- Decision gate: snapshot vs. delta — when parallel subagents are sufficient vs. when a persistent team is needed
- Mode 2 guidance: how to dispatch multiple subagents in parallel, how to synthesize their independent returns
- Mode 3 guidance: how to use TeamCreate, how to set up team with persona-based teammates, prompt assembly (agent.md + collab-mode.md + customization), session management (don't shut down prematurely, let teammates write their own reports), fallback to Mode 2 if agent teams unavailable
- Output preservation: how and when to save session reports to `.plans/reviews/`; Mode 2 vs. Mode 3 reporting differences
- Naming and description: clearly differentiated from Superpowers' `dispatching-parallel-agents`

**Dependencies:**
- COMP-1 (agent files referenced by index)
- COMP-2 (templates and collab-mode used for dispatch and reporting)
- Claude Code Agent tool (Mode 2)
- Claude Code TeamCreate (Mode 3, experimental — requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`)

**Key Design Decisions:**
- The skill is guidance, not control flow — tells the agent what to consider, not what to execute
- Decision gate is the core value: forces snapshot vs. delta consideration before choosing a dispatch mode
- Notes experimental status of agent teams and provides fallback guidance
- Does NOT embed agent personas — only the index; full personas load at Tier 3 when agents are dispatched

---

### COMP-4: Tier 1 Command Pointers

**Purpose:** Add minimal agent consultation reminders to thinking commands without bloating their context.

**Satisfies:** REQ-F5, REQ-F6, REQ-N3

**Responsibilities:**
- Add 2-line pointer to `/spec`, `/architect`, `/charter`: Mode 1 (single consult) inline, Modes 2 & 3 via consult-team skill
- List natural-fit agents per command (just names)
- Do NOT add pointers to `/build`, `/deliver`, `/breakdown`, `/define`

**Dependencies:**
- COMP-3 (skill referenced by pointer)
- Existing command files in `.claude/commands/`

**Key Design Decisions:**
- Approximately 4 lines per command (heading + 2 guidance lines) — enough to remind, not enough to prime
- Mode 1 is inline (dispatch a single agent directly), Modes 2 & 3 require loading the skill (decision gate)
- Natural-fit suggestions: `/spec` → Critic, User Advocate, Skeptic; `/architect` → Designer, Prompt Engineer, Critic; `/charter` → Stakeholder, Project Manager
- Doing commands stay completely clean — user can always manually invoke the skill

---

## 4. Interfaces

### INT-1: Agent Dispatch Interface

**Connects:** COMP-3 (consult-team skill) → COMP-1 (agent files) → COMP-2 (collab-mode + context block)

**Type:** File read + prompt assembly

**Direction:** Unidirectional (skill guides the main agent to read and assemble)

**Contract:**
```
Prompt assembly by mode:

Mode 1 (single consult):
  1. Main agent reads agent file verbatim (e.g., agents/critic.md)
  2. Main agent writes customization section, identifying it as such
  3. Dispatch prompt = [agent file] + [customization]
  4. Dispatch via Agent tool

Mode 2 (parallel perspectives):
  Same as Mode 1, repeated for each selected agent
  All dispatched via Agent tool in parallel

Mode 3 (collaborative team):
  1. Main agent reads agent file verbatim
  2. Main agent reads collab-mode.md
  3. Main agent writes customization section
  4. Spawn prompt = [agent file] + [collab-mode.md] + [customization]
  5. Dispatch via TeamCreate
```

---

### INT-2: Command Pointer Interface

**Connects:** COMP-4 (Tier 1 pointers) → COMP-3 (consult-team skill)

**Type:** Skill invocation reference

**Direction:** Unidirectional (command points to skill)

**Contract:**
```
Tier 1 pointer format (in thinking command files):

## Agent Consultation

For a quick single perspective, dispatch: [agent name], [agent name], or [agent name].
For multi-agent input (parallel or collaborative), invoke the consult-team skill.

Mode 1: Main agent dispatches directly using Agent tool (no skill load)
Modes 2 & 3: Main agent invokes consult-team skill via Skill tool,
             then follows loaded guidance including decision gate
```

---

### INT-3: Session Report Interface

**Connects:** COMP-1 (agents) + Main Agent → COMP-2 (report template) → `.plans/reviews/`

**Type:** Multi-author file write

**Direction:** Multiple writers → review directory

**Contract:**
```
Mode 2 (parallel subagents):
  Main agent writes consolidated session report using template:
    .plans/reviews/[ARTIFACT-ID]-agent-review.md
  Contains: metadata, findings per agent, synthesis

Mode 3 (collaborative team):
  Each teammate writes their own report directly:
    .plans/reviews/[ARTIFACT-ID]-[agent-name]-report.md
  Contains:
    - Their findings and analysis
    - The customized instructions they received (appended context block)
    - Self-evaluation
    - Questions or concerns for the user/team

  Main agent writes a separate lead review:
    .plans/reviews/[ARTIFACT-ID]-lead-review.md
  Contains:
    - Assessment of each teammate's work
    - Verification that customized instructions were followed
    - Synthesis across all perspectives
    - Team reconstitution notes for future sessions
    - Disagreements or tensions observed between teammates

  Main agent can compare teammate's reported instructions against
  what was actually sent to verify context passing fidelity.

User interaction paths (Mode 3):
  Standard:  Teammate ──message──▶ Main Agent ──relay──▶ User
  In-depth:  User ──Shift+Down──▶ Teammate (direct terminal interaction)
```

---

## 5. Data Model

### 5.1 Entity Overview

```
┌──────────────┐     assembled into      ┌─────────────────┐
│ DATA-1       │─────────────────────────▶│ Dispatch Prompt  │
│ Agent Def    │                          │ (Mode 1 & 2)    │
└──────────────┘                          └─────────────────┘
       │
       │ + (Mode 3 only)
       ▼
┌──────────────┐     assembled into      ┌─────────────────┐
│ DATA-2       │─────────────────────────▶│ Dispatch Prompt  │
│ Collab Mode  │                          │ (Mode 3)        │
└──────────────┘                          └─────────────────┘
       │
       │ + (all modes)
       ▼
┌──────────────┐
│ DATA-3       │
│ Context Block│
└──────────────┘

       Outputs:
┌──────────────┐
│ DATA-4       │──────▶ .plans/reviews/
│ Session Rpt  │
└──────────────┘
```

### DATA-1: Agent Definition File

**Purpose:** Define a single agent persona

**Used by:** COMP-1, COMP-3 (index reads frontmatter), INT-1 (prompt assembly)

**Schema/Structure:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | frontmatter string | Yes | Agent identifier (e.g., "critic") |
| category | frontmatter string | Yes | One of: evaluative, perspective, structural, meta |
| purpose | frontmatter string | Yes | One-line description for index listing |
| Identity | markdown section | Yes | Who this agent is, what perspective they bring |
| Reasoning Approach | markdown section | Yes | How they think, what they look for, priorities |
| Output Format | markdown section | Yes | Structure of their responses |
| Self-Evaluation | markdown section | Yes | Instructions to reflect on their own performance |

**Constraints:**
- Files must be functional standalone (no assumption of appended content)
- Focused and concise — establish perspective and expectations, not exhaustive instructions

---

### DATA-2: Collaborative Mode Extension

**Purpose:** Add Mode 3-specific awareness to any agent

**Used by:** COMP-2, INT-1 (inserted between agent file and customization for Mode 3)

**Schema/Structure:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Session awareness | markdown section | Yes | You are a persistent teammate, not a subagent; you maintain context across the session |
| Direct capabilities | markdown section | Yes | Can write files to .plans/reviews/, can request relay to user, user may interact directly via Shift+Down |
| Reporting duties | markdown section | Yes | Write your own report including findings, the instructions you received, and self-evaluation |
| Team dynamics | markdown section | Yes | Maintain your perspective even in disagreement; flag changes that affect your domain |

**Constraints:**
- Single file (`collab-mode.md`) used for all agents — not per-agent
- Must not duplicate anything from agent definition files
- Focused on what's different about being a persistent teammate vs. a one-shot subagent

---

### DATA-3: Context Block (Customization)

**Purpose:** Per-dispatch situational context appended by the main agent

**Used by:** COMP-2 (template), all dispatch modes via INT-1

**Schema/Structure:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Section identifier | markdown heading | Yes | Main agent identifies this as the customization section |
| Phase | string | Yes | Current workflow phase (specifying, designing, reviewing, etc.) |
| Topic | string | Yes | What's being evaluated |
| Focus | string | No | Specific aspects to pay attention to |
| Materials | file paths or inline | Yes | What to read or what's provided inline |

**Constraints:**
- Written by the main agent, not templated rigidly — template provides structure, main agent writes naturally
- Keep it focused: enough context to orient, not a full project dump

---

### DATA-4: Session Report

**Purpose:** Persist consultation outputs beyond the terminal session

**Used by:** COMP-2 (template), COMP-3 (guidance on when/how to write), INT-3

**Schema/Structure (flexible template — all modes):**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Metadata | section | Yes | Artifact ID, date, agent name(s), dispatch mode |
| Instructions received | section | Mode 3 teammates: the customization block they were given; Mode 2/lead: user's team instructions | What this agent was told to do |
| Findings | section | Yes | Analysis and recommendations |
| Self-evaluation | section | Yes | What worked, what they struggled with, prompt improvement suggestions |
| Synthesis | section | Lead review and Mode 2 only | Cross-perspective analysis, areas of agreement/disagreement |
| Reconstitution notes | section | Lead review (Mode 3) only | Team composition, open concerns, context summary for next session |

**Constraints:**
- One flexible template covers all modes; sections left empty when not applicable
- Naming: `[ARTIFACT-ID]-agent-review.md` (Mode 2), `[ARTIFACT-ID]-[agent-name]-report.md` (Mode 3 teammates), `[ARTIFACT-ID]-lead-review.md` (Mode 3 lead)
- All reports go to `.plans/reviews/`

---

## 6. Design Decisions

### DEC-1: Three-Mode Dispatch with Decision Gate

**Context:** The framework needs agent consultation at different scales — from quick sanity checks to sustained collaborative work sessions.

**Decision:** Three distinct dispatch modes (single consult, parallel perspectives, collaborative team) with Mode 1 inline in commands and Modes 2 & 3 behind a skill-load decision gate.

**Rationale:** The natural tendency is to default to the lightest option. Demonstrated during brainstorming when the main agent assumed subagents when the user meant persistent teams. Forcing Modes 2 & 3 through the skill ensures the snapshot vs. delta tradeoff is explicitly considered.

**Alternatives Considered:**
- All three modes inline: Low friction but removes the decision gate; agent defaults to Mode 2 when Mode 3 is needed
- All three modes in skill: Adds a skill load for simple single consults that don't need it

**Consequences:**
- Mode 1 is frictionless (good for quick checks)
- Modes 2 & 3 require one extra step that forces a better decision

---

### DEC-2: Layered Prompt Assembly (Agent + Collab + Customization)

**Context:** Agent personas need to work across all three dispatch modes without modification, but Mode 3 requires additional awareness of persistent session capabilities.

**Decision:** Three independent, stackable prompt layers: base agent file (standalone), collaborative mode extension (Mode 3 only), and customization block (all modes). Each layer is functional without the layers above it.

**Rationale:** Keeps agent files clean and reusable. The collab-mode extension is a single shared file rather than per-agent variants, avoiding 7x duplication. Customization isn't assumed by the agent file, so agents work standalone if dispatched without it.

**Alternatives Considered:**
- Separate Mode 1/2 and Mode 3 agent files: Duplicates persona content across two files per agent
- Embed collab awareness in every agent file: Bloats Mode 1 & 2 dispatches with irrelevant session management instructions

---

### DEC-3: Agents Write Their Own Reports (Mode 3)

**Context:** Mode 3 teammates are full parallel sessions, not subordinate subagents. They maintain context, can interact directly with the user, and see deltas across the work session.

**Decision:** In Mode 3, each teammate writes their own report directly to `.plans/reviews/`, including findings, the instructions they received, and self-evaluation. The main agent writes a separate lead review assessing the team's work. In Mode 2, the main agent writes a consolidated report.

**Rationale:** Teammates are independent professionals, not funnels. Their self-authored reports capture nuance that would be lost in main-agent summarization. Including the instructions they received allows verification of context passing fidelity. The lead review adds managerial perspective without replacing the source material.

**Alternatives Considered:**
- Main agent consolidates all reports: Loses individual nuance; introduces telephone-game summarization errors
- Only teammate reports, no lead review: Loses the cross-perspective synthesis and instruction fidelity check

---

### DEC-4: Skills as Guidance, Not Control Flow

**Context:** The Superpowers plugin separates dispatch logic into its own skill with deterministic workflow sequences. Praxisity needs a different approach.

**Decision:** The consult-team skill provides knowledge and decision frameworks. It does not prescribe execution sequences. The main agent reads the guidance and makes its own coordination decisions.

**Rationale:** Skills are loaded context — instructions in the agent's working memory. Treating them as functions creates false expectations about execution guarantees. The agent may need to adapt based on the situation. Guidance enables adaptation; control flow fights it.

**Alternatives Considered:**
- Deterministic skill workflow (Superpowers pattern): More predictable but brittle; doesn't adapt to unexpected situations
- No skill at all (pure user instruction): Works but requires the user to remember and specify everything every time

---

## 7. Implementation Considerations

### 7.1 Implementation Order

| Order | Component | Dependencies | Notes |
|-------|-----------|--------------|-------|
| 1 | Directory structure | None | Create `.claude/skills/consult-team/agents/`, `agents/resources/[per-agent]/`, `templates/`, `.plans/reviews/` |
| 2 | COMP-2: Templates + collab-mode | None | Small standalone files. Context block, session report template, collab-mode.md. Needed before testing dispatch. |
| 3 | COMP-1: Agent definition files | None | Write the 8 agent personas. Foundation that everything else references. |
| 4 | COMP-3: consult-team skill | COMP-1 (for index), COMP-2 (for template references) | Core deliverable. References agent index and templates. Includes decision gate. |
| 5 | COMP-4: Tier 1 command pointers | COMP-3 (skill must exist to reference) | Lightest lift — 2 lines added to 3 command files (`/spec`, `/architect`, `/charter`). |
| 6 | Bootstrapping test | All components | Use the agents on real spec work (framework rework) to validate before finalizing. |

### 7.2 Risk Areas

| Risk | Impact | Mitigation |
|------|--------|------------|
| Agent teams experimental flag not enabled or unavailable | Mode 3 unusable; lose delta-awareness capability | Skill includes fallback guidance to use Mode 2; note prerequisite clearly |
| Agent personas too generic to provide useful differentiated feedback | Consultation produces redundant output; wasted tokens | Bootstrapping test on real spec work before finalizing; self-evaluation data informs revisions |
| Customization blocks become bloated over time | Diminishes agent focus; noisy prompts | Skill guidance emphasizes "focused and informative"; lead review checks instruction quality |
| Main agent defaults to Mode 2 despite decision gate | Loses delta-awareness when it's needed | Skill's snapshot vs. delta framing makes the tradeoff explicit; user can always direct Mode 3 |
| Teammate reports vary wildly in format and quality | Hard to compare across agents; synthesis becomes difficult | Output Format section in each agent file standardizes structure; collab-mode.md reinforces reporting duties |

### 7.3 Testing Strategy

| Level | Approach | Covers |
|-------|----------|--------|
| Smoke test | Dispatch one agent (Mode 1) on a focused question from SPEC-005 | COMP-1, COMP-2 (context block), basic dispatch |
| Mode 2 test | Parallel dispatch of 3 agents on a spec section review | COMP-3 (skill guidance for parallel), synthesis |
| Mode 3 test | Full collaborative team on the framework rework spec | COMP-3 (team guidance), collab-mode.md, reporting, self-evaluation |
| Integration | Verify Tier 1 pointers trigger correctly during `/spec` or `/architect` run | COMP-4 |
| Bootstrapping | Use agents on real work, review self-evaluations, refine prompts | All components — the real test |

All testing is manual — run the workflow, observe behavior, review outputs.

### 7.4 Design-Phase Learning: The Fresh Eyes Reviewer

During this design session, the spec reviewer (dispatched cold with no conversation context) caught two contradictions the authors missed — a line count discrepancy and a conflict between the spec's out-of-scope and the design's Mode 3 reporting. Both felt resolved because they'd been discussed, but the documents still said the old thing.

This pattern will recur constantly. The Fresh Eyes Reviewer (8th agent, added during design) is specifically designed for cold-read cross-document consistency. It reads linked specs, designs, and DIPs without brainstorming history — the way a future implementer will. It is likely to be one of the most frequently dispatched standalone agents.

---

## 8. Out of Scope

**From Specification (inherited):**
- Auto-invocation of the consult-team skill by commands
- Custom agent-to-agent communication protocols (platform's SendMessage exists)
- Agents modifying project files (beyond their own reports in `.plans/reviews/`)
- Code review agents (covered by Superpowers for now)
- Automated agent prompt refinement
- Populating Tier 3 agent-specific resources upfront
- Todoist integration for agent task tracking

**Design-Specific Exclusions:**
- Hooks integration (TeammateIdle, TaskCreated, TaskCompleted) — available via Claude Code but not configured as part of this implementation; future optimization
- Agent performance metrics or scoring — self-evaluation is qualitative, not quantitative
- Multi-team support — one team at a time per Claude Code limitation
- Split-pane (tmux/iTerm2) configuration — users configure this via Claude Code settings, not Praxisity

---

## 9. Open Questions

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| DQ-1 | Should the collab-mode.md instruct teammates to coordinate report writing timing, or let them write whenever they finish? | Open | Start with write-when-finished; coordinate if reports conflict |
| DQ-2 | What is the optimal team size for spec review vs. design review vs. implementation? | Deferred | Will be informed by bootstrapping experience; Claude Code docs suggest 3-5 teammates |

---

## 10. Appendices

### A. Glossary

| Term | Definition |
|------|------------|
| Snapshot | A one-time view of current state; what Modes 1 & 2 (subagents) see |
| Delta | Awareness of changes over time; what Mode 3 (persistent teammates) see |
| Decision gate | The point in the skill where the agent must choose between snapshot and delta dispatch |
| Progressive loading | Architecture where content enters context only when needed, organized in tiers |
| Tier 1 | Command-level pointers (2 lines, always loaded) |
| Tier 2 | consult-team skill (loaded on demand) |
| Tier 3 | Individual agent files + resources (loaded per-dispatch) |
| Context block | Per-dispatch customization appended by main agent to orient the dispatched agent |
| Collab-mode | Shared extension file adding Mode 3 awareness to any agent |

### B. References

- [SPEC-005: Agent Consultation System](../specs/005-agent-consultation-system.md)
- [Claude Code Agent Teams documentation](https://code.claude.com/docs/en/agent-teams)
- [D4C-ARS Bug Report](../references/d4c-praxisity-bug-report.md)
- [v0.5.0 Bug Report](../references/new-project-bug-report.md)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-03-28 | Andrew Robert Spenn | Initial draft from brainstorming and architect session |

---
