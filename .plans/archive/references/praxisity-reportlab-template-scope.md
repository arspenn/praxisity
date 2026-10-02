# Praxisity PDF Template - ReportLab Scoping Report

**Date:** December 2025
**Purpose:** Define what is needed to build a deterministic, IEEE-inspired PDF template using ReportLab for use with Claude's built-in PDF generation tools.

---

## 1. Environment Findings

The Claude environment has the following relevant tools verified and available:

**PDF Generation:** ReportLab 4.4.10 is installed with full Platypus support (the high-level document layout engine). This is the tool referenced by Claude's built-in PDF skill at `/mnt/skills/public/pdf/SKILL.md`. LaTeX (pdflatex, xelatex, lualatex) is also present but not recommended for MVP due to special character escaping issues with AI-generated content.

**Available Font Families (TTF, verified registerable):**

| Family | Variants Available | Notes |
|---|---|---|
| Liberation Sans | Regular, Bold, Italic, BoldItalic | Metrically equivalent to Arial. Clean, modern sans-serif. |
| Liberation Serif | Regular, Bold, Italic, BoldItalic | Metrically equivalent to Times New Roman. Closest to IEEE's standard font. |
| Liberation Mono | Regular, Bold, Italic, BoldItalic | Metrically equivalent to Courier New. For code blocks. |
| DejaVu Sans | Regular, Bold, Oblique, BoldOblique, ExtraLight, Condensed variants | Wider character set. Good fallback. |
| DejaVu Serif | Regular, Bold, Italic, BoldItalic, Condensed variants | Alternative serif option. |
| DejaVu Sans Mono | Regular, Bold, Oblique, BoldOblique | Alternative monospace. |

**Font Recommendation:** Liberation Serif (body) + Liberation Sans (headings) + Liberation Mono (code). This closely mirrors IEEE's Times New Roman standard while using freely available fonts that are guaranteed present in the environment. Alternatively, go all-sans with Liberation Sans for a more modern look - this departs from IEEE but aligns better with the "simplified modern" goal.

**ReportLab Layout Components Verified:**

- `BaseDocTemplate` + `PageTemplate` + `Frame` - custom page layouts with headers/footers
- `ParagraphStyle` - full control over font, size, leading, spacing, alignment, indentation
- `TableStyle` - cell-level control over borders, padding, backgrounds, alignment
- `KeepTogether` - prevents page breaks within grouped elements
- `HexColor` - custom colors
- Unit constants: `inch`, `cm`, `mm`
- Text alignment: `TA_LEFT`, `TA_CENTER`, `TA_RIGHT`, `TA_JUSTIFY`

---

## 2. What the Template File Must Contain

The deliverable is a single Python module (e.g., `praxisity_style.py`) that any Claude instance can import when generating a PDF. It needs the following components:

### 2.1 Font Registration Block

Registers TTF fonts with ReportLab and creates font family mappings so bold/italic markup in Paragraphs automatically selects the correct variant. Without this, ReportLab falls back to Helvetica/Courier which are built-in but lower quality.

**Complexity:** Low. Roughly 20-30 lines of boilerplate. Straightforward but must handle the case where font files aren't at the expected path (fallback to Helvetica).

### 2.2 Color Constants

A small set of named hex color values used throughout all styles. Based on the earlier research, this is roughly 5-6 values: body text, secondary text, accent, surface/background, border, and white.

**Complexity:** Trivial. Just named constants.

### 2.3 Page Layout Definition

Uses `BaseDocTemplate` with one or more `PageTemplate` objects that define:

- Page size (US Letter: 8.5 x 11 inches)
- Margins (simplified IEEE: roughly 1 inch all sides, or 1.25 inch left/right for better line length)
- Content frame(s) - single column for our simplified variant
- Header/footer draw functions (called on every page via `onPage`/`onPageEnd` callbacks)

