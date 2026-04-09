# Specification: [SPEC-008] Portable Research Prompt

## Metadata

| Field | Value |
|-------|-------|
| Spec ID | SPEC-008 |
| Title | Portable Research Prompt for Free-Tier Claude.ai |
| Status | Draft |
| Author | Andrew |
| Created | 2026-04-08 |
| Last Updated | 2026-04-08 |
| Charter Reference | CHARTER.md — Bootstrapping Principle, Principle 6 (dual-use design) |

### Related Documents

| Document | Relationship |
|----------|--------------|
| Compass artifact (free-tier research) | Informs — platform capabilities and constraints |
| Second brain architecture (memory reference) | Informs — lethal trifecta verification model |
| SPEC-004 (skills and patterns) | Related to — prompt embodies skill patterns in portable form |

---

## 1. Problem Statement

Non-technical users have access to powerful free AI tools (Claude.ai free tier with Sonnet 4.6) but lack the prompt engineering knowledge to get structured, high-quality output from them. The gap isn't capability — free-tier Claude can do web search, code execution, file creation, and deep analysis — it's that users don't know how to direct the conversation. Meanwhile, prompt chaining techniques that could guide users through complex workflows exist but are locked inside developer tooling (Claude Code skills, MCP servers, custom slash commands) that require paid plans and technical setup. There is no accessible way for an inexperienced user to paste a single prompt and get a structured, multi-turn guided experience that draws expert-quality output from them without them needing to know what to ask.

---

## 2. Goals and Objectives

### 2.1 Primary Goal

Define a portable, self-contained prompt format that transforms a single paste into Claude.ai's free tier into a structured, multi-turn guided workflow — producing expert-quality output from non-technical users.

### 2.2 Objectives

| ID | Objective | Success Metric |
|----|-----------|----------------|
| OBJ-1 | A non-technical user can copy-paste the prompt and immediately begin a guided workflow with no setup or instructions beyond the prompt itself | User produces structured output on first attempt without external help |
| OBJ-2 | The prompt embeds all gathering, structuring, and output generation behavior — no external files, tools, or references required | Prompt functions identically in a fresh Claude.ai free-tier conversation with no prior context |
| OBJ-3 | The guided conversation draws domain-relevant detail from the user without requiring them to know what to provide upfront | Output contains specifics the user didn't know to volunteer, surfaced through the prompt's questioning strategy |
| OBJ-4 | Establish a reusable pattern for creating additional portable prompts across different domains | Second prompt created from the pattern takes less than half the effort of the first |

---

## 3. Requirements

### 3.1 Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-F1 | The prompt shall be a single block of text that can be pasted into a fresh Claude.ai free-tier conversation with no modifications | MUST | Zero-setup is the entire value proposition |
| REQ-F2 | The prompt shall guide the user through structured information gathering one topic at a time, waiting for responses before proceeding | MUST | Non-technical users get overwhelmed by multi-part asks |
| REQ-F3 | The prompt shall instruct the AI to produce two specific artifacts: a query report and a research report | MUST | The conversation must converge on concrete, verifiable outputs designed for downstream prompt chaining |
| REQ-F4 | The prompt shall embed all behavioral instructions (tone, pacing, gathering strategy, output format) inline — no references to external files or tools | MUST | Free-tier Claude.ai has no file system, no skills, no project context |
| REQ-F5 | The prompt shall work within Sonnet 4.6's 200K token context window, leaving substantial room for the multi-turn conversation that follows | MUST | Prompt can't consume a large portion of the available context |
| REQ-F6 | Output shall include direct quotations from sources with IEEE-style in-text citations (e.g., [1], [2]) that hyperlink to the correct reference. Each citation must point to the actual source for the claim it supports | MUST | Traceability and robustness of evidence. IEEE style avoids the web client's tendency to misplace inline hyperlinks |
| REQ-F7 | The AI shall use web search to confirm that each hyperlink in the references section points to the correct page or resource for the information being cited | MUST | Free tier can search but not sub-agent; the prompt's verification scope is link-to-source correctness, not independent fact-checking |
| REQ-F8 | The prompt shall include a self-check protocol — instructions for the AI to audit its own draft for mismatched citations (wrong link for a given claim) and unsupported synthesis. The prompt must explicitly state that self-verification of factual accuracy is outside the prompt's scope; that is the user's responsibility in a separate conversation | MUST | The prompt interacts with the user and the outside world (via web search) but should not be trusted to verify its own work — per the lethal trifecta principle: untrusted output cannot serve as trusted input without independent external verification |
| REQ-F9 | Minimize summarization; preserve original source language and specifics. Limit synthesis to only where the user explicitly requests it | MUST | Accuracy and traceability over polish |
| REQ-F10 | Dual-audience language: precise prompt engineering for AI, accessible language for user-facing output | SHOULD | Prompt is read by AI; output is read by user |
| REQ-F11 | Leverage free-tier capabilities (web search, code execution, artifacts) when they improve output quality | COULD | Available but prompt must not depend on them |
| REQ-F12 | After gathering, the AI shall produce a Query Report artifact describing the planned search strategy, output structure, and error handling before beginning research | MUST | User-auditable plan and in-context self-reference. Must be independently verifiable in a separate conversation per the lethal trifecta principle: an AI system's output cannot be trusted as input to the next stage without independent verification by a separate agent or human. The query report and research report are separated so each can be verified independently before being used downstream |
| REQ-F13 | The research output shall be a separate markdown artifact from the query report | MUST | Separation enforces independent verification of intent (query report) and evidence (research report) in separate conversations before either can be trusted as input to downstream prompt chains |

