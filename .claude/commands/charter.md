---
description: Create or update project charter (constitution)
tags: [planning, governance, charter]
---

# Charter Command

Create or update your project's charter - the constitution that guides all decisions.

## Constraints

- Only ask questions needed to populate the charter template
- Don't add sections or content beyond what the template defines
- Keep interactions focused - gather one section at a time
- Accept brief answers; the user can elaborate if they choose
- If uncertain about project type or domain, ask rather than assume

## Pre-Flight

1. Read PLANNING.md for session context (create if missing)
2. Update PLANNING.md: set Active Command to /charter
3. Check if CHARTER.md exists - if so, offer to (r)eview, (u)pdate, or (c)ancel
4. Read CLAUDE.md to extract project name/type as defaults
5. Verify charter template exists at `.praxisity/templates/charter.template.md`

## Charter Flow

### Introduction

Show a brief intro explaining the charter's role as project governance, then proceed to gather information section by section.

### Gather Charter Content

For each section, provide a brief explanation, show domain-relevant examples, prompt for input, and store the response. Accept what the user provides without excessive validation.

**Section 1: Mission**
- One clear sentence describing what this project accomplishes
- Examples vary by domain (software: "Build a real-time collaborative editor"; public-health: "Reduce hospital readmissions through care coordination")

**Section 2: Principles**
- 3-5 core values that guide decisions
- Should be specific and actionable, not generic platitudes
- Collect one per line until blank line

**Section 3: Scope**
- In Scope: features, capabilities, deliverables
- Out of Scope: things stakeholders might expect but won't be delivered
- Collect each as list items

**Section 4: Stakeholders**
- Primary users/beneficiaries
- Contributors (who builds/maintains)
- Secondary stakeholders and advisory (optional)

**Section 5: Success Criteria**
- Primary success metrics (measurable outcomes)
- Milestones (time-bound achievements)
- Quality indicators

**Section 6: Constraints**
- Timeline, resources, technical, regulatory
- Prompt by category, allow skipping

**Section 7: Domain Context**
- Detect project type from CLAUDE.md or ask
- For SOFTWARE: tech stack, architecture approach, quality standards
- For PUBLIC-HEALTH: theoretical framework, target population, intervention model
- For RESEARCH: research questions, methodology, data sources
- For OTHER: domain name and key context

**Section 8: Charter Maintenance**
- Review schedule (default: Quarterly)
- Amendment process (optional)

### Review and Confirm

Show a summary of all gathered content. Offer to (y)es save, (e)dit a section, or (c)ancel.

## Generate CHARTER.md

1. Read the charter template
2. Fill placeholders with gathered values
3. Remove HTML comments and unused domain sections
4. Add dates (established, last reviewed, next review)
5. Write to CHARTER.md

## Post-Save

1. Update CLAUDE.md with the mission statement
2. Optionally create a Todoist reminder for charter review (if MCP available)
3. Optionally commit to git with conventional format
4. Update PLANNING.md with completion status and next steps

## Success Message

Confirm the charter was saved, explain what it guides (decisions, AI behavior, scope), and suggest next steps:
1. Share with stakeholders
2. Reference when making decisions
3. Create first specification with /spec
4. Update charter as understanding evolves

---

## Behavior Notes

- Idempotent: safe to run multiple times; updates existing charter
- Flexible: all sections except Mission can have minimal input
- Minimal validation: warn on brief answers but accept user choice
- PLANNING.md integration: reads on start, updates during execution, records completion
