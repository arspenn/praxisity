## Cross-Document Consistency Review

**Documents reviewed:**
- `.plans/specs/005-agent-consultation-system.md` (SPEC-005)
- `.plans/designs/004-agent-consultation-system.md` (DESIGN-004)
- `.plans/prompts/004-templates-and-extensions.md` (DIP-004)
- `.plans/prompts/005-agent-definition-files.md` (DIP-005)
- `.plans/prompts/006-consult-team-skill.md` (DIP-006)
- `.plans/prompts/007-tier1-command-pointers.md` (DIP-007)
- `.claude/skills/consult-team/SKILL.md`
- `.claude/skills/consult-team/templates/context-block.md`
- `.claude/skills/consult-team/templates/session-report.md`
- `.claude/skills/consult-team/templates/collab-mode.md`
- `.claude/agents/critic.md`
- `.claude/agents/skeptic.md`
- `.claude/agents/user-advocate.md`
- `.claude/agents/stakeholder.md`
- `.claude/agents/designer.md`
- `.claude/agents/project-manager.md`
- `.claude/agents/prompt-engineer.md`
- `.claude/agents/consistency-reviewer.md`
- `.claude/agents/README.md`
- `.claude/commands/spec.md`
- `.claude/commands/architect.md`
- `.claude/commands/charter.md`

**Status:** Issues Found

---

## Issues

### 1. Consistency Reviewer Output Format Deviates from All Other Agents

**Severity: Important**

**Location:** `.claude/agents/consistency-reviewer.md` Output Format section vs. all other 7 agent files

**Problem:** The consistency-reviewer was written before the others (it was the reference implementation during design) and its Output Format section differs from the pattern established by the other 7 agents:

