# Agent-Authoring SKILL.md — Cold-Read Clarity Report

**Date:** 2026-04-08
**Review Scope:** `.claude/skills/agent-authoring/SKILL.md` + `references/platform-reference.md`
**Reviewer Context:** None — reading as unfamiliar user

---

## Summary

The skill is **mostly clear and well-structured**, but has several assumptions that a cold reader wouldn't have, plus some tension between the SKILL.md and platform-reference.md around tone and audience. The platform reference is valuable but creates some duplication.

---

## What I Can Understand

**1. What an "agent definition file" is:**
- Clear. A markdown file (name.md) that lives in `.claude/agents/` with YAML frontmatter + markdown body.
- Purpose: defines how a subagent behaves and what it can do.
- I get the analogy: it's a system prompt + configuration combined into one file.

**2. Frontmatter fields and what they do:**
- **Required fields** are explicit: `name`, `description`.
- **Common optional fields** are explained with practical defaults: `tools`, `model`, `memory`.
- **Praxisity-specific field** (`category`) is clearly marked as "Claude Code ignores this."
- The platform-reference.md table adds completeness (advanced fields like `maxTurns`, `hooks`, etc.).

**3. Body sections:**
- **Identity**: Who the agent is + core question. Clear anchor.
- **Reasoning Approach**: A numbered checklist + scope boundaries (what to ignore).
- **Output Format**: Metadata + Instructions Received + findings + strengths + self-evaluation.
- **Self-Evaluation**: Three prompts about what worked, what was hard, how the prompt could improve.

Four sections, consistently named. Straightforward.

**4. Prompt engineering principles:**
- **Positive scoping** — use "What you ignore" instead of cross-agent references.
- **No elephants** — don't describe behaviors you want to avoid.
- **Concise** — 50-100 lines is right; 150+ is over-specified.
- **Standalone operation** — the file must work without appended customization.
- **Single-level dispatch** — agents don't spawn agents.
- **Dual consumption** — useful to human AND AI.
- **Calibrated taxonomies** — define severity levels if you use them.

These are actionable and make sense.

**5. What to do after writing:**
- Save to `.claude/agents/[name].md`
- Update `.claude/agents/README.md`
- Run `/agents` or use team dispatch
- Test the agent
- Update roster docs if needed

Clear workflow.

---

## Issues & Confusions

### 1. **Undefined term: "Cold reader"**

**Quote:** "In Mode 1 dispatch" (line 37, via reference to Reasoning Approach section, line 37)

**Issue:** The SKILL.md references "Mode 1 dispatch" when explaining why NOT to name other agents in scope boundaries. A cold reader has no idea what "Mode 1" is.

**What I'd need:** A sentence explaining that Mode 1 is single-agent dispatch, vs Mode 3 (team dispatch). Or remove the reference entirely and just say "when this agent works alone, don't prime it with knowledge of teammates."

---

### 2. **Assumed context: `.claude/agents/README.md` exists and has an entry format**

**Quote:** "Update `.claude/agents/README.md` with the new agent's entry, unless the user says otherwise" (line 58)

**Issue:** I don't know:
- Does this file already exist?
- What's the entry format? (Alphabetical? Category? One line or paragraph?)
- What happens if the file doesn't exist?

**What I'd need:** An example entry, or a link to the actual file to see the pattern.

---

### 3. **Tension: Self-evaluation placement**

**Quote from SKILL.md line 41:** "**Self-Evaluation** — Embedded in the Output Format template."

**Issue:** This is confusing. Is self-evaluation:
- A separate section in the body?
- Part of every report the agent writes?
- Part of the agent definition file itself?

The phrasing "embedded in the Output Format template" is unclear. Does it mean "include these three prompts in the Output Format section"? Or "each report the agent writes should have a self-eval"?

**What I'd need:** An example agent file showing the actual structure, so I can see where self-eval goes in the markdown body.

---

### 4. **Missing concrete example**

**Quote:** "Read an existing agent file as a reference — any file in `.claude/agents/` works. Note the structure: YAML frontmatter + markdown body with consistent sections." (line 13)

**Issue:** The instruction tells me to read an existing file, but I can't. A cold reader encountering this skill without an existing agent to reference will be stuck.

**What I'd need:** An inline example agent (even a small one) showing frontmatter + all four body sections, so I can see the actual structure.

---

### 5. **Platform-reference.md vs SKILL.md: Duplication and tone mismatch**

**Observation:**

The SKILL.md lines 19-26 list fields in prose + emphasis. The platform-reference.md lines 9-23 list the same fields in a table. Duplication, but:

- SKILL.md explains rationale ("Default for review agents: `Read, Grep, Glob, Write`")
- Platform-reference.md is comprehensive but doesn't explain when to use what

**Also, tone mismatch:**
- SKILL.md is instructional and warm: "Default to `inherit` unless you have a specific reason, unless the user says otherwise."
- Platform-reference.md is encyclopedic: "| `model` | Model to use. Options: `inherit`, `sonnet`, `opus`, `haiku`, or a full model ID. | `inherit` |"

**What's unclear:** Which one should I read first? Are they redundant? The SKILL.md says "read platform-reference.md for the full list" (line 17), but then SKILL.md itself covers the common fields — so why not just cross-reference once?

---

### 6. **Memory semantics: "project" vs other options unexplained**

**Quote:** "memory — `project` recommended by default. When enabled, the platform automatically injects memory instructions into the agent's system prompt AND enables Read/Write/Edit tools for the memory directory. Memory path: `.claude/agent-memory/<name>/`. Omit for lightweight agents that don't need persistence, unless the user says otherwise." (line 26)

