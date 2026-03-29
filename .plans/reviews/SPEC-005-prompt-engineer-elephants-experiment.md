## Prompt Engineer Self-Experiment: "What You Ignore" Sections

**Date:** 2026-03-29
**Method:** Read all 10 files from this session's work, observing my own processing behavior when encountering scope-boundary sections vs. files without them. This is introspective reporting on attention patterns, not a consistency review.

**Files reviewed:**
- SPEC-005 (spec)
- DESIGN-004 (design)
- DIP-004 through DIP-007 (4 DIPs)
- SKILL.md (consult-team skill)
- context-block.md, session-report.md, collab-mode.md (3 templates)

---

## Experiment 1: Does "What you ignore" pull attention toward excluded topics?

**What I observed:** When I re-read the agent files during my initial review and then read the broader corpus here, the "What you ignore" sections did not strongly pull my attention toward the excluded topics *as concepts*. Reading "Quality of implementation -- that's the Critic's job" in the skeptic's file did not make me start thinking about implementation quality in a distracting way.

What it *did* do was activate awareness of the other agents as entities. After reading the skeptic's "What you ignore" section, I was primed to think about the Critic, the Designer, and the Consistency Reviewer as named actors in the system. When I then read the spec and design documents, I found myself mapping concepts to agent names ("this is what the Designer would evaluate") rather than just processing the content on its own terms.

**Assessment:** My original report overstated the "elephants" risk for the excluded *topics*. The real effect is subtler: these sections prime the agent with a mental model of the full team roster and their responsibilities. For an agent that is supposed to be narrowly focused on its own perspective, this team-awareness may be the actual interference vector -- not "thinking about code quality" but "thinking about what the Critic would say about code quality."

**Severity downgrade:** The raw "don't think about elephants" framing from my initial report was too strong. The sections are not causing agents to do the excluded work. They are causing agents to be aware of the broader team context, which may or may not be desirable.

---

## Experiment 2: Navigating files WITH vs. WITHOUT "What you ignore"

**Files with explicit scope boundaries (agent files):**
The "What you ignore" sections gave me a clear sense of each agent's lane *before* I started processing their reasoning approach. When I read the designer's file, the exclusion list ("whether the scope is right," "user experience," "specific implementation details") immediately told me the boundaries. I knew what the designer would NOT talk about, which helped me predict the shape of its output.

**Files without scope-exclusion sections (templates, skill, DIPs, spec, design):**
These files use a different mechanism for scope: "DO/DO NOT" blocks in DIPs, "Out of Scope" in the spec, and implicit scoping through section structure in the skill and templates.

Comparing my experience:
- **DIP scope boundaries (DO/DO NOT):** These were *more* effective as navigation aids than the agent "What you ignore" blocks. The DIP format presents scope as positive assertions first ("DO: create context block template"), then exclusions second ("DO NOT: create agent definition files"). I found myself reading the "DO" block, forming a clear picture of scope, and then using the "DO NOT" block only as a verification pass. The ordering matters -- positive first, then negative as confirmation.
- **Spec "Out of Scope":** Similar pattern -- it comes after the full requirements section, so by the time I reached it, I already had a positive model of what was in scope. The out-of-scope section confirmed rather than defined.
- **Skill (SKILL.md):** No explicit exclusion section at all. The skill opens with "Mode 1 is not covered here" and then proceeds entirely with positive guidance. I found this the cleanest to process -- I was never told what to avoid, only what to do. My attention never wandered toward Mode 1 specifics while reading the Mode 2/3 guidance.
- **Templates:** No scope exclusions. Pure structural guidance. Very clean to process.

**Key observation:** The files without "What you ignore" sections were not harder to navigate. They achieved scope clarity through structure and positive framing. The agent files are the only documents in the entire system that define scope primarily through negation.

---

## Experiment 3: Is the cross-agent referencing useful or diluting?

**The cross-references ("that's the Critic's job"):**

These serve two distinct functions that should be evaluated separately:

**Function 1: Deconflicting overlapping concerns.** When the skeptic says "Quality of implementation -- that's the Critic's job," it is drawing a boundary between "is this necessary?" (skeptic) and "is this well-made?" (critic). These are genuinely adjacent concerns that could bleed into each other. The cross-reference is useful for boundary maintenance.

