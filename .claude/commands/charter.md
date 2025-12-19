---
description: Create or update project charter (constitution)
tags: [planning, governance, charter]
---

# Charter Command

Create or update your project's charter - the constitution that guides all decisions and AI behavior.

## Purpose

The charter is your project's governance document. It defines:
- Mission (what you're building)
- Principles (values that guide decisions)
- Scope (what's in/out)
- Stakeholders (who's involved)
- Success criteria (how you measure achievement)
- Constraints (limitations)
- Domain context (field-specific knowledge)

A well-crafted charter:
- Aligns stakeholders
- Guides AI assistance throughout the project
- Prevents scope creep
- Provides decision-making framework

## Pre-Flight Checks

### Read PLANNING.md

```bash
cat PLANNING.md 2>/dev/null
```

**If PLANNING.md exists:**
- Parse current session context
- Note any prior charter work

**If PLANNING.md doesn't exist:**
- Create fresh PLANNING.md

**Update PLANNING.md:**
```markdown
## Session Context
- **Active Command:** /charter
- **Started:** [timestamp]
- **Task:** Create/update project charter
```

### Check if charter already exists

```bash
ls -la CHARTER.md
```

**If CHARTER.md exists:**
- This is an UPDATE operation
- Prompt: "CHARTER.md already exists. Would you like to (r)eview, (u)pdate, or (c)ancel?"
  - `r` - Display current charter and exit
  - `u` - Continue to update flow
  - `c` - Exit command

**If CHARTER.md does NOT exist:**
- This is a CREATE operation
- Check if charter template exists:
  ```bash
  ls -la .praxisity/templates/charter.template.md
  ```
- If template doesn't exist, show error and exit

### Read CLAUDE.md for context

Read `CLAUDE.md` to extract:
- Project name
- Project type (software/public-health/research/other)
- Current version

This provides defaults for charter questions.

## Charter Creation/Update Flow

### Introduction

Show:
```
📜 Project Charter

Your charter is the constitution of your project.
It guides all decisions and AI behavior.

This process will help you think deeply about:
- What you're building and why
- What values guide your choices
- What's in and out of scope
- How you'll measure success

Take your time. Be specific. You can always update later.
```

### Guided Questionnaire

For each section, provide:
1. **Explanation** - What this section is for
2. **Current value** - If updating, show existing content
3. **Examples** - Domain-specific good examples
4. **Prompt** - Ask for user input
5. **Validation** - Check if input is sufficient

---

#### 1. Mission

**Explanation:**
```
MISSION: One clear sentence describing what this project accomplishes.

Good missions are:
- Specific (not vague)
- Outcome-focused (not just activity)
- Concise (one sentence)
```

**Examples (domain-specific):**

For SOFTWARE:
- "Build a real-time collaborative text editor with conflict-free editing"
- "Create a personal finance tracker that automatically categorizes transactions"

For PUBLIC-HEALTH:
- "Reduce hospital readmissions for heart failure patients through AI-powered care coordination"
- "Improve vaccination rates in underserved communities through mobile clinic intervention"

For RESEARCH:
- "Investigate the relationship between social media use and adolescent mental health outcomes"
- "Develop a computational model of protein folding for drug discovery"

**Prompt:**
"What is your project's mission? (One clear sentence):"

**Validation:**
- Must be at least 10 words
- Should be one sentence (warn if multiple sentences, but allow)
- If too vague (e.g., "make things better"), prompt for specificity

**Store as:** `MISSION`

---

#### 2. Principles

**Explanation:**
```
PRINCIPLES: 3-5 core values that guide ALL decisions in this project.

Good principles are:
- Specific to your project (not generic platitudes)
- Actionable (explain what they mean in practice)
- Decision-guiding (help when facing tough choices)

Bad: "Quality is important"
Good: "Privacy-first: User data never leaves their device"
```

**Examples (domain-specific):**

For SOFTWARE:
- "API-first: All features accessible via documented API"
- "Offline-capable: Core functionality works without internet"
- "Zero-config: Works out of the box with sensible defaults"

For PUBLIC-HEALTH:
- "Evidence-based: Every intervention backed by peer-reviewed research"
- "Community-centered: Program design driven by target population input"
- "Equity-focused: Outcomes measured across demographic subgroups"

For RESEARCH:
- "Reproducible: All analyses documented with version-controlled code"
- "Open science: Preregistration of hypotheses and open data when possible"
- "Theory-driven: Grounded in established theoretical frameworks"

**Prompt:**
"Enter your principles, one per line. When done, enter a blank line."

**Process:**
- Collect lines until user enters blank line
- Must have at least 3 principles
- Each should be substantial (warn if <10 words)

**Store as:** `PRINCIPLES` (array)

---

#### 3. Scope

**Explanation:**
```
SCOPE: Clear boundaries of what you WILL and WON'T do.

The "Out of Scope" section is especially important - it prevents scope creep
by explicitly listing things stakeholders might expect but you won't deliver.
```

**Prompt for In Scope:**
"What is IN SCOPE for this project? List features, capabilities, user groups, deliverables."
"Enter items one per line. When done, enter a blank line."

**Collect items until blank line**

**Store as:** `IN_SCOPE` (array)

**Prompt for Out of Scope:**
"What is OUT OF SCOPE? Include things people might expect but you won't do."
"Enter items one per line. When done, enter a blank line."

**Examples to suggest:**
- "For MVP, you might exclude: advanced features, additional platforms, 24/7 support"
- "Consider explicitly excluding adjacent use cases or earlier-phase features"

**Collect items until blank line**

**Store as:** `OUT_OF_SCOPE` (array)

---

#### 4. Stakeholders

**Explanation:**
```
STAKEHOLDERS: Who is involved in or affected by this project?

Categories:
- Primary Users/Beneficiaries: Who directly benefits?
- Contributors: Who builds/maintains this?
- Secondary Stakeholders: Who is indirectly affected?
- Advisory/Oversight: Who provides guidance or approval?
```

**Prompt:**
"Who are the PRIMARY USERS/BENEFICIARIES?"
"Enter one per line. Blank line when done."

**Store as:** `STAKEHOLDERS_PRIMARY` (array)

**Prompt:**
"Who are the CONTRIBUTORS (builders, maintainers)?"
"Enter one per line. Blank line when done."

**Store as:** `STAKEHOLDERS_CONTRIBUTORS` (array)

**Prompt:**
"Who are SECONDARY STAKEHOLDERS (indirectly affected/have input)? (optional)"
"Enter one per line. Blank line when done."

**Store as:** `STAKEHOLDERS_SECONDARY` (array)

**Prompt:**
"Who provides ADVISORY/OVERSIGHT? (optional)"
"Enter one per line. Blank line when done."

**Store as:** `STAKEHOLDERS_ADVISORY` (array)

---

#### 5. Success Criteria

**Explanation:**
```
SUCCESS CRITERIA: How do you know when you've succeeded?

Think outcomes, not just outputs:
- Bad: "Ship 50 features"
- Good: "80% user satisfaction in post-deployment survey"

Include:
- Primary Success Metrics (measurable outcomes)
- Milestones (time-bound achievements)
- Quality Indicators (how you measure quality)
```

**Prompt:**
"What are your PRIMARY SUCCESS METRICS? (measurable outcomes)"
"Enter one per line. Blank line when done."

**Store as:** `SUCCESS_METRICS` (array)

**Prompt:**
"What are your MILESTONES? (time-bound achievements)"
"Enter one per line. Blank line when done."

**Store as:** `SUCCESS_MILESTONES` (array)

**Prompt:**
"What are your QUALITY INDICATORS? (how you measure quality)"
"Enter one per line. Blank line when done."

**Store as:** `SUCCESS_QUALITY` (array)

---

#### 6. Constraints

**Explanation:**
```
CONSTRAINTS: What limits your work?

Categories:
- Timeline: Deadlines, funding periods
- Resources: Budget, team size
- Technical: Platform requirements, performance needs
- Regulatory: Legal, ethical, compliance requirements
- Other: Domain-specific constraints
```

**For each category, prompt:**
"[CATEGORY] CONSTRAINTS: (Enter items or press Enter to skip)"
"Enter one per line. Blank line when done."

**Store as:**
- `CONSTRAINTS_TIMELINE` (array)
- `CONSTRAINTS_RESOURCES` (array)
- `CONSTRAINTS_TECHNICAL` (array)
- `CONSTRAINTS_REGULATORY` (array)
- `CONSTRAINTS_OTHER` (array)

---

#### 7. Domain Context

**Explanation:**
```
DOMAIN CONTEXT: Project-specific context that guides work.

This is where domain expertise lives. The questions depend on your project type.
```

**Get project type from CLAUDE.md or ask:**
"Project type: (s)oftware, (p)ublic-health, (r)esearch, or (o)ther?"

**Based on project type, ask domain-specific questions:**

##### For SOFTWARE:

**Tech Stack:**
"What is your tech stack? (e.g., language/framework, database, infrastructure)"
"Enter one per line. Blank line when done."
**Store as:** `DOMAIN_TECH_STACK` (array)

**Architecture Approach:**
"What is your architecture approach? (e.g., monolith, microservices, serverless, and why)"
**Store as:** `DOMAIN_ARCHITECTURE` (string)

**Quality Standards:**
"What are your quality standards? (testing approach, performance targets, security requirements)"
"Enter one per line. Blank line when done."
**Store as:** `DOMAIN_QUALITY` (array)

##### For PUBLIC-HEALTH:

**Theoretical Framework:**
"What theoretical framework guides this intervention? (e.g., Social Cognitive Theory, Health Belief Model)"
**Store as:** `DOMAIN_THEORY` (string)

**Evidence Base:**
"What research supports this approach?"
**Store as:** `DOMAIN_EVIDENCE` (string)

**Target Population:**
"Describe the target population: (demographics, health status, setting)"
"Enter one per line. Blank line when done."
**Store as:** `DOMAIN_POPULATION` (array)

**Intervention Model:**
"How does the intervention work? (Theory of change?)"
**Store as:** `DOMAIN_INTERVENTION` (string)

**Evaluation Approach:**
"How will outcomes be measured?"
**Store as:** `DOMAIN_EVALUATION` (string)

##### For RESEARCH:

**Research Questions:**
"What are your research questions? (primary and secondary)"
"Enter one per line. Blank line when done."
**Store as:** `DOMAIN_RESEARCH_QUESTIONS` (array)

**Methodology:**
"What is your methodology? (qualitative/quantitative/mixed-methods and why)"
**Store as:** `DOMAIN_METHODOLOGY` (string)

**Theoretical Framework:**
"What theories guide this research?"
**Store as:** `DOMAIN_THEORY` (string)

**Data Sources:**
"What are your data sources? (where data comes from, sample size)"
"Enter one per line. Blank line when done."
**Store as:** `DOMAIN_DATA_SOURCES` (array)

**Analysis Plan:**
"How will data be analyzed?"
**Store as:** `DOMAIN_ANALYSIS` (string)

**Contribution:**
"How does this advance the field?"
**Store as:** `DOMAIN_CONTRIBUTION` (string)

##### For OTHER:

**Domain:**
"What is your domain/field?"
**Store as:** `DOMAIN_NAME` (string)

**Key Context:**
"What critical information guides work in this domain?"
**Store as:** `DOMAIN_CONTEXT` (string)

---

#### 8. Charter Maintenance

**Explanation:**
```
CHARTER MAINTENANCE: How will you keep this charter current?
```

**Prompt:**
"How often should this charter be reviewed? (e.g., Quarterly, After major milestones):"
**Default:** "Quarterly"
**Store as:** `REVIEW_SCHEDULE` (string)

**Prompt:**
"How are charter changes made? Who approves? (optional):"
**Store as:** `AMENDMENT_PROCESS` (string, optional)

---

### Review and Confirmation

**Show complete charter summary:**
```
📋 Charter Summary
==================

MISSION:
[MISSION]

PRINCIPLES:
1. [principle 1]
2. [principle 2]
...

IN SCOPE:
- [item 1]
- [item 2]
...

OUT OF SCOPE:
- [item 1]
- [item 2]
...

[... continue for all sections ...]
```

**Prompt:**
"Does this look correct? (y)es to save, (e)dit to modify, (c)ancel:"

- `y` - Proceed to save
- `e` - Ask which section to edit, then re-prompt for that section
- `c` - Exit without saving

---

## Generating CHARTER.md

### Step 1: Read Template

Read `.praxisity/templates/charter.template.md`

### Step 2: Fill Template

Replace placeholders with collected values:

- `[One sentence mission statement]` → `MISSION`
- The principles list → `PRINCIPLES` (formatted as numbered list)
- In Scope items → `IN_SCOPE` (formatted as bullet list)
- Out of Scope items → `OUT_OF_SCOPE` (formatted as bullet list)
- Stakeholders sections → Respective stakeholder arrays
- Success Criteria sections → Respective success arrays
- Constraints sections → Respective constraint arrays
- Domain Context sections → Domain-specific content
- Review Schedule → `REVIEW_SCHEDULE`
- Amendment Process → `AMENDMENT_PROCESS`

**Remove:**
- HTML comments (<!-- ... -->)
- Placeholder brackets [ ]
- Domain sections that don't apply to this project type
- Optional sections that were left empty

**Add dates:**
- Charter established: `[CURRENT_DATE]` (if creating new)
- Last reviewed: `[CURRENT_DATE]`
- Next review: Calculate based on review schedule (e.g., +3 months if "Quarterly")

### Step 3: Write File

Write generated content to `CHARTER.md`

Show: "✓ Charter saved to CHARTER.md"

---

## Post-Save Actions

### Update CLAUDE.md

Read `CLAUDE.md` and update:
- Mission (one-liner in Project Identity section)
- Last updated date

Show: "✓ Updated CLAUDE.md with charter mission"

### Create Todoist Task (Optional)

If Todoist MCP is available:

Ask: "Create reminder to review charter? (yes/no)"

If yes:
- Create task: "Review project charter"
- Due date: Based on `REVIEW_SCHEDULE` (e.g., 3 months from now if "Quarterly")
- Project: The project's Todoist project
- Section: "Planning"

Show: "✓ Created charter review reminder in Todoist"

### Git Commit (Optional)

Ask: "Commit charter to git? (yes/no)"

If yes:
```bash
git add CHARTER.md CLAUDE.md
git commit -m "docs(charter): $(if [ create/update ]; then echo 'create' else echo 'update'; fi) project charter

Updated project governance and mission statement"
```

Show: "✓ Committed charter to git"

---

## Success Message

```
✅ Charter $(if create: "Created" else: "Updated")

Your project charter is ready at CHARTER.md

This charter guides:
- All project decisions
- AI assistance behavior
- Scope boundaries
- Success measurement

📝 Next Steps:

1. Share charter with stakeholders for alignment

2. Reference charter when making project decisions

3. Create your first specification:
   /spec

4. Update charter as understanding evolves
   (Run /charter again anytime)

📚 The charter is a living document. Review $(REVIEW_SCHEDULE).
```

### Update PLANNING.md

```markdown
## Completed

- **Charter:** [Created/Updated] CHARTER.md
- **Mission:** [First 50 chars of mission]...
- **Timestamp:** [completion time]

## Next Steps
- [ ] Share charter with stakeholders
- [ ] Create first specification: /spec
```

---

## Command Behavior Notes

**Idempotency:**
- Can be run multiple times safely
- Updates existing charter instead of overwriting
- Preserves git history of charter evolution

**Flexibility:**
- All sections except Mission can be skipped (just press Enter)
- Can edit individual sections after review
- Domain sections auto-selected based on project type

**Validation:**
- Minimal validation to avoid being annoying
- Warnings for too-brief answers, but allow user choice
- Mission and principles required; others optional

**User Experience:**
- Clear explanations before each section
- Domain-specific examples
- Review before saving
- Ability to edit after review

**PLANNING.md Integration:**
- Reads existing context on start
- Updates with command start
- Records completion and next steps
- Enables session recovery if interrupted
