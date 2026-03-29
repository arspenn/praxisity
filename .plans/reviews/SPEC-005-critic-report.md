## Critic Review

**Artifact:** SPEC-005 Agent Consultation System (spec, design, skill, 8 agents, templates)
**Date:** 2026-03-29
**Dispatch Mode:** Mode 3 (collaborative team)

---

## Findings

### [Severity: Critical] -- Orphaned agent memory directory with no corresponding agent file

**Location:** `.claude/agent-memory/fresh-eyes-reviewer/` (6 files, actively populated), `.claude/agents/` (no `fresh-eyes-reviewer.md`)

**Problem:** There is a `fresh-eyes-reviewer` directory under `.claude/agent-memory/` containing project memories, feedback records, and naming convention notes -- but no corresponding agent file exists in `.claude/agents/`. The README roster lists 8 agents and 5 future agents; "fresh-eyes-reviewer" is not among either list. Two review files in `.plans/reviews/` are attributed to it (`SPEC-005-fresh-eyes-reviewer-report.md`, `SPEC-005-fresh-eyes-reviewer-report-2.md`), indicating it was used during this session.

**Impact:** This appears to be a renamed or removed agent that left behind persistent state. The memory files will never be loaded by any agent (since no agent claims that name), but they occupy a namespace that could collide if a future agent with a similar name is created. The review reports reference an agent that doesn't exist in the system, making them misleading for anyone reviewing the `.plans/reviews/` directory. This is exactly the kind of artifact that the Consistency Reviewer was designed to catch -- and it was missed.

**Suggested fix:** Either (a) create a `fresh-eyes-reviewer.md` agent file if it's intended to exist (the README's "Future Agents" section mentions a `cold-reader` that sounds similar), or (b) delete the orphaned memory directory and note in the review reports that they were produced by a pre-roster prototype agent.

---

### [Severity: Critical] -- The system cannot actually verify what it claims to verify

**Location:** SPEC-005 REQ-F8, DESIGN-004 DEC-3, INT-3 contract, session-report.md template "Instructions Received" field

**Problem:** A core design claim is that agent-authored reports enable "verification of context passing fidelity" -- the main agent can compare what it sent against what the agent says it received. This is stated in DEC-3, reinforced in INT-3, and baked into the session report template.

But this verification is performative, not real. The agent receives its instructions as part of the prompt. When the template asks it to record "the customization block you were given," the agent is summarizing its own input from memory -- the same context window it's already operating within. There is no independent attestation mechanism. The agent could hallucinate, summarize incorrectly, or omit parts of its instructions, and the "verification" would surface only the most egregious discrepancies. For Mode 2 (snapshot subagents), the agent returns its results *and* writes the report in the same context window -- there is literally no point at which information could be lost between receiving instructions and recording them.

The real risk this design tries to address (telephone-game summarization loss between agents and the main agent) is genuine. But the mechanism for addressing it (self-reported instruction recording) does not deliver the verification guarantee the documents claim.

**Impact:** The spec and design overstate a capability, which creates false confidence. A future developer trusting this "verification" as a quality gate will be misled. This is the kind of assumption that survives single-perspective review -- the logic *sounds* right until you trace the actual data flow.

**Suggested fix:** Downgrade the claim from "verification" to "transparency." The Instructions Received section is still useful -- it creates an audit trail and helps humans understand what the agent was asked. But call it what it is: a self-reported record, not a verifiable cross-check. Remove or soften language like "enables verification of context passing fidelity" in DEC-3 and INT-3. If actual verification matters, the main agent should write the instructions it sent to a separate file (not through the agent) and compare against the agent's report -- but this is probably not worth building now.

---

### [Severity: Important] -- Review file naming convention is already violated by the system that created it

**Location:** DESIGN-004 COMP-2 naming convention, INT-3 contract, session-report.md template, `.plans/reviews/` actual contents

**Problem:** The naming convention defined across all documents is `[ARTIFACT-ID]-[agent-name]-report.md`. The session report template even gives examples: `SPEC-005-critic-report.md`, `DESIGN-004-lead-review.md`. But the actual `.plans/reviews/` directory tells a different story:

Files following the convention:
- `SPEC-005-fresh-eyes-reviewer-report.md`
- `SPEC-005-fresh-eyes-reviewer-report-2.md`
- `SPEC-005-prompt-engineer-report.md`

Files NOT following the convention:
- `review-dip004-implementation-2026-03-29.md`
- `review-dip004-implementation-round2-2026-03-29.md`
- `review-dip005-agents-2026-03-29.md`
- `review-dip006-skill-2026-03-29.md`
- `review-dip-consistency-2026-03-29.md`
- `review-dip-consistency-round2-2026-03-29.md`
- `review-rename-consistency-2026-03-29.md`
- `agent-prompt-comparison-report.md`
- `test-team-dispatch-2026-03-29.md`

9 of 12 files violate the convention that the system explicitly defines. This was already flagged by the consistency reviewer in `review-dip005-agents-2026-03-29.md` (Issue 1) -- and the consistency-reviewer's own Output Format was fixed to match the convention. But the historical files were left as-is, and more importantly, new files continued to be created under the old convention *after* the naming standard was established.

