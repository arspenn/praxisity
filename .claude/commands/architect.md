---
description: Create a design document for a specification
tags: [planning, design, architecture]
---

# Architect Command

Create a design document that defines HOW to implement a specification.

## Purpose

Design documents translate specifications (WHAT) into architecture (HOW). They define:
- Overall architecture and patterns
- Components and their responsibilities
- Interfaces between components
- Data models and structures
- Key design decisions with rationale
- Implementation guidance

A well-crafted design:
- Traces every element back to spec requirements
- Provides clear implementation guidance for DIPs
- Documents decisions and trade-offs
- Reduces ambiguity during implementation

**This command creates HOW. It requires a spec that defines WHAT.**

## Pre-Flight Checks

### Read PLANNING.md

```bash
cat PLANNING.md 2>/dev/null
```

**If PLANNING.md exists:**
- Parse current session context
- Check for active spec reference (use if available)
- Note any prior design work

**If PLANNING.md doesn't exist:**
- Create fresh PLANNING.md

**Update PLANNING.md:**
```markdown
## Session Context
- **Active Command:** /architect
- **Started:** [timestamp]
- **Task:** Create design document
```

### Check for Specifications

```bash
ls .plans/specs/*.md 2>/dev/null
```

**If no specs exist:**
- Show error: "No specifications found in .plans/specs/"
- Show: "Create a specification first with /spec"
- Exit command

**If specs exist:**
- List available specs with their IDs and titles
- Prompt user to select which spec to design for

### Select Specification

**Show:**
```
📋 Available Specifications:

  1. SPEC-001: [Title from file]
  2. SPEC-002: [Title from file]
  ...

Which specification is this design for? (enter number or spec ID):
```

**Validation:**
- Must select a valid spec
- Parse the selected spec file to extract:
  - Spec ID and title
  - Requirements (REQ-F1, REQ-F2, REQ-N1, etc.)
  - Use cases (UC-1, UC-2, etc.)
  - Acceptance criteria (AC-1, AC-2, etc.)
  - Out of scope items
  - Constraints

**Store as:** `SELECTED_SPEC` (object with all parsed data)

### Check for Design Template

```bash
ls -la .praxisity/templates/design.template.md
```

**If template doesn't exist:**
- Show error: "Design template not found at .praxisity/templates/design.template.md"
- Exit command

### Check for Existing Design

```bash
ls .plans/designs/*.md 2>/dev/null | grep -i "[spec-slug]"
```

**If design already exists for this spec:**
- Show: "A design for SPEC-[NNN] already exists: [filename]"
- Ask: "(v)iew existing, (c)reate new version, or (a)bort?"
  - `v` - Display existing design and exit
  - `c` - Continue to create new design (will have incremented number)
  - `a` - Exit command

### Determine Next Design Number

```bash
ls .plans/designs/*.md 2>/dev/null | sort -V | tail -1
```

**Logic:**
- If no designs exist: Next number is `001`
- If designs exist: Extract highest number, increment by 1, zero-pad to 3 digits

**Store as:** `DESIGN_NUMBER`

### Create Designs Directory if Needed

```bash
mkdir -p .plans/designs
```

### Detect Project Domain

**Check CLAUDE.md for project type, or ask:**
```
Project domain: (s)oftware, (p)ublic-health, (r)esearch, or (o)ther?
```

**Store as:** `PROJECT_DOMAIN`

This affects which architecture sections are shown.

---

## Design Creation Flow

### Introduction

Show:
```
🏗️ New Design Document

Creating design for: SPEC-[SPEC_ID]: [SPEC_TITLE]

Designs define HOW to implement what the spec defined.
You'll create components, interfaces, and data models
that satisfy the spec's requirements.

This will be saved as: .plans/designs/[DESIGN_NUMBER]-[name].md

Requirements to address:
  Functional: [count] (REQ-F1 through REQ-F[n])
  Non-Functional: [count] (REQ-N1 through REQ-N[n])
  Use Cases: [count] (UC-1 through UC-[n])

Let's design your solution.
```

---

### Gather Design Metadata

#### Design Title

**Prompt:**
"Design title (or press Enter for '[SPEC_TITLE] Design'):"

**Default:** "[SPEC_TITLE] Design"

**Store as:** `DESIGN_TITLE`

