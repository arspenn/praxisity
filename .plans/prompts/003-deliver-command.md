# DIP-003: Implement /deliver Command and Style Module

> **For AI Agent:** This is a Detailed Implementation Prompt. Follow these instructions precisely.
> Read all referenced documents before beginning implementation.
>
> **TodoWrite Integration:** Use Claude's TodoWrite tool to track progress through this DIP.
> Create todos from the Implementation Steps below and mark them complete as you progress.

## Context

| Field | Value |
|-------|-------|
| DIP ID | DIP-003 |
| Task | Implement the /deliver command and ReportLab style module |
| Spec | [SPEC-003](../../.plans/specs/003-deliver-command.md) |
| Design | [DESIGN-003](../../.plans/designs/003-deliver-command.md) |
| Todoist Task | N/A |
| Created | 2026-03-21 |

## Objective

Create the `/deliver` command (`.claude/commands/deliver.md`) and the ReportLab style module (`.praxisity/praxisity_style.py`) that together convert markdown documents into professionally styled PDFs.

## Required Reading

Before implementation, read and understand these sections:

### From Specification (SPEC-003)
- [ ] Section 3.1: REQ-F1 - File selection/path input
- [ ] Section 3.1: REQ-F2 - Style module for consistent formatting
- [ ] Section 3.1: REQ-F3 - Parse markdown and provide structured content
- [ ] Section 3.1: REQ-F4 - Output to `deliverables/` directory
- [ ] Section 3.1: REQ-F5 - Generate output filename from source
- [ ] Section 3.1: REQ-F6 - Report success or failure with path
- [ ] Section 3.1: REQ-F7 - Optionally commit to git
- [ ] Section 3.1: REQ-F8 - Update PLANNING.md
- [ ] Section 3.2: REQ-N1 - Single generic style module, extensible
- [ ] Section 3.2: REQ-N2 - Professional-quality output
- [ ] Section 4: UC-1 - Generate PDF from a Spec or Design Document
- [ ] Section 4: UC-2 - Generate PDF from a Project Deliverable
- [ ] Section 5: AC-1 through AC-4

### From Design (DESIGN-003)
- [ ] Section 3: COMP-1 - Pre-Flight
- [ ] Section 3: COMP-2 - Generation and Delivery
- [ ] Section 4: INT-1 - Style Module Interface
- [ ] Section 4: INT-2 - PLANNING.md Interface
- [ ] Section 5: DATA-1 - Delivery Job
- [ ] Section 6: DEC-1 - ReportLab via Claude's Built-in Capability
- [ ] Section 6: DEC-2 - Style Module as Python File
- [ ] Section 6: DEC-3 - No Template Selection at MVP
- [ ] Section 9: DQ-1 - Style decisions (all resolved)

### From Supporting Documents
- [ ] [ReportLab Scoping Report](../references/praxisity-reportlab-template-scope.md) - Style module structure, component details, font paths

### From Charter
- [ ] Principle 4: Self-documenting (git-versioned documents with professional PDF outputs)

## Implementation Instructions

> **Agent Action:** Before starting, use TodoWrite to create todos from these steps:
> ```
> TodoWrite([
>   { content: "Read required spec/design sections", status: "pending", activeForm: "Reading documentation" },
>   { content: "Step 1: Create praxisity_style.py", status: "pending", activeForm: "Building style module" },
>   { content: "Step 2: Write deliver.md command", status: "pending", activeForm: "Writing deliver command" },
>   { content: "Step 3: Test with a real document", status: "pending", activeForm: "Testing PDF generation" },
>   { content: "Verify acceptance criteria", status: "pending", activeForm: "Verifying acceptance criteria" },
>   { content: "Complete safety checklist and commit", status: "pending", activeForm: "Completing safety checklist" }
> ])
> ```
> Mark each todo in_progress when starting, completed when done.

### Step 1: Create `praxisity_style.py` style module

Build the Python module at `.praxisity/praxisity_style.py` per the ReportLab scoping report structure:

**1.1 Font Registration Block (~25-35 lines)**
- Register Liberation Sans (Regular, Bold, Italic, BoldItalic) for body and headings
- Register Liberation Mono (Regular, Bold, Italic, BoldItalic) for code blocks
- Create font family mappings so bold/italic markup selects correct variants
- Include fallback to Helvetica/Courier if font files not found at expected paths

**1.2 Color Constants (~10-15 lines)**
- Body text color
- Secondary text color (metadata, captions)
- Accent color (headings)
- Border color (table rules)
- Background color (code blocks, table header)

