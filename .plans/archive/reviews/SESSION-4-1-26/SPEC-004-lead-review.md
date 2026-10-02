## Lead Review

**Artifact:** SPEC-004 — Command Behavioral Fixes and Pattern Standards
**Date:** 2026-04-01
**Dispatch Mode:** Mode 2: parallel
**Team Composition:** critic, skeptic, project-manager, consistency-reviewer, designer, user-advocate, stakeholder, prompt-engineer, spot

## Per-Agent Assessment

- **Critic:** Thorough, evidence-based review. Read all command files and the full bug report. Identified the REQ-F1/REQ-N1 contradiction and the 27-bug mapping gap — both emerged as top consensus findings. Correctly flagged REQ-F3's blanket MUST as under-specified.
- **Skeptic:** Sharp scope challenge. Recommended dropping the standalone standards document, dropping REQ-F8, demoting REQ-N2, and enumerating OBJ-3 bugs. Raised the key insight that AI agents don't follow cross-references like code follows imports — inline duplication may be necessary.
- **Project Manager:** Practical feasibility assessment. Estimated 4-7 hours total effort. Flagged REQ-F7 as potentially already satisfied by existing CLAUDE.md hint. Identified `/deliver` Python bugs as a different kind of work than markdown command edits.
- **Consistency Reviewer:** Systematic cross-document verification. Found BUG-031 misattributed to REQ-F1 (it's about marking sections N/A, not copy-then-edit). Caught missing BUG-012 in REQ-F3 citations. Noted Charter tension around Todoist mandate vs. REQ-F6 deferral.
- **Designer:** Strong architectural analysis. Identified the standards delivery mechanism as the primary design question. Proposed splitting REQ-N1 into two tiers (section-level rewrites for pattern-class, targeted edits for command-specific). Confirmed command file structure supports the changes without reorganization.
- **User Advocate:** Focused on UX impact. Flagged REQ-F3 as friction for experienced users — supports a "fast mode" where the agent drafts from context and presents for review. Called REQ-F1 the best UX improvement (deterministic template output builds trust).
- **Stakeholder:** Reviewer/consumer perspective. Confirmed the five pattern classes are the right extractions. Two blockers identified: missing disposition table and unbounded OBJ-3. Verdict: "close but not ready."
- **Prompt Engineer:** Evaluated dual-consumption fitness. Found that numbered lists already failed to prevent parallelization (BUG-016/017) — the fix needs stronger language than what was already defeated. Flagged "don't think about elephants" risk with BUG-009 exception clause in bug report. Noted REQ-F4 is a meta-pattern, not a uniform template.
- **Spot:** Cold-read clarity check. Identified 9 missing elements including undefined terms (batching, targeted edit), missing deliverables section, 7-vs-8 commands contradiction, and undefined bug tracking table schema. Verdict: "implementable but requires clarification."

## Synthesis

### Areas of Agreement (6+ agents)

**1. The bug disposition table is the biggest gap.** (critic, skeptic, PM, consistency-reviewer, stakeholder, spot)
OBJ-3, OBJ-4, REQ-N2, and AC-6 all promise that every bug gets a disposition, but the spec never provides one. ~27 bugs sit outside the five pattern classes with no explicit categorization. The design phase has no target list for command-specific fixes. **Resolution: add a disposition table before `/architect`.**

**2. REQ-F1 ("targeted edits") conflicts with the scope of Generate section rewrites.** (critic, designer, prompt-engineer)
Implementing copy-then-edit requires rewriting the entire Generate section of 4-5 commands. That's not a "targeted edit" by any reasonable definition. **Resolution: split REQ-N1 into two tiers — section-level rewrites acceptable for pattern-class standards, targeted edits only for command-specific bugs.**

**3. REQ-F3 blanket MUST is too rigid.** (critic, skeptic, designer, user-advocate, prompt-engineer)
The bug report itself hedges on strict enforcement. Need to distinguish user-facing gathering (one-at-a-time protects UX) from agent execution steps (batching is efficient). Experienced users would find rigid enforcement pedantic. **Resolution: apply REQ-F3 specifically to user-facing prompts in gather phases; allow agent-side execution batching with individual completion marking.**

**4. Standards delivery mechanism is undefined.** (designer, prompt-engineer, spot)
The spec says standards will be "documented in a reference that all commands can cite" but never specifies where the reference lives, how commands consume it, or whether standards are duplicated inline vs. referenced. This is the primary design question. **Resolution: acknowledge as an open architectural question for the design phase (this is appropriately a design decision, not a spec decision).**

### Areas of Moderate Agreement (3-5 agents)

**5. REQ-F7 may already be satisfied.** (PM, skeptic, prompt-engineer)
CLAUDE.md already contains: "Just because a template or example has a certain number of items, there is no requirement for your output to contain the same number of items filled out." REQ-F7 proposes adding essentially the same note. **Resolution: verify whether existing hint is sufficient; if so, close REQ-F7.**

**6. BUG-040 (context compaction) needs explicit deferral.** (PM, stakeholder)
This is a platform limitation, not fixable by command edits. Should be named in Out of Scope with rationale. **Resolution: add to Section 8.**

**7. UC-2 adds minimal value.** (skeptic, prompt-engineer)
Exists to justify the standards document; adds no testable acceptance criteria. May lead the architect to over-invest in the reference document. **Resolution: keep but note as aspirational context, not a design driver.**

**8. Missing acceptance criteria for MUST requirement REQ-N1.** (critic, consistency-reviewer)
Every other MUST requirement has an AC. REQ-N1 does not. **Resolution: add AC-7 for REQ-N1.**

### Unique Insights Worth Preserving

- **Consistency Reviewer:** BUG-031 is misattributed to REQ-F1. Its root cause (removing sections instead of marking N/A) is not addressed by copy-then-edit. Needs its own sub-requirement or reassignment.
- **Consistency Reviewer:** BUG-012 (/charter batched gathering) is missing from REQ-F3's cited bugs.
- **Consistency Reviewer:** CHARTER.md still mandates Todoist; REQ-F6's deferral represents an undocumented direction change.
- **Prompt Engineer:** The fix for parallelization (REQ-F2) needs to be phrased more aggressively than numbered lists — the numbered list pattern was already defeated. Explicit "do not begin step N+1 until step N is complete" language needed.
- **Prompt Engineer:** BUG-009 exception clause in bug report ("if user explicitly requests prior context") is a "don't think about elephants" risk if carried into the standard.
- **Designer:** The command file structure already supports the changes — Pre-Flight, Generate, Success Message sections map directly to pattern-class standards. No reorganization needed.
- **Skeptic:** AI agents don't reliably follow cross-references. Repeating behavioral instructions inline in each command file may be necessary, not redundant.

### Unresolved Tensions

**1. Standards reference document: create it or skip it?**
- Skeptic says drop it — apply patterns directly to command files, use bug report as rationale archive.
- Designer says it's the only new architectural component and needs clear structural definition.
- Prompt-engineer notes AI agents don't follow cross-references well, arguing for inline duplication.
- **User decision needed:** Is the standards document a design artifact for human authors, an AI-consumed reference, or both?

**2. REQ-F3 scope: how much flexibility?**
- Critic proposes an exception clause (draft-then-approve when context is rich).
- User-advocate wants a "fast mode" for experienced users.
- Skeptic says just do the fix as stated and revisit later.
- **User decision needed:** Strict one-at-a-time, or allow draft-then-approve with mandatory pause between sections?

**3. `/deliver` bugs: same spec or separate?**
- PM notes `/deliver` bugs (BUG-038, 039, 045, 046) are Python code fixes, not markdown command edits — different kind of work.
- **User decision needed:** Keep in disposition table as deferred, or handle separately?

## Readiness Verdict

**Not yet ready for `/architect` — but close.** Two items need resolution first:

1. **Add a bug disposition table** classifying all 46 bugs as: addressed by REQ-F1–F8, command-specific targeted fix, deferred, or won't-fix. (~30 min of focused work)
2. **Resolve the REQ-F1/REQ-N1 tension** by splitting REQ-N1 into two tiers or adding an explicit exception for Generate section rewrites.

Optional but recommended before design:
- Fix BUG-031 misattribution (reassign from REQ-F1 to its own sub-requirement)
- Add BUG-012 to REQ-F3 citations
- Verify REQ-F7 against existing CLAUDE.md hint
- Add BUG-040 to Out of Scope
- Add missing AC for REQ-N1
