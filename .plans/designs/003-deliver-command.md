# Design: DESIGN-003 Deliver Command

## Metadata

| Field | Value |
|-------|-------|
| Design ID | DESIGN-003 |
| Title | Deliver Command Design |
| Status | Draft |
| Author | Andrew Robert Spenn |
| Created | 2026-03-21 |
| Last Updated | 2026-03-21 |

### Specification References

| Spec ID | Title | Requirements Addressed |
|---------|-------|------------------------|
| [SPEC-003](../specs/003-deliver-command.md) | Deliver Command | REQ-F1 through REQ-F8, REQ-N1, REQ-N2 |

### Related Documents

| Document | Relationship |
|----------|--------------|
| [DESIGN-002](002-build-command.md) | Related to — /build produces artifacts that /deliver converts |
| [ReportLab Scoping Report](../references/praxisity-reportlab-template-scope.md) | Depends on — defines style module structure and environment capabilities |

---

## 1. Overview

### 1.1 Design Summary

The `/deliver` command is a Claude Code command (`.claude/commands/deliver.md`) that generates professional PDFs from project markdown files. It reads the source markdown, then instructs Claude to generate a PDF using ReportLab with a consistent style module (`praxisity_style.py`). The style module defines fonts, colors, page layout, paragraph styles, and table formatting so that every PDF produced by the framework looks consistent.

The command has two implementation artifacts: the command file itself (orchestration) and the style module (visual consistency).

### 1.2 Design Principles

- **Fail early, fail clearly** — Check for style module before attempting generation; surface actionable error messages
- **Minimal decisions** — User picks the file; everything else is automatic
- **Extensible by convention** — Style module structure supports future domain-specific variants without command changes

### 1.3 Requirements Coverage

| Requirement | Design Section | Approach |
|-------------|----------------|----------|
| REQ-F1 | COMP-1 | Accept path argument or list project markdown files |
| REQ-F2 | COMP-2 | Import `praxisity_style.py` for consistent formatting |
| REQ-F3 | COMP-2 | Parse markdown, build ReportLab document with styled elements |
| REQ-F4 | COMP-2 | Create `deliverables/` if needed, write output there |
| REQ-F5 | COMP-2 | Derive filename from source file name |
| REQ-F6 | COMP-2 | Report output path on success, surface error on failure |
| REQ-F7 | COMP-2 | Offer to `git add` and commit the deliverable |
| REQ-F8 | COMP-2 | Write delivery status to PLANNING.md |
| REQ-N1 | COMP-1, COMP-2 | Ship one style module; structure supports future variants |
| REQ-N2 | COMP-2 | Professional output via IEEE-inspired style module |

---

## 2. Architecture

### 2.1 System Context

```
┌─────────────┐     ┌─────────────┐
│  Pre-Flight │────▶│ Generation  │
│             │     │ & Delivery  │
│ - Select md │     │             │
│ - Verify    │     │ - Parse md  │
│   style mod │     │ - ReportLab │
└─────────────┘     │ - Output    │
                    │ - Report    │
                    │ - Git?      │
                    │ - State     │
                    └─────────────┘
                         │
                         ▼ (on failure)
                    ┌──────────┐
                    │  HALT    │
                    │ Show err │
                    └──────────┘
```

### 2.2 Architecture Pattern

**Pattern:** Linear pipeline — two phases. No loops, no verification duality.

**Rationale:** Simple wrapper around PDF generation. Complexity lives in the style module, not the command flow.

### 2.3 Technology Choices

| Layer/Concern | Technology | Rationale |
|---------------|------------|-----------|
| Command format | Markdown (`.claude/commands/deliver.md`) | Framework standard |
| PDF generation | ReportLab (Platypus) | Built into Claude environment, no external dependencies |
| Style definition | Python module (`praxisity_style.py`) | Importable by any PDF generation script, provides consistent styling |
| Fonts | Liberation family (Serif, Sans, Mono) | Available in Claude environment, metrically equivalent to Times/Arial/Courier |

---

## 3. Components

### COMP-1: Pre-Flight

**Purpose:** Verify prerequisites and gather user selection.

**Satisfies:** REQ-F1

**Responsibilities:**
- Read PLANNING.md for session context
- Accept file path argument or list project markdown files for selection
- Verify `praxisity_style.py` exists — if missing, halt with clear message

**Dependencies:**
- `.praxisity/praxisity_style.py`
- PLANNING.md