**Issue:**
- Why is `project` recommended? What's the difference between `project`, `user`, and `local`?
- The platform-reference.md lists all three options but doesn't explain the tradeoff.
- "When enabled" — enabled for what? The agent? Every report it writes?

**What I'd need:** A sentence explaining the scope: `project` = shared across agents in this project, `user` = shared across all user's projects, `local` = per-agent only? (Guessing.)

---

### 7. **Output Format template: What does it look like?**

**Quote:** "**Output Format** — Structure for the agent's reports. Include: metadata (artifact, date, dispatch mode), Instructions Received section, findings section (with a domain-specific taxonomy), strengths section, and self-evaluation." (line 39)

**Issue:** This describes what a report should contain, but it's in the "Body Sections" part (which defines the agent's persona). Confusing mapping:
- Is the **Output Format section** (body section 3) instructions TO the agent on how to write reports?
- Or is it describing what reports WILL look like?

**What I'd need:** An example showing what the Output Format section actually reads like in the agent file (e.g., "Your report should have these sections:...").

---

### 8. **Prompt engineering principle: "No elephants" lacks concreteness**

**Quote:** "**No elephants.** Don't describe capabilities or behaviors you want the agent to avoid. Describing them activates them." (line 48)

**Issue:** I understand the general principle, but what does it look like in practice?
- Bad: "Don't write overly verbose summaries"?
- Good: "Write concise summaries"?

**What I'd need:** 2-3 concrete examples of what NOT to do in an agent file.

---

### 9. **Dispatch after creation: `/agents` vs `team dispatch` distinction**

**Quote:** "Run `/agents` to register the agent for standalone dispatch, OR use team dispatch (`team_name` parameter) which loads mid-session agents without registration" (line 59)

**Issue:** A cold reader doesn't know:
- What is `/agents`? Is it a command? A skill?
- What's the difference in practice? When would I pick one over the other?
- What does "mid-session" mean?

**What I'd need:** A brief explanation: "`/agents` is a command that reloads the agent registry; use it if you want the agent available for any future session. Team dispatch lets you use the agent immediately without reloading; use it if you're still developing the agent."

---

### 10. **Platform-reference.md: Link to official docs**

**Observation:** The platform-reference.md provides a link to Claude Code official docs (line 3). Good. But:
- SKILL.md doesn't reference this link.
- The SKILL.md says "read platform-reference.md" (line 17), but doesn't say the platform-reference.md is derived from official docs.

**What I'd need:** A note in SKILL.md saying: "For the full spec, the platform-reference.md mirrors the Claude Code official documentation at [link]."

---

### 11. **Memory injection: "first 200 lines / 25KB"**

**Quote from platform-reference.md line 50:** "Includes the first 200 lines / 25KB of the agent's `MEMORY.md`"

**Issue:** Is this a technical limit or a feature? When would an agent memory file be 25KB+? What happens if it exceeds the limit — does the agent not see it, or is it truncated?

**What I'd need:** Clarification: "The platform includes up to 200 lines (or 25KB, whichever comes first) of the memory file. Larger memory files are truncated."

---

## Complementarity Check: SKILL.md vs platform-reference.md

**Good complementarity:**
- SKILL.md teaches philosophy + workflow. Platform-reference.md provides exhaustive reference.
- Platform-reference.md section "Key Platform Behaviors" (lines 44–80) adds practical info about dispatch, scope priority, and constraints that SKILL.md doesn't cover.

**Poor complementarity:**
- Frontmatter fields are duplicated (SKILL.md prose + platform-reference.md table). The SKILL.md tells me to read platform-reference.md, but SKILL.md already covers the common fields — creates redundancy.
- No cross-reference explaining the relationship. A cold reader might not realize they complement each other.

**Suggestion:** Add a "For full reference, see platform-reference.md" link after the Frontmatter section in SKILL.md. Or restructure: move all field documentation to platform-reference.md, and have SKILL.md say "see the field reference in platform-reference.md."

---

## What's Clear — Strengths

1. **Four consistent body sections** are memorable and easy to follow.
2. **Prompt engineering principles** (no elephants, positive scoping, etc.) are sound.
3. **Workflow is linear:** Before → Frontmatter → Body → Principles → After.
4. **Platform-reference.md is comprehensive** — tables are easy to scan.
5. **Praxisity-specific additions** are clearly marked as such.

---

## Recommendations for a Cold Reader

**Priority 1 — Add missing context:**
- Explain "Mode 1 dispatch" or remove the reference.
- Add 1-2 concrete examples: a minimal agent file + a sample memory.md structure.
- Define when to use `memory: project` vs `user` vs `local`.

**Priority 2 — Clarify structure:**
- Clarify where self-evaluation goes (in the Output Format section of the agent file, right?).
- Explain the Output Format section as "instructions TO the agent" not "what reports look like."
- Clarify what `/agents` command does and when to use it vs team dispatch.

**Priority 3 — Reduce duplication:**
- Streamline field documentation (SKILL.md or platform-reference.md, not both).
- Add a bridge sentence linking SKILL.md to platform-reference.md.

---

## Verdict

**Clarity for cold reader:** 6/10

The skill teaches a valid process and the platform-reference is solid. But missing examples, assumed context around dispatch modes, and some confusing terminology (self-evaluation placement, "Mode 1") would trip up someone new to the project. With 20 minutes of example cleanup and context filling, this becomes 9/10.