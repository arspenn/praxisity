## Prompt Engineer Review

**Artifact:** `.plans/references/portable-research-prompt-v0.1.md`
**Spec:** `.plans/specs/008-portable-research-prompt.md`
**Date:** 2026-04-08
**Dispatch Mode:** Mode 1 (direct review)

## Instructions Received

Review the v0.1 portable research prompt for prompt engineering quality across 10 dimensions. The prompt will be copy-pasted by a non-technical user into a fresh Claude.ai free-tier conversation (Sonnet 4.6, 200K context, web search, no sub-agents). Must be completely self-contained. Expect it needs work; be thorough and specific.

---

## Findings

### 1. Elephants — "Do not synthesize unless I ask"

**Location:** Research Phase Rules, line 43
**The problem:** The instruction "Do not synthesize unless I ask" teaches Sonnet what synthesis IS and primes it to think about when synthesis might be appropriate. This is a textbook "don't think about elephants" instruction. In practice, Sonnet will now actively consider at each claim whether it's synthesizing, which paradoxically increases the likelihood of soft synthesis (combining framings, choosing which source to present first as if building an argument, etc.) and of over-flagging in the self-check.
**Why it matters:** The self-check protocol asks Sonnet to flag instances of unrequested synthesis. This creates a perverse incentive: Sonnet will either (a) flag nearly everything as potential synthesis to be safe, making the self-check noisy, or (b) rationalize that its blending of sources isn't really "synthesis" because it didn't draw an explicit conclusion, letting actual synthesis through.
**Fix:** Replace the negative instruction with a positive structural constraint. Instead of "do not synthesize," tell it how to organize:

> **One source at a time.** Present each source's findings in its own paragraph or block. Attribute every claim to its specific source. If I want you to compare or combine findings across sources, I will ask.

This achieves the same goal through structure rather than prohibition.

---

### 2. Elephants — "Do not summarize broadly"

**Location:** Research Phase Rules, line 45
**The problem:** Same class as above. "Do not round, generalize, or compress specifics into vague statements" tells Sonnet exactly what bad behavior looks like, which makes that behavior salient in its processing. Sonnet now has to actively resist summarizing at every turn, which is cognitively expensive and fragile.
**Fix:** Reframe as a positive instruction:

> **Keep the specifics.** When a source provides numbers, names, dates, or data points, include them exactly as stated. Specificity is more valuable than readability in this report.

---

### 3. Ambiguity — Gathering phase will collapse

**Location:** Gathering Phase, lines 12-21
**The problem:** The instruction says "Ask these questions one at a time" but then lists 5 specific questions. Sonnet 4.6 on free tier has a strong tendency to bundle questions when it can see the full list — it will often ask 2-3 at once to be "efficient," especially questions 3 and 4 (timeframe and geography) which feel like natural pairs. The instruction "one at a time" is fighting against the model's default helpfulness bias AND against the visible list of questions that makes batching trivially easy.
**Why it matters:** REQ-F2 and AC-2 require one-at-a-time pacing. This is one of the highest-risk requirements because it fights the model's default behavior.
**Fix:** Two changes needed:

(a) Remove the numbered list of questions from the prompt. Instead, embed the gathering logic as a sequence the model must follow, revealing each question only after the previous one:

> Ask me what I want to research. After I answer, ask about the intended audience. Then ask about timeframe. Then geography. Then anything else I should mention. One question per message. Do not preview upcoming questions.

(b) Add a reinforcement at the "Start Now" section:

> Begin by asking me the first question only. Do not list or preview the remaining questions.

The current structure where Sonnet can see all 5 questions at once is the primary failure mode for one-at-a-time pacing. However, fully hiding the questions means the user can't see them either, which conflicts with dual consumption — a non-technical user might want to know what's coming. This is a genuine tension the spec doesn't resolve. The fix above sacrifices user preview for behavioral reliability. An alternative is to keep the list visible but add a stronger behavioral lock:

> You can see the full list of gathering questions above. Ask them ONE AT A TIME. Send one question, wait for my response, then send the next. Never combine questions into a single message.

This is weaker but preserves readability. Test both.

---

### 4. Ambiguity — "Accept whatever I give you" is underspecified

**Location:** Gathering Phase, line 13
**The problem:** "Accept whatever I give you — short answers are fine. If I skip a question, move on." This doesn't address what happens when:
- The user gives a contradictory answer (e.g., "global scope" then later "just the US")
- The user gives an answer that doesn't match the question (misunderstands)
- The user gives an extremely vague topic like "health stuff"

The spec (UC-1 alternative flow) says "Claude draws out specifics through targeted follow-ups without being pushy" but the prompt doesn't instruct this behavior. "Accept whatever I give you" actively discourages follow-ups.
**Why it matters:** A non-technical user who says "I want to research health" and gets no follow-up will get a useless research report. The prompt's "accept whatever" instruction fights against the spec's "draw out specifics" requirement.
**Fix:** Replace with:

