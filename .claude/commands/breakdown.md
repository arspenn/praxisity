---
description: Break down a design into Todoist tasks
tags: [planning, tasks, todoist, breakdown]
---

# Breakdown Command

Decompose a design document into actionable Todoist tasks.

## Constraints

- Only create tasks for elements defined in the design
- Don't add tasks for features not in the spec or design
- Keep tasks small and concrete (<30 min each)
- Use clear action verbs (Create, Implement, Add, Write, Test)
- Avoid ambiguous tasks like "Figure out" or "Look into"

## Pre-Flight

1. Read PLANNING.md for session context; create if missing
2. Update PLANNING.md with /breakdown as active command
3. Check Todoist MCP availability - if not available, exit with setup guidance
4. Check for designs in `.plans/designs/` - if none exist, exit with guidance to run /architect first
5. List available designs with their IDs, titles, and linked specs
6. Prompt user to select a design
7. Parse selected design to extract components (COMP-N), interfaces (INT-N), data entities (DATA-N), and implementation order
8. Check for existing tasks for this design in Todoist - if found, offer to (a)dd more, (r)eplace all, or (c)ancel

## Breakdown Flow

### Introduction

Show which design is being broken down, list the components/interfaces/data entities, and explain that tasks will be created with ADHD-friendly sizing and design section references.

### Select Todoist Project

Show available projects and let user select one or create a new project.

### Select/Create Section

Prompt for section name (default: "Implementation"). Create if it doesn't exist.

### Generate Tasks

For each design element, generate appropriately-sized tasks:

**Component tasks (COMP-N):**
- Simple components (1-3 responsibilities): single "Implement COMP-N: [name]" task
- Complex components (4+ responsibilities): break into subtasks per responsibility plus scaffolding and testing

**Interface tasks (INT-N):**
- Define contract/schema
- Implement handler
- Add error handling and auth if applicable
- Integration tests

**Data entity tasks (DATA-N):**
- Create schema/model
- Implement validation
- Add migration if applicable

**Task naming convention:** `[Action] [ELEMENT-ID]: [brief description]`

### Review Generated Tasks

Show task summary with counts per element type. Display the full task list with descriptions.

Offer options:
- (c)reate all tasks in Todoist
- (e)dit - modify specific tasks
- (a)dd - add custom tasks
- (r)emove - remove specific tasks
- (x) cancel

### Create Tasks in Todoist

Create tasks in batches with:
- Design section reference in description
- Priority based on critical path (p2 for critical, p3 default)
- Labels: "praxisity", design ID

Preserve implementation order from design.

## Post-Creation

1. Update PLANNING.md with created task IDs and counts
2. Optionally commit PLANNING.md to git

## Success Message

Confirm tasks were created, show counts by element type, and suggest next steps:
1. Open Todoist to see tasks
2. Start with first task in order
3. For complex tasks, generate a DIP with /define
4. When implementing, use /build for git safety

---

## Behavior Notes

- Todoist MCP required - cannot function without it
- Micro-chunking: enforces <30 min task sizing
- Traceability: tasks reference COMP-N, INT-N, DATA-N
- Idempotent: checks for existing tasks, offers add/replace/cancel
- ADHD-informed: external storage, visual progress, small completable tasks
- PLANNING.md integration: records all created task IDs for reference
