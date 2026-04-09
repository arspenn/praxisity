## User Advocate Review

**Artifact:** SPEC-008 Portable Research Prompt — v0.2 prompt, test outputs (Query Report + Research Report), instructor baseline, spec, design
**Date:** 2026-04-09
**Dispatch Mode:** Mode 3 (Collaborative Team)

## Instructions Received

Review the v0.2 portable research prompt and its test outputs from the perspective of the target user: a non-technical person (e.g., public health intern) who will copy-paste this prompt into Claude.ai's free tier. No prompt engineering experience. Evaluate whether the prompt serves them — will they understand what's happening, feel in control, and get useful output? Specific focus areas: first impressions, two-artifact structure clarity, Problem Log usefulness, comparison to instructor baseline, and prompt chaining accessibility.

---

## User Experience Assessment

### [Impact: Blocking] — The user is never told what to do after the conversation ends

**What a new user encounters:** They paste the prompt, answer questions, get two artifacts. The conversation ends. They have a Query Report and a Research Report. Now what?

**Why it's a problem:** The entire architecture depends on "prompt chaining" — using these artifacts as input to a verification conversation. But the word "prompt chaining" never appears in user-facing output. The Limitations Statement says "must be independently verified in a separate session" but offers no guidance on what that means, how to do it, or with what prompt. A public health intern reading "independently verified in a separate session" would likely interpret this as "show it to my supervisor" — which is one valid path but misses the designed intent of pasting the Research Report into a new AI conversation for verification.

The framework philosophy is "use the system to build the user." But the user can't learn a workflow they don't know exists. This is the single biggest gap: the prompt produces chain-ready output but never teaches the user about chains.

**Suggested improvement:** The Closing Block (COMP-6 in the design) should include a brief, plain-language explanation: "These two documents are designed to be checked. You can start a new conversation, paste the Research Report, and ask Claude to verify the sources and claims. This is a separate step because the same AI that wrote the research should not be the one to verify it." This teaches the concept without jargon and gives a concrete next action.

---

### [Impact: Friction] — The prompt reads as instructions for the AI, not for the user

**What a new user encounters:** A 96-line document that opens accessibly ("You are a research assistant guiding me through a structured process") but quickly shifts to technical prompt engineering language: "Use web search for every claim," "Quote directly from sources," "Link accuracy is critical," "Error Handling" tables. The user is reading the prompt before pasting it — and much of what they read is not addressed to them.

**Why it's a problem:** The spec requires the prompt be "usable by someone with no prompt engineering experience" (REQ-N1). The prompt satisfies this functionally — pasting it works. But experientially, the user is asked to paste a document full of instructions they don't fully understand. This doesn't stop them from pasting, but it creates a subtle power imbalance: the prompt knows things the user doesn't, and the user is along for the ride rather than in control.

The design calls this "dual-audience language" (REQ-F10: "AI reads instructions, user reads output"). But the prompt itself is the first thing the user reads, and it's written almost entirely for the AI.

**Suggested improvement:** Add a brief section at the top — 2-3 sentences — addressed directly to the user: "This prompt will guide an AI research assistant through a structured process. You don't need to understand the technical instructions below — just paste this into a new Claude.ai conversation, and the assistant will ask you questions one at a time. You'll review a research plan before any research begins." This separates the human audience from the AI audience and gives the user confidence before they encounter the technical sections.

---

### [Impact: Friction] — The two-artifact structure is explained but not motivated

**What a new user encounters:** The prompt's opening message says "You'll get two downloadable documents: a Query Report (the research plan) and a Research Report (the findings)." The parentheticals explain what each is. But the user is never told *why* there are two, or what the Query Report is for after the conversation.

**Why it's a problem:** A non-technical user will likely skim or ignore the Query Report and focus on the Research Report — the "real" output. The Query Report's value is twofold: (1) it's an approval gate so the user can redirect research before it starts, and (2) it's a reference for downstream verification ("did the AI follow its own plan?"). The first value is experienced in-conversation. The second value is invisible unless someone explains it.

