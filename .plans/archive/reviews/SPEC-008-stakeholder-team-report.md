## Stakeholder Review

**Artifact:** SPEC-008 Portable Research Prompt — v0.2 test outputs (Research Report, Query Report), instructor baseline, spec, and design
**Date:** 2026-04-09
**Dispatch Mode:** Mode 3 (collaborative team)
**Intended Audience:** BSI (public health) internship supervisor or professor receiving student research output; more broadly, anyone receiving AI-assisted research from a non-technical user

## Instructions Received

Evaluate all SPEC-008 materials from the perspective of the person on the receiving end — a supervisor or professor who will consume the student's output. Key questions assigned:

1. If a student handed me the Research Report as preliminary research, what would my reaction be?
2. Does the Problem Log increase or decrease confidence in the work?
3. How does the instructor's baseline compare to the v0.2 Research Report? Which is more useful?
4. Would the Query Report be valuable as a demonstration of research process?
5. Is the "independently verified" disclaimer practical?
6. Would I accept work produced this way?

---

## Audience Fit Assessment

### [Impact: Weakened] — The Research Report answers the wrong question for a public health audience

**What the audience sees:** A student submits a 288-line Research Report on "top 5 trending topics in the United States." The five topics are: the Iran war, the No Kings protest movement, Artemis II, gas prices, and higher education reform. Each topic has a "Public Health Relevance" paragraph tacked onto the end.

**Why it doesn't serve them:** A BSI supervisor asked for trending topics research. What they got back is essentially a general current events report with public health connections bolted on after the fact. The "Public Health Relevance" paragraphs feel like afterthoughts — because they are. Compare this to the instructor's baseline output, which identified measles outbreaks, federal health funding cuts, GLP-1 drugs, youth mental health, and public health infrastructure dismantling. Those ARE public health topics. The v0.2 output found topics that are trending in general and then searched for health angles.

This is not a failure of the prompt's engineering. The prompt did what it was told — find trending topics in the United States. But from the supervisor's chair, the student didn't actually research public health. They researched the news cycle and added health footnotes. A professor would circle this and write: "This is a current events summary, not a public health analysis."

**Suggested improvement:** This is partly a gathering problem. If the prompt had drawn out "public health" as the domain focus more forcefully during gathering, the research would have been scoped differently. But it's also a structural issue: the prompt doesn't instruct the AI to evaluate whether the topics it finds actually belong to the stated domain. Adding a filter — "Do the topics you identified fall within the stated audience's domain? If not, search specifically within that domain" — would catch this.

---

### [Impact: Minor] — The Research Report is genuinely well-sourced and traceable

**What the audience sees:** Every claim is attributed to a specific source with a URL. Direct quotations are used extensively. Multiple outlets are cited per topic. The source list at the end is organized by topic.

**Why this serves them well:** If I'm a supervisor reading this, I can actually check the student's work. I can click a link and verify whether NPR actually reported what the report claims. This is dramatically better than the typical student submission where claims float unsourced. The report doesn't just say "gas prices went up" — it says who reported the specific number, when, and provides the link. This is the kind of sourcing I'd expect from a professional analyst, not a first-year intern. It would earn trust quickly.

---

### [Impact: Weakened] — The Topic Deep Dives are excessively long for preliminary research

**What the audience sees:** Each of the five topics gets 30-50 lines of detailed sourcing. The full report is 288 lines. This is enormous for what should be a landscape scan — "what's trending."

**Why it doesn't serve them:** A supervisor asking for "top 5 trending topics" wants a landscape overview, not a deep dive on each. The summary table (Section 2) is actually the most useful part of the report. The deep dives belong in a follow-up assignment where the student picks one topic to investigate thoroughly. Handing a supervisor 288 lines of dense sourcing when they wanted a 1-page overview creates two problems: (1) they won't read it all, and (2) the student looks like they don't understand the assignment's scope.

The instructor's baseline output, for all its problems, is actually closer to the right length for this task — a single-page table with analyst notes. It answers "what's trending" without drowning the reader.

**Suggested improvement:** The prompt should calibrate output depth to the research question. A "what are the top 5" question calls for a summary with sources, not a monograph. The deep dive format would be appropriate for "analyze [Topic X] in depth." This is a design-level issue — the output structure in the Query Report should match the scope of the question.

---

### [Impact: Misses Audience] — The "Public Health Relevance" sections are unsolicited editorial

**What the audience sees:** After each topic's sourced findings, there's an italicized paragraph connecting the topic to public health. These paragraphs cite no sources. They read like the AI's own analysis.

