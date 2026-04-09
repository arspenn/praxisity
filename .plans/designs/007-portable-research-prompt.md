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
| [SPEC-008](../specs/008-portable-research-prompt.md) | Portable Research Prompt for Free-Tier Claude.ai | REQ-F1–F13, REQ-N1–N4 |

### Related Documents

| Document | Relationship |
|----------|--------------|
| [portable-research-prompt-v0.2.md](../references/portable-research-prompt-v0.2.md) | Prototype — v0.2 prompt being designed against |
| [SPEC-008-prompt-v0.1-review.md](../reviews/SPEC-008-prompt-v0.1-review.md) | Informs — PE review findings driving design decisions |
| [Query_Report1.md](../references/Query_Report1.md) | Test output — v0.2 query report artifact |
| [Research_Report1.md](../references/Research_Report1.md) | Test output — v0.2 research report artifact |
| [public_health_trending_topics_april2026.md](../references/public_health_trending_topics_april2026.md) | Baseline — instructor's barebones prompt and output for comparison |
| [Compass artifact](../references/compass_artifact_wf-13120d19-5bce-4e73-9fff-357d7def829e_text_markdown.md) | Informs — free-tier platform capabilities and constraints |

---

## 1. Overview

### 1.1 Design Summary

The prompt is architected as a five-phase conversational pipeline: Orient → Gather → Plan → Research → Deliver, followed by a Closing block. Each phase has an explicit gate — the conversation cannot advance until the user signals approval at the two critical junctures (gathering confirmation and query report approval). The prompt's primary engineering challenge is controlling Sonnet 4.6's default behaviors (batching questions, paraphrasing sources, skipping verification) through structural constraints embedded in natural language, while remaining readable to a non-technical user who will see the prompt text before pasting it.

The v0.2 prototype established the phase architecture and was tested live against a public health trending topics query. The test confirmed that Sonnet produces both artifacts in the artifact panel, follows the gathering and planning flow, uses direct quotations, verifies links via web search, and generates a genuinely useful Problem Log. The design refines v0.2 based on observed issues: unsolicited editorial sections, Wikipedia used without distinction from primary sources, and generic landing page URLs cited instead of specific articles.

### 1.2 Design Principles

- **Structure over prohibition** — Control behavior through how output is organized, not through "don't do X" instructions
- **Show your work over self-assessment** — Produce auditable evidence rather than pass/fail claims
- **Chain-ready over publication-ready** — Output must be usable as direct input to the next prompt, not polished for final delivery
- **Front-load for smooth execution** — Invest tokens upfront in behavioral specificity to reduce mid-conversation confusion

### 1.3 Requirements Coverage

| Requirement | Design Section | Approach |
|-------------|----------------|----------|
| REQ-F1 (single paste, no mods) | All components | Prompt is one self-contained text block |
| REQ-F2 (one-at-a-time gathering) | COMP-2 | Sequential prose questions, not numbered list (DEC-1) |
| REQ-F3 (two artifacts) | COMP-3, COMP-5 | Separate artifact panel documents |
| REQ-F4 (all instructions inline) | All components | No external file references |
| REQ-F5 (fits 200K context) | REQ-N2 | Prompt under 6000 tokens |
| REQ-F6 (direct quotes, correct links) | COMP-4 | Positive framing: "quote directly," link verification by title+org search |
| REQ-F7 (web search verification) | COMP-4 | Concrete mechanism: search title + source org (DEC-8) |
| REQ-F8 (self-check / problem log) | COMP-5 | Problem Log replaces self-assessment (DEC-2) |
| REQ-F9 (minimize summarization) | COMP-4 | "Keep the specifics" positive framing (DEC-4) |
| REQ-F10 (dual-audience language) | All components | AI reads instructions, user reads output |
| REQ-F11 (leverage free-tier features) | COMP-4 (web search), COMP-3/5 (artifacts) | Used when available, not depended on |
| REQ-F12 (query report) | COMP-3 | Artifact with search strategy, error handling, fixed limitations text |
| REQ-F13 (separate artifacts) | COMP-3, COMP-5 | Independent verification per lethal trifecta (DEC-9) |
| REQ-N1 (no experience needed) | COMP-1, COMP-2 | Scripted orientation, conversational gathering |
| REQ-N2 (under 4000-6000 tokens) | All | Token budget managed via implementation |
| REQ-N3 (natural conversation) | COMP-1, COMP-2, COMP-6 | Tone directive (DEC-7), one-at-a-time pacing |
| REQ-N4 (expert-quality output) | COMP-4, COMP-5 | Structural constraints produce verifiable, source-backed research |

