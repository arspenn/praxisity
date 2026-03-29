## Cross-Document Consistency Review: DIP-005 Agent Files

**Documents reviewed:**
- `/home/arspenn/Dev/praxisity/.claude/agents/consistency-reviewer.md`
- `/home/arspenn/Dev/praxisity/.claude/agents/critic.md`
- `/home/arspenn/Dev/praxisity/.claude/agents/skeptic.md`
- `/home/arspenn/Dev/praxisity/.claude/agents/user-advocate.md`
- `/home/arspenn/Dev/praxisity/.claude/agents/stakeholder.md`
- `/home/arspenn/Dev/praxisity/.claude/agents/designer.md`
- `/home/arspenn/Dev/praxisity/.claude/agents/project-manager.md`
- `/home/arspenn/Dev/praxisity/.claude/agents/prompt-engineer.md`
- `/home/arspenn/Dev/praxisity/.plans/specs/005-agent-consultation-system.md` (REQ-F1, REQ-F4, REQ-F7, AC-1, AC-4)
- `/home/arspenn/Dev/praxisity/.plans/designs/004-agent-consultation-system.md` (COMP-1, DATA-1, INT-3)

**Status:** Issues Found

---

## Issues

### Issue 1 — Naming Convention Mismatch: consistency-reviewer.md Output Format

**Location:** `/home/arspenn/Dev/praxisity/.claude/agents/consistency-reviewer.md` — Output Format section

**What the file says:**
> `review-[subject]-[YYYY-MM-DD].md`

**What all 7 other agent files say:**
> `[ARTIFACT-ID]-[agent-name]-report.md`

**What the design defines as authoritative:**
DESIGN-004 COMP-2 Key Design Decisions: `Report naming: [ARTIFACT-ID]-[agent-name]-report.md` (every dispatched agent, all modes).
DESIGN-004 INT-3 Contract: `.plans/reviews/[ARTIFACT-ID]-[agent-name]-report.md`
The session-report.md template header (INT-3 output) also documents this convention with examples.

**Why it matters:** The consistency-reviewer is inconsistent with the naming convention it is supposed to enforce in others. More concretely: the consult-team skill's output preservation guidance, any lead review synthesis, and any tooling or grepping against `.plans/reviews/` will pattern-match on `[ARTIFACT-ID]-[agent-name]-report.md`. Reports from the consistency-reviewer will not match that pattern. The old convention predates SPEC-005 and should be updated.

**Fix:** Update the consistency-reviewer Output Format section to use `[ARTIFACT-ID]-consistency-reviewer-report.md` as the filename convention, consistent with all 7 other agents and INT-3.

Note: Historical review files written under the old convention (`review-[subject]-[YYYY-MM-DD].md`) are already in `.plans/reviews/` and are correctly left as-is. Only the agent file's Output Format instruction needs updating.

---

### Issue 2 — Roster Count: Two Extra Files in `.claude/agents/`

**Location:** `/home/arspenn/Dev/praxisity/.claude/agents/` directory

**What AC-4 requires:**
> "Given the `.claude/agents/` directory, when listed, then it contains exactly 8 agent files: critic.md, skeptic.md, user-advocate.md, stakeholder.md, designer.md, project-manager.md, prompt-engineer.md, consistency-reviewer.md"

**What actually exists (10 .md files):**
```
consistency-reviewer.md
critic.md
designer.md
fresh-eyes-reviewer-generated.md   ← extra, not in AC-4 list
fresh-eyes-reviewer-old.md         ← extra, not in AC-4 list
project-manager.md
prompt-engineer.md
skeptic.md
stakeholder.md
user-advocate.md
```

**Why it matters:** Two files (`fresh-eyes-reviewer-generated.md` and `fresh-eyes-reviewer-old.md`) are inactive backup/historical artifacts from the rename process. Claude Code loads ALL `.md` files in `.claude/agents/` as registered agents. This means two stale agent definitions are live in the platform — they appear in `/agents` listings, can be @-mentioned, and consume registration overhead. The `fresh-eyes-reviewer-generated.md` file was noted in a prior review as a historical artifact from `/agents` command testing. Neither should be in the active directory.

**Fix:** Remove both files from `.claude/agents/`. If historical record is needed, move them to `.plans/archive/` or delete them. The active agent is `consistency-reviewer.md`.

---

## Checklist: Items That Pass

### 1. Frontmatter fields — all 8 agents are consistent

Every agent file has exactly these frontmatter fields in the same order:
```yaml
name: [agent-name]
description: [single-line description]
category: [evaluative|perspective|structural|meta]
tools: Read, Grep, Glob, Write
model: inherit
memory: project
```

No agent has missing or extra frontmatter fields. All use `model: inherit` and `memory: project` as specified.

### 2. Body sections — consistent across all 8 agents

All 8 files use the same 5 section structure:
- `## Identity`
- `## Project Context`
- `## Reasoning Approach` (contains "What you ignore:" list)
- `## Critical Rules`
- `## Output Format` (contains embedded Self-Evaluation prompts inside the report template)

