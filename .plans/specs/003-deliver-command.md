# Specification: SPEC-003 Deliver Command

## Metadata

| Field | Value |
|-------|-------|
| Spec ID | SPEC-003 |
| Title | Deliver Command |
| Status | Draft |
| Author | Andrew Robert Spenn |
| Created | 2026-03-21 |
| Last Updated | 2026-03-21 |
| Charter Reference | [CHARTER.md](../../CHARTER.md) — Principle 4 (self-documenting) |

### Related Documents

| Document | Relationship |
|----------|--------------|
| [SPEC-002](002-build-command.md) | Related to — /build produces artifacts that /deliver converts |
| [Foundation Plan](../../praxisity-foundation-plan.md) | Depends on — Pandoc Integration section (approach revised to ReportLab) |
| [ReportLab Scoping Report](../references/praxisity-reportlab-template-scope.md) | Depends on — defines style module approach and environment capabilities |

---

## 1. Problem Statement

The Praxisity framework produces markdown documents throughout its workflow — specs, designs, reports, research outputs — but has no command to convert them into professional deliverables. Users must manually generate PDFs with inconsistent formatting and manage output paths. This prevents the framework from completing its lifecycle and limits its usefulness for practitioners who need to share polished outputs with stakeholders.

---

## 2. Goals and Objectives

### 2.1 Primary Goal

Convert markdown documents into professional PDF deliverables using a consistent style module with minimal user configuration.

### 2.2 Objectives

| ID | Objective | Success Metric |
|----|-----------|----------------|
| OBJ-1 | Generate PDF output from any markdown document in the project | PDF produced in `deliverables/` directory |
| OBJ-2 | Produce consistent, professional output through a reusable style module | All generated PDFs follow the same typography, layout, and formatting |
| OBJ-3 | Require minimal user input beyond source file selection | User selects file, command handles the rest |

---

## 3. Requirements

### 3.1 Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-F1 | The command shall accept a markdown file path or present project markdown files for selection | MUST | Entry point to delivery |
| REQ-F2 | The command shall instruct Claude to generate a PDF using the `praxisity_style.py` module for consistent formatting | MUST | Style consistency is the core value |
| REQ-F3 | The command shall parse the source markdown and provide it as structured content for PDF generation | MUST | Claude needs the content to render |
| REQ-F4 | The command shall output to `deliverables/` directory, creating it if needed | MUST | Consistent output location |
| REQ-F5 | The command shall generate a sensible output filename from the source file name | MUST | No manual naming required |
| REQ-F6 | The command shall report success or failure with the output file path | MUST | User needs to know where to find the deliverable |
| REQ-F7 | The command shall optionally commit the deliverable to git | SHOULD | Version-controlled outputs |
| REQ-F8 | The command shall update PLANNING.md with delivery status | SHOULD | Session state continuity |

### 3.2 Non-Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-N1 | The command shall use a single generic style module at MVP, with the module structure supporting future domain-specific variants | MUST | Start simple, extend later |
| REQ-N2 | The command shall produce professional-quality output suitable for stakeholder review | SHOULD | The whole point of PDF delivery |

---

## 4. User Stories / Use Cases

### UC-1: Generate PDF from a Spec or Design Document

**Actor:** Practitioner needing to share planning artifacts with stakeholders

**Preconditions:**
- Markdown source file exists
- `praxisity_style.py` module exists in `.praxisity/`

**Flow:**
1. User invokes `/deliver`
2. Command presents markdown files for selection
3. User selects source file
4. Command reads the markdown, instructs Claude to generate a PDF using the style module
5. PDF is written to `deliverables/`
6. Command reports output path
7. Optionally commits deliverable to git

**Postconditions:**
- PDF exists in `deliverables/`
- PLANNING.md updated

**Alternative Flows:**
- Generation fails: command surfaces the error for user to diagnose

---

### UC-2: Generate PDF from a Project Deliverable

**Actor:** Researcher or consultant producing a final report

**Preconditions:**
- Markdown document written (in `docs/` or project root)

**Flow:**
1. User invokes `/deliver` with file path argument
2. Command skips file selection
3. Command generates PDF using style module
4. Reports output path

**Postconditions:**
- Professional PDF ready for distribution

---

## 5. Acceptance Criteria

| ID | Criterion | Validates |
|----|-----------|-----------|
| AC-1 | Given markdown files in the project, when `/deliver` is invoked, then available files are presented for selection | REQ-F1 |
| AC-2 | Given a source file, when PDF generation runs, then the output uses consistent styling from `praxisity_style.py` | REQ-F2, REQ-N2 |
| AC-3 | Given a source file, when generation completes, then a PDF exists in `deliverables/` | REQ-F3, REQ-F4 |
| AC-4 | Given a generated PDF, when the command completes, then the output file path is reported to the user | REQ-F5, REQ-F6 |

---

## 6. Constraints

### 6.1 Inherited from Charter

- Timeline: 4 weeks to MVP
- Scope: Strict MVP discipline to avoid feature creep

### 6.2 Spec-Specific Constraints

- PDF generation uses Claude's built-in ReportLab capability — no external dependencies required
- MVP ships with one generic style module; domain-specific variants are post-MVP

---

## 7. Dependencies

### 7.1 Depends On

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| ReportLab | Built-in | Available | Already present in Claude environment |
| `praxisity_style.py` | Resource | Not yet built | Style module defining fonts, layout, table styles |

### 7.2 Enables

| Dependent | Relationship |
|-----------|--------------|
| End-to-end workflow test | `/deliver` completes the full charter-to-PDF lifecycle |
| Portfolio documentation | Professional outputs for showcasing projects |

---

## 8. Out of Scope

The following are explicitly NOT part of this specification:

- Multiple domain-specific style variants beyond one generic (post-MVP)
- Citation management and bibliography generation (post-MVP)
- HTML or other non-PDF output formats (post-MVP)
- Batch generation of multiple documents in one invocation (post-MVP)
- Custom styling or style module creation workflow (post-MVP)
- Pandoc or LaTeX-based generation (replaced by ReportLab approach)

---

## 9. Open Questions

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| Q-1 | What PDF generation approach should be used? | Resolved | ReportLab via Claude's built-in capability. No external dependencies. Style consistency provided by `praxisity_style.py` module. |
| Q-2 | Should `/deliver` support non-PDF output (HTML, DOCX) at MVP? | Resolved | No — PDF only at MVP |
| Q-3 | Style decisions (serif/sans, alignment, margins, headers, numbering, first page) | Open | To be resolved before implementation |

---

## 10. References

- [CHARTER.md](../../CHARTER.md)
- [Foundation Plan](../../praxisity-foundation-plan.md)
- [ReportLab Scoping Report](../references/praxisity-reportlab-template-scope.md)
- [ReportLab User Guide](https://docs.reportlab.com/reportlab/userguide/)
- IEEE Editorial Style Manual — visual reference for clean document formatting

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-03-21 | Andrew Robert Spenn | Initial draft (Pandoc/LaTeX approach) |
| 0.2 | 2026-03-21 | Andrew Robert Spenn | Revised to ReportLab approach — removed all Pandoc/LaTeX dependencies |