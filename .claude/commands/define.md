---
description: Generate a DIP (Detailed Implementation Prompt) for a task
tags: [planning, dip, implementation, prompts]
---

# Define Command

Generate a Detailed Implementation Prompt (DIP) for a specific task.

## Constraints

- Only include information relevant to the specific task
- Don't expand scope beyond what the design element specifies
- Auto-generate content from spec/design where possible, let user accept or modify
- Keep implementation steps concrete and verifiable
- Scope boundaries should be explicit - what to do AND what not to do

## Pre-Flight

1. Read PLANNING.md for session context; create if missing
2. Update PLANNING.md with /define as active command
3. Verify DIP template exists at `.praxisity/templates/dip.template.md`
4. Check for designs in `.plans/designs/` - if none exist, exit with guidance
5. Determine next DIP number from `.plans/prompts/`
6. Create `.plans/prompts/` directory if needed

## Task Selection

Prompt user to select what to create a DIP for:

1. **Design component (COMP-N)** - Select design, then select component
2. **Design interface (INT-N)** - Select design, then select interface
3. **Data entity (DATA-N)** - Select design, then select entity
4. **Todoist task** - Search or enter task ID, extract design references from task
5. **Custom task** - Describe task, specify related design and elements

For options 1-3: Parse the design to load the element's details and the linked spec.

For option 4: Requires Todoist MCP. Look for COMP-N, INT-N, DATA-N references in task.

For option 5: Prompt for task description and relevant design elements.

## DIP Content Gathering

### Auto-Generate from Design

Pull content automatically where possible:

- **Title**: Based on element type and name
- **Objective**: From element's purpose in design
- **Required reading**: Spec sections (REQ-F/N, UC, AC) the element satisfies, design sections (COMP, INT, DATA, DEC), charter principles/constraints
- **Implementation steps**: Standard pattern based on element type
- **Scope boundaries**: DO from responsibilities, DO NOT from out-of-scope items
- **Acceptance criteria**: From spec AC items that relate to this element

Show auto-generated content and let user accept or edit each section.

### Additional Prompts

- **Files in scope**: Which files/directories this task touches
- **Files out of scope**: Explicitly excluded files
- **Verification commands**: How to test the implementation (e.g., `npm test`, `pytest`)

## Review and Confirm

Show DIP summary with section counts. Offer to (y)es generate, (e)dit a section, or (c)ancel.

## Generate DIP File

1. Read the DIP template
2. Fill context table (DIP ID, task, spec link, design link, Todoist task if applicable)
3. Populate objective, required reading checklists, implementation steps
4. Fill technical requirements from design
5. Add scope boundaries (DO/DO NOT) and files
6. Add acceptance criteria table and verification commands
7. Generate commit instructions based on element type
8. Write to `.plans/prompts/[NUMBER]-[SLUG].md`

## Post-Save

1. Update PLANNING.md with DIP reference
2. If from Todoist task, optionally update task description with DIP link
3. Optionally commit to git: `dip([element]): add DIP-[N] for [ELEMENT]`

## Success Message

Confirm DIP was generated, summarize what it provides (reading sections, steps, criteria), and suggest next steps:
1. Review the DIP for completeness
2. Execute by reading and following instructions, using TodoWrite to track progress
3. Or run /build for guided execution with git safety
4. On completion, all acceptance criteria should pass

---

## Behavior Notes

- Each run creates a NEW DIP with incremented number
- Auto-generation: pulls from spec/design to reduce manual entry
- Flexibility: works from design elements, Todoist tasks, or custom descriptions
- TodoWrite integration: DIP includes instructions for progress tracking
- Traceability: links spec REQ-N → design COMP-N → DIP
- PLANNING.md integration: records DIP reference and next actions