---

### COMP-2: Generation and Delivery

**Purpose:** Parse markdown, generate PDF with consistent styling, report results, update state.

**Satisfies:** REQ-F2, REQ-F3, REQ-F4, REQ-F5, REQ-F6, REQ-F7, REQ-F8, REQ-N2

**Responsibilities:**
- Read and parse the source markdown file
- Generate a Python script that imports `praxisity_style.py` and builds a ReportLab PDF from the parsed content
- Create `deliverables/` directory if it doesn't exist
- Generate output filename from source file name
- Execute the script to produce the PDF
- If generation fails, surface the error for user to diagnose
- On success, report output file path
- Offer to commit the deliverable to git
- Update PLANNING.md with delivery status

**Dependencies:**
- COMP-1 (source file selection)
- `praxisity_style.py` (style definitions)
- ReportLab (built-in)
- Git CLI (optional)
- PLANNING.md

---

## 4. Interfaces

### INT-1: Style Module Interface

**Connects:** COMP-2 ↔ `praxisity_style.py`

**Type:** Python import

**Direction:** Read

**Contract:**
- Module exports: font registration function, color constants, page layout definitions, paragraph style dictionary, table style defaults, convenience builder functions
- COMP-2 imports and uses these to produce consistently styled PDF output

---

### INT-2: PLANNING.md Interface

**Connects:** COMP-1, COMP-2 ↔ PLANNING.md

**Type:** File

**Direction:** Bidirectional

**Contract:**
- Read: session context
- Write: delivery status, output path, source file reference

---

## 5. Data Model

### DATA-1: Delivery Job

**Purpose:** Represents a single invocation of `/deliver`.

**Used by:** COMP-1, COMP-2

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Source File | Path | Yes | Markdown file to convert |
| Output Path | Path | Generated | `deliverables/[source-name].pdf` |
| Style Module | Path | Fixed | `.praxisity/praxisity_style.py` |
| Status | Enum | Yes | Pending → Generating → Complete → Failed |
| Error Output | Text | No | Error details if generation fails |

**Constraints:**
- Source file must be markdown
- Output filename derived from source filename

---

## 6. Design Decisions

### DEC-1: ReportLab via Claude's Built-in Capability, Not Pandoc/LaTeX

**Context:** The original design used Pandoc + lualatex, requiring users to install both tools. Finding compatible, properly licensed LaTeX templates proved difficult.

