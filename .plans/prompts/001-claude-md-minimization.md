# DIP-001: CLAUDE.md Minimization Implementation

> **For AI Agent:** This is a Detailed Implementation Prompt. Follow these instructions precisely.
> Read all referenced documents before beginning implementation.
>
> **TodoWrite Integration:** Use Claude's TodoWrite tool to track progress through this DIP.
> Create todos from the Implementation Steps below and mark them complete as you progress.

## Context

| Field | Value |
|-------|-------|
| DIP ID | DIP-001 |
| Task | Minimize CLAUDE.md to corrective/non-obvious content, relocate removed content to README.md, update claude.template.md |
| Spec | [SPEC-001](../specs/001-claude-md-minimization.md) |
| Design | [DESIGN-001](../designs/001-claude-md-minimization.md) |
| Todoist Task | N/A |
| Created | 2026-03-20 |

## Objective

Minimize CLAUDE.md from ~373 lines to ~50-70 lines by removing agent-discoverable content and relocating human-facing content to README.md, then update claude.template.md to guide new projects toward the same minimal philosophy.

## Required Reading

Before implementation, read and understand these sections:

### From Specification (SPEC-001)
- [ ] Section 3.1: REQ-F1 - Audit and classify every CLAUDE.md section
- [ ] Section 3.1: REQ-F2 - Retain mental model shifts agent cannot infer
- [ ] Section 3.1: REQ-F3 - Retain safety guardrails and workflow constraints
- [ ] Section 3.1: REQ-F4 - Relocate removed content to appropriate artifacts
- [ ] Section 3.1: REQ-F5 - Update claude.template.md for minimal content
- [ ] Section 3.1: REQ-F6 - Preserve PLANNING.md reference
- [ ] Section 3.2: REQ-N1 - Readable in under 60 seconds
- [ ] Section 3.2: REQ-N2 - Don't break slash command functionality

### From Design (DESIGN-001)
- [ ] Section 2.1: Content Classification table (keep/remove/relocate decisions for every section)
- [ ] Section 3: COMP-1 - Minimized CLAUDE.md structure
- [ ] Section 3: COMP-2 - README.md updates
- [ ] Section 3: COMP-3 - Updated claude.template.md
- [ ] Section 6: DEC-1 - Relocate to README, not inline comments
- [ ] Section 6: DEC-2 - Keep design-first workflow chain
- [ ] Section 6: DEC-3 - Strip Project Identity to minimum (name, type, mission only)
- [ ] Section 6: DEC-4 - Template should explain the philosophy

### From Charter
- [ ] Principles: Design before implementation
- [ ] Principles: Self-documenting
- [ ] Constraints: Strict MVP discipline

## Implementation Instructions

> **Agent Action:** Before starting, use TodoWrite to create todos from these steps:
> ```
> TodoWrite([
>   { content: "Read required spec/design sections", status: "pending", activeForm: "Reading documentation" },
>   { content: "Step 1: Relocate content to README.md", status: "pending", activeForm: "Relocating content to README.md" },
>   { content: "Step 2: Minimize CLAUDE.md", status: "pending", activeForm: "Minimizing CLAUDE.md" },
>   { content: "Step 3: Update claude.template.md", status: "pending", activeForm: "Updating claude.template.md" },
>   { content: "Step 4: Verify slash commands", status: "pending", activeForm: "Verifying slash commands" },
>   { content: "Verify acceptance criteria", status: "pending", activeForm: "Verifying acceptance criteria" },
>   { content: "Complete safety checklist and commit", status: "pending", activeForm: "Completing safety checklist" }
> ])
> ```

### Step 1: Relocate Content to README.md

Add the following content to README.md in appropriate sections. Do not restructure existing README content -- add new sections after "Contributing".

**Content to relocate (from current CLAUDE.md):**

1. **Template Design Principles** (lines 100-117) -- Add as new section "## Template Design Principles"
   - Self-documenting, placeholder clarity, example-driven, domain-flexible, remove guidance, opinionated but adaptable, dual-use design
   - Include the template testing checklist

2. **Key Design Decisions** (lines 284-308) -- Add as new section "## Design Decisions"
   - Why Markdown Commands?
   - Why Templates Not Generators?
   - Why Separate .praxisity/ Directory?

3. **Development Workflow** (lines 119-151) -- Add as new section "## Development Workflow"
   - For Framework Development (5 steps)
   - For Command Implementation (6 steps)
   - For Template Creation (6 steps)

4. **Development Commands** (lines 222-260) -- Merge into existing README "Setup" section or add as "## Development"
   - Todoist MCP setup (already in README -- skip if duplicate)
   - Testing commands
   - Document generation (future)

5. **MVP Structure** (lines 325-346) -- Add as new section "## Roadmap"
   - Week 1-4 breakdown

6. **Command Authoring for Opus 4.5** (lines 89-98) -- Add under Development Workflow or as subsection
   - Explicit constraints, calmer language, condensed pre-flight, etc.

**Input:** Current CLAUDE.md (lines 100-346), current README.md
**Output:** README.md with relocated sections added
**Verify:** Every piece of relocated content from CLAUDE.md exists somewhere in README.md