**Generate slug:**
- Convert to lowercase, replace spaces with hyphens, remove special characters

**Store as:** `DESIGN_SLUG`

#### Design Author

**Prompt:**
"Author name (or press Enter for git user.name):"

**Default:** Result of `git config user.name` or "Unknown"

**Store as:** `DESIGN_AUTHOR`

---

### Section 1: Design Overview

**Explanation:**
```
DESIGN OVERVIEW

Summarize your approach in 2-3 paragraphs:
- What is the high-level solution?
- What key principles guide this design?
- How does it address the spec's requirements?
```

**Prompt:**
"Describe your overall design approach:"

**Validation:**
- Must be at least 50 characters

**Store as:** `DESIGN_SUMMARY`

#### Design Principles

**Prompt:**
"What principles guide this design? (2-4 principles)"
"Enter one per line. Blank line when done."

**Examples to show based on domain:**

For SOFTWARE:
```
Examples:
- "Favor composition over inheritance"
- "Fail fast, recover gracefully"
- "Stateless services for horizontal scaling"
```

For PUBLIC-HEALTH:
```
Examples:
- "Community health workers as primary implementers"
- "Low-literacy friendly materials"
- "Integration with existing clinic workflow"
```

For RESEARCH:
```
Examples:
- "Minimize participant burden"
- "Maximize internal validity"
- "Reproducible analysis pipeline"
```

**Validation:**
- Must have at least 2 principles

**Store as:** `DESIGN_PRINCIPLES` (array)

---

### Section 2: Architecture

**The questions here depend on PROJECT_DOMAIN.**

#### For SOFTWARE:

**Architecture Pattern:**
```
ARCHITECTURE PATTERN

What high-level pattern will you use?
Common patterns: Layered, Microservices, Event-driven, Monolith,
                 Serverless, MVC, CQRS, Hexagonal
```

**Prompt:**
"What architecture pattern will you use?"

**Store as:** `ARCH_PATTERN`

**Prompt:**
"Why is this pattern appropriate for the requirements?"

**Store as:** `ARCH_RATIONALE`

**Technology Choices:**

**Prompt:**
"Enter your technology choices."
"Format: [Layer/Concern] | [Technology] | [Rationale]"
"Example: Frontend | React | Component reusability, team expertise"
"Blank line when done."

**Store as:** `TECH_CHOICES` (array of objects)

#### For PUBLIC-HEALTH:

**Intervention Model:**
```
INTERVENTION MODEL

Describe your intervention's logic model:
Inputs → Activities → Outputs → Outcomes → Impact
```

**Prompt:**
"Describe your intervention model (how does change happen?):"

**Store as:** `INTERVENTION_MODEL`

**Delivery Model:**

**Prompt:**
"Setting (where does intervention occur):"
**Store as:** `DELIVERY_SETTING`

**Prompt:**
"Frequency (how often):"
**Store as:** `DELIVERY_FREQUENCY`

**Prompt:**
"Duration (how long):"
**Store as:** `DELIVERY_DURATION`

**Prompt:**
"Delivered by (who implements):"
**Store as:** `DELIVERY_BY`

#### For RESEARCH:

**Study Design:**

**Prompt:**
"Study design type (e.g., RCT, Cohort, Qualitative, Mixed-methods):"

**Store as:** `STUDY_DESIGN`

**Prompt:**
"Why is this design appropriate for the research questions?"

**Store as:** `STUDY_RATIONALE`

**Methodology:**

**Prompt:**
"Enter methodological choices."
"Format: [Aspect] | [Approach] | [Justification]"
"Example: Sampling | Purposive | Maximum variation for diverse perspectives"
"Blank line when done."

**Store as:** `METHODOLOGY_CHOICES` (array)

---

### Section 3: Components

**Explanation:**
```
COMPONENTS

What are the major parts of your solution?
Each component gets an ID (COMP-1, COMP-2) for traceability.

For each component, you'll define:
- Purpose (what it does)
- Which requirements it satisfies
- Its responsibilities
- Dependencies
```

**Show requirements to address:**
```
Requirements to cover:
  REQ-F1: [brief description]
  REQ-F2: [brief description]
  ...
```

**Prompt:**
"How many major components will your design have?"

**For each component (1 to N):**

