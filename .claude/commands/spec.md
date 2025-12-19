---
description: Create a new specification document
tags: [planning, specification, design-first]
---

# Spec Command

Create a specification document that defines WHAT you're building.

## Constraints

- Only gather information needed to populate the spec template
- Don't add requirements or sections beyond what the user provides
- Keep each prompt focused on one section at a time
- Accept the level of detail the user provides
- Section IDs (REQ-F1, UC-1, AC-1) are for traceability - generate them automatically

## Pre-Flight

1. Read PLANNING.md for session context; create if missing
2. Update PLANNING.md with /spec as active command
3. Check for CHARTER.md - if missing, warn and ask whether to continue
4. If charter exists, load it for context (mission, principles, constraints, out-of-scope)
5. Verify spec template exists at `.praxisity/templates/spec.template.md`
6. Determine next spec number from `.plans/specs/` (e.g., 001, 002)
7. Create `.plans/specs/` directory if needed

## Specification Flow

### Introduction

Explain that specifications define WHAT (not HOW), establish requirements and acceptance criteria, and will be referenced by designs and DIPs through section IDs.

### Gather Metadata

- **Title**: Brief descriptive title (e.g., "User Authentication", "Patient Intake Form")
- **Author**: Default to git user.name

Generate slug from title (lowercase, hyphens).

### Gather Spec Content

For each section, briefly explain what's needed, show a domain-relevant example, and prompt for input.

**Section 1: Problem Statement**
- What problem does this solve? Why does it matter?
- Should connect to charter mission if available

**Section 2: Goals and Objectives**
- Primary goal: one sentence describing the outcome
- Objectives: specific, measurable targets (collect as list with description + metric)

**Section 3: Requirements**
- Functional (REQ-F): what the solution does - collect with priority (MUST/SHOULD/COULD) and rationale
- Non-functional (REQ-N): qualities like performance, security - same format, optional

**Section 4: Use Cases**
- How will users interact with the solution?
- For each: title, actor, preconditions, flow steps, postconditions

**Section 5: Acceptance Criteria**
- How do we know it's successfully implemented?
- Format: Given [context], when [action], then [result]
- Each should trace to a requirement

**Section 6: Constraints**
- Inherit from charter if available
- Add any spec-specific constraints

**Section 7: Dependencies**
- What this spec depends on (other specs, external systems)
- What this spec enables (future work)

**Section 8: Out of Scope**
- What is explicitly NOT part of this spec
- Inherit from charter, add spec-specific exclusions
- Require at least one item to enforce boundary thinking

**Section 9: Open Questions**
- Uncertainties to resolve before or during implementation
- Optional

**Section 10: References**
- External docs, research, links
- Auto-add charter reference if exists

### Review and Confirm

Show summary with counts (requirements, use cases, acceptance criteria). Offer to (y)es save, (e)dit a section, or (c)ancel.

## Generate Specification File

1. Read the spec template
2. Fill metadata table (ID, title, status=Draft, author, dates, charter reference)
3. Populate each section with gathered content
4. Generate section IDs: REQ-F1, REQ-N1, UC-1, AC-1, OBJ-1, etc.
5. Remove HTML comments and empty placeholders
6. Write to `.plans/specs/[NUMBER]-[SLUG].md`

## Post-Save

1. Optionally create Todoist task for spec review (if MCP available)
2. Optionally commit to git with conventional format: `spec([slug]): add SPEC-[N]`
3. Update PLANNING.md with completion, active artifacts, and next steps

## Success Message

Confirm the spec was created, summarize what it defines (requirements, use cases, acceptance criteria), and suggest next steps:
1. Review for completeness
2. Get stakeholder alignment if needed
3. Create design document with /architect
4. Section IDs will be referenced by designs and DIPs

---

## Behavior Notes

- Each run creates a NEW spec with incremented number
- Out of scope is required to enforce boundary thinking
- Charter integration: loads context, inherits constraints and exclusions
- Dual-use design: section IDs enable both human reading and AI parsing
- PLANNING.md integration: reads context, tracks state, records completion