- Missing **Dispatch Mode** metadata field (all other 7 agents include `**Dispatch Mode:** [Mode 1/2/3]`)
- Missing **Instructions Received** section (REQ-F8 and DATA-4 require every agent report to include "the customized instructions they received"; the session report template includes this section; all 7 newer agents omit it too — see Issue #2 — but the consistency-reviewer's format is structurally different in other ways)
- Uses **Status: Approved | Issues Found** pattern instead of the severity-based findings pattern used by the other 7
- Self-Evaluation uses different sub-headings: "Most frequent inconsistency types", "Unable to assess", "Document structure quality" vs. the standard "What worked well", "What you struggled with", "Prompt improvement suggestions"

**Why it matters:** DIP-005 says "use [consistency-reviewer] as the pattern for structure, tone, and length" — but the other 7 agents actually ended up establishing a different and more consistent pattern among themselves. The consistency-reviewer is now the outlier, not the reference. An implementer following DIP-005 literally would create agents matching the consistency-reviewer's format, which contradicts what was actually built.

**Impact:** Moderate. The consistency-reviewer still functions, but when a lead review compares reports across agents, its format won't align with the session report template or the other agents' output. The Self-Evaluation sub-headings differ, which means synthesis tools or future automation expecting a consistent format will need special-casing.

---

### 2. No Agent Embeds "Instructions Received" in Output Format (Spec Requires It)

**Severity: Important**

**Location:** SPEC-005 REQ-F8, DESIGN-004 INT-3 contract, DATA-4 schema, session report template vs. all 8 agent files

**Problem:** REQ-F8 states: "Every dispatched agent... shall write its own report directly to `.plans/reviews/` including findings, **instructions received**, and self-evaluation." The session report template (`.claude/skills/consult-team/templates/session-report.md`) includes an explicit "## Instructions Received" section in the Agent Report format. DESIGN-004 INT-3 contract lists "The customized instructions they received (appended context block)" as a required report field.

None of the 8 agent files include an "Instructions Received" section in their Output Format. All 7 newer agents have Findings + Self-Evaluation but no instruction echo. The consistency-reviewer similarly omits it.

**Why it matters:** The session report template defines the expected format, but agents write their reports guided by their own Output Format section, not by reading the template at dispatch time. Without the instruction in their own persona file, agents may not include this section. The skill (SKILL.md) mentions the session report template but does not explicitly instruct agents to include their instructions received — it describes this as a feature of the written report system ("you can compare what you sent... against what the agent says it received").

**Impact:** Agents may not include the "Instructions Received" section in practice, undermining the context-passing verification that REQ-F8 and DEC-3 were designed to enable. The gap is between what the spec/design require and what the agent files actually instruct.

---

### 3. Command Pointer Format Differs from DIP-007 Specification

**Severity: Minor**

**Location:** DIP-007 Step 1 (INT-2 contract format) vs. actual command file pointers

**Problem:** DIP-007 specifies the INT-2 pointer format as:
```
## Agent Consultation

For a quick single perspective, dispatch: [agent name], [agent name], or [agent name].
For multi-agent input (parallel or collaborative), invoke the consult-team skill.
```

The actual pointers in all three command files use a different wording:
```
## Agent Consultation

For a quick single perspective, dispatch a Praxisity agent from your available agents.
For multi-agent input (parallel or collaborative), invoke the consult-team skill.
```

Two differences:
1. No specific agent names are listed (DIP-007 specified Critic/User Advocate/Skeptic for spec, Designer/Prompt Engineer/Critic for architect, Stakeholder/Project Manager for charter)
2. The wording "dispatch a Praxisity agent from your available agents" replaces the named-agent format

**Why it matters:** This actually matches DESIGN-004's INT-2 contract (lines 343-350), which uses the generic format. The DIP-007 specified named agents per command as natural-fit suggestions, but the implementation followed the design's INT-2 format instead. The design and implementation agree; the DIP is the outlier.

**Impact:** Low. The implemented format is arguably better — it avoids stale agent names in command files and points to the README for the full roster. However, this means DIP-007's AC-1/AC-2/AC-3 criteria (which specify named agents) are technically not satisfied by the implementation as written. The DESIGN-004 INT-2 contract was updated after DIP-007 was written but DIP-007 was not updated to match.

---

### 4. DIP-006 AC-1 Contradicts Skill Implementation (Agent Index)

**Severity: Minor**

**Location:** DIP-006 AC-1 vs. `.claude/skills/consult-team/SKILL.md` "Available Agents" section

**Problem:** DIP-006 Step 1 says "Read the frontmatter of all 8 agent files... Extract name, description, and category for each. Organize by category" and specifies creating an "Index table for the skill, grouped by category." However, DIP-006 AC-1 was updated to say: "it directs the main agent to the platform's native agent listing and to `.claude/agents/README.md` for the roster, rather than duplicating the index."

The skill as implemented follows AC-1's updated requirement — no embedded index, points to README.md instead. But Step 1 of DIP-006 still describes building an embedded index table. The DIP's implementation steps and its acceptance criteria contradict each other.

**Why it matters:** The resolution is clear (AC-1 wins, and the implementation follows it), but the DIP itself is internally inconsistent. If someone re-implements from DIP-006, Step 1 says build an index; AC-1 says don't.

**Impact:** Low. The implementation is correct. This is a DIP authoring inconsistency that would only matter if re-implementing.

---

### 5. DIP-005 Created Date vs. DIP-004 Created Date

**Severity: Minor**

**Location:** DIP-004 metadata (Created: 2026-03-28) vs. DIP-005 metadata (Created: 2026-03-29)

**Problem:** DIP-004 (templates and directories) was created on 2026-03-28, and DIP-005 (agent files) on 2026-03-29. This is fine on its own, but DIP-005 says consistency-reviewer.md "already exists and serves as the reference implementation." The consistency-reviewer was created during the design session on 2026-03-28 — before DIP-004 created the templates it was supposed to follow. This means the reference implementation predates the session report template and context block template it should be consistent with, which explains Issue #1 above.

**Why it matters:** Explains why the consistency-reviewer diverges from the other agents. Not a bug per se, but documents the causal chain.

**Impact:** Informational.

---

### 6. Collab-mode.md Missing Mention of Session Report Template Path

**Severity: Minor**

**Location:** `.claude/skills/consult-team/templates/collab-mode.md` Reporting Duties section

**Problem:** The collab-mode.md says "write your own report to `.plans/reviews/` using the session report template format" but does not provide the path to the session report template (`.claude/skills/consult-team/templates/session-report.md`). In Mode 3, the collab-mode content is part of the task prompt. If the agent hasn't loaded the consult-team skill, it may not know where the template is.

The SKILL.md provides the full path. But in Mode 3 dispatch, the agent receives: system=[agent.md], task=[collab-mode.md content] + [context block]. The skill content is not guaranteed to be part of the prompt.

**Why it matters:** A Mode 3 teammate that hasn't been separately pointed to the session report template may write their report in their own Output Format rather than the session report template format. The Output Format section in each agent file already covers report writing, so in practice the agent would use that. But the collab-mode's reference to "the session report template format" is an unresolvable reference without the path.

**Impact:** Low. Agents will fall back to their own Output Format section, which is functional. The template path could be added to collab-mode.md for completeness.

---

### 7. README.md Agent Table Order vs. Spec/Design Order

**Severity: Cosmetic**

**Location:** `.claude/agents/README.md` vs. SPEC-005 REQ-F4, DESIGN-004 COMP-1 roster

**Problem:** The README.md lists agents in this order: consistency-reviewer, critic, skeptic, user-advocate, stakeholder, designer, project-manager, prompt-engineer. The spec (REQ-F4) and design (COMP-1) list them as: Critic, Skeptic, User Advocate, Stakeholder, Designer, Project Manager, Prompt Engineer, Consistency Reviewer. The README leads with consistency-reviewer (because it was written first), while the spec/design lead with the evaluative category.

**Why it matters:** Doesn't affect functionality. The grouping by category is consistent — both group evaluative, perspective, structural, meta. The order within the README just differs.

**Impact:** Cosmetic only.

---

## Verified Consistencies (No Issues Found)

These cross-references were checked and found consistent:

1. **Agent count:** 8 agents stated in SPEC-005 REQ-F4, DESIGN-004 COMP-1, DIP-005, README.md. Exactly 8 `.md` files exist in `.claude/agents/` (plus README.md). Confirmed.

2. **Agent names:** All 8 names (critic, skeptic, user-advocate, stakeholder, designer, project-manager, prompt-engineer, consistency-reviewer) match across spec, design, DIPs, skill, README, and file names. Confirmed.

3. **Category assignments:** Evaluative (critic, skeptic), Perspective (user-advocate, stakeholder), Structural (designer, project-manager), Meta (prompt-engineer, consistency-reviewer). Consistent across COMP-1, all 8 agent frontmatter `category` fields, and README.md. Confirmed.

4. **Frontmatter fields:** All 8 agents have: name, description, category, tools (Read, Grep, Glob, Write), model (inherit), memory (project). Matches DATA-1 schema, REQ-F1, DIP-005 technical requirements. Confirmed.

5. **Body sections:** All 8 agents have Identity (or equivalent intro), Project Context, Reasoning Approach, Critical Rules, Output Format, Self-Evaluation. Matches DATA-1 schema. Confirmed. (Note: consistency-reviewer's Self-Evaluation sub-headings differ — see Issue #1.)

6. **Report destination:** All 8 agents instruct writing to `.plans/reviews/`. Matches REQ-F8, INT-3, session report template. Confirmed.

7. **Naming convention:** All 8 agents use `[ARTIFACT-ID]-[agent-name]-report.md` pattern. Matches INT-3 contract and session report template naming convention. Confirmed.

8. **Thinking vs. doing command split:** `/spec`, `/architect`, `/charter` have Agent Consultation pointers. `/build`, `/deliver`, `/breakdown`, `/define` have none. Matches REQ-F5, REQ-F6, COMP-4. Confirmed.

9. **Pointer wording consistency:** All three command files use identical pointer text. Confirmed.

10. **Skill name differentiation:** "consult-team" with description emphasizing "multi-perspective consultation on the same work" vs. Superpowers' "dispatching-parallel-agents". Matches REQ-F10. Confirmed.

11. **Three dispatch modes:** SPEC-005 REQ-F11, DESIGN-004 DEC-1, SKILL.md all describe the same three modes: single expert (Mode 1), parallel perspectives (Mode 2), collaborative team (Mode 3). Mode 1 handled by Tier 1 pointers, Modes 2-3 by skill. Confirmed.

12. **Decision gate:** SKILL.md presents snapshot vs. delta decision gate matching DESIGN-004 DEC-1 and COMP-3. Confirmed.

13. **Prompt assembly by mode:** SKILL.md Mode 2 and Mode 3 dispatch instructions match DESIGN-004 INT-1 contract (system=[agent.md], task=[context block] for Mode 2; system=[agent.md], task=[collab-mode + context block] for Mode 3). Confirmed.

14. **Template file paths:** Context block at `.claude/skills/consult-team/templates/context-block.md`, session report at `.claude/skills/consult-team/templates/session-report.md`, collab-mode at `.claude/skills/consult-team/templates/collab-mode.md`. Referenced consistently in DIP-004, DIP-006, SKILL.md. Files exist at those paths. Confirmed.

15. **Skill file path:** `.claude/skills/consult-team/SKILL.md`. Referenced in DIP-006, DIP-007, and command pointers (indirectly via "invoke the consult-team skill"). Confirmed.

16. **Mode 3 prerequisites:** SKILL.md notes `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` and Claude Code v2.1.32+. Matches DESIGN-004 Section 2.3 note. Confirmed.

17. **Fallback guidance:** SKILL.md includes "If unavailable, fall back to Mode 2." Matches DESIGN-004 risk area and COMP-3 design decision. Confirmed.

18. **Core questions per agent:** README.md core questions match DESIGN-004 COMP-1 roster table. Confirmed.

19. **DIP numbering and sequencing:** DIP-004 (templates) -> DIP-005 (agents) -> DIP-006 (skill) -> DIP-007 (pointers). Each DIP's "Files Out of Scope" correctly excludes the other DIPs' files. Confirmed.

20. **Scope boundaries across DIPs:** No overlap in files-in-scope across the four DIPs. DIP-004 owns templates, DIP-005 owns agents, DIP-006 owns skill, DIP-007 owns command pointers. Confirmed.

---

## Recommendations (advisory, do not block approval)

1. **Update consistency-reviewer Output Format** to include Dispatch Mode metadata and align Self-Evaluation sub-headings with the pattern established by the other 7 agents. This is the highest-value fix — it eliminates the format outlier.

2. **Add "Instructions Received" section** to all 8 agent Output Format templates, or add explicit guidance in the Output Format section to "include the context block / instructions you received" per the session report template. This closes the gap between REQ-F8/DATA-4 and what agents are actually instructed to do.

3. **Add session report template path** to collab-mode.md's Reporting Duties section (`.claude/skills/consult-team/templates/session-report.md`) so Mode 3 teammates can find it without the skill being loaded.

4. **Update DIP-006 Step 1** to match AC-1 (reference README/platform rather than building embedded index), or add a note that Step 1 was superseded by AC-1 during implementation. This resolves the DIP's internal contradiction.

5. **Update DIP-007** to reflect that the INT-2 contract was revised to use generic agent references rather than named per-command agents, or note that this change was made during implementation.

---

## Self-Evaluation

- **Most frequent inconsistency types:** (1) Pre-existing reference implementation diverging from later-established patterns (consistency-reviewer format vs. other 7 agents). (2) DIPs not updated when design decisions evolved during implementation (DIP-006 Step 1, DIP-007 named agents).
- **Unable to assess:** Technical runtime behavior of agent dispatch, actual token costs, whether `memory: project` behaves as expected in practice.
- **Document structure quality:** Cross-referencing was straightforward. The traceability system (REQ-F -> COMP -> INT -> DATA -> DEC -> DIP -> implementation) made it possible to follow any requirement from spec through to file. The main difficulty was that the consistency-reviewer was written before the templates, so comparing it against them required understanding the temporal sequence.
- **Prompt improvement suggestions:** My Output Format section should include Dispatch Mode and Instructions Received fields like the other 7 agents — I am the inconsistency I was hired to find.
