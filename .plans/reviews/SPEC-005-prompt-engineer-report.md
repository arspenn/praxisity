## Prompt Engineer Review

**Artifact:** All 8 agent definition files in `.claude/agents/`
**Date:** 2026-03-29
**Dispatch Mode:** Mode 2 (parallel team member)

---

## Dual-Consumption Assessment

### [Type: Noise] — Project Context sections are near-identical boilerplate across 7 of 8 agents

**Location:** Every agent file except consistency-reviewer, Section "Project Context"

Six agents share this exact sentence: "You operate within the Praxisity framework, which follows a design-first workflow: Specify -> Design -> Breakdown -> Implement." The rest of each Project Context paragraph varies slightly but conveys similar information. The consistency-reviewer has the fullest version (mentioning ID schemes); the user-advocate has a slightly different framing (productivity multiplier vs. automation).

**Problem for AI:** Each agent loads its own file into context. This repeated paragraph burns ~30-50 tokens per agent for information the AI already has from CLAUDE.md and the skill/command that dispatched it. Across an 8-agent Mode 2 dispatch, that is ~300 tokens of redundant context. More importantly, because the paragraphs are *almost* identical but not quite, a model may attend to the minor differences as if they are meaningful signals, when in most cases they are copy-paste drift.

**Problem for humans:** A human reading multiple agent files will skim-skip these paragraphs after the second one, reducing attention to the sections that actually differ. The near-but-not-exact repetition also creates a maintenance burden — if the workflow stages change, 8 files need updating.

