# Design: [DESIGN-007] Portable Research Prompt

## Metadata

| Field | Value |
|-------|-------|
| Design ID | DESIGN-007 |
| Title | Portable Research Prompt for Free-Tier Claude.ai |
| Status | Draft |
| Author | Andrew |
| Created | 2026-04-09 |
| Last Updated | 2026-04-09 |

### Specification References

| Spec ID | Title | Requirements Addressed |
|---------|-------|------------------------|
| [SPEC-008](../specs/008-portable-research-prompt.md) | Portable Research Prompt for Free-Tier Claude.ai | REQ-F1, F4–F9, REQ-N1–N4 |

### Related Documents

| Document | Relationship |
|----------|--------------|
| [portable-research-prompt-v0.4.md](../references/portable-research-prompt-v0.4.md) | Current prototype — minimal prompt based on instructor baseline |
| [portable-research-prompt-v0.3.md](../references/portable-research-prompt-v0.3.md) | Prior prototype — full conversational pipeline (exceeded free-tier limits) |
| [portable-research-prompt-v0.2.md](../references/portable-research-prompt-v0.2.md) | Prior prototype — two-artifact pipeline |
| [public_health_trending_topics_april2026.md](../references/public_health_trending_topics_april2026.md) | Baseline — instructor's prompt that works within free-tier limits |
| [SPEC-008-prompt-v0.1-review.md](../reviews/SPEC-008-prompt-v0.1-review.md) | PE review of v0.1 |
| [Query_Report1.md](../references/Query_Report1.md) | Test output — v0.2 query report |
| [Research_Report1.md](../references/Research_Report1.md) | Test output — v0.2 research report |
| Team review reports | Informs — `.plans/reviews/SPEC-008-*-team-report.md` |
| [Compass artifact](../references/compass_artifact_wf-13120d19-5bce-4e73-9fff-357d7def829e_text_markdown.md) | Informs — free-tier capabilities and constraints |

---

## 1. Overview

### 1.1 Design Summary

**v0.1–v0.3 designed a five-phase conversational pipeline (Orient → Gather → Plan → Research → Deliver). Empirical testing proved this exceeds free-tier session limits — a user ran out of usage after the second gathering question.** The conversation overhead (multiple round-trips before any research begins) consumes the limited free-tier message budget before the prompt can do its actual job.

v0.4 pivots to the approach that already works: the instructor's single-shot prompt format. The user fills in their goal, pastes the prompt, and gets a single markdown artifact. No multi-turn gathering, no plan approval gate, no conversation flow control. The design challenge shifts from "how to control a multi-turn conversation" to "how much source quality can we add to a single-shot prompt without exceeding the session budget."

The strategy is additive: start from the instructor's proven baseline (~95 words), add only what demonstrably improves output quality, and test each addition against the session limit. v0.4 adds three innovations validated by the Mode 3 team review: source verification, Problem Log, and structural constraint against editorial sections.

### 1.2 Design Principles

- **Minimum effective prompt** — Every word must earn its token cost against the session budget. The free-tier limit is the primary constraint, not the 200K context window.
- **Structure over prohibition** — Control behavior through output format, not "don't do X" instructions. (Retained from v0.1–v0.3.)
- **Show your work over self-assessment** — Problem Log shows what happened, not whether it was good. (Retained from v0.1–v0.3.)
- **Additive from baseline** — Start from a prompt that works within limits, add incrementally, test each addition.

### 1.3 Requirements Coverage

The v0.4 pivot changes which spec requirements can be addressed within free-tier constraints:

| Requirement | Status | Approach |
|-------------|--------|----------|
| REQ-F1 (single paste, no mods) | **Met** | User fills in Goal field and pastes |
| REQ-F2 (one-at-a-time gathering) | **Deferred** | Exceeds session budget. User provides context in Goal field instead. |
| REQ-F3 (two artifacts) | **Superseded** | Merged to single artifact (team decision). Verification is future work. |
| REQ-F4 (all instructions inline) | **Met** | Entire prompt is self-contained |
| REQ-F5 (fits 200K context) | **Met** | ~180 tokens |
| REQ-F6 (direct quotes, correct links) | **Met** | Prompt instructs direct quotations and link verification |
| REQ-F7 (web search verification) | **Partially met** | Prompt instructs link verification; cannot specify DEC-8 mechanism at this token budget |
| REQ-F8 (problem log) | **Met** | Problem Log in output structure |
| REQ-F9 (minimize summarization) | **Partially met** | "Include direct quotations where possible" — softer than v0.3 but within token budget |
| REQ-F10 (dual-audience language) | **Met** | Prompt is readable by both AI and user |
| REQ-F12 (query report) | **Deferred** | Methodology can be added as a report section in future iterations |
| REQ-F13 (separate artifacts) | **Superseded** | Single artifact. Verification prompt is future work. |
| REQ-N1 (no experience needed) | **Met** | Fill-in-the-blank format |
| REQ-N2 (under 4000-6000 tokens) | **Met** | ~180 tokens — well under |
| REQ-N3 (natural conversation) | **Deferred** | No conversation — single-shot |
| REQ-N4 (expert-quality output) | **Testing** | v0.2 test showed expert-quality is achievable; v0.4 needs testing |