**Impact:** The naming convention exists in the documents but was never enforced in practice. If tooling, scripts, or grep patterns are built to match `[ARTIFACT-ID]-[agent-name]-report.md`, they will miss the majority of existing reviews. This undermines the design's stated rationale for standardized naming ("any tooling or grepping against `.plans/reviews/` will pattern-match on `[ARTIFACT-ID]-[agent-name]-report.md`").

**Suggested fix:** This is a bootstrapping artifact -- the reviews were written before and during the convention being established. Accept the historical files as-is. But add a note in the session report template or the skill that "reviews written before SPEC-005 implementation may use different naming conventions." The real fix is that going forward, all agents and the lead agent must actually follow the convention.

---

### [Severity: Important] -- Skill defers entirely to platform for agent index, but the platform listing may not be available

**Location:** SKILL.md "Available Agents" section, DESIGN-004 DQ-3 resolution

**Problem:** The skill says: "Praxisity agents are registered as native Claude Code subagents in `.claude/agents/`. When loaded, they appear in your available agent types with their descriptions." It then adds: "If agents don't appear in your available types, run `/agents` to register them."

DQ-3 in the design documents that native dispatch failed on first attempt because the agent file was created mid-session and not loaded. The resolution was "run `/agents`." But `/agents` is not a Praxisity command -- it is presumably a Claude Code built-in. The skill's guidance is: "if the platform's listing doesn't work, use a different platform feature to fix it."

The skill provides zero agent information inline. If the platform listing is unavailable or stale (new session, `/agents` not run, edge case), the main agent has no fallback within the skill itself. It must either run `/agents` (platform-dependent), read `.claude/agents/README.md` (which provides a roster but not descriptions), or grep the agent files directly.

**Impact:** The decision to defer entirely to the platform's native listing is architecturally clean but creates a brittleness. A single skill load should be sufficient to know what agents are available. Currently, the skill requires the platform to be in the right state, plus potentially a README read, to provide what REQ-F3 says the skill itself should provide: "available agents (index from frontmatter)."

**Suggested fix:** Include a minimal agent index in the skill as a fallback -- just name, category, and one-line description. This is <30 lines. The skill already says "see README.md for the full roster" -- replace that with the actual roster. The platform's native listing is still the preferred path for dispatch, but the skill should be self-contained for selection.

---

### [Severity: Important] -- "Don't think about elephants" problem flagged but not resolved

**Location:** All 8 agent files, "What you ignore" sections; SPEC-005-prompt-engineer-report.md (Issue 2)

**Problem:** The Prompt Engineer report explicitly flagged this as a significant issue: every agent's "What you ignore" section names the other agents' concerns, which primes the model to think about exactly those things. The report proposed a specific fix: "Reframe as positive scope boundaries rather than negations."

The current agent files still contain the negation framing. The Prompt Engineer's feedback was recorded in `.plans/reviews/` but not incorporated. Example from the Skeptic: "Quality of implementation -- that's the Critic's job. Cross-document consistency -- that's the Consistency Reviewer's job." This tells the Skeptic about the Critic's concerns and the Consistency Reviewer's concerns in the act of saying "don't think about them."

**Impact:** Every agent dispatch loads content that works against the agent's focus. For a Mode 2 dispatch of 3-4 agents, each agent is primed with awareness of the others' domains. This is exactly the "don't think about elephants" failure mode that the progressive loading architecture was designed to prevent -- but it's embedded in the agent files themselves.

**Suggested fix:** Apply the Prompt Engineer's recommendation. Replace "What you ignore" sections with positive scope definitions. The Skeptic's section becomes: "Your scope is limited to: necessity, scope justification, and complexity-to-benefit ratio." Remove cross-references to other agents' names and roles from the agent files -- put those in the README where they serve human readers without priming the AI.

---

### [Severity: Important] -- Mode 3 depends on an experimental feature with no degradation path beyond "use Mode 2"

**Location:** SPEC-005 REQ-F11, DESIGN-004 Section 2.3, SKILL.md "Mode 3: Collaborative Team"

