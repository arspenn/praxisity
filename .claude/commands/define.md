---
description: Generate a DIP (Detailed Implementation Prompt) for a task
tags: [planning, dip, implementation, prompts]
---

# Define Command

Generate a Detailed Implementation Prompt (DIP) for a specific task.

## Purpose

DIPs provide complete context for AI agent implementation. They:
- Link task to relevant spec sections (REQ-F/N, UC, AC)
- Link task to relevant design sections (COMP, INT, DATA, DEC)
- Define explicit scope boundaries (DO and DO NOT)
- Include acceptance criteria and verification steps
- Integrate with TodoWrite for progress tracking
- Ensure consistent, high-quality implementation

A well-crafted DIP:
- Reduces AI variability (same input → same quality output)
- Prevents scope creep (explicit boundaries)
- Enables verifiable completion (testable criteria)
- Maintains traceability (spec → design → DIP → code)

**This command creates INSTRUCTIONS. It requires a design that defines HOW.**

## Pre-Flight Checks

### Read PLANNING.md

```bash
cat PLANNING.md 2>/dev/null
```

**If PLANNING.md exists:**
- Parse current session context
- Check for active spec/design references
- Look for existing task breakdown info

**If PLANNING.md doesn't exist:**
- Create fresh PLANNING.md

### Update PLANNING.md

```markdown
## Session Context
- **Active Command:** /define
- **Started:** [timestamp]
```

### Check for DIP Template

```bash
ls -la .praxisity/templates/dip.template.md
```

**If template doesn't exist:**
- Show error: "DIP template not found at .praxisity/templates/dip.template.md"
- Exit command

### Check for Designs

```bash
ls .plans/designs/*.md 2>/dev/null
```

**If no designs exist:**
- Show error: "No designs found in .plans/designs/"
- Show: "Create a design first with /architect"
- Exit command

### Determine Next DIP Number

```bash
ls .plans/prompts/*.md 2>/dev/null | sort -V | tail -1
```

**Logic:**
- If no DIPs exist: Next number is `001`
- If DIPs exist: Extract highest number, increment by 1, zero-pad to 3 digits

**Store as:** `DIP_NUMBER`

### Create Prompts Directory if Needed

```bash
mkdir -p .plans/prompts
```

---

## Task Selection Flow

### Introduction

Show:
```
📝 Generate DIP (Detailed Implementation Prompt)

DIPs provide complete context for AI implementation.
They link specs, designs, and acceptance criteria
into a single, executable instruction set.

Select what to create a DIP for:
  1. Design component (COMP-N)
  2. Design interface (INT-N)
  3. Data entity (DATA-N)
  4. Todoist task
  5. Custom task

Enter selection (1-5):
```

### Option 1-3: Design Element

**If selecting design element (COMP, INT, or DATA):**

**Show available designs:**
```
Available Designs:
  1. DESIGN-001: [Title]
  2. DESIGN-002: [Title]
  ...

Select design (number):
```

**Parse selected design to extract:**
- Components (COMP-1, COMP-2, etc.)
- Interfaces (INT-1, INT-2, etc.)
- Data entities (DATA-1, DATA-2, etc.)
- Linked spec ID

**Store as:** `SELECTED_DESIGN`

**Show available elements based on selection type:**

For COMP:
```
Components in DESIGN-[N]:
  COMP-1: [name] - [purpose]
  COMP-2: [name] - [purpose]
  ...

Select component (e.g., COMP-1):
```

For INT:
```
Interfaces in DESIGN-[N]:
  INT-1: [name] - [connects]
  INT-2: [name] - [connects]
  ...

Select interface (e.g., INT-1):
```

For DATA:
```
Data Entities in DESIGN-[N]:
  DATA-1: [name] - [purpose]
  DATA-2: [name] - [purpose]
  ...

Select data entity (e.g., DATA-1):
```

**Store as:** `SELECTED_ELEMENT` (e.g., "COMP-2")

**Load linked spec:**
```bash
cat .plans/specs/[spec-file].md
```

