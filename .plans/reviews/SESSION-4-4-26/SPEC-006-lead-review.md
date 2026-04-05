## Lead Review

**Artifact:** SPEC-006 + /gather SKILL.md prototype
**Date:** 2026-04-04
**Dispatch Mode:** Mode 2: parallel
**Team Composition:** critic, prompt-engineer, designer, consistency-reviewer, spot

## Synthesis

### Strong Consensus (all or nearly all agents)

**1. REQ-G8/G9 (memory-as-settings) completely missing from prototype.** (critic, designer, PE — all flagged)
The spec describes a stateful skill with calibration and preference loading (two MUST requirements). The prototype is entirely stateless. DESIGN-005 COMP-5 also has no coverage of the memory subsystem. Either the prototype needs extending or this is explicitly acknowledged as Phase 2.

**2. BUG-034 is misclassified.** (critic, PE, consistency-reviewer)
BUG-034 is about `/do` batching DIP execution steps — agent-driven work, not user-input gathering. DESIGN-005 COMP-5 explicitly excludes `/do` from the gather skill's applicability. The gather skill will not fix BUG-034. Remove from SPEC-006 citations.

**3. Stale "shared file" references need propagation.** (consistency-reviewer)
The v0.4 decision (shared file → support skill) wasn't propagated to all locations. 6 stale references in DESIGN-005, Q-4 resolution text in SPEC-004. Root cause: decision recorded in revision history but not updated in all body text.

### Important Findings (2-3 agents)

**4. "What You Must Not Do" is an elephants problem.** (PE)
Five prohibitions that are a complete recipe for the batching failure mode. Line 40 literally says "Do not present all sections at once for batch approval" — activating the exact representation it's trying to suppress. Recommendation: cut the section, add a structural verification step to the positive flow instead.

**5. "Sufficient context" is self-assessed with no calibration.** (PE, spot)
The agent will almost always conclude it has sufficient context. BUG-018 happened this way. PE recommends making the gate observable: "draft only when user has already provided direct input on this topic in this conversation." Spot recommends: "If you're uncertain whether context is sufficient, prompt instead."

**6. REQ-G3 vs REQ-G5 contradiction.** (critic)
REQ-G3 (MUST): "shall not draft content for sections the user has not yet been prompted for." REQ-G5 (SHOULD): "fill in the rest" allows drafting remaining sections. A SHOULD cannot override a MUST without an explicit exception clause. Fix: add "unless the user explicitly requests it" to REQ-G3.

**7. "Fill in the rest" confirmation sequence ambiguous.** (spot)
Does "present each individually for confirmation" mean strict one-at-a-time (present, wait, present, wait) or present all then batch-approve? Needs an explicit example.

### Minor Findings

**8. DATA-2 in DESIGN-005 is stale.** (critic, designer)
Describes a "3 sections, under 20 lines" file from the shared-file era. The SKILL.md is 6 sections, 50 lines. Update DATA-2.

**9. REQ-G7 has no acceptance criterion.** (critic)

**10. DESIGN-005 needs DEC-8 for memory-as-settings.** (designer)
The framework pattern identified in SPEC-006 should be reflected in the design as a new design decision.

### What's Strong

- The core rule ("present one section at a time, wait for response") is unambiguous (spot: 8/10 clarity)
- Sub-section handling directly addresses BUG-012
- Skip-request handling is clean
- Self-containment achieved — zero cross-references
- Workflow/support skill taxonomy is architecturally sound
- The skill composes well with workflow skills on orthogonal concerns (what vs. how)

## Action Items

| # | Action | Priority | Source |
|---|--------|----------|--------|
| 1 | Remove BUG-034 from SPEC-006 citations | High | critic, PE, CR |
| 2 | Add exception clause to REQ-G3: "unless the user explicitly requests it (REQ-G5)" | High | critic |
| 3 | Cut "What You Must Not Do" section from SKILL.md; replace with structural verification | High | PE |
| 4 | Tighten "sufficient context" — make gate observable, not self-assessed | High | PE, spot |
| 5 | Add explicit "fill in the rest" example to SKILL.md | Medium | spot |
| 6 | Propagate "shared file → support skill" to all stale references in SPEC-004 and DESIGN-005 | Medium | CR |
| 7 | Acknowledge REQ-G8/G9 as Phase 2 of the prototype, or extend SKILL.md now | Medium | critic, designer, PE |
| 8 | Update DESIGN-005: DATA-2, add DEC-8 (memory-as-settings) | Medium | designer |
| 9 | Add AC-G8 for REQ-G7 | Low | critic |