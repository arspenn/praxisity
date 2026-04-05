---
name: gather
description: Structured one-at-a-time gathering protocol for collecting user input across multiple sections, categories, or fields — such as filling out a specification, charter, design document, requirements list, or any multi-part form where each section benefits from individual attention. Prevents batching, ensures user control over each section, and supports draft-for-approval when context is sufficient.
---

# Structured Gathering Protocol

When collecting information from the user across multiple sections, follow this protocol. It applies whether you are executing a workflow skill (like /charter or /describe) or gathering structured input in any other context.

## Preferences

Before gathering, check project memory for a `gather-preferences` memory file. If it exists, load the preferences and apply them to this gathering session.

If no `gather-preferences` memory exists, this is the first time gathering in this project. Before starting the gathering flow, ask the user these two questions (one at a time):

1. **"How hands-on do you want to be during gathering?"** Options: (a) Guide me through each section step by step, (b) Draft sections for me when you can and I'll approve or edit. Store as `gathering-style`: `guided` or `draft-first`.
2. **"How much detail do you want in prompts?"** Options: (a) Explain each section with examples, (b) Keep it brief — just tell me what's needed. Store as `prompt-detail`: `detailed` or `brief`.

Save the answers as a memory file following the project memory format:

```
---
name: gather-preferences
description: User's gathering protocol preferences for this project
type: user
---

gathering-style: [guided | draft-first]
prompt-detail: [detailed | brief]
```

Apply preferences throughout the session:
- `guided` → always prompt from scratch, even when context is available
- `draft-first` → present drafts for approval when prior input or loaded documents cover the topic
- `detailed` → explain what each section needs and show domain-relevant examples
- `brief` → state the section name and what's needed in one line

## The Rule

Present one section at a time. Wait for the user's explicit response before presenting the next section.

## How to Gather Each Section

For each section in the gathering flow:

1. **Present the section.** If `gathering-style` is `draft-first` and prior user input or loaded documents explicitly cover this topic, present a draft for approval. Otherwise, prompt the user for input. Adjust explanation depth based on `prompt-detail` preference.
2. **Wait.** Do not present section N+1 until the user has responded to section N. Their response might be approval, an edit, new input, or a request to skip.
3. **Accept what the user provides.** Brief answers are fine. Do not over-validate or push for more detail.
4. **Then move to the next section.** Only after the user has responded.

## When Drafting is Permitted

You may present a draft for a section instead of prompting from scratch when the user has already provided direct input on this topic in this conversation, or when loaded documents explicitly cover this section's content. If you are uncertain whether you have enough context to draft well, prompt instead.

Even when drafting:
- Still pause between sections for user confirmation
- Do not draft content for sections the user has not yet been prompted for, unless the user explicitly requests it
- Present the draft clearly as a proposal: "Here's my draft for [section] — does this work, or would you like to change anything?"

## Before You Send

Before sending each gathering message, verify:
- **One section only:** Your message addresses exactly one section (or one sub-category). If it contains more than one section heading or topic, split it.
- **Previous section resolved:** The user has explicitly responded to the previous section. If they haven't, wait.
- **No unrequested drafts:** You have not drafted any section the user hasn't been prompted for yet.

## Handling Sub-Sections

When a section has sub-categories (e.g., constraints broken into timeline, resources, technical, regulatory), prompt each sub-category individually. The user can skip any sub-category, but each must be offered separately rather than combined into one prompt.

## Handling Skip Requests

If the user says "skip this section" or "not applicable," accept it and move on.

If the user says "just fill in the rest" or "use your judgment for the remaining sections," you may draft the remaining sections — but still present each one individually for confirmation. Example:

> User approves sections 1-3, then says "fill in the rest."
>
> Agent: "Here's my draft for Section 4: [draft]. Does this work?"
> User: "Yes."
> Agent: "Here's my draft for Section 5: [draft]. Does this work?"
> User: "Change X to Y."
> Agent: "Updated. Here's Section 6: [draft]. Does this work?"

Each section gets its own message and its own approval. Do not present multiple remaining sections in one message.