> Short answers are fine. If I skip a question, move on. If my answer is very broad, you may ask one follow-up to narrow the scope, then accept whatever I give.

---

### 5. Noise — Source Priority defaults are domain-locked

**Location:** Query Report, line 30
**The problem:** "Default starting points: CDC, WHO, NIH, state/national health departments, peer-reviewed journals" hardcodes a public health domain bias. The spec says (Section 8) the prompt should define "the prompt format and behavior, not the subject matter of any particular prompt instance." But the prompt itself bakes in health-specific sources. If someone uses this prompt for, say, educational policy research, the AI will default to searching CDC and WHO first.
**Why it matters:** The spec wants this to be domain-agnostic (REQ-F4: "all behavioral instructions inline"), but the prompt is domain-specific. This creates confusion — is it a research prompt or a public health research prompt?
**Fix:** Either:
(a) Own the domain specialization: rename to "Public Health Research Prompt" and lean into it, OR
(b) Make source priority dynamic:

> **Source Priority** — Primary sources from authoritative institutions first. Choose starting sources based on my research topic. Expand based on my guidance during gathering.

If the first test is intentionally public health (per Q-3), ship (a) for v0.1 but note that v0.2 should generalize.

---

### 6. Feasibility — IEEE citations with hyperlinked reference numbers

**Location:** Research Phase Rules, line 47
**The problem:** "Each citation number must hyperlink to the corresponding entry in the References section at the end." This asks Sonnet to produce markdown with internal anchor links — e.g., `[[1]](#ref-1)` — inside a Claude.ai artifact. Whether this renders correctly depends on the artifact viewer. Claude.ai's markdown artifact renderer may or may not support internal anchor links. If it doesn't, Sonnet will either:
- Produce `[1]` as plain text with no hyperlink (silently failing the requirement)
- Produce a broken `[1](#ref-1)` that displays as a link but goes nowhere
- Try to use HTML `<a>` tags which may be stripped

**Why it matters:** REQ-F6 and AC-3 require functional hyperlinks from citation to reference. If the rendering environment doesn't support this, the requirement is impossible.
**Fix:** Test empirically whether Claude.ai artifact markdown supports internal anchors. If not, change the requirement to:

> Use IEEE-style numbered references. Place citation numbers in brackets [1], [2] in the body text. List all references in a numbered References section at the end. Number them to match.

This drops the hyperlink requirement between citation and reference (which is a reading convenience, not a verification necessity) while preserving the link requirement on the reference URLs themselves.

---

### 7. Feasibility — Link verification via web search

**Location:** Research Phase Rules, line 49
**The problem:** "Before including any URL in the references, use web search to confirm that the link points to the correct page." This instruction asks Sonnet to do something specific: take a URL, search for it (or visit it via web search), and confirm the content matches. In practice, Sonnet's web search capability is keyword-based query submission, not URL verification. Sonnet cannot HTTP GET a URL. What it CAN do is search for the article title + site and confirm the result exists. This is a meaningful but different kind of verification than what the instruction implies.
**Why it matters:** Sonnet will likely interpret this instruction as "I should search for this URL" which may or may not actually verify the link. It may also simply claim to have verified links without actually performing a search (a known failure mode for Sonnet when given verification tasks that are procedurally awkward).
**Fix:** Be specific about the mechanism:

> **Link verification:** For each reference, search the web for the article title and source organization. Confirm that the URL you cite appears in search results pointing to that content. If you cannot confirm the URL through search, include the reference but mark it: "[unverified link]".

This gives Sonnet a concrete action (search for title + org) rather than an abstract instruction (verify the link).

---

### 8. Theater — Self-check protocol

**Location:** Self-Check Protocol, lines 59-68
**The problem:** The self-check asks Sonnet to audit its own output for four specific issues. In practice:
- **Citation-link match** (item 1): Sonnet wrote the citations and references in the same generation pass. Asking it to verify its own work immediately after producing it is like asking someone to proofread their own essay — they'll see what they intended, not what they wrote. The model's confidence in its own output makes it unlikely to catch genuine mismatches.
- **Unrequested synthesis** (item 2): As noted in finding #1, this is fighting the elephants problem. Sonnet will either over-flag or under-flag.
- **Missing specifics** (item 3): Same issue — Sonnet decided to summarize because it seemed appropriate. Asking it to second-guess that decision with no new information won't change the output.
- **Unverified links** (item 4): This is the most useful check because it's mechanical — did I mark things [unverified]? Yes or no.

