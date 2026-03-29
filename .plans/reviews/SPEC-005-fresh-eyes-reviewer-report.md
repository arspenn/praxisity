# Cross-Document Consistency Review

**Documents reviewed:**
- `/home/arspenn/Dev/praxisity/.plans/specs/005-agent-consultation-system.md` (SPEC-005)
- `/home/arspenn/Dev/praxisity/.plans/designs/004-agent-consultation-system.md` (DESIGN-004)

**Reviewer:** Fresh Eyes Reviewer (cold read, no conversation context)
**Date:** 2026-03-28

**Status:** Issues Found

---

## Issues

### 1. DESIGN-004: Section 1.1 — Deliverable count says "8 agent definition prompts" but also lists additional file types without a clear total

DESIGN-004 Section 1.1 states: "The entire deliverable is authored files: 8 agent definition prompts, 1 skill document, 1 collaborative mode extension, 1 flexible report template, 1 context block template, a directory structure, and minor edits to 3 existing command files."

That is 8 + 1 + 1 + 1 + 1 = 12 authored files plus directory creation and 3 command edits. This is internally consistent within the design. However, SPEC-005 never enumerates a context block template or collaborative mode extension as distinct deliverables -- those concepts are implicit in the requirements (REQ-F2, REQ-F11) but not called out as discrete artifacts. An implementer reading only the spec would not know a `collab-mode.md` file or a context block template file is expected.

**Why it matters:** An implementer working from the spec's acceptance criteria would build agent files and a skill but might not create the `collab-mode.md` or context block template as standalone files, since the spec does not list them as deliverables or reference them by filename.

### 2. SPEC-005: REQ-F4 says "8 agents across 4 categories" -- DESIGN-004 COMP-2 says collab-mode avoids "7x duplication"

DESIGN-004 COMP-2 states: "Collab-mode.md is a single shared file, not per-agent -- avoids 7x duplication." With 8 agents, the avoided duplication would be 8x (or 7 additional copies beyond the first), not 7x. This is a minor arithmetic ambiguity -- "7x" could be read as "7 extra copies" (which would be correct for 8 agents) or as "7 total copies" (which would correspond to 7 agents). The phrasing is imprecise but not necessarily wrong.

**Why it matters:** Low impact. The meaning is clear enough in context, but it introduces a moment of uncertainty about whether the author was counting 7 or 8 agents.

### 3. SPEC-005: REQ-F1 specifies "standard fields (name, description, tools, model, memory)" -- DESIGN-004 DATA-1 marks tools, model, and memory as "No" (not required)

SPEC-005 REQ-F1 says agent files must have "standard fields (name, description, tools, model, memory) plus custom `category` field." This reads as all five being required fields. DESIGN-004 DATA-1 marks `tools`, `model`, and `memory` as Required: "No" in the schema table, with only `name` and `description` as required.

The spec's wording ("with standard fields X, Y, Z") does not explicitly say "all required," but a cold reader would reasonably interpret listing them together as meaning they are all part of the standard definition. The design then softens this, making three of them optional.

**Why it matters:** An implementer reading the spec alone would likely include all five fields in every agent file. An implementer reading the design would omit `tools`, `model`, and `memory` for some agents. The spec should either mark which fields are optional or the design should explain why it diverges.

### 4. SPEC-005: REQ-F3 lists five things the skill shall provide -- DESIGN-004 COMP-3 responsibilities list does not include "what to preserve from sessions"

SPEC-005 REQ-F3 says the skill shall provide guidance on: "(1) available agents, (2) when to use single consult vs. team session, (3) how to manage parallel agent sessions, (4) how to synthesize feedback, and (5) what to preserve from sessions."

