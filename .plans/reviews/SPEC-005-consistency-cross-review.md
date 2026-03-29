## Cross-Agent Consistency Review

**Reviewer:** Consistency Reviewer
**Date:** 2026-03-29
**Purpose:** Check whether agent reports contradict each other, identify where agents agree across perspectives, and flag where one agent approves something another flagged.

**Reports reviewed:**
- `SPEC-005-critic-report.md`
- `SPEC-005-skeptic-report.md`
- `SPEC-005-designer-report.md`
- `SPEC-005-prompt-engineer-report.md`
- `SPEC-005-user-advocate-report.md`
- `SPEC-005-project-manager-report.md`
- `SPEC-005-fresh-eyes-reviewer-report.md`
- `SPEC-005-consistency-reviewer-report.md`

---

## Contradictions and Tensions

### 1. Designer approves what the Critic flags: "Instructions Received" verification

**Critic (Issue 2, Critical):** The "Instructions Received" verification claim is "performative, not real." The agent summarizes its own input from the same context window -- there is no independent attestation. The documents overstate a capability. Recommends downgrading from "verification" to "transparency."

**Designer (INT-3 assessment):** Calls the Instructions Received section "a clever verification mechanism" and describes it positively: "The main agent can compare what it sent... against what the agent reports receiving. This catches context-passing failures without adding any runtime machinery."

**Verdict:** Direct contradiction. The Critic analyzed the actual data flow and concluded verification is impossible within a single context window. The Designer evaluated the architectural pattern and found it sound. The Critic's analysis is stronger here -- the Designer's assessment assumes the Instructions Received section provides verification, but the Critic correctly identifies that self-reported instruction recording within the same context window cannot verify anything. However, both implicitly agree the section has value (the Critic calls it useful for "transparency" and "audit trail"; the Designer calls it "human-auditable"). The disagreement is about the strength of the claim, not the value of the feature.

**Recommendation:** Follow the Critic's suggestion -- downgrade "verification" language to "transparency" in DEC-3, INT-3, and the skill. The section is worth keeping for the reasons both agents identify; the claim about what it achieves just needs to be accurate.

---

### 2. Skeptic challenges 8 agents; Project Manager and Critic confirm differentiation

**Skeptic (Issue 2, Overcomplicated):** 8 agents is too many. Proposes merging to 5: Evaluator (Critic+Skeptic), User Advocate, Designer (merged with Prompt Engineer), Project Manager, Consistency Reviewer. Argues Critic/Skeptic overlap, User Advocate/Stakeholder overlap, and Designer/Prompt Engineer overlap.