**Extract from spec:**
- Requirements that the element satisfies (from design's "Satisfies" field)
- Related use cases
- Related acceptance criteria

**Store as:** `LINKED_SPEC`, `LINKED_REQUIREMENTS`, `LINKED_USE_CASES`, `LINKED_ACCEPTANCE_CRITERIA`

### Option 4: Todoist Task

**Check Todoist MCP:**
```
mcp__todoist__user-info
```

**If not available:** Show error and suggest options 1-3 or 5.

**If available:**

**Prompt:**
"Enter Todoist task ID, or search term to find task:"

**If search term provided:**
```
mcp__todoist__find-tasks with searchText: "[search term]"
```

**Show matching tasks:**
```
Matching Tasks:
  1. [Task content] (ID: [id])
  2. [Task content] (ID: [id])
  ...

Select task (number):
```

**Parse task to extract design references:**
- Look for COMP-N, INT-N, DATA-N in task name or description
- Look for DESIGN-N reference

**If design reference found:**
- Load that design
- Extract relevant sections

**If no design reference:**
- Ask user to specify which design/element this relates to

**Store as:** `TODOIST_TASK_ID`, `TODOIST_TASK_CONTENT`

### Option 5: Custom Task

**Prompt:**
"Describe the task:"

**Store as:** `CUSTOM_TASK`

**Prompt:**
"Which design does this relate to?"

**Show available designs and let user select.**

**Prompt:**
"Which design elements are relevant? (comma-separated, e.g., COMP-1, INT-2)"

**Store as:** `RELEVANT_ELEMENTS`

---

## DIP Content Gathering

### Update PLANNING.md

```markdown
## Gathered State
### DIP Target
- Type: [COMP/INT/DATA/Todoist/Custom]
- Element: [COMP-N or task description]
- Design: DESIGN-[N]
- Spec: SPEC-[N]
```

### Task Title

**Auto-generate from element:**
- For COMP: "Implement [COMP-N]: [component name]"
- For INT: "Implement [INT-N]: [interface name]"
- For DATA: "Create [DATA-N]: [entity name]"
- For Todoist: Use task content
- For Custom: Use provided description

**Prompt:**
"DIP title (or Enter to accept '[auto-generated title]'):"

**Store as:** `DIP_TITLE`

### Objective

**Auto-generate based on element:**
- Pull purpose from design section
- Format as single clear sentence

**Prompt:**
"DIP objective (one sentence describing completion state):"
"Suggested: '[auto-generated objective]'"

**Store as:** `DIP_OBJECTIVE`

### Required Reading

**Auto-populate from design:**

**From Spec:**
- Requirements the element satisfies (REQ-F/N)
- Use cases that involve this element (UC-N)
- Acceptance criteria for these requirements (AC-N)

**From Design:**
- The element's section (COMP-N, INT-N, or DATA-N)
- Related design decisions (DEC-N)
- Dependencies (other COMP/INT referenced)

**From Charter:**
- Relevant principles
- Relevant constraints

**Show:**
```
Required Reading (auto-detected):

From SPEC-[N]:
  - REQ-F1: [title]
  - REQ-F3: [title]
  - UC-2: [title]
  - AC-1, AC-3

From DESIGN-[N]:
  - COMP-2: [name]
  - INT-1: [name] (dependency)
  - DEC-1: [title]

From Charter:
  - Principle: [relevant principle]

Add or remove items? (Enter to accept, or edit):
```

**Store as:** `REQUIRED_READING_SPEC`, `REQUIRED_READING_DESIGN`, `REQUIRED_READING_CHARTER`

### Implementation Steps

**Auto-generate based on element type:**

**For COMP (Component):**
1. Create file structure/scaffold for [component]
2. Implement core functionality: [from responsibilities]
3. Implement [responsibility 2]
4. Add error handling
5. Write unit tests
6. Verify against acceptance criteria

**For INT (Interface):**
1. Define interface contract/schema
2. Implement endpoint/handler
3. Add input validation
4. Implement error responses
5. Add authentication/authorization (if applicable)
6. Write integration tests
7. Verify against acceptance criteria

**For DATA (Data Entity):**
1. Create schema/model definition
2. Implement validation rules
3. Create migration (if applicable)
4. Add repository/access methods
5. Write tests
6. Verify against acceptance criteria

**Show:**
```
Implementation Steps (auto-generated):

1. [Step 1]
2. [Step 2]
3. [Step 3]
...

Edit steps? (Enter to accept, 'e' to edit):
```

**If edit:**
- Show numbered list
- Allow add, remove, reorder, modify

**Store as:** `IMPLEMENTATION_STEPS` (array)

### Scope Boundaries

**Auto-generate DO list from:**
- Element's responsibilities (from design)
- Requirements it satisfies

**Auto-generate DO NOT list from:**
- Spec's out of scope
- Design's out of scope
- Other components (don't modify COMP-X when working on COMP-Y)

**Prompt:**
```
Scope Boundaries (auto-generated):

DO:
  - [action 1]
  - [action 2]

DO NOT:
  - [exclusion 1]
  - [exclusion 2]
  - Do not modify unrelated components
  - Do not add features not in spec

Edit? (Enter to accept, 'e' to edit):
```

**Store as:** `SCOPE_DO`, `SCOPE_DO_NOT`

### Files in Scope

**Prompt:**
"Which files/directories are in scope for this task?"
"Enter paths one per line (blank when done):"

**Suggest based on project structure if detectable.**

**Store as:** `FILES_IN_SCOPE` (array)

**Prompt:**
"Any files explicitly OUT of scope? (blank to skip):"

**Store as:** `FILES_OUT_OF_SCOPE` (array)

### Acceptance Criteria

**Auto-populate from spec:**
- Pull AC-N items that relate to the requirements this element satisfies

**Prompt:**
```
Acceptance Criteria (from spec):

  AC-1: Given [x], when [y], then [z]
  AC-3: Given [x], when [y], then [z]

Add task-specific criteria? (Enter to accept, 'a' to add):
```

**If add:**
- Prompt for additional criteria in Given/When/Then format

**Store as:** `ACCEPTANCE_CRITERIA` (array)

### Verification Commands

**Prompt:**
"Commands to verify implementation (e.g., test commands):"
"Enter one per line. Blank when done."

**Suggest common patterns:**
```
Suggestions:
  npm test
  pytest
  go test ./...
  cargo test
```

**Store as:** `VERIFICATION_COMMANDS` (array)

---

## Review and Confirmation

**Show DIP summary:**

```
📝 DIP Summary
==============

ID: DIP-[DIP_NUMBER]
Title: [DIP_TITLE]
For: [SELECTED_ELEMENT] in DESIGN-[N]

Objective:
[DIP_OBJECTIVE]

Required Reading: [count] sections
Implementation Steps: [count] steps
Acceptance Criteria: [count] criteria
Files in Scope: [count] paths

Linked:
  Spec: SPEC-[N]
  Design: DESIGN-[N]
  Todoist: [task ID if applicable]

File: .plans/prompts/[DIP_NUMBER]-[slug].md
```

**Prompt:**
"Generate DIP? (y)es, (e)dit section, (c)ancel:"

- `y` - Generate DIP
- `e` - Ask which section, re-prompt
- `c` - Exit without saving

---

## Generate DIP File

### Step 1: Read Template

```bash
cat .praxisity/templates/dip.template.md
```

### Step 2: Fill Template

**Context table:**
- DIP ID → `DIP-[DIP_NUMBER]`
- Task → `DIP_TITLE`
- Spec → Link to spec file
- Design → Link to design file
- Todoist Task → Task ID or "N/A"
- Created → Current date

**Objective:**
- Fill with `DIP_OBJECTIVE`

**Required Reading:**
- Generate checklists from `REQUIRED_READING_*` arrays
- Format with section references and titles

**Implementation Instructions:**
- Generate TodoWrite example with actual step names
- Generate Step N sections from `IMPLEMENTATION_STEPS`
- Include Input/Output/Verify for each step
- Add TodoWrite reminders

**Technical Requirements:**
- Generate from requirements and design sections
- Fill "Must Implement" from element responsibilities
- Fill "Must Satisfy" table from linked requirements
- Fill interface/data tables from design

**Scope Boundaries:**
- Fill DO from `SCOPE_DO`
- Fill DO NOT from `SCOPE_DO_NOT`
- Fill files in/out of scope

**Acceptance Criteria:**
- Generate table from `ACCEPTANCE_CRITERIA`
- Add verification commands

**Commit Instructions:**
- Auto-generate commit type based on element type
- Auto-generate scope from element name
- Include DIP reference and requirement IDs

**Notes:**
- Add any gathered context or warnings

### Step 3: Write File

**Generate slug:**
- From DIP title, lowercase, hyphens, no special chars

**Write to:** `.plans/prompts/[DIP_NUMBER]-[slug].md`

**Show:** "✓ DIP saved to .plans/prompts/[DIP_NUMBER]-[slug].md"

---

## Post-Save Actions

### Update PLANNING.md

```markdown
## DIP Generated

- **DIP:** DIP-[NUMBER]: [TITLE]
- **For:** [ELEMENT] in DESIGN-[N]
- **File:** .plans/prompts/[filename]
- **Created:** [timestamp]

## Next Steps
- [ ] Execute DIP: Read and follow .plans/prompts/[filename]
- [ ] Or use /build to execute with git safety
```

### Update Todoist Task (Optional)

**If task came from Todoist:**

**Prompt:**
"Update Todoist task with DIP reference? (yes/no)"

If yes:
```
mcp__todoist__update-tasks with tasks:
[{
  "id": "[TODOIST_TASK_ID]",
  "description": "[existing description]\n\nDIP: .plans/prompts/[filename]"
}]
```

**Show:** "✓ Updated Todoist task with DIP link"

### Git Commit (Optional)

**Prompt:**
"Commit DIP to git? (yes/no)"

If yes:
```bash
git add .plans/prompts/[DIP_NUMBER]-[slug].md PLANNING.md
git commit -m "dip([element]): add DIP-[NUMBER] for [ELEMENT]

Detailed implementation prompt for [DIP_TITLE]
Links: SPEC-[N], DESIGN-[N]"
```

**Show:** "✓ Committed DIP to git"

---

## Success Message

```
✅ DIP Generated

DIP-[NUMBER]: [TITLE]
File: .plans/prompts/[DIP_NUMBER]-[slug].md

This DIP provides:
  - [count] required reading sections
  - [count] implementation steps
  - [count] acceptance criteria
  - Explicit scope boundaries
  - TodoWrite integration
  - Git safety checklist

📝 Next Steps:

1. Review the DIP for completeness
   cat .plans/prompts/[filename]

2. Execute the DIP:
   - Read the DIP and follow instructions
   - Use TodoWrite to track progress
   - Or run /build for guided execution

3. The DIP integrates:
   - Claude's TodoWrite (internal progress)
   - Todoist MCP (external tracking)
   - PLANNING.md (session state)

4. On completion:
   - All acceptance criteria must pass
   - Todoist task marked complete
   - PLANNING.md updated

📚 DIPs are single-use instructions. Create new DIPs
   for subsequent tasks.
```

---

## Command Behavior Notes

**PLANNING.md Integration:**
- Reads existing context on start
- Updates with DIP target and gathered state
- Records generated DIP reference
- Suggests next actions

**Auto-Generation:**
- Attempts to auto-populate from spec/design
- User can accept or modify suggestions
- Reduces manual entry while maintaining control

**Traceability:**
- Every DIP links to spec requirements
- Every DIP links to design sections
- Todoist task updated with DIP reference
- Commit message includes all links

**TodoWrite Integration:**
- Generated DIP includes TodoWrite instructions
- Steps formatted for todo creation
- Completion checklist includes TodoWrite cleanup

**Flexibility:**
- Works from design elements (COMP, INT, DATA)
- Works from Todoist tasks
- Works from custom task descriptions
- Adapts to available information

**Idempotency:**
- Each run creates NEW DIP with incremented number
- Safe to generate multiple DIPs
- Previous DIPs preserved
