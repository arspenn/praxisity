---
name: charter
description: Create or update a project charter — the constitution that governs all decisions, scope, and AI behavior for the project.
disable-model-invocation: true
---

# Charter

Create or update your project's charter. The charter is the project's constitution — it defines the mission, principles, scope, and constraints that guide every decision.

## Constraints

- Only gather information needed to populate the charter template
- Do not add sections or content beyond what the template defines
- Accept brief answers — the user can elaborate if they choose
- If uncertain about project type or domain, ask rather than assume
- All sections except Mission can have minimal input or be skipped

## Pre-Flight

Execute these steps sequentially in the order listed. Do not begin step N+1 until step N is complete. Do not batch or parallelize pre-flight steps.

1. Read PLANNING.md for session context. Create if missing.
2. Update PLANNING.md: set active skill to `/charter`, status to "in progress". This must complete before step 3.
3. Check if CHARTER.md exists. If so, read it and offer the user three options: (r)eview and update — walk through each section showing current content as drafts for approval or revision, (s)tart fresh — ignore existing content and gather from scratch, or (c)ancel.
4. Read CLAUDE.md to extract project name and type as defaults.
5. Verify the charter template exists at `${CLAUDE_SKILL_DIR}/templates/charter.template.md`. Read it — the HTML comments are your guide for what to gather in each section.

## Charter Flow

### Introduction

Briefly explain to the user: "The charter is your project's constitution. It defines the mission, principles, scope, and constraints that guide all decisions — including how AI assists you. I'll walk through each section one at a time."

### Gather Charter Content

For each section below, follow the gathering protocol (see /gather). Present one section at a time. Wait for the user's response before moving to the next.

**Section 1: Mission**
Prompt for one clear sentence describing what this project accomplishes. If the user's prior conversation or CLAUDE.md already states the mission, present it as a draft for approval.

**Section 2: Principles**
Prompt for core values that guide decisions. These should be specific and actionable, not generic platitudes. Collect one principle at a time until the user indicates they're done. The number of principles should match what the project needs — there is no fixed count.

**Section 3: Scope**
Two sub-sections — prompt each separately:
- **In Scope:** Features, capabilities, deliverables this project will address.
- **Out of Scope:** Things stakeholders might expect but won't be delivered. Emphasize that being explicit about exclusions prevents scope creep.

**Section 4: Stakeholders**
Four sub-categories — prompt each separately, allow skipping:
- Primary users/beneficiaries
- Contributors (who builds/maintains)
- Secondary stakeholders
- Advisory/oversight (optional)

**Section 5: Success Criteria**
Three sub-categories — prompt each separately:
- Primary success metrics (measurable outcomes)
- Milestones (time-bound achievements)
- Quality indicators

**Section 6: Constraints**
Five sub-categories — prompt each separately, allow skipping:
- Timeline
- Resources
- Technical
- Regulatory/compliance
- Other

**Section 7: Domain Context**
Detect the project type from CLAUDE.md or ask the user. Then prompt for the domain-specific fields:
- **Software:** tech stack, architecture approach, quality standards
- **Public Health:** theoretical framework, evidence base, target population, intervention model, evaluation approach — prompt each field individually
- **Research:** research questions, methodology, theoretical framework, data sources, analysis plan, contribution
- **Other:** domain name and key context

**Section 8: Charter Maintenance**
Two items — prompt each separately:
- Review schedule (suggest quarterly as default)
- Amendment process (optional — how changes are made, who approves)

**Section 9: Glossary**
Review all content gathered so far. Identify any terms that would be unclear to someone reading the charter without project context. The charter must be self-contained per the dual-use design principle — it is both human governance and AI prompt context. Present a draft glossary table for approval. If no specialized terms were used, this section can be skipped.

### Review and Confirm

Show a structured summary of all gathered content with section headers. Offer three options: (y)es save, (e)dit a section, or (c)ancel.

## Generate CHARTER.md

Copy the template to the destination, then use Edit for all modifications. Never use Write for template-derived files.

1. Copy template: `cp ${CLAUDE_SKILL_DIR}/templates/charter.template.md CHARTER.md`
2. Read the fresh copy of CHARTER.md.
3. Use Edit to apply these permitted operations only:
   - **Placeholder substitution:** Replace `[bracketed placeholders]` with gathered content.
   - **Domain section removal:** Remove the domain sections that don't match the project type (e.g., remove "For Software Projects" if the project is public health).
   - **HTML comment stripping:** Remove all `<!-- ... -->` guidance comments.
   - **N/A marking:** For any section the user skipped, replace the placeholder content with "N/A — [reason]". Do not remove the section.
   - **Content population:** Fill gathered user input into the appropriate sections.
   - **Table row adjustment:** If gathered content has more or fewer items than template examples, add or remove rows. Template example counts are illustrative, not prescriptive.
4. Set dates:
   - **New charter:** "Charter established" = today, "Last reviewed" = today, "Next review" = derived from review schedule or left as placeholder.
   - **Update:** Preserve the original "Charter established" date. Set "Last reviewed" = today. Update "Next review" if the review schedule changed.
5. Verify: the original template at `${CLAUDE_SKILL_DIR}/templates/charter.template.md` must be byte-for-byte unchanged.

## Post-Save

1. Update CLAUDE.md with the mission statement if not already present.
2. Optionally create a task in the project's task management service for charter review (if available).
3. Optionally commit to git: `charter: create project charter` or `charter: update project charter`.

## Completion Gate

Update PLANNING.md with completion status, the charter as an active artifact, and suggested next steps. This is a hard gate — do not display the success message until PLANNING.md has been updated in this run.

## Success Message

Show all of the following:
- Confirmation that CHARTER.md was saved
- What the charter guides: decisions, AI behavior, scope boundaries
- Next steps:
  1. Share with stakeholders for alignment
  2. Reference when making project decisions
  3. Create your first specification with /describe
  4. Update the charter as understanding evolves

## Agent Consultation

For a quick perspective on charter quality, dispatch a Praxisity agent:
`Agent(subagent_type: "stakeholder", prompt: "Does this charter serve its intended audience?")`

For multi-perspective review, use the consult-team skill.