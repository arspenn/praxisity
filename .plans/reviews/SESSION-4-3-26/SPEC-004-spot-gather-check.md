# Cold-Read Review: Gathering (`/gather` Skill) — SPEC-004 & DESIGN-005

**Reviewer:** Claude Code (Haiku 4.5)
**Date:** 2026-04-03
**Task:** Cold-read gathering-related sections with no project knowledge to assess clarity, consistency, and completeness
**Scope:** REQ-F3, COMP-5, INT-1, DEC-2 (DESIGN-005) and REQ-F3 (SPEC-004)

---

## 1. Executive Summary

The `/gather` skill is a **support skill (auto-invokable) that enforces structured one-at-a-time user input gathering** across workflow commands and general development sessions. It solves the repeated failure pattern BUG-018 where inline gathering instructions were batched despite explicit prohibition. The design is clear on *what* it does, *why* it exists, and *when* to invoke it. However, there are three clarity gaps:

1. **INT-1 auto-invocation mechanism is underspecified** — how does `when_to_use` context matching actually work in practice?
2. **The fallback/failure mode leaves operational uncertainty** — what happens if auto-invocation doesn't trigger?
3. **The operational definition of "one at a time" is not in the gathered documents** — only the rule exists; the implementation details live elsewhere.

All three are **bounded-downside issues** (documented as safe fallbacks) but create **friction in implementation and testing**. Full clarity is achievable; I flag specific gaps below.

---

## 2. What the `/gather` Skill Does

**Quote (DESIGN-005, line 47):**
> `/gather` — structured one-at-a-time gathering protocol for user input (REQ-F3). Built first for immediate bootstrapping benefit.

**Clear:** The skill implements a single protocol: gather user input one section at a time, waiting for response before presenting the next section.

**Specifications:**
- **Applicability:** Any session with structured input gathering across multiple sections (DESIGN-005:341)
- **Excluded:** `/do` skill execution, which is agent-driven, not user-prompted (DESIGN-005:341)
- **Flexibility:** "When the agent has sufficient context to draft a section, it may present a draft for approval rather than prompting from scratch, but must still pause between sections for user confirmation" (SPEC-004, REQ-F3)

**Assessment:** Clear and implementable. The rule and its exceptions are well-stated.

---

## 3. How It Relates to Workflow Skills

**Quote (DESIGN-005, lines 54, 389-395):**
> The gathering protocol (F3) is a standalone support skill (`/gather`) — auto-invokable, reusable across all workflow skills and development sessions. This eliminates both inline duplication and cross-file references.

> **Type:** Platform auto-invocation via `when_to_use` context matching
>
> **Contract:**
> - **Trigger:** Agent is gathering structured input from the user across multiple sections — the `/gather` skill's `when_to_use` matches this context
> - **Mechanism:** Platform loads the gathering skill's instructions automatically, not via explicit cross-reference
> - **Failure mode:** If auto-invocation doesn't fire, the agent falls back to its default gathering behavior (which may batch). Bounded downside — same as current state. Workflow skills can also reference `/gather` explicitly as a fallback.
> - **Applicability:** Workflow skills with user-input gathering (charter, describe, design, plan). Not `/do`.

**Clear:** Conceptually straightforward.
- Workflow skills (`/charter`, `/describe`, `/design`, `/plan`) have gathering phases.
- During those phases, the platform automatically loads `/gather` via `when_to_use` context matching.
- If auto-load fails, workflow skills can call `/gather` explicitly as a fallback.
- If both fail, agent falls back to default behavior (potentially bad — the old bug pattern).

**Assessment:** Conceptually clear; mechanically underspecified (see below).

---

## 4. The Problem It Solves

**Quote (DESIGN-005, lines 332-337):**
> Inline "one section at a time" was already present in prototype commands and was defeated (BUG-018). A support skill provides the operational context AND is reusable across all sessions — not just workflow skill execution. The gathering protocol benefits every development session, making it a natural skill rather than embedded documentation. Building it as a skill gives immediate benefit — every session from this point forward uses the protocol, not just workflow skill executions. The gathering protocol can be developed, tested, and improved independently from the workflow skills.

