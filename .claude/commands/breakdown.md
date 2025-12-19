---
description: Break down a design into Todoist tasks
tags: [planning, tasks, todoist, breakdown]
---

# Breakdown Command

Decompose a design document into actionable Todoist tasks.

## Purpose

The breakdown command translates designs into implementable tasks. It:
- Parses design components, interfaces, and data models
- Applies ADHD-friendly micro-chunking (<30 min tasks)
- Creates tasks in Todoist with proper structure
- Links tasks to design sections for traceability

A well-executed breakdown:
- Makes implementation approachable (small, concrete tasks)
- Maintains traceability (tasks reference COMP-N, INT-N, etc.)
- Enables progress tracking via Todoist
- Reduces cognitive load (no need to hold full design in memory)

**This command creates TASKS from designs. It requires a design that defines HOW.**

## Pre-Flight Checks

### Read PLANNING.md

```bash
cat PLANNING.md 2>/dev/null
```

**If PLANNING.md exists:**
- Parse current session context
- Check for active design reference
- Use as starting point if relevant

**If PLANNING.md doesn't exist:**
- Create fresh PLANNING.md with session start

### Update PLANNING.md

Write to PLANNING.md:
```markdown
## Session Context
- **Active Command:** /breakdown
- **Started:** [timestamp]
```

### Check for Todoist MCP

Attempt to use Todoist MCP:
```
mcp__todoist__user-info
```

**If Todoist MCP not available:**
- Show error: "Todoist MCP is required for /breakdown"
- Show: "Configure Todoist MCP in Claude Code settings"
- Show setup instructions from CLAUDE.md
- Exit command

**If Todoist MCP available:**
- Store user info for reference
- Show: "✓ Todoist connected as [user name]"

### Check for Designs

```bash
ls .plans/designs/*.md 2>/dev/null
```

**If no designs exist:**
- Show error: "No designs found in .plans/designs/"
- Show: "Create a design first with /architect"
- Exit command

**If designs exist:**
- List available designs with their IDs, titles, and linked specs

### Select Design

**Show:**
```
📋 Available Designs:

  1. DESIGN-001: [Title] (for SPEC-001)
  2. DESIGN-002: [Title] (for SPEC-002)
  ...

Which design should be broken down? (enter number or design ID):
```

**Validation:**
- Must select a valid design
- Parse selected design to extract:
  - Design ID and title
  - Linked spec ID
  - Components (COMP-1, COMP-2, etc.)
  - Interfaces (INT-1, INT-2, etc.)
  - Data entities (DATA-1, DATA-2, etc.)
  - Implementation order (if specified)
  - Risk areas

**Update PLANNING.md:**
```markdown
## Active Artifacts
- **Design:** DESIGN-[N]: [Title]
- **Spec:** SPEC-[N]: [Title]

## Gathered State
### Design Components
- COMP-1: [name] - [purpose summary]
- COMP-2: [name] - [purpose summary]
...
```

### Check for Existing Breakdown

Check if tasks already exist for this design in Todoist:
```
mcp__todoist__find-tasks with searchText "[DESIGN-NNN]"
```

**If tasks exist:**
- Show: "Found [N] existing tasks for DESIGN-[NNN]"
- Ask: "(a)dd more tasks, (r)eplace all, or (c)ancel?"
  - `a` - Continue, will add new tasks
  - `r` - Delete existing tasks first, then create new
  - `c` - Exit command

---

## Breakdown Flow

### Introduction

Show:
```
🔨 Task Breakdown

Breaking down: DESIGN-[ID]: [TITLE]
For spec: SPEC-[ID]: [TITLE]

Components to break down:
  COMP-1: [name]
  COMP-2: [name]
  ...

Interfaces:
  INT-1: [name]
  INT-2: [name]
  ...

Data entities:
  DATA-1: [name]
  ...

Tasks will be created in Todoist with:
- ADHD-friendly sizing (<30 min each)
- References to design sections
- Suggested implementation order

Let's create your task breakdown.
```

### Select/Create Todoist Project

**Prompt:**
"Which Todoist project should tasks go into?"

**Show available projects:**
```
mcp__todoist__find-projects
```