**Complexity:** Medium. The `BaseDocTemplate`/`PageTemplate`/`Frame` pattern is ReportLab's most powerful layout mechanism but also its most verbose. The header/footer callbacks in particular require canvas-level drawing code (lines, text positioning in absolute coordinates). This is the most likely area for bugs.

**Key decisions needed:**

- Static header content (document title? section name? logo placeholder?)
- Footer content (page number style and position)
- Whether the first page gets a different template (cover page vs. content page)

### 2.4 Paragraph Styles Dictionary

A dictionary or stylesheet object defining every text style used in documents. Each `ParagraphStyle` specifies: fontName, fontSize, leading (line height), spaceBefore, spaceAfter, alignment, firstLineIndent, leftIndent, textColor, and keepWithNext.

**Minimum styles needed for MVP:**

| Style Name | Purpose | Key Properties |
|---|---|---|
| `Title` | Document title on first page | Large, bold, centered or left-aligned |
| `Subtitle` | Document subtitle/version | Smaller than title, secondary color |
| `Heading1` | Major sections (roman numeral in IEEE) | Bold, larger, space above, keepWithNext |
| `Heading2` | Subsections | Bold, medium, space above, keepWithNext |
| `Heading3` | Sub-subsections | Bold or bold-italic, body size, keepWithNext |
| `BodyText` | Main content | Justified or left-aligned, standard leading |
| `BodyTextIndent` | Indented body (e.g., under lists) | Same as body with leftIndent |
| `Caption` | Figure/table captions | Smaller, italic or regular, centered |
| `CodeBlock` | Preformatted code | Monospace, smaller, background shading |
| `InlineCode` | Code within paragraphs | Monospace at ~0.9x body size |
| `FooterText` | Running footer | Small, gray, centered |
| `HeaderText` | Running header | Small, gray |
| `Metadata` | Author, date, version info | Small, secondary color |

**Complexity:** Medium. Each style is simple individually but there are many of them and they must be internally consistent (sizes must form a clear hierarchy, spacing must be proportional). Getting the leading (line height) right relative to fontSize is the main tuning challenge.

### 2.5 Table Style Defaults

A `TableStyle` definition for standard data tables. IEEE uses minimal horizontal rules with no vertical lines. In ReportLab terms this means:

- `LINEABOVE` on first row (header separator)
- `LINEBELOW` on first row (header separator)
- `LINEBELOW` on last row (table closer)
- `TOPPADDING` and `BOTTOMPADDING` on all cells
- `BACKGROUND` on header row (light gray)
- `FONTNAME` bold on header row
- `ALIGN` right for numeric columns (this may need to be per-table rather than template-level)

**Complexity:** Low-medium. The `TableStyle` command syntax is list-based and somewhat unintuitive but well-documented.

### 2.6 Convenience/Builder Functions

Optional but highly recommended for the MVP - utility functions that simplify document generation so Claude doesn't have to remember the full ReportLab API every time:

- `create_document(filename, title, author, ...)` - returns a configured BaseDocTemplate
- `build_table(data, col_widths, ...)` - returns a styled Table with defaults applied
- `code_block(text)` - returns a properly styled preformatted Paragraph
- `horizontal_rule()` - returns a thin line spacer

**Complexity:** Medium. These are the "nice to have" that make the template genuinely reusable vs. just a style reference. Without them, every PDF generation task requires Claude to re-implement the same boilerplate.

---

## 3. Complexity Assessment

| Component | Lines (est.) | Difficulty | Risk |
|---|---|---|---|
| Font registration | 25-35 | Low | Font path may vary across environments |
| Color constants | 10-15 | Trivial | None |
| Page layout + header/footer | 60-100 | Medium-High | Header/footer callbacks are fiddly |
| Paragraph styles | 80-120 | Medium | Tuning proportions takes iteration |
| Table style defaults | 20-30 | Low-Medium | ReportLab TableStyle syntax is awkward |
| Convenience functions | 50-80 | Medium | API surface decisions |
| **Total** | **~250-380** | **Medium** | **Integration testing needed** |

