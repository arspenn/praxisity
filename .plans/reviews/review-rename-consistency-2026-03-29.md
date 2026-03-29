## Cross-Document Consistency Review: consistency-reviewer Rename

**Documents reviewed:**
- `/home/arspenn/Dev/praxisity/.claude/agents/consistency-reviewer.md`
- `/home/arspenn/Dev/praxisity/.plans/specs/005-agent-consultation-system.md`
- `/home/arspenn/Dev/praxisity/.plans/designs/004-agent-consultation-system.md`
- `/home/arspenn/Dev/praxisity/.plans/prompts/004-templates-and-extensions.md`
- `/home/arspenn/Dev/praxisity/.plans/prompts/005-agent-definition-files.md`
- `/home/arspenn/Dev/praxisity/.plans/prompts/006-consult-team-skill.md`
- `/home/arspenn/Dev/praxisity/.plans/references/d4c-praxisity-bug-report.md`

**Status:** Approved

---

## Remaining "fresh-eyes" References

**In the 7 specified files:** None found. Clean.

**In the broader repo** (for context, not blocking): The following files contain "fresh-eyes" but are explicitly outside rename scope:
- `.claude/agents/fresh-eyes-reviewer-generated.md` — historical artifact from `/agents` command testing, not an active agent
- `.claude/agents/fresh-eyes-reviewer-old.md` — backup of the original file before rename
- `.plans/reviews/` — multiple historical reports written under the old name, correctly left as-is per instructions

---

## Agent Roster Count — All Locations

The count of 8 agents is consistent everywhere it appears:

| Location | Count | List includes consistency-reviewer? |
|---|---|---|
| SPEC-005 REQ-F4 | 8 | Yes |
| SPEC-005 AC-4 (explicit filename list) | 8 | Yes — `consistency-reviewer.md` |
| DESIGN-004 COMP-1 Key Design Decisions (file list) | 8 | Yes — `consistency-reviewer.md` |
| DESIGN-004 Agent Roster table | 8 | Yes — "Consistency Reviewer \| Meta" |
| DESIGN-004 Section 7.4 | 8th agent named | "The Consistency Reviewer (8th agent, added during design)" |
| DIP-005 Must Satisfy REQ-F4 | 8 | Yes — `consistency-reviewer` |
| DIP-005 Files in Scope list | 8 | Yes — `consistency-reviewer.md (verify only, already exists)` |
| DIP-005 Verification Commands grep | 8 names | Yes — `consistency-reviewer` |
| DIP-006 Step 1 index | 8 | "Meta: Prompt Engineer, Consistency Reviewer" |
| DIP-006 Verification Commands grep | 8 names | Yes — `consistency-reviewer` |

No location shows 7 or lists the old filename. Roster count is consistent throughout.

---

## consistency-reviewer.md Identity Assessment

**Name field:** `consistency-reviewer` — correct, matches new name.

**Description:** "Cross-document consistency reviewer. Catches contradictions, mismatches, and stale references across specs, designs, and DIPs. Use after writing or revising any planning artifact, or as a persistent teammate during sustained work."

This is broader than the old "cold read only" framing and accurately reflects the dual capability — one-shot cold read (Mode 1/2) and persistent teammate (Mode 3). The description is coherent with the new name and the DESIGN-004 Section 7.4 description: "When dispatched as a one-shot subagent it reads cold — the way a future implementer will. When running as a persistent teammate it leverages accumulated session context to catch regressions as work evolves."

**Identity section:** Explicitly covers both modes: "When dispatched as a one-shot reviewer, you read documents without the author's conversation context... When running as a persistent teammate, you leverage your accumulated session context to catch regressions as the work evolves." This is a clean expansion that preserves the original cold-read capability while adding persistent-teammate framing. The identity is coherent after the rename and refocusing.

**Self-Evaluation sub-bullets in Output Format:** The agent file retains the reviewer-specific sub-bullets ("Most frequent inconsistency types," "Unable to assess," "Document structure quality"). This is correct — these are the right reflection prompts for this specific agent's domain. The session-report.md fix (generic template) and the agent file's own Output Format (domain-specific) are now properly differentiated. No conflict.

---

## Internal Consistency Check

All cross-references from the DIPs back to the agent are consistent with the new name:

- DIP-004 Step 1 note: "from consistency-reviewer work" — consistent
- DIP-004 Step 4 Verify note: "would make sense appended to any of the 8 agent definitions" — no name-specific reference, fine
- DIP-005 Objective: "consistency-reviewer.md already exists and serves as the reference implementation" — consistent
- DIP-005 Step 1 verification note: "what makes consistency-reviewer effective" — consistent
- DIP-005 Step 5 Verify note: "distinct from Consistency Reviewer — Prompt Engineer evaluates prompt quality, Consistency Reviewer checks cross-document consistency" — consistent and accurately characterizes the distinction
- DIP-005 Notes section: "the consistency-reviewer is the right density" — consistent
- DIP-006 Step 1 index listing: "Meta: Prompt Engineer, Consistency Reviewer" — consistent

The design's Section 7.4 heading and body text both use "Consistency Reviewer" — the section title was updated as part of the rename, and the body now accurately describes the expanded dual-mode capability rather than just the original cold-read framing.

---

## Old vs. New Agent Comparison

**Files compared:**
- Old: `/home/arspenn/Dev/praxisity/.claude/agents/fresh-eyes-reviewer-old.md`
- New: `/home/arspenn/Dev/praxisity/.claude/agents/consistency-reviewer.md`

### Structure