**Why it doesn't serve them:** These sections violate the report's own methodology. The rest of the report carefully attributes everything to specific sources. Then suddenly there are unsourced paragraphs making claims like "Fuel and pharmaceutical supply chain disruptions have global implications" and "Gas price spikes disproportionately burden lower-income households." These may be true, but they're the AI editorializing, not reporting. A careful supervisor would notice the shift in voice and ask: "Where did this come from?"

Worse, these sections are exactly what the design document (DQ-1) already flagged as a known issue. The v0.2 test confirmed that Sonnet adds editorial sections not defined in the Query Report. The fact that this was predicted and still shipped means either the fix wasn't implemented or it wasn't effective.

**Suggested improvement:** The design's proposed fix is correct: "Stick to the section headings defined in the Query Report — do not add sections not defined there." If Public Health Relevance analysis is desired, it should be defined as a section in the Query Report during the planning phase, with the same sourcing requirements as everything else.

---

### [Impact: Minor] — The Problem Log is genuinely valuable and builds trust

**What the audience sees:** Six specific, honest disclosures: an unconfirmed link, three platform gaps (Instagram, Reddit, Quora), an attendance figure flagged as an organizer claim, a paraphrasing note, and a contradiction between sources on the Lebanon ceasefire question.

**Why this serves them well:** This is the single most impressive part of the output from a supervisor's perspective. Most student work (and most AI-generated work) presents findings as if everything went smoothly. This report says: "Here's where I hit walls, here's what I couldn't verify, here's where sources disagree." That is exactly what I'd want to see in research I'm going to build on.

