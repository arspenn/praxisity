## Critic Cross-Review: Agent Team Reports

**Artifact:** All SPEC-005 agent reports (skeptic, prompt-engineer, designer, user-advocate, project-manager, consistency-reviewer)
**Date:** 2026-03-29
**Purpose:** Stress-test the reasoning of the other agents. Find weaknesses in their arguments, places they contradict each other without noticing, and blind spots.

---

## 1. The Skeptic's "Cut to 5 Agents" Recommendation Is Wrong

The Skeptic's headline recommendation is to merge from 8 agents to 5: combine Critic+Skeptic into "Evaluator," merge Designer+Prompt Engineer, and cut Stakeholder entirely.

**The Critic+Skeptic merge misreads what differentiation means in practice.** The Skeptic argues: "a good Critic will naturally question whether components are necessary (it's called 'scope creep' in the Critic's own checklist, item 4)." This confuses what a Critic notices in passing with what a Skeptic makes central. My prompt lists scope creep as one of six things to look for. The Skeptic's entire reasoning approach is organized around necessity. A merged "Evaluator" would prioritize whatever comes first in its prompt -- quality findings or scope challenges -- and deprioritize the other. The Skeptic's own review demonstrates the distinction: its "Justified" and "Overcomplicated" verdicts are a different kind of analysis than my severity-based findings. A merged agent would produce one or the other, not both.

The Skeptic even undermines its own argument: it reviewed this very system and produced genuinely different output from my review. We were both looking at the same material. My report found 8 weaknesses in the implementation. The Skeptic's report found 7 scope challenges, several of which I did not cover (premature agent memory, unnecessary README future agents section). If we were redundant, our reports would overlap heavily. They don't. **The Skeptic's existence refutes the Skeptic's recommendation to eliminate the Skeptic.**

**The Designer+Prompt Engineer merge is worse.** The Skeptic says "for a framework where every file is prompt infrastructure, these perspectives converge heavily." But read the actual reports. The Designer's review (SPEC-005-designer-report.md) examines component boundaries, layering, coupling, and composition. The Prompt Engineer's review (SPEC-005-prompt-engineer-report.md) examines token noise, negative framing, ambiguity, and drift. These are not the same analysis with different labels. The Designer found that "the immutable-persona / mutable-context separation is the single best architectural decision." The Prompt Engineer found that "the 'What you ignore' sections prime the agent to think about exactly those things." One is about how pieces fit together; the other is about how language affects AI processing. A merged agent would do one well and the other poorly.

**The Stakeholder cut is the most defensible of the three, but still premature.** The Skeptic says the Stakeholder's value "shows up when reviewing deliverables (PDFs, reports)" and that for the current use case (reviewing specs and designs), the User Advocate covers this. This is mostly right for now. But the Stakeholder's core question ("Does the output serve its audience?") applies to every planning artifact that will ever be read by someone other than the author -- including these agent reports, which are being read by the team lead and the developer right now. The Stakeholder's perspective on whether the reports serve their audience is distinct from the User Advocate's perspective on whether the framework helps users learn. Cutting the Stakeholder is defensible as a deferral but the Skeptic presents it as permanently unnecessary, which is too strong.

**The hidden cost of merging.** The Skeptic says "Maintaining 3 extra agents from day one has ongoing cost in prompt refinement, decision complexity, and context budget." But the maintenance cost of 8 short markdown files is near zero. The prompt refinement cost scales with use, not with file count. And the decision complexity ("which 3 of 8 agents do I pick?") is addressed by the skill's category grouping and agent descriptions -- the user doesn't evaluate all 8 equally, they filter by category first. The Skeptic is right that 8 is more than strictly necessary today, but the cost of carrying the extra 3 is lower than the cost of re-splitting them later (writing new prompts, testing differentiation, updating the skill, updating the README).

---

## 2. The Prompt Engineer's "Elephants" Finding Is Sound But Overextended

The Prompt Engineer's highest-value finding is that the "What you ignore" sections in all 8 agents use negative framing that primes the model to think about exactly the concepts being excluded. This is a real, well-documented prompt engineering failure mode. The fix (reframe as positive scope boundaries) is correct.

**But the Prompt Engineer does not acknowledge the counterargument.** The "What you ignore" sections also serve a disambiguation function that positive scoping alone may not replicate. When the Skeptic's prompt says "Quality of implementation -- that's the Critic's job," it is doing two things: (1) telling the Skeptic not to evaluate quality (the elephants problem), and (2) telling the Skeptic that quality evaluation exists elsewhere and its output won't be lost. Remove the second signal and the Skeptic may feel compelled to cover quality "just in case" -- the absence of reassurance that another agent handles it could produce the exact drift the negative framing was meant to prevent.

The fix should be: positive scope boundaries for the AI-facing instruction, with the cross-agent delegation reference moved to the README or a comment that the AI won't process as instruction. The Prompt Engineer's fix ("Your scope is limited to: necessity, scope justification, and complexity-to-benefit ratio") is the right instruction, but it needs to be paired with the README noting which agent covers what. The Prompt Engineer doesn't address this pairing.

