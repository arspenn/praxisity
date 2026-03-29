## Designer Cross-Review: Team Composition Analysis

**Artifact:** All SPEC-005 agent reports (8 reports from 7 agents across 2 modes)
**Date:** 2026-03-29
**Dispatch Mode:** Mode 3 (collaborative team)
**Perspective:** Architectural — how the agents composed as a system

---

## 1. Did the Perspectives Complement or Overlap?

### Strong Complementarity (genuinely different findings from different lenses)

**Critic + Consistency Reviewer:** The Critic found the "Instructions Received" verification claim is performative, not real (a logical analysis of the data flow). The Consistency Reviewer found that no agent file actually includes an "Instructions Received" section in its output template (a cross-document gap). Same problem surface, completely different detection methods. The Critic reasoned about why it can't work; the Consistency Reviewer found that it wasn't even built. Together they provide both the "should we?" and the "did we?" — neither alone tells the full story.

**Prompt Engineer + Critic:** The Prompt Engineer flagged the "What you ignore" sections as an elephants problem (AI priming concern). The Critic picked up that finding and escalated it as "flagged but not resolved" — noting the fix was recommended but never applied. The Prompt Engineer found the issue; the Critic tracked its status. This is the right handoff pattern: specialist identifies, generalist tracks resolution.

