# Clarity Check: SPEC-008 — Portable Research Prompt

**Reviewer:** Claude Code (clarity audit, no project background)
**Document:** `.plans/specs/008-portable-research-prompt.md`
**Date:** 2026-04-08
**Overall Assessment:** Document is clear, well-structured, and internally consistent. No blocking ambiguities. See issues below.

---

## Summary

SPEC-008 defines a single-paste prompt for free-tier Claude.ai users that structures a guided research workflow with source verification. The spec is well-scoped, requirements are testable, and acceptance criteria are concrete. The document successfully bridges technical precision (for prompt engineering) with accessibility language (for non-technical users).

The only substantive issues are:

1. **REQ-F7 / AC-3 ambiguity**: "Verified hyperlinks" is not fully defined — unclear what "verification" means operationally when Claude is restricted to web search and cannot perform link testing.

2. **REQ-F12 / REQ-F13 security claim**: The lethal trifecta rationale relies on an external reference that is not fully explained within the spec, creating a trust gap for readers unfamiliar with the pattern.

3. **Conversation capacity estimation**: The spec acknowledges session limits (REQ-N2 discusses 4k–6k tokens for the prompt itself) but lacks empirical guidance on total conversation depth before hitting the 5-hour reset or session usage limit.

---

## Issues

### 1. REQ-F7 / AC-3: "Verified hyperlinks" is operationally vague

**Location:** Lines 59–60, 116–117

**Quote:**
> REQ-F6: Output shall include direct quotations from sources with verified hyperlinks, not paraphrased summaries
>
> AC-3: Given the drafting phase, when Claude includes a factual claim, then it provides a direct quotation and a hyperlink that has been verified via web search

**What's unclear:**
- "Verified" is ambiguous. Does it mean:
  - Claude successfully fetched the URL and confirmed the quoted text appears on that page?
  - Claude confirmed the link is accessible (HTTP 200 response)?
  - Claude confirmed the link is still alive and hasn't been redirected?
  - Something else?

- Free-tier Claude has web search, but web search is not the same as link testing. The Compass artifact confirms web search "counts against usage limits" but does not specify whether Claude can test link validity programmatically. Can Claude submit a HEAD request to verify a link, or does "web search" mean only keyword-based queries?

**What's needed to understand:**
- Clarify whether verification means: (a) fetching the page to confirm the quote exists, (b) confirming the URL is accessible, or (c) something weaker.
- Specify the mechanism: Is this manual inspection of search results, or can Claude programmatically test URLs?
- Define fallback behavior: What does the prompt do if web search cannot verify a link?

**Impact:** Moderate. This affects acceptance criteria and test design. Testers won't know when AC-3 is satisfied.

---

### 2. REQ-F12 / REQ-F13: "Lethal trifecta" security model not explained inline

**Location:** Lines 12, 65–66

**Quote (header):**
> | Charter Reference | CHARTER.md — Bootstrapping Principle, Principle 6 (dual-audience) |

**Quote (requirements):**
> REQ-F12: After gathering, the AI shall produce a Query Report artifact describing the planned search strategy, output structure, and error handling before beginning research | MUST | User-auditable plan and in-context self-reference. Must be independently verifiable in a separate conversation per the lethal trifecta — untrusted output cannot be used as trusted input without external verification
>
> REQ-F13: The research output shall be a separate markdown artifact from the query report | MUST | Separation enforces independent verification of intent (query report) and evidence (research report) in separate conversations before either can be trusted as input to downstream prompt chains

**What's unclear:**
- The rationale for REQ-F12 and REQ-F13 rests on "the lethal trifecta" security model, but this model is not defined in the spec itself. Readers are directed to external references (CHARTER.md, project memory).
- The claim that "separate conversations" enable "independent verification" assumes readers understand the lethal trifecta framework. A reader without that context cannot assess whether the security logic is sound.
- The phrase "untrusted output cannot be used as trusted input without external verification" is asserted but not justified within the spec. Why is this principle necessary for a research prompt on free-tier Claude.ai? What threat is being mitigated?

**What's needed to understand:**
- Either: (a) define the lethal trifecta model inline in Section 3 (Constraints), or (b) explicitly explain in the requirement rationale why query and research reports must be separately verifiable.
- Clarify what "independently verifiable in a separate conversation" operationally means: Does the user need to re-run the query report prompt in a fresh conversation to trust it? Or is it sufficient that the artifacts are self-contained and can be inspected offline?

**Impact:** Low-to-moderate. This doesn't block implementation, but it weakens the spec's justification for architectural decisions. Readers will have to hunt external references to understand "why" these requirements exist.

---

### 3. Conversation depth vs. session limits: Empirical guidance missing

**Location:** Section 6.1, Line 130

**Quote:**
> Session usage limit resets every 5 hours — complex prompts may hit this mid-conversation

**What's unclear:**
- The spec acknowledges the risk ("may hit this mid-conversation") but doesn't provide guidance on conversation depth. How many exchanges can a user expect before hitting the limit?
- REQ-N2 specifies the *prompt itself* should be ~4k–6k tokens. But what about the total conversation? After gathering, query report, and research execution, how much context will be consumed?
- The Compass artifact estimates "a session-based usage limit that will reset every five hours. The number of messages you can send will vary based on demand." But this is vague for specification purposes.
- Q-1 in Section 9 explicitly asks "How does the prompt handle hitting the free-tier session usage limit mid-conversation?" and is marked "Resolved" with the answer "Mitigate through prompt brevity — maximize specificity while minimizing language. Test empirically. Not a prompt-level recovery feature."

