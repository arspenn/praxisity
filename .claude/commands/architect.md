---
description: Create a design document for a specification
tags: [planning, design, architecture]
---

# Architect Command

Create a design document that defines HOW to implement a specification.

## Constraints

- Only gather information needed to populate the design template
- Don't add components, interfaces, or patterns beyond what the user specifies
- Keep prompts focused on one design element at a time
- Accept the user's architectural decisions without over-validating
- Section IDs (COMP-1, INT-1, DATA-1, DEC-1) are for traceability - generate them automatically

## Pre-Flight

1. Read PLANNING.md for session context; create if missing
2. Update PLANNING.md with /architect as active command
3. Check for specifications in `.plans/specs/` - if none exist, exit with guidance to run /spec first
4. List available specs and prompt user to select one
5. Parse selected spec to extract requirements (REQ-F/N), use cases (UC), acceptance criteria (AC), constraints, and out-of-scope items
6. Check for existing design for this spec - if found, offer to (v)iew, (c)reate new version, or (a)bort
7. Verify design template exists at `.praxisity/templates/design.template.md`
8. Determine next design number from `.plans/designs/`
9. Detect project domain from CLAUDE.md or ask (software/public-health/research/other)

## Design Flow

### Introduction

Show which spec is being designed for, list the requirements to address, and explain that designs define HOW to implement what the spec defined.

### Gather Metadata

- **Title**: Default to "[Spec Title] Design"
- **Author**: Default to git user.name

Generate slug from title.

### Gather Design Content

For each section, explain what's needed, show domain-relevant examples, and prompt for input.

**Section 1: Design Overview**
- Summary: 2-3 paragraphs describing the high-level approach
- Design principles: 2-4 principles guiding this design (e.g., "Fail fast, recover gracefully")

**Section 2: Architecture**

Questions vary by project domain:

*For SOFTWARE:*
- Architecture pattern (Layered, Microservices, Event-driven, etc.) and why
- Technology choices: layer/concern, technology, rationale

*For PUBLIC-HEALTH:*
- Intervention model: how does change happen (inputs → activities → outputs → outcomes)
- Delivery model: setting, frequency, duration, delivered by whom

*For RESEARCH:*
- Study design type and justification
- Methodological choices: aspect, approach, justification

**Section 3: Components**
- Show requirements to cover
- For each component: name, purpose, which requirements it satisfies, responsibilities, dependencies
- After all components, check that MUST requirements are covered (warn if gaps)

**Section 4: Interfaces**
- How components communicate with each other and external systems
- For each: name, what it connects, type (API/Event/File/Protocol/Handoff), contract description
- Can be skipped if components don't interact yet

**Section 5: Data Model**
- What data the solution manages
- For each entity: name, purpose, which components use it, key fields
- Can be skipped

**Section 6: Design Decisions**
- Key decisions and their rationale
- For each: title, what was decided, why, alternatives considered

**Section 7: Implementation Considerations**
- Build order: suggested sequence for implementing components
- Risk areas: risk, impact, mitigation
- Testing strategy: level, approach, what it covers

**Section 8: Out of Scope**
- Inherit from spec
- Add any design-specific exclusions

**Section 9: Open Questions**
- Unresolved design questions
- Optional

### Review and Confirm

Show summary with component count, interface count, data entity count, decision count, and requirements coverage. Offer to (y)es save, (e)dit a section, or (c)ancel.

## Generate Design File

1. Read the design template
2. Fill metadata table (ID, title, status=Draft, author, dates, spec reference)
3. Add requirements coverage matrix showing which components satisfy which requirements
4. Populate each section with gathered content
5. Generate section IDs: COMP-1, INT-1, DATA-1, DEC-1, etc.
6. Remove HTML comments, unused domain sections, and empty placeholders
7. Write to `.plans/designs/[NUMBER]-[SLUG].md`

## Post-Save

1. Optionally create Todoist task for design review (if MCP available)
2. Optionally commit to git: `design([slug]): add DESIGN-[N] for SPEC-[M]`
3. Update PLANNING.md with completion, active artifacts, and next steps

## Success Message

Confirm the design was created, summarize what it defines (components, interfaces, data, decisions), and suggest next steps:
1. Review for completeness - does every MUST requirement have a component?
2. Get peer review if applicable
3. Break down into tasks with /breakdown
4. Design IDs will be referenced by tasks and DIPs

---

## Behavior Notes

- Each run creates a NEW design with incremented number
- Can create multiple designs for same spec (versions, alternatives)
- Validates requirement coverage but warns rather than blocking
- Domain awareness: different architecture questions per project type
- Traceability: spec REQ-N → design COMP-N
- PLANNING.md integration: may auto-select spec if one is active