### 3.2 Non-Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-N1 | The prompt shall be usable by someone with no prompt engineering experience — the user's only action is paste and respond to questions | MUST | Target audience is non-technical |
| REQ-N2 | The prompt text should be under ~4000 tokens, with flexibility up to 6000 if the additional instruction weight demonstrably improves conversation quality and reduces mid-session confusion | SHOULD | Front-loading behavior pays off across the entire conversation; 200K context can absorb it |
| REQ-N3 | The prompt's gathering strategy shall feel like a natural conversation, not an interrogation or form-filling exercise | SHOULD | User engagement depends on not feeling like they're being processed |
| REQ-N4 | Output quality should be comparable to what an experienced prompt engineer would produce through manual iteration | SHOULD | The whole point is closing the skill gap |

---

## 4. User Stories / Use Cases

### UC-1: First-time user pastes a research prompt

**Actor:** Non-technical user (e.g., public health intern)

**Preconditions:**
- User has a Claude.ai free account and an open conversation
- User has a copy of the prompt (received from supervisor, collaborator, or downloaded)

**Flow:**
1. User pastes the prompt into the chat box and sends it
2. Claude responds with an opening message that orients the user — what this will produce, roughly how long it will take, and the first gathering question
3. User answers each question in turn; Claude asks follow-ups only where needed
4. After gathering is complete, Claude signals it's moving to drafting and produces the Query Report artifact — describing the planned search strategy, output structure, and error handling
5. User reviews and approves the query report before research begins
6. Claude executes the research with inline source verification via web search, producing the Research Report artifact with direct quotations and verified links
7. Claude runs the self-check protocol, flagging any unverified claims or links
8. User receives both artifacts as downloadable markdown files

**Postconditions:**
- User has two separate artifacts: a query report (verifiable intent) and a research report (verifiable evidence)
- Both artifacts are designed for use as input to downstream prompt chains

**Alternative Flows:**
- User gives very short answers → Claude draws out specifics through targeted follow-ups without being pushy
- User provides a file upload alongside the prompt → Claude incorporates the uploaded material as source context
- Web search returns a dead link → Claude flags it explicitly rather than silently dropping the source

---

## 5. Acceptance Criteria

| ID | Criterion | Validates |
|----|-----------|-----------|
| AC-1 | Given a fresh free-tier Claude.ai conversation, when the prompt is pasted with no other context, then Claude begins the gathering flow without error or confusion | REQ-F1, REQ-F4 |
| AC-2 | Given the gathering phase, when Claude asks questions, then it asks one topic at a time and waits for the user's response before proceeding | REQ-F2 |
| AC-3 | Given the drafting phase, when Claude includes a factual claim, then it provides a direct quotation with an IEEE-style in-text citation that hyperlinks to the correct reference entry | REQ-F6, REQ-F7 |
| AC-4 | Given a completed draft, when Claude runs the self-check protocol, then it explicitly lists any citation-to-link mismatches and any synthesis it performed without explicit user request. It does not claim to have verified factual accuracy | REQ-F8, REQ-F9 |
| AC-5 | Given a non-technical user with no prompt engineering experience, when they paste and respond conversationally, then they produce both artifacts without needing external instructions | REQ-N1, REQ-N3 |
| AC-6 | Given the full prompt text, when measured, then it is under 6000 tokens | REQ-N2 |
| AC-7 | Given the completed conversation, when artifacts are examined, then the query report and research report are separate downloadable markdown artifacts | REQ-F12, REQ-F13 |

