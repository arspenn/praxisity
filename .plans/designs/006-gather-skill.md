# Design: DESIGN-006 Gather Support Skill

## Metadata

| Field | Value |
|-------|-------|
| Design ID | DESIGN-006 |
| Title | Gather Support Skill |
| Status | Draft |
| Author | Lead Agent + 5-agent review team |
| Created | 2026-04-04 |
| Last Updated | 2026-04-04 |

### Specification References

| Spec ID | Title | Requirements Addressed |
|---------|-------|------------------------|
| [SPEC-006](../specs/006-gather-skill.md) | Gather Support Skill | REQ-G1 through REQ-G9 |
| [SPEC-004](../specs/004-command-fixes-and-patterns.md) | Command Behavioral Fixes | REQ-F3 (parent requirement) |

### Related Documents

| Document | Relationship |
|----------|--------------|
| [DESIGN-005](005-command-rewrites.md) | Parent design — COMP-5 (Gathering Protocol), DEC-2, DEC-8 |
| [Bug Report](../references/new-project-bug-report.md) | Evidence base — BUG-012, BUG-018 |
| [SESSION-4-4-26 reviews](../reviews/SESSION-4-4-26/) | 5-agent review of spec + prototype |

---

## 1. Overview

### 1.1 Design Summary

The `/gather` skill is a support skill that codifies the one-at-a-time gathering protocol as a reusable, auto-invokable behavior. Unlike workflow skills (which the user invokes to produce an artifact), support skills are loaded by the agent automatically when the context matches. The agent uses `/gather` whenever it needs to collect structured input from the user across multiple sections.

The skill has two subsystems:
1. **Gathering protocol** — the one-at-a-time rules, drafting permissions, sub-section handling, and skip/fill-in-the-rest behavior
2. **Memory-as-settings** — on first invocation, calibrates user preferences (gathering style, prompt detail) and persists them to project memory for all future sessions

### 1.2 Design Principles

- **Positive framing over prohibitions:** Rules are expressed as verification checks ("before you send, verify one section only") rather than negative prohibitions ("do not batch"). Negative lists teach the failure mode they're trying to prevent (elephants problem, identified by prompt-engineer review).
- **Observable gates over self-assessment:** Drafting permission is gated on observable conditions ("user has already provided direct input on this topic") rather than self-assessed judgment ("sufficient context"). Self-assessed gates caused BUG-018.
- **Memory is the settings store:** Per-project preferences use the Claude Code agent SDK memory system. No config files, no custom persistence. First-run calibration is two questions; subsequent runs load silently.
- **Self-contained:** Zero cross-references to other files. The skill is fully self-contained — loaded by the platform when needed, no dependencies on shared files.

### 1.3 Requirements Coverage

| Requirement | Component | Approach |
|-------------|-----------|----------|
| REQ-G1 | COMP-1 | "The Rule" — one section at a time, wait for response |
| REQ-G2 | COMP-1, COMP-2 | Drafting permitted when observable conditions met; respects `gathering-style` preference |
| REQ-G3 | COMP-1 | No unrequested drafts — verified in "Before You Send" check; exception for explicit user request (REQ-G5) |
| REQ-G4 | COMP-1 | Sub-section handling — each sub-category prompted individually |
| REQ-G5 | COMP-1 | "Fill in the rest" — draft remaining sections, but present each individually for confirmation |
| REQ-G6 | COMP-3 | Auto-invocation via `description` field context matching; `disable-model-invocation` defaults to `false` |
| REQ-G7 | COMP-3 | Description covers any gathering context, not just workflow skills |
| REQ-G8 | COMP-2 | Memory check on every invocation; calibration on first run |
| REQ-G9 | COMP-2 | Uses Claude Code agent SDK project memory; writes to MEMORY.md per official documentation |

---

## 2. Architecture

### 2.1 Skill Structure

```
.claude/skills/gather/
└── SKILL.md                   ← the entire skill (no templates, no supporting files)
```

No templates or supporting files — `/gather` is a protocol skill, not a document-producing skill. The SKILL.md contains the complete gathering protocol and memory-as-settings instructions.

### 2.2 Skill Type

**Support skill** — auto-invokable by the agent, also user-invokable via `/gather`.

| Frontmatter Field | Value | Rationale |
|-------------------|-------|-----------|
| `name` | `gather` | Invoked as `/gather` |
| `description` | Structured one-at-a-time gathering protocol... | Platform uses this for auto-invocation context matching |
| `user-invocable` | `true` (default) | User can invoke manually if auto-invocation doesn't fire |
| `disable-model-invocation` | `false` (default) | Agent can auto-invoke when context matches |

Contrast with **workflow skills** (charter, describe, design, plan, do) which will set `disable-model-invocation: true` to prevent auto-invocation.

### 2.3 Interaction with Workflow Skills

When a workflow skill is active (e.g., `/charter`) and reaches its Gather phase, the platform detects structured gathering context and auto-loads `/gather`'s instructions. The two skills compose on orthogonal concerns:

