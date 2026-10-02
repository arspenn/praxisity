## Skeptic Review

**Artifact:** SPEC-005 Agent Consultation System + DESIGN-004 + all implementation files
**Date:** 2026-03-29
**Dispatch Mode:** Mode 3: collaborative team

## Scope Challenges

### Verdict: Justified -- The core idea (multi-perspective review via subagents)

**What it does:** Lets you dispatch specialist agents to review planning artifacts from different angles before finalizing them.

**Why it's justified:** The D4C bug report and the v0.5.0 46-bug test provide real evidence that single-perspective review misses things. The consistency reviewer catching two contradictions during the design session itself is a live demonstration. The problem is real.

**Risk of removing:** You go back to single-perspective blind spots, which is the documented status quo problem.

---

### Verdict: Overcomplicated -- 8 agents where 4-5 would suffice

**What it does:** Defines 8 distinct agent personas across 4 categories.

**Why I'm challenging it:** Several agents have overlapping mandates or address problems that don't exist yet:

- **Critic vs. Skeptic overlap:** The Critic asks "what's wrong?" and the Skeptic asks "do we need this?" In theory these are distinct. In practice, when reviewing a spec, a good Critic will naturally question whether components are necessary (it's called "scope creep" in the Critic's own checklist, item 4). The Skeptic's differentiation is thin -- it's essentially the Critic with a YAGNI focus. You could merge these into a single evaluative agent with instructions to cover both quality and necessity.

- **User Advocate vs. Stakeholder overlap:** The User Advocate represents the person using the framework. The Stakeholder represents the person consuming the framework's outputs. For a solo developer building a framework they'll use themselves, these two audiences collapse. The Stakeholder's value shows up when reviewing deliverables (PDFs, reports), but for the current use case (reviewing specs and designs during framework development), the User Advocate alone covers this. The Stakeholder is premature until Praxisity has actual external-facing deliverables being reviewed by external people.

- **Designer vs. Prompt Engineer overlap in this context:** The Designer reviews architecture and component boundaries. The Prompt Engineer reviews dual-consumption quality. For a framework where every file is prompt infrastructure, these perspectives converge heavily. The Designer's "progressive loading tradeoffs" concern is also the Prompt Engineer's "signal-to-noise ratio" concern. During spec/design review (the current use case), one structural reviewer covering both architecture and prompt quality would be sufficient.

- **Consistency Reviewer earns its place.** Cross-document consistency checking is mechanically distinct from evaluative or perspective review. It caught real issues during the design session. Keep it.

- **Project Manager earns its place.** Feasibility and sequencing for a solo developer is a genuinely different lens than quality review. Keep it.

**Simpler alternative:** Start with 4-5 agents: Evaluator (merged Critic+Skeptic), User Advocate, Designer (merged with Prompt Engineer concerns), Project Manager, Consistency Reviewer. Add the split agents when you have evidence the merged ones produce blurred or insufficient feedback. The spec already says "roster designed for the current framework rework use case" and "roster expansion happens through use" -- apply that principle to the initial roster too.

**Risk of simplifying:** You lose some specificity in the evaluative and perspective dimensions. A merged Evaluator might not push as hard on YAGNI as a dedicated Skeptic would. But you also reduce: 8 agent files to maintain, 8 agent prompts to refine, 8 potential dispatch choices for the user to evaluate. The cognitive load of "which 3 of 8 agents do I pick?" is nontrivial.

---

### Verdict: Justified -- 3 dispatch modes

**What it does:** Single expert consult (Mode 1), parallel perspectives (Mode 2), collaborative team (Mode 3).

**Why it's justified:** I initially wanted to challenge this as overcomplicated, but the modes map to genuinely different platform mechanisms (Agent tool vs. TeamCreate) with genuinely different capabilities (snapshot vs. delta). Mode 1 is just "dispatch one agent" -- removing it means you always need the skill for even a quick question. Mode 3 is experimental and may not even be available, but when it is, persistent context across a work session is categorically different from snapshot dispatch. The decision gate between Mode 2 and Mode 3 is the right forcing function.

**Risk of removing any mode:** Mode 1 removal adds unnecessary friction to simple questions. Mode 3 removal loses delta-awareness, which is the capability that caught regressions in the D4C project. Mode 2 removal... you could argue Mode 2 is just "Mode 1 run N times," but the skill's synthesis guidance and lead review structure add real coordination value.

---

### Verdict: Justified -- Progressive loading (3-tier architecture)

**What it does:** Tier 1 (command pointers), Tier 2 (skill load), Tier 3 (agent files loaded at dispatch).

**Why it's justified:** The spec cites a real problem: the theory-of-change skill's ~90 lines of reference-verification methodology being loaded even when not relevant. The "don't think about elephants" argument is sound -- loading 8 agent personas into every session would prime the agent to think about consultation when it should be thinking about the task. The tiers map cleanly to "remind," "guide," and "execute."

**Risk of removing:** Without progressive loading, every command session carries the full weight of the consultation system. For a `/build` session that never uses agents, that's pure noise.

---

### Verdict: Overcomplicated -- The template and reporting infrastructure

**What it does:** 3 templates (context block, session report, collab-mode), a naming convention, a lead review format, "instructions received" verification sections, reconstitution notes, per-agent assessments.

**Why I'm challenging it:** This is bureaucracy scaffolding for a system that hasn't been used once. The spec says "build what's needed now, expand from experience." The reporting infrastructure assumes:

1. That you'll need to verify what instructions agents received (the "telephone game" concern). This is a real concern for Mode 3 persistent teams but not for Mode 1/2 where the dispatch prompt is right there in your conversation history.

