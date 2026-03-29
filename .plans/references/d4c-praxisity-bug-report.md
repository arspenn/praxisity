# D4C-ARS Praxisity Framework Bug Report

**Date:** 2026-03-27
**Tested on:** Praxisity framework (version inherited from project initialization)
**Test project:** D4C-ARS (public-health, Theory of Change for flu vaccination)
**Reference:** See `/home/arspenn/Dev/praxisity/.plans/references/new-project-bug-report.md` for prior bug report

---

## Confirmed Bugs from Prior Report

### BUG-038: RESOLVED -- /deliver now handles numbered lists

The md_to_pdf.py shared module built during this project handles numbered lists correctly. Lines matching `^\d+\.\s+` render with `styles["BulletItem"]` and the number as bulletText. This was fixed as part of the refactoring of /deliver into a reusable module.

### BUG-046: RESOLVED -- /deliver now handles `---` horizontal rules

The md_to_pdf.py parser detects `---` and renders a `Spacer(1, 12)`. No longer falls through to body text.

### BUG-039: PARTIALLY RESOLVED -- /deliver generation scripts

The refactoring into `scripts/md_to_pdf.py` means /deliver no longer needs to generate per-document scripts. However, the original per-document script (`scripts/generate_logic_constructs_pdf.py`) was kept as a thin wrapper for backward compatibility. The command spec still describes per-document script generation, which should be updated.

### BUG-009 pattern: NOT OBSERVED in /build

The /build command read DIPs as instructions and executed them without template copy issues. The DIP template was used correctly during /define (the DIPs were written from scratch via Write, not copied from template and edited, which is the BUG-009 pattern). However, the DIP content was generated from design/spec context, not from the template structure, so the impact was minimal -- the DIPs were structurally faithful to the template.

### BUG-017 pattern: IMPROVED but still present

PLANNING.md was generally updated at the start of commands (e.g., `/build` set the active command before executing steps). However, the update was sometimes the second or third action rather than strictly the first. The pattern is improved compared to the prior report but not fully fixed.

---

## New Bugs Found in D4C-ARS

### BUG-047: /deliver command spec does not reflect shared module architecture

**Severity:** Medium
**Status:** Open (command-level update needed)
**Affects:** /deliver

The /deliver command spec says to "Write and execute a Python script that imports from praxisity_style" for each document. During this project, we refactored this into a shared module (`scripts/md_to_pdf.py`) that handles all deliverables through a CLI:

```bash
python3 scripts/md_to_pdf.py deliverables/any-document.md
```

The shared module approach is superior: consistent output across documents, no per-document scripts to maintain, and features (DOI links, citation hyperlinks, tables, lists) developed once and applied everywhere.

**Fix needed in command:** Update the /deliver command spec to:
1. Check for an existing `md_to_pdf.py` (or equivalent) shared module in the project
2. If present, use it rather than generating a new script
3. If absent, generate the shared module on first /deliver invocation, not a per-document script
4. The module should be the persistent artifact, not individual scripts

---

### BUG-048: /deliver command spec does not address URL escaping in PDF generation

**Severity:** High
**Status:** Open (command-level fix needed)
**Affects:** /deliver

ReportLab's Paragraph markup uses XML, so text must be entity-escaped (&, <, >). If URLs are processed after XML escaping, a regex character class like `[^\s,;&lt;)]+` silently excludes common URL characters (`l`, `t`) because `&lt;` is parsed as individual characters inside a regex class. This truncates every URL after its first `l` or `t`.

**What happened:** All DOI and website URLs in generated PDFs were truncated to a few characters. The fix is to extract URLs from raw text BEFORE XML escaping, then escape the non-URL text segments separately.

**Fix needed in command:** The /deliver spec's Generation section should include a behavioral note: "When generating ReportLab Paragraph content, extract URLs from raw text before XML escaping. Do not run URL regexes on already-escaped text." The shared md_to_pdf.py module implements this correctly via `_linkify_urls()`.

---

### BUG-049: /deliver command spec does not mention internal citation hyperlinks

**Severity:** Low
**Status:** Open (command-level enhancement)
**Affects:** /deliver

Documents with numbered references ([1], [2]...) benefit from internal hyperlinks where in-text citations jump to the corresponding reference entry. ReportLab supports this via `<a name="refN"/>` anchors and `<a href="#refN">` links. The /deliver command spec does not mention this capability.

