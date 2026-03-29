# SPEC-005 Spot Report: Agent File Review (Fresh Eyes)

**Reviewer:** Spot (no prior project context)
**Date:** 2026-03-29
**Scope:** All 8 agent files in `.claude/agents/`

---

## Per-Agent Summaries

### 1. consistency-reviewer.md

**What it says:** This agent cross-checks planning documents for contradictions -- mismatched IDs, wrong counts, stale references, terminology drift. It reads all linked artifacts and flags where they disagree.

**What's clear:**
- The checklist of what to cross-reference (requirement IDs, component IDs, file paths, counts, terminology, scope boundaries, version references) is concrete and actionable.
- The "What you ignore" section draws a sharp line -- not an editor, not a product manager.
- The "never assume something is true because it makes sense" rule is strong.
- The output format is specific and usable.

**What's confusing:**
- The description mentions "one-shot reviewer" vs. "persistent teammate" modes, but there is no explanation of what those modes are or how dispatch differs between them. I'd have to know the framework to parse that.
- "Dispatch Mode: [Mode 1/2/3]" appears in other agents' output templates but not this one. Yet the description implies multiple modes exist. Inconsistency in whether this agent has modes or not.
- "Update your agent memory" -- what is agent memory? How does the agent write to it? There is no instruction on format or location, just a directive to do it.

---

### 2. critic.md

**What it says:** Adversarial reviewer that stress-tests planning artifacts for weaknesses, contradictions, unstated assumptions, and scope creep. Unlike the consistency-reviewer, it evaluates the logic and soundness of the content itself, not just cross-document alignment.

**What's clear:**
- The distinction from consistency-reviewer is evident: critic judges whether the content is sound, not whether documents agree.
- "Every problem you raise should include a path to fixing it" is a strong guardrail against drive-by criticism.
- The severity calibration instruction ("distinguish between 'this will cause a real failure' and 'this could be slightly better'") is useful.

**What's confusing:**
- "Dispatch Mode: [Mode 1/2/3]" in the output template -- what are modes 1, 2, and 3? No definition anywhere in this file.
- The overlap with the skeptic is not addressed. The critic says it looks for "scope creep" and the skeptic says it's the "YAGNI enforcer." A reader unfamiliar with the project would not know when to use one vs. the other based on these files alone.
- Same "update your agent memory" instruction with no explanation.

---

### 3. skeptic.md

**What it says:** Challenges whether something should exist at all. The YAGNI enforcer. Asks "do we even need this?" rather than "is this well-done?"

**What's clear:**
- The framing against the critic is explicit and helpful: "Where the Critic asks 'what's wrong with this?', you ask 'do we even need this?'"
- The distinction between "unnecessary" and "premature" is good -- it gives the agent a vocabulary for nuance.
- "Respect the user's stated goals -- challenge the approach, not the mission" prevents the agent from going rogue.

**What's confusing:**
- Same undefined "Dispatch Mode: [Mode 1/2/3]".
- The "What you ignore" list says "Quality of implementation" and "Whether it's technically feasible." So who covers feasibility? The project-manager talks about "what's realistic" but from a scheduling/capacity lens, not a technical feasibility lens. There may be a gap, or I may be misunderstanding scope boundaries.
- Same undefined "agent memory" directive.

---

### 4. user-advocate.md

**What it says:** Represents the end user -- a solo practitioner learning structured AI workflows. Evaluates whether the framework helps users learn and grow, not just produce output. Holds the standard of "use the system to build the user."

**What's clear:**
- The user persona is well-defined: solo practitioner (student, developer, researcher, consultant).
- "If a feature is powerful but opaque, it fails" is a clear, testable standard.
- The onboarding friction lens is specific and useful.
- The "transferable skills vs. framework dependency" criterion is distinctive and not something other agents cover.

**What's confusing:**
- Same undefined dispatch modes.
- "Does this teach a useful concept or just add a step?" -- how does the agent determine this without knowing the user's skill level? The persona is broad (student to consultant). Different users would have very different answers.
- Same undefined "agent memory" directive.

---

### 5. stakeholder.md

**What it says:** Represents someone consuming the framework's outputs -- a professor, client, collaborator, or reviewer. Evaluates whether deliverables serve their intended audience. Does not use the framework; judges what it produces.

**What's clear:**
- Clean separation from user-advocate: user-advocate is about the person using the framework, stakeholder is about the person receiving its outputs.
- "Framework jargon leaking into external-facing content" is a specific, actionable concern.
- "Always identify the audience before evaluating" is a good forcing function.

**What's confusing:**
- Same undefined dispatch modes.
- How does the stakeholder know who the intended audience is? The output template has an "Intended Audience" field, but the instructions don't say how to determine it. Does the dispatching mechanism provide this? Does the artifact declare it?
- Same undefined "agent memory" directive.

---

### 6. designer.md

