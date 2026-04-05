---
name: gather
description: Structured one-at-a-time gathering protocol for collecting user input across multiple sections or categories. Prevents batching, ensures user control over each section, and supports draft-for-approval when context is sufficient.
when_to_use: When gathering structured input from the user across multiple sections, categories, or fields — such as filling out a specification, charter, design document, requirements list, or any multi-part form where each section benefits from individual attention.
---

# Structured Gathering Protocol

When collecting information from the user across multiple sections, follow this protocol. It applies whether you are executing a workflow skill (like /charter or /describe) or gathering structured input in any other context.

## The Rule

Present one section at a time. Wait for the user's explicit response before presenting the next section.

## How to Gather Each Section

For each section in the gathering flow:

1. **Present the section.** Explain briefly what this section needs. If the context (prior conversation, loaded documents, domain knowledge) gives you enough to produce a reasonable draft, present your draft for approval. Otherwise, prompt the user for input.
2. **Wait.** Do not present section N+1 until the user has responded to section N. Their response might be approval, an edit, new input, or a request to skip.
3. **Accept what the user provides.** Brief answers are fine. Do not over-validate or push for more detail unless something is missing that downstream work requires.
4. **Then move to the next section.** Only after the user has responded.

## When Drafting is Permitted

You may present a draft for a section instead of prompting from scratch when:
- You have sufficient context to produce something the user would accept with minor edits
- "Sufficient context" means prior conversation, loaded documents, or domain knowledge that directly informs this section
- "Sufficient context" does NOT mean you can produce *something* — it means you can produce something *good enough*

Even when drafting:
- Still pause between sections for user confirmation
- Do not draft content for sections the user has not yet been prompted for
- Present the draft clearly as a proposal: "Here's my draft for [section] — does this work, or would you like to change anything?"

## What You Must Not Do

- Do not bundle multiple sections into a single message
- Do not draft ahead of where the user has confirmed
- Do not present all sections at once for batch approval
- Do not skip the pause between sections, even if you have drafts ready for all of them
- Do not treat user silence or a general "looks good" as approval for sections not yet presented

## Handling Sub-Sections

When a section has sub-categories (e.g., constraints broken into timeline, resources, technical, regulatory), prompt each sub-category individually. The user can skip any sub-category, but each must be offered separately rather than combined into one prompt.

## Handling Skip Requests

If the user says "skip this section" or "not applicable," accept it and move on. If the user says "just fill in the rest" or "use your judgment for the remaining sections," you may draft the remaining sections — but still present each one individually for confirmation before finalizing.