**Prompt:**
"Component [N] name:"
**Store as:** `COMP_NAME`

**Prompt:**
"Component [N] purpose (what it does):"
**Store as:** `COMP_PURPOSE`

**Prompt:**
"Which requirements does it satisfy? (comma-separated, e.g., REQ-F1, REQ-F2):"
**Validation:** Must reference valid requirement IDs from spec
**Store as:** `COMP_SATISFIES`

**Prompt:**
"Key responsibilities (one per line, blank when done):"
**Store as:** `COMP_RESPONSIBILITIES` (array)

**Prompt:**
"Dependencies (other components or external, one per line, blank if none):"
**Store as:** `COMP_DEPENDENCIES` (array)

**Collect all components as:** `COMPONENTS` (array of component objects)

**Validation after all components:**
- Check that all MUST requirements are covered by at least one component
- Warn if any MUST requirement is not addressed:
  "Warning: REQ-F[N] is not covered by any component. Continue anyway? (y/n)"

---

### Section 4: Interfaces

**Explanation:**
```
INTERFACES

How do components communicate with each other and external systems?
Each interface gets an ID (INT-1, INT-2) for traceability.

Types: API, Event, File, Protocol, Handoff
```

**Prompt:**
"How many interfaces will you define? (Enter 0 if components don't interact yet)"

**For each interface (1 to N):**

**Prompt:**
"Interface [N] name:"
**Store as:** `INT_NAME`

**Prompt:**
"Connects which components? (e.g., COMP-1 to COMP-2, or COMP-1 to External API):"
**Store as:** `INT_CONNECTS`

**Prompt:**
"Interface type (API/Event/File/Protocol/Handoff):"
**Store as:** `INT_TYPE`

**Prompt:**
"Brief description of the contract/interaction:"
**Store as:** `INT_CONTRACT`

**Collect all interfaces as:** `INTERFACES` (array)

---

### Section 5: Data Model

**Explanation:**
```
DATA MODEL

What data/information does your solution manage?
Each entity gets an ID (DATA-1, DATA-2) for traceability.
```

**Prompt:**
"How many data entities/datasets will you define? (Enter 0 to skip)"

**For each entity (1 to N):**

**Prompt:**
"Entity [N] name:"
**Store as:** `DATA_NAME`

**Prompt:**
"Entity [N] purpose (what this data represents):"
**Store as:** `DATA_PURPOSE`

**Prompt:**
"Which components use this? (comma-separated COMP-N IDs):"
**Store as:** `DATA_USED_BY`

**Prompt:**
"Key fields (one per line as 'name | type | description', blank when done):"
**Store as:** `DATA_FIELDS` (array)

**Collect all entities as:** `DATA_ENTITIES` (array)

---

### Section 6: Design Decisions

**Explanation:**
```
DESIGN DECISIONS

Document key decisions and their rationale.
These help future maintainers understand WHY, not just WHAT.
Each gets an ID (DEC-1, DEC-2) for reference.
```

**Prompt:**
"How many key design decisions should be documented?"

**For each decision (1 to N):**

**Prompt:**
"Decision [N] title (brief name):"
**Store as:** `DEC_TITLE`

**Prompt:**
"What was decided?"
**Store as:** `DEC_DECISION`

**Prompt:**
"Why? (rationale):"
**Store as:** `DEC_RATIONALE`

**Prompt:**
"What alternatives were considered? (one per line, blank if none):"
**Store as:** `DEC_ALTERNATIVES` (array)

**Collect all decisions as:** `DECISIONS` (array)

---

### Section 7: Implementation Considerations

**Explanation:**
```
IMPLEMENTATION GUIDANCE

Help implementers by specifying:
- Suggested build order
- Risk areas to watch
- Testing strategy
```

#### Implementation Order

**Prompt:**
"What order should components be built? (List COMP-N IDs in order, comma-separated):"
**Example:** "COMP-1, COMP-2, COMP-3"

**Store as:** `IMPL_ORDER` (array)

#### Risk Areas

**Prompt:**
"What are the risky or complex parts of this design?"
"Format: [Risk] | [Impact] | [Mitigation]"
"Blank line when done (or Enter to skip)."

**Store as:** `IMPL_RISKS` (array)

#### Testing Strategy

