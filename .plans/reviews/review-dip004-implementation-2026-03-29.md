## Implementation Review: DIP-004 Templates and Extensions

**Documents reviewed:**
- `/home/arspenn/Dev/praxisity/.claude/skills/consult-team/templates/context-block.md` (implemented)
- `/home/arspenn/Dev/praxisity/.claude/skills/consult-team/templates/session-report.md` (implemented)
- `/home/arspenn/Dev/praxisity/.claude/skills/consult-team/templates/collab-mode.md` (implemented)
- `/home/arspenn/Dev/praxisity/.plans/designs/004-agent-consultation-system.md` — DATA-2, DATA-3, DATA-4, INT-1, INT-3
- `/home/arspenn/Dev/praxisity/.plans/prompts/004-templates-and-extensions.md` — AC-1 through AC-5

**Status:** Issues Found

---

## Acceptance Criteria Verification

### AC-1: Context block provides clear structure for phase, topic, focus, and materials

**Result: PASS**

All four DATA-3 fields are present and understandable:
- `**Phase:**` with enumerated options (specifying, designing, reviewing, implementing, other)
- `**Topic:**` with clear description
- `**Focus:**` marked optional, with guidance text
- `**Materials:**` as a bullet list

The template correctly frames itself as a guide rather than a rigid form.

---

### AC-2: Session report template provides structure for agent report (metadata, instructions received, findings, self-evaluation)

**Result: CONDITIONAL PASS — self-evaluation sub-bullets are fresh-eyes-reviewer-specific (see Issue 1)**

All four top-level sections are present. The metadata fields cover artifact ID, date, agent name, and dispatch mode. Instructions received and findings sections are appropriately generic. The `## Self-Evaluation` section is present but its sub-bullets are lifted from the fresh-eyes-reviewer's own Output Format section:

```
- **Most frequent inconsistency types:** [what patterns you saw]
- **Unable to assess:** [what fell outside your expertise]
- **Document structure quality:** [whether cross-referencing was easy or difficult]
- **Prompt improvement suggestions:** [how YOUR OWN agent prompt could be improved...]
```

The first three bullets are document-review framing specific to a consistency reviewer. They do not apply to a Critic, Project Manager, Stakeholder, or any other agent. DATA-4 specifies generic self-evaluation covering "what worked, what they struggled with, and prompt improvement suggestions" — not document structure or inconsistency types.

---

### AC-3: Session report template provides structure for lead review (metadata, per-agent assessment, synthesis, reconstitution notes)

**Result: PASS**

All four lead review sections are present and match DATA-4:
- Metadata with artifact ID, date, dispatch mode, and team composition
- `## Per-Agent Assessment` with per-agent quality/fidelity/retention sub-structure
- `## Synthesis` with areas of agreement, disagreement, and unresolved tensions
- `## Reconstitution Notes (Mode 3 only)` with team composition, open concerns, context summary, and per-agent status

INT-3 lead review fields all covered, including the "disagreements or tensions observed between agents" item (present as "Unresolved tensions").

---

### AC-4: collab-mode.md adds all four DATA-2 sections without duplicating agent file content

**Result: PASS**

All four required sections are present with appropriate content:

| DATA-2 Field | Present | Content Match |
|---|---|---|
| Session awareness | Yes — `## Session Awareness` | Covers persistence, delta-awareness, contrast with snapshot subagents |
| Direct capabilities | Yes — `## Direct Capabilities` | Covers writing to `.plans/reviews/`, relay to user, Shift+Down, shared task list |
| Reporting duties | Yes — `## Reporting Duties` | Covers writing own report, not waiting for main agent, source-of-truth status |
| Team dynamics | Yes — `## Team Dynamics` | Covers maintaining perspective in disagreement, flagging domain-relevant changes |

No agent persona sections (Identity, Reasoning Approach, Output Format, Self-Evaluation) are present. File is agent-agnostic.