---

## 2. Architecture

### 2.1 System Context

```
┌──────────────┐
│  User pastes  │
│    prompt     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   ORIENT     │ → Scripted opening message
│   (COMP-1)   │   (what this produces, how it works)
└──────┬───────┘
       │ automatic
       ▼
┌──────────────┐
│   GATHER     │ → Sequential questions, one per message
│   (COMP-2)   │   (topic, audience, timeframe, geography, other)
└──────┬───────┘
       │ user confirms summary (INT-2)
       ▼
┌──────────────┐
│    PLAN      │ → Query Report artifact
│   (COMP-3)   │   (search strategy, source priority, error handling)
└──────┬───────┘
       │ user approves (INT-3)
       ▼
┌──────────────┐
│  RESEARCH    │ → Web search + source collection
│   (COMP-4)   │   (direct quotes, link verification, problem logging)
└──────┬───────┘
       │ automatic
       ▼
┌──────────────┐
│   DELIVER    │ → Research Report artifact + Problem Log
│   (COMP-5)   │   (findings by section, source list, issues encountered)
└──────┬───────┘
       │ automatic
       ▼
┌──────────────┐
│    CLOSE     │ → Offer to expand, add sources, or revise
│   (COMP-6)   │
└──────────────┘
```

### 2.2 Architecture Pattern

**Pattern:** Sequential Pipeline with Gates

The prompt operates as a linear pipeline where each phase produces a specific output and requires user approval before the next phase begins at two critical junctures. This is the simplest architecture that satisfies the requirements — no branching, no parallel paths, no conditional logic beyond minor follow-ups during gathering.

**Trade-offs:**
- Pros: Simple, predictable, easy for non-technical users to follow, minimal token overhead for flow control
- Cons: No mid-research checkpoints (could lose work if session limit hit), no ability to loop back to gathering without restarting

### 2.3 Technology Choices

| Concern | Choice | Rationale |
|---------|--------|-----------|
| Model | Sonnet 4.6 (free tier) | Only option on free tier; confirmed capable of web search, artifacts, extended conversations |
| Output format | Markdown artifacts in Claude.ai artifact panel | Downloadable, readable, chain-ready as input to next prompt |
| Citation format | Numbered source list grouped by section, no IEEE | Dropped IEEE — too complex for Sonnet to execute reliably. Focus is correct link → correct content (DEC-3) |
| Verification | Web search for title + org confirmation | Sonnet can't HTTP GET URLs; searching for article title + source org is the feasible verification mechanism (DEC-8) |
| Gathering control | Sequential prose, not numbered list | PE review confirmed numbered lists cause batching (DEC-1) |

---

## 3. Components

### COMP-1: Orientation Block

**Purpose:** Scripted opening message that tells the user what this process produces and how it works before any questions are asked.

**Satisfies:** REQ-F1, REQ-N1, REQ-N3

**Responsibilities:**
- Deliver a fixed opening message (not improvised by Sonnet) explaining: two artifacts will be produced, a few questions will be asked first, the user controls the pace
- Set conversational tone for the session
- Transition directly into first gathering question

**Dependencies:** None — this is the entry point

---

### COMP-2: Gathering Sequence

**Purpose:** Collect research parameters from the user through one-at-a-time conversational questions.

**Satisfies:** REQ-F2, REQ-N1, REQ-N3

**Responsibilities:**
- Ask five questions in sequence: topic, audience, timeframe, geography, open-ended
- One question per message, wait for response before next
- Allow one follow-up if an answer is very broad, then accept what's given
- Accept skips without pushback
- Summarize understanding in 2-3 sentences and ask for confirmation before proceeding