DESIGN-004 COMP-3 Responsibilities lists: agent index, decision gate, Mode 2 guidance, Mode 3 guidance, output preservation, and naming/description differentiation. Items (1)-(3) map cleanly. Item (4) -- synthesis -- appears under Mode 2 guidance ("how to synthesize their independent returns") but is not called out as a separate responsibility. Item (5) -- "what to preserve" -- maps to "output preservation" but with a subtle shift: the spec says "what to preserve from sessions" (broader, could include team composition, open threads, unresolved disagreements) while the design narrows this to "how and when to save session reports."

**Why it matters:** The spec's "what to preserve" is broader than report writing. If the skill only covers report-saving, it may miss guidance on preserving team composition notes, unresolved questions, or open threads -- things REQ-N4 explicitly requires for team reconstitution.

### 5. SPEC-005: REQ-F11 says "three dispatch modes" with Mode 1 described as "single expert consult (Mode 1, one subagent via Agent tool)" -- DESIGN-004 COMP-3 says Mode 1 is "handled inline by COMP-4"

SPEC-005 REQ-F11 requires the consult-team skill to "support three dispatch modes" including Mode 1. DESIGN-004 COMP-3 explicitly states its purpose covers "Mode 2 (parallel perspectives) and Mode 3 (collaborative team)" and that "Mode 1 (single consult) is handled inline by COMP-4."

This means the skill does NOT support all three modes as REQ-F11 requires. Mode 1 guidance lives in the command pointers (COMP-4), not in the skill (COMP-3). The design's Requirements Coverage table (Section 1.3) maps REQ-F11 to "COMP-3, DEC-1" -- but COMP-3 explicitly excludes Mode 1.

**Why it matters:** If an implementer tests AC-10 ("Given the consult-team skill, when loaded, then it provides guidance for all three dispatch modes: Mode 1..."), the skill will fail that acceptance criterion because Mode 1 is not in the skill by design. Either the spec's AC-10 needs to be revised to reflect that Mode 1 is in the command pointers, or the design needs to include at least a reference to Mode 1 within the skill.

### 6. SPEC-005: AC-9 validates REQ-F10 but there is no AC for REQ-F9

SPEC-005 has acceptance criteria AC-1 through AC-11, validating REQ-F1 through REQ-F12. The mapping skips REQ-F9 (persistent memory via `memory: project`). There is no acceptance criterion that validates the persistent memory feature.

AC mapping as written:
- AC-1 -> REQ-F1
- AC-2 -> REQ-F2
- AC-3 -> REQ-F3
- AC-4 -> REQ-F4
- AC-5 -> REQ-F5
- AC-6 -> REQ-F6
- AC-7 -> REQ-F7
- AC-8 -> REQ-F8
- AC-9 -> REQ-F10 (skips REQ-F9)
- AC-10 -> REQ-F11
- AC-11 -> REQ-F12

**Why it matters:** REQ-F9 (memory: project, `.claude/agent-memory/<name>/`) has no acceptance criterion. An implementer has no way to verify this requirement is met. Given REQ-F9 is marked COULD priority this may be intentional, but it is not stated.

### 7. SPEC-005: REQ-F1 specifies agent file location as `.claude/agents/` -- DESIGN-004 also references `.claude/skills/consult-team/templates/` for templates

DESIGN-004 Section 7.1 (Implementation Order, step 1) says to create `.claude/skills/consult-team/templates/` for templates. SPEC-005 does not mention this directory path anywhere. The spec references `.plans/reviews/` for outputs and `.claude/agents/` for agent files, but the template storage location is a design-only decision.

Additionally, DESIGN-004 COMP-2 describes the context block template and collab-mode.md but does not specify their exact file paths. The implementation order mentions `.claude/skills/consult-team/templates/` but it is unclear whether collab-mode.md lives there or in `.claude/agents/` alongside the agent files.

**Why it matters:** An implementer would need to decide where `collab-mode.md`, the context block template, and the session report template live. The design introduces a directory path in the implementation order but does not explicitly assign files to it in the component descriptions.

### 8. SPEC-005: Out of Scope says "Agents modifying project files" with an exception for reports -- DESIGN-004 DEC-4 gives agents broader capabilities