---

## 6. Constraints

### 6.1 Platform Constraints

- Sonnet 4.6 only — no model selection on free tier
- 200K token context window (not the 1M API window)
- Session usage limit resets every 5 hours — complex prompts may hit this mid-conversation
- No Research mode, no sub-agents, no Claude Code, no Claude Cowork
- Web search available but counts against usage limits
- No persistent memory between conversations (memory exists but can't be relied on for the prompt's function)

### 6.2 Spec-Specific Constraints

- The prompt must be fully self-contained — no companion files, no setup instructions, no "first do X"
- Cannot use any tool or feature that requires a paid plan
- The prompt is the only engineering surface — all behavioral shaping must happen in the initial message
- Verification must happen inline via web search, not via a separate automated pass

---

## 7. Dependencies

### 7.1 Depends On

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| Claude.ai free tier with Sonnet 4.6 | External | Available | Platform must continue offering web search, artifacts, and code execution on free tier |
| Web search capability on free tier | External | Available | Required for inline source verification — if removed, REQ-F7 breaks |

### 7.2 Enables

| Dependent | Relationship |
|-----------|--------------|
| Future Praxisity research sub-agent | This prompt pattern is a prototype for the portable research workflow the sub-agent will automate |
| BSI internship deliverables | Direct use case — prompt will be used to produce internship work product |
| Framework prompt-chaining pattern library | First validated example of a self-contained portable prompt; informs future prompts in other domains |

---

## 8. Out of Scope

The following are explicitly NOT part of this specification:

- Integration into Praxisity as a skill or command — this is a standalone deliverable; framework integration is a future decision
- Multi-conversation workflows — the prompt must complete its work within a single conversation session
- Paid-tier features (Research mode, Opus, Claude Code, Cowork) — the prompt must function on free tier only
- Automated verification pipelines or sub-agent orchestration — verification happens inline via single-thread web search
- Custom UI, browser extensions, or any delivery mechanism beyond copy-paste
- Prompt generation tooling — this spec covers one prompt; a generator/templating system is future work
- Specific domain content — the spec defines the prompt format and behavior, not the subject matter of any particular prompt instance

---

## 9. Open Questions

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| Q-1 | How does the prompt handle hitting the free-tier session usage limit mid-conversation? | Resolved | Mitigate through prompt brevity — maximize specificity while minimizing language. Test empirically and report back for next iteration. Not a prompt-level recovery feature. |
| Q-2 | Should the query report artifact include estimated token/message budget? | Resolved | Desirable but not feasible for Sonnet to estimate accurately. Drop. |
| Q-3 | What specific domain will the first test prompt target? | Resolved | Broad public health topic scan — "top 5 public health topics in the news." Gathering surfaces: intended audience/stakeholder, timeframe (user-specified date range if applicable, e.g., 2018–2023), geography. Output is a query report + research report, not a final deliverable. Designed for downstream prompt chaining. First test will be built immediately following this spec as a BSI internship deliverable. |
| Q-4 | Should the prompt instruct the AI to prefer certain source types? | Resolved | Default to primary sources of good repute. Hardcode known examples (CDC, WHO, NIH, state health departments). Flex beyond those based on user guidance during gathering. |

---

## 10. References

- [Compass artifact: Claude free tier capabilities research](.plans/references/compass_artifact_wf-13120d19-5bce-4e73-9fff-357d7def829e_text_markdown.md) — Platform constraints and capabilities for free-tier Claude.ai
- Second brain architecture (project memory: reference_second_brain_architecture.md) — Lethal trifecta security model informing the verification separation pattern
- [CHARTER.md](../../CHARTER.md) — Project principles, specifically bootstrapping and "framework builds the user"

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-04-08 | Andrew | Initial draft via /gather |
| 0.2 | 2026-04-08 | Andrew | Spot check fixes: IEEE citation style, lethal trifecta defined inline, verification scope clarified, charter ref fixed, Q-3 timeline added |