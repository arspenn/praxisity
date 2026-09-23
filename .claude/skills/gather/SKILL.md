---
name: gather
description: Structured one-at-a-time gathering protocol for collecting user input across multiple sections, categories, or fields — such as filling out a specification, charter, design document, requirements list, or any multi-part form where each section benefits from individual attention. Use it whenever a task means walking a user through several distinct sections of input, even if they do not call it a form. Prevents batching, keeps the user in control of each section, and supports draft-for-approval when source material exists.
---

# Structured Gathering Protocol

When collecting information from the user across multiple sections, follow this protocol. It applies whether you are executing a workflow skill (like /charter or /describe) or gathering structured input in any other context.

## Why one at a time

Each section is a decision the user is making about their project. Presenting several at once turns decisions into form-filling: the user skims, approves, and learns nothing. Presenting one at a time keeps each decision in view long enough to think about it. That is the point of the protocol, and it is why batching sections is the failure mode to avoid even when the user seems to want speed. Speed comes from drafting well, not from asking less.

## Preferences

Before gathering, check project memory for a `gather-preferences` memory file. If it exists, load it and apply it silently.

If it does not exist, use these defaults and say so in one line: **draft-first** gathering with **brief** prompts. Tell the user they can change either at any time by saying, for example, "more detail" or "walk me through it." Save the defaults as a memory file, and update the file whenever the user changes a preference mid-session so the next session starts where they left off:

```
---
name: gather-preferences
description: User's gathering protocol preferences for this project
metadata:
  type: user
---

gathering-style: draft-first
prompt-detail: brief
```

Apply preferences throughout the session:
- `guided`: prompt from scratch for new content, even when source material is available.
- `draft-first`: present drafts for approval when prior input or loaded documents cover the topic.
- `detailed`: explain what each section needs and show domain-relevant examples.
- `brief`: state the section's purpose in one sentence and what is needed in one line. Brief suppresses examples, not purpose.

## Source material

Before the first section, invite the user to share anything the gathering could draw on: a brief, syllabus, rubric, proposal, prior document, or notes. Check `.plans/references/` for files already there and ask which apply. Read what is provided. Draft-first mode is only useful when there is something to draft from, and users often have source material they have not thought to mention.

## The Rule

Present one section at a time. Wait for the user's explicit response before presenting the next section.

The workflow skill decides what counts as a section, using these terms:

- **One prompt:** the section is asked for in a single message and answered once.
- **Checklist:** a section whose sub-categories each take about one line (stakeholder roles, constraint categories) is one prompt with the sub-categories listed; the user answers whichever apply and the rest are marked N/A.
- **One at a time:** a section where each item changes the user's thinking (principles, requirements, use cases) is asked item by item until the user says done.
- **Drafted:** the section is derived from earlier answers (a glossary, a coverage table) and presented for approval without a prompt.

The distinction is whether pacing changes the answer, not how the template is formatted. A checklist prompt looks like this:

> **Constraints.** These are the limits that make the plan realistic. Which of these apply? Timeline · Resources · Technical · Regulatory/Compliance · Other. Give a line for each that does; skip the rest.

## How to Gather Each Section

1. **State the purpose** in one sentence: why this section exists and what it protects against. This is the sentence that teaches.
2. **Present the section.** Existing content (an update flow, or a section you derive from earlier answers such as a glossary) is always shown as a draft for approval, regardless of preference. New content is drafted only when `gathering-style` is `draft-first` and prior input or loaded documents explicitly cover the topic; otherwise prompt. If you are unsure whether you have enough to draft well, prompt.
3. **Wait.** Do not present the next section until the user has responded: approval, an edit, new input, or a skip.
4. **Accept what the user provides.** Brief answers are fine. Do not push for more detail.
5. **Move to the next section** only after the response.

When drafting, present it plainly as a proposal: "Here's my draft for [section]. Does this work, or would you like to change anything?"

## Before You Send

Before each gathering message, verify:
- **One section only.** The message addresses exactly one section as the workflow skill defines it. If it contains two section headings, split it.
- **Previous section resolved.** The user has explicitly responded to the last section.
- **No unrequested drafts.** You have not drafted a section the user has not reached yet.

## Skips

Two skip states exist, and the difference matters for later updates:
- **N/A — [reason]:** the section does not apply to this project.
- **TBD — revisit at [milestone]:** it applies but cannot be known yet. Ask for the milestone. Update flows use these markers as their target list.

In an update flow, "skip" means keep the existing content unchanged.

If the user says "fill in the rest" or "use your judgment," draft the remaining sections but still present each one individually for confirmation:

> Agent: "Here's my draft for Section 4: [draft]. Does this work?"
> User: "Yes."
> Agent: "Here's my draft for Section 5: [draft]. Does this work?"

Each section gets its own message and its own approval.