The protest attendance item (#4) is particularly good — it distinguishes between an organizer claim and a verified count. The contradiction item (#6) presents both sides without resolving it. These demonstrate research maturity that would be impressive coming from any student, let alone an AI-assisted one.

**One concern:** The Problem Log currently sits at the end of the Research Report. A supervisor scanning quickly might miss it. Consider whether it should be more prominent — perhaps a brief "X issues flagged in Problem Log" note at the top of the report.

---

### [Impact: Weakened] — The Query Report is process documentation, not a research deliverable

**What the audience sees:** A 103-line document describing search strategy, source priority, output structure, error handling, and a limitations statement.

**Why it doesn't fully serve them:** This depends heavily on the audience and context. For a professor evaluating a student's research methodology, the Query Report is valuable — it shows the student thought about their approach before diving in. It demonstrates planning, which is a research skill. A methods section is expected in academic work.

However, the Query Report as written reads more like prompt engineering documentation than a research methods section. Phrases like "Phase 3 — Social Platforms (X / Twitter)" with specific search terms listed are useful for reproducing the research but aren't how a student would present methodology to a professor. A professor expects something like: "I surveyed major U.S. and international news outlets, social media trend data, and community forums over a 30-day period, prioritizing authoritative sources." The current Query Report is too operationally detailed for an academic audience and not detailed enough to be a proper reproducibility document.

**Suggested improvement:** The Query Report serves two masters (user audit during the conversation, and downstream methodology documentation) and isn't fully optimized for either. For the stakeholder use case, a "Methods Summary" section in the Research Report itself would be more appropriate than a separate document. The Query Report's primary value is as a mid-conversation checkpoint, not as a deliverable.

---

### [Impact: Minor] — The "independently verified" disclaimer is honest but impractical

**What the audience sees:** At the bottom of the Research Report: "This research report is AI-generated. All findings must be independently verified before use."

**Why this partially serves them:** The honesty is appreciated. Disclosing that the work is AI-generated is the right call ethically and practically.

**Why it doesn't fully serve them:** "Independently verified" is vague. What does that mean for a student? Check every link? Read every source? Run the same queries themselves? A supervisor reading this disclaimer would ask: "Verified how? By whom? To what standard?" The spec calls this the "lethal trifecta" — untrusted output needs external verification. But the implementation is "must be independently verified" with no guidance on what verification looks like.

For a realistic BSI internship context: the student should spot-check 3-5 key claims by clicking through to the sources and confirming the quoted text exists on the page. That's a practical verification standard. "All findings must be independently verified" sounds like the student needs to redo the entire research project, which defeats the purpose of doing it in the first place.

**Suggested improvement:** Make the verification guidance concrete and proportionate. Something like: "This report is AI-generated. Before relying on any specific claim, confirm it by visiting the linked source. The Problem Log identifies areas of particular uncertainty."

---

### [Impact: Weakened] — The v0.2 output is less useful than the instructor's baseline for the stated purpose

**What the audience sees (instructor baseline):** A focused, single-page table of five public health topics with cross-platform momentum signals, brief analyst notes, and a clean methodology statement. Topics: measles, health funding cuts, GLP-1 drugs, youth mental health, public health infrastructure.

**What the audience sees (v0.2 output):** A 288-line general current events report with public health relevance paragraphs appended. Topics: Iran war, No Kings protests, Artemis II, gas prices, higher education reform.

**Why the baseline serves better:** The baseline answers the actual question — "what's trending in public health?" The v0.2 output answers a different question — "what's trending in the U.S.?" — and then tries to connect it to public health. For a BSI supervisor, the baseline is immediately actionable. The v0.2 output requires the supervisor to mentally filter out the non-public-health content to find the health angles.

**What the v0.2 does better:** Sourcing. The baseline lists source types at the bottom but doesn't cite specific articles. The v0.2 output cites dozens of specific sources with URLs and direct quotations. If the baseline's claims are wrong, the supervisor has no way to check. If the v0.2's claims are wrong, the supervisor can verify in minutes.

**The honest comparison:** The baseline is a better answer to the right question with no way to check it. The v0.2 output is a worse answer to the wrong question with excellent traceability. An ideal output would combine the baseline's topic selection with the v0.2's sourcing discipline.

**Important caveat:** This comparison is somewhat unfair. The instructor's baseline was produced by a different prompt that explicitly scoped to public health from the start. The v0.2 prompt asked about trending topics generally and let the audience field do the scoping work. The v0.2 prompt's gathering phase didn't sufficiently constrain the domain. That's a prompt design issue, not a fundamental flaw in the approach.

---

## What Serves the Audience Well

1. **Source traceability is exceptional.** Every claim attributed, URLs provided, direct quotations used. This is professional-grade sourcing that a supervisor can actually audit.

2. **The Problem Log is a genuine innovation.** Disclosing research limitations proactively builds trust rather than eroding it. A supervisor seeing six honest disclosures about gaps and contradictions would trust this work more, not less. This is the standout feature of the entire system.

3. **The two-artifact structure (query + research) demonstrates methodology.** For academic contexts, showing your plan before executing it is a research skill. The structure teaches the student to plan before diving in.

4. **The summary table (Section 2) is the right format for a landscape scan.** If the report stopped at the summary table plus a source list, it would be closer to the right scope for a "top 5" question.

5. **Error handling is pre-committed and followed.** The report handles contradictions (Lebanon ceasefire), unconfirmed links, and missing data exactly as the Query Report said it would. This consistency is reassuring.

---

## Broader Stakeholder Questions

### Would I accept work produced this way?

**Yes, with conditions.** The methodology is sound and the sourcing discipline is impressive. The conditions:

1. The topic selection must actually match the assignment's domain. General trending topics =/= public health topics. This is the biggest gap.
2. The student must demonstrate they understand what they're handing in. A cover note saying "I used an AI-assisted research process; here's what I verified and here's what I'd investigate further" shows judgment.
3. The output length needs to match the assignment scope. A 288-line report for a "top 5" question is overbuilt.
4. The unsourced editorial sections need to go or be properly sourced.

### What would make me more comfortable?

- Seeing the student's own annotations on the report — "I checked this claim; this link is dead; I'd want to dig deeper here"
- A brief cover memo in the student's own voice explaining what they learned and what surprised them
- Evidence that the student made choices (e.g., "I picked these 5 over the other candidates because...") rather than just accepting the AI's output wholesale

### What would make me less comfortable?

- If the student presented this as entirely their own work without disclosing the AI assistance
- If the student couldn't answer basic questions about the sources ("What did the NPR article actually say?")
- If the Problem Log items were presented as resolved when they clearly aren't ("link unconfirmed" treated as "link works")

---

## Self-Evaluation

- **What worked well:** Reading the Research Report as a supervisor naturally — before reading any of the design documents — gave me an authentic first impression. The topic selection problem jumped out immediately because I was reading as someone who wanted public health research and got general news. Reading the design documents afterward confirmed that many of the issues I found were already identified by the team (unsolicited editorial sections, Wikipedia sourcing, generic URLs), which validates that the review process is working.

- **What I struggled with:** Separating the prompt's design quality from the output's audience fit. The prompt engineering is clearly thoughtful (the Problem Log is brilliant, the gating structure is sound), but the output it produced doesn't serve the stated audience as well as a simpler, more domain-focused approach would. Recognizing that the prompt can be well-designed AND produce output that misses its audience is the nuance this review needed to hold.

- **Prompt improvement suggestions:** My agent prompt should include guidance on evaluating the gap between "technically correct" and "useful to the reader." A deliverable can satisfy every spec requirement and still not serve the audience. My prompt should also explicitly ask me to evaluate whether the output teaches the user (student) anything about the domain — since Praxisity's mission is "the framework builds the user through use," the stakeholder perspective should include whether the process made the student better at research, not just whether it produced a document.