**Prompt:**
"How should this design be tested?"
"Format: [Level: Unit/Integration/System] | [Approach] | [Covers]"
"Blank line when done (or Enter to skip)."

**Store as:** `IMPL_TESTING` (array)

---

### Section 8: Out of Scope

**Explanation:**
```
OUT OF SCOPE

What does this design explicitly NOT cover?
Inherit from spec and add design-specific exclusions.
```

**Show inherited from spec:**
```
From specification (will be inherited):
- [item 1]
- [item 2]
```

**Prompt:**
"Any additional design-specific exclusions? (one per line, blank if none):"

**Store as:** `OUT_OF_SCOPE_DESIGN` (array, can be empty)

---

### Section 9: Open Questions

**Prompt:**
"Any unresolved design questions? (one per line, blank to skip):"

**Store as:** `OPEN_QUESTIONS` (array, can be empty)

---

## Review and Confirmation

**Show design summary:**

```
🏗️ Design Summary
=================

ID: DESIGN-[DESIGN_NUMBER]
Title: [DESIGN_TITLE]
For Spec: SPEC-[SPEC_ID]: [SPEC_TITLE]
Author: [DESIGN_AUTHOR]

ARCHITECTURE:
Pattern: [ARCH_PATTERN or STUDY_DESIGN or "See intervention model"]

COMPONENTS: [count] defined
  [list COMP-1: name, COMP-2: name, etc.]

INTERFACES: [count] defined

DATA ENTITIES: [count] defined

DESIGN DECISIONS: [count] documented

REQUIREMENTS COVERAGE:
  ✓ [count] requirements addressed
  [⚠ [count] requirements not explicitly covered - if any]

File: .plans/designs/[DESIGN_NUMBER]-[DESIGN_SLUG].md
```

**Prompt:**
"Does this look correct? (y)es to save, (e)dit section, (c)ancel:"

- `y` - Proceed to save
- `e` - Ask which section (1-9), re-prompt for that section
- `c` - Exit without saving

---

## Generating Design File

### Step 1: Read Template

Read `.praxisity/templates/design.template.md`

### Step 2: Fill Template

**Metadata table:**
- `DESIGN-NNN` → `DESIGN-[DESIGN_NUMBER]`
- `[Descriptive title]` → `[DESIGN_TITLE]`
- Status → `Draft`
- Author → `[DESIGN_AUTHOR]`
- Dates → Current date (YYYY-MM-DD)

**Specification References table:**
- Add row for `SELECTED_SPEC` with requirements list

**Section 1 (Overview):**
- 1.1 → `DESIGN_SUMMARY`
- 1.2 → Bullet list from `DESIGN_PRINCIPLES`
- 1.3 Requirements Coverage → Generate matrix from components' `COMP_SATISFIES`

**Section 2 (Architecture):**
- Use domain-appropriate subsections
- Fill from `ARCH_PATTERN`, `TECH_CHOICES`, `INTERVENTION_MODEL`, etc.
- Remove non-applicable domain sections

**Section 3 (Components):**
- Generate COMP-1, COMP-2, etc. from `COMPONENTS` array
- Include purpose, satisfies, responsibilities, dependencies

**Section 4 (Interfaces):**
- Generate INT-1, INT-2, etc. from `INTERFACES` array
- Include connects, type, contract

**Section 5 (Data Model):**
- Generate DATA-1, DATA-2, etc. from `DATA_ENTITIES` array
- Include purpose, used by, fields table

**Section 6 (Design Decisions):**
- Generate DEC-1, DEC-2, etc. from `DECISIONS` array
- Include context (from decision), decision, rationale, alternatives

**Section 7 (Implementation):**
- 7.1 Order → Table from `IMPL_ORDER`
- 7.2 Risks → Table from `IMPL_RISKS`
- 7.3 Testing → Table from `IMPL_TESTING`
- 7.4, 7.5 → Leave as prompts or generate from non-functional requirements

**Section 8 (Out of Scope):**
- Inherited → From spec
- Design-specific → From `OUT_OF_SCOPE_DESIGN`

**Section 9 (Open Questions):**
- Generate DQ-1, DQ-2, etc. from `OPEN_QUESTIONS`

**Section 10 (Appendices):**
- Add reference to spec file
- Keep glossary as placeholder

**Revision History:**
- Add: `0.1 | [DATE] | [AUTHOR] | Initial draft`

