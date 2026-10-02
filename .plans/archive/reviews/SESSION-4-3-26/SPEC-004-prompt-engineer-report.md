## Agent Report

**Agent:** prompt-engineer
**Artifact:** SPEC-004 — Command Behavioral Fixes and Pattern Standards
**Date:** 2026-04-03
**Dispatch Mode:** Mode 3: collaborative team

## Instructions Received

Assigned as dual-consumption specialist for the SPEC-004 /architect phase. Role: ensure design decisions and written commands actually constrain AI behavior as intended. Three research tasks assigned: Q-3 (command vs skill format), Q-4 (standards delivery mechanism), Q-5 (agent prompt readiness). Also responsible for reviewing command/skill drafts for AI-consumption effectiveness.

## Findings

### Q-3: Command vs Skill Format

**Recommendation: Migrate to skills format.**

Key evidence from Claude Code source (cli.js):
- The platform's own `/init` feature lists 5 extension points. `.claude/commands/` is not among them. Skills (`.claude/skills/<name>/SKILL.md`) are extension point #2.
- `/init` Phase 2 scans for `Existing .claude/skills/ and .claude/rules/ directories` — does not scan for `.claude/commands/`.
- `/init` creates skills at `.claude/skills/<name>/SKILL.md`, never commands.

Skills have capabilities commands lack:
- `allowed-tools`: per-skill tool restrictions
- `when_to_use`: AI auto-invocation triggers
- `context: fork`: subagent execution
- `disable-model-invocation`: prevents AI from auto-triggering destructive skills
- Named `$arg_name` parameters (vs single `$ARGUMENTS` string)
- Per-step annotations: Success criteria (required), Execution mode, Artifacts, Human checkpoint, Rules
- Directory structure enabling supporting files

Commands are legacy — still functional but not the platform's documented or recommended format.

### Q-4: Standards Delivery Mechanism

**Final position (after convergence with designer): Hybrid with mechanical/judgment distinction.**

- F1 (copy-then-edit): inline at Generate phase — mechanical rule
- F2 (sequential pre-flight): inline at Pre-Flight phase — mechanical rule
- F3 (one-at-a-time gathering): shared file with imperative loading — judgment rule needing operational "why"
- F4 (complete success message): per-skill checklists — unique to each skill
- F5 (PLANNING.md gate): inline one-liner at completion phase — mechanical rule

Key insight: The designer proved that F3 cannot compress to inline. The prototype already had "Keep each prompt focused on one section at a time" (spec.md line 14) as an inline constraint — it was defeated in BUG-018. A short inline rule is exactly what already failed. Judgment standards need the "why" context that a shared file provides.

Shared file is read by AI at runtime via imperative instruction at the gather phase boundary. A separate human-only reference document serves skill authors.

### Q-5: Agent Prompt Readiness for Mode 3

4 prompt fixes recommended:
1. critic.md: Add Draft-status calibration (distinguish incomplete from incorrect)
2. designer.md: Make progressive loading check conditional on material type
3. prompt-engineer.md: Add prompt-infrastructure evaluation guidance
4. spot.md: Add "unresolved — may be intentional" labeling

Vocabulary impact from skills migration: minimal (only prompt-engineer.md line 18 needs updating).
Agents are Mode 3 ready via collab-mode.md template.

### 6 Prototype Failure Findings

From analyzing the 6 command files as prompts:
1. Generate sections use "Read then Write" — the word "Write" maps to the Write tool, causing BUG-009
2. Numbered lists don't create sequencing — Claude parallelized them (BUG-016/017)
3. Constraint vs. flow structure mismatch — "one at a time" in Constraints, continuous block in flow
4. Success messages are prose, not checklists — agents abbreviate
5. Behavior Notes sections summarize the body — gives AI a shortcut to skim
6. Cross-references are unreliable for AI — inline duplication beats "see document X"

### Skill Frontmatter Recommendations

Provided to designer for DEC-6:
- `/spec`, `/charter`, `/architect`, `/define`: allowed-tools = Read, Write, Edit, Glob, Grep
- `/build`: add Bash for verification and git
- `/new-project`: disable-model-invocation = true (destructive), add Bash
- `/build`: named argument `$dip_path` replaces `$ARGUMENTS`
- All skills: context = inline (all require user interaction)

## What's Well-Engineered

- The spec's pattern extraction into 5 behavioral standards maps cleanly to the mechanical/judgment distinction
- REQ-F1's `cp` then Edit prescription names exact tools — leaves no room for interpretation
- The bug report as evidence base is invaluable — specific failure modes ground every design decision
- The designer's convergence on inline vs shared file was productive cross-perspective collaboration

## Self-Evaluation

- **What worked well:** Platform source analysis provided definitive evidence for Q-3 that moved the decision from opinion to fact. The mechanical/judgment distinction (from the designer) was the right architectural lens for Q-4 — I should have seen it first.
- **What you struggled with:** I conceded on F3 too quickly when the team lead asked if it could compress. The designer had to correct me with the evidence (existing inline constraint already defeated). I should have checked my own prototype analysis before reversing position.
- **Prompt improvement suggestions:** My agent prompt should include guidance on evaluating whether a proposed instruction is stronger than one that already failed. "Is this the same class of instruction that was already defeated?" is a check I should perform automatically when reviewing compressed alternatives.

## Session State at Pause

- All assigned tasks complete (#1, #2, #5)
- Designer writing design document (Task #7) with my Q-3 frontmatter details and Q-4 hybrid design
- Waiting on designer's `gathering-standards.md` draft for F3 phrasing review
- No uncommitted work — all output delivered via messages and this report