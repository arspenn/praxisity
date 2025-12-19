---
description: Initialize a new project from the Praxisity framework
tags: [setup, initialization, praxisity]
---

# New Project Command

Transform the Praxisity framework repository into a clean project ready for your work.

**Warning: This operation removes Praxisity development artifacts and resets git history. Not easily reversible.**

## Constraints

- Only create files defined in templates
- Don't add extra configuration or features
- Keep parameter gathering focused on essentials
- Accept user inputs without excessive validation

## Pre-Flight

1. Verify `.praxisity/` directory exists (confirms this is a Praxisity repo)
2. Check git status - warn if uncommitted changes, ask to continue
3. Check if `praxisity-foundation-plan.md` exists - if not, this may have already been run; confirm before proceeding

## Parameter Gathering

Collect project information:

1. **Project name** (required) - alphanumeric with hyphens/underscores
2. **Project type** - software, public-health, research, or other
3. **Todoist project name** - default to project name
4. **Starting version** - default to 0.1.0

Show summary and require explicit "yes" to proceed.

## Execution

### Step 1: Remove Development Artifacts

- Clear contents of `.plans/specs/`, `.plans/designs/`, `.plans/prompts/`, `.plans/decisions/`
- Clear `deliverables/`
- Remove `praxisity-foundation-plan.md`
- Remove existing `CLAUDE.md`, `CHARTER.md`, `README.md`, `CHANGELOG.md`

### Step 2: Generate CLAUDE.md

Read `.praxisity/templates/claude.template.md`, replace placeholders with project info, remove non-applicable domain sections based on project type, write to `CLAUDE.md`.

### Step 3: Generate CHARTER.md

Copy charter template to `CHARTER.md` (user will fill via /charter).

### Step 4: Generate README.md

Read `.praxisity/templates/readme.template.md`, replace placeholders, write to `README.md`.

### Step 5: Generate CHANGELOG.md

Read `.praxisity/templates/changelog.template.md`, replace placeholders ([PROJECT_NAME], [VERSION], [DATE]), remove guidance comments, write to `CHANGELOG.md`.

### Step 6: Create Todoist Project (Optional)

If Todoist MCP is available and user confirms:
- Create project with specified name
- Add sections: Planning, Specifications, Design, Implementation, Delivery
- Add first task: "Complete project charter (/charter command)"

### Step 7: Reset Git History

- Remove `.git/`
- Initialize fresh repository
- Create initial commit with project metadata
- Optionally set remote if user provides URL

## Success Message

Confirm initialization complete. List what was preserved (commands, templates, safety logic) and what was created (fresh git, CLAUDE.md, CHARTER.md, README.md, CHANGELOG.md, optionally Todoist project).

Suggest next steps:
1. Fill in charter with /charter
2. Update README.md with project details
3. Create first specification with /spec
4. Push to repository if remote was set

---

## Behavior Notes

- Not idempotent: running multiple times will lose user work
- Pre-flight checks help prevent accidental re-runs
- Preserves framework commands and templates
- Creates clean slate for new project