- **Workflow skill** defines WHAT to gather (sections, content, domain context)
- **Gather skill** defines HOW to gather (one at a time, drafting rules, pause behavior)

The workflow skill does not need to reference `/gather` — the platform handles the loading. If auto-invocation fails (QG-2 from SPEC-006), workflow skills can add an explicit fallback reference.

---

## 3. Components

### COMP-1: Gathering Protocol

**Purpose:** Enforce one-at-a-time gathering with observable drafting gates and positive verification checks.

**Satisfies:** REQ-G1, REQ-G2, REQ-G3, REQ-G4, REQ-G5

**Structure within SKILL.md:**

| Section | Purpose | Key Decision |
|---------|---------|--------------|
| The Rule | Core constraint — one section at a time | Two sentences, zero ambiguity |
| How to Gather Each Section | 4-step procedure | Step 1 respects `gathering-style` preference |
| When Drafting is Permitted | Observable gate for draft-first mode | "Prior user input or loaded documents explicitly cover this topic" — not self-assessed |
| Before You Send | Pre-send verification checklist | Replaces negative prohibitions with positive checks (elephants fix) |
| Handling Sub-Sections | Per-sub-category prompting | Each sub-category offered separately, skippable |
| Handling Skip Requests | Skip and "fill in the rest" | Explicit example showing one-at-a-time confirmation sequence |

**Key design decisions:**

**DEC-G1: Positive framing over prohibitions.** The prototype's "What You Must Not Do" section was replaced with "Before You Send" — a verification checklist the agent runs before each message. Three checks: one section only, previous section resolved, no unrequested drafts. This was the prompt-engineer's recommendation after identifying the original section as an elephants problem — five prohibitions that teach the exact batching strategy they're trying to prevent.

**DEC-G2: Observable drafting gate.** "Sufficient context" was replaced with an observable condition: "user has already provided direct input on this topic in this conversation, or loaded documents explicitly cover this section's content." Self-assessed "sufficient context" caused BUG-018 — the agent always concludes it has enough context. The observable gate requires pointing to specific prior input, not a judgment call. Default when uncertain: prompt instead of draft.

