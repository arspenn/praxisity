## Agent Report

**Agent:** critic
**Artifact:** SPEC-004
**Date:** 2026-04-01
**Dispatch Mode:** Mode 2: parallel

## Instructions Received

Review SPEC-004 for weaknesses, contradictions, unstated assumptions, gaps between problem statement and proposed solution, and scope creep risks. Assess whether requirements are well-defined enough to design against and whether acceptance criteria validate the requirements.

## Findings

### [Critical] REQ-F1 contradicts REQ-N1

REQ-F1 requires switching from "Read template, fill, Write" to "cp then Edit" — but this means rewriting every command's entire Generate section. REQ-N1 says "each command fix shall be a targeted edit — no unrelated refactoring." These cannot both hold for the Generate section changes. Commands affected: `/spec`, `/charter`, `/architect`, `/define`.

**Fix:** Acknowledge Generate sections as an explicit exception to REQ-N1, or redefine "targeted" to mean "limited to sections that need to change for the bug fix."

### [Critical] REQ-F3 "one section at a time" is underspecified

The bug report itself hedges on strict enforcement — BUG-018 acknowledges the agent's instinct to move quickly was responsive to context, and floats a "fast mode" concept SPEC-004 does not incorporate. A rigid rule will make commands feel slow for experienced users.

**Fix:** Split REQ-F3 into pause-between-sections (MUST) and no-bulk-draft (SHOULD), or add an exception clause allowing draft-then-approve when context is rich.

### [Important] 27 of 46 bugs have no requirement to design against

Requirements map to ~19 bugs through five pattern classes. The remaining 27 are covered only by OBJ-3 ("low-effort targeted edit") and OBJ-4 ("document deferred bugs"), but no requirements specify which bugs fall where. The triage decisions will happen during design, blurring the specify/design boundary.

**Fix:** Add a disposition table classifying each bug as addressed by REQ-F1–F8, targeted command edit, or deferred with rationale.

### [Important] No acceptance criteria for REQ-F6, REQ-F7, REQ-F8

8 functional requirements but only 6 acceptance criteria. REQ-F6 (Todoist), REQ-F7 (template anchoring in CLAUDE.md), and REQ-F8 (template anchoring in command specs) have no corresponding ACs.

### [Important] REQ-F1 does not account for section deletion and comment stripping

Current commands describe transformations beyond placeholder substitution: "Remove HTML comments and empty placeholders." Using Edit to remove 15-20 HTML comment blocks is mechanically awkward. The spec should acknowledge that "placeholder substitution" includes section removal and comment stripping.

### [Minor] AC-1 tests a necessary but insufficient condition

The template source being unchanged is trivially true whenever `cp` is used. The interesting validation is whether the output file preserves template structure for non-edited sections.

### [Minor] Q-2 is marked Open but REQ-N2 already answers it

REQ-N2 commits to the bug report fix tracking table as the disposition record. Q-2 can be resolved.

## Strengths

1. Pattern extraction is well-supported by evidence — each requirement cites specific bug IDs
2. Scope boundaries are clear and disciplined (Section 8)
3. REQ-F6 (Todoist coupling guard) is a smart defensive requirement
4. Honest about unknowns (Q-1, Q-2)

## Self-Evaluation

- **What worked well:** Reading every command file alongside the bug report exposed the REQ-F1/REQ-N1 contradiction and template transformation complexity
- **What you struggled with:** Calibrating severity on REQ-F3 — the bug report is ambivalent about strict enforcement
- **Prompt improvement suggestions:** Guidance on handling Draft-status specs — distinguishing "not yet done" from "wrong"
