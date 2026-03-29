## User Advocate Review

**Agent:** user-advocate
**Artifact:** SPEC-005 Agent Consultation System (full implementation: SKILL.md, command pointers, agent files, templates, README)
**Date:** 2026-03-29
**Dispatch Mode:** Mode 3 (collaborative team)

## Instructions Received

Evaluate the agent consultation system from the perspective of a solo practitioner (student, developer, researcher) encountering this framework for the first time. Assess whether they can understand how to invoke agent consultation, whether the consult-team skill is clear, and whether the command pointers help or confuse. Key materials: SKILL.md, command pointers in spec.md/architect.md/charter.md, agents/README.md, and templates.

## User Experience Assessment

### [Impact: Blocking] — The `/agents` command referenced in SKILL.md does not exist

**What a new user encounters:** SKILL.md line 17 says "If agents don't appear in your available types, run `/agents` to register them." A user who hits this situation types `/agents` and gets nothing — there is no such command in `.claude/commands/`. The eight `.claude/commands/` files are: charter, spec, architect, breakdown, define, build, deliver, new-project. None of them is `/agents`.

**Why it's a problem:** This is the first dead end a user hits when something goes wrong with agent discovery. The instruction implies a fix exists; it doesn't. The user has no recovery path except reading the agent files manually or guessing at Claude Code internals. For a solo practitioner without deep Claude Code knowledge, this is a wall.

**Suggested improvement:** Either create a minimal `/agents` command that lists the registered agents, or remove the reference from SKILL.md and replace it with accurate instructions for what to do when agents aren't visible (e.g., "agents are automatically available as subagent types when their files exist in `.claude/agents/`").

---

### [Impact: Friction] — The Tier 1 command pointers assume the user already knows what "consult-team skill" means

**What a new user encounters:** At the bottom of `/spec`, `/architect`, and `/charter`, there is a section titled "Agent Consultation" with three lines:

> For a quick single perspective, dispatch a Praxisity agent from your available agents.
> For multi-agent input (parallel or collaborative), invoke the consult-team skill.
> Agent names and descriptions are visible in the Agent tool's available types when properly registered. See .claude/agents/README.md for the full roster.

A user who has never seen the framework before reads "invoke the consult-team skill" and doesn't know what that means. Is it a slash command? Do they type `/consult-team`? Do they ask the AI to "invoke consult-team"? The word "skill" is framework jargon that hasn't been introduced to the user at this point.

**Why it's a problem:** The pointer is designed to be compact (good for context budget), but it sacrifices actionability. The user knows consultation exists but not how to trigger it. The gap between "I see this is available" and "I can actually use it" is unbridged.

**Suggested improvement:** Add one concrete example of how to invoke it. Even something like: "Tell the agent: 'use the consult-team skill to get multi-perspective feedback on this draft'" would make the pointer actionable. The pointer doesn't need to explain the whole system — just give the user a sentence they can copy.

---

### [Impact: Friction] — Mode 1 has no guidance anywhere the user can find it

**What a new user encounters:** SKILL.md line 10 says "Mode 1 (single expert consult) is not covered here — for a quick single-agent opinion, dispatch directly from the Tier 1 pointer in your command." The Tier 1 pointer says "For a quick single perspective, dispatch a Praxisity agent from your available agents." Neither tells the user HOW to dispatch a single agent. What do they type? What does "dispatch" mean in practice?

**Why it's a problem:** Mode 1 is supposed to be the simplest entry point — the thing a user tries before committing to a full team review. But it's the mode with the least guidance. The user is caught between two documents that each point at the other. SKILL.md says "go to the command pointer." The command pointer says "dispatch from your available agents" without explaining what dispatching looks like. A new user who wants to say "hey, can the critic look at this?" has no model for how to phrase that request.

**Suggested improvement:** Either the Tier 1 pointer or SKILL.md (or both) should include one concrete example: "To get a single agent's perspective, ask: 'Have the critic review this spec draft.'" The AI will figure out the Agent tool mechanics — the user just needs to know they can ask in natural language.

---

### [Impact: Friction] — The decision gate between Mode 2 and Mode 3 is clear in concept but the mechanics diverge sharply

**What a new user encounters:** SKILL.md explains the snapshot vs. delta distinction well — "Will the agents need to see how the work changes during this session?" is a genuinely helpful question. But then Mode 2 says "Dispatch each agent using the Agent tool" (simple), while Mode 3 says "Create a team with TeamCreate" and mentions `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`, `v2.1.32+`, `TeamCreate`, `team_name`, `name` parameters, `Shift+Down`. The complexity cliff between modes is steep.

**Why it's a problem:** A user who decides "yes, I want delta-awareness" is suddenly confronted with experimental feature flags, version requirements, and unfamiliar platform mechanics. The fallback instruction ("If unavailable, fall back to Mode 2") is good, but the user doesn't know how to check whether the experimental feature is available. They'll likely just avoid Mode 3 entirely, which means the most valuable mode for sustained work is effectively inaccessible to new users.

**Suggested improvement:** Add a brief "how to check" note: "If `TeamCreate` doesn't appear in your available tools, Mode 3 is not available in your Claude Code version — use Mode 2." Also consider whether Mode 3 instructions should be in a separate section or document to avoid overwhelming users who just want Mode 2.

