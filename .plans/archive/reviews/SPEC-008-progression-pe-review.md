## Prompt Engineer Review

**Artifact:** `.plans/references/bsi-workshop-prompt-progression.md`
**Date:** 2026-04-14
**Dispatch Mode:** Mode 1 (standalone consult)

## Instructions Received

Review the BSI workshop prompt progression (Steps 0-5) for prompt engineering quality. The progression teaches public health professionals how prompt engineering differs from search engine querying. Each step builds on the last by adding one concept. Target platform is free-tier Claude.ai (Sonnet 4.6, 200K context, web search, artifacts). Evaluate for progression coherence, per-step prompt quality, session limit risk, educational clarity, missing steps, and cross-step consistency.

## Dual-Consumption Assessment

### Ambiguity — "Role" field primes Sonnet toward general industry analysis, not public health research

**Location:** All steps, `Role` field
**Problem for AI:** "Act as an industry analyst for public health" is the instructor's baseline language. It tells Sonnet to be a generalist industry analyst *scoped to* public health. Compare the instructor's baseline output: it produced topics like the Iran war, No Kings protests, and Artemis II — general trending topics with public health relevance bolted on afterward ("Public Health Relevance" subsections). The v0.2 research report did the same. The Role never changed to match the progression's increasing source specificity. By Step 2, you're telling Sonnet to search CDC/WHO/NIH and include direct quotations from peer-reviewed journals, but the Role still says "industry analyst" — a persona that wouldn't naturally prioritize those sources.
**Problem for humans:** Not visible to the audience. They won't notice that the Role field is working against the Sources field.
**Suggested fix:** Change Role in Steps 1-5 to "Act as a public health research analyst" (matching v0.4). This aligns the persona with the source instructions and gives the audience an additional delta to observe between Step 0 and Step 1: "We didn't just add sources — we changed who the AI pretends to be."

---

### Ambiguity — Step 0 includes "Steps" field that gets silently dropped

**Location:** Step 0 vs Step 1
**Problem for AI:** Step 0 has a `Steps` field with explicit search instructions (news outlets in the US, global outlets discussing the US). Step 1 replaces this with a `Sources` field but drops the sequential search strategy entirely. The audience is told "Added a `Sources` field directing the AI to authoritative public health sources instead of general news only" — but a `Steps` field was also removed. From Sonnet's perspective, Step 0's instructions tell it *how* to search (sequentially, two stages). Step 1 tells it *where* to look (source types) but not in what order or how many passes.
**Problem for humans:** The "What changed" note only mentions the addition. A workshop attendee comparing the two prompts would notice the Steps field disappeared and wonder if that was intentional or an error. This undermines the "exactly one concept changed" framing.
**Suggested fix:** Either (a) keep Step 0 as the true instructor baseline without the Steps field — just Role/Goal/Output — making it an even simpler "search engine query" baseline, or (b) acknowledge in the "What changed" note that the Steps field was replaced by Sources, and explain why ("We replaced a rigid procedure with a flexible source list — the AI decides the search order, but we control where it looks").

---

### Noise — Step 4 structural constraint may not produce a visible delta

**Location:** Step 4, the "Do not add editorial analysis" line
**Problem for AI:** This is a prohibition — and the design doc itself flags the elephants risk. But the bigger issue for the progression is *visibility*. Whether Sonnet adds unsolicited "Implications" or "Analysis" sections is inconsistent across runs. The v0.2 test showed 5 unsolicited editorial sections; the instructor's baseline output also added "Analyst Notes" and "Cross-Platform Momentum Signals" sections. But in a live demo, Step 3 might not produce extra sections — in which case Step 4 has no visible effect, and the audience sees a step that "changed nothing." That's a progression failure.
**Problem for humans:** If Step 3 and Step 4 produce identical-looking output, the audience loses confidence that prompt additions matter. The instructor would need to explain a counterfactual ("Step 3 *could have* added extra sections"), which is a weak pedagogical position.
**Suggested fix:** Consider swapping the ordering: make structural control Step 3, and transparency (Problem Log) Step 4. The Problem Log is guaranteed to produce visible output (it's a new section that either appears or doesn't). That way, even if structural control doesn't produce a visible delta, it's followed by a step that definitely does. Alternatively, reframe Step 4's "What to look for" to be honest: "Compare to Step 3. If Step 3 already has no extra sections, the constraint was unnecessary — and that's a real prompt engineering lesson too. Not every addition matters every time."