**Remove:**
- HTML comments
- Unused domain sections
- Empty placeholder text

### Step 3: Write File

Write to: `.plans/designs/[DESIGN_NUMBER]-[DESIGN_SLUG].md`

Show: "✓ Design saved to .plans/designs/[DESIGN_NUMBER]-[DESIGN_SLUG].md"

---

## Post-Save Actions

### Create Todoist Task (Optional)

If Todoist MCP is available:

**Prompt:**
"Create Todoist task to track this design? (yes/no)"

If yes:
- Find or create "Design" section in project
- Create task: "Review and approve: DESIGN-[NUMBER] [TITLE]"
- Description: "Design for SPEC-[SPEC_ID] needs review before breakdown.\nFile: .plans/designs/[filename]"
- Priority: p2 (high)
- Label: "design"

Show: "✓ Created design review task in Todoist"

### Git Commit (Optional)

**Prompt:**
"Commit design to git? (yes/no)"

If yes:
```bash
git add .plans/designs/[DESIGN_NUMBER]-[DESIGN_SLUG].md
git commit -m "design([DESIGN_SLUG]): add DESIGN-[DESIGN_NUMBER] for SPEC-[SPEC_ID]

Design document defining architecture for [SPEC_TITLE]."
```

Show: "✓ Committed design to git"

---

## Success Message

```
✅ Design Created

DESIGN-[DESIGN_NUMBER]: [DESIGN_TITLE]
For: SPEC-[SPEC_ID]: [SPEC_TITLE]
File: .plans/designs/[DESIGN_NUMBER]-[DESIGN_SLUG].md

This design defines:
- [count] components (COMP-1 through COMP-[n])
- [count] interfaces (INT-1 through INT-[n])
- [count] data entities (DATA-1 through DATA-[n])
- [count] design decisions (DEC-1 through DEC-[n])

📝 Next Steps:

1. Review the design for completeness
   - Does every MUST requirement have a component?
   - Are interfaces clearly defined?
   - Are risks identified and mitigated?

2. Get stakeholder/peer review (if applicable)

3. Break down into implementation tasks:
   /breakdown

   This will create Todoist tasks for each component
   and interface, referencing the design sections.

4. Design IDs will be used by:
   - /breakdown (tasks reference COMP-N, INT-N)
   - /define (DIPs cite spec REQ-N and design COMP-N)
   - /build (implementation follows design)

📚 Designs are living documents. Update as implementation reveals insights.
```

### Update PLANNING.md

```markdown
## Completed

- **Design:** Created DESIGN-[NUMBER]: [TITLE]
- **For Spec:** SPEC-[SPEC_ID]: [SPEC_TITLE]
- **File:** .plans/designs/[filename]
- **Components:** [count] | **Interfaces:** [count] | **Data:** [count]
- **Timestamp:** [completion time]

## Active Artifacts
- **Spec:** SPEC-[SPEC_ID]: [SPEC_TITLE]
- **Design:** DESIGN-[NUMBER]: [TITLE]

## Next Steps
- [ ] Review design for completeness
- [ ] Break down into tasks: /breakdown
```

---

## Command Behavior Notes

**Idempotency:**
- Each run creates a NEW design with incremented number
- Can create multiple designs for same spec (versions/alternatives)
- Safe to run multiple times

**Flexibility:**
- Interfaces can be skipped (0)
- Data entities can be skipped (0)
- Open questions can be empty
- But components are required (at least 1)

**Validation:**
- Checks that MUST requirements are covered
- Warns but doesn't block if coverage incomplete
- Ensures traceability from spec to design

**Spec Integration:**
- Requires spec to exist
- Loads and displays spec requirements
- Validates requirement references
- Inherits out-of-scope items

**Domain Awareness:**
- Different architecture questions for software/health/research
- Removes non-applicable sections from output
- Examples tailored to domain

**Dual-Use Design:**
- Section IDs (COMP-N, INT-N, DATA-N, DEC-N) enable AI parsing
- Human-readable explanations throughout
- Traceability from spec REQ-N to design COMP-N

**PLANNING.md Integration:**
- Reads existing context on start (may auto-select spec if active)
- Updates with command start and gathered state
- Records completion and active artifacts
- Suggests next steps
- Enables session recovery if interrupted