SPEC-005 Section 8 states: "Agents modifying project files -- agents return analysis and recommendations for project artifacts; the main agent or user acts on them. All dispatched agents (every mode) write their own reports to `.plans/reviews/`, but do not modify other project files."

DESIGN-004 COMP-1 gives review-focused agents `tools: Read, Grep, Glob, Write` and notes "Write for `.plans/reviews/` reports only." However, "action-oriented agents (Designer, Project Manager) may need broader tool access." If Designer or Project Manager agents have unrestricted Write access, they could technically modify project files, which the spec explicitly places out of scope.

**Why it matters:** The design opens the door for action-oriented agents to have broader write access than the spec allows. Either the spec's out-of-scope should note that some agents may have broader tool access (restricted by their persona instructions rather than tool restrictions), or the design should restrict all agents' write access to `.plans/reviews/`.

---

## Recommendations (advisory, do not block approval)

1. **Clarify template file locations in the design.** COMP-2 describes three template/extension files but never assigns them to specific paths. The implementation order mentions `.claude/skills/consult-team/templates/` but the connection to specific files is implicit. Adding a "File Locations" row to each DATA section would eliminate ambiguity.

2. **Consider adding a brief note to the spec about the collab-mode.md deliverable.** The spec's requirements imply the need for a collaborative mode extension (REQ-F11, REQ-F12) but do not name it as a file. Since the spec drives acceptance criteria, and AC-11 tests Mode 3 behavior, the connection between the deliverable and the requirement should be traceable.

3. **The design's Appendix A Glossary is useful and well-structured.** The spec would benefit from defining "snapshot" and "delta" since it uses the concepts (implicitly in the mode descriptions) without naming them.

4. **The design references Claude Code v2.1.32+ as a prerequisite for agent teams (Section 2.3 Note).** The spec does not mention any version requirement. If this is a hard dependency, it should appear in the spec's Dependencies table (Section 7.1).

---

## Self-Evaluation

**What types of inconsistencies I found most frequently:** Scope and coverage mismatches -- where one document defines a boundary (spec's out-of-scope, acceptance criteria) and the other document either exceeds that boundary or leaves it uncovered. The Mode 1 / AC-10 issue (Issue 5) and the missing AC for REQ-F9 (Issue 6) are the most implementation-impactful findings.

**What I felt unable to assess:**
- Technical feasibility of the Claude Code Agent tool and TeamCreate mechanisms. I took the documents' claims about platform capabilities at face value.
- Whether the 8 agent personas will actually produce differentiated, useful feedback. This is a quality question that only bootstrapping testing can answer.
- Whether the `.claude/agent-memory/<name>/` path convention is correct for Claude Code's `memory: project` feature. I flagged the missing acceptance criterion but cannot verify the technical claim.

**Whether the documents were structured in a way that made cross-referencing easy or difficult:** Mostly easy. Both documents use consistent ID schemes (REQ-F1, COMP-1, DATA-1, etc.) and the design's Requirements Coverage table (Section 1.3) made it straightforward to check that every requirement had a design mapping. The spec's acceptance criteria table with explicit "Validates" column was particularly useful. The main difficulty was tracing template files to specific locations -- the design describes them conceptually in COMP-2 and DATA-2/DATA-3 but defers path decisions to the implementation order, creating a gap between "what the file is" and "where it lives."

**Suggestions for how my prompt could be improved for this kind of review:**
- Providing the reviewer with the actual Claude Code subagent documentation (or a summary) would enable verification of technical claims about platform capabilities, frontmatter fields, and tool restrictions.
- A checklist-style requirement for "verify every acceptance criterion is testable as written" would have surfaced the AC-10 / Mode 1 issue faster.
- Asking the reviewer to produce a coverage matrix (every requirement mapped to design component AND acceptance criterion) as a structured artifact would make gaps like the missing REQ-F9 AC mechanically detectable rather than requiring manual cross-referencing.