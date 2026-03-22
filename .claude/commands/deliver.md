---
description: Generate a professional PDF from a markdown document
tags: [delivery, pdf, output, reportlab]
---

# Deliver Command

Generate a professional PDF from a project markdown document using the Praxisity style module.

## Constraints

- Use ReportLab with `.praxisity/praxisity_style.py` for all styling
- Output to `deliverables/` directory only
- Generate filename from source file name — do not ask the user to name the output
- Do not use Pandoc, LaTeX, or any external PDF tools
- Keep the generated Python script focused — import the style module, don't redefine styles inline

## Pre-Flight

1. Read PLANNING.md for session context; create if missing
2. Update PLANNING.md with /deliver as active command
3. Verify `.praxisity/praxisity_style.py` exists — if missing, halt with message: "Style module not found. Ensure praxisity_style.py exists in .praxisity/"
4. If argument provided, use it as source file path
5. If no argument: list project markdown files and prompt for selection
   - Include files from: project root, `.plans/specs/`, `.plans/designs/`, `docs/`
   - Exclude: PLANNING.md, CLAUDE.md, node_modules, .git

## Generation

1. Read the source markdown file
2. Parse the markdown into structured elements:
   - Title (from first `#` heading)
   - Metadata (from tables at the top, if present)
   - Headings (`##`, `###`, `####`)
   - Body paragraphs
   - Tables (pipe-delimited markdown tables)
   - Code blocks (fenced with ```)
   - Bullet lists
3. Create `deliverables/` directory if it doesn't exist
4. Generate output filename: strip `.md` extension, add `.pdf` (e.g., `002-build-command.md` → `002-build-command.pdf`)
5. Write and execute a Python script that:
   - Imports from `praxisity_style` (add `.praxisity/` to sys.path)
   - Uses `create_document()` for page setup
   - Uses `title_block()` for the first page
   - Maps markdown elements to style module styles:
     - `##` → `styles["Heading1"]`
     - `###` → `styles["Heading2"]`
     - `####` → `styles["Heading3"]`
     - Body text → `styles["BodyText"]`
     - Bullet items → `styles["BulletItem"]`
     - Code blocks → `code_block()`
     - Tables → `build_table()`
   - Builds the document with `doc.build(elements)`
6. If generation fails, show the error and ask user how to proceed

## Post-Generation

1. Report success with the output file path
2. Offer to commit the deliverable to git:
   - Stage only the PDF file: `git add deliverables/[filename].pdf`
   - Commit with: `docs(deliverables): generate [filename].pdf via /deliver`
3. Update PLANNING.md with delivery status and output path

## Success Message

Confirm PDF was generated. Show:
- Source file
- Output path
- Page count (if available)
- Suggested next steps

---

## Behavior Notes

- Each run generates ONE PDF from ONE source file
- No template selection at MVP — the style module is used automatically
- If only structural elements (headings, tables) are present with minimal prose, the output will still be professional
- Markdown parsing should be tolerant of format variations
- PLANNING.md integration: reads context, records delivery status


ARGUMENTS: $ARGUMENTS