**Function 2: Building team awareness.** Each agent ends up knowing the entire team roster and each member's responsibility. For a Mode 1 single-consult agent, this team awareness is entirely unnecessary -- the agent does not need to know about the Critic, Designer, or anyone else. For a Mode 3 collaborative teammate, team awareness might actually be useful (they can direct observations to the right colleague).

**Observation during processing:** When I was reading the agent files as standalone documents (as a Mode 1 agent would encounter them), the cross-references made me curious about the other agents and their perspectives. I found myself wanting to compare the skeptic's scope with the critic's scope to verify the boundary was drawn correctly. This is a meta-concern that has nothing to do with the skeptic's actual job of evaluating necessity. The cross-references invited system-level thinking when the agent should be doing content-level analysis.

When I read collab-mode.md, which has NO cross-agent references, I experienced no such pull. It says "maintain your perspective even when it conflicts with other teammates" without naming those teammates or their concerns. This was effective -- it established the social norm (hold your ground) without specifying against whom.

---

## Conclusions

### What my initial report got right:
- The "What you ignore" sections do create team-roster awareness that is unnecessary for Mode 1 agents
- Positive scoping ("Your scope is limited to X") would be cleaner than negative scoping ("What you ignore: Y")
- The collab-mode.md pattern (acknowledge teammates exist without naming their specific concerns) is better prompt engineering

### What my initial report got wrong:
- I overstated the "elephants" effect. These sections are not causing agents to do the excluded work. They are priming team awareness, not topic activation. The difference matters for the fix.
- I framed this as a universal problem. In Mode 3 (collaborative team), some degree of cross-agent awareness might actually help coordination. The problem is Mode 1 specific -- solo agents loaded with team context they cannot use.

### Recommendation (revised from initial report):

**Do not remove the scope boundary concept.** It is useful. The DIP files, the spec, and even the skill all have scope boundaries and they work. The issue is the specific implementation in agent files.

**Reframe from negation to positive scoping, but preserve the cross-references in a reduced form.** Instead of:

```
What you ignore:
- Quality of implementation -- that's the Critic's job
- Cross-document consistency -- that's the Consistency Reviewer's job
- Whether it's technically feasible -- that's the Designer's job
```

Use:

```
Your scope is limited to: necessity, scope justification, and complexity-to-benefit ratio.

Adjacent concerns handled by other agents: implementation quality (Critic), cross-document consistency (Consistency Reviewer), technical feasibility (Designer).
```

This preserves the deconfliction function (agents know where their lane ends) while reducing the "team roster" priming. The cross-references move from a prominent list the agent processes as instructions to a subordinate note it can reference if needed. The positive scope statement comes first, establishing the agent's identity before mentioning anyone else.

**Consider whether Mode 3 agents should get the cross-references at all.** Collab-mode.md could include a "your teammates and their domains" section, making the cross-references load-on-demand rather than baked into every agent file. This would mean Mode 1 agents (who read only their own file) get no team awareness, while Mode 3 agents (who also get collab-mode) get the full roster. This aligns the information with who needs it.

---

## Self-Evaluation

- **What worked well:** Reading the full 10-file corpus forced me to compare how scope is handled in different document types. The agent files' approach stood out as the outlier -- not because it is broken, but because every other document in the system does scope differently and arguably better. This comparative evidence is stronger than the theoretical argument I made in my initial report.

- **What I struggled with:** Honest introspection about my own processing is unreliable. I cannot truly observe whether the "elephants" effect is happening because the observation itself changes the process. My report of "what I noticed while reading" is a reconstruction, not a recording. The strongest evidence is the structural comparison (how do other files handle scope?) rather than the introspective claim (what happened in my attention?).

- **Prompt improvement suggestions:** For self-experiments like this, the prompt should specify a concrete behavioral test rather than relying on introspection. For example: "After reading the skeptic's file, immediately review the spec. Track whether your first 5 observations are about necessity/scope (skeptic's domain) or about other concerns (implementation quality, consistency, feasibility). Count them." A measurable outcome would be more trustworthy than narrative self-report.
