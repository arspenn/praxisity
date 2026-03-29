# Context Block Template

This template provides structure for the per-dispatch customization that accompanies every agent invocation. The main agent fills this out and delivers it as part of the task.

## Delivery Mechanism

How this content reaches the agent depends on the dispatch mode:

- **Modes 1 & 2 (native dispatch):** This becomes the `prompt` parameter in the Agent tool. The platform loads the agent file as the system prompt; this context block is the task.
- **Mode 3 (collaborative team):** This is appended after collab-mode.md content in the `prompt` parameter. The platform still loads the agent file as the system prompt.
- **Fallback:** If native dispatch is unavailable, the main agent includes the agent file content + this context block together in the `prompt` for a general-purpose agent.

## Template

The main agent should write naturally within this structure — it is a guide, not a rigid form. Identify this section with a clear heading so the agent knows where persona instructions end and situational context begins.

```markdown
## Your Task

**Phase:** [specifying | designing | reviewing | implementing | other]

**Topic:** [what is being evaluated or worked on]

**Focus:** [optional — specific aspects to pay attention to, concerns to address, or questions to answer]

**Materials:**
- [file path or inline content to review]
- [additional materials as needed]

[Any additional context the main agent wants to provide — keep it focused and informative, not a full project dump]
```