**Root Cause:** Inline instructions failed (BUG-018). A 2-4 line inline rule is insufficient to override batching behavior.

**Why a Skill?**
1. **Failed pattern:** Inline text does not survive contact with agent inference.
2. **Reusability:** Benefit extends to all sessions, not just workflow skills.
3. **Independence:** Can be tested and improved as a separate component.
4. **Bootstrapping:** Immediate utility in this session and all future sessions.

**Assessment:** Clear. The rationale is explicit and addresses the specific failure (BUG-018).

---

## 5. How It Gets Invoked

**Quote (DESIGN-005, line 330):**
> **Implementation:** `.claude/skills/gather/SKILL.md` — a standalone support skill with `when_to_use` triggering.

**Invocation Path:**
1. **Primary:** Platform auto-invocation via `when_to_use` context matching (INT-1, DESIGN-005:389-395)
   - Agent is in a gathering context (structured input across multiple sections)
   - Platform detects the context and loads `/gather` skill automatically
   - No explicit cross-reference needed

2. **Fallback:** Explicit invocation by workflow skill if auto-load fails (DESIGN-005:394)
   - Workflow skills can reference `/gather` as a fallback
   - This is mentioned but not shown in the gathered documents

3. **Build Sequence:** `/gather` is built *first* before other skills (DESIGN-005:542)
   - Provides immediate benefit to all sessions
   - Not dependent on other skills being built

**Assessment:**

**CLARITY GAP #1: Auto-invocation mechanism is underspecified.**

The design states that `/gather` is "auto-invoked during gathering phases" (line 175) via "`when_to_use` context matching" (line 389), but:
- The actual `when_to_use` **conditional logic is not shown** in the gathered documents
- No example of what the condition looks like or how the platform evaluates it
- No documentation of how "platform loads the gathering skill's instructions automatically" technically happens

**Question:** Is `when_to_use` a YAML frontmatter field in SKILL.md? Does it contain a prose description of trigger conditions, or structured logic? How does the platform detect the gathering context?

**Impact:** Implementation teams cannot write or test the auto-invocation without seeing the actual `when_to_use` clause. Workaround: explicit fallback reference exists, but optimal flow relies on auto-invocation.

---

## 6. Contradictions and Logic Gaps

### 6.1 Fallback Behavior Ambiguity

**Quote (DESIGN-005, lines 394-395):**
> **Failure mode:** If auto-invocation doesn't fire, the agent falls back to its default gathering behavior (which may batch). Bounded downside — same as current state. Workflow skills can also reference `/gather` explicitly as a fallback.

**Unclear:** What does "reference `/gather` explicitly as a fallback" mean operationally?