2. That you'll need to reconstitute teams across sessions frequently enough to warrant a template section for it. This is speculative. You might just re-dispatch with the same context block.

3. That lead reviews synthesizing across all agents need a structured format. For Mode 2, the main agent already sees all the returns. A lead review adds value only if you need to persist the synthesis for a future session that won't have the original context.

**Simpler alternative:** Start with: agents write reports (they need persistence). Drop the lead review template -- the main agent can write a synthesis if it wants to, it doesn't need a template to do it. Drop the "instructions received" section from agent reports -- it's verification theater until you actually encounter context passing failures. Drop reconstitution notes until you've actually needed to reconstitute a team. Keep the context block template -- it genuinely helps structure dispatch prompts.

**Risk of simplifying:** If you do hit context passing issues, you'll wish you had the verification section. But you can add it then. The cost of adding a template section later is near zero. The cost of maintaining unused template sections now is also low in isolation, but it contributes to the overall complexity budget that makes this system feel heavyweight.

---

### Verdict: Premature -- Agent persistent memory (`memory: project`)

**What it does:** Agents accumulate knowledge across sessions in `.claude/agent-memory/<name>/`.

**Why I'm challenging it:** The spec marks this as COULD priority, which is appropriate. But the design treats it as a default (`memory: project` in every agent frontmatter). For a system that hasn't been used once, every agent starts accumulating memories from day one. You have no idea what memories will be useful. The memory system could accumulate noise that degrades future performance rather than improving it. The research paper referenced in your own project memory notes that agent MD files have "marginal/negative impact on performance with 20%+ cost increase."

**Simpler alternative:** Omit `memory: project` from the initial agent files. Add it to specific agents after you've used them enough to know that cross-session knowledge accumulation actually helps. The agent files are version-controlled -- adding one line to frontmatter later is trivial.

**Risk of removing:** You lose the ability for agents to learn from early sessions. But "learn" assumes the memories are useful. Without curation, they may not be.

---

### Verdict: Unnecessary -- README.md with "Future Agents" section

**What it does:** Lists 5 planned-but-not-built agents (cold-reader, domain-expert, editor, devil's-advocate, integrator).

**Why I'm challenging it:** This is speculative design documented as if it's a roadmap. The spec says "roster expansion happens through use and self-evaluation, not speculative design." The README contradicts this by speculatively designing future agents. It also creates a "don't think about elephants" problem: any agent or user reading the README is now primed with 5 future agents that don't exist, which could influence recommendations ("we should use the domain-expert for this" when no domain-expert exists).

**Simpler alternative:** Remove the "Future Agents" section entirely. When a new agent is needed, design it then. The README should describe what exists, not what might exist.

**Risk of removing:** You lose the brainstorming notes about future agents. If those ideas are valuable, capture them in a planning document, not in the README that agents read as context.

---

## What Earns Its Complexity

1. **The core concept** of dispatching specialist subagents for multi-perspective review is well-motivated by real evidence (D4C bug report, v0.5.0 test).

2. **The 3-tier progressive loading** is a sound architectural choice that solves a documented context bloat problem.

3. **The 3 dispatch modes** map to genuinely different platform capabilities with genuinely different tradeoffs. The decision gate between snapshot and delta is valuable.

4. **Native Claude Code subagent format** is the right call -- building a custom format would be pure overhead.

5. **The consult-team skill as guidance, not control flow** is the right design philosophy for a system where the agent needs to adapt.

6. **The decision to have agents write their own reports** is sound -- it's the minimal persistence mechanism needed for outputs to survive context compression.

7. **The consistency-reviewer agent** is the most clearly justified of the 8, having demonstrated its value during the design session itself.

## Bottom Line

The system is about 60% well-justified and 40% premature optimization. The core architecture (progressive loading, dispatch modes, skill-as-guidance) is sound. The agent roster is overbuilt for the current use case. The reporting infrastructure assumes failure modes that haven't been observed. The persistent memory defaults to accumulating data before there's evidence it helps.

**If I could cut one thing:** Reduce to 5 agents. The merged agents can always be split later when evidence shows the merged perspective is too blurred. Splitting is cheap. Maintaining 3 extra agents from day one has ongoing cost in prompt refinement, decision complexity, and context budget.

**If I could cut two things:** Also drop `memory: project` from agent frontmatter until you've used the system enough to know what memories are worth keeping.

**What I would NOT cut:** The 3-tier loading, the 3 dispatch modes, the skill, the context block template, agents writing their own reports. These earn their complexity.

## Self-Evaluation

- **What worked well:** Having the full spec, design, skill, all 8 agent files, and all 3 templates in context gave me enough material to make specific, grounded challenges rather than generic "this seems like a lot" objections. The strongest challenges (agent count, premature memory) connect back to the project's own stated principles.

- **What you struggled with:** It's hard to challenge the 3-mode architecture when the modes genuinely map to different platform mechanisms. My initial instinct was "3 modes is too many" but the evidence changed my mind. I may have been too generous here -- a stronger skeptic might argue that Mode 3 should be deferred entirely until the experimental feature stabilizes.

- **Prompt improvement suggestions:** My prompt tells me to check the dependency chain for components that exist only to support other components that might not be needed. I did this for the templates but could have been more systematic about it. A checklist approach ("for each component, what breaks if you remove it?") might produce more thorough coverage. Also, my prompt says "respect the user's stated goals -- challenge the approach, not the mission" but doesn't give guidance on how to handle cases where the approach IS the mission (the consultation system is both the approach and the thing being built).