---

## 2. Architecture

### 2.1 System Context

```
┌──────────────────┐
│  User writes     │
│  Goal in prompt  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  User pastes     │
│  prompt + goal   │
└────────┬─────────┘
         │ single message
         ▼
┌──────────────────┐
│  Sonnet executes │
│  web searches +  │
│  builds report   │
└────────┬─────────┘
         │ single output
         ▼
┌──────────────────┐
│  Markdown        │
│  artifact in     │
│  artifact panel  │
└──────────────────┘
```

### 2.2 Architecture Pattern

**Pattern:** Single-Shot with Structured Output

No conversation pipeline. One input, one output. All behavioral control is in the prompt's output format specification. This is the simplest possible architecture and the only one confirmed to work within free-tier session limits.

**Trade-offs:**
- Pros: Proven to complete within session limits, zero conversation overhead, simplest user experience
- Cons: No gathering (user must know what to ask), no approval gate (no chance to course-correct), less control over research strategy

### 2.3 Technology Choices

| Concern | Choice | Rationale |
|---------|--------|-----------|
| Model | Sonnet 4.6 (free tier) | Only option |
| Output format | Markdown artifact | Explicitly specified; prevents JavaScript/React artifacts |
| Prompt format | Role/Goal/Sources/Links/Output | Matches instructor's proven format |
| Domain | Public health | Hardcoded source list; generalization deferred post-internship |

---

## 3. Components

### COMP-1: Prompt Template

**Purpose:** The entire prompt — a fill-in-the-blank template the user completes and pastes.

**Satisfies:** REQ-F1, REQ-F4, REQ-N1

**Sections:**
- **Role** — Fixed: public health research analyst
- **Goal** — User fills this in
- **Sources** — Authoritative PH sources + web search verification instruction
- **Links** — Specific-page requirement + [link unconfirmed] pattern
- **Output** — Markdown artifact structure with findings, source list, problem log

**Key constraint:** ~135 words / ~180 tokens. Every addition must be tested against session limits.

---

### COMP-2: Output Structure

**Purpose:** Define what the markdown artifact contains so Sonnet produces structured, verifiable output.

**Satisfies:** REQ-F6, REQ-F8, REQ-F9

**Sections defined in the prompt:**
- Findings organized by topic, with quoted sources and URLs
- Source list grouped by topic
- Problem log (unconfirmed links, contradictions, gaps, summarized claims)

**Structural constraint:** "Do not add editorial analysis or commentary sections beyond what the goal asks for." — Addresses DQ-1 without prohibition.

---

## 4. Interfaces

### INT-1: User → Prompt

**Type:** Fill-in-the-blank

**Contract:** User writes their research goal in the Goal field. The prompt provides the Role, Sources, Links, and Output structure. User pastes the complete prompt as a single message.

---

### INT-2: Sonnet → Artifact

**Type:** Automatic

**Contract:** Sonnet produces a single markdown document in the artifact panel. The document follows the Output structure defined in the prompt.

---

No user gates. No mid-session approval. The trade-off for fitting within session limits.

---

## 5. Data Model

### DATA-1: Research Report Artifact

**Purpose:** Single output document with source-backed findings and a problem log

| Field | Required | Description |
|-------|----------|-------------|
| Findings | Yes | Organized by topic. Each finding: quoted content, source name, URL |
| Source List | Yes | Grouped by topic. Each entry: org/author, title, URL |
| Problem Log | Yes | Unconfirmed links, contradictions, gaps, summarized claims |

---

## 6. Design Decisions

### DEC-1: Single-Shot Over Conversational Pipeline (NEW — supersedes v0.1–v0.3)

**Context:** v0.3 conversational pipeline exceeded free-tier session limits. A user ran out of usage after the second gathering question. The instructor's single-shot prompt completes successfully.

**Decision:** Abandon the multi-turn pipeline. Use the instructor's single-shot format as the baseline and add quality improvements incrementally.