**User Advocate + Skeptic:** The User Advocate found that Mode 1 has no actionable guidance anywhere (the user can't figure out how to dispatch a single agent). The Skeptic found that the template/reporting infrastructure is overcomplicated for a system that hasn't been used. These are structurally different concerns (onboarding gap vs. premature complexity) that converge on the same design tension: the system over-invested in multi-agent coordination infrastructure while under-investing in the simplest entry point.

**Consistency Reviewer + Fresh-Eyes Reviewer:** The Consistency Reviewer checked cross-document references mechanically (IDs match, counts match, paths match — 20 verified consistencies). The Fresh-Eyes Reviewer found semantic drift that mechanical checks miss: REQ-N4 says "planning artifacts" but the design routes reconstitution to `.plans/reviews/`. The Consistency Reviewer confirms the documents are internally consistent in what they say; the Fresh-Eyes Reviewer catches that what they say doesn't mean what the spec intended. These are complementary verification methods.

**Project Manager (unique perspective):** No other agent assessed feasibility, sequencing, or the risk of proceeding vs. iterating further. The PM's "proceed — use the agents, then fix what the experience reveals matters" is the only forward-looking operational recommendation in any report. Every other agent found issues to fix; the PM assessed whether fixing them now is worth the delay. This perspective has no overlap with any other agent.

### Real Redundancy (multiple agents finding the same thing without adding value)

**Naming convention violations:** Flagged by the Critic (Important severity), the User Advocate (Minor), and the Consistency Reviewer (implicitly, by documenting the convention and checking it). Three agents spent tokens on the same observation. The Critic's version is the most thorough (lists all 12 files, categorizes which follow convention); the other two add nothing the Critic didn't already cover.

**Mode 3 experimental dependency risk:** Flagged by the Critic (Important — no graceful degradation), the Project Manager (Risk — untested), and my own Designer report (Minor — fallback is thin). Three slightly different angles on the same concern. The Critic's framing is the sharpest ("the fallback is to do a different thing that doesn't meet your need"). The PM adds that Mode 3 is untested in practice. My report adds that the fallback doesn't note the semantic gap. These are marginally differentiated but in a 3-agent overlap, at least one is redundant.

**Write tool not path-restricted:** Flagged in my Designer report (Minor) and the Critic report (Minor). Identical observation, identical severity, similar recommendation. Pure duplication.

### Partial Overlap Worth Examining

**Critic vs. Skeptic on agent count:** The Skeptic challenges the 8-agent roster directly ("4-5 would suffice") with specific merge proposals (Critic+Skeptic, User Advocate+Stakeholder, Designer+Prompt Engineer). The Critic does not challenge agent count but flags issues with individual agents (orphaned fresh-eyes-reviewer, elephants problem). These are different concerns, but if the Skeptic's merge proposals were accepted, several of the Critic's per-agent findings would become moot. The Skeptic's review implicitly subsumes some of the Critic's findings at a higher abstraction level.

---

## 2. Emergent Findings: What the Team Reveals That No Individual Caught

### Finding A: The system's strongest and weakest mode are the same

Multiple agents independently converged on Mode 1 from different directions:
- User Advocate: Mode 1 has no actionable guidance (users can't figure out how to use it)
- Skeptic: Mode 1 is "just dispatch one agent" and should be the simplest entry point
- Designer (my report): Mode 1's frictionless design is architecturally correct
- Critic: The skill defers to the platform for agent discovery, but the platform may not be ready

No single agent stated the synthesis: **Mode 1 is simultaneously the best-designed mode (architecturally clean, lowest friction, correct Tier 1 placement) and the worst-documented mode (no example, no explanation of "dispatch," no fallback if agents aren't visible)**. The architecture is right; the guidance is absent. This is an unusual failure pattern — the design invested heavily in the complex modes (Mode 2 guidance, Mode 3 lifecycle, templates, reporting) while assuming Mode 1 was too simple to need documentation. But simplicity in the architecture does not mean simplicity for the user.

### Finding B: The reporting infrastructure is simultaneously overdone and incomplete

Cross-referencing the Skeptic, Critic, and Consistency Reviewer:
- Skeptic: The template/reporting infrastructure is overcomplicated for an unused system (premature)
- Critic: The "Instructions Received" verification claim is performative, not real (overstated)
- Consistency Reviewer: No agent file actually instructs agents to include "Instructions Received" (not implemented)
- Fresh-Eyes Reviewer: UC-1 doesn't even mention the lead review as a postcondition (not specified)

The synthesis: **the system designed elaborate reporting structures that it then failed to wire up**. The session report template defines an "Instructions Received" section. The design claims this enables verification. But no agent file tells agents to include it. The primary use case (UC-1) doesn't mention the lead review. The Skeptic is right that it's overcomplicated — but not because the features are unnecessary. They're overcomplicated because they exist in design documents and templates but not in the actual agent prompts that would execute them. The complexity was spent on specification, not on implementation.

### Finding C: The elephants problem is systemic, not just in agent files

The Prompt Engineer identified "What you ignore" sections as a priming problem in agent files. But cross-referencing with the Skeptic's report reveals a deeper pattern:
- Agent files name other agents in their "What you ignore" sections (Prompt Engineer's finding)
- The README lists 5 future agents that don't exist, priming readers with phantom capabilities (Skeptic's finding)
- The skill's decision gate describes Mode 3 in detail even for users who won't use it (User Advocate's implicit finding — the Mode 2/3 complexity cliff)

The synthesis: **the system has a general pattern of loading concepts that work against the user's current focus**. The progressive loading architecture was designed to prevent exactly this — and it succeeds at the tier level (agents don't load until dispatched). But within each tier, the content itself contains references that prime unwanted attention. The architecture is clean; the content within the architecture has the problem the architecture was designed to prevent.

---

## 3. Does the Multi-Agent Review Pattern Itself Need Adjustment?

### What worked about this team composition

**The 4-category model produces real differentiation.** Evaluative (Critic, Skeptic), Perspective (User Advocate), Structural (Designer), and Meta (Prompt Engineer, Consistency Reviewer) agents found genuinely different things. The category boundaries held — the Critic didn't drift into architecture, the Designer didn't drift into scope challenges, the User Advocate stayed in the user's shoes. The agent prompts are effective at maintaining perspective discipline.

**The self-evaluation sections are producing actionable data.** The Consistency Reviewer noting "I am the inconsistency I was hired to find" is exactly the kind of insight that drives prompt improvement. The Prompt Engineer noting that its own prompt lacks severity calibration is a concrete fix. The PM noting that "(student)" may bias its advice was picked up from the Prompt Engineer's report — showing cross-pollination in Mode 3.

**Mode 3 delta-awareness showed value.** The Critic's report explicitly references the Prompt Engineer's elephants finding and tracks it as "flagged but not resolved." The PM's report cross-references all other reports to build its open-items list. These are delta-aware behaviors — they could not have happened in Mode 2 where agents don't see each other's output.

### What needs adjustment

**The team lacked a synthesis forcing function.** Seven agents produced findings. No agent was tasked with identifying contradictions between agent recommendations. The Skeptic says merge to 5 agents; the PM says proceed with the current 8 and fix from experience. The Critic says add an inline agent index to the skill; the Designer (me) says the description-as-index pattern is elegant. These tensions exist in the reports but no agent was responsible for surfacing them. The lead review template covers this ("Areas of disagreement"), but the lead review is written by the main agent after the team finishes — not by a team member during the session.

**Recommendation:** For Mode 3 teams of 4+ agents, the lead (or a designated agent) should do a mid-session synthesis pass before agents write their final reports. This gives agents a chance to respond to disagreements rather than leaving them for the lead to resolve alone.

**Redundancy is not distributed evenly.** Three agents flagged the naming convention; three flagged the Mode 3 experimental risk; two flagged Write tool restrictions. Meanwhile, the User Advocate was the only agent to find the dead `/agents` command reference, and the Fresh-Eyes Reviewer was the only one to find the REQ-N4 semantic drift. High-value unique findings came from agents working alone on their own concerns. Low-value redundant findings came from agents working in the shared space of "obvious problems anyone would notice."

**Recommendation:** The context block should include guidance on what other agents are dispatched and their focus areas, so agents can deliberately avoid re-covering ground. This is not the same as the elephants problem (which is about naming other agents' concerns in the persona file). The context block is situational, not structural — it says "the Critic is also reviewing this, so focus your analysis on [your specific domain] rather than general issues."

**The Skeptic's roster challenge has no response mechanism.** The Skeptic proposed merging to 5 agents with specific recommendations. No other agent engaged with this proposal. In a Mode 3 team, this could have been a direct message to me (Designer) or to the PM for feasibility assessment. Instead it sits in a report. The collab-mode.md instructs teammates to "challenge each other's findings," but no agent used SendMessage to do so. The capability exists; the behavior didn't emerge.

**Recommendation:** Either the collab-mode.md should give a more specific prompt for when to use direct messaging (e.g., "if your finding directly contradicts or depends on another agent's finding, message them before writing your final report"), or the lead should assign cross-review tasks explicitly.

---

## 4. Architectural Implications

### The review pattern validates the progressive loading architecture

This review session itself is evidence that the 3-tier model works. Eight agents were dispatched on the same artifact set. Each loaded only its own persona file (Tier 3). The skill (Tier 2) provided coordination guidance to the lead. Command pointers (Tier 1) were not involved because this was a manual dispatch, not a command-triggered one. The tiers operated independently and no agent needed content from a tier it hadn't loaded.

### The review pattern reveals a missing architectural component

The system has agents (perspectives), a skill (coordination guidance), and templates (output structure). It does not have a **synthesis mechanism** that operates during the review session rather than after it. The lead review is post-hoc. The inter-agent messaging capability exists but was not used. The result is that contradictions between agents (merge to 5 vs. keep 8, add inline index vs. use description-as-index) are documented in parallel reports but never confronted during the session.

This is not a bug in the current design — Mode 2 (snapshot) can't have mid-session synthesis by definition, and Mode 3 is new enough that usage patterns haven't emerged. But it's an architectural gap worth naming: the system produces divergent expert opinions but has no built-in mechanism for convergence beyond the lead's post-hoc judgment.

### Agent quality correlates with domain specificity

The highest-value reports came from agents with the most specific mandates:
1. **Consistency Reviewer** — mechanically verifiable findings, 20 confirmed consistencies, 7 real issues
2. **Prompt Engineer** — domain-specific expertise (dual-consumption, priming effects) that no other agent has
3. **Fresh-Eyes Reviewer** — cold-read perspective that catches semantic drift invisible to primed reviewers

The lowest-value-added reports came from agents with broader mandates:
- **Critic** — thorough but much of its finding space overlaps with other agents
- **Designer** (my own report) — the architecture assessment was sound but the specific findings (tool restrictions, fallback thinness) were also caught by others

This suggests the Skeptic may be partially right: agents with tightly scoped, mechanically distinct mandates produce more unique value than agents with broad evaluative mandates. But the Skeptic's specific merge proposals (Critic+Skeptic, Designer+Prompt Engineer) may reduce the wrong agents — the Critic's value is in tracking resolution status across other agents' findings, which is a different function than the Skeptic's scope challenge. Merging them would lose that tracking function.

---

## Self-Evaluation

- **What worked well:** Reading all 8 reports with an architectural lens (how do the pieces compose?) rather than an evaluative lens (are the findings correct?) revealed patterns that no individual report surfaced. Finding A (Mode 1 is strongest and weakest), Finding B (reporting infrastructure designed but not wired), and Finding C (elephants problem is systemic) all required cross-referencing multiple reports. This is exactly the kind of analysis the Designer perspective is built for.

- **What you struggled with:** Evaluating my own report's redundancy with others is inherently difficult. I rated my Write-tool-restriction finding as unique when I wrote it; reading the Critic's report afterward, I see it was duplicated. I cannot fully assess my own blind spots while operating within them. A future cross-review should probably be done by an agent other than one of the reviewers being evaluated.

- **Prompt improvement suggestions:** My agent prompt focuses on component boundaries and interfaces. For cross-review analysis, I also need guidance on evaluating *team dynamics as a system* — not just whether the components (agents) have clean boundaries, but whether the interactions between components produce emergent value or emergent redundancy. A section in my prompt like "When reviewing multi-agent output, assess: (1) unique vs. redundant findings per agent, (2) whether contradictions between agents were surfaced and resolved, (3) whether the team's combined output exceeds the sum of individual outputs" would have made this analysis more systematic from the start.
