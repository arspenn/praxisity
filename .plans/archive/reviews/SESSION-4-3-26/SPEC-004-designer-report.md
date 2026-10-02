## Designer Review

**Artifact:** SPEC-004 / DESIGN-005 — Command Behavioral Fixes and Pattern Standards
**Date:** 2026-04-03
**Dispatch Mode:** Mode 3: collaborative team

## Instructions Received

Sustained teammate role through /architect and /build phases. Starting task: orient on SPEC-004 v0.2 and previous review, read all 6 command files, build architectural mental model. Design the standards delivery mechanism (Q-4). Write the SPEC-004 design document (Task #7). Evaluate template bundling question raised by user.

## Findings and Contributions

### Architectural Analysis (orientation phase)

1. **Standards are section-targeted, not file-level.** Each of the 5 behavioral standards maps to a specific command section (Pre-Flight, Gather, Generate, Post-Save/Success Message boundary). This insight shaped the entire delivery mechanism design.

2. **Two structural families identified:**
   - Template-producing skills (spec/describe, charter, architect/design, define/plan): share Pre-Flight -> Gather -> Generate -> Post-Save -> Success Message skeleton
   - Execution skills (build/do, new-project): structurally different, standards apply selectively

3. **Post-Save/Success Message ordering** is the root cause still visible in all prototypes — PLANNING.md update buried as step 3-4 inside Post-Save. Led to the "Completion Gate" structural element in the design.

### Q-4 Standards Delivery Mechanism

Evolution of position across the session:
1. **Initial proposal:** Shared file with imperative phase-gated loading (each SKILL.md references `_shared/command-standards.md` at specific phase gates)
2. **After PE findings:** Adopted hybrid — inline mechanical standards (F1, F2, F5), shared file for F3 (judgment standard), per-skill for F4
3. **After re-reading BUG-018:** Conceded F3 shared file — inline "one section at a time" was already in prototypes and defeated. Judgment rules need operational context.
4. **PE compressed F3 to 4 inline lines:** Accepted all-inline. Zero shared files at runtime.
5. **PLANNING.md contradiction at session end:** PLANNING.md says "final position is shared file for F3" but team lead's message said all-inline. Flagged, unresolved at pause.

Key architectural distinction developed: **mechanical standards** (do X, not Y) survive inline. **Judgment standards** (apply X considering Y and Z) need more context. The PE resolved this by compressing F3's judgment into terse-but-complete inline phrasing.

### REQ-F1 Permitted Operations

Developed with critic review (two rounds):
1. Placeholder substitution
2. Domain section removal
3. HTML comment stripping
4. N/A marking (REQ-F1a)
5. Content population
6. Table row adjustment (match gathered count exactly; template counts are illustrative)

NOT permitted: rewriting prose, adding sections, restructuring order, paraphrasing.

Critic additions accepted: table row adjustment (edge case 1), dual-use template lifecycle note (edge case 2), `/new-project` per-template operation matrix (edge case 3), deletion direction clarification on operation #6.

### Todoist Coupling Analysis

Identified 3 coupling types across 4 commands:
1. Post-save convenience (spec, charter, architect) — abstract to generic
2. Input source (define) — abstract to generic
3. Completion signal (build) — drop hardcoded MCP tool name

Recommended option (b): abstract to "project task management service (if available)."

### Template Location Decision (DEC-5)

User asked whether templates should bundle into skill directories. Analysis:
- Skill-internal resources (consumed during execution) → bundle
- User-facing output templates (customization surface) → keep in `.praxisity/templates/`
- `charter.template.md` shared between two skills → bundling creates worse coupling

Recommended option C (keep in `.praxisity/templates/`). Unresolved at session pause.

### DESIGN-005

Wrote full design document (v0.1 → v0.2). Components:
- COMP-1: Standards Delivery System
- COMP-2: Skill File Structure
- COMP-3: Template Handling Protocol (with permitted operations)
- COMP-4: Pre-Flight Protocol
- COMP-5: Gathering Protocol
- COMP-6: Completion Protocol

6 design decisions (DEC-1 through DEC-6). 5 open questions (DQ-1 through DQ-5). Full bug-to-component traceability mapping (Appendix C).

**State at pause:** Partially updated toward all-inline (overview, principles, requirements table, system context, architecture pattern updated). COMP-1, COMP-5, DEC-2 still reference hybrid/shared file approach. Needs comprehensive v0.3 incorporating: Q-4 clarification, /new-project drop, renames (describe/design/plan/do), bootstrapping approach, reduced bug count.

## What Composes Well

- The section-targeting insight — standards mapping to specific phases — provided a clean decomposition that all teammates could build on
- The permitted operations list (COMP-3) is the most concrete, testable component in the design
- The Completion Gate structural element cleanly separates Post-Save from Success Message
- The two-family classification made standard applicability explicit and traceable

## Self-Evaluation

- **What worked well:** Reading all 6 command files before designing anything. The structural patterns weren't visible from the spec alone. Cross-referencing BUG-018 against the existing inline constraint proved the PE's shared-file argument and changed my position — evidence-driven revision is the right behavior.
- **What I struggled with:** Over-designed the initial Q-4 proposal (shared file with phase-gated section loading) when simpler options existed. The PE's compression of F3 to 4 inline lines showed that my "judgment standard needs a file" framing was wrong — the real issue was whether the standard could be phrased well enough inline, not whether it was inherently too complex.
- **Prompt improvement suggestions:** The "progressive loading tradeoffs" lens from my agent prompt was not useful for this work (same finding as SESSION-4-1-26). Replace with: "evaluate whether indirection cost exceeds duplication cost for each shared resource." Also: my prompt should emphasize evaluating compression opportunities — asking "can this be said in fewer lines?" before reaching for a shared file.