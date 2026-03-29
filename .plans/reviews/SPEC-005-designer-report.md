## Designer Review

**Artifact:** DESIGN-004 Agent Consultation System (+ SKILL.md, agent files, templates)
**Date:** 2026-03-29
**Dispatch Mode:** Mode 3: collaborative team

## Instructions Received

Evaluate the architecture of the Praxisity Agent Consultation System. Specifically: does the 3-tier progressive loading work, are the component boundaries clean, is the layered prompt assembly well-composed, does the skill's relationship to agents and templates make sense, and are there hidden coupling issues.

Materials reviewed:
- `.plans/designs/004-agent-consultation-system.md` (full document)
- `.claude/skills/consult-team/SKILL.md`
- `.claude/skills/consult-team/templates/context-block.md`
- `.claude/skills/consult-team/templates/collab-mode.md`
- `.claude/skills/consult-team/templates/session-report.md`
- `.claude/agents/README.md`
- All 8 agent files in `.claude/agents/`
- `.plans/specs/005-agent-consultation-system.md` (partial, for cross-reference)

## Architecture Assessment

### [Impact: Structural] -- The 3-tier progressive loading is sound and well-motivated

The tiering model (Tier 1: command pointers, Tier 2: skill on demand, Tier 3: agent files per dispatch) is the right architecture for this problem. Each tier loads strictly more content than the previous one, and the loading triggers are clear:

- Tier 1 is always present but tiny -- a reminder, not instructions.
- Tier 2 loads only when the user or main agent decides multi-agent consultation is needed.
- Tier 3 loads only the specific agents dispatched, not the full roster.

This means a `/build` session touches zero consultation content, and a `/spec` session that dispatches 3 of 8 agents loads only those 3 persona files. The context budget scales with actual usage, not potential usage. This is a clean progressive disclosure pattern.

One architectural subtlety worth noting: the design correctly observes that the platform loads the agent file as the system prompt (not injected into the task prompt). This means Tier 3 content occupies system prompt space, which is architecturally distinct from the task prompt where the context block lands. The layering respects this platform boundary rather than fighting it.

### [Impact: Structural] -- Layered prompt assembly composes well with one caveat

The three-layer stack (agent file + collab-mode + context block) is well-designed:

- **Agent file (immutable, all modes):** Standalone persona. Functions without any appended content.
- **Collab-mode (Mode 3 only):** Adds session awareness without touching the persona. Single shared file avoids 8x duplication.
- **Context block (all modes):** Per-dispatch situational orientation.

The layers are independent and stackable. The agent file never assumes collab-mode exists. Collab-mode never assumes a specific agent identity. The context block never assumes either layer's content. This means any combination works: agent alone (Mode 1 ad-hoc), agent + context (Mode 1/2 structured), agent + collab + context (Mode 3).

**Caveat -- delivery ordering in Mode 3:** The design specifies that the task prompt for Mode 3 is `[collab-mode content] + [context block]`. This means the agent reads collab-mode instructions before the task specifics. This is the right order (establish operating mode before presenting the task), but the design doesn't state *why* this ordering matters. If an implementer reverses it (context block first, then collab-mode), the agent might anchor on the task and treat collab-mode as an afterthought. The SKILL.md does get the ordering right in its Mode 3 section (line 59: "include the collab-mode content... followed by the context block"), but it reads as incidental rather than intentional.

**Recommendation:** Add a one-line rationale to INT-1's Mode 3 contract: "Collab-mode precedes context block so the agent establishes its operating mode before receiving the task."

### [Impact: Coupling] -- Skill-to-agent coupling is minimal and well-bounded

The skill (SKILL.md) references agents only through the platform's available agent types and their descriptions. It does not embed persona content, does not hardcode agent file paths, and does not maintain a separate index. The `description` field in each agent's frontmatter doubles as the index entry. This is an elegant design choice that eliminates a synchronization problem: there is no separate index file that could drift out of sync with the actual agent files.

The skill references templates by path (`.claude/skills/consult-team/templates/`), which is a direct, non-abstract dependency. This is appropriate -- templates are co-located with the skill and change together.

### [Impact: Minor] -- Agent file structure is consistent but the "Project Context" section introduces mild coupling

All 8 agent files follow the same 4-section structure (Identity, Reasoning Approach, Output Format, Self-Evaluation embedded in Output Format). However, the design document (DATA-1, line 448-454) specifies the sections as: Identity, Reasoning Approach, Output Format, Self-Evaluation. In the actual files, most agents embed Self-Evaluation within the Output Format section rather than as a standalone section. Additionally, 7 of 8 agents include a "Project Context" section and a "Critical Rules" section not listed in the DATA-1 schema. The actual files have: Identity, Project Context, Reasoning Approach, Critical Rules, Output Format (with embedded self-eval).

This is not a structural problem -- the files work well as they are. But it is a design-to-implementation drift. The DATA-1 schema says 4 sections; the files have 5 distinct sections with self-eval folded into one of them. If the design is meant to be the source of truth for the format, it should reflect what was actually built. If the files are authoritative, the DATA-1 schema should be updated.

The "Project Context" section across agents is nearly identical boilerplate ("You operate within the Praxisity framework, which follows a design-first workflow..."). This is a reasonable trade-off: it costs ~2-3 lines per agent but ensures each agent is fully standalone without assuming prior context. The slight per-agent variation (e.g., project-manager mentions "solo developer", stakeholder mentions "deliverables") is good -- it tailors the framing to the perspective.