**DEC-G3: REQ-G3/G5 exception clause.** REQ-G3 (MUST: don't draft unprompted sections) and REQ-G5 (SHOULD: "fill in the rest" allows drafting) appeared to contradict. Resolved by adding an explicit exception: "unless the user explicitly requests it." The user's explicit request is the only override for REQ-G3.

---

### COMP-2: Memory-as-Settings

**Purpose:** Persist per-project gathering preferences using the Claude Code agent SDK memory system.

**Satisfies:** REQ-G8, REQ-G9

**Memory lifecycle:**

```
Every invocation:
  1. Check project memory for `gather-preferences`
  2. Found → load, apply silently, proceed to gathering
  3. Not found → first time in this project:
     a. Ask two calibration questions (one at a time)
     b. Save to project memory as `gather-preferences`
     c. Apply preferences, proceed to gathering
```

**Calibration questions (fixed — agent does not improvise):**

1. **Gathering style:** "How hands-on do you want to be during gathering?" → `guided` (always prompt from scratch) or `draft-first` (present drafts when context available)
2. **Prompt detail:** "How much detail do you want in prompts?" → `detailed` (explain with examples) or `brief` (section name + one line)

**Memory file format:**

```markdown
---
name: gather-preferences
description: User's gathering protocol preferences for this project
type: user
---

gathering-style: [guided | draft-first]
prompt-detail: [detailed | brief]
```

**Preference effects:**

| Preference | Value | Effect |
|------------|-------|--------|
| `gathering-style` | `guided` | Always prompt from scratch, even when context is available |
| `gathering-style` | `draft-first` | Present drafts for approval when prior input or loaded documents cover the topic |
| `prompt-detail` | `detailed` | Explain what each section needs and show domain-relevant examples |
| `prompt-detail` | `brief` | State the section name and what's needed in one line |

**Key design decision:**

**DEC-G4: Fixed calibration questions.** The PE recommended fixed questions to prevent the agent from improvising a 10-question configuration quiz. Two questions, two binary choices, asked one at a time per the gathering protocol itself. The calibration IS the first gathering — the skill eats its own dog food.

**DEC-G5: Main project memory, not skill-specific memory.** Preferences are stored in the main project memory (`~/.claude/projects/[path]/memory/`) per the official Claude Code memory tool documentation, not in a skill-specific memory path. Project memory is loaded into every session — any agent, subagent, or skill invocation sees preferences automatically. No separate memory systems.

---

### COMP-3: Auto-Invocation

**Purpose:** Enable the platform to load `/gather` automatically when structured gathering is detected.

**Satisfies:** REQ-G6, REQ-G7

**Mechanism:** The `description` field in SKILL.md frontmatter serves as the auto-invocation trigger. The platform matches conversation context against skill descriptions to decide which skills to load. The description is crafted to match gathering contexts broadly:

> "Structured one-at-a-time gathering protocol for collecting user input across multiple sections, categories, or fields — such as filling out a specification, charter, design document, requirements list, or any multi-part form where each section benefits from individual attention."

**Key findings from research:**

- `when_to_use` is NOT a supported frontmatter field (IDE diagnostic confirmed). The `description` field is what the platform uses for context matching.
- `disable-model-invocation` defaults to `false` — no explicit setting needed for auto-invocation.
- `user-invocable` defaults to `true` — user can also type `/gather` manually.

**Failure mode:** If auto-invocation doesn't fire, the agent falls back to its default gathering behavior. Bounded downside — same as current state before the skill existed. Workflow skills can add an explicit reference as a fallback if testing reveals unreliable auto-invocation.

---

## 4. Interfaces

### INT-G1: Gather Skill ↔ Project Memory

**Connects:** SKILL.md (COMP-2) ↔ project memory system

**Type:** Read + Write (via memory tool)

**Contract:**
- **Read:** On every invocation, check for `gather-preferences` memory file
- **Write:** On first invocation only, save calibration results as `gather-preferences`
- **Format:** Standard memory frontmatter (name, description, type) + preference key-value pairs
- **Path:** Main project memory per official Claude Code documentation

### INT-G2: Gather Skill ↔ Workflow Skills

**Connects:** `/gather` ↔ `/charter`, `/describe`, `/design`, `/plan`

**Type:** Platform auto-invocation (implicit) or explicit reference (fallback)

**Contract:**
- **Trigger:** Platform detects structured gathering context during workflow skill execution
- **Composition:** Workflow skill defines WHAT (sections); gather skill defines HOW (protocol)
- **Independence:** Neither skill references the other's internals. They compose via the platform.
- **Exclusion:** `/do` does not trigger gathering — its DIP execution steps are agent-driven, not user-input gathering

---

## 5. Design Decisions Summary

| ID | Decision | Rationale |
|----|----------|-----------|
| DEC-G1 | Positive framing (verification checks) over negative prohibitions | Negative prohibitions teach the failure mode (elephants problem) |
| DEC-G2 | Observable drafting gate over self-assessed "sufficient context" | Self-assessment caused BUG-018; observable gate requires pointing to specific prior input |
| DEC-G3 | REQ-G3 exception clause for explicit user request | Resolves MUST/SHOULD contradiction between REQ-G3 and REQ-G5 |
| DEC-G4 | Fixed calibration questions (2 questions, binary choices) | Prevents agent from improvising a configuration quiz |
| DEC-G5 | Main project memory for preference storage | Loaded into every session automatically; follows official SDK documentation |

---

## 6. Out of Scope

- Template handling (REQ-F1) — separate concern, inline in workflow skills
- What sections to gather — defined by consuming workflow skills
- File creation or modification — this skill governs conversation, not output
- Advanced preference UI — preferences live in agent memory
- BUG-034 (/do execution batching) — agent-driven work, not user-input gathering; `/gather` does not apply to `/do`

---

## 7. Open Questions (from SPEC-006)

| ID | Question | Status | Design Impact |
|----|----------|--------|---------------|
| QG-1 | What calibration questions on first run? | Resolved | DEC-G4: two fixed questions (gathering-style, prompt-detail) |
| QG-2 | How does auto-invocation interact with active workflow skill? | Open | INT-G2 defines the expected composition; needs empirical testing during `/charter` build |
| QG-3 | Memory path for preferences? | Resolved | DEC-G5: main project memory per official SDK docs |
| QG-4 | Can other skills read gathering preferences? | Open | Architecturally yes — project memory is shared. Validate during `/charter` build |

---

## 8. Testing Strategy

| Test | Validates | Method |
|------|-----------|--------|
| First-run calibration | AC-G4 | Invoke `/gather` or `/charter` in a fresh project; verify two calibration questions asked, preferences saved to memory |
| Subsequent-run loading | AC-G5 | Invoke again in same project; verify preferences loaded silently, no re-prompting |
| One-at-a-time enforcement | AC-G1 | Run a multi-section gathering; verify each section gets its own message with a pause |
| Draft-for-approval | AC-G2 | With `draft-first` preference, provide context for a section; verify draft presented with approval prompt |
| Sub-category handling | AC-G3 | Gather a section with sub-categories (e.g., constraints); verify each sub-category prompted individually |
| "Fill in the rest" | AC-G6 | Approve first few sections, say "fill in the rest"; verify remaining sections presented one at a time |
| Auto-invocation during workflow | AC-G7 | Run `/charter`; verify gathering protocol applies without explicit `/gather` invocation |
| General session use | AC-G8 | Outside a workflow skill, ask to gather structured input; verify protocol applies |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-04-04 | Lead Agent | Initial design — synthesized from SPEC-006, 5-agent review findings, and prototype iteration |

---