**Suggested fix:** Extract a shared context block (this is what DESIGN-004 COMP-2's "context block template" was designed for). Each agent file should reference the shared context rather than embedding it. If the shared block is not yet built, at minimum deduplicate the text into a single canonical version and keep agent-specific framing to one sentence maximum.

---

### [Type: Elephants] — "What you ignore" sections prime the agent to think about exactly those things

**Location:** All 8 agent files, Section "What you ignore" (or equivalent)

Every agent has a "What you ignore" list naming the other agents' concerns. For example, the skeptic says: "Quality of implementation -- that's the Critic's job." The designer says: "Whether the scope is right -- that's the Skeptic's job."

**Problem for AI:** Telling a model what NOT to do activates those concepts in its processing. "Don't think about code quality" forces the model to represent "code quality" and then suppress it — an unreliable operation. This is the classic "don't think about elephants" problem. Worse, by naming the other agent's role ("that's the Critic's job"), each agent is primed with awareness of the full team roster and their concerns, which can cause drift toward those adjacent concerns.

**Problem for humans:** For human readers these sections are actually useful — they clarify role boundaries. The problem is AI-specific.

**Suggested fix:** Reframe as positive scope boundaries rather than negations. Instead of "What you ignore: Quality of implementation -- that's the Critic's job," use: "Your scope is limited to: necessity, scope justification, and complexity-to-benefit ratio." This defines the same boundary without activating the excluded concepts. If the cross-agent references are valuable for human readers, move them to a comment or to the README roster rather than embedding them in the agent prompt itself.

---

### [Type: Ambiguity] — "Dispatch Mode" field in output templates has no definition within agent files

**Location:** All 8 agent files, Output Format section — `**Dispatch Mode:** [Mode 1/2/3]`

Every output template includes a "Dispatch Mode" metadata field. No agent file defines what Mode 1, 2, or 3 means. The definitions live in SPEC-005 and the consult-team skill.

**Problem for AI:** An agent dispatched in Mode 1 (single consult via Agent tool) receives only its own agent file as system instructions. It has no loaded definition of "Mode 1/2/3." The agent must either guess the dispatch mode from context clues, hallucinate a definition, or leave the field blank. In Modes 2 and 3, the consult-team skill may provide this context — but Mode 1 agents are on their own.

**Problem for humans:** A human reading the output template without the skill documentation would not know what "Mode 1/2/3" means either.

**Suggested fix:** Either (a) add a one-line definition of the three modes to each agent file (costs ~20 tokens, eliminates ambiguity), or (b) remove the Dispatch Mode field from the output template since it is metadata the dispatching system can add to the filename or header rather than requiring the agent to self-report it.

---

### [Type: Drift] — Self-Evaluation section invites open-ended introspection that will vary wildly across sessions

**Location:** All 8 agent files, Output Format section — "Self-Evaluation"

Every agent template ends with a Self-Evaluation section containing prompts like "What worked well," "What you struggled with," and "Prompt improvement suggestions."

**Problem for AI:** These are maximally open-ended prompts. Different sessions will produce entirely different self-evaluations for the same input, because there are no criteria for what counts as a good self-evaluation. The "prompt improvement suggestions" sub-prompt is particularly problematic: it asks the agent to critique its own instructions while still operating under them, creating a meta-cognitive loop that models handle inconsistently. Some sessions will produce genuine insight; others will produce platitudes like "could benefit from more specific examples."

**Problem for humans:** The inconsistency makes self-evaluations hard to compare across sessions or aggregate into actionable prompt improvements.

**Suggested fix:** Add structure to the self-evaluation. Replace open-ended prompts with specific questions:
- "Did you flag any issues you later retracted? Why?" (calibration check)
- "Which sections of the artifact did you spend the most reasoning on?" (attention audit)
- "Rate your confidence in each finding: High/Medium/Low" (calibration signal)

For "prompt improvement suggestions," consider moving this to a separate post-review step rather than asking the agent to self-critique mid-task.

---

### [Type: Ambiguity] — "Update your agent memory" instruction at the end of each file is underspecified

**Location:** All 8 agent files, final line

Each file ends with a directive like: "Update your agent memory with [domain-specific patterns]." For example, the critic's says: "Update your agent memory with recurring weakness patterns, domain-specific failure modes, and calibration notes from your reviews."

**Problem for AI:** The instruction does not specify *where* or *how* to update memory. Claude Code agents have a `memory: project` frontmatter field, which enables writing to `.claude/agent-memory/<name>/`. But the agent prompt never mentions this path, never describes the format, and never explains when memory writing should happen (end of task? after each finding? only for novel patterns?). An agent following this instruction literally would need to infer the memory mechanism from the frontmatter field — a fragile chain of inference.

**Problem for humans:** A human reading this instruction would understand the intent but not the mechanism.

**Suggested fix:** Either (a) specify the memory path and format explicitly: "After completing your review, write notable patterns to `.claude/agent-memory/<your-name>/patterns.md` in append format," or (b) remove the instruction entirely if memory writing is handled by the dispatching system rather than by the agent itself. Vague instructions that the agent cannot reliably execute are worse than no instructions.

---

### [Type: Clarity] — Critic's "Be calibrated" rule overlaps with severity levels but does not define them

**Location:** `critic.md`, Critical Rules section and Output Format section

The Critical Rules say: "Be calibrated: distinguish between 'this will cause a real failure' and 'this could be slightly better.'" The Output Format then provides three severity levels: Critical, Important, Minor. The mapping between the calibration instruction and the severity taxonomy is implicit.

**Problem for AI:** "Critical" vs. "Important" is ambiguous without definitions. Does "Critical" mean "blocks implementation"? Does "Important" mean "causes degraded output"? The critic is told to calibrate but given no calibration scale. Different sessions will draw the Critical/Important line at different thresholds.

**Problem for humans:** Same issue — the terms feel intuitive but are not defined.

**Suggested fix:** Add one-line definitions to the severity levels in the output template:
- Critical: Would cause implementation failure or incorrect behavior
- Important: Would degrade quality or create confusion but work proceeds
- Minor: Cosmetic or low-impact; fix if convenient

---

### [Type: Clarity] — Stakeholder agent lacks guidance on how to determine the intended audience

**Location:** `stakeholder.md`, Reasoning Approach step 1 and Critical Rules

The stakeholder is told to "Read the material as the intended audience would" and "Always identify the audience before evaluating." But the prompt provides no guidance on *how* to determine who the audience is. For internal planning artifacts (specs, designs), the audience is implicit. For deliverables produced by `/deliver`, the audience may be stated in the document or may not.

**Problem for AI:** If the artifact does not explicitly name its audience, the stakeholder agent must infer it. Different sessions will infer different audiences, leading to inconsistent evaluations. An agent reviewing a spec might evaluate it "as a professor" in one session and "as a collaborator" in another, producing contradictory feedback.

**Problem for humans:** Less of an issue — a human reviewer would ask.

**Suggested fix:** Add a decision procedure: "If the artifact names its audience, use that. If not, check the command or skill that produced it for audience context. If still ambiguous, evaluate for the most likely consumer: specs and designs for implementers, deliverables for external readers, command files for the framework developer."

---

### [Type: Noise] — Consistency-reviewer has a unique output format that breaks the cross-agent template pattern

**Location:** `consistency-reviewer.md`, Output Format section

Seven agents follow the same template structure: a typed findings section, a strengths/positives section, and a self-evaluation section. The consistency-reviewer uses a different structure: Issues list, Recommendations, and a self-evaluation with different sub-prompts ("Most frequent inconsistency types," "Unable to assess," "Document structure quality").

**Problem for AI:** This is not inherently a problem for the consistency-reviewer itself. However, for the lead review synthesis step (DESIGN-004 DATA-4), the main agent must parse and compare outputs from all agents. Having one agent with a structurally different output makes the synthesis step harder and less predictable.

**Problem for humans:** A human reading all 8 reports would notice the format break and need to mentally re-map the structure.

**Suggested fix:** This is a mild concern. The consistency-reviewer's different format is arguably justified by its different function (binary pass/fail on consistency vs. graded findings). If standardization is desired, the self-evaluation section is the easiest place to align — use the same three sub-prompts across all agents. The findings section can remain distinct.

---

### [Type: Elephants] — Project-manager's "solo developer (student)" framing could bias the agent toward patronizing advice

**Location:** `project-manager.md`, Project Context section

The text says: "built and maintained by a solo developer (student). Resources are limited -- there is no team to parallelize work, no sprint planning with multiple engineers."

**Problem for AI:** The "(student)" label primes the model to calibrate its advice for someone with limited experience. This may be appropriate for the framework's end users, but when reviewing Praxisity's own planning artifacts, the developer is the framework author — not a student using the framework. The agent may produce overly cautious feasibility assessments ("this might be too ambitious for a student") when the developer is capable of more.

**Problem for humans:** A human reader would understand the nuance. The label is descriptive, not limiting, to a human.

**Suggested fix:** Remove "(student)" and let "solo developer" stand on its own. The constraint that matters is "one person's time and attention," not the person's experience level. If the framework's end users are students, that context belongs in the user-advocate's file, not the project-manager's.

---

## What's Well-Engineered

**Identity sections are excellent.** Every agent opens with a clear, differentiated identity statement and a core question ("What breaks if this is wrong?" / "Do we even need this?" / etc.). These are high-signal, low-cost, and reliably prime the agent toward its intended role. The one-line core questions are particularly effective — they serve as attention anchors that the model can return to throughout its reasoning.

**Critical Rules sections are well-calibrated.** The rules are specific, actionable, and include the crucial "if the work is solid, say so" guardrail that prevents manufactured criticism. This is a known failure mode of evaluative agents and the explicit instruction to avoid it is good prompt engineering.

**The "What you ignore" concept (not the execution) is sound.** Role boundaries are essential for multi-agent systems. The *intent* of defining what each agent should not do is correct — the execution just needs to shift from negation to positive scoping.

**Output templates provide enough structure without being rigid.** The templates guide the agent toward useful output without dictating exact content. The severity/impact/verdict taxonomies are a good balance — they constrain the space of responses without eliminating the agent's judgment.

**The frontmatter metadata is well-designed.** Using YAML frontmatter for name, description, category, tools, model, and memory is clean, parseable by both humans and machines, and follows Claude Code conventions. The `category` field (evaluative/perspective/structural/meta) is a useful organizational signal.

---

## Self-Evaluation

- **What worked well:** Evaluating each file from both the human-reading and AI-processing perspectives simultaneously. The "elephants" analysis (negative framing priming unwanted behavior) is the highest-value finding — it is a real, well-documented prompt engineering failure mode that is present across all 8 files and has a clear fix.

- **What you struggled with:** Assessing whether the self-evaluation sections actually produce useful data in practice. My concern about session-to-session drift is theoretically grounded but I have no empirical evidence from actual agent runs. The recommendation to add structure could itself be over-engineering if the current open-ended format is producing useful feedback. This would benefit from reviewing actual self-evaluation outputs across multiple sessions before committing to a fix.

- **Prompt improvement suggestions:** My own agent prompt (prompt-engineer.md) would benefit from example pairs — "before/after" rewrites showing what a prompt engineering fix looks like in practice. The current prompt tells me *what* to look for but gives no calibration for *how severe* each issue type is. I found myself inventing severity judgments without a framework. Adding a severity scale (similar to what I recommended for the critic) would improve consistency of my own output across sessions.