**What we built:** The md_to_pdf.py module automatically detects [N] citations in body text, creates anchor bookmarks at reference entries, and links them. It also applies a distinct color to all hyperlinks (internal and external).

**Fix needed in command:** Add citation hyperlinking as a feature in the /deliver spec's Generation section. Note the ReportLab constraint: `<a name="..."/>` must be self-closing with no content.

---

### ISSUE-004: No framework pattern for persistent agent teams across DIPs

**Severity:** Medium
**Status:** Open (framework-level enhancement)
**Affects:** /build, /define

The D4C-ARS audit used a three-member review team (Evidence Auditor, Claim Reviewer, Construct Analyst) that was opened during DIP-006 and persisted through DIP-007 and into the executive summary writing. The team built context during the master table audit that made their formal review of downstream corrections much more effective than a cold read.

The /build command spec has no concept of "team persists across builds." The /define command has no way to specify that a DIP should inherit an existing team. The team lifecycle (open, persist, debrief, close) was managed ad hoc through DIP notes ("Do NOT shut down the agent team").

**Fix needed in framework:** Consider a team lifecycle pattern for multi-DIP workflows:
1. DIP that opens a team specifies the team purpose and membership
2. Subsequent DIPs that inherit the team reference it by name
3. Team closure is explicit and user-initiated, not automatic at DIP completion
4. The /build command recognizes "team is running" state and routes review tasks to existing team members

---

### ISSUE-005: /deliver spec assumes static document content

**Severity:** Low
**Status:** Open (command-level enhancement)
**Affects:** /deliver

The /deliver spec treats PDF generation as a one-time conversion. In practice, documents are iteratively corrected (as during the citation audit) and regenerated multiple times. The shared module approach (`md_to_pdf.py`) handles this naturally, but the command spec describes a single-run workflow.

**Fix needed in command:** Acknowledge that /deliver may be run repeatedly on the same document. The generation step should check for and overwrite existing PDFs without prompting (since the source markdown is the authoritative version).

---

## Positive Findings

### /build handled non-software DIPs well

DIP-006 (master table citation audit) and DIP-007 (downstream correction) were research/audit tasks, not software implementation. The /build command's step-by-step verification model worked effectively for this domain: each step had clear inputs, outputs, and verification criteria. The scope boundaries (DO/DO NOT) were particularly valuable for preventing scope creep between the two DIPs.

### /define produced good audit DIPs

The DIP template's structure (objective, required reading, implementation steps, scope boundaries, acceptance criteria, commit instructions) transferred well from software to research. The "Files in Scope / Files Out of Scope" sections were especially useful for audit work where different DIPs operate on different subsets of the deliverables.

### The spec/architect/define/build pipeline scales to analytical work

The full Praxisity pipeline (SPEC-009 -> DESIGN-005 -> DIP-006 + DIP-007) worked for a citation audit, which is far from the software development use case the framework was designed for. The pipeline's value was in forcing clear scoping (what is in the audit, what is not), dependency mapping (master table before downstream documents), and explicit acceptance criteria (verifiable conditions for "audit complete").

---

### ISSUE-006: DIP template duplicates requirement satisfaction in two locations

**Severity:** Low
**Status:** Open (template-level fix needed)
**Affects:** `/define`, DIP template

The DIP template lists which requirements a DIP satisfies in two places: the Must Satisfy table (Section: Technical Requirements) and the Commit Instructions `Satisfies:` line. During SPEC-005 work, fixing one without updating the other caused a sync issue caught by the fresh-eyes-reviewer. This happened twice in one session.

**Fix needed in template:** Collapse requirement satisfaction into a single authoritative location (the Must Satisfy table) and have the commit message template reference it rather than duplicating the list. E.g., the commit template could say `Satisfies: [see Must Satisfy table]` or auto-generate from the table.

---

## Fix Tracking (D4C-ARS Bugs Only)

| Bug | Artifact Fixed | Command Updated |
|-----|---------------|-----------------|
| BUG-038 | Yes (md_to_pdf.py) | No |
| BUG-046 | Yes (md_to_pdf.py) | No |
| BUG-039 | Partial (shared module approach) | No |
| BUG-047 | N/A (new) | No |
| BUG-048 | Yes (md_to_pdf.py) | No |
| BUG-049 | Yes (md_to_pdf.py) | No |
| ISSUE-004 | N/A (new) | No |
| ISSUE-005 | N/A (new) | No |
| ISSUE-006 | N/A (new) | No |