**What's needed to understand:**
- Empirical testing (or reference to past testing) showing: typical number of turns until usage limit, approximate token consumption per turn, whether the pattern REQ-F12/REQ-F13 (query report, then research) is feasible within a single 5-hour session.
- Explicit guidance in the prompt design or acceptance criteria on warning thresholds (e.g., "if approaching limit, stop and summarize").

**Impact:** Low. This doesn't block the spec but leaves implementation guidance uncertain. Testers may discover the prompt hits session limits before completing the research phase.

---

### 4. Minor: Charter reference mismatch

**Location:** Line 13

**Quote:**
> | Charter Reference | CHARTER.md — Bootstrapping Principle, Principle 6 (dual-audience) |

**What's unclear:**
- The reference lists "Principle 6 (dual-audience)" but CHARTER.md lists Principle 6 as **"Dual-use design"** (not "dual-audience"). The concept is the same — "All templates, skills, and outputs optimized for both human understanding and AI agent consumption" — but the terminology differs.

**What's needed to understand:**
- Confirm: Is "dual-audience" the intended term here, or should it reference "dual-use design"? Either way, it's a minor terminology inconsistency.

**Impact:** Negligible. The concept is clear from context, but the reference should match the source document exactly.

---

### 5. Q-3 Resolution is slightly incomplete

**Location:** Section 9, Q-3

**Quote:**
> Q-3: What specific domain will the first test prompt target? | Resolved | Broad public health topic scan — "top 5 public health topics in the news." Gathering surfaces: intended audience/stakeholder, timeframe, geography. Output is a query report + research report, not a final deliverable. Designed for downstream prompt chaining.

**What's unclear:**
- The resolution describes *what* the first prompt will do ("top 5 public health topics in the news") but doesn't specify *when* it will be built or *how* it relates to the internship use case mentioned in Section 7.2 ("BSI internship deliverables").
- Is the "top 5 public health topics" prompt the final deliverable for the internship, or a prototype to test the pattern?

**What's needed to understand:**
- Link this open question's resolution to the project timeline or BSI internship scope.

**Impact:** Very low. This is internal process documentation; it doesn't affect the spec's functional requirements.

---

## What's Clear

The following aspects of the spec are well-defined and unambiguous:

- **Problem statement** (Section 1): Non-technical users lack prompt engineering skills to extract structured output from free-tier Claude. The gap is process/guidance, not capability.
- **Goals** (Section 2): Primary goal is clear — portable, self-contained, zero-setup prompt that produces structured output from non-technical users.
- **Functional requirements** (Section 3.1): REQ-F1 through F13 are testable, with clear success/fail criteria. The emphasis on traceability (direct quotes + verified links) and self-audit (REQ-F8) is well-motivated.
- **Non-functional requirements** (Section 3.2): Token budget, tone, engagement, quality parity are all reasonable and measurable.
- **User stories** (Section 4): UC-1 walks through the happy path clearly. Alternative flows (short answers, file uploads, dead links) are realistic.
- **Acceptance criteria** (Section 5): AC-1 through AC-7 map cleanly to requirements and are independently verifiable.
- **Platform constraints** (Section 6.1): Sonnet 4.6, 200K token window, 5-hour session reset, no sub-agents — all backed by the Compass artifact.
- **Out of scope** (Section 8): Sharp boundary. No ambiguity about what the prompt does NOT do (framework integration, multi-conversation workflows, paid-tier features, custom UI).

---

## Structural and Stylistic Notes

- **Metadata table** (Section 0): Well-formatted and complete.
- **Related documents** table: Helpful cross-references, though the Compass artifact link is a UUID path that may not be stable.
- **Revision history**: Appropriate for a draft.
- **Dual-audience language**: Spec engineering language is precise (e.g., "MUST", "SHOULD", "COULD" per RFC-2119 convention implicit in the tables). Expected user-facing prompt language is flagged in REQ-F10, which is good.

---

## Recommendations

### For Specification Clarity

1. **Define "verified hyperlinks" operationally** (REQ-F7/AC-3): Specify whether verification means page-fetch, link test, or search-result inspection. Add a fallback behavior for unverifiable links.

2. **Explain the lethal trifecta security rationale inline** (REQ-F12/F13): Either embed a brief definition of the model in Section 6 (Constraints), or rewrite the requirement rationale to justify the separation without external reference.

3. **Provide empirical conversation capacity guidance**: Add a note under REQ-N2 or Section 6.1 estimating typical turns before usage limit, or explicitly delegate this to testing phase with acceptance criteria for "prompt must complete gathering + query report + one research report within a 5-hour session."

4. **Verify Charter reference terminology**: Confirm "Principle 6 (dual-audience)" vs. CHARTER.md's "Principle 6 (dual-use design)."

### For Implementation

1. Start with REQ-F7 verification testing early — this is the highest-risk technical requirement.
2. Empirically test conversation depth against session limits before finalizing the prompt.
3. Consider whether REQ-F12 (query report before research) is essential or a "nice-to-have" — it adds a turn that consumes tokens and delays results.

---

## Conclusion

This is a well-written, professionally structured specification. The problem is clearly motivated, requirements are testable, and acceptance criteria are concrete. The three issues flagged above are clarifications, not blockers. The spec is ready for design/implementation phase with minor refinements to operationalize "verification" and justify the security model.

**Recommendation:** Proceed to prompt design. Resolve REQ-F7 ambiguity during prototype testing.