```
Existing projects:
  1. [Project Name]
  2. [Project Name]
  ...
  N. Create new project

Select project (number) or name for new project:
```

**If creating new:**
```
mcp__todoist__add-projects with projects array:
[{ "name": "[Project Name]", "viewStyle": "list" }]
```
- Store returned project ID

**Store as:** `TODOIST_PROJECT_ID`

**Update PLANNING.md:**
```markdown
### Todoist Target
- Project: [name] (ID: [id])
```

### Create/Select Section

**Prompt:**
"Which section for implementation tasks? (or Enter for 'Implementation')"

**Check existing sections:**
```
mcp__todoist__find-sections with projectId: "[TODOIST_PROJECT_ID]"
```

**If section exists:** Use its ID
**If section doesn't exist:** Create it:
```
mcp__todoist__add-sections with sections array:
[{ "name": "[Section Name]", "projectId": "[TODOIST_PROJECT_ID]" }]
```

**Store as:** `TODOIST_SECTION_ID`

---

### Generate Task Breakdown

For each component, interface, and data entity, generate micro-tasks.

**Micro-Chunking Principles:**
1. Each task completable in <30 minutes
2. Clear, concrete action verbs (Create, Implement, Add, Write, Test)
3. No ambiguous tasks ("Figure out", "Look into")
4. Dependencies noted in task descriptions
5. Reference design section in task name or description

#### Component Tasks

For each COMP-N:

**Analyze component:**
- Purpose
- Responsibilities (from design)
- Dependencies
- Complexity estimate

**Generate tasks:**

**Pattern for simple components (1-3 responsibilities):**
```
- [ ] Implement [COMP-N]: [component name]
      Description: Implements [brief purpose]. See DESIGN-[N] section COMP-[N].
      Dependencies: [list from design]
```

**Pattern for complex components (4+ responsibilities):**
Break into subtasks:
```
- [ ] Create [COMP-N] structure/scaffold
- [ ] Implement [COMP-N]: [responsibility 1]
- [ ] Implement [COMP-N]: [responsibility 2]
- [ ] Add [COMP-N]: [responsibility 3]
- [ ] Test [COMP-N]: unit tests
```

**Task naming convention:**
`[Action] [COMP-N]: [brief description]`

Examples:
- "Implement COMP-1: User authentication service"
- "Create COMP-2: Database connection handler"
- "Add COMP-1: Password hashing logic"
- "Test COMP-3: Input validation"

#### Interface Tasks

For each INT-N:

**Generate tasks:**
```
- [ ] Define INT-[N]: [interface name] contract
- [ ] Implement INT-[N]: [description]
- [ ] Test INT-[N]: integration test
```

**For complex interfaces (APIs, protocols):**
```
- [ ] Define INT-[N]: Request/response schema
- [ ] Implement INT-[N]: Endpoint handler
- [ ] Implement INT-[N]: Error handling
- [ ] Add INT-[N]: Authentication/authorization
- [ ] Test INT-[N]: Happy path
- [ ] Test INT-[N]: Error cases
```

#### Data Entity Tasks

For each DATA-N:

**Generate tasks:**
```
- [ ] Create DATA-[N]: [entity name] schema/model
- [ ] Implement DATA-[N]: Validation logic
- [ ] Add DATA-[N]: Migration (if applicable)
```

---

### Review Generated Tasks

**Show task summary:**
```
📋 Generated Task Breakdown

DESIGN-[ID]: [TITLE]

Component Tasks: [count]
  COMP-1: [task count] tasks
  COMP-2: [task count] tasks
  ...

Interface Tasks: [count]
  INT-1: [task count] tasks
  ...

Data Entity Tasks: [count]
  DATA-1: [task count] tasks
  ...

Total: [total count] tasks

Suggested order (from design):
  1. [First component/task]
  2. [Second component/task]
  ...
```

**Show full task list:**
```
Tasks to create:

1. [ ] [Task name]
   └─ [Description preview]

2. [ ] [Task name]
   └─ [Description preview]

...
```

**Update PLANNING.md:**
```markdown
## Generated Tasks
- Total: [count] tasks
- Components: [count]
- Interfaces: [count]
- Data: [count]

### Task List
1. [Task 1 name]
2. [Task 2 name]
...
```

