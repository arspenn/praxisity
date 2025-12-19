---
description: Initialize a new project from the Praxisity framework
tags: [setup, initialization, praxisity]
---

# New Project Initialization

This command transforms the Praxisity framework repository into a clean project ready for your work.

**⚠️ WARNING: This operation removes Praxisity development artifacts and is NOT easily reversible.**

## What This Command Does

**Removes:**
- All contents of `.plans/` (Praxisity's own planning docs)
- All contents of `deliverables/` (Praxisity's outputs)
- `praxisity-foundation-plan.md`
- Current `CLAUDE.md`, `CHARTER.md`, `README.md`, `CHANGELOG.md`
- Git history (resets to fresh repository)

**Preserves:**
- `.claude/commands/` (all framework commands)
- `.praxisity/templates/` (document templates)
- `.praxisity/safety/` (git safety logic)
- Empty `src/`, `docs/` directories

**Creates:**
- Fresh `CLAUDE.md` (from template, populated with your project info)
- Fresh `CHARTER.md` (from template, ready to fill)
- Fresh `README.md` (from template, populated with your project info)
- Fresh `CHANGELOG.md` (reset to v0.1.0)

## Pre-Flight Checks

Before proceeding, verify:

1. **Check that .praxisity/ directory exists**
   ```bash
   ls -la .praxisity/
   ```

   If this directory doesn't exist, you're not in a Praxisity framework repository.
   Exit the command.

2. **Check git status**
   ```bash
   git status
   ```

   If there are uncommitted changes, warn the user:
   ```
   ⚠️  You have uncommitted changes.
   Recommendation: Commit or stash your changes before running /new-project.
   ```

   Ask: "Continue anyway? (yes/no)"
   If no, exit the command.

3. **Verify we're not already initialized**

   If `praxisity-foundation-plan.md` does not exist, this may have already been run.

   Ask: "It appears /new-project may have already been run. Continue anyway? (yes/no)"
   If no, exit the command.

## Parameter Gathering

Ask the user for the following information:

### 1. Project Name
**Prompt:** "What is your project name?"
**Validation:**
- Required (cannot be empty)
- Should be alphanumeric with hyphens/underscores allowed
**Store as:** `PROJECT_NAME`

### 2. Project Type
**Prompt:** "What type of project is this?"
**Options:**
1. software - Software development project
2. public-health - Public health program or intervention
3. research - Academic or scientific research
4. other - Other domain

**Store as:** `PROJECT_TYPE`

### 3. Todoist Project Name
**Prompt:** "What should your Todoist project be named? (default: [PROJECT_NAME])"
**Default:** Same as PROJECT_NAME
**Store as:** `TODOIST_PROJECT_NAME`

### 4. Version
**Prompt:** "Starting version? (default: 0.1.0)"
**Default:** 0.1.0
**Store as:** `VERSION`

### 5. Confirmation
**Show summary:**
```
📋 New Project Summary
----------------------
Name: [PROJECT_NAME]
Type: [PROJECT_TYPE]
Todoist: [TODOIST_PROJECT_NAME]
Version: [VERSION]

This will DELETE Praxisity development artifacts.
This operation is NOT easily reversible.
```

**Prompt:** "Proceed with initialization? Type 'yes' to continue:"
**Validation:** Must type exactly "yes" (case-insensitive)
If not "yes", exit with message: "Initialization cancelled."

## Execution Steps

### Step 1: Remove Development Artifacts

```bash
# Remove contents of .plans/ but keep directories
rm -f .plans/specs/*
rm -f .plans/designs/*
rm -f .plans/prompts/*
rm -f .plans/decisions/*

# Remove contents of deliverables/ but keep directory
rm -f deliverables/*

# Remove foundation plan
rm -f praxisity-foundation-plan.md

# Remove current project files (we'll replace these)
rm -f CLAUDE.md CHARTER.md README.md CHANGELOG.md
```

Show: "✓ Removed Praxisity development artifacts"

### Step 2: Generate CLAUDE.md from Template

Read `.praxisity/templates/claude.template.md`

Replace placeholders:
- `[PROJECT_NAME]` → PROJECT_NAME
- `[software | public-health | research | other]` → PROJECT_TYPE
- `[SEMVER]` → VERSION
- `[planning | active-development | maintenance | archived]` → "planning"
- `[One sentence - what does this project accomplish?]` → "[To be defined in charter]"
- `[X.Y.Z]` (Praxisity version) → "1.0.0" (or current framework version)
- `[TODOIST_PROJECT_NAME]` → TODOIST_PROJECT_NAME
- `[specification | design | implementation | delivery | maintenance]` → "specification"
- `[Current sprint/milestone focus]` → "Run /charter to establish project governance"
- `[What was just completed? What's the current state?]` → "Project initialized from Praxisity framework"
- `[DATE]` → Current date (YYYY-MM-DD format)

Remove the domain sections that don't match PROJECT_TYPE:
- If PROJECT_TYPE is "software", remove public health and research sections
- If PROJECT_TYPE is "public-health", remove software and research sections
- If PROJECT_TYPE is "research", remove software and public health sections
- If PROJECT_TYPE is "other", keep all sections as examples

Write to `CLAUDE.md`

Show: "✓ Created CLAUDE.md from template"

### Step 3: Generate CHARTER.md from Template

Read `.praxisity/templates/charter.template.md`

No placeholder replacement needed (user will fill this via /charter command)

Write to `CHARTER.md`

Show: "✓ Created CHARTER.md from template"

### Step 4: Generate README.md from Template

Read `.praxisity/templates/readme.template.md`

Replace placeholders:
- `[PROJECT_NAME]` → PROJECT_NAME
- `[One-line project description]` → "A [PROJECT_TYPE] project managed with Praxisity"
- `[SEMVER]` → VERSION
- `[Planning | Active Development | Beta | Production | Maintenance]` → "Planning"
- `[DATE]` → Current date (YYYY-MM-DD format)
- `[TODOIST_PROJECT_NAME]` → TODOIST_PROJECT_NAME

Write to `README.md`

Show: "✓ Created README.md from template"

### Step 5: Generate CHANGELOG.md

Create new CHANGELOG.md:
```markdown
# Changelog

All notable changes to [PROJECT_NAME] will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

---

## [[VERSION]] - [CURRENT_DATE]

### Added
- Project initialized from Praxisity framework
- Core directory structure
- Framework commands and templates
```

Replace `[PROJECT_NAME]`, `[VERSION]`, `[CURRENT_DATE]`

Write to `CHANGELOG.md`

Show: "✓ Created CHANGELOG.md"

### Step 6: Create Todoist Project (Optional)

**Check if Todoist MCP is available:**

Try to list Todoist projects. If MCP is not available or fails, skip this step with message:
"⚠️  Todoist MCP not available. You can create the Todoist project manually later."

**If Todoist MCP is available:**

Ask: "Create Todoist project '[TODOIST_PROJECT_NAME]'? (yes/no)"

If yes:
1. Create Todoist project with name TODOIST_PROJECT_NAME
2. Create sections:
   - "Planning"
   - "Specifications"
   - "Design"
   - "Implementation"
   - "Delivery"
3. Add first task to "Planning" section: "Complete project charter (/charter command)"

Show: "✓ Created Todoist project '[TODOIST_PROJECT_NAME]'"

### Step 7: Reset Git History

**Remove existing git repository:**
```bash
rm -rf .git
```

Show: "✓ Removed old git history"

**Initialize fresh git repository:**
```bash
git init
git add .
git commit -m "chore: initialize project from Praxisity framework v1.0.0

Project: [PROJECT_NAME]
Type: [PROJECT_TYPE]
Version: [VERSION]

Generated with Praxisity - A design-first workflow framework
https://github.com/[USERNAME]/praxisity"
```

Replace `[PROJECT_NAME]`, `[PROJECT_TYPE]`, `[VERSION]` in commit message.

Show: "✓ Initialized fresh git repository"

**Ask about remote:**
"Do you want to set a git remote? (Enter URL or press Enter to skip):"

If user provides URL:
```bash
git remote add origin [URL]
```
Show: "✓ Set git remote to [URL]"

If user skips:
Show: "ℹ️  You can set remote later with: git remote add origin <url>"

## Success Message

```
🎉 Project Initialization Complete!

Your new project '[PROJECT_NAME]' is ready.

📁 What was preserved:
   - Framework commands in .claude/commands/
   - Templates in .praxisity/templates/
   - Safety logic in .praxisity/safety/

📝 What was created:
   - Fresh git repository with initial commit
   - CLAUDE.md (AI guidance)
   - CHARTER.md (project constitution template)
   - README.md (project overview)
   - CHANGELOG.md (version history)
   [- Todoist project '[TODOIST_PROJECT_NAME]' (if created)]
   [- Git remote '[REMOTE_URL]' (if configured)]

🚀 Next Steps:

1. Review and fill in CHARTER.md
   Run: /charter

2. Update README.md with project details
   Edit: README.md

3. Create your first specification
   Run: /spec

4. [If you didn't set a remote] Push to your repository:
   git remote add origin <your-repo-url>
   git push -u origin main

📚 Documentation:
   - See CLAUDE.md for AI configuration and architecture notes
   - See CHARTER.md for project governance
   - See .plans/ for specifications, designs, and decisions

Happy building! 🛠️
```

## Error Handling

If any step fails:
1. Show clear error message with what failed
2. Show what was completed successfully
3. Show how to recover or continue manually
4. Do NOT attempt to auto-rollback (changes may be partially complete)

## Idempotency

This command is NOT idempotent. Running it multiple times will:
- Delete and recreate the same files
- Potentially lose user work

The pre-flight checks help prevent accidental re-runs.