**Problem:** Mode 3 requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` and Claude Code v2.1.32+. The skill notes: "If unavailable, fall back to Mode 2." The design risk table also says: "Skill includes fallback guidance to use Mode 2."

But Mode 2 and Mode 3 solve fundamentally different problems. Mode 2 is snapshot; Mode 3 is delta-aware. The entire Section 2.2 architecture motivates this distinction. The design says: "When a fix from one perspective breaks something from another, a persistent teammate catches it because they saw the change." Mode 2 cannot do this. Falling back from Mode 3 to Mode 2 loses the core capability that motivated choosing Mode 3 in the first place.

The fallback is "if you can't do the thing you need, do a different thing that doesn't meet your need." This is acknowledged implicitly but never confronted directly.

**Impact:** If the experimental feature is unavailable (common -- experimental flags get removed, renamed, or changed), the system loses its most distinctive capability with no graceful degradation. The spec and design treat this as a minor risk, but it could make the entire Mode 3 concept undeliverable.

**Suggested fix:** Acknowledge this explicitly: the fallback to Mode 2 is a capability loss, not a graceful degradation. If Mode 3 matters (and the design argues convincingly that it does), document what specific delta-aware behaviors are lost when falling back, and whether any can be approximated in Mode 2 (e.g., sequential dispatch with context carry-forward, or a single persistent subagent that runs multiple review passes). Don't oversell Mode 2 as a substitute.

---

### [Severity: Minor] -- Agent tool restrictions don't actually prevent file modification

**Location:** DESIGN-004 COMP-1, all 8 agent files (`tools: Read, Grep, Glob, Write`)

**Problem:** The design states: "All agents use restricted tool access: `tools: Read, Grep, Glob, Write` -- read-only for project files, Write for `.plans/reviews/` reports only." The out-of-scope section says agents do "not modify project files (beyond their own reports in `.plans/reviews/`)."

But `Write` does not have a path restriction. An agent with `Write` access can write anywhere, not just `.plans/reviews/`. The constraint "Write for reports only" is a prompt instruction, not a platform enforcement. If an agent's reasoning leads it to decide that modifying a project file would be helpful (possible under adversarial or confused prompting), the tool restriction does not prevent it.

**Impact:** Low in practice -- the agents are well-prompted to stay in their lane. But the design implies this is an enforced constraint ("restricted tool access") when it's actually a convention. A future developer reading the design might trust this as a security boundary.

**Suggested fix:** Clarify in the design that `Write` is unrestricted and the `.plans/reviews/` limitation is enforced by prompt instruction, not platform capability. If Claude Code supports path-restricted write access in the future, update to use it. Alternatively, consider using `Bash` with a specific write command restricted to the reviews directory, if the platform supports more granular tool configuration.

---

### [Severity: Minor] -- Session report template conflates two different document types

**Location:** `.claude/skills/consult-team/templates/session-report.md`

**Problem:** The template says "This template covers both agent-authored reports and main agent lead reviews. One flexible format -- leave sections empty when not applicable." But agent reports and lead reviews have different authors, different purposes, and different audiences. Agent reports are authored by subagents about their own findings. Lead reviews are authored by the main agent about the agents' work.

In practice, the "one flexible format" means: agents use the first half and ignore the second half; the main agent uses the second half and ignores the first half. They never overlap. This isn't "flexible" -- it's two templates in one file.

**Impact:** Minor -- the template works. But it's slightly misleading. A human reading the template expects a single coherent document; what they get is two non-overlapping sections.

**Suggested fix:** Either split into `agent-report.md` and `lead-review.md`, or at minimum add a sentence in the template explaining that each consumer uses their relevant section and ignores the other. The current framing of "one flexible format" oversells the unity.

---

## Strengths

**The three-tier progressive loading architecture is genuinely well-designed.** The separation of concerns -- command pointers that remind without bloating, a skill that provides coordination knowledge on demand, and agent files that load only per-dispatch -- is elegant and addresses a real problem (context pollution). The decision gate between snapshot and delta dispatch is a genuinely useful forcing function.

**The "every agent writes its own report" decision (DEC-3) is the right call.** Even though the "verification" claim is overstated, the underlying principle -- source-of-truth reports written by the entity that did the analysis, not summarized through a telephone game -- is sound and will pay off as the system scales.

**The agent personas are well-differentiated.** Each agent has a clear, non-overlapping core question. The separation between Critic ("what's wrong?") and Skeptic ("do we need this?") is particularly good -- these are commonly conflated but serve genuinely different functions.

**The design's honesty about the experimental Mode 3 dependency is refreshing.** DQ-3 documents a real failure (native dispatch didn't work on first try) and the resolution. The risk table acknowledges the experimental flag dependency. This is better than most designs at surfacing what might go wrong.

**Document-based persistence is the right architectural bet.** Terminal sessions are ephemeral. Putting all continuity in files rather than session state means the system doesn't break when Claude Code updates, sessions timeout, or the experimental APIs change.

---

## Self-Evaluation

- **What worked well:** Having access to the full system -- spec, design, skill, all 8 agents, all templates, all existing reviews, actual file system state -- let me find discrepancies between what the documents say and what actually exists. The orphaned `fresh-eyes-reviewer` memory directory and the naming convention violations are things that only surface by checking the filesystem against the spec.

- **What you struggled with:** Calibrating between "this is a bootstrapping artifact from a first-session build" and "this is a real problem." Many of the issues (naming violations, unresolved prompt engineer feedback, orphaned directories) are natural consequences of building and testing iteratively in a single session. The question is which ones will cause problems going forward vs. which ones are historical noise. I erred toward flagging them and letting the developer decide.

- **Prompt improvement suggestions:** My prompt could benefit from explicit guidance on how to handle bootstrapping-phase artifacts -- should I judge the system as if it's v1.0 release-ready, or as a first-session build where some cleanup is expected? The answer affects severity ratings. Also, my "What you ignore" section has the same elephants problem I flagged in other agents.
