## Prompt Engineer Review

**Artifact:** CLAUDE.md — two new sections (Human <-> Machine interface, skill-forge hint)
**Date:** 2026-04-08
**Dispatch Mode:** Mode 1

## Instructions Received

Review changes to CLAUDE.md for prompt engineering quality. Two additions: a new "Human <-> Machine interface" section and a new hint about /skill-forge. Evaluate signal-to-noise, instruction clarity, elephants, dual consumption, and placement. Verdict: clean commit or needs revision.

## Dual-Consumption Assessment

### Ambiguity — "interface between" is a role description, not an instruction

**Location:** "Human <-> Machine interface" section
**Problem for AI:** The section tells the agent what it *is* ("you are this framework's interface"), not what to *do* differently because of that identity. Claude Code will process this as a role framing — which it does well with — but there is no behavioral delta. The agent cannot point to this section and derive a different action than it would have taken without it. Compare to the Bootstrapping Principle above it, which ends with a concrete gate: "ask: 'What did we learn...'" The interface section has no equivalent.
**Problem for humans:** Reads fine. Communicates a mental model. A human gets the philosophy.
**Suggested fix:** Either add a behavioral implication (what should the agent do *because* of this role?) or accept that this section is human-facing philosophy and not prompt infrastructure. If the intent is to remind the agent that it bridges two audiences, the existing Charter Principle 6 ("Dual-use design") already covers this more precisely. If the intent is something else — e.g., "translate between human intent and machine execution, don't just execute" — that behavioral instruction should be stated explicitly.

Candidate rewording if you want it to carry behavioral weight:

```
## Human <-> Machine Interface
You bridge the human side (developer input, review decisions) and the machine side
(sub-agents, tool calls, file operations). When ambiguity exists, surface it to the
human side rather than resolving it silently on the machine side.
```

### Noise — The interface section duplicates existing coverage

**Location:** "Human <-> Machine interface" section vs. Charter Principle 6 and the file header
**Problem for AI:** Line 3 already says "This file provides guidance to Claude Code." Charter Principle 6 says "All templates, skills, and outputs optimized for both human understanding and AI agent consumption." The new section adds the words "sub-agents, SDK, tool calls" and "command line input, user review of outputs, direct user responses" but these are enumerations of things the agent already knows it has access to. Context budget cost for zero behavioral gain.
**Problem for humans:** Minor. It is a short section. But if a human asks "what does this section do that nothing else does?" the answer is not obvious.
**Suggested fix:** If this section stays, it should say something the Charter and header do not. The unique concept seems to be: "you are the mediating layer, not just a tool." If that is the intent, make it explicit and actionable. If it is not carrying unique load, cut it.

### Clarity — The skill-forge hint is well-targeted but has a typo

**Location:** Hints from the developer, second bullet
**Problem for AI:** "durring" will be processed fine — LLMs are robust to typos. No behavioral impact.
**Problem for humans:** Reads as unpolished. Minor, but CLAUDE.md is a high-visibility file.
**Suggested fix:** Fix the typo: "during."

### Clarity — "consider using" is the right verb for a hint

**Location:** Hints from the developer, second bullet
**Problem for AI:** "consider using" is appropriately soft for a hint. It does not create an obligation to invoke skill-forge on every session, which would be disruptive. The agent will treat this as a contextual trigger — when a process-learning threshold is crossed, check whether skill-forge applies. This is well-calibrated.
**Problem for humans:** Clear.
**Assessment:** No fix needed. This is good prompt writing.

### Drift — Placement of "interface" section between Bootstrapping and Hints creates an odd grouping

**Location:** Document structure, lines 40-45
**Problem for AI:** The document flows: Identity -> Context -> Focus -> Workflow -> References -> Bootstrapping -> Interface -> Hints. The Interface section is a philosophical frame. The Hints section is tactical corrections. The Bootstrapping section is a process principle. These three final sections have no structural relationship, but their proximity will cause an LLM to read them as a group. Bootstrapping's "ask at session end" gate will carry more weight if it is not immediately diluted by an identity statement and tactical hints.
**Problem for humans:** The ordering reads slightly fragmented at the end.
**Suggested fix:** If the interface section stays, place it after "Framework Development Context" (line 11-15), where it reinforces the "what is this project / what is your role" framing. That groups identity-related content together. Alternatively, fold it into the file header or the Project Identity section.

## What's Well-Engineered

**The skill-forge hint is a good example of a progressive behavioral nudge.** It does not mandate invocation, does not over-explain what skill-forge does (the skill's own description handles that), and places the trigger condition ("learned a substantial amount about a specific process") appropriately. The agent can evaluate this condition naturally rather than checking a binary rule.

**The existing hint about template item counts is effective.** It solves a real LLM failure mode (pattern-matching on example structure), gives a clear behavioral override ("use the right amount"), and names the anti-pattern explicitly.

**The overall CLAUDE.md is lean.** At 45 lines, it is well within the context budget for a file that loads on every session. The discipline of pointing to PLANNING.md and CHARTER.md instead of duplicating their content is strong prompt architecture.

## Verdict

**The skill-forge hint is clean. Commit it after fixing the typo.**

**The "Human <-> Machine interface" section needs revision or removal.** In its current form, it costs context budget without producing a behavioral change the agent would not already exhibit. It either needs to be made actionable (tell the agent what to do differently because of this framing) or recognized as human-facing philosophy and handled accordingly — perhaps as a comment in the file rather than a section, or folded into Project Identity.

If you want to keep both changes in a single commit, my recommendation: fix the typo, and either reword the interface section to include a behavioral directive or move it into the Project Identity section as a single sentence.

## Self-Evaluation

- **What worked well:** Reading the full document in context rather than evaluating the diff in isolation. The placement issue only becomes visible when you see the document flow. Checking whether the interface section duplicates Charter Principle 6 caught real redundancy.
- **What you struggled with:** Distinguishing between "this is philosophy that a student-developer values having in the file" and "this is not pulling its weight as prompt infrastructure." The user is building a framework that teaches through use — some content may be there for the user's benefit as a reader, not the agent's benefit as an instruction-follower. That is a legitimate design choice I should not override.
- **Prompt improvement suggestions:** My agent prompt could benefit from a heuristic for content that is human-facing-only in an otherwise dual-consumption file. Something like: "Not every line in CLAUDE.md must be an AI instruction. Flag it if it costs context without behavioral impact, but acknowledge if it serves the human audience intentionally."