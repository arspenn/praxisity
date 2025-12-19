---
description: Create a new specification document
tags: [planning, specification, design-first]
---

# Spec Command

Create a new specification document that defines WHAT you're building.

## Purpose

Specifications are the entry point to the design-first workflow. They define:
- The problem being solved
- Goals and measurable objectives
- Functional and non-functional requirements
- Use cases showing how the solution will be used
- Acceptance criteria for validation
- Scope boundaries (what's in and out)

A well-crafted specification:
- Aligns stakeholders on what success looks like
- Provides clear requirements for design phase
- Enables precise DIPs through section IDs (REQ-1, UC-1, etc.)
- Prevents scope creep through explicit exclusions

**This command creates WHAT. The `/architect` command creates HOW.**

## Pre-Flight Checks

### Read PLANNING.md

```bash
cat PLANNING.md 2>/dev/null
```

**If PLANNING.md exists:**
- Parse current session context
- Check for active charter reference
- Note any prior spec work

**If PLANNING.md doesn't exist:**
- Create fresh PLANNING.md

**Update PLANNING.md:**
```markdown
## Session Context
- **Active Command:** /spec
- **Started:** [timestamp]
- **Task:** Create new specification
```

### Check for Charter

```bash
ls -la CHARTER.md
```

**If CHARTER.md does NOT exist:**
- Show warning: "No CHARTER.md found. Specifications should align with your project charter."
- Ask: "Continue without charter? (y/n)"
  - `n` - Exit and suggest running `/charter` first
  - `y` - Continue with warning noted

**If CHARTER.md exists:**
- Read it to extract:
  - Mission statement (for alignment check)
  - Principles (for constraint context)
  - In-scope items (for validation)
  - Out-of-scope items (to inherit)
- Store for reference during questionnaire

### Check for Spec Template

```bash
ls -la .praxisity/templates/spec.template.md
```

**If template doesn't exist:**
- Show error: "Spec template not found at .praxisity/templates/spec.template.md"
- Exit command

### Determine Next Spec Number

```bash
ls .plans/specs/*.md 2>/dev/null | sort -V | tail -1
```

**Logic:**
- If no specs exist: Next number is `001`
- If specs exist: Extract highest number, increment by 1, zero-pad to 3 digits
- Example: If `003-auth-system.md` exists, next is `004`

**Store as:** `SPEC_NUMBER` (e.g., "001", "004")

### Create Specs Directory if Needed

```bash
mkdir -p .plans/specs
```

---

## Specification Creation Flow

### Introduction

Show:
```
📋 New Specification

Specifications define WHAT you're building.
They establish requirements, use cases, and acceptance criteria.

This will be saved as: .plans/specs/[SPEC_NUMBER]-[name].md

The spec template uses section IDs (REQ-1, UC-1, AC-1) for traceability.
These IDs will be referenced by designs and DIPs later.

Let's define your specification.
```

If charter was loaded, also show:
```
📜 Charter Context Loaded:
   Mission: [first 100 chars of mission]...
   Your spec should align with this mission.
```

---

### Gather Spec Metadata

#### Spec Title

**Prompt:**
"What is this specification about? (brief title, e.g., 'User Authentication', 'Patient Intake Form'):"

**Validation:**
- Must be at least 3 characters
- Should be concise (warn if >50 characters but allow)

**Store as:** `SPEC_TITLE`

**Generate slug:**
- Convert to lowercase
- Replace spaces with hyphens
- Remove special characters
- Example: "User Authentication" → "user-authentication"

**Store as:** `SPEC_SLUG`

#### Spec Author

**Prompt:**
"Author name (or press Enter for git user.name):"

**Default:** Result of `git config user.name` or "Unknown"

**Store as:** `SPEC_AUTHOR`

---

### Section 1: Problem Statement

**Explanation:**
```
PROBLEM STATEMENT

What problem does this solve? Why does it matter?
Write this so someone unfamiliar with the project understands the need.

Good problem statements:
- Describe the current state and its limitations
- Explain who is affected and how
- Quantify the impact if possible
- Connect to charter mission
```

**Show domain-specific examples based on project type (from CLAUDE.md or ask):**

For SOFTWARE:
```
Example: "Users currently wait 30+ seconds for search results because
the system performs full-table scans. This causes 40% abandonment."
```

For PUBLIC-HEALTH:
```
Example: "Heart failure patients at Hospital X have 25% readmission rate,
above national average. Each readmission costs ~$15,000."
```

For RESEARCH:
```
Example: "Existing literature relies on cross-sectional surveys, limiting
causal inference. Longitudinal data with objective measures is needed."
```

**Prompt:**
"Describe the problem this specification addresses:"

**Validation:**
- Must be at least 20 characters
- Warn if <50 characters (encourage detail)

**Store as:** `PROBLEM_STATEMENT`

---

### Section 2: Goals and Objectives

**Explanation:**
```
GOALS AND OBJECTIVES

What does success look like? Be specific and measurable.
- Goal: High-level outcome (one sentence)
- Objectives: Specific, measurable targets (OBJ-1, OBJ-2, etc.)

Format objectives as: "[Who] will be able to [do what], resulting in [metric]."
```

**Prompt for Primary Goal:**
"What is the primary goal? (one sentence describing the outcome):"

**Store as:** `PRIMARY_GOAL`

**Prompt for Objectives:**
"Enter objectives one at a time. For each, provide:"
"  - Description (what will be achieved)"
"  - Success metric (how you'll measure it)"
"Enter blank line when done."

**Collect as array of objects:**
```
[
  { description: "...", metric: "..." },
  { description: "...", metric: "..." }
]
```

**Validation:**
- Must have at least 1 objective
- Each objective should have both description and metric

**Store as:** `OBJECTIVES` (array)

---

### Section 3: Requirements

**Explanation:**
```
REQUIREMENTS

What must the solution DO (functional) and BE (non-functional)?

Use MoSCoW prioritization:
- MUST: Non-negotiable for this spec
- SHOULD: Important but can defer if necessary
- COULD: Nice to have if time permits

Each requirement gets an ID (REQ-F1, REQ-N1) for traceability.
```

#### Functional Requirements

**Prompt:**
"Enter FUNCTIONAL requirements (what the solution must DO)."
"For each, provide:"
"  - Requirement (The system shall...)"
"  - Priority (MUST/SHOULD/COULD)"
"  - Rationale (why this matters)"
"Enter blank line when done."

**Collect as array:**
```
[
  { requirement: "...", priority: "MUST", rationale: "..." },
  ...
]
```

**Validation:**
- Must have at least 1 functional requirement
- Priority must be MUST, SHOULD, or COULD

**Store as:** `REQUIREMENTS_FUNCTIONAL` (array)

#### Non-Functional Requirements

**Prompt:**
"Enter NON-FUNCTIONAL requirements (qualities: performance, security, usability)."
"Same format: Requirement, Priority, Rationale."
"Enter blank line when done (or press Enter to skip)."

**Store as:** `REQUIREMENTS_NONFUNCTIONAL` (array, can be empty)

---

### Section 4: Use Cases

**Explanation:**
```
USE CASES

How will users/stakeholders interact with the solution?
Each use case gets an ID (UC-1, UC-2) for traceability.

Describe:
- Actor: Who performs this
- Preconditions: What must be true before
- Flow: Steps that occur
- Postconditions: What's true after
```

**Prompt:**
"Enter use cases. For each, provide:"
"  - Title (brief name)"
"  - Actor (who performs this)"
"  - Preconditions (comma-separated, or 'none')"
"  - Flow (numbered steps, separate with semicolons)"
"  - Postconditions (comma-separated)"
"Enter blank line when done."

**Example to show:**
```
Example:
  Title: User logs in
  Actor: Registered user
  Preconditions: User has account, User is on login page
  Flow: 1. Enter email; 2. Enter password; 3. Click submit; 4. System validates
  Postconditions: User session created, User redirected to dashboard
```

**Collect as array:**
```
[
  {
    title: "...",
    actor: "...",
    preconditions: ["...", "..."],
    flow: ["...", "...", "..."],
    postconditions: ["...", "..."]
  },
  ...
]
```

**Validation:**
- Must have at least 1 use case
- Each use case must have title, actor, and flow

**Store as:** `USE_CASES` (array)

---

### Section 5: Acceptance Criteria

**Explanation:**
```
ACCEPTANCE CRITERIA

How do we know this spec is successfully implemented?
Format: "Given [context], when [action], then [result]."

Each criterion should trace to a requirement (REQ-F1, etc.).
```

**Prompt:**
"Enter acceptance criteria. For each:"
"  - Criterion (Given... when... then...)"
"  - Validates (which requirement ID, e.g., REQ-F1)"
"Enter blank line when done."

**Collect as array:**
```
[
  { criterion: "Given..., when..., then...", validates: "REQ-F1" },
  ...
]
```

**Validation:**
- Must have at least 1 acceptance criterion
- Should have criteria covering all MUST requirements

**Store as:** `ACCEPTANCE_CRITERIA` (array)

---

### Section 6: Constraints

**Explanation:**
```
CONSTRAINTS

What limits the solution?
Some constraints come from your charter; add any spec-specific ones.
```

**If charter was loaded, show:**
```
Charter constraints (will be inherited):
- [constraint 1 from charter]
- [constraint 2 from charter]
```

**Prompt:**
"Enter any ADDITIONAL constraints specific to this spec."
"Categories: Technical, Timeline, Resources, Regulatory, Other"
"Enter one per line. Blank line when done (or Enter to skip)."

**Store as:** `CONSTRAINTS_SPECIFIC` (array, can be empty)

---

### Section 7: Dependencies

**Explanation:**
```
DEPENDENCIES

What must exist for this spec to be implementable?
What does this spec enable?
```

**Prompt for Depends On:**
"What does this spec DEPEND ON? (other specs, systems, resources)"
"Enter one per line with status (Available/Pending/Blocked)."
"Format: [Name] | [Type: Spec/External/Resource] | [Status]"
"Blank line when done (or Enter if none)."

**Example:**
```
Example: Authentication API | External | Available
```

**Store as:** `DEPENDENCIES_ON` (array, can be empty)

**Prompt for Enables:**
"What does this spec ENABLE? (future specs, features)"
"Enter one per line. Blank line when done (or Enter if none)."

**Store as:** `DEPENDENCIES_ENABLES` (array, can be empty)

---

### Section 8: Out of Scope

**Explanation:**
```
OUT OF SCOPE

CRITICAL: What is explicitly NOT part of this spec?
This prevents scope creep and sets clear boundaries.

Include things users might expect but you won't deliver.
```

**If charter was loaded and has out-of-scope items:**
```
Charter excludes (inherited):
- [item from charter]
```

**Prompt:**
"What is OUT OF SCOPE for this specification?"
"Include things stakeholders might expect but you won't deliver."
"Enter one per line. Blank line when done."

**Validation:**
- Must have at least 1 out-of-scope item (enforce thinking about boundaries)

**Store as:** `OUT_OF_SCOPE` (array)

---

### Section 9: Open Questions

**Explanation:**
```
OPEN QUESTIONS

What needs to be resolved before or during implementation?
Track uncertainties here. Resolve before moving to design if possible.
```

**Prompt:**
"Any open questions to track? (or Enter to skip)"
"Enter one per line. Blank line when done."

**Store as:** `OPEN_QUESTIONS` (array, can be empty)

---

### Section 10: References

**Prompt:**
"Any external references? (docs, research, links)"
"Enter one per line. Blank line when done (or Enter to skip)."

**Auto-add:** Link to CHARTER.md if it exists

**Store as:** `REFERENCES` (array)

---

## Review and Confirmation

**Show complete spec summary:**

```
📋 Specification Summary
========================

ID: SPEC-[SPEC_NUMBER]
Title: [SPEC_TITLE]
Author: [SPEC_AUTHOR]

PROBLEM:
[PROBLEM_STATEMENT - truncated to 200 chars]...

PRIMARY GOAL:
[PRIMARY_GOAL]

OBJECTIVES: [count] defined
FUNCTIONAL REQUIREMENTS: [count] ([MUST count] MUST, [SHOULD count] SHOULD)
NON-FUNCTIONAL REQUIREMENTS: [count] defined
USE CASES: [count] defined
ACCEPTANCE CRITERIA: [count] defined
OUT OF SCOPE: [count] items

File: .plans/specs/[SPEC_NUMBER]-[SPEC_SLUG].md
```

**Prompt:**
"Does this look correct? (y)es to save, (e)dit to modify a section, (c)ancel:"

- `y` - Proceed to save
- `e` - Ask which section to edit (1-10), re-prompt for that section
- `c` - Exit without saving

---

## Generating Specification File

### Step 1: Read Template

Read `.praxisity/templates/spec.template.md`

### Step 2: Fill Template

Replace placeholders and populate sections:

**Metadata table:**
- `SPEC-NNN` → `SPEC-[SPEC_NUMBER]`
- `[Descriptive title]` → `[SPEC_TITLE]`
- `Status` → `Draft`
- `[Name]` → `[SPEC_AUTHOR]`
- `Created` and `Last Updated` → Current date (YYYY-MM-DD)
- `Charter Reference` → `[CHARTER.md](../../CHARTER.md)` if exists

**Section 1 (Problem Statement):**
- Replace placeholder with `PROBLEM_STATEMENT`

**Section 2 (Goals and Objectives):**
- `2.1 Primary Goal` → `PRIMARY_GOAL`
- `2.2 Objectives` → Table with OBJ-1, OBJ-2, etc. from `OBJECTIVES`

**Section 3 (Requirements):**
- `3.1 Functional` → Table with REQ-F1, REQ-F2, etc. from `REQUIREMENTS_FUNCTIONAL`
- `3.2 Non-Functional` → Table with REQ-N1, REQ-N2, etc. from `REQUIREMENTS_NONFUNCTIONAL`

**Section 4 (Use Cases):**
- Generate UC-1, UC-2, etc. from `USE_CASES`
- Format each with Actor, Preconditions, Flow, Postconditions

**Section 5 (Acceptance Criteria):**
- Table with AC-1, AC-2, etc. from `ACCEPTANCE_CRITERIA`

**Section 6 (Constraints):**
- `6.1 Inherited from Charter` → Constraints from charter if loaded
- `6.2 Spec-Specific` → `CONSTRAINTS_SPECIFIC`

**Section 7 (Dependencies):**
- `7.1 Depends On` → Table from `DEPENDENCIES_ON`
- `7.2 Enables` → Table from `DEPENDENCIES_ENABLES`

**Section 8 (Out of Scope):**
- Bullet list from `OUT_OF_SCOPE`

**Section 9 (Open Questions):**
- Table with Q-1, Q-2, etc. from `OPEN_QUESTIONS` (all status "Open")

**Section 10 (References):**
- List from `REFERENCES`

**Revision History:**
- Add initial entry: `0.1 | [DATE] | [AUTHOR] | Initial draft`

**Remove:**
- All HTML comments (<!-- ... -->)
- Placeholder brackets that weren't filled
- Empty sections (keep headers, remove placeholder content)

### Step 3: Write File

Write to: `.plans/specs/[SPEC_NUMBER]-[SPEC_SLUG].md`

Show: "✓ Specification saved to .plans/specs/[SPEC_NUMBER]-[SPEC_SLUG].md"

---

## Post-Save Actions

### Create Todoist Task (Optional)

If Todoist MCP is available:

**Prompt:**
"Create Todoist task to track this spec? (yes/no)"

If yes:
- Find or create "Specifications" section in project
- Create task: "Review and approve: SPEC-[NUMBER] [TITLE]"
- Description: "Specification needs review before proceeding to design.\nFile: .plans/specs/[filename]"
- Priority: p2 (high)
- Label: "spec"

Show: "✓ Created spec review task in Todoist"

### Git Commit (Optional)

**Prompt:**
"Commit specification to git? (yes/no)"

If yes:
```bash
git add .plans/specs/[SPEC_NUMBER]-[SPEC_SLUG].md
git commit -m "spec([SPEC_SLUG]): add SPEC-[SPEC_NUMBER] [SPEC_TITLE]

Initial specification draft defining requirements and acceptance criteria."
```

Show: "✓ Committed specification to git"

---

## Success Message

```
✅ Specification Created

SPEC-[SPEC_NUMBER]: [SPEC_TITLE]
File: .plans/specs/[SPEC_NUMBER]-[SPEC_SLUG].md

This specification defines:
- [count] functional requirements (REQ-F1 through REQ-F[n])
- [count] use cases (UC-1 through UC-[n])
- [count] acceptance criteria (AC-1 through AC-[n])

📝 Next Steps:

1. Review the specification for completeness
   - Are all requirements clear and testable?
   - Do acceptance criteria cover all MUST requirements?
   - Is out-of-scope explicit enough?

2. Get stakeholder alignment (if applicable)

3. Create the design document:
   /architect

   The design will reference this spec's requirements
   (e.g., "REQ-F1 is satisfied by component X")

4. Section IDs (REQ-F1, UC-1, AC-1) will be used by:
   - /architect (design references requirements)
   - /breakdown (tasks reference requirements)
   - /define (DIPs cite specific sections)

📚 Specifications are living documents. Update as understanding evolves.
```

### Update PLANNING.md

```markdown
## Completed

- **Spec:** Created SPEC-[NUMBER]: [TITLE]
- **File:** .plans/specs/[filename]
- **Requirements:** [count] functional, [count] non-functional
- **Timestamp:** [completion time]

## Active Artifacts
- **Spec:** SPEC-[NUMBER]: [TITLE]

## Next Steps
- [ ] Review specification for completeness
- [ ] Create design document: /architect
```

---

## Command Behavior Notes

**Idempotency:**
- Each run creates a NEW spec with incremented number
- To update existing spec, edit the file directly
- Safe to run multiple times (creates new specs each time)

**Flexibility:**
- Most sections can be minimal (single item)
- Open questions and references can be empty
- Non-functional requirements can be skipped
- But out-of-scope is required (forces boundary thinking)

**Validation:**
- Minimal validation to avoid friction
- Warnings for brief answers, but allows user choice
- Required: title, problem, goal, 1+ objective, 1+ requirement, 1+ use case, 1+ acceptance criterion, 1+ out-of-scope

**Charter Integration:**
- Loads charter context if available
- Inherits constraints and out-of-scope items
- Adds charter reference automatically

**Dual-Use Design:**
- Section IDs enable AI parsing and precise referencing
- Human-readable explanations and examples throughout
- Structured tables for both human scanning and AI extraction

**PLANNING.md Integration:**
- Reads existing context on start
- Updates with command start and gathered state
- Records completion and active artifacts
- Suggests next steps
- Enables session recovery if interrupted