### Step 2: Minimize CLAUDE.md

Replace the entire CLAUDE.md with the following minimal structure. This is the target content:

```markdown
# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Identity

**Name:** Praxisity Framework
**Type:** Development Framework / Tooling
**Mission:** Build a design-first workflow framework enabling consistent, structured planning and execution for multi-disciplinary projects through AI-assisted tooling.

## Framework Development Context

This repository IS the Praxisity framework itself. We are building the tool, not using it (yet). Commands and templates created here will be used by future projects. Quality and thoughtfulness in design are paramount.

Once core commands exist, we'll use Praxisity to build Praxisity (eating our own dog food). The `.plans/` directory contains our own specifications and designs.

## Current Focus

**For current tasks and session state, see `PLANNING.md`.**

PLANNING.md contains:
- Active command/task context
- Gathered state during command execution
- Completed work this session
- Next steps

This separation keeps CLAUDE.md stable while PLANNING.md handles dynamic session state.

Commands read PLANNING.md on start, update it during execution, record completion and next steps. It is archived to `.plans/archive/PLANNING-[timestamp].md` at task end or new session.

## Design-First Workflow

Every Praxisity project follows: Specify -> Design -> Breakdown -> Implement

This framework enforces that workflow through command dependencies:
- `/spec` creates specifications
- `/architect` requires specs to exist
- `/breakdown` requires designs to exist
- `/define` requires both specs and designs
- `/build` requires DIPs to exist

## Important Files

**praxisity-foundation-plan.md** - Source of truth for MVP scope. Reference when making decisions. Will be removed by `/new-project` for end users.
```

**Input:** Current CLAUDE.md (373 lines)
**Output:** Minimized CLAUDE.md (~50 lines)
**Verify:**
- Line count is under 80 lines (target: 50%+ reduction from 373)
- Contains: project identity (name, type, mission), framework context, PLANNING.md reference, design-first workflow, important files pointer
- Does NOT contain: directory trees, command patterns, template principles, git workflow, development commands, MVP timeline, testing strategy, references section

### Step 3: Update claude.template.md

Rewrite `.praxisity/templates/claude.template.md` to reflect the minimal philosophy. The new template should:

1. Keep the same placeholder convention ([BRACKETS])
2. Replace the comprehensive structure with a minimal one matching COMP-1's structure
3. Add guidance comments explaining WHY minimal is better, with examples of what belongs and what doesn't
4. Remove: Architecture Overview, Development Commands, Domain Conventions, Git Safety details, Key Patterns, References sections
5. Keep: Project Identity, Current Focus/PLANNING.md, Workflow Rules (trimmed), Critical Context (for genuine corrections only)

The key guidance comment should explain:
- This file is for behavioral corrections, not codebase documentation
- If the agent can discover it by reading code, it doesn't belong here
- Add content only when you observe the agent consistently getting something wrong
- Research shows comprehensive context files increase costs by 20%+ with marginal benefit

**Input:** Current claude.template.md (233 lines)
**Output:** Minimal claude.template.md (~80-100 lines)
**Verify:** Template contains guidance comments explaining the minimal philosophy. Template does not encourage directory trees, dependency lists, or comprehensive architecture descriptions.

### Step 4: Verify Slash Commands

Check that commands relying on CLAUDE.md still have what they need:

1. `/architect` (line 28) reads CLAUDE.md for domain detection -- **Project Identity section retained with Type field? Yes.**
2. `/charter` (lines 23, 65, 89) reads CLAUDE.md for project name/type and updates mission -- **Project Identity retained with Name, Type, Mission? Yes.**
3. `/new-project` (lines 43-47) generates CLAUDE.md from template -- **Template updated in Step 3? Yes.**

No commands parse specific content sections beyond metadata. All metadata fields are retained.

**Input:** Minimized CLAUDE.md, updated template
**Output:** Confirmation that all commands have the data they need
**Verify:** Each command listed above can extract project name, type, domain, and mission from the minimized CLAUDE.md

## Technical Requirements

### Must Implement
- [ ] All content classified as "relocate" in DESIGN-001 Section 2.1 exists in README.md
- [ ] Minimized CLAUDE.md contains only keep-classified content from DESIGN-001 Section 2.1
- [ ] claude.template.md includes philosophy guidance comments per DEC-4
- [ ] Project Identity retains name, type, and mission per DEC-3

### Must Satisfy
| Requirement | How to Satisfy |
|-------------|----------------|
| REQ-F1 | Classification table in DESIGN-001 Section 2.1 is the audit -- implement its decisions |
| REQ-F2 | "This repository IS the Praxisity framework" block retained in minimized CLAUDE.md |
| REQ-F3 | Git safety details removed from CLAUDE.md -- they live in /build command and .praxisity/safety/ |
| REQ-F4 | All relocated content added to README.md in Step 1 before removal in Step 2 |
| REQ-F5 | claude.template.md rewritten with minimal philosophy in Step 3 |
| REQ-F6 | PLANNING.md reference and lifecycle retained in minimized CLAUDE.md |
| REQ-N1 | ~50 lines is readable well under 60 seconds |
| REQ-N2 | Step 4 verifies command compatibility |

