# Session Report Template

This template covers both agent-authored reports and main agent lead reviews. One flexible format — leave sections empty when they don't apply to your mode.

## Naming Convention

- **Agent reports (all modes):** `[ARTIFACT-ID]-[agent-name]-report.md`
- **Lead reviews (Modes 2 & 3):** `[ARTIFACT-ID]-lead-review.md`
- **All reports go to:** `.plans/reviews/`

Examples: `SPEC-005-critic-report.md`, `DESIGN-004-lead-review.md`

## Agent Report

Every dispatched agent writes this — Mode 1, 2, or 3. This is the source of truth for what the agent found. The direct return to the main agent is for quick synthesis; the written report persists.

```markdown
## Agent Report

**Agent:** [agent name]
**Artifact:** [artifact ID being reviewed, e.g., SPEC-005]
**Date:** [YYYY-MM-DD]
**Dispatch Mode:** [Mode 1: single consult | Mode 2: parallel | Mode 3: collaborative team]

## Instructions Received

[Paste or summarize the context block / task prompt you were given. This enables the main agent to verify what was sent vs. what was received.]

## Findings

[Your analysis, structured per your Output Format section. Include specific document paths and section references.]

## Self-Evaluation

- **What worked well:** [what aspects of your approach were effective]
- **What you struggled with:** [where your perspective had limits or blind spots]
- **Prompt improvement suggestions:** [how YOUR OWN agent prompt could be improved — what instructions were unclear, what capabilities were missing, what would help you do this better next time]
```

## Lead Review

The main agent writes this for Modes 2 & 3. Synthesizes across all agent reports.

```markdown
## Lead Review

**Artifact:** [artifact ID]
**Date:** [YYYY-MM-DD]
**Dispatch Mode:** [Mode 2: parallel | Mode 3: collaborative team]
**Team Composition:** [list of agents dispatched]

## Per-Agent Assessment

For each agent:
- **[Agent name]:** [quality of work, whether instructions were followed, context retention (Mode 3)]

## Synthesis

- **Areas of agreement:** [what multiple agents flagged]
- **Areas of disagreement:** [where agents contradicted each other]
- **Unresolved tensions:** [issues needing user decision]

## Reconstitution Notes (Mode 3 only)

[For cross-session continuity. Include:]
- Team composition and roles
- Open concerns not yet resolved
- Context summary for the next session
- What each teammate was working on when the session ended
```