**Key Design Decisions:**
- Questions written as sequential prose, not a numbered list — prevents Sonnet from batching (DEC-1)
- "One follow-up allowed" balances "accept whatever" with "draw out specifics" (PE finding #4)

**Dependencies:** COMP-1 (orientation must complete first)

---

### COMP-3: Query Report Generator

**Purpose:** Produce the first artifact — a search plan the user can audit and the AI can use as in-context self-reference during research.

**Satisfies:** REQ-F3, REQ-F12

**Responsibilities:**
- Create a markdown document in the artifact panel containing: research question, scope, search strategy with specific terms, source priority, output structure with section headings, error handling plan for four scenarios, limitations statement
- The limitations statement is fixed text embedded in the prompt (not improvised) (DEC-5)
- Wait for user approval; if changes requested, revise and re-present; if research question changes, return to gathering (COMP-2)

**Key Design Decisions:**
- Error handling is pre-committed, not reactive — Sonnet writes its plan for dead links, contradictions, unverifiable claims, and insufficient sources before encountering them
- Output structure section defines the Research Report's headings, creating a contract between the two artifacts

**Dependencies:** COMP-2 (gathering must complete and be confirmed)

---

### COMP-4: Research Engine

**Purpose:** Execute web searches, collect sources, and build findings with direct quotations and verified links.

**Satisfies:** REQ-F6, REQ-F7, REQ-F9

**Responsibilities:**
- Use web search for every claim — do not rely on training data alone
- Quote directly from sources; describe only when quoting isn't possible
- Present each source's findings separately — one source per block, attributed
- Preserve all specifics exactly as stated (numbers, names, dates)
- Verify each link by searching for article title + source organization; mark unconfirmed links
- Follow the error handling plan written in the Query Report
- Stick to the section headings defined in the Query Report — do not add sections not defined there

**Key Design Decisions:**
- "One source per block" is a structural constraint replacing "do not synthesize" — positive framing (DEC-4)
- "Keep the specifics" replaces "do not summarize" — positive framing (DEC-4)
- Link verification mechanism is explicitly "search for title + org" not "verify the URL" — matches what Sonnet can actually do (DEC-8)

**Dependencies:** COMP-3 (query report must be approved)

---

### COMP-5: Research Report Generator

**Purpose:** Produce the second artifact — structured findings with source list and problem log.

**Satisfies:** REQ-F3, REQ-F13, REQ-F8, REQ-F9

**Responsibilities:**
- Create a separate markdown document in the artifact panel
- Organize findings by the section headings defined in the Query Report
- Each finding includes: the information (quoted where possible), source name/org, URL
- Source list at the end grouped by report section
- Problem Log section listing: unconfirmed links, contradictions presented, missing sources, instances where summary was used instead of direct quote and why, any sections where Wikipedia or other secondary/aggregation sources were used

**Key Design Decisions:**
- Problem Log replaces self-assessment — "show what happened" not "did I do well" (DEC-2)
- Source list grouped by section supports downstream verification — a verifier can check one section at a time
- Explicit separation from Query Report enforces independent verification per lethal trifecta (DEC-9)

**Dependencies:** COMP-4 (research must be complete)

---

### COMP-6: Closing Block

**Purpose:** End the conversation productively with options for follow-up.

**Satisfies:** REQ-N3

**Responsibilities:**
- After delivering the Research Report, ask if the user wants to expand any section, search for additional sources, or revise anything
- Do not offer unsolicited next steps beyond these three options

**Dependencies:** COMP-5 (research report must be delivered)

---

## 4. Interfaces

### INT-1: Orient → Gather

**Connects:** COMP-1 → COMP-2

**Type:** Automatic

**Direction:** Unidirectional

**Contract:** Orientation message is delivered, then first gathering question is asked in the same message. No user action required to trigger this transition.

---

### INT-2: Gather → Plan (User Gate)

**Connects:** COMP-2 → COMP-3

**Type:** User-gated

**Direction:** Unidirectional (with possible loop back to COMP-2)

**Contract:** After the final gathering question is answered, Sonnet restates its understanding in 2-3 sentences and asks the user to confirm. User must explicitly confirm before the Query Report is generated. If user corrects the summary, Sonnet updates and re-confirms.

---

### INT-3: Plan → Research (User Gate)

**Connects:** COMP-3 → COMP-4

**Type:** User-gated

**Direction:** Unidirectional (with possible loop back to COMP-2)

**Contract:** Query Report artifact is created in the artifact panel. Sonnet tells the user it is ready for review and waits. User must explicitly approve. If user requests changes, Sonnet revises the artifact and re-presents. If user wants to change the research question entirely, Sonnet returns to COMP-2 (gathering). Research does not begin until approval.

---

### INT-4: Research → Deliver

**Connects:** COMP-4 → COMP-5

**Type:** Automatic

**Direction:** Unidirectional

**Contract:** Research findings are compiled into the Research Report artifact including the Problem Log. No separate user gate — the research phase flows directly into artifact creation.

---

### INT-5: Deliver → Close

**Connects:** COMP-5 → COMP-6

**Type:** Automatic

**Direction:** Unidirectional

**Contract:** After the Research Report artifact is created, Sonnet offers three follow-up options: expand a section, search for additional sources, or revise. User can engage or end the conversation.

---

**Gate design rationale (DEC-6):** Exactly two user gates. These prevent the two costliest errors: researching the wrong topic (INT-2) and researching the wrong way (INT-3). Additional gates would consume messages against the session limit.

---

## 5. Data Model

### DATA-1: Query Report Artifact

**Purpose:** User-auditable research plan and in-context self-reference for the AI during research

**Used by:** COMP-3 (generates it), COMP-4 (references it during research)

| Field | Required | Description |
|-------|----------|-------------|
| Research Question | Yes | Restated from gathering, confirmed by user |
| Scope | Yes | Audience, timeframe, geography |
| Search Strategy | Yes | Specific search terms, order of searches, rationale |
| Source Priority | Yes | Starting institutions + any user-specified sources |
| Output Structure | Yes | Section headings for the Research Report — defines the contract |
| Error Handling | Yes | Pre-committed plan for: dead links, contradictions, unverifiable claims, insufficient sources |
| Limitations Statement | Yes | Fixed text — AI-generated, must be independently verified |

---

### DATA-2: Research Report Artifact

**Purpose:** Structured findings with full source traceability, chain-ready as input to verification prompt

**Used by:** COMP-5 (generates it), downstream prompt chains (consumes it)

| Field | Required | Description |
|-------|----------|-------------|
| Title and Scope | Yes | Carried from Query Report |
| Findings | Yes | Organized by section headings from Query Report. Each finding: quoted content, source name/org, URL |
| Source List | Yes | All sources grouped by report section. Each entry: org/author, page title, URL |
| Problem Log | Yes | Unconfirmed links, contradictions presented, missing sources, summaries used instead of quotes (with reason), secondary/aggregation sources noted |

**Key constraint:** The Research Report must be parseable by a new conversation with no additional context. A person or AI reading just this artifact should be able to identify every claim, its source, and whether the link was confirmed.

---

## 6. Design Decisions

### DEC-1: Sequential Prose Over Numbered Question List

**Context:** PE review found that Sonnet batches questions when it can see a numbered list.

**Decision:** Write gathering questions as sequential prose ("First ask X. After I respond, ask Y.") rather than a visible numbered list.

**Rationale:** Structural prevention is more reliable than behavioral instruction. Sonnet can't batch what it doesn't see as a list.

**Alternatives Considered:**
- Numbered list with stronger "one at a time" instruction: Weaker — fights model default behavior
- Hiding questions entirely: Sacrifices dual-use readability for the human who sees the prompt before pasting

---

### DEC-2: Problem Log Over Self-Assessment

**Context:** PE review identified self-check as theater — "did you mess up?" reliably gets "no."

**Decision:** Replace pass/fail self-check with a Problem Log that shows what happened: unconfirmed links, contradictions, summaries used, sources not found.

**Rationale:** "Show your work" produces auditable evidence. "Grade your work" produces false confidence.

**Alternatives Considered:**
- Keep self-check with more specific questions: Still self-assessment — same failure mode
- Drop self-check entirely: Loses the only in-conversation quality signal

---

### DEC-3: Drop IEEE Citation Format

**Context:** IEEE in-text citations with hyperlinked reference numbers add complexity. Internal anchor links may not render in Claude.ai's artifact viewer.

**Decision:** Use a simple numbered source list grouped by report section. No in-text citation numbers. Each finding is attributed inline by source name.

**Rationale:** The goal is right link → right content, not publication formatting. Citation formatting is a downstream prompt's job. Grouping sources by section gives verifiers a clear audit path.

**Alternatives Considered:**
- IEEE with anchor links: May not render; adds token cost for formatting instructions
- IEEE without anchor links: Numbered references still require Sonnet to maintain consistent numbering across a long document — fragile

---

### DEC-4: Positive Structure Over Negative Prohibition

**Context:** PE review flagged "do not synthesize" and "do not summarize" as elephants — priming the behavior they prohibit.

**Decision:** Replace all "don't do X" research rules with structural instructions: "one source per block," "keep the specifics," "quote directly."

**Rationale:** Telling the model how to organize eliminates the need to tell it what to avoid.

**Alternatives Considered:**
- Keep prohibitions alongside positive instructions: Redundant at best, counterproductive at worst

---

### DEC-5: Fixed Limitations Statement

**Context:** The lethal trifecta requires that AI output not be trusted without independent verification.

**Decision:** The limitations statement in the Query Report is fixed text embedded in the prompt, not generated by Sonnet.

**Rationale:** Sonnet may soften, hedge, or omit a self-generated disclaimer. A fixed string ensures the warning is always present and always says what it needs to say.

**Alternatives Considered:**
- Let Sonnet generate the disclaimer: Risk of watering it down or omitting it

---

### DEC-6: Two User Gates, No More

**Context:** More approval gates increase user control but slow the conversation in a session-limited environment.

**Decision:** Exactly two gates — gathering confirmation (INT-2) and query report approval (INT-3). Research and delivery flow automatically.

**Rationale:** These two gates prevent the two costliest errors: researching the wrong topic and researching the wrong way. Additional gates would consume messages against the session limit.

**Alternatives Considered:**
- Mid-research checkpoint: Costs messages; Sonnet would need to pause artifact creation mid-stream
- No gates (fully automatic): User loses control; spec requires approval steps

---

### DEC-7: Tone Directive

**Context:** PE review noted Sonnet's default persona varies by session — sometimes chatty, sometimes robotic.

**Decision:** Add a brief tone line: conversational and brief during gathering, precise and formal in reports.

**Rationale:** One sentence of tone guidance produces consistent sessions. Without it, the prompt's user experience is partially random.

**Alternatives Considered:**
- Detailed persona description: Overkill for a prompt this size; burns tokens for marginal improvement

---

### DEC-8: Link Verification Scoped to Link-Content Match

**Context:** Sonnet can't HTTP GET URLs. The prompt's job is interaction and web search, not self-verification of factual accuracy.

**Decision:** Verification means: search for article title + source organization, confirm the URL appears in results pointing to that content. Factual accuracy verification is explicitly out of scope — that's the user's job in a separate conversation.

**Rationale:** Matches what Sonnet can actually do. Separates link correctness (achievable) from truth verification (not achievable by the same agent per lethal trifecta).

**Alternatives Considered:**
- Full fact-checking in the same conversation: Violates lethal trifecta
- No verification at all: Produces unreliable links

---

### DEC-9: Separate Artifacts for Independent Verification

**Context:** The lethal trifecta requires that untrusted output cannot serve as trusted input without external verification.

**Decision:** Query report and research report are separate artifacts so each can be verified independently in separate conversations before being used downstream.

**Rationale:** If both were in one document, verifying intent vs. evidence would be tangled. Separation creates clean verification targets.

**Alternatives Considered:**
- Single combined artifact: Faster to produce, but conflates verifiable intent with verifiable evidence

---

### DEC-10: Domain-Flexible with Public Health Defaults

**Context:** First test is public health (BSI internship). Hardcoding source defaults reduces gathering burden.

**Decision:** Default source list includes CDC, WHO, NIH, state health departments. Prompt also instructs Sonnet to expand based on user guidance. Source priority in Query Report adjusts per topic.

**Rationale:** Good defaults for the target use case. "Expand based on guidance" keeps it flexible.

**Alternatives Considered:**
- Fully domain-agnostic: User must specify sources from scratch every time
- Separate prompt per domain: Premature — test one first, generalize later

---

### DEC-11: Prompt Brevity as Session Limit Mitigation

**Context:** Free-tier session limits are unpublished and dynamic. No programmatic recovery.

**Decision:** Maximize specificity while minimizing language. No prompt-level recovery feature. Test empirically and iterate.

**Rationale:** Every token saved is a token available for research. The unpublished message count limit is the real constraint.

**Alternatives Considered:**
- Recovery instructions: Adds complexity for an untestable edge case

---

## 7. Implementation Considerations

### 7.1 Implementation Order

| Order | Component | Dependencies | Notes |
|-------|-----------|--------------|-------|
| 1 | COMP-1 Orientation Block | None | Write the fixed opening message — sets tone |
| 2 | COMP-2 Gathering Sequence | COMP-1 | Sequential prose questions, one follow-up rule, confirmation summary |
| 3 | COMP-3 Query Report Generator | COMP-2 | Artifact structure, fixed limitations text, error handling scenarios |
| 4 | COMP-4 Research Engine | COMP-3 | Positive-framing research rules, link verification mechanism |
| 5 | COMP-5 Research Report Generator | COMP-4 | Artifact structure, source list grouping, Problem Log template |
| 6 | COMP-6 Closing Block | COMP-5 | Three follow-up options |
| 7 | Tone directive | All | Cross-cutting — add last once full prompt reads naturally |
| 8 | Token audit | All | Measure final prompt, trim if over 6000, add specificity if under 4000 |

### 7.2 Risk Areas

| Risk | Impact | Mitigation |
|------|--------|------------|
| Sonnet batches gathering questions despite sequential prose | Gathering phase collapses, user overwhelmed | DEC-1 mitigates structurally; reinforcement at "Start Now" section; test and strengthen if needed |
| Sonnet paraphrases instead of quoting | Output loses traceability | DEC-4 positive framing; Problem Log catches instances |
| Session limit hit mid-research | Incomplete Research Report, lost work | DEC-11 keeps prompt lean; test to determine typical conversation depth |
| Sonnet doesn't use artifact panel | Output is inline chat, not downloadable | Explicit "in the artifact panel" instruction in COMP-3 and COMP-5 |
| Sonnet claims link verification without searching | False confidence in source quality | DEC-8 specifies concrete mechanism; Problem Log forces disclosure |
| Fixed limitations text gets paraphrased or dropped | User misses verification warning | Embed as quoted block with "include this text exactly" |
| User gives extremely vague topic | Query Report is too broad, research sprawls | One follow-up allowed; Query Report approval gate catches bad scope |
| Sonnet adds unsolicited editorial sections | Unrequested synthesis (observed in v0.2 test) | Instruct to stick to section headings defined in Query Report |
| Generic landing page URLs cited instead of specific articles | Links don't point to actual source content | Instruct that every URL must point to a specific page, not a homepage or section landing |

### 7.3 Testing Strategy

| Level | Approach | Covers |
|-------|----------|--------|
| Smoke test | Paste into fresh free-tier conversation, answer minimally, verify both artifacts appear in artifact panel | REQ-F1, F3, F12, F13, AC-1, AC-7 |
| Gathering pacing | Test one-at-a-time across 3+ sessions | REQ-F2, AC-2, DEC-1 |
| Source quality | Check 5+ URLs — do they point to correct content? | REQ-F6, F7, AC-3 |
| Quote fidelity | Compare 3+ quotations against actual source text | REQ-F9 |
| Problem Log honesty | Verify Problem Log entries match observable issues | REQ-F8, AC-4, DEC-2 |
| Non-technical user test | Someone unfamiliar with prompt engineering completes full flow | REQ-N1, N3, AC-5 |
| Token measurement | Count prompt tokens, verify under 6000 | REQ-N2, AC-6 |
| Session viability | Complete full flow, note message count vs typical limits | Constraint 6.1 |
| Chain readiness | Paste Research Report into new conversation, ask to verify claims — sufficient context? | REQ-F13, DATA-2 |
| Baseline comparison | Compare output quality against instructor's barebones prompt output | REQ-N4 |

### 7.4 Security Considerations

- The prompt produces AI-generated content that must not be treated as verified — fixed limitations statement (DEC-5) addresses this
- No sensitive data flows through the prompt — it searches public sources only
- The lethal trifecta separation (DEC-9) is the primary security mechanism — output is not trusted until independently verified in a separate session

---

## 8. Out of Scope

**From Specification (inherited):**
- Integration into Praxisity as a skill or command
- Multi-conversation workflows (prompt completes in one session)
- Paid-tier features (Research mode, Opus, Claude Code, Cowork)
- Automated verification pipelines or sub-agent orchestration
- Custom UI or delivery mechanism beyond copy-paste
- Prompt generation tooling
- Specific domain content beyond default public health source list

**Design-Specific Exclusions:**
- Publication-ready citation formatting (IEEE, APA, etc.) — downstream prompt's job (DEC-3)
- Factual claim verification — separate conversation per lethal trifecta (DEC-8)
- Complete suppression of all synthesis — v0.2 test showed Sonnet adds editorial sections even with structural constraints; tightening can reduce but not eliminate without excessive instruction weight
- Wikipedia source filtering — v0.2 used Wikipedia for aggregation; blocking it loses useful context; flagging as secondary source is the better approach

---

## 9. Open Questions

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| DQ-1 | Should the prompt explicitly instruct Sonnet to avoid editorial sections? | Open | v0.2 test showed "Public Health Relevance" sections added without request. Preferred fix: "Stick to the section headings defined in the Query Report — do not add sections not defined there." Avoids elephant problem. |
| DQ-2 | Should Wikipedia be flagged differently from primary sources? | Open | v0.2 used Wikipedia for protest counts and war timeline. Useful but not authoritative. Candidate instruction: "If using Wikipedia, note it as a secondary/aggregation source in the Problem Log." |
| DQ-3 | How should the prompt handle generic landing page URLs? | Open | v0.2 cited NPR homepage twice. Candidate instruction: "Every URL must point to a specific page, not a homepage or section landing page." |

---

## 10. Appendices

### A. Glossary

| Term | Definition |
|------|------------|
| Lethal trifecta | Security principle: AI output cannot be trusted as input to the next stage without independent verification by a separate agent or human |
| Prompt chaining | Using the output of one AI conversation as structured input to another |
| Artifact panel | Claude.ai's side panel for creating downloadable documents, code, and visualizations |
| Problem Log | A factual record of issues encountered during research, replacing self-assessment |
| Query Report | First artifact — the research plan, auditable by user, self-referencing for the AI |
| Research Report | Second artifact — structured findings with sources and Problem Log |

### B. References

- [SPEC-008: Portable Research Prompt](../specs/008-portable-research-prompt.md)
- [PE Review of v0.1](../reviews/SPEC-008-prompt-v0.1-review.md)
- [v0.2 Prototype](../references/portable-research-prompt-v0.2.md)
- [v0.2 Test: Query Report](../references/Query_Report1.md)
- [v0.2 Test: Research Report](../references/Research_Report1.md)
- [Instructor Baseline](../references/public_health_trending_topics_april2026.md)
- [Free-tier Capabilities Research](../references/compass_artifact_wf-13120d19-5bce-4e73-9fff-357d7def829e_text_markdown.md)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-04-09 | Andrew | Initial draft via /architect with v0.2 test data |