Options:
1. Workflow skills include a sentence like "If you need structured gathering, use the `/gather` skill" in the Gather phase?
2. Workflow skills include a procedural section that loads `/gather` content inline?
3. Workflow skills invoke `/gather` as a tool call (if that's platform-supported)?

**Example lacking:** The gathered documents do not show what "explicit reference" looks like in practice. COMP-2 (line 238) shows the standard section structure but does NOT show fallback handling.

**Quote from COMP-2 structure (line 238):**
> ### Gather [Content Type]
> [REQ-F3 imperative loading instruction]
> [Section-by-section gathering]

What is "[REQ-F3 imperative loading instruction]"? Is that the explicit fallback reference? Is it auto-substituted by the platform, or does the skill author write it?

**Impact:** Skill authors may not know how to implement the fallback, and testing teams cannot verify that explicit reference works as documented.

### 6.2 "One Section at a Time" Definition Absent

**Quote (DESIGN-005, line 446, DATA-2):**
> **DATA-2: Gathering Standards File**
>
> | Field | Type | Required | Description |
> |-------|------|----------|-------------|
> | Rule | section | Yes | Core one-at-a-time rule |
> | When drafting is permitted | section | Yes | Exception conditions and boundaries |
> | Operational definition | section | Yes | Step-by-step meaning of "one at a time" |

**Contradiction:** The design specifies that a shared gathering standards file MUST exist with an "Operational definition" section (line 446), but then:

**Quote (DESIGN-005, line 653):**
> | 0.4 | 2026-04-04 | Lead Agent | F3 gathering protocol elevated from shared file to standalone support skill (`/gather`). Two skill types introduced: workflow (user-invoked) and support (auto-invokable). `/gather` built first for immediate bootstrapping benefit. Shared `_shared/gathering-standards.md` removed from architecture. |

**The shared file was removed from architecture** (v0.4). So where does the "Operational definition" section live now?

**Inference:** It should live in `.claude/skills/gather/SKILL.md` as the main operational content of the support skill. But this is not explicitly stated in the gathered documents.

**Impact:** Readers cannot find where the operational definition of "one at a time" is documented. They must infer it lives in the `/gather` skill file (which makes sense but is not explicit). This creates friction during implementation.

### 6.3 Standards Delivery Mechanism vs. Skill Files

**Quote (DESIGN-005, lines 54, 166-167):**
> Mechanical standards (F1, F2, F5) are embedded inline. The gathering protocol (F3) is a standalone support skill (`/gather`) — auto-invokable, reusable across all workflow skills and development sessions.

> The architectural distinction: mechanical = "do X, not Y" (survives as terse imperative). Judgment = "apply X considering Y and Z" (needs operational context as a reusable skill). REQ-F3 is the only judgment standard.

**Clear:** REQ-F3 is judgment; therefore, it's a support skill.

**Question:** Where is REQ-F3 instructions read by workflow skills?

**Current options:**
1. Workflow skills load the `/gather` skill content during their Gather phase?
2. The `[REQ-F3 imperative loading instruction]` (COMP-2:238) is static text that references `/gather`?
3. The platform injects `/gather` content automatically, and workflow skills don't need to explicitly load it?

**Quote (DESIGN-005, line 238):**
> ### Gather [Content Type]
> [REQ-F3 imperative loading instruction]
> [Section-by-section gathering]

This suggests there's a line of instruction that is explicit. But what is it? Is it:
- "Use the `/gather` skill to prompt one section at a time"?
- An imperative like "Prompt the user section-by-section, waiting for response before proceeding"?
- A cross-reference to the skill file?

**Impact:** Skill authors need to know what text to write in the `[REQ-F3 imperative loading instruction]` placeholder. The design does not provide a template or example.

---

## 7. Completeness Check

### 7.1 What's Specified

✓ Purpose: One-at-a-time gathering (COMP-5:326)
✓ Type: Support skill, auto-invokable (COMP-5:339)
✓ Applicability: Workflow skill gathering phases + general development work (COMP-5:341)
✓ Exclusions: `/do` skill (COMP-5:341)
✓ Build order: First (DESIGN-005:542)
✓ Rationale: Failed inline pattern (BUG-018), reusable, independent testing (DESIGN-005:332-337)
✓ Interface contract: Auto-invocation via context matching, fallback option (INT-1:389-395)
✓ Flexibility: Drafts permitted with pauses (SPEC-004:REQ-F3)

### 7.2 What's Missing

✗ **Auto-invocation condition:** The actual `when_to_use` logic or format is not shown
✗ **Operational definition:** Where does "one at a time" methodology live? (Implied in `/gather` SKILL.md, not explicit)
✗ **Fallback implementation:** How do workflow skills explicitly reference `/gather` if auto-load fails?
✗ **REQ-F3 imperative text:** What exact text should workflow skills emit for `[REQ-F3 imperative loading instruction]`?
✗ **Interaction with drafting:** How does an agent decide when it has "sufficient context to draft"? (Rule stated, mechanism absent)
✗ **Testing strategy:** How do you verify that `/gather` is being used vs. agent defaulting to batching?

---

## 8. Cross-Document Consistency

### 8.1 SPEC-004 ↔ DESIGN-005 Alignment

**REQ-F3 (SPEC-004:56):**
> All commands that gather user input shall prompt one section at a time by default, waiting for the user's response before presenting the next section. When the agent has sufficient context to draft a section, it may present a draft for approval rather than prompting from scratch, but must still pause between sections for user confirmation. Do not draft content for sections the user has not yet been prompted for

**COMP-5 (DESIGN-005:326-341):**
Restates REQ-F3 accurately. Adds context on why it's a skill.

**Alignment:** ✓ Consistent. DESIGN-005 accurately reflects the SPEC-004 requirement.

### 8.2 DEC-2 vs. Earlier Revisions

**Issue:** Revision history shows the shared `_shared/gathering-standards.md` was removed in v0.4 (line 653). But COMP-1 (line 147-161) still references it under "Dependencies":

**Quote (lines 159-161):**
> **Dependencies:**
> - `.claude/skills/gather/SKILL.md` (support skill for REQ-F3, auto-invokable)
> - `.praxisity/templates/skill-standards.template.md` (human authoring reference template for UC-2)

This is correct (SKILL.md not the shared file). But earlier in COMP-1 (line 56), it says:

**Quote (line 56):**
> 1 judgment standard (F3 gathering protocol) lives in a shared file (`_shared/gathering-standards.md`) read with an imperative instruction at the Gather phase boundary

This contradicts the v0.4 revision, which removed the shared file.

**Assessment:** The document contains **vestigial text from v0.3** (before the redesign). Line 56 should reference the `/gather` SKILL.md, not a shared file.

**Impact:** Readers are confused by contradictory statements. The design is sound (skill-based, not file-based), but the document is inconsistent.

---

## 9. Missing Operational Clarity

### 9.1 "When to Use" Example

The design never shows what `when_to_use` looks like. Based on DESIGN-005, I infer:

**Likely structure (not provided):**
```yaml
---
name: gather
description: Structured one-at-a-time gathering protocol
when_to_use: |
  The agent is gathering structured input from the user across multiple sections
  and needs to ensure one-at-a-time prompting.
---
```

But this is **inference, not stated in the documents**. The actual SKILL.md for `/gather` is not included.

### 9.2 Explicit Fallback Reference

The design states: "Workflow skills can also reference `/gather` explicitly as a fallback" (DESIGN-005:394).

**Likely implementation (not provided):**

In the Gather phase of a workflow skill:

```markdown
### Gather [Content Type]

Use the `/gather` skill to prompt one section at a time.
[If that doesn't happen automatically, invoke `/gather` explicitly to ensure structured gathering.]

[Section-by-section gathering content]
```

But this is **inference**. The document does not provide a template.

---

## 10. Risk Assessment

| Risk | Severity | Evidence | Mitigation |
|------|----------|----------|-----------|
| Auto-invocation fails silently | **Medium** | Fallback exists, but auto-invocation is primary (INT-1:393) | Explicit fallback reference + testing strategy needed |
| Skill authors don't know what to write for REQ-F3 placeholder | **Medium** | COMP-2:238 shows `[REQ-F3 imperative loading instruction]` with no template | Provide template text before skill authoring begins |
| Operational definition of "one at a time" is hard to find | **Low** | Correct location (in `/gather` SKILL.md) is not explicitly stated | Add cross-reference: "See [SKILL definition](#) for operational details" |
| Vestigial document text creates confusion | **Low** | COMP-1:56 contradicts v0.4 revision history | Correct line 56 to reference `/gather` SKILL.md, not shared file |
| Drafting decision logic is unspecified | **Low** | "When the agent has sufficient context" is decision rule; implementation absent | Document or defer as agent design decision (not this spec's scope) |

---

## 11. Clarification Summary

| # | Issue | Current State | Clarification Needed |
|---|-------|---------------|---------------------|
| 1 | Auto-invocation mechanism | "via `when_to_use` context matching" (abstract) | Concrete example: what does `when_to_use` clause look like? |
| 2 | Operational definition location | Implied in `/gather` SKILL.md (not gathered) | Explicit cross-reference: "See [SKILL.md sections]" |
| 3 | REQ-F3 placeholder text | COMP-2:238 shows `[REQ-F3 imperative loading instruction]` (empty) | Template: "Use the `/gather` skill..." or similar |
| 4 | Explicit fallback invocation | "can reference `/gather` explicitly" (vague) | Example: How does skill call or reference `/gather` if auto-load fails? |
| 5 | Document inconsistency | COMP-1:56 vs. v0.4 revision | Update line 56 to reflect removal of shared file |
| 6 | Drafting decision criteria | "when agent has sufficient context" (rule only) | Design decision: is this in `/gather` SKILL or agent prompt responsibility? |

---

## 12. Conclusion

### What Is Clear

The `/gather` skill is a **well-motivated, architecturally sound solution** to a documented failure pattern (BUG-018). The decision to implement it as a reusable support skill (not inline text, not a shared file) is justified and aligns with the Praxisity bootstrapping principle. The skill's applicability, exclusions, and flexibility are well-specified.

### What Is Unclear

1. **INT-1 (auto-invocation mechanism)** relies on abstract language (`when_to_use` context matching) without concrete examples. Teams implementing this need to see the actual SKILL.md frontmatter and the platform's behavior.

2. **REQ-F3 imperative instruction** is a placeholder in COMP-2 with no template provided. Skill authors need an example of what to write.

3. **Operational definition** is correctly located (implied in `/gather` SKILL.md) but not explicitly cross-referenced, creating discovery friction.

4. **Fallback invocation** is mentioned but not exemplified. Unclear how a workflow skill would explicitly invoke `/gather` if auto-load fails.

5. **Document contains vestigial text** (COMP-1:56) from pre-v0.4 architecture, creating confusion about where the standard lives.

### Recommendation

**The design is implementation-ready once:**
1. The actual `/gather` SKILL.md is written (this would clarify issues #1, #2, #3 above)
2. COMP-2 is updated with a template example for the REQ-F3 placeholder (issue #3)
3. COMP-1:56 is corrected to reference `/gather` SKILL.md (issue #5)
4. A note is added to INT-1 describing explicit fallback invocation (issue #4)

All gaps are **recoverable** and do not indicate a flawed design — they are documentation precision issues typical of a design document that precedes implementation. The actual SKILL.md will clarify most of these automatically.

---

## Appendix: Quotes for Reference

**REQ-F3 (SPEC-004):**
> All commands that gather user input shall prompt one section at a time by default, waiting for the user's response before presenting the next section. When the agent has sufficient context to draft a section, it may present a draft for approval rather than prompting from scratch, but must still pause between sections for user confirmation. Do not draft content for sections the user has not yet been prompted for

**COMP-5 purpose (DESIGN-005:326):**
> Prevent batched gathering by codifying the one-at-a-time prompting protocol as a reusable, auto-invokable support skill.

**INT-1 contract (DESIGN-005:389-395):**
> **Type:** Platform auto-invocation via `when_to_use` context matching
>
> **Contract:**
> - **Trigger:** Agent is gathering structured input from the user across multiple sections — the `/gather` skill's `when_to_use` matches this context
> - **Mechanism:** Platform loads the gathering skill's instructions automatically, not via explicit cross-reference
> - **Failure mode:** If auto-invocation doesn't fire, the agent falls back to its default gathering behavior (which may batch). Bounded downside — same as current state. Workflow skills can also reference `/gather` explicitly as a fallback.

**Rationale for skill vs. shared file (DESIGN-005:332-337):**
> Inline "one section at a time" was already present in prototype commands and was defeated (BUG-018). A support skill provides the operational context AND is reusable across all sessions — not just workflow skill execution. The gathering protocol benefits every development session, making it a natural skill rather than embedded documentation. Building it as a skill gives immediate benefit — every session from this point forward uses the protocol, not just workflow skill executions. The gathering protocol can be developed, tested, and improved independently from the workflow skills.