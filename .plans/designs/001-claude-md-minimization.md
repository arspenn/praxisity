# Design: DESIGN-001 CLAUDE.md Minimization

## Metadata

| Field | Value |
|-------|-------|
| Design ID | DESIGN-001 |
| Title | CLAUDE.md Minimization |
| Status | Draft |
| Author | Andrew Robert Spenn |
| Created | 2026-03-20 |
| Last Updated | 2026-03-20 |

### Specification References

| Spec ID | Title | Requirements Addressed |
|---------|-------|------------------------|
| [SPEC-001](../specs/001-claude-md-minimization.md) | CLAUDE.md Minimization | REQ-F1, REQ-F2, REQ-F3, REQ-F4, REQ-F5, REQ-F6, REQ-N1, REQ-N2 |

### Related Documents

| Document | Relationship |
|----------|--------------|
| [CLAUDE.md](../../CLAUDE.md) | Artifact being modified |
| [claude.template.md](../../.praxisity/templates/claude.template.md) | Affected by |
| [README.md](../../README.md) | Relocation target |

---

## 1. Overview

### 1.1 Design Summary

The approach is a section-by-section audit of the current 373-line CLAUDE.md, classifying each into keep/remove/relocate. The minimized file retains only: (1) the identity/context that establishes this repo as the framework itself, (2) PLANNING.md state management instructions, (3) the design-first workflow constraint, and (4) a pointer to non-obvious files. Everything else is either already discoverable from code or gets relocated to README.md.

Content is relocated to README.md before any removals from CLAUDE.md, ensuring no information loss at any point during implementation.

### 1.2 Design Principles

1. **If the agent can find it, don't tell it** -- only include what's non-obvious or corrective
2. **Every line must earn its place** -- each line should steer behavior the agent would otherwise get wrong
3. **Relocate, don't delete** -- removed content must land somewhere appropriate

### 1.3 Requirements Coverage

| Requirement | Design Section | Approach |
|-------------|----------------|----------|
| REQ-F1 | Section 2 (Architecture) | Section-by-section classification table |
| REQ-F2 | COMP-1 | "This IS the framework" block retained |
| REQ-F3 | COMP-1 | Git safety referenced briefly; details live in commands |
| REQ-F4 | COMP-2 | Relocated content goes to README.md |
| REQ-F5 | COMP-3 | Template updated with "corrections only" philosophy |
| REQ-F6 | COMP-1 | PLANNING.md reference and lifecycle retained |
| REQ-N1 | COMP-1 | Target ~50-70 lines, readable in under 60 seconds |
| REQ-N2 | Section 7.3 | Verify all slash commands post-change |

---

## 2. Architecture

### 2.1 Content Classification

Audit of every current CLAUDE.md section against the classification criteria:

| Current Section | Lines | Classification | Rationale |
|---|---|---|---|
| Project Identity (name, type, version, mission) | 1-13 | **Keep (trim)** | Agent needs to know this is a framework. Version/status discoverable from git/CHANGELOG |
| Framework Development Context | 14-19 | **Keep** | Critical mental model shift -- "this IS the framework" (REQ-F2) |
| Current Focus / PLANNING.md | 20-30 | **Keep** | Non-obvious state management behavior (REQ-F6) |
| Architecture Overview / Framework Structure | 31-58 | **Remove** | Agent can glob/ls this. Directory tree is the most discoverable content possible |
| Command Architecture | 59-98 | **Remove** | Agent reads .claude/commands/ directly. Pattern visible from existing commands |
| Template Design Principles | 100-117 | **Relocate** | Not discoverable from code alone, but biases agent unnecessarily. Move to README |
| Development Workflow | 119-151 | **Remove** | Step-by-step guides for humans, not agent corrections. Discoverable from project structure |
| Core Framework Concepts | 153-220 | **Mixed** | Design-first philosophy is non-obvious (keep). DIP concept, Todoist rationale, git safety details discoverable from commands/templates |
| Development Commands | 222-260 | **Remove** | Setup instructions for humans. README material |
| Git Workflow | 262-282 | **Remove** | Conventional commits is standard. Agent already knows this pattern |
| Key Design Decisions | 284-308 | **Relocate** | Useful context but for humans, not agent corrections. README material |
| Testing Strategy | 310-323 | **Remove** | Human workflow, not agent steering |
| MVP Structure | 325-346 | **Remove** | Timeline/roadmap is human planning. Discoverable from Todoist/PLANNING.md |
| Important Files | 348-362 | **Keep (trim)** | Pointer to praxisity-foundation-plan.md is non-obvious. Others discoverable |
| References | 364-372 | **Remove** | All discoverable from the codebase |

**Result: ~373 lines down to ~50-70 lines.**

---

## 3. Components

### COMP-1: Minimized CLAUDE.md

**Purpose:** The reduced context file containing only corrective/non-obvious content

**Satisfies:** REQ-F1, REQ-F2, REQ-F3, REQ-F6, REQ-N1

**Responsibilities:**
- Establish that this repo IS the framework (mental model shift)
- Direct agent to PLANNING.md for session state
- Communicate design-first workflow constraint (command dependency chain)
- Brief reference to git safety (details in commands)
- Point to non-obvious files (praxisity-foundation-plan.md)

**Proposed structure:**
1. Project Identity (name, type, mission -- drop version/status)
2. Framework Development Context ("this IS the framework" block)
3. PLANNING.md State Management (reference + lifecycle behavior)
4. Design-First Workflow (command dependency chain -- non-obvious constraint)
5. Non-Obvious Files (just praxisity-foundation-plan.md)