**Project Manager (What's Well-Planned section):** "Agent differentiation is real. The prompt engineer found prompt-quality issues (elephants, boilerplate). The consistency reviewer found cross-reference errors and naming mismatches. The fresh-eyes reviewer found spec-to-design semantic drift. These are genuinely different perspectives producing non-overlapping findings."

**Critic (Strengths section):** "The agent personas are well-differentiated. Each agent has a clear, non-overlapping core question. The separation between Critic ('what's wrong?') and Skeptic ('do we need this?') is particularly good -- these are commonly conflated but serve genuinely different functions."

**Verdict:** Genuine tension, not a contradiction. The Skeptic's challenge is about whether the differentiation is *necessary* for the current use case, not whether it exists. The PM and Critic confirm differentiation exists in practice (agents produced non-overlapping findings). But the Skeptic's point stands: differentiation existing doesn't mean all 8 are needed right now. The PM's evidence is from a meta-review (agents reviewing their own system), which the PM themselves flagged as not the intended use case.

**Recommendation:** This is a scope decision for the developer. The agents exist and work. The Skeptic's proposal to merge to 5 is structurally sound but would discard work already done. The strongest version of the Skeptic's argument is: if starting fresh, build 5, not 8. Since the 8 are already built, the question is whether maintaining them is worth the ongoing cost (prompt refinement, decision complexity). The bootstrapping test on real work will generate the evidence to answer this.

---

### 3. Designer approves what the Prompt Engineer flagged: Project Context boilerplate

**Prompt Engineer (Issue 1, Noise):** Project Context sections are "near-identical boilerplate across 7 of 8 agents," burning ~300 tokens of redundant context in an 8-agent dispatch. Recommends extracting to a shared context block.

**Designer (Minor issue):** Acknowledges the "nearly identical boilerplate" but calls it "a reasonable trade-off: it costs ~2-3 lines per agent but ensures each agent is fully standalone without assuming prior context. The slight per-agent variation... is good -- it tailors the framing to the perspective."

**Verdict:** Mild tension. Both see the same fact (near-identical text across agents). The Prompt Engineer evaluates it as noise costing tokens. The Designer evaluates it as a necessary cost of standalone operation. Both are right within their lens. The question is whether standalone operation (Designer's concern) outweighs token efficiency (Prompt Engineer's concern).

**Recommendation:** The Designer's argument for standalone operation is architecturally sound -- agent files should work without assuming any other content is loaded. But the Prompt Engineer's token cost concern is real for Mode 2 dispatches of 3+ agents. Consider whether the shared context block template (which already exists) could serve the same purpose: if the main agent always includes a brief project context in the context block, the per-agent Project Context sections become redundant. This would satisfy both perspectives -- standalone operation via the dispatch mechanism, not via embedded boilerplate.

---

### 4. Prompt Engineer flags "elephants" problem; no other agent addresses it

**Prompt Engineer (Issue 2, Elephants):** "What you ignore" sections in all 8 agents name the other agents' concerns, priming the model to think about exactly those things. Proposes reframing as positive scope boundaries.

**Critic (Issue 5, Important):** Endorses the Prompt Engineer's finding: "'Don't think about elephants' problem flagged but not resolved... The current agent files still contain the negation framing."

**No other agent contradicts or addresses this.**

**Verdict:** Agreement between the two agents who would be expected to evaluate this issue. The Prompt Engineer identified it; the Critic validated it as unresolved. No agent defended the current approach. This is the closest thing to unanimous signal in the reports.

**Recommendation:** This is the highest-confidence fix across all reports. Two agents independently flag it, no agent defends the status quo, and the fix (positive scoping instead of negation) is well-defined. Prioritize this in the next prompt refinement pass.

---

### 5. Mode 3 fallback: Critic, Designer, Project Manager agree on the gap but frame it differently

**Critic (Issue 6, Important):** "Falling back from Mode 3 to Mode 2 loses the core capability that motivated choosing Mode 3 in the first place." Calls the fallback "a capability loss, not a graceful degradation."

**Designer (Minor issue):** "Mode 2 fallback loses delta-awareness." Recommends a one-line addition about breaking work into smaller review gates to partially compensate.

**Project Manager (Risk):** Mode 3 is "designed-but-unverified." Recommends the bootstrapping test explicitly include a Mode 3 test.

**Skeptic (Justified):** Validated Mode 3's existence: "persistent context across a work session is categorically different from snapshot dispatch."

**Verdict:** All four agents agree Mode 3 is valuable and that the fallback to Mode 2 is lossy. The disagreement is on severity: the Critic treats it as an important design flaw (the fallback is presented as adequate when it isn't), the Designer treats it as a minor UX concern, and the PM treats it as an unverified risk needing testing. No agent suggests Mode 3 should be removed.

**Recommendation:** Follow the Critic's framing -- update the fallback language to acknowledge the capability loss, per the Critic's specific suggestion. Follow the PM's recommendation -- include Mode 3 in the bootstrapping test. The Designer's suggestion (smaller review gates to compensate) is a useful mitigation to add to the fallback guidance.

---

### 6. User Advocate flags dead `/agents` reference; no other agent caught it

**User Advocate (Issue 1, Blocking):** SKILL.md references `/agents` to register agents, but no such command exists in `.claude/commands/`. "This is the first dead end a user hits when something goes wrong with agent discovery."

**No other agent flagged this.**

**Verdict:** Not a contradiction -- a gap in coverage. The User Advocate was the only agent to walk the actual user path and discover that `/agents` is not a Praxisity command. The Critic, Consistency Reviewer, and Fresh-Eyes Reviewer all read the SKILL.md but none checked whether `/agents` existed. This validates the User Advocate's distinct perspective.

**Note:** `/agents` may be a Claude Code built-in rather than a Praxisity command. If so, it exists but is not in `.claude/commands/`. The User Advocate's concern would then be about documentation (the skill should clarify this is a platform command, not a Praxisity command) rather than a dead reference.

---

### 7. Skeptic challenges agent memory; PM implicitly agrees

**Skeptic (Premature):** `memory: project` defaults to accumulating data before there's evidence it helps. References the project's own memory about agent MD files having "marginal/negative impact on performance with 20%+ cost increase." Recommends omitting it until evidence shows it helps.

**Project Manager (no direct mention):** Does not mention memory but lists the Prompt Engineer's finding that "Agent memory update instructions are underspecified" as an open item.

**Prompt Engineer (Issue 5, Ambiguity):** Memory update instructions at the end of each agent file are vague -- no path, format, or timing specified. "Vague instructions that the agent cannot reliably execute are worse than no instructions."

**Verdict:** The Skeptic and Prompt Engineer converge from different angles: the Skeptic says the feature is premature, the Prompt Engineer says the implementation guidance is underspecified. Together they suggest that `memory: project` is included without sufficient thought about how it will actually be used. No agent defends the memory feature.

**Recommendation:** The Skeptic's "remove until evidence shows it helps" and the Prompt Engineer's "specify the mechanism or remove the instruction" are complementary. At minimum, either specify how memory writing works or remove the vague "Update your agent memory" instruction from agent files. Whether to remove `memory: project` from frontmatter is a stronger call the developer should make.

---

### 8. Consistency Reviewer's own format: flagged by both Consistency Reviewer and Prompt Engineer

**Consistency Reviewer (Issue 1, Important):** The consistency-reviewer's Output Format deviates from all other 7 agents -- missing Dispatch Mode field, different Self-Evaluation sub-headings, different structure overall.

**Prompt Engineer (Issue 8, Noise):** Same finding: "Having one agent with a structurally different output makes the synthesis step harder and less predictable."

**Prompt Engineer adds nuance:** "This is a mild concern. The consistency-reviewer's different format is arguably justified by its different function (binary pass/fail on consistency vs. graded findings)."

**Verdict:** Agreement on the fact, mild disagreement on severity. Both agents see the format divergence. The Prompt Engineer partially defends it (different function justifies different format). The Consistency Reviewer flags it without defending it (and self-deprecatingly notes "I am the inconsistency I was hired to find").

**Recommendation:** Align the Self-Evaluation sub-headings across all 8 agents (easy, low-risk). Leave the findings structure distinct for the consistency-reviewer (the Prompt Engineer's defense of functional differentiation is sound).

---

## Areas of Strong Agreement (3+ agents concur)

| Topic | Agents Agreeing | Nature of Agreement |
|-------|-----------------|---------------------|
| Progressive loading architecture is sound | Designer, Skeptic, PM, User Advocate, Critic | All affirm the 3-tier model; none challenge it |
| Decision gate between Mode 2 and Mode 3 is valuable | Designer, Skeptic, PM, User Advocate | All approve the forcing function |
| "Every agent writes own report" is the right call | Critic, Designer, PM | All agree, though Critic downgrades the verification claim |
| Agent differentiation produces non-overlapping output | Critic, PM | Both cite evidence from actual review outputs |
| "What you ignore" elephants problem needs fixing | Prompt Engineer, Critic | Both flag, neither defends status quo |
| Mode 3 fallback to Mode 2 is lossy | Critic, Designer, PM, Skeptic | All agree; differ on severity |
| Document-based persistence is correct | Designer, PM, Critic | All affirm files over session state |
| "If the work is solid, say so" rule is important | PM, Prompt Engineer | Both highlight this guardrail |

## Areas Where Only One Agent Flagged (potential blind spots or unique perspectives)

| Finding | Agent | Why No Others Flagged |
|---------|-------|----------------------|
| Dead `/agents` reference in SKILL.md | User Advocate | Only agent that walked the user path end-to-end |
| Orphaned fresh-eyes-reviewer memory directory | Critic | Only agent that checked the filesystem against the roster |
| Naming convention violations in `.plans/reviews/` | Critic, User Advocate | Both noticed; other agents read reports by path, not by convention |
| "(student)" label may bias PM agent | Prompt Engineer | Domain-specific to AI prompt processing; not visible to other perspectives |
| Stakeholder lacks audience determination guidance | Prompt Engineer | Specific to prompt quality, not visible to other reviews |
| 8 agents should be 5 | Skeptic | The Skeptic's unique mandate; other agents evaluate what exists, not whether it should exist |

---

## Self-Evaluation

- **What worked well:** Reading all 8 reports in sequence revealed patterns that no individual report surfaces. The convergence on the "elephants" problem (Prompt Engineer + Critic), the tension around agent count (Skeptic vs. PM + Critic), and the multi-agent agreement on Mode 3 fallback are all cross-cutting signals that only emerge from comparison.

- **What you struggled with:** Distinguishing between "contradiction" and "different emphasis." The Designer approving Project Context boilerplate while the Prompt Engineer flags it isn't really a contradiction -- they're evaluating against different criteria. I tried to be precise about this, but some classifications are judgment calls.

- **Prompt improvement suggestions:** For this specific task (cross-agent review), I would benefit from a structured framework: for each finding in each report, classify it as (a) also flagged by another agent, (b) contradicted by another agent, (c) implicitly validated by another agent's analysis, or (d) unique to this agent. A mechanical pass through that framework before writing the narrative would ensure completeness.
