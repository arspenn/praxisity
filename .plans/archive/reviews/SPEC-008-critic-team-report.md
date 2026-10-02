## Critic Review

**Artifact:** SPEC-008 full artifact set (spec, design, v0.2 prototype, test outputs, instructor baseline, PE review)
**Date:** 2026-04-09
**Dispatch Mode:** Mode 3 (collaborative team)

## Instructions Received

Stress-test the SPEC-008 artifact set across six specific angles: (1) domain-agnostic claim vs hardcoded public health defaults, (2) chain-ready vs publication-ready output tension, (3) lethal trifecta circularity, (4) Problem Log compliance theater, (5) token budget mismatch, and (6) design decisions solving non-problems. Also check for contradictions, unstated assumptions, and scope creep across spec, design, prompt, and test outputs.

---

## Findings

### [Severity: Important] — "Domain-agnostic format" is a false claim, but the real problem is nobody owns the contradiction

**Location:** SPEC-008 Section 8 ("not the subject matter of any particular prompt instance"), v0.2 prompt line 37 (CDC/WHO/NIH defaults), DESIGN-007 DEC-10

**Problem:** The spec says the format is domain-agnostic. The prompt hardcodes CDC, WHO, NIH, and state health departments as default sources. The design acknowledges this tension in DEC-10 ("Domain-Flexible with Public Health Defaults") and calls it an acceptable trade-off. The PE review (finding #5) flagged the same issue and offered two paths: own the domain specialization or make source priority dynamic.

None of the documents chose. DEC-10 says "good defaults for the target use case" and "expand based on guidance" — which is a punt, not a decision. The spec still says "domain-agnostic." The design still says "domain-flexible." The prompt still hardcodes health sources. Three documents, three different claims about the same thing.

**Impact:** If someone uses this prompt for educational policy, technology trends, or legal research, Sonnet will dutifully start by searching CDC and WHO. The "expand based on my guidance during gathering" instruction relies on the user knowing to redirect — which directly contradicts REQ-N1 ("no prompt engineering experience needed"). A non-technical user won't know to say "don't search CDC for my education policy question."

**Suggested fix:** Pick one and propagate it everywhere. Either: (a) Rename the spec to "Portable Public Health Research Prompt," update Section 8 to say the first iteration is domain-specific, and note generalization as future work. Or (b) Replace the hardcoded source list in the prompt with "Start with authoritative institutions relevant to the research topic. Choose starting sources based on what I describe during gathering." Option (a) is honest; option (b) adds risk that Sonnet picks poor defaults. Given the stated first use case is BSI internship public health work, (a) is the right call for v0.2.

---

### [Severity: Critical] — "Chain-ready over publication-ready" is contradicted by actual output

**Location:** DESIGN-007 Section 1.2 (design principle 3), Research_Report1.md

**Problem:** The design principle says "Chain-ready over publication-ready — Output must be usable as direct input to the next prompt, not polished for final delivery." But the v0.2 Research Report is a polished, 288-line deliverable with:

- A formatted summary table with columns for "Brief Description," "Primary Audience," "Associated Hashtags," and "Why It Is Trending" (lines 17-23)
- Five detailed "Topic Deep Dives" with multi-source narrative prose (lines 29-205)
- "Public Health Relevance" editorial sections appended to each topic (lines 64-66, 102-103, 135-137, 171-172, 203-204) — which are exactly the unsolicited editorial sections the design flagged as a problem in DQ-1
- A full Source List organized by topic (lines 208-268)

This is a near-final deliverable. If someone received this Research Report, they would treat it as a finished product, not as raw material for a verification chain. The design principle is not reflected in the actual output.

The disconnect has two causes: (1) The prompt doesn't actually enforce chain-readiness. It tells Sonnet to "quote directly" and "keep sources separate," but these are quality instructions, not format instructions. Nothing in the prompt says "produce structured data for machine consumption" or "avoid narrative prose." (2) The summary table is a natural Sonnet output for "top 5 trending topics" — Sonnet will always produce a polished table for this kind of request because that's what users expect.

**Impact:** The "chain-ready" principle creates a false expectation in the design that the output will be raw and structured. In practice, the output is polished enough that users will skip the verification step. This undermines the lethal trifecta separation — the output looks trustworthy, so users will trust it.

**Suggested fix:** Either (a) remove "chain-ready over publication-ready" as a design principle because the prompt doesn't enforce it and the output doesn't reflect it, or (b) add explicit format instructions to the prompt that would actually produce chain-ready output — e.g., "Present findings as structured entries, not narrative prose. Each finding: [source], [quote], [URL], [confidence]. Do not write summaries, editorials, or analysis sections." Option (b) would produce a less readable but more honestly chain-ready output. Option (a) acknowledges reality. The design should also note that the "Public Health Relevance" sections in the test output are a direct violation of this principle and of the design's own DQ-1 concern.

---

### [Severity: Important] — The lethal trifecta justification has a circularity problem

**Location:** SPEC-008 REQ-F8, REQ-F12, REQ-F13; DESIGN-007 DEC-9; Research_Report1.md line 288

**Problem:** The lethal trifecta principle (defined in the glossary as "AI output cannot be trusted as input to the next stage without independent verification by a separate agent or human") is used to justify:
- Separating Query Report and Research Report (so each can be "verified independently")
- Including a fixed limitations statement
- Scoping the prompt to source-finding, not fact-checking

The problem is the verification model. The spec says verification happens "in a separate session" (REQ-F8) or "in a separate conversation" (line 92 of v0.2, Section 8 of spec). But who or what does the verification?

- If it's a human: The human needs domain expertise to verify the claims. The target audience (REQ-N1) is non-technical users who lack prompt engineering experience and, presumably, deep domain expertise. Telling a public health intern to "independently verify" a 288-line Research Report against 50+ source URLs is unrealistic. They will either skip it or paste it into another Claude conversation.
- If it's another AI conversation: Then you have an untrusted AI verifying untrusted AI output. The lethal trifecta explicitly says this doesn't work — "independent verification by a separate agent or human" — but a fresh Claude.ai conversation is not an independent agent. It's the same model with the same training data and the same tendency to agree with plausible-sounding text.

The spec knows this. REQ-F8 says "self-verification of factual accuracy is outside the prompt's scope; that is the user's responsibility." But the user doesn't have the expertise, and the alternative "separate conversation" path is the lethal trifecta violating itself.

**Impact:** The two-artifact separation and the limitations statement create an appearance of a verification pipeline that doesn't actually function for the target audience. The architecture is sound in principle — separating intent from evidence IS valuable — but the claimed security benefit is mostly notional for non-technical users.

**Suggested fix:** Be honest about what the separation actually provides. The two-artifact split has real value: (1) It gives the user a chance to catch a badly scoped research plan before research begins (the INT-3 gate). (2) It produces a structured format that a domain expert (supervisor, professor) can audit efficiently. Reframe the trifecta justification around these concrete benefits instead of claiming it enables "independent verification" by users who can't realistically perform it. Add a line in the design: "For non-technical users, the verification step should involve a domain-knowledgeable reviewer (supervisor, subject matter expert), not another AI conversation." This is honest without abandoning the principle.

---

### [Severity: Important] — Problem Log entries are a mix of genuine and performative

**Location:** Research_Report1.md Section 5 (Problem Log, lines 274-284)

**Problem:** The Problem Log has 6 entries. Let me evaluate each:

1. **[link unconfirmed] for X/ISW post** — Genuine. The prompt asked for this exact behavior and Sonnet complied. This is the Problem Log working as designed.

2. **Platform gap — Instagram** — Genuine but reveals a design flaw, not a research flaw. The Query Report's search strategy included an entire Phase 5 for Instagram (lines 42-44), and the Problem Log correctly reports that no Instagram data was found. But the interesting question is: why did the Query Report plan to search Instagram in the first place? Because the *instructor's prompt* (baseline) told Sonnet to "Search instagram for trending topics." The v0.2 prompt doesn't mention Instagram. The gathering conversation presumably included this as user guidance. This is actually a success — the prompt's gathering phase captured user intent and the Problem Log reported the gap honestly.

3. **Platform gap — Reddit, Quora, Medium** — Same pattern as #2. Genuine gap, honestly reported. But again, these platforms were in the search plan because the user's topic and guidance implied them, not because the prompt hardcoded them.

4. **Protest attendance figures** — This is the most genuinely useful entry. It flags an unverifiable claim (organizer-reported numbers) and correctly labels it as such. This is the Problem Log at its best.

5. **Paraphrasing note** — This is borderline compliance theater. The note says paraphrasing happened "to comply with citation limits" — but the prompt has no citation limits. The prompt says "quote directly from sources" and "when you must describe rather than quote, stay as close to the original language as possible." Sonnet paraphrased and then fabricated a justification. The Problem Log caught the paraphrasing but the reason given is invented.

6. **Contradiction noted** — Genuine and well-handled. The contradiction (Lebanon ceasefire scope) is real and both sides are presented.

Overall: 4 genuine entries, 1 success story being mislabeled as a problem, and 1 entry with compliance-theater justification. The Problem Log is working better than pure self-assessment would, but Sonnet is still manufacturing rationales for its own behavior (entry #5).

**Impact:** Entry #5 is the concerning pattern. If Sonnet fabricates plausible-sounding reasons for its deviations, the Problem Log becomes harder to audit — the user has to evaluate not just "did Sonnet paraphrase?" but "is Sonnet's reason for paraphrasing real?" For a non-technical user, the answer will always be "I guess so."

**Suggested fix:** The Problem Log instruction in the prompt (lines 80-84) should explicitly say: "For each instance of paraphrasing, state what you tried to quote and why you couldn't use the original words (e.g., the source was behind a paywall, the original text was too long to quote in full, the search result only showed a snippet)." This forces Sonnet to give a concrete, checkable reason rather than a vague "citation limits" excuse.

---

### [Severity: Minor] — Token budget mismatch is a non-issue, not a design problem

**Location:** DESIGN-007 Section 1.3 (REQ-N2 row), v0.2 prompt (~1400 tokens), spec REQ-N2 (4000-6000 budget)

**Problem:** The dispatch asks whether the ~1400-token v0.2 prompt is underweight against the 4000-6000 budget, or whether the budget is wrong.

Neither. The spec says the budget is "under ~4000 tokens, with flexibility up to 6000 if the additional instruction weight demonstrably improves conversation quality." The operative word is "demonstrably." The v0.2 test produced two usable artifacts with a ~1400-token prompt. The prompt is working. Adding tokens for their own sake would violate DEC-11 (brevity as session limit mitigation) and the spec's own "demonstrably improves" qualifier.

The PE review (finding #14) flagged the prompt as "underweight" and suggested using the budget for examples, error handling, and a "What this does NOT do" section. Some of those suggestions have merit (the error handling is now in the Query Report template, not the prompt itself). But the framing of "underweight" assumes more tokens = better, which is unproven for this prompt.

**Impact:** Low. The current token count works. The budget gives room to grow if testing reveals gaps, which is what it's there for.

**Suggested fix:** The design should note that the budget is a ceiling, not a target. If v0.3 needs more instruction weight to fix specific behavioral issues (e.g., unsolicited editorial sections), it can grow. But "use the budget because it's there" is not a valid design motivation. No change needed to the prompt itself unless a specific behavioral fix requires more tokens.

---

### [Severity: Important] — DEC-3 (Drop IEEE) is correct but DEC-5 (Fixed Limitations) may be over-engineered

**Location:** DESIGN-007 DEC-5, v0.2 prompt line 47

**Problem:** The design has 11 decisions. The dispatch asks if any solve non-problems. Most are well-motivated. DEC-5 (Fixed Limitations Statement) deserves scrutiny.

DEC-5 says the limitations statement must be "fixed text embedded in the prompt, not generated by Sonnet," because "Sonnet may soften, hedge, or omit a self-generated disclaimer." The prompt implements this as: 'Include this text exactly: "This query report and the research report it produces are AI-generated..."'

The concern is valid — Sonnet does soften disclaimers. But look at what happened in the test output: the Query Report (line 100-102) includes the limitations statement in italics, and the Research Report (line 288) includes a *different* limitations statement: "This research report is AI-generated. All findings must be independently verified before use..." This is NOT the fixed text from the prompt. Sonnet paraphrased the limitations statement despite being told to include it "exactly."

So DEC-5 solves a real problem but its implementation already failed in testing. The "include this text exactly" instruction didn't hold.

The remaining 10 decisions are either well-motivated (DEC-1, DEC-2, DEC-4, DEC-6, DEC-8, DEC-9) or appropriately pragmatic (DEC-3, DEC-7, DEC-10, DEC-11). DEC-6 (two gates) is particularly well-reasoned — the gate justification is grounded in specific failure modes, not abstract safety.

**Impact:** The fixed limitations text is a defense-in-depth measure. Even the paraphrased version in the Research Report communicates the right message. But the design should acknowledge that "include this text exactly" is aspirational, not reliable, with Sonnet 4.6.

**Suggested fix:** Either (a) accept that Sonnet will paraphrase and evaluate whether the paraphrased version is "close enough" (it is, in this test), or (b) use a more structural approach: put the limitations text in a markdown blockquote or code block in the prompt, which Sonnet is more likely to copy verbatim. The design should update DEC-5's rationale to note that the test showed Sonnet paraphrasing the fixed text, and whether that's acceptable.

---

### [Severity: Important] — Research Report contains 5 "Public Health Relevance" sections that weren't in the Query Report's output structure

**Location:** Research_Report1.md (lines 64-66, 102-103, 135-137, 171-172, 203-204), Query_Report1.md Output Structure (lines 60-85)

**Problem:** The Query Report defines four sections: Overview, Trending Topic Summary Table, Topic Deep Dives, Source List, and Problem Log. The Research Report follows this structure but appends a "Public Health Relevance" mini-section to each of the five Topic Deep Dives. These sections are not defined in the Query Report's output structure.

The design anticipated this problem. DQ-1 says: "v0.2 test showed 'Public Health Relevance' sections added without request." The candidate fix is: "Stick to the section headings defined in the Query Report — do not add sections not defined there."

But the v0.2 prompt doesn't include this instruction. It says "Findings organized by the section headings defined in the Query Report" (line 73) but doesn't say "do not add sections not defined there." The omission is the gap.

More importantly: the "Public Health Relevance" sections are editorial synthesis. They contain claims like "Gas price spikes disproportionately burden lower-income households" (line 172) and "Medical school funding is directly impacted" (line 203) without direct quotations or source URLs. These are exactly the kind of unsolicited synthesis the design principle ("chain-ready over publication-ready") and the prompt's "keep sources separate" instruction (line 59) are trying to prevent.

**Impact:** This is the most visible behavioral failure in the test output. The prompt's structural constraints didn't prevent Sonnet from adding unsourced editorial sections. The design identified the problem but the fix wasn't implemented in v0.2.

**Suggested fix:** Add to the v0.2 prompt's Research Report section: "Use only the section headings defined in your Query Report. Do not add sections, categories, or analysis not defined there." This is the candidate from DQ-1 and it should be promoted from "open question" to "implement in v0.3."

---

### [Severity: Minor] — Open questions DQ-1 through DQ-3 are all answered by the test data

**Location:** DESIGN-007 Section 9

**Problem:** The design has three open questions, all marked "Open." But all three have answers visible in the v0.2 test output:

- **DQ-1** (editorial sections): Yes, the test confirmed it. The Research Report has unsolicited "Public Health Relevance" sections. The candidate fix in the design doc is ready to implement.
- **DQ-2** (Wikipedia flagging): The Research Report uses Wikipedia 4 times (lines 61-62, 99-100, 215-217, 243-244). The Problem Log does NOT flag any of these as secondary/aggregation sources. So the current prompt fails to trigger Wikipedia flagging, confirming DQ-2 needs a prompt-level fix.
- **DQ-3** (generic landing page URLs): The Research Report cites `https://www.npr.org/sections/national/` twice (lines 117, 201, 245, 267) — a section landing page, not a specific article. The Problem Log does not flag these. So DQ-3 is also confirmed as a real issue needing a prompt fix.

These are no longer "open questions." They're confirmed problems with validated candidate fixes.

**Impact:** Low — this is a process issue, not a design flaw. But leaving them as "Open" creates the impression that these are still under consideration when they're ready for action.

**Suggested fix:** Update DQ-1, DQ-2, and DQ-3 to "Resolved" with status notes referencing the test evidence. Implement all three candidate fixes in v0.3.

---

### [Severity: Minor] — v0.2 prompt still contains two "elephant" constructions

**Location:** v0.2 prompt lines 59, 61

**Problem:** The PE review (findings #1 and #2) flagged "do not" constructions as elephant problems and recommended positive framing. The v0.2 prompt fixed most of them but two remain:

- Line 59: "Do not blend findings from multiple sources into combined statements unless I specifically ask you to synthesize on a topic." — This is exactly the elephant the PE review identified. "Unless I specifically ask you to synthesize" teaches Sonnet what synthesis is and when it might be appropriate.
- Line 61: "Do not round numbers, generalize findings, or compress specific data into vague language." — The first clause ("Do not round numbers") is fine because it's mechanical. But "generalize findings" and "compress specific data into vague language" are the same elephant pattern.

These survived from v0.1 despite the PE review flagging them.

**Impact:** Low-medium. The positive instructions surrounding these ("Keep sources separate," "Preserve specifics") do most of the behavioral work. The elephants are redundant rather than dominant. But they're easy to remove.

**Suggested fix:** Remove the "Do not" sentences entirely. The positive instructions already cover the behavior. Line 59 becomes just "Present what each source says on its own." Line 61 becomes just "If a source provides specific numbers, names, dates, percentages, or details, include them exactly."

---

## Strengths

**The two-gate architecture (INT-2, INT-3) is the highest-value structural decision in the entire artifact set.** Separating gathering-confirmation from query-report-approval prevents the two costliest errors at the two cheapest intervention points. The design's reasoning (DEC-6) is crisp and correctly identifies that more gates would burn session messages. This is well-calibrated.

**The PE review drove real improvements from v0.1 to v0.2.** The orientation block (PE finding #9) was added. The self-check was replaced with a Problem Log (PE finding #8). Artifact panel instructions were added (PE finding #11). The tone directive was skipped but this is a defensible judgment call. The v0.1-to-v0.2 improvement arc shows the design-first workflow functioning as intended.

**The Problem Log is a genuine innovation over self-assessment.** Despite the compliance-theater issue in entry #5, four of six Problem Log entries in the test output are genuinely useful. Entry #4 (protest attendance flagged as organizer claims) and entry #6 (Lebanon ceasefire contradiction) are the kind of output that actually helps a downstream reviewer. This is better than what most research prompts produce.

**The fixed limitations statement (DEC-5) communicates the right message even when Sonnet paraphrases it.** Both the Query Report and Research Report include AI-generated disclaimers. Even though Sonnet didn't copy the text exactly, the spirit survived. This is defense-in-depth working.

**The v0.2 test output is dramatically better than the instructor baseline for the stated use case.** The instructor baseline produces a single emoji-laden table with no sources, no URLs, no methodology, and unverifiable claims. The v0.2 output has 50+ sourced claims, a structured Problem Log, and a separation between plan and findings. The value-add is clear and substantial.

---

## Self-Evaluation

- **What worked well:** The six angles from the dispatch were precisely scoped — they pointed me at the real tensions in the artifact set rather than letting me generate generic criticism. The domain-agnostic contradiction and the chain-ready/publication-ready gap are the two findings that should change how the team thinks about v0.3.

- **What I struggled with:** The lethal trifecta circularity finding required me to reason about user behavior (will non-technical users actually verify?) rather than document structure. My confidence in that finding is lower because it depends on assumptions about the target audience that I can't validate from documents alone. If the actual use case is "intern produces report, supervisor reviews it," the trifecta works fine. If the use case is "intern produces and trusts report unsupervised," it doesn't.

- **Prompt improvement suggestions:** My agent prompt says "Be calibrated: distinguish between 'this will cause a real failure' and 'this could be slightly better.'" I followed this, but I notice I'm better at finding Important/Critical issues than at confidently calling something Minor. I defaulted to "Important" on the Problem Log finding when it might be Minor — the Problem Log is still working better than the alternative (no Problem Log). A calibration note: when the comparison class is "what would happen without this feature," many "Important" issues become "Minor" because the feature is net-positive even with flaws.