The spec (REQ-F8) acknowledges self-verification of factual accuracy is out of scope. But the self-check as written is still largely theater for items 1-3.
**Why it matters:** A "Self-Check Results" section that says "All citations verified, no unrequested synthesis found, all specifics preserved" gives the user false confidence. It looks like quality assurance but provides almost none.
**Fix:** Make the self-check produce useful output rather than pass/fail claims:

> ## Self-Check
> Before delivering the final report, produce a Self-Check section listing:
> 1. **Reference summary** — For each reference [N], state: the claim it supports (brief), the source name, and whether you confirmed the URL via web search (yes/no).
> 2. **Organization note** — Were any findings from different sources combined into the same paragraph? List the paragraph and sources.
> 3. **Specificity note** — List any places where you summarized rather than quoting directly, and why.
> 4. **Unverified links** — List any references you could not confirm via search.
>
> Do not claim to have verified factual accuracy. That is my responsibility.

The difference: instead of asking "did you mess up?" (which always gets "no"), ask "show your work" (which produces auditable evidence the user can actually check).

---

### 9. Missing Behavior — No opening orientation

**Location:** "Start Now" section, line 72
**The problem:** The spec (UC-1, step 2) requires: "Claude responds with an opening message that orients the user — what this will produce, roughly how long it will take, and the first gathering question." The prompt says only: "Begin the gathering phase. Ask me the first question." There is no instruction to orient the user.
**Why it matters:** A non-technical user who pastes this prompt and gets back "What do you want to research?" with no context will be confused. They need a brief framing: "I'll ask you a few questions, then create a research plan for your approval, then do the research. Let's start..."
**Fix:**

> ## Start Now
> Begin by briefly telling me what this process will produce (a query report and a research report) and how many questions you'll ask. Then ask the first gathering question.

---

### 10. Missing Behavior — No recovery from approval rejection

**Location:** Query Report, line 35
**The problem:** "Wait for my approval before proceeding. I may ask you to adjust the plan." But there's no instruction for what "adjust" means. Can the user reject the whole plan? Can they add requirements? What if they want to change the research question entirely? Sonnet needs to know the scope of permissible adjustment.
**Why it matters:** Without guidance, Sonnet will either (a) treat any pushback as a minor edit and proceed too quickly, or (b) re-run the entire gathering phase, wasting tokens.
**Fix:** Add a sentence:

> Wait for my approval before proceeding. If I ask for changes, revise the Query Report and show me the updated version. If I want to change the research question, return to the gathering phase.

---

### 11. Missing Behavior — Artifact format instruction

**Location:** Throughout
**The problem:** The prompt says "Create a markdown artifact titled..." but doesn't instruct Sonnet to use Claude.ai's artifact feature specifically. On free-tier Claude.ai, Sonnet CAN create artifacts (the panel on the right side), but it won't always do so — it may just produce the markdown inline in the chat. The word "artifact" in the prompt might be interpreted as "a document" rather than "use the artifact panel."
**Why it matters:** REQ-F3 and AC-7 require "downloadable" artifacts. Inline markdown in chat is not downloadable in the same way.
**Fix:** Be explicit:

> Create a markdown artifact (using the artifact panel, not inline in chat) titled "Query Report"...

Or more naturally:

> Create an artifact titled "Query Report" — this should appear in the artifact panel to the right, not in the chat itself.

---

### 12. Ambiguity — "Follow these instructions exactly"

**Location:** Line 1
**The problem:** "Follow these instructions exactly" is a common prompt opening that Sonnet has seen thousands of times. It's effectively noise — the model doesn't follow instructions more precisely because you told it to. It's the prompt engineering equivalent of "please be accurate." It consumes tokens without producing behavioral change.
**Why it matters:** Token efficiency. Every word in a ~1100-token prompt needs to earn its place.
**Fix:** Cut it. The sectioned structure of the prompt already implies "follow this." If you want compliance reinforcement, make it specific: put behavioral locks on the instructions that actually need them (one-at-a-time gathering, wait-for-approval pause).

---

### 13. Drift — No tone/voice instruction

**Location:** Absent
**The problem:** The prompt doesn't specify how Sonnet should talk to the user during the gathering phase. Sonnet's default on free tier is chatty and eager to please. For a non-technical user, this might be fine — or it might be condescending, overly formal, or inconsistent. The spec (REQ-N3) requires the gathering to "feel like a natural conversation, not an interrogation or form-filling exercise."
**Why it matters:** Without tone guidance, Sonnet will default to its trained persona, which varies by session. Some sessions will feel warm and conversational; others will feel robotic. Consistency across sessions matters for a portable prompt.
**Fix:** Add a brief voice line in the "How You Work" section or a new one-liner section:

> **Tone:** Be conversational and brief during gathering. Don't over-explain. In the reports, be precise and formal.

---

### 14. Token Efficiency — The prompt is underweight