**1.3 Page Layout Definition (~60-100 lines)**
- Page size: US Letter (8.5 x 11 inches)
- Margins: 1 inch all sides
- Single column layout
- No header or footer at MVP
- First page: title block at top with extra spacing, content follows

**1.4 Paragraph Styles Dictionary (~80-120 lines)**

| Style Name | Purpose | Key Properties |
|---|---|---|
| Title | Document title on first page | Large, bold, left-aligned |
| Subtitle | Document subtitle/version | Smaller than title, secondary color |
| Heading1 | Major sections | Bold, larger, space above, keepWithNext |
| Heading2 | Subsections | Bold, medium, space above, keepWithNext |
| Heading3 | Sub-subsections | Bold, body size, keepWithNext |
| BodyText | Main content | Left-aligned, standard leading |
| CodeBlock | Preformatted code | Monospace, smaller, background shading |
| Caption | Table captions | Smaller, secondary color |
| Metadata | Author, date info | Small, secondary color |

All styles use Liberation Sans except CodeBlock (Liberation Mono). Arabic numbering (1, 1.1, 1.2). Left-aligned text throughout.

**1.5 Table Style Defaults (~20-30 lines)**
- Minimal horizontal rules (IEEE-inspired): line above header, line below header, line below last row
- No vertical lines
- Light background on header row
- Bold font on header row
- Consistent cell padding

**1.6 Convenience Builder Functions (~50-80 lines)**
- `create_document(filename, title, author)` — returns a configured BaseDocTemplate
- `build_table(data, col_widths)` — returns a styled Table with defaults applied
- `code_block(text)` — returns a properly styled preformatted Paragraph

**Input:** ReportLab scoping report, DQ-1 style decisions
**Output:** `.praxisity/praxisity_style.py` (~250-380 lines)
**Verify:** Module imports without error; `python -c "import praxisity_style"` from `.praxisity/` succeeds

**TodoWrite:** Mark "Step 1" as `in_progress` before starting, `completed` when done.

### Step 2: Write deliver.md command

Write `.claude/commands/deliver.md` covering both components:

**COMP-1 (Pre-Flight):**
- Read PLANNING.md for session context
- Accept file path argument or list project markdown files for selection
- Verify `praxisity_style.py` exists at `.praxisity/praxisity_style.py` — if missing, halt with clear message

**COMP-2 (Generation and Delivery):**
- Read and parse the source markdown file
- Instruct Claude to generate a PDF using ReportLab, importing `praxisity_style.py` for all styling
- Create `deliverables/` directory if it doesn't exist
- Generate output filename from source file name (e.g., `002-build-command.md` → `002-build-command.pdf`)
- If generation fails, surface the error for user to diagnose
- On success, report output file path
- Offer to commit the deliverable to git (specific file add)
- Update PLANNING.md with delivery status

Keep the command concise and imperative — no rationale or explanations.

**Input:** DESIGN-003, existing command patterns
**Output:** `.claude/commands/deliver.md`
**Verify:** Command file exists with proper frontmatter; follows structural patterns of other commands

**TodoWrite:** Mark "Step 2" as `in_progress` before starting, `completed` when done.

### Step 3: Test with a real document

- Invoke `/deliver` and select SPEC-002 (build command spec) as source
- Visually review the generated PDF for:
  - Title block renders correctly
  - Headings follow size hierarchy
  - Tables render with minimal rules and proper alignment
  - Code blocks have monospace font and background
  - Page margins are consistent
  - Text is left-aligned
- If quality issues exist, iterate on `praxisity_style.py` until output is professional

**Input:** Generated PDF from SPEC-002
**Output:** Verified, professional-quality PDF in `deliverables/`
**Verify:** PDF opens correctly; visual review passes for typography, tables, and layout

**TodoWrite:** Mark "Step 3" as `in_progress` before starting, `completed` when done.

## Technical Requirements

### Must Implement
- [ ] File selection from project markdown files or path argument (REQ-F1)
- [ ] PDF generation using `praxisity_style.py` for consistent formatting (REQ-F2)
- [ ] Markdown parsing and structured content for ReportLab (REQ-F3)
- [ ] Output to `deliverables/` directory (REQ-F4)
- [ ] Automatic output filename from source name (REQ-F5)
- [ ] Success/failure reporting with file path (REQ-F6)
- [ ] Optional git commit of deliverable (REQ-F7)
- [ ] PLANNING.md update (REQ-F8)
- [ ] Single generic style module, extensible structure (REQ-N1)
- [ ] Professional-quality output (REQ-N2)