### [Impact: Structural] -- The decision gate is the skill's highest-value component

The snapshot vs. delta decision gate in the skill is structurally important. It sits at the right chokepoint: after the user decides they want multi-agent input, but before they commit to a dispatch mode. The skill frames this as a question ("Will the agents need to see how the work changes during this session?") rather than a flowchart, which is consistent with DEC-5 (skills as guidance, not control flow).

The default advice ("When in doubt, start with Mode 2") is pragmatic. Mode 2 is cheaper, simpler, and sufficient for most review gates. The escalation path ("You can always escalate to Mode 3") is noted but the reverse direction is not: once you've started a Mode 3 team, you can't easily downgrade mid-session. This asymmetry is acknowledged implicitly but could be stated more directly.

### [Impact: Coupling] -- Report interface (INT-3) has a healthy multi-writer design

The report interface allows both agents and the main agent to write to `.plans/reviews/`. The naming convention (`[ARTIFACT-ID]-[agent-name]-report.md` vs. `[ARTIFACT-ID]-lead-review.md`) prevents collisions. Agents own their reports; the lead owns the synthesis. No writer depends on another writer's output to produce its own.

The "Instructions Received" section in agent reports is a clever verification mechanism. The main agent can compare what it sent (the context block it composed) against what the agent reports receiving. This catches context-passing failures without adding any runtime machinery -- it's a human-auditable check built into the document format.

### [Impact: Minor] -- Tool restriction boundary is appropriate but could tighten

All agents are configured with `tools: Read, Grep, Glob, Write`. The design states agents should write only to `.plans/reviews/`. However, the `Write` tool itself is not path-restricted -- an agent could theoretically write anywhere. This is a soft boundary enforced by prompt instructions, not a hard platform constraint.

This is acceptable for the current scope. The agents are review agents, not implementation agents; their prompts consistently direct output to `.plans/reviews/`. But if the roster expands to include agents with broader mandates, the lack of path-level Write restrictions could become a real coupling risk (an agent accidentally overwriting a planning artifact, for instance). The design acknowledges this in COMP-1: "Broader tool access may be considered in future iterations but is out of scope per SPEC-005 Section 8." This is the right call for now.

### [Impact: Minor] -- Mode 3 fallback path is documented but thin

The skill states: "This requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` to be enabled and Claude Code v2.1.32+. If unavailable, fall back to Mode 2." The fallback is correct but does not address the semantic gap: Mode 2 cannot catch regressions across edits, which is Mode 3's primary value. A user who wanted delta-awareness and gets snapshot-only may not realize the degradation.

This is not a structural flaw -- it's a UX concern at the boundary of Mode 2 and Mode 3. A single line in the fallback guidance noting "Mode 2 fallback loses delta-awareness; consider breaking work into smaller review gates to partially compensate" would help.

## What Composes Well

**The immutable-persona / mutable-context separation.** This is the single best architectural decision in the system. Agent files never change at dispatch time. Customization is always appended, never injected. This eliminates an entire class of prompt-drift bugs where edits to one dispatch contaminate future dispatches.

**Single collab-mode.md shared across all agents.** Avoids 8 copies of Mode 3 instructions. The content is genuinely mode-specific (not persona-specific), so sharing it is correct. If a future need arises for per-agent collab behavior, the layering supports it: add an optional per-agent collab extension between collab-mode.md and the context block. But don't build that until it's needed.

**Description-as-index.** Using the frontmatter `description` field as both the platform's agent description and the skill's index entry eliminates a synchronization problem. There is exactly one place to update when an agent's purpose changes.

**Document-based persistence.** All continuity lives in files (`.plans/reviews/`), never in terminal state. This means session crashes, context compression, and agent shutdowns don't lose work. The architecture correctly treats the terminal session as ephemeral and the file system as durable.

**Self-evaluation as a feedback loop.** Every agent includes self-evaluation in its output format. This is not just a reporting feature -- it's an architectural feedback mechanism. Self-evaluation data accumulated across reviews provides concrete evidence for prompt refinement. The `memory: project` setting means agents can build on this across sessions.

## Self-Evaluation

- **What worked well:** Reading all files before forming judgments. The architecture is coherent enough that patterns emerged from the full picture that wouldn't have been visible from individual files. The layered prompt assembly, in particular, only reveals its elegance when you see how agent files, collab-mode, and context blocks interact across all three modes.

- **What you struggled with:** Distinguishing between design intent and implementation reality. The DATA-1 schema says one thing; the actual agent files do something slightly different (extra sections, embedded self-eval). I flagged this as a minor issue, but I'm not fully confident whether the design document was meant to be updated after implementation or whether the files are the authoritative version. A designer reviewing a design document against its implementation always faces this ambiguity.

- **Prompt improvement suggestions:** My agent prompt says to evaluate "progressive loading tradeoffs" but doesn't give me guidance on how to assess whether the indirection cost of a tier is justified. I evaluated this qualitatively ("Tier 2 loads only when needed -- good"), but a more structured framework for assessing tier boundaries would strengthen my reviews. Something like: "For each tier boundary, assess: (1) what content is saved by not loading it, (2) what capability is lost until it loads, (3) whether the trigger for loading is clear and reliable."