The biggest risk is that ReportLab's Platypus layout engine has behaviors that are hard to predict without rendering - things like page break decisions, table splitting across pages, and how `KeepTogether` interacts with available page space. This is why running through the full design workflow is the right call.

---

## 4. Key Design Decisions to Make Before Implementation

These are the "slider" positions that need to be set before writing code:

1. **Serif or Sans-Serif body text?** IEEE uses serif (Times). Modern/minimal leans sans (Liberation Sans). This is a visual preference call.

2. **First page treatment?** Options: (a) content starts immediately with title at top, (b) separate cover/title page, (c) title block at top of first page with extra spacing. Option (c) is probably the MVP sweet spot.

3. **Section numbering style?** IEEE uses roman numerals for top-level (I, II, III) and letters for subsections (A, B, C). Do we keep this or switch to Arabic (1, 1.1, 1.2)? Numbering could also be left to content rather than template.

4. **Text alignment?** IEEE uses justified. Justified looks more polished but can create awkward spacing without hyphenation. Left-aligned (ragged right) is safer for AI-generated content of variable length. ReportLab does support hyphenation via the `pyphen` library but that's another dependency to verify.

5. **Header/footer content?** Minimal recommendation: document title in header (left-aligned), page number in footer (centered). Skip these on the first page.

6. **Target line length?** This determines margins. For 11pt Liberation Serif on US Letter, ~1.25" left/right margins give roughly 65 characters per line - the readability sweet spot.

---

## 5. Relevant Resources

### ReportLab Documentation
- ReportLab User Guide (Platypus chapter): https://docs.reportlab.com/reportlab/userguide/ch5_platypus/
- ReportLab Paragraph XML Markup: https://docs.reportlab.com/reportlab/userguide/ch6_paragraphs/
- ReportLab Tables: https://docs.reportlab.com/reportlab/userguide/ch7_tables/
- ReportLab API Reference: https://docs.reportlab.com/reportlab/userguide/

### Claude Environment Resources
- PDF Skill (main): `/mnt/skills/public/pdf/SKILL.md`
- PDF Skill (advanced reference): `/mnt/skills/public/pdf/REFERENCE.md`
- PDF Skill (forms): `/mnt/skills/public/pdf/FORMS.md`

### Font Files (verified present)
- Liberation Sans: `/usr/share/fonts/truetype/liberation/LiberationSans-*.ttf`
- Liberation Serif: `/usr/share/fonts/truetype/liberation/LiberationSerif-*.ttf`
- Liberation Mono: `/usr/share/fonts/truetype/liberation/LiberationMono-*.ttf`
- DejaVu Sans: `/usr/share/fonts/truetype/dejavu/DejaVuSans*.ttf`
- DejaVu Serif: `/usr/share/fonts/truetype/dejavu/DejaVuSerif*.ttf`
- DejaVu Sans Mono: `/usr/share/fonts/truetype/dejavu/DejaVuSansMono*.ttf`

### IEEE Source Documents (uploaded)
- IEEE Editorial Style Manual: writing conventions, section structure, heading rules
- IEEE Reference Style Guide: citation formatting patterns

### Previous Research
- Style guidelines report from this conversation (comprehensive typography/layout research with sources from Butterick's Practical Typography, Material Design, USWDS, and others)

---

## 6. Recommendation

Build this as a Praxisity `deliver` command task using the full design workflow. The template file itself is ~300 lines of Python, but getting the proportions right requires visual iteration. The design spec should lock down the six decisions in Section 4, then implementation can proceed mechanically.

The deliverable is one file: `praxisity_style.py`. It imports into any PDF generation script, provides pre-configured styles and a document builder, and produces visually consistent output without the generating Claude instance needing to know anything about typography.