---

### Elephants — "Do not add editorial analysis or commentary sections"

**Location:** Steps 4 and 5, final line before Step 5's interactivity addition
**Problem for AI:** This is literally a "don't think about elephants" instruction. The design doc (DEC-4) flags this but keeps it because v0.2 testing showed the problem. However, the progression is now being used to teach prompt engineering — and a prohibition instruction is the opposite of what the progression is supposed to demonstrate. Steps 1-3 all use positive structure ("include X," "mark it Y," "note Z"). Step 4 breaks the pattern with a negative constraint. Sonnet may partially comply, partially ignore, or comply in letter but not spirit (e.g., embedding editorial content inside the findings rather than in a separate section).
**Problem for humans:** If the instructor is teaching "structure over prohibition" (a principle from the design doc), Step 4 contradicts it. A savvy attendee might ask "why are we telling it what NOT to do instead of what TO do?"
**Suggested fix:** Rewrite as a positive structural instruction: "The output should contain only the sections listed above." This achieves the same constraint without the prohibition framing, and maintains the progression's pattern of additive positive structure.

---

### Drift — Step 5's interactivity instruction is too vague for Sonnet

**Location:** Step 5, "Ask me highly detailed questions before beginning research."
**Problem for AI:** "Highly detailed questions" gives Sonnet no calibration for what counts as highly detailed. In testing, Sonnet might ask 2 broad questions or 15 narrow ones. There's no instruction about how many questions, whether to ask them all at once or one at a time, or when to stop asking and start working. The v0.3 prototype (which used a full gathering pipeline) hit the session limit after 2 questions — and that was with carefully scoped gathering. An unconstrained "ask me highly detailed questions" instruction could easily trigger 5+ round-trips before research even begins.
**Problem for humans:** The audience won't know what to expect. Some will get 2 questions, others 8. The "What to look for" says "Does the AI ask relevant questions?" but relevance is subjective and the output variance between audience members will be high.
**Suggested fix:** Constrain the round-trips: "Before beginning research, ask me 2-3 questions to understand what I'm looking for." This caps the session cost, sets audience expectations, and gives Sonnet a clear stopping condition. The "What changed" note can explain: "We limited it to 2-3 questions because every question-and-answer costs you free-tier usage."

---

### Clarity — "What to look for" notes are excellent but inconsistently actionable

**Location:** Steps 1-5, "What to look for" sections
**Problem for AI:** N/A — these are human-facing only.
**Problem for humans:** Steps 2 and 3 give concrete, testable actions: "Can you click the links and find the quoted text?" and "Try clicking a link marked [link unconfirmed]." Steps 1 and 4 give comparison tasks: "Do the topics change?" and "Compare to Step 3." Step 5 asks a yes/no question. The actionable steps (2, 3) are much stronger pedagogically than the comparison steps (1, 4) because they produce a definitive yes/no answer. Step 1's "Do the topics change?" might get a "no" if Sonnet finds the same topics regardless of source instructions — and the audience won't know if that means the step failed or the topics were genuinely the same.
**Suggested fix:** For Step 1, add a concrete check: "Look at the sources cited. Do you see CDC, WHO, or NIH references that weren't in the Step 0 output?" For Step 4: "Count the section headers. Are there fewer than in Step 3?"

---

### Ambiguity — Step 2 overloads with two concepts

**Location:** Step 2, Sources and Links fields
**Problem for AI:** Step 2 adds three new behaviors simultaneously: (1) "use web search to find the original source" in Sources, (2) "Include direct quotations where possible" in Sources, and (3) the entire Links field with the `[link unconfirmed]` pattern. The progression principle is one concept per step. Direct quotations and link verification are both about verifiability, but they're different mechanisms — one controls content (quote the source), the other controls metadata (URL must point to specific page). An AI processing this gets a large behavioral surface area change in one step.
**Problem for humans:** The "What changed" note tries to bundle these as one concept ("verification") but a non-technical attendee will see two new things: "now it quotes things" and "now links have to be specific." The delta is too large to attribute to a single change.
**Suggested fix:** Split Step 2 into two steps. Step 2: Source quality — add "For each claim, use web search to find the original source. Include direct quotations where possible" to the Sources field. Step 3: Link integrity — add the Links field. This keeps each step to one concept and gives you a 7-step progression (0-6), which better fills a workshop slot. Alternatively, if 6 steps is the hard cap, move direct quotations to Step 1 alongside source selection (both are about "where does the information come from") and make Step 2 purely about link verification.