### Must Satisfy
| Requirement | How to Satisfy |
|-------------|----------------|
| REQ-F1 | List markdown files or accept path argument |
| REQ-F2 | Import and use `praxisity_style.py` for all PDF styling |
| REQ-F4 | Create `deliverables/` if missing, write PDF there |
| REQ-F5 | Strip `.md` extension, add `.pdf` |
| REQ-N2 | IEEE-inspired minimal design with clean typography |

### Interfaces to Implement/Use
| Interface | Role | Contract Reference |
|-----------|------|-------------------|
| INT-1 | Implement | Style module exports fonts, colors, styles, builders |
| INT-2 | Use | Read/write PLANNING.md for state |

### Data Entities to Create/Modify
| Entity | Action | Schema Reference |
|--------|--------|-----------------|
| DATA-1 (Delivery Job) | Create | Tracked during command execution |

## Scope Boundaries

### DO (In Scope)
- Create the style module with all components from scoping report
- Write the deliver command covering both components
- Test against a real project document
- Apply resolved style decisions (sans-serif, left-aligned, Arabic numbering, 1" margins, no header/footer, title block)

### DO NOT (Out of Scope)
- Do not create multiple style variants
- Do not add citation/bibliography support
- Do not support HTML or DOCX output
- Do not support batch generation
- Do not modify other commands
- Do not modify CLAUDE.md
- Do not add Pandoc or LaTeX dependencies
- Do not add image embedding (text-only at MVP)

### Files in Scope
```
.claude/commands/deliver.md
.praxisity/praxisity_style.py
deliverables/ (created by command)
```

### Files Out of Scope
```
.praxisity/templates/pandoc/ (deprecated, do not modify)
.claude/commands/ (all other commands)
CLAUDE.md
```

## Acceptance Criteria

All criteria must pass for this DIP to be considered complete.

| ID | Criterion | Test |
|----|-----------|------|
| AC-1 | Given markdown files in the project, when `/deliver` is invoked, then available files are presented for selection | Invoke `/deliver`, verify file list appears |
| AC-2 | Given a source file, when PDF generation runs, then output uses consistent styling from `praxisity_style.py` | Visual review of generated PDF — fonts, spacing, tables match style module |
| AC-3 | Given a source file, when generation completes, then a PDF exists in `deliverables/` | Check `deliverables/` directory for output file |
| AC-4 | Given a generated PDF, when the command completes, then the output file path is reported to the user | Observe command output message |

### Verification Commands
```bash
# Verify command file exists
ls -la .claude/commands/deliver.md

# Verify style module exists
ls -la .praxisity/praxisity_style.py

# Verify style module imports cleanly
cd .praxisity && python -c "import praxisity_style; print('OK')"

# Verify deliverables directory and output
ls -la deliverables/
```

## Safety Checklist

Before committing, verify:

- [ ] No secrets, keys, or credentials in code
- [ ] No `git add .` or `git add -A` used
- [ ] All new files explicitly added
- [ ] Conventional commit message prepared
- [ ] No unrelated changes included

## Commit Instructions

When implementation is complete:

```bash
# Stage only files in scope
git add .claude/commands/deliver.md .praxisity/praxisity_style.py

# Commit with conventional format
git commit -m "feat(commands): add /deliver command with ReportLab style module

Implements DIP-003: /deliver command and praxisity_style.py
Satisfies: REQ-F1, REQ-F2, REQ-F3, REQ-F4, REQ-F5, REQ-F6, REQ-F7, REQ-F8, REQ-N1, REQ-N2"
```

**Commit type:** feat
**Scope:** commands

## Completion Checklist

> **Agent Action:** Work through this checklist, marking each item in your TodoWrite as you go.

- [ ] All implementation steps completed (all step todos marked `completed`)
- [ ] All acceptance criteria verified (verification commands passed)
- [ ] Safety checklist passed (no secrets, explicit git adds)
- [ ] Code committed with proper message
- [ ] PLANNING.md updated with completion status
- [ ] TodoWrite cleared or marked all complete

## Notes

- The style module is the implementation dependency — build it first, then the command
- Reference the ReportLab scoping report (`temp/praxisity-reportlab-template-scope.md`) for detailed component specifications and font paths
- The `deliverables/` directory should be added to `.gitignore` if PDF files should not be tracked, or committed if version-controlled outputs are desired — let the user decide during the git commit step
- The `.praxisity/templates/pandoc/` directory with its `.gitkeep` is now deprecated but should not be removed as part of this DIP

---

**End of DIP-003**

> **Final Agent Actions:**
> 1. Ensure all TodoWrite items are marked `completed`
> 2. Update PLANNING.md with:
>    - DIP completion status
>    - Any deviations or decisions made
>    - Next suggested action