---

### COMP-2: README.md Updates

**Purpose:** Destination for relocated human-facing content

**Satisfies:** REQ-F4

**Responsibilities:**
- Receive template design principles
- Receive key design decisions (why markdown commands, why templates not generators, why .praxisity/)
- Receive development workflow steps
- Receive setup instructions (Todoist MCP, testing)
- Receive MVP timeline/roadmap

---

### COMP-3: Updated claude.template.md

**Purpose:** Template for new projects that guides toward minimal content

**Satisfies:** REQ-F5

**Responsibilities:**
- Provide skeleton with only corrective/non-obvious sections
- Include guidance comments explaining the "corrections only" philosophy with examples of what belongs and what doesn't
- Discourage codebase descriptions, directory trees, dependency lists

---

## 6. Design Decisions

### DEC-1: Relocate to README, not inline comments

**Context:** Removed content needs a home. Options were README.md, inline code comments, ADRs, or a new docs file.

**Decision:** README.md is the primary relocation target.

**Rationale:** README is the natural home for human-facing project documentation -- design philosophy, setup instructions, workflow guides. It's already expected to contain this content.

**Alternatives Considered:**
- Inline comments in templates/commands: Scatters information, hard to maintain
- New CONTRIBUTING.md or docs/ folder: Over-engineering for current project size
- ADRs for everything: Wrong granularity -- most of this is guidance, not decisions

---

### DEC-2: Keep design-first workflow chain in CLAUDE.md

**Context:** The command dependency chain (/spec -> /architect -> /breakdown -> /define -> /build) could be considered discoverable by reading commands.

**Decision:** Keep it. This is a workflow constraint, not a codebase description.

**Rationale:** An agent asked to "implement feature X" would not naturally discover that it should run /spec first. This is a behavioral override -- exactly what the research says belongs in the file. The commands themselves don't document their ordering relationship.

---

### DEC-3: Strip Project Identity to minimum

**Context:** Current identity block has name, type, version, status, and mission. Version and status are git-discoverable.

**Decision:** Keep name, type, and mission only. Drop version and status.

**Rationale:** Name and type are read by /charter and /architect commands (REQ-N2). Mission provides alignment context. Version and status go stale and are available from CHANGELOG/git tags.

---

### DEC-4: Template should explain the philosophy, not just provide a skeleton

**Context:** The updated claude.template.md could either be a bare skeleton or include guidance comments explaining why minimal is better.

**Decision:** Include guidance comments explaining the "corrections only" philosophy with examples of what belongs and what doesn't.

**Rationale:** Without explanation, users will fall back to the common pattern of describing their entire codebase. The template needs to actively steer against this. Comments get removed in final docs per existing template conventions.

---

## 7. Implementation Considerations

### 7.1 Implementation Order

| Order | Component | Dependencies | Notes |
|---|---|---|---|
| 1 | COMP-2: README.md updates | None | Relocate content first -- ensure nothing is lost before removing |
| 2 | COMP-1: Minimized CLAUDE.md | COMP-2 | Safe to remove now that content is relocated |
| 3 | COMP-3: claude.template.md | COMP-1 | Use the minimized CLAUDE.md as the model for the template |
| 4 | Verification | COMP-1, COMP-2, COMP-3 | Invoke each slash command to confirm no breakage (REQ-N2) |

### 7.2 Risk Areas

| Risk | Impact | Mitigation |
|---|---|---|
| Slash commands break due to missing context | Commands fail or produce wrong output | DEC-3 retains project name/type/domain. Verify each command post-change |
| Agent loses non-obvious guidance we didn't identify | Agent makes mistakes it didn't make before | Conservative approach -- when in doubt, keep. Can always remove more later |
| README becomes bloated dumping ground | Trades one problem for another | Organize relocated content into clear sections. Only relocate what isn't code-discoverable |

### 7.3 Testing Strategy

| Level | Approach | Covers |
|---|---|---|
| Manual | Read minimized CLAUDE.md -- can you understand it in under 60 seconds? | REQ-N1 |
| Manual | Line count comparison (target: 50%+ reduction) | AC-1 |
| Command | Invoke /spec, /architect, /breakdown, /define, /charter, /new-project | REQ-N2, AC-5 |
| Review | Check every removed line against codebase -- is it discoverable or relocated? | AC-2 |

---

## 8. Out of Scope

**From Specification (inherited):**
- Progressive context expansion mechanisms
- Automated CLAUDE.md generation or /init-style tooling
- Changes to slash command logic
- Changes to CHARTER.md
- Benchmarking agent performance before/after

**Design-Specific Exclusions:**
- Restructuring README.md beyond adding relocated content
- Updating any slash command internals (only verifying they work)
- Creating new documentation files or folders

---

## 9. Open Questions

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| DQ-1 | Should the git safety section be a brief statement or include the specific rules? | Resolved | Brief reference only -- details live in /build command and .praxisity/safety/. Only include if commands don't cover it adequately. |

---

## 10. Appendices

### B. References

- [SPEC-001: CLAUDE.md Minimization](../specs/001-claude-md-minimization.md)
- [Gloaguen et al., 2026 - "Evaluating AGENTS.md"](https://arxiv.org/pdf/2602.11988)
- Theo Browne video discussion on agent MD minimization (YouTube, March 2026)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-03-20 | Andrew Robert Spenn | Initial draft |