Without understanding why they have two documents, the user will treat the Query Report as bureaucratic overhead — something the AI made them approve before getting to the good part. This undermines the design's verification architecture.

**Suggested improvement:** When presenting the Query Report for approval, the AI should say something like: "This plan is yours to keep — if you verify the research later, you can check whether I followed the plan I committed to." One sentence. It makes the two-artifact structure meaningful to the user without requiring them to understand the lethal trifecta.

---

### [Impact: Friction] — The Problem Log mixes actionable information with AI apologies

**What a new user encounters:** A Problem Log with 6 entries. Some are genuinely useful (#4: protest attendance figures are organizer claims, not verified; #6: sources contradict each other on ceasefire scope). Others read as the AI apologizing for not completing tasks the user never explicitly asked about (#2: "No direct Instagram trend data was found"; #3: "No direct Reddit thread scrapes or Quora digest snapshots were found").

**Why it's a problem:** The Problem Log is designed to replace self-assessment with "show what happened" — a strong design decision (DEC-2). But in practice, the v0.2 output's Problem Log contains entries that are methodology gaps (Instagram/Reddit/Quora data not found) rather than evidence problems. A non-technical user reading "platform gap — Instagram" may think the research is incomplete or unreliable, when the actual findings are well-sourced through major news outlets.

The Problem Log creates anxiety proportional to its length, not proportional to the severity of the issues it documents. Six entries looks like a lot went wrong. In reality, only 2-3 entries are things the user needs to act on.

**Suggested improvement:** Consider restructuring the Problem Log into two categories: "Things to check" (contradictions, unverified claims, organizer-reported numbers) and "Methodology notes" (platform gaps, paraphrasing decisions). The first category is actionable. The second is informational. This lets the user focus their verification effort on what matters.

---

### [Impact: Friction] — Domain flexibility undercuts domain usefulness

**What a new user encounters:** The v0.2 prompt defaults to public health sources (CDC, WHO, NIH) but gathers the research question from the user. In the test, the user asked for "top 5 trending topics" — a general question. The prompt faithfully researched general trending topics (Iran war, protests, moon mission, gas prices, higher ed reform). Each topic includes a "Public Health Relevance" paragraph bolted on at the end.

The instructor's baseline, by contrast, hardcoded "Act as an industry analyst for public health" and produced five directly relevant public health topics (measles, funding cuts, GLP-1 drugs, youth mental health, infrastructure).

**Why it's a problem:** A public health intern who uses the v0.2 prompt and gets a report about the Iran-Israel war and Artemis II moon mission will be confused about why a public health research tool produced geopolitics research. The "Public Health Relevance" paragraphs feel retrofitted — because they are. The prompt's gathering phase correctly captured what the user asked for, but a non-technical user may not know they should ask for public-health-specific topics. They'll assume the tool knows what they need.

This is a case where flexibility hurts more than it helps. The target user doesn't have the domain expertise to direct the tool effectively. They need the tool to bring domain knowledge to the gathering phase.

**Suggested improvement:** For the public health use case specifically, the gathering phase should include a question like: "Should I focus specifically on public health topics, or look at general trending topics and highlight their public health implications?" This gives the user a choice without requiring them to know the right answer upfront.

---

### [Impact: Minor] — The Limitations Statement is honest but jarring

**What a new user encounters:** At the bottom of the Query Report: "This query report and the research report it produces are AI-generated. Both documents must be independently verified in a separate session before being treated as reliable sources. Neither artifact should be used as trusted input to further work without external verification."

**Why it's a problem:** This is correct and important (DEC-5). But for a non-technical user, this reads as "don't trust anything I just produced." Combined with the Problem Log, it can create an impression that the tool is unreliable. A student might wonder why they went through the whole process if the output can't be trusted.

The issue isn't the disclaimer — it's the lack of context around it. The user isn't told that this disclaimer is a feature, not a bug. It's not that the AI did bad work; it's that no AI output should be treated as verified without a second check. This is a principle the user could learn and carry to other contexts.

**Suggested improvement:** Frame the Limitations Statement as a principle rather than a warning. Something like: "This is AI-generated research. The standard practice with AI output is to verify it independently — the same AI that wrote the research shouldn't be the one to verify it. Treat these documents as a thorough first draft, not a finished product." This teaches the concept rather than just issuing a disclaimer.

---

### [Impact: Minor] — The v0.2 output is better research but worse deliverable

**What a new user encounters:** If they compare v0.2 output to what a simpler prompt produces (like the instructor baseline), they'll notice: the baseline is a clean, polished table they could email to their supervisor right now. The v0.2 output is a 289-line evidence document they'd need to read through, extract key findings from, and potentially reorganize before sharing.

**Why it's a problem:** This isn't a design flaw — the v0.2 output is intentionally structured for verification, not presentation. But a student who needs to produce a deliverable today will prefer the simpler output. The v0.2 output's value proposition — traceability, source attribution, verification readiness — is invisible to someone who just needs "the answer."

The framework philosophy is that the v0.2 process builds better research habits. But the first impression matters: if the first use produces something less immediately useful than a simpler approach, the user may not come back for the second use.

**Suggested improvement:** Not a prompt change — this is a positioning issue. If the prompt is given to students by an instructor, the instructor should explain that this tool produces research materials, not final deliverables. The output is the starting point for their own analysis, not the endpoint. This context could also be embedded in the orientation message.

---

## What Works Well for Users

**The gathering phase is genuinely helpful.** One question at a time, conversational, accepting of short answers. A non-technical user would feel comfortable in this phase. The one-follow-up-allowed design (from the PE review fix) balances helpfulness with respect for the user's time.

**The approval gate before research begins is empowering.** The Query Report pause is the moment where the user feels most in control. They can see the plan, modify it, and approve it. This is well-designed and well-timed.

**The Research Report's source-by-source structure is educational.** Even if a student doesn't fully appreciate it on first use, reading a report where each claim is attributed to a specific source with a URL teaches them what rigorous research looks like. This is the "builds the user" philosophy working as intended.

**The Problem Log concept is sound.** Even though the v0.2 execution mixes actionable and informational entries, the principle of "show what happened" rather than "grade your work" is genuinely useful. When the entries are actionable (contradicting sources, unverified claims), they give the user a concrete verification checklist.

**The orientation message is clear.** "I'll ask you a few questions, then create a plan, then do research. You'll get two documents." A non-technical user knows exactly what they're getting into.

**The error handling pre-commitment in the Query Report is invisible but valuable.** The user may not appreciate it, but the fact that the AI wrote down what it would do when things go wrong — before encountering problems — produces more consistent behavior. This is good design that doesn't burden the user.

---

## Self-Evaluation

- **What worked well:** Putting myself in the intern's shoes and reading every document in order of encounter (prompt first, then outputs) revealed gaps that are invisible from the developer's perspective. The prompt chaining gap is obvious when you ask "what does the user do next?" but easy to miss when you're thinking about verification architecture. The baseline comparison was revealing — the instructor's simpler prompt produces more immediately useful output, which is an important data point for positioning.

- **What you struggled with:** Drawing the line between "this is too complex for the user" and "this complexity is necessary and just needs better explanation." The two-artifact structure, the Problem Log, the Limitations Statement — these are all good ideas. The user experience problem isn't that they exist, it's that they're not motivated or explained. I may be overstating the intimidation factor of the prompt itself — a student told by their supervisor "paste this into Claude" will probably just paste it without reading, which makes many of my "first impression" concerns moot. But the post-conversation gap (what do I do with these documents?) is real regardless of whether they read the prompt first.

- **Prompt improvement suggestions:** My agent prompt could benefit from a specific rubric for evaluating "builds the user" — right now I'm interpreting this principle case by case. A checklist like "does the user learn a transferable concept? can they explain what happened to someone else? would they modify their behavior in future AI interactions?" would make my assessments more consistent. I should also be pushed to distinguish between "the user doesn't understand this" (a problem) and "the user doesn't need to understand this" (not a problem) — some complexity is correctly hidden from the user.