| Section | Old | New |
|---------|-----|-----|
| Identity | Present | Present |
| Project Context | Absent | Added |
| Reasoning Approach | Present | Present (expanded) |
| Critical Rules | Absent | Added (5 rules) |
| Output Format | Present | Present (expanded) |
| Self-Evaluation | Present | Present (reformatted) |

The new file adds two sections (Project Context, Critical Rules) that are part of the standard agent template pattern. Both additions strengthen the file as a standalone dispatch target — an agent reading it cold now has Praxisity workflow context and explicit rules that prevent specific failure modes (inventing issues, vague citations, assuming unstated things are true).

---

### Description Field

**Old:** "Reads specs, designs, and DIPs cold — without conversation context — to catch contradictions, mismatches, and stale references that authors miss. Use after writing or revising any planning artifact."

**New:** "Cross-document consistency reviewer. Catches contradictions, mismatches, and stale references across specs, designs, and DIPs. Use after writing or revising any planning artifact, or as a persistent teammate during sustained work."

The new description correctly expands the use case to include Mode 3 (persistent teammate). The cold-read framing is removed from the description but preserved in the Identity section. Net change: broader dispatch applicability described, same core function retained.

---

### Identity

**Old:** Framed entirely around the cold-read advantage:
> "You are a consistency reviewer who reads documents cold. You have no knowledge of the conversations that produced these documents... This is your advantage. Authors carry conversation context that makes resolved decisions feel written down when they aren't. You catch the gap between what was decided and what was recorded."

**New:** Dual-mode framing:
> "When dispatched as a one-shot reviewer, you read documents without the author's conversation context — catching gaps between what was decided and what was recorded. When running as a persistent teammate, you leverage your accumulated session context to catch regressions as the work evolves."

**What was gained:** The new version is operationally complete — it tells the agent how to behave in both dispatch modes without ambiguity.

**What was lost:** The old version's "This is your advantage" framing was motivationally sharp. It told the agent *why* the cold-read works, not just *that* it should do it. This reasoning — authors carry conversation context that makes resolved decisions *feel* written down when they aren't — is the core insight behind the whole agent concept. The new version describes the behavior but drops the underlying model. For a one-shot dispatch (Mode 1/2), the motivational framing had real value as calibration: it tells the agent to resist filling gaps with "obvious" inferences.

**Assessment:** The loss is minor but real. The new version is functionally correct; the old version's framing was a better AI prompt for the cold-read case because it preempted the most common failure mode (assuming something is true because it makes sense).

---

### Reasoning Approach

**Old:** 5-step numbered list, then separate "What you look for" and "What you ignore" bullet lists. Plain-English descriptions of what to look for.

**New:** 4-step numbered list with "What you look for" items embedded in step 2 as sub-bullets. "What you ignore" list at the end. Adds the Project Context section with Praxisity-specific ID format conventions (REQ-F/N, COMP-N, INT-N, DATA-N, DEC-N). Adds one new item: "Version and decision references: check they point to current state, not stale revisions."

**Net changes:**
- The Project Context section making ID formats explicit is a meaningful improvement — it gives the agent the specific vocabulary it needs to do the cross-reference work without having to infer naming conventions from examples
- The embedded sub-bullet structure in step 2 is slightly harder to scan than the separate "What you look for" block in the old version; the old separation was cleaner visually
- The additional "Version and decision references" check item is a genuine improvement — it was absent from the old version and caught real issues in the SPEC-005 reviews (stale DEC references)

---

### Output Format

**Old:** Issue format: `- [Document]: [Section] — [specific inconsistency] — [why it matters for implementation]`

**New:** Same core issue format, plus:
- Explicit "Recommendations (advisory, do not block approval)" block added as a named section
- Instruction to update agent memory added at the end of the template

Both additions improve the format. The recommendations block was present in practice (prior reviews used it) but not in the old template — the new version makes it explicit and clarifies its advisory-only status. The memory update instruction implements REQ-F9 (persistent knowledge accumulation) within the agent's output instructions.

---

### Self-Evaluation

**Old:** 4 plain-prose prompts embedded in a sentence ("After completing your review, write your report... and include a self-evaluation section at the end: [bullet list]").

**New:** Same 4 prompts reformatted as labeled sub-bullets with descriptive headers ("Most frequent inconsistency types," "Unable to assess," "Document structure quality," "Prompt improvement suggestions"). The "Prompt improvement suggestions" item adds specificity: "what instructions were unclear, what capabilities were missing, what would help you do this review better next time."

**Assessment:** The new format is unambiguously better. The labeled sub-bullets produce more structured output and are easier to compare across sessions. The added specificity in the last bullet increases the quality of self-evaluation data.

---

### Summary Assessment

The new file is a net improvement. The Project Context section, Critical Rules, expanded output format, and reformatted self-evaluation all add genuine value. The dual-mode framing in Identity is operationally correct and necessary for Mode 3 use.

The one meaningful regression: the old Identity section's "This is your advantage" motivational framing was a stronger AI prompt for cold-read dispatches. It preempted the failure mode of gap-filling by inference. The new version describes the dual-mode behavior accurately but doesn't explain *why* the cold-read works the way it does — the model behind the behavior. This is worth noting but does not affect the rename or consistency verdict.

---

## Self-Evaluation

**Most frequent inconsistency types:** None found. This was a clean rename with no stragglers in the specified files.

**Unable to assess:** Whether any other files outside the 7 specified (e.g., PLANNING.md, command files, README) reference "fresh-eyes" in a way that should have been updated. Only the 7 specified files were in scope for this review.

**Document structure quality:** Straightforward. The rename touched the agent name in a limited, traceable set of locations, and all were updated consistently.

**Prompt improvement suggestions:** No changes needed.