---

### [Impact: Minor] — Template files are guidance for the AI, not the user, but this isn't stated

**What a new user encounters:** Three template files exist in `.claude/skills/consult-team/templates/`: context-block.md, collab-mode.md, session-report.md. A curious user opens these and finds instructions like "The main agent should write naturally within this structure" and "You are operating as a persistent teammate, not a one-shot subagent." These are AI-facing instructions that the user doesn't need to read, edit, or understand.

**Why it's a problem:** It's not a big problem — a savvy user will figure this out. But for someone trying to understand the system, opening these files and finding AI-to-AI communication is disorienting. It blurs the line between "things I need to know" and "things the framework handles internally."

**Suggested improvement:** A one-line note at the top of each template: "This template is used by the AI agent during dispatch. You don't need to edit or understand it to use agent consultation." Alternatively, SKILL.md could note this when it references the templates.

---

### [Impact: Minor] — Review report naming convention is inconsistent in practice

**What a new user encounters:** The session-report template defines the convention `[ARTIFACT-ID]-[agent-name]-report.md`. But the existing files in `.plans/reviews/` include names like `review-dip004-implementation-2026-03-29.md`, `review-rename-consistency-2026-03-29.md`, `test-team-dispatch-2026-03-29.md`, and `agent-prompt-comparison-report.md` alongside properly-named ones like `SPEC-005-prompt-engineer-report.md`. A user looking at the reviews directory sees no consistent pattern.

**Why it's a problem:** The inconsistency is minor but erodes trust in the system's structure. If the framework says "reports go here with this naming convention" but the actual files don't follow it, the user wonders which convention to trust. For a framework that values traceability and structure, this is a credibility gap.

**Suggested improvement:** This is a cleanup task, not a design issue. Existing reports from before the convention was formalized don't need to be renamed, but future agent-authored reports should follow the convention strictly. The SKILL.md could note that older reports may predate the convention.

---

### [Impact: Minor] — The README agent roster table is helpful but disconnected from actual invocation

**What a new user encounters:** `.claude/agents/README.md` has a clean table of 8 agents with their categories and core questions. This is the most user-friendly entry point into understanding what agents are available. But it doesn't tell the user how to use any of them. It's a menu without ordering instructions.

**Why it's a problem:** The README is a reference document, not a how-to. That's fine for its purpose. But since SKILL.md and the command pointers both point users here ("See .claude/agents/README.md for the full roster"), it's the first place many users will land. They'll see the agents, think "I want the critic to look at my spec," and then... not know what to do next.

**Suggested improvement:** Add one sentence at the top of the README: "To use an agent, ask the AI to dispatch one during any thinking command (e.g., 'have the critic review this'), or invoke the consult-team skill for multi-agent review." This bridges from "here's what's available" to "here's how to start."

## What Works Well for Users

**The agent roster design is genuinely useful.** Eight agents with distinct, clearly-named roles covering evaluative, perspective, structural, and meta concerns. The "core question" column in the README is particularly good — a user can scan it and immediately understand which agent to pick. "What's wrong with this?" vs. "Do we even need this?" vs. "Would a new user understand?" — these are questions a solo practitioner actually asks themselves.

**The snapshot vs. delta decision gate is well-articulated.** "Will the agents need to see how the work changes during this session, or is a snapshot of the current state sufficient?" is a genuinely helpful framing. It turns a technical choice (subagent vs. team) into a practical question the user can answer from their own context.

**The progressive loading architecture (Tier 1/2/3) is invisible to the user in the right way.** A user running `/spec` sees a small pointer. They don't see the full skill, the templates, or the agent files until they're needed. This is correct — the framework handles its own complexity budget without making the user manage it.

**The "when in doubt, start with Mode 2" guidance is appropriate.** It gives uncertain users a safe default and a clear escalation path. This is much better than presenting all three modes as equal choices.

**Self-evaluation in agent output is a learning opportunity.** When agents include what they struggled with and how their prompts could improve, the user gets insight into the review process itself. For a solo practitioner learning structured workflows, seeing an agent say "I struggled with X" is educational — it models the kind of reflection the framework wants users to develop.

**The command pointer placement (end of thinking commands, absent from doing commands) respects attention.** Users aren't nagged about consultation during builds. They see the option when they're in a thinking phase where it's most valuable.

## Self-Evaluation

- **What worked well:** Reading every file in the chain — from command pointer to SKILL.md to templates to agent files to actual review output — gave me a complete picture of the user journey. The dead `/agents` command reference is the kind of thing you only catch by actually walking the path a user would walk.
- **What you struggled with:** I don't have direct experience with Claude Code's skill invocation mechanics, so I can't verify whether "invoke the consult-team skill" actually works as a natural language instruction to the AI. My concern about it being unclear may be overblown if Claude Code reliably interprets that phrasing. I also can't test whether agents actually appear in "available types" automatically — my assessment of the `/agents` dead reference assumes they might not, which may not match reality.
- **Prompt improvement suggestions:** My agent prompt could benefit from a concrete example of what "onboarding friction" looks like in a Claude Code context specifically — the gap between "framework feature exists" and "user can trigger it" is a recurring pattern here, and having a sharper vocabulary for Claude Code interaction patterns would help me be more specific about fixes.