**Rationale:** A prompt that can't complete is worse than a prompt with fewer features. The session limit is the binding constraint, not the context window or prompt engineering best practices.

**Alternatives Considered:**
- Compress the pipeline to fewer turns: Still risks hitting limits; each round-trip has hidden token costs from web search
- Keep pipeline for paid users, single-shot for free: Scope creep — spec covers free tier only

**What this supersedes:** DEC-1 (sequential prose), DEC-5 (fixed limitations text), DEC-6 (two user gates), DEC-7 (tone directive), DEC-9 (separate artifacts) from v0.1–v0.3 design are all retired. These were good engineering for a pipeline that doesn't fit the constraint.

---

### DEC-2: Problem Log Over Self-Assessment (RETAINED)

**Context:** PE review identified self-check as theater.

**Decision:** Problem Log shows what happened: unconfirmed links, contradictions, gaps, summarized claims.

**Rationale:** Validated by v0.2 test data — 4 of 6 Problem Log entries were genuinely useful. All 5 agents in the Mode 3 review agreed this was the standout feature.

---

### DEC-3: Drop Citation Formatting (RETAINED)

**Decision:** No IEEE or other formal citation style. Inline attribution by source name + URL. Formatting is a downstream concern.

---

### DEC-4: Positive Structure Over Prohibition (RETAINED, simplified)

**Decision:** "Do not add editorial analysis or commentary sections beyond what the goal asks for." — One structural constraint in the output section.

**Rationale:** v0.2 test showed 5 unsolicited "Public Health Relevance" editorial sections. This single line addresses it without elephants.

---

### DEC-8: Link Verification (RETAINED, simplified)

**Decision:** "Every URL must point to the specific page where the information was found, not a homepage. If you cannot confirm a link, mark it [link unconfirmed]."

**Rationale:** The full DEC-8 mechanism ("search for article title + source organization") is too many tokens for v0.4. The simplified version still establishes the principle and the failure-marking pattern. Can be expanded in future iterations if token budget allows.

---

### DEC-10: Public Health Focused (UPDATED per developer decision)

**Decision:** Prompt is explicitly public health. Source list includes CDC, WHO, NIH, peer-reviewed journals. Generalization deferred to post-internship.

**Rationale:** Developer decision during Mode 3 review. Eliminates the three-way domain contradiction across spec/design/prompt.

---

### DEC-11: Prompt Brevity as Primary Constraint (UPDATED — now the binding constraint)

**Decision:** The free-tier session limit is the primary design constraint. The prompt must be as short as possible while producing verifiable output. Every addition is tested against session viability.

**Rationale:** v0.3 proved that a 1400-token prompt with multi-turn conversation exceeds free-tier limits. The instructor's ~95-word prompt works. v0.4 at ~135 words is the first increment to test.

---

### DEC-12: Additive Iteration Strategy (NEW)

**Context:** v0.1–v0.3 took a top-down approach (design the ideal, then cut). This consistently produced prompts that exceeded session limits.

**Decision:** Start from the instructor's baseline (confirmed to work), add one feature at a time, test each addition against session limits. Only keep additions that survive testing.

**Rationale:** Bottom-up from proven baseline is safer than top-down from ideal specification when the binding constraint is empirical and unpublished.

**Iteration plan:**
1. v0.4: Baseline + source verification + problem log + structural constraint (~135 words) — TEST
2. v0.5: If v0.4 works, add methodology section or gathering question — TEST
3. Continue until session limit is found, then stop one step before it

---

## 7. Implementation Considerations

### 7.1 Implementation Order

| Order | Step | Notes |
|-------|------|-------|
| 1 | Test v0.4 on free tier | Does it complete? Does the problem log appear? Are links verifiable? |
| 2 | If passes: add one feature (e.g., methodology section) → v0.5 | Test again |
| 3 | If fails: cut the heaviest instruction and retest | Find the minimum effective prompt |
| 4 | Repeat until session limit is found | Stop one step before it |

### 7.2 Risk Areas