One observation: DATA-2 direct capabilities lists "Can write files to .plans/reviews/, can request relay to user, user may interact directly via Shift+Down." The implementation adds a fourth item — access to the shared task list — which is not in the DATA-2 schema but is accurate Mode 3 behavior (task list is a TeamCreate feature). This is a beneficial addition, not a contradiction.

---

### AC-5: Session report naming convention is documented

**Result: PASS**

The Naming Convention section at the top of the template documents:
- Agent reports: `[ARTIFACT-ID]-[agent-name]-report.md`
- Lead reviews: `[ARTIFACT-ID]-lead-review.md`
- Destination: `.plans/reviews/`
- Examples: `SPEC-005-critic-report.md`, `DESIGN-004-lead-review.md`

Matches INT-3 naming exactly.

---

## Issues

### Issue 1 — session-report.md self-evaluation sub-bullets are fresh-eyes-reviewer-specific, not generic

**Location:** `session-report.md` → Agent Report section → `## Self-Evaluation`

**What is implemented:**
```markdown
- **Most frequent inconsistency types:** [what patterns you saw]
- **Unable to assess:** [what fell outside your expertise]
- **Document structure quality:** [whether cross-referencing was easy or difficult]
- **Prompt improvement suggestions:** [how YOUR OWN agent prompt could be improved...]
```

**What DATA-4 specifies:** "What worked, what they struggled with, prompt improvement suggestions"

**The source of the problem:** These three sub-bullets appear verbatim in `.claude/agents/fresh-eyes-reviewer.md`'s Output Format section. They were copied from there into the shared template. They are appropriate self-evaluation prompts for a consistency reviewer but nonsensical for other agents:
- "Most frequent inconsistency types" — meaningless for a Project Manager reviewing sequencing, or a Stakeholder reviewing audience fit
- "Document structure quality" — only relevant to cross-document review work

**Why it matters for implementation:** This is the template all 8 agents will be told to use for their reports. When the Critic, Skeptic, User Advocate, Stakeholder, Designer, Project Manager, or Prompt Engineer reads this template, they will be prompted to reflect on "inconsistency types" and "document structure quality" — producing misaligned or awkward self-evaluations. The template is supposed to be agent-agnostic; it is currently fresh-eyes-reviewer-specific.

**Suggested correction:** Replace the three reviewer-specific sub-bullets with the generic form from DATA-4:
```markdown
- **What worked well:** [what aspects of your approach were effective]
- **What you struggled with:** [where your perspective had limits or blind spots]
- **Prompt improvement suggestions:** [how YOUR OWN agent prompt could be improved — what instructions were unclear, what would help you do this better next time]
```

---

## INT-1 Dispatch Contract Verification

The context block template's Delivery Mechanism section documents all three modes accurately:

| Mode | INT-1 Contract | Template Documents |
|------|----------------|-------------------|
| Modes 1 & 2 | `Agent(subagent_type: "[name]", prompt: [context block])` | "This becomes the `prompt` parameter in the Agent tool. The platform loads the agent file as the system prompt; this context block is the task." |
| Mode 3 | `prompt: [collab-mode.md content] + [context block]` | "This is appended after collab-mode.md content in the `prompt` parameter." |
| Fallback | `Agent(subagent_type: "general-purpose", prompt: [agent file content] + [context block])` | "the main agent includes the agent file content + this context block together in the `prompt` for a general-purpose agent" |

All three delivery mechanisms match the INT-1 contract. PASS.

---

## Self-Evaluation

**Most frequent inconsistency types:** Content transplant errors — content from a specific agent's instructions was copied into a shared template without being generalized. This is a subtle form of scope leakage.

**Unable to assess:** Whether the self-evaluation sub-bullet framing matters in practice — if agents improvise freely within the template structure, the specific bullets may have little effect on output quality. The gap is real but its practical impact is uncertain.

**Document structure quality:** All three files are well-structured and immediately usable. The context block and collab-mode files are clearly focused. The session report is appropriately flexible.

**Prompt improvement suggestions:** The review would benefit from a "who is the intended reader?" check on any shared template. If a template is shared by N agents with different domains, each field should be tested against the least-obvious agent type, not just the most familiar one.