**Prompt:**
"Review the tasks above. Options:"
"  (c)reate all tasks in Todoist"
"  (e)dit - modify task list"
"  (a)dd - add custom tasks"
"  (r)emove - remove specific tasks"
"  (x) cancel"

#### If Edit:
Show numbered list, ask which to edit, allow modification.

#### If Add:
**Prompt:** "Enter custom task (or blank to finish):"
- Collect task name
- Collect description (optional)
- Collect design reference (COMP-N, INT-N, or custom)
- Add to task list

#### If Remove:
Show numbered list, ask which to remove.

---

### Create Tasks in Todoist

**For each task, create in Todoist:**

```
mcp__todoist__add-tasks with tasks array:
[
  {
    "content": "[Task name]",
    "description": "[Description with design reference]",
    "projectId": "[TODOIST_PROJECT_ID]",
    "sectionId": "[TODOIST_SECTION_ID]",
    "priority": "[p3 default, p2 for critical path]",
    "labels": ["praxisity", "[design-id]"]
  },
  ...
]
```

**Batch creation:**
- Create tasks in batches of 10-20 for efficiency
- Show progress: "Creating tasks... [N/Total]"

**Order preservation:**
- If design specified implementation order, set task order accordingly
- First task in order gets created first (maintains Todoist order)

**Priority assignment:**
- Critical path items: p2 (high)
- Normal items: p3 (medium)
- Nice-to-have: p4 (low)

**Labels:**
- Add "praxisity" label for framework tracking
- Add design ID as label (e.g., "design-001")

---

### Update PLANNING.md with Results

```markdown
## Todoist Tasks Created

- **Project:** [name]
- **Section:** [name]
- **Total Tasks:** [count]
- **Created:** [timestamp]

### Task IDs
- [Task name]: [Todoist task ID]
- [Task name]: [Todoist task ID]
...

## Next Steps
- [ ] Start implementation with first task
- [ ] Generate DIPs for complex tasks: /define
- [ ] Track progress in Todoist
```

---

## Post-Creation Actions

### Git Commit (Optional)

**Prompt:**
"Commit PLANNING.md update to git? (yes/no)"

If yes:
```bash
git add PLANNING.md
git commit -m "plan(breakdown): create task breakdown for DESIGN-[ID]

[Total] tasks created in Todoist for [DESIGN_TITLE]"
```

---

## Success Message

```
✅ Task Breakdown Complete

DESIGN-[ID]: [TITLE]

Created [TOTAL] tasks in Todoist:
  - Project: [project name]
  - Section: [section name]

Task Summary:
  Components: [count] tasks
  Interfaces: [count] tasks
  Data Entities: [count] tasks

Labels applied: praxisity, [design-id]

📝 Next Steps:

1. Open Todoist to see your tasks
   [Project URL if available]

2. Start with the first task in order

3. For complex tasks, generate a DIP:
   /define [task reference]

   DIPs provide detailed implementation context
   linking specs and designs.

4. When implementing, use:
   /build

   This applies git safety and tracks progress.

📊 Track your progress in Todoist. Tasks reference
   design sections (COMP-N, INT-N) for context.
```

---

## Command Behavior Notes

**PLANNING.md Integration:**
- Reads existing state on start
- Updates throughout command execution
- Records all created task IDs for reference
- Enables session recovery if interrupted

**Todoist MCP Required:**
- This command cannot function without Todoist MCP
- Validates connection before proceeding
- Uses batch operations for efficiency

**Micro-Chunking:**
- Enforces <30 minute task sizing
- Breaks complex components into subtasks
- Uses concrete action verbs
- No ambiguous "figure out" tasks

**Traceability:**
- Tasks reference design sections (COMP-N, INT-N, DATA-N)
- Labels link tasks to specific design
- Descriptions include design file reference

**Idempotency:**
- Checks for existing tasks before creating
- Offers to add, replace, or cancel
- Safe to run multiple times

**Flexibility:**
- Can edit generated tasks before creation
- Can add custom tasks
- Can remove unwanted tasks
- Supports manual ordering adjustments

**ADHD-Informed Design:**
- External task storage (not in context)
- Visual progress tracking in Todoist
- Small, completable tasks
- Clear next actions