The Self-Evaluation prompts appear inside the Output Format code block template — not as a standalone `## Self-Evaluation` section. This is consistent across all 8, including consistency-reviewer. DESIGN-004 REQ-F7 describes this as "Self-Evaluation section in every agent file's output instructions" — satisfied by its placement within Output Format instructions.

### 3. Categories match REQ-F4 and DESIGN-004 COMP-1 roster

| Agent | Category in file | Category in DESIGN-004 |
|-------|-----------------|----------------------|
| critic | evaluative | Evaluative |
| skeptic | evaluative | Evaluative |
| user-advocate | perspective | Perspective |
| stakeholder | perspective | Perspective |
| designer | structural | Structural |
| project-manager | structural | Structural |
| prompt-engineer | meta | Meta |
| consistency-reviewer | meta | Meta |

All match. Lowercase in frontmatter is correct for YAML values.

### 4. Core questions match DESIGN-004 COMP-1 Agent Roster table

All 8 agents' Identity sections reflect the core question or concept assigned in the design. The Critic's identity shifts framing slightly ("What breaks if this is wrong?" vs. design's "What's wrong with this?") but covers the same domain and is not an inconsistency that would cause implementation problems.

### 5. "What you ignore" cross-deferral accuracy

All agents that name other agents by name do so correctly — no agent defers to a non-existent agent name. Specific accurate deferrals:
- skeptic → Critic, Consistency Reviewer, Designer ✓
- user-advocate → Critic, Designer, Skeptic ✓
- project-manager → Designer, Critic, User Advocate ✓
- prompt-engineer → Consistency Reviewer, Skeptic ✓
- designer → Skeptic, User Advocate ✓

The consistency-reviewer's "What you ignore" section names no other agents (describes ignored content types instead), which is acceptable.

### 6. All 8 agents write to `.plans/reviews/` — confirmed

Every Output Format section instructs writing to `.plans/reviews/` with a filename using agent name. (The convention itself is the Issue 1 subject for consistency-reviewer specifically.)

### 7. Agent differentiation — no redundant output pairs

All 8 agent perspectives are sufficiently differentiated:
- Critic (logical weaknesses) vs. Skeptic (necessity) vs. Consistency Reviewer (ID/path cross-references): three distinct lenses
- User Advocate (internal framework user) vs. Stakeholder (external output consumer): inside vs. outside perspective
- Designer (architecture/coupling) vs. Project Manager (sequencing/feasibility): structural design vs. execution planning
- Prompt Engineer (AI/human dual consumption) vs. Consistency Reviewer (cross-document agreement): single-file quality vs. multi-file agreement

Scope appears in Critic, Skeptic, and Project Manager but from different angles (scope vs. requirements / scope vs. necessity / scope vs. capacity). Not redundant — complementary views on the same dimension.

### 8. Roster count — 8 correct agent files confirmed

The 8 files named in AC-4 all exist and contain valid agent definitions. The issue (Issue 2) is the 2 extra files beyond those 8, not missing files.

---

## Recommendations (advisory, do not block approval)

- **consistency-reviewer "What you ignore" section** — the other 6 agents that name specific agents by name in their ignore lists provide clearer boundaries. The consistency-reviewer's ignore list ("Writing style differences," "Sections that could be 'more detailed'," "New features or scope expansion," "Stylistic preferences") describes exclusion by content type. This works but is less crisp than "that's the Prompt Engineer's job." If the consistency-reviewer's scope ever needs clarifying in practice, naming the Prompt Engineer for single-file quality and the Critic for logic errors would sharpen the boundary.

- **Critic's ignore list** — the critic defers to "Critic's and Designer's job" in the user-advocate ignore list (that's a different agent's file), but in the critic's own ignore list there is no explicit deferral to the Skeptic for necessity/YAGNI questions. The Skeptic defers to the Critic ("quality of implementation — that's the Critic's job"), but the Critic does not reciprocate. The Critic's Reasoning Approach does say "scope creep — features or complexity beyond what was requested" but this overlaps with the Skeptic's domain without acknowledging it. Advisory only.

---

## Self-Evaluation

- **Most frequent inconsistency types:** Single agent diverging from the convention established by the other 7 (Issue 1); directory state not matching spec AC criteria (Issue 2). Both are leftover artifacts from the pre-DIP-005 state.

- **Unable to assess:** Whether the agent personas will produce genuinely differentiated and useful output in practice — this requires actual dispatch testing (the bootstrapping phase in DESIGN-004 Section 6). Prompt effectiveness can only be judged under use.

- **Document structure quality:** Straightforward. Having all 8 agent files use the same 5-section body structure made cross-comparison rapid. The consistent frontmatter made field-by-field checking mechanical. DESIGN-004's Agent Roster table was the authoritative source for category and core question verification.

- **Prompt improvement suggestions:** The review request asked about "overlapping core questions" and "redundant output" — these required judgment calls about degree of overlap, not just fact-checking. A clearer framing would be: "Flag cases where two agents would produce *substantively identical* output on the same artifact." That test is more concrete than "overlapping questions." My current reasoning approach does not include this specific test — adding it would sharpen future reviews of agent roster consistency.