| Risk | Impact | Mitigation |
|------|--------|------------|
| v0.4 still exceeds session limits | Can't complete; need to cut further | Fall back to instructor baseline + problem log only |
| Sonnet ignores source verification at this token budget | Links unverified, output no better than baseline | Test and compare; if verification isn't happening, the instruction isn't earning its tokens |
| Sonnet creates JavaScript artifact instead of markdown | User can't easily use the output | "Create a markdown artifact" explicit in v0.4 |
| Problem Log is empty (Sonnet doesn't self-report issues) | Loses the standout feature | Test; if empty, may need more explicit Problem Log instruction (costs tokens) |
| "Do not add editorial sections" is ignored | Unsolicited synthesis sections appear | Test; if persistent, may need to remove (it's only 12 words) |

### 7.3 Testing Strategy

| Level | Approach | Covers |
|-------|----------|--------|
| Session viability | Paste v0.4 on free tier, confirm full completion | Primary constraint |
| Source quality | Check 3+ URLs from output | REQ-F6, F7 |
| Problem Log presence | Verify Problem Log appears and contains entries | REQ-F8, DEC-2 |
| Editorial suppression | Verify no unsolicited sections beyond goal | DEC-4 |
| Baseline comparison | Compare v0.4 output quality to instructor baseline | REQ-N4 |
| Additive testing | After each feature addition, rerun session viability | DEC-12 |

---

## 8. Out of Scope

**From Specification (inherited):**
- Integration into Praxisity as a skill or command
- Paid-tier features
- Automated verification pipelines
- Custom UI or delivery beyond copy-paste
- Prompt generation tooling

**Deferred by session-limit constraint:**
- Multi-turn gathering (REQ-F2) — exceeds session budget
- Research plan / approval gate (REQ-F12) — exceeds session budget
- Separate verification artifact (REQ-F13) — merged to single output
- Conversational flow control — single-shot only
- Tone directive — costs tokens, single-shot doesn't need it
- Detailed verification mechanism (full DEC-8) — costs tokens; simplified version in v0.4

**Future work:**
- Purpose-built verification prompt (separate spec)
- Domain generalization (post-internship)
- Additive features from v0.5+ iteration

---

## 9. Open Questions

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| DQ-1 | Editorial sections | Resolved | Single structural constraint: "Do not add editorial analysis or commentary sections beyond what the goal asks for." |
| DQ-2 | Wikipedia flagging | Deferred | Not enough token budget in v0.4. Add in v0.5 if session allows. |
| DQ-3 | Landing page URLs | Resolved | "Every URL must point to the specific page where the information was found, not a homepage." |
| DQ-4 | Where is the session limit? | Open | Empirical testing required. v0.3 exceeded it. Instructor baseline fits. v0.4 is between them. |
| DQ-5 | Does source verification actually happen at ~180 tokens? | Open | Test required. If Sonnet ignores the instruction at this brevity, the tokens aren't earning their place. |

---

## 10. Appendices

### A. Glossary

| Term | Definition |
|------|------------|
| Lethal trifecta | Security principle: AI output cannot be trusted as input without independent verification |
| Problem Log | A factual record of issues encountered during research, replacing self-assessment |
| Session limit | Free-tier usage cap that resets every 5 hours; unpublished exact count |
| Single-shot | One user message, one AI response — no multi-turn conversation |
| Additive iteration | Starting from a proven baseline and adding features one at a time |

### B. Version History — Design Approach

| Version | Architecture | Token Budget | Session Viable? |
|---------|-------------|-------------|-----------------|
| v0.1 | 5-phase pipeline, two artifacts | ~1100 tokens | Not tested |
| v0.2 | 5-phase pipeline, two artifacts | ~1400 tokens | Succeeded (paid-tier test) |
| v0.3 | 5-phase pipeline, single artifact | ~1500 tokens | **Failed** — user hit limit after 2nd question |
| v0.4 | Single-shot, single artifact | ~180 tokens | **Testing** |

### C. References

- [SPEC-008: Portable Research Prompt](../specs/008-portable-research-prompt.md)
- [v0.4 Prototype](../references/portable-research-prompt-v0.4.md)
- [v0.3 Prototype](../references/portable-research-prompt-v0.3.md)
- [v0.2 Prototype](../references/portable-research-prompt-v0.2.md)
- [v0.2 Test: Query Report](../references/Query_Report1.md)
- [v0.2 Test: Research Report](../references/Research_Report1.md)
- [Instructor Baseline](../references/public_health_trending_topics_april2026.md)
- [PE Review of v0.1](../reviews/SPEC-008-prompt-v0.1-review.md)
- [Mode 3 Team Reports](../reviews/SPEC-008-*-team-report.md)
- [PM Daily Report](../reviews/SPEC-008-pm-daily-report.md)
- [Free-tier Capabilities Research](../references/compass_artifact_wf-13120d19-5bce-4e73-9fff-357d7def829e_text_markdown.md)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-04-09 | Andrew | Initial draft — 5-phase pipeline architecture |
| 0.2 | 2026-04-09 | Andrew | Pivot to single-shot after free-tier session limit failure. Additive iteration from instructor baseline. v0.4 prompt. |