## Scope Boundaries

### DO (In Scope)
- Add relocated content to README.md
- Rewrite CLAUDE.md to minimal version
- Rewrite claude.template.md with minimal philosophy
- Verify slash commands can extract needed metadata

### DO NOT (Out of Scope)
- Do not modify any slash commands
- Do not modify CHARTER.md
- Do not restructure existing README.md content (only add sections)
- Do not create new files or directories
- Do not implement progressive context expansion
- Do not benchmark agent performance
- Do not refactor unrelated code
- Do not modify files outside the scope listed below

### Files in Scope
```
CLAUDE.md
README.md
.praxisity/templates/claude.template.md
```

### Files Out of Scope
```
CHARTER.md
.claude/commands/ (all command files)
.praxisity/safety/
.praxisity/templates/ (all templates except claude.template.md)
.plans/ (specs, designs, decisions -- read only)
```

## Acceptance Criteria

All criteria must pass for this DIP to be considered complete.

| ID | Criterion | Test |
|----|-----------|------|
| AC-1 | Given the minimized CLAUDE.md, when line count is measured, then it is at least 50% smaller than 373 lines | `wc -l CLAUDE.md` returns under 187 |
| AC-2 | Given every removed section, when checked against README.md, then relocated content exists there | Manual review: template principles, design decisions, dev workflow, dev commands, MVP structure all in README |
| AC-3 | Given the minimized CLAUDE.md, when read, then every line is a behavioral correction, safety guardrail, or non-obvious context | Manual review: no directory trees, no command patterns, no dependency lists |
| AC-4 | Given claude.template.md, when reviewed, then it guides toward minimal corrective content | Template contains philosophy comments explaining what belongs and what doesn't |
| AC-5 | Given the minimized CLAUDE.md, when slash commands are checked, then project name/type/domain/mission are extractable | Verify Project Identity section contains Name, Type, Mission fields |
| AC-6 | Given the minimized CLAUDE.md, when an agent reads it, then it is not biased toward irrelevant patterns | No mention of specific technologies, patterns, or architecture details that could bias behavior |

### Verification Commands
```bash
# Check line count (target: under 187, ideal: ~50-70)
wc -l CLAUDE.md

# Verify project identity fields exist
grep -c "Name:\|Type:\|Mission:" CLAUDE.md

# Verify PLANNING.md reference exists
grep -c "PLANNING.md" CLAUDE.md

# Verify design-first workflow exists
grep -c "spec\|architect\|breakdown\|define\|build" CLAUDE.md

# Verify template has philosophy guidance
grep -c "behavioral correction\|agent can discover\|corrective" .praxisity/templates/claude.template.md
```

## Safety Checklist

Before committing, verify:

- [ ] No secrets, keys, or credentials in code
- [ ] No `git add .` or `git add -A` used
- [ ] All new files explicitly added
- [ ] Conventional commit message prepared
- [ ] No unrelated changes included

## Commit Instructions

When implementation is complete:

```bash
# Stage only files in scope
git add CLAUDE.md README.md .praxisity/templates/claude.template.md

# Commit with conventional format
git commit -m "refactor(claude-md): minimize CLAUDE.md to corrective content only

Implements DIP-001: CLAUDE.md Minimization
Satisfies: REQ-F1, REQ-F2, REQ-F3, REQ-F4, REQ-F5, REQ-F6, REQ-N1, REQ-N2

- Reduce CLAUDE.md from ~373 to ~50 lines
- Relocate human-facing content to README.md
- Update claude.template.md with minimal philosophy
- Informed by Gloaguen et al. 2026 research on agent MD effectiveness"
```

**Commit type:** refactor
**Scope:** claude-md

## Completion Checklist

> **Agent Action:** Work through this checklist, marking each item in your TodoWrite as you go.

- [ ] All implementation steps completed (all step todos marked `completed`)
- [ ] All acceptance criteria verified (verification commands passed)
- [ ] Safety checklist passed (no secrets, explicit git adds)
- [ ] Code committed with proper message
- [ ] PLANNING.md updated with completion status
- [ ] TodoWrite cleared or marked all complete

## Notes

- The content classification in DESIGN-001 Section 2.1 is the authoritative source for keep/remove/relocate decisions. If in doubt about a specific line, refer to that table.
- When writing the minimized CLAUDE.md, the exact wording in Step 2 is a starting point -- adjust for clarity but do not add back removed content.
- The claude.template.md rewrite in Step 3 is the most creative step -- use the minimized CLAUDE.md as a model but ensure the template has guidance comments explaining the philosophy (per DEC-4).
- README.md additions should feel natural alongside existing content. Avoid dumping content -- organize it into sections that flow with what's already there.

---

**End of DIP-001**

> **Final Agent Actions:**
> 1. Ensure all TodoWrite items are marked `completed`
> 2. Update PLANNING.md with:
>    - DIP completion status
>    - Any deviations or decisions made
>    - Next suggested action