## Session Limit Risk Assessment

| Step | Estimated Cost | Risk Level | Notes |
|------|---------------|------------|-------|
| 0 | Low | Safe | Confirmed working — this is the instructor baseline |
| 1 | Low | Safe | Same structure, slightly more specific search targets |
| 2 | Medium | Watch | Web search verification adds search round-trips. "Find the original source" may cause Sonnet to do 5+ additional searches |
| 3 | Medium | Watch | Problem Log adds output length but no extra searches. Marginal increase from Step 2 |
| 4 | Medium | Safe | Removal instruction, no new search behavior. Slightly shorter output if it works |
| 5 | High | At risk | Each user question-and-answer is a round-trip. With "highly detailed questions" unconstrained, could be 3-8 round-trips before research. v0.3 died at 2 questions with a 1500-token prompt. This step uses a shorter prompt but the same conversation pattern that killed v0.3 |

**Step 5 is the highest-risk step and the most likely to fail.** The progression note warns about this, which is good. But the warning is at the bottom of the step — in a workshop setting, attendees will paste first and read warnings second. Consider moving the session budget warning to the "What changed" note itself, or bolding it.

**Step 2 is the hidden risk.** The "use web search to find the original source" instruction triggers additional search calls per claim. If Sonnet finds 5 topics and does 2-3 verification searches per topic, that's 10-15 extra searches on top of the initial research. Each search costs session budget. This is the step most likely to push the total session cost above the instructor baseline without being obviously interactive.

## What's Well-Engineered

**The cumulative prompt structure is excellent.** Each step shows the full prompt, not just the diff. This is exactly right for a non-technical audience — they never have to mentally merge changes. It also works perfectly as AI input since each block is self-contained and pasteable.

**The `[link unconfirmed]` pattern is a standout prompt engineering technique.** It gives Sonnet a graceful degradation path — instead of hallucinating a URL or silently dropping a source, it has a named behavior for the failure case. This is one of the hardest things to teach non-technical users (that you can design for AI failure modes), and the progression introduces it naturally.

**The Problem Log concept is well-placed in the progression.** It's concrete, visible, and produces a section that either exists or doesn't — making it easy for workshop attendees to verify the step worked.

**The "What changed" / "What to look for" structure is pedagogically sound.** It gives the audience both the intent (what we added) and the verification method (how to check it worked). This dual structure mirrors the prompt engineering pattern itself: instruction + verification.

**The session budget warning on Step 5 is honest and well-framed.** It tells users the trade-off rather than hiding it. "If you run low on usage, the earlier steps work without any conversation" is a clean fallback that preserves the value of steps 0-4.

**The shared Goal across all steps is a good control variable.** Same goal, different prompt structure = the audience can isolate the effect of each change. The Goal is specific enough to produce comparable output across steps.

## Self-Evaluation

- **What worked well:** Having the instructor baseline output, v0.2 test outputs, and design doc all in context let me evaluate the progression against empirical evidence rather than theorizing. The v0.3 session limit failure is the most important data point — it calibrates every risk assessment.
- **What I struggled with:** Judging the Step 4 elephant issue. The design doc already flagged it, and the team already decided to keep it. My recommendation to rewrite as positive structure is the same recommendation the design doc's own principles would suggest, but the team may have kept the prohibition for a reason I can't see from the documents (e.g., positive-structure alternatives were tested and failed). I'm flagging it anyway because the progression is an educational artifact, and teaching prohibition in a progression that's supposed to demonstrate additive positive structure is a contradiction the audience might catch.
- **Prompt improvement suggestions:** My review prompt should explicitly ask whether I have access to test outputs from the artifact under review. I evaluated against v0.2 and baseline outputs, but the progression itself hasn't been tested — I'm predicting behavior rather than analyzing results. That distinction should be clearer in my analysis.