**What it says:** Evaluates architecture -- component boundaries, interfaces, data flow, dependencies, coupling, and composition. Thinks about progressive loading tradeoffs and minimal surface area.

**What's clear:**
- The focus on boundaries and interfaces (not implementation) is well-defined.
- The progressive loading evaluation criteria are specific to this framework and would be hard to get from another agent.
- "When something is too tightly coupled, propose the specific cut point" is concrete.

**What's confusing:**
- Same undefined dispatch modes.
- "Progressive loading" is used without definition. The description says "content enters agent context only when needed, organized in tiers" but doesn't explain what tiers are or how loading works. A reader with no project background would not understand this.
- The name "designer" might cause confusion -- in many contexts, "designer" means UI/UX. This is really an architecture reviewer. The description clarifies it, but the name alone could mislead.
- Same undefined "agent memory" directive.

---

### 7. project-manager.md

**What it says:** Tracks scope, dependencies, sequencing, and feasibility for a solo developer. Guards against redesigning everything at once.

**What's clear:**
- The solo developer constraint is stated upfront and shapes all the reasoning -- "there is no team to parallelize work."
- The dependency graph analysis instructions are concrete.
- "Respect the user's ambition -- your job is to make it achievable, not to shrink it" is a good calibration.
- The distinction between "too much" (unhelpful) and "here's what to cut or defer" (helpful) is strong.

**What's confusing:**
- Same undefined dispatch modes.
- "How long would this realistically take for one person?" -- an AI agent has no reliable basis for estimating human work duration. This is an instruction the agent likely cannot follow well, but it's presented as a core reasoning step.
- Same undefined "agent memory" directive.

---

### 8. prompt-engineer.md

**What it says:** Evaluates whether files are optimized for dual consumption -- human-readable AND effective as AI prompts. Checks signal-to-noise ratio, instruction clarity, "don't think about elephants" problems, and cross-session consistency.

**What's clear:**
- The dual-consumption framing is distinctive and well-explained: "every file is both the output of a prompt and the input to a future prompt."
- The "don't think about elephants" concept is named and explained (content that primes unwanted behavior by mentioning what NOT to do).
- The distinction between "confusing to humans" and "ambiguous to AI" is useful.
- "Context budget -- every line loaded into an agent's context has a cost" is a concrete constraint.

**What's confusing:**
- Same undefined dispatch modes.
- The "Drift" issue type in the output format -- what does it mean? Ambiguity, Noise, Elephants, and Clarity are self-explanatory or explained. Drift is not.
- Same undefined "agent memory" directive.

---

## Cross-Cutting Observations

### What's clear across all agents

1. **Consistent structure.** Every file follows the same pattern: frontmatter, identity, project context, reasoning approach, what to ignore, critical rules, output format. Easy to compare and navigate.

2. **Sharp scope boundaries.** Each agent has a "What you ignore" section that explicitly carves out what's NOT its job. This prevents overlap and gives each agent a clear lane.

3. **Constructive orientation.** Every agent is told to acknowledge when things are good, not manufacture criticism. This is a strong design choice that prevents review fatigue.

4. **Self-evaluation requirement.** Every output template includes a self-evaluation section with "prompt improvement suggestions." This creates a feedback loop where agents critique their own prompts.

### What's confusing across all agents

1. **Dispatch modes are undefined.** Every output template references "Dispatch Mode: [Mode 1/2/3]" but no agent file explains what the modes are. This is the single most confusing element across the entire set. Are the modes defined elsewhere? If so, these files don't reference where.

2. **"Agent memory" is unexplained.** Every file ends with "Update your agent memory with..." but none of them explain what agent memory is, where it lives, how to write to it, or what format it should take. The frontmatter has `memory: project` which might be related, but the connection is not stated.

3. **The `model: inherit` and `category` frontmatter fields are undocumented.** What does "inherit" inherit from? What do categories "meta," "evaluative," "structural," and "perspective" control? These might be framework internals, but from a cold read they're opaque.

4. **No dispatch or orchestration instructions.** None of these files explain how agents get invoked, what context they receive, or who/what sends them work. The files define what each agent does but not how they fit into a workflow.

5. **Critic vs. Skeptic boundary.** While the skeptic explicitly differentiates itself from the critic, the critic's scope includes "scope creep" which overlaps with the skeptic's entire purpose. If both review the same artifact, their scope creep findings could conflict or duplicate.

6. **Technical feasibility gap.** The skeptic ignores "whether it's technically feasible." The designer ignores "scope decisions." The project-manager thinks about "what's realistic" but from a capacity lens. The critic is closest to a feasibility reviewer but doesn't claim that role explicitly. It's unclear who owns "this design is technically impossible/impractical."

7. **"Progressive loading" and "tiers" are framework jargon.** The designer and prompt-engineer reference these concepts without defining them. Someone dispatching these agents would need to already understand the framework to evaluate whether the agents are doing their job on this dimension.