**Decision:** Use ReportLab (already available in Claude's environment) with a Python style module for consistent formatting. No external dependencies.

**Rationale:** ReportLab is already present. It eliminates the Pandoc + LaTeX dependency chain, template compatibility issues, and engine selection concerns. The style module provides the same consistency benefit as a LaTeX template.

**Alternatives Considered:**
- Pandoc + lualatex: Heavy dependencies, template compatibility issues, licensing concerns
- Pandoc + Typst: Newer, less proven ecosystem
- Raw Claude PDF generation without style module: Inconsistent output

**Consequences:**
- Zero external dependencies for PDF generation
- Style module must be built and maintained as a project artifact
- PDF quality depends on ReportLab capabilities (good for documents, less flexible than LaTeX for complex academic layouts — acceptable for MVP)

---

### DEC-2: Style Module as Python File, Not Configuration

**Context:** The styling rules could be a YAML config, a JSON file, or a Python module.

**Decision:** Python module (`praxisity_style.py`) that exports ReportLab style objects and builder functions directly.

**Rationale:** ReportLab's API is Python-native. A Python module can export ready-to-use `ParagraphStyle` objects, `TableStyle` definitions, and convenience functions. A config file would require a parser layer translating config into ReportLab API calls — added complexity with no benefit.

**Alternatives Considered:**
- YAML/JSON config: Requires translation layer, can't express ReportLab-specific constructs naturally
- Inline in command: Not reusable, bloats the command file

**Consequences:**
- Style module is directly importable — no parsing needed
- Tightly coupled to ReportLab API (acceptable — ReportLab is the only PDF engine at MVP)

---

### DEC-3: No Template Selection at MVP

**Context:** The Pandoc-based design had template selection. With a single style module, there's nothing to select.

**Decision:** At MVP, the style module is automatically used. No selection step. When future variants are added, the command can be extended to offer a choice.

**Rationale:** One style module = no decision needed. Minimal user input (design principle 2).

**Consequences:**
- MVP flow is: select file → generate. One decision.
- Future variants require command update to add selection logic

---

### DEC-4: Reference Files Stored in `.plans/references/`

**Context:** External reference documents (IEEE style guides, ReportLab scoping report) were uploaded to a `temp/` directory during design. These are referenced by the spec and design but had no permanent home.

**Decision:** Create `.plans/references/` as a permanent location for external reference materials. Move all reference files there and update document links.

**Rationale:** The `.plans/` directory already organizes planning artifacts by type (specs, designs, prompts, decisions). References are a natural addition. `temp/` communicates impermanence, which is wrong for documents that specs and designs depend on.

**Consequences:**
- Reference documents are version-controlled alongside the artifacts that cite them
- `.plans/` directory structure gains a new subdirectory

---

## 7. Implementation Considerations

### 7.1 Implementation Order

| Order | Component | Dependencies | Notes |
|-------|-----------|--------------|-------|
| 1 | `praxisity_style.py` | None | Must exist before the command can be tested |
| 2 | COMP-1 (Pre-Flight) | Style module | File selection, module verification |
| 3 | COMP-2 (Generation and Delivery) | COMP-1, style module | PDF generation, reporting, state update |

### 7.2 Risk Areas

| Risk | Impact | Mitigation |
|------|--------|------------|
| ReportLab table rendering with complex/wide tables | Tables may overflow or render poorly | Test style module against actual spec/design documents with heavy tables; adjust column widths in builder functions |
| Markdown parsing edge cases | Some markdown features may not map cleanly to ReportLab elements | Focus on the elements actually used in Praxisity documents (headings, tables, lists, code blocks, paragraphs); skip unsupported features gracefully |
| Style module font paths differ across environments | Font registration fails silently, falls back to Helvetica | Include fallback logic in font registration block |

### 7.3 Testing Strategy

| Level | Approach | Covers |
|-------|----------|--------|
| Style module | Generate test PDF with all style elements (headings, tables, code, lists) | `praxisity_style.py` quality |
| Basic generation | Convert SPEC-002 to PDF via `/deliver` | COMP-1, COMP-2 end-to-end |
| Table-heavy document | Convert a design document with multiple tables | Table style robustness |
| File path argument | Invoke `/deliver` with explicit path | REQ-F1, UC-2 |

---

## 8. Out of Scope

**From Specification (inherited):**
- Multiple domain-specific style variants beyond one generic
- Citation management and bibliography generation
- HTML or other non-PDF output formats
- Batch generation of multiple documents
- Custom styling or style module creation workflow
- Pandoc or LaTeX-based generation

**Design-Specific Exclusions:**
- Style variant selection UI (only one style at MVP)
- Markdown frontmatter/metadata extraction for PDF title pages (content comes from the document itself)
- Image embedding (text-only documents at MVP)

---

## 9. Open Questions

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| DQ-1 | Style decisions | Resolved | (1) Sans-serif body — Liberation Sans for body and headings, Liberation Mono for code. More accessible and modern. (2) Title block at top of first page with extra spacing, no separate cover page. (3) Arabic numbering (1, 1.1, 1.2) — simpler and more flexible than Roman numerals. (4) Left-aligned / ragged right — consistent spacing, avoids awkward justified stretches. (5) No header or footer at MVP. (6) 1" margins all sides (standard US Letter default). |

---

## 10. Appendices

### A. Glossary

| Term | Definition |
|------|------------|
| ReportLab | Python library for PDF generation; Platypus is its high-level document layout engine |
| Style module | `praxisity_style.py` — Python file exporting fonts, colors, paragraph styles, table styles, and builder functions for consistent PDF output |
| Liberation fonts | Open-source font family metrically equivalent to Times New Roman (Serif), Arial (Sans), and Courier New (Mono) |

### B. References

- [SPEC-003: Deliver Command](../specs/003-deliver-command.md)
- [ReportLab Scoping Report](../references/praxisity-reportlab-template-scope.md)
- [ReportLab User Guide](https://docs.reportlab.com/reportlab/userguide/)
- IEEE Editorial Style Manual — visual reference for clean document formatting

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-03-21 | Andrew Robert Spenn | Initial draft (Pandoc/lualatex approach) |
| 0.2 | 2026-03-21 | Andrew Robert Spenn | Revised to ReportLab approach — removed all Pandoc/LaTeX dependencies, restructured components and interfaces |