**Location:** Overall
**The problem:** At ~1100 tokens, this prompt is well under the 4000-6000 token budget the spec allows (REQ-N2). The spec explicitly notes that "front-loading behavior pays off across the entire conversation; 200K context can absorb it." The prompt has room to add the fixes above AND more behavioral specificity without approaching any limit.
**Why it matters:** Every instruction gap identified above (no orientation, no tone, no artifact panel instruction, vague gathering locks, theater self-check) exists because the prompt is trying to be concise when it has budget to be precise. The ~1100-token prompt is optimized for the wrong constraint.
**Fix:** Use the budget. The fixes above would bring the prompt to roughly 1800-2200 tokens — still well under 4000. The remaining budget could be used for:
- An example of what a good gathering answer looks like (showing the user they can be brief)
- More explicit error handling instructions (what to do when web search returns nothing relevant)
- A "What this does NOT do" section for the user (this is not fact-checked; you must verify independently)

---

### 15. Missing Behavior — What happens at the end?

**Location:** Absent
**The problem:** After the Research Report and Self-Check are delivered, there's no instruction for what happens next. Does Sonnet offer to revise? Does it ask if the user wants synthesis? Does it sign off? Without a closing instruction, Sonnet will default to "Is there anything else I can help with?" which is generic and unhelpful.
**Why it matters:** The user may want to ask follow-up questions, request synthesis on specific points, or ask Sonnet to expand a section. A brief closing instruction shapes this productively.
**Fix:**

> ## After Delivery
> After delivering the Research Report, ask if I want you to: expand any section, search for additional sources on a specific point, or revise anything. Do not offer to synthesize unless I ask.

Wait — that last sentence is an elephant. Better:

> After delivering the Research Report, ask if I want to expand, add sources, or revise anything.

---

## Summary of Priority Fixes

| Priority | Issue | Finding # |
|----------|-------|-----------|
| **High** | Gathering will collapse into batched questions | 3 |
| **High** | Self-check is theater — restructure as "show your work" | 8 |
| **High** | No opening orientation for non-technical user | 9 |
| **High** | Artifact panel not explicitly invoked | 11 |
| **Medium** | "Don't synthesize" is an elephant — restructure as positive constraint | 1, 2 |
| **Medium** | Link verification mechanism is vague | 7 |
| **Medium** | IEEE internal hyperlinks may not render | 6 |
| **Medium** | Source priority is domain-locked | 5 |
| **Medium** | No tone instruction creates session drift | 13 |
| **Medium** | Prompt is underweight for its token budget | 14 |
| **Low** | "Accept whatever" fights "draw out specifics" | 4 |
| **Low** | No approval rejection handling | 10 |
| **Low** | "Follow these instructions exactly" is noise | 12 |
| **Low** | No closing behavior | 15 |

---

## What's Well-Engineered

- **Phase structure (Gather-Plan-Pause-Research-Check):** This is excellent prompt architecture. The explicit pause gate between Query Report and Research is the single most valuable structural decision — it prevents Sonnet from running off with a bad plan. Most prompts skip this.
- **Query Report as separate artifact:** Separating intent from evidence is genuinely useful for downstream verification, not just security theater.
- **"Do not claim to have verified the factual accuracy of any claims" (line 68):** This is a well-placed boundary. It's specific, it's a positive constraint (defines what NOT to claim rather than what NOT to do), and it addresses a real failure mode where Sonnet says "I've verified all facts."
- **Error Handling section in Query Report (line 32):** Forcing the AI to pre-commit to error handling strategies before it encounters errors is smart. This creates a self-referential contract the AI can check against.
- **[unverified link] marking pattern (line 49):** Giving a specific label for the failure case is better than most prompts manage. Sonnet now has a concrete action for the "I can't verify this" case instead of silently dropping or silently including.
- **Overall brevity and clarity:** The prompt reads clean. A non-technical user who glances at it won't be intimidated. The section headers are scannable. The language is direct.

---

## Self-Evaluation

- **What worked well:** The spec gave me concrete acceptance criteria to evaluate against, which made it easy to identify where the prompt under-delivers (orientation, artifact panel, gathering pacing). Evaluating for the specific Sonnet 4.6 free-tier context — not Claude Code, not API — kept the review grounded in real constraints.
- **What I struggled with:** Determining whether the self-check is genuinely useful or pure theater required judgment about model behavior that I can't verify without testing. I flagged it as theater with a concrete alternative, but I may be underestimating Sonnet's ability to catch its own citation mismatches in a fresh review pass.
- **Prompt improvement suggestions for my own agent prompt:** The 10-dimension evaluation framework provided in the task prompt was excellent scaffolding — it prevented me from doing a generic "this is unclear" review and forced specific failure-mode analysis. I would benefit from having a standing reference of known Sonnet 4.6 behavioral tendencies (batching questions, compliance theater, artifact vs. inline decisions) so I don't have to reason about them from scratch each time.