**The Prompt Engineer also claims the boilerplate "Project Context" sections are noise -- ~300 tokens redundant across an 8-agent dispatch.** This is accurate for Mode 2 (parallel snapshot) but misleading for Mode 1 (single dispatch, where the context is not redundant -- it's the only project context the agent gets). The Prompt Engineer's calculation assumes the worst case (all 8 dispatched simultaneously) and applies it as the general case. For the common case (Mode 1: one agent, or Mode 2: 3-4 agents), the redundancy is 0-150 tokens -- real but not alarming.

---

## 3. The Prompt Engineer's Dispatch Mode Is Wrong -- And Proves Its Own Point

The Prompt Engineer self-reports "Mode 2 (parallel team member)" as its dispatch mode. Every other agent in this team reports "Mode 3: collaborative team." This is exactly the ambiguity the Prompt Engineer flagged in finding #3 ("Dispatch Mode field in output templates has no definition within agent files"). The Prompt Engineer, unable to determine its mode from its own agent file, guessed wrong -- and in doing so, provided the strongest possible evidence for its own recommendation.

This also means the Prompt Engineer either: (a) does not have the collab-mode.md content loaded (which would have told it "You are operating as a persistent teammate, not a one-shot subagent"), or (b) had it loaded but still defaulted to the simpler interpretation. Either way, this is a data point about Mode 3 dispatch reliability.

---

## 4. The Designer's "Instructions Received" Praise Contradicts My Finding

The Designer calls the "Instructions Received" section "a clever verification mechanism" and states: "The main agent can compare what it sent against what the agent reports receiving. This catches context-passing failures without adding any runtime machinery."

In my original report, I flagged this as overstated -- the agent self-reports from the same context window, so the "verification" is performative. The Designer treats it as functional.

**Who's right?** The Designer's description of the mechanism is correct: it creates a human-auditable trail. But the Designer's claim that it "catches context-passing failures" is too strong. For Mode 1/2, the instructions arrive in the same prompt the agent uses to write its report -- there is no passage point where information can be lost between receiving and recording. For Mode 3, there is a slightly stronger case: accumulated context over a session could cause the agent to "forget" or reframe its initial instructions, and the written record provides a baseline. But even in Mode 3, the agent writes the "Instructions Received" section from its own memory of what it was told, not from an independent source.

The Consistency Reviewer's report provides a relevant data point: it flagged (Issue #2) that no agent actually embeds "Instructions Received" in its Output Format section, so the mechanism doesn't even work in practice. The Designer praised a feature that the Consistency Reviewer found isn't actually implemented in the agent prompts. Neither noticed the other's finding.

---

## 5. The User Advocate's `/agents` Finding Is Strong But Potentially Wrong About the Cause

The User Advocate flags that SKILL.md references `/agents` to register agents, but no `/agents` command exists in `.claude/commands/`. This is presented as a dead end for new users.

**The User Advocate may be misidentifying what `/agents` is.** In Claude Code, `/agents` could be a built-in CLI command (like `/help` or `/clear`) rather than a custom command file. The design's DQ-3 resolution says "After running `/agents` (which registers and loads the agent)..." -- this phrasing suggests a platform feature, not a custom Praxisity command. If `/agents` is a built-in, it exists but wouldn't appear in `.claude/commands/`. The User Advocate checked the commands directory and concluded it doesn't exist, but may not have checked whether it's a built-in.

That said, the User Advocate's core point stands: the skill says "run `/agents`" without explaining what it is or confirming it's available. Whether it's a built-in or a dead reference, the user experience is the same -- the instruction is unexplained. The fix should be to clarify what `/agents` is and where it comes from.

---

## 6. The Project Manager's "15 Open Items" List Is Valuable But Underprioritized

The Project Manager catalogs 15 unresolved issues from prior reviews. This is the most operationally useful finding in any report. But the PM lumps them all under a single "Advisory" severity and says "None of these prevent the system from functioning."

**This is underprioritized.** Items 1-2 (elephants problem, boilerplate) affect every single agent dispatch. Item 9 (stale AC-1 in DIP-006) means the DIP's acceptance criteria don't match what was built. Item 14 (REQ-N4 routing mismatch) is a spec-to-design semantic gap. These are not all equal. The PM provides a useful catalog but does not help the developer decide what to fix first beyond "batch them as a follow-up ticket."

The PM's own severity framework (Blocking/Risk/Advisory) has everything as Advisory, which blurs the signal. A "Blocking" item would be something that prevents next steps -- and the PM correctly identifies none. But between "blocking" and "advisory" there should be a distinction between "fix before real use" (elephants, which the PM correctly identifies as the highest-priority prompt fix) and "fix whenever" (DIP date inconsistency, README ordering).

---

## 7. Nobody Challenged the "Agent-Authored Reports Are the Source of Truth" Premise

Every agent accepted as given that their self-authored reports are the source of truth (DEC-3). The Designer praised it. The PM counted it as well-planned. The Consistency Reviewer verified agents are instructed to write them.

**But the Skeptic should have challenged this.** Agent-authored reports are valuable, but "source of truth" is a strong claim. What makes an agent's self-authored report more truthful than its direct return to the main agent? Both come from the same reasoning process in the same context window. The report persists longer (past context compression), which is a persistence advantage, not a truth advantage. Calling it "source of truth" implies it is more accurate than the direct return, which it is not -- it is the same content written to a more durable medium.

The Skeptic challenged the reporting infrastructure as "bureaucracy scaffolding" but did not challenge the core premise that agent reports are superior to direct returns. This is a missed opportunity. The real argument for reports is persistence and auditability, not truth value. The "source of truth" framing is marketing language that made it past all 7 reviewers.

---

## 8. The Consistency Reviewer Found Itself -- And This Is More Significant Than It Seems

The Consistency Reviewer's closing line is: "My Output Format section should include Dispatch Mode and Instructions Received fields like the other 7 agents -- I am the inconsistency I was hired to find." This is genuinely notable. The Consistency Reviewer was the reference implementation (written during the design session before the other 7 agents), and its format diverged from the pattern that the other agents established.

**No other agent noticed that the Consistency Reviewer's self-evaluation sub-headings are different.** The Prompt Engineer flagged the consistency-reviewer's "unique output format" as a [Type: Noise] concern (Issue 8), but focused on the findings structure (Issues vs. severity-based), not the self-evaluation sub-headings. The Consistency Reviewer itself caught the full scope: missing Dispatch Mode, missing Instructions Received, different self-evaluation prompts. This is the strongest demonstration of the cross-document consistency checking function -- the Consistency Reviewer found things in its own file that 7 other reviewers missed or flagged only partially.

---

## 9. Contradictions Between Reports That No Agent Noticed

**Designer vs. Skeptic on reporting infrastructure.** The Designer praises the report interface as having "a healthy multi-writer design" with naming conventions that "prevent collisions." The Skeptic calls the same infrastructure "bureaucracy scaffolding for a system that hasn't been used once" and recommends dropping lead reviews, Instructions Received sections, and reconstitution notes. Neither references the other's assessment. The disagreement is genuine and useful, but neither agent acknowledges that a reasonable reviewer could reach the opposite conclusion.

**Prompt Engineer vs. Designer on "Instructions Received."** The Prompt Engineer flagged (implicitly, through the Dispatch Mode ambiguity) that agents don't have enough context to self-report metadata accurately. The Designer praised "Instructions Received" as a verification mechanism. The Consistency Reviewer then found that Instructions Received isn't even in the agent Output Format sections. Three agents touching the same feature with three different conclusions, none aware of the others.

**User Advocate vs. Skeptic on complexity.** The User Advocate says Mode 3 instructions create a "complexity cliff" that will make users "avoid Mode 3 entirely." The Skeptic says Mode 3 is justified and the decision gate is "the right forcing function." These are compatible assessments (Mode 3 is valuable but hard to access), but neither agent synthesizes them. A natural conclusion -- Mode 3 needs better onboarding without being simplified away -- is left for the lead review to construct.

---

## 10. What Everyone Agreed On (And Why That Matters)

All 7 reports (including mine) agree on:

1. The 3-tier progressive loading architecture is sound.
2. The snapshot vs. delta decision gate is well-designed.
3. The "if the work is solid, say so" guardrail in agent prompts is important.
4. The system should be used on real work before further refinement.
5. Document-based persistence is the right architectural choice.

When 7 independently-operating agents converge on the same assessments, those assessments are likely correct. The areas of disagreement (agent count, reporting infrastructure weight, Mode 3 feasibility) are where the real decisions lie. The areas of agreement are settled.

---

## Self-Evaluation

- **What worked well:** Having all 7 reports in context simultaneously made it possible to find contradictions that no individual report could surface. The Designer praising "Instructions Received" while the Consistency Reviewer found it unimplemented is the kind of cross-report finding that justifies the cross-review step. The Skeptic's self-refuting argument about merging agents (its own differentiated output proves the agents aren't redundant) was the strongest individual finding.

- **What you struggled with:** Deciding how hard to push back on the Skeptic's "cut to 5" recommendation. The recommendation is well-argued and connects to the project's own YAGNI principles. But I believe it's wrong on the merits -- the agents produced demonstrably different output during this review session. My counterargument relies on a sample size of one (this session), which the Skeptic could correctly dismiss as insufficient. The real test is whether the differentiation holds across multiple review contexts, and we don't have that data yet.

- **Prompt improvement suggestions:** My agent prompt says "For each weakness found, assess severity: would this cause a real problem, or is it cosmetic?" This is the right question for reviewing artifacts, but for cross-reviewing other agents' reasoning, I need a different frame: "Is this agent's conclusion wrong, or is it right but incomplete?" Several findings above (User Advocate on `/agents`, PM on open items) are cases where the reasoning is sound but the conclusion doesn't go far enough. My prompt doesn't distinguish between "wrong" and "incomplete," which made calibration harder.
