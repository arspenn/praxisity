# README.md Clarity Review

**Date:** 2026-04-17
**Document Reviewed:** `/home/arspenn/Dev/praxisity/README.md`
**Scope:** Evaluation as a public-facing README for open-source project discovery

## Executive Summary

The README successfully communicates what Praxisity is and establishes credibility with its core audience (Claude Code users in structured workflow spaces). However, it contains **4 significant clarity issues** that would confuse newcomers unfamiliar with Claude Code, the skills platform, or the project's intended use cases. These are not minor polish issues — they affect whether a public-facing reader can understand what to do with this framework.

## Document Purpose Assessment

**What appears to be:** A public-facing README for an open-source workflow framework built on Claude Code. It targets developers, researchers, and project managers seeking structured planning tools powered by AI.

**Apparent intended audience:** People who:
1. Already use Claude Code (or know what it is)
2. Understand the concept of "skills" as platform features
3. Are looking for a structured workflow system
4. May not understand what agents do or how dispatch modes work

**Actual accessibility:** The README is **partially accessible**. It works well for experienced Claude Code users but creates friction for discoverers.

---

## Clarity Issues

### Issue 1: "Skills" Are Never Defined Before Use

**Location:** Lines 31-51 (Skills section)

**Confusing text:**
```
Skills are directory-based prompt specifications that Claude Code loads as instructions.
There are two types:

**Workflow skills** are user-invoked and drive a specific phase of work. Each bundles
its own templates.
```

**What's unclear:**
- The phrase "directory-based prompt specifications" is jargon. A newcomer doesn't know if this is:
  - Folders in the filesystem?
  - Files within those folders?
  - Cloud-hosted resources?
  - Some Claude Code-specific construct they should recognize?

- "Claude Code loads as instructions" suggests skills are inputs to Claude Code, but *how*? Do you point Claude Code at a folder? Is it automatic?

- "Bundles its own templates" — what's a template in this context? Is it a document template, a code template, or a prompt template?

**What you'd need to know to understand it:**
- A concrete example: "Skills are directories containing a README (instructions) and template files. When you invoke `/charter`, Claude Code reads the skill's README as instructions and loads templates for you to fill in."
- Or: Show the actual filesystem structure of one skill so readers can see what "directory-based" means

**Suggestion for fix:**
```
Skills are directory-based prompt packages that Claude Code loads as instructions.
Each skill is a folder containing:
- A skill README with detailed instructions
- Template files (markdown) for you to fill out during that phase

When you run `/charter`, Claude Code reads the charter skill's instructions and opens its
template for you to write your project constitution.
```

---

### Issue 2: Agent Dispatch Modes Are Introduced Without Context

**Location:** Lines 52-64 (Agent Consultation section)

**Confusing text:**
```
Praxisity includes a roster of 9 specialist agents that provide multi-perspective
review on work products:

critic · designer · project-manager · prompt-engineer · skeptic · spot ·
stakeholder · user-advocate · consistency-reviewer

Agents are consulted in three dispatch modes:

- **Mode 1** — Single expert opinion from one agent
- **Mode 2** — Parallel independent reviews on a snapshot
- **Mode 3** — Persistent collaborative team that sees changes over time
```

**What's unclear:**
- Why are agents "consulted"? Is this a feature request mechanism? Do you ask an agent for feedback? Do they run automatically? The verb is passive and the mechanism is invisible.

- What does "dispatch mode" mean? This is technical jargon. Is it about how you invoke agents? How Claude Code handles them? How they respond?

- What's a "snapshot" (Mode 2)? What does "sees changes over time" (Mode 3) mean operationally?

- No indication of *when* or *why* you'd use each mode. Is there guidance? Do you choose? Do they run automatically?

- "Persistent collaborative team" — do the agents talk to each other? Do they see each other's reviews? Do they reach consensus?

**What you'd need to know to understand it:**
- A workflow example: "When you finish designing, you run `/consult-team`. This dispatches agents to review your design document. Mode 1 gets one agent's opinion (fast). Mode 2 sends your design to all 9 agents in parallel and collects feedback. Mode 3 starts a persistent team that reviews your design, gives feedback, and continues to see and comment on revisions as you iterate."

**Suggestion for fix:**
```
When you complete a phase (e.g., after designing), you can request agent feedback using
`/consult-team`. Praxisity includes 9 specialist agents that each bring a different review
perspective:

**critic** · **designer** · **project-manager** · **prompt-engineer** · **skeptic** ·
**spot** · **stakeholder** · **user-advocate** · **consistency-reviewer**

You can dispatch them in three modes:

- **Mode 1** — Get a single expert opinion (fastest, for quick feedback)
- **Mode 2** — Get all 9 agents reviewing your work in parallel (comprehensive snapshot review)
- **Mode 3** — Start a persistent team that reviews your work and continues to comment as you iterate

See `/consult-team` skill documentation for when to use each mode.
```

---

### Issue 3: Workflow Diagram Shows 5 Skills but Only 4 Are Described in Getting Started

**Location:** Lines 15-27 (Workflow section) vs. Lines 66-81 (Getting Started section)

**Confusing text:**

In the workflow diagram:
```
/charter        Establish project constitution (scope, principles, constraints)
    ↓
/describe       Specify what to build (requirements, acceptance criteria)
    ↓
/design         Architect how it works (structure, interfaces, trade-offs)
    ↓
/plan           Generate implementation prompts (DIPs — self-contained build instructions)
    ↓
/do             Execute with git safety
```

Then in Getting Started:
```
Start with `/charter` to establish your project's scope and principles, then follow
the workflow phases.
```

**What's unclear:**
- "Follow the workflow phases" is vague. Do you run all 5 in order? Can you skip any? What happens if you go out of order?

- `/do` isn't actually explained in the Overview or Getting Started — it appears only in the diagram. Does it run the DIPs automatically? Does it require manual input?

- Is each skill optional or required?

**What you'd need to know to understand it:**
- Clear instructions: "Run these 5 skills in order. Do not skip or reorder. Each builds on the previous one."
- Or: A clearer Getting Started flow like:
  ```
  1. Run `/charter` first — establish your project's constitution
  2. Run `/describe` — define what you're building
  3. Run `/design` — design how it works
  4. Run `/plan` — generate build instructions
  5. Run `/do` — execute the build with git safety checks
  ```

---

### Issue 4: "Bootstrapping Principle" and "Self-Documenting" Are Vague and Project-Centric

**Location:** Lines 102-112 (Principles section) and line 11 (opening section)

**Confusing text:**
```
The framework builds the user through use, and the user builds the framework through
experience.
```

And:

```
2. **Bootstrapping** — Use the system to build the system, the system to build the user,
   the user to build the system
4. **Self-documenting** — The work IS the documentation; specs, designs, and plans
   are git-versioned artifacts
```

**What's unclear:**
- "Framework builds the user" and "system builds the user" — what does "build the user" mean? Does it mean educate? Train? Improve their skills? This is philosophically interesting but operationally vague.

- "Bootstrapping" as stated (use system to build system, system to build user, user to build system) is circular and doesn't explain what the reader should *do*. It reads like project philosophy, not a user-facing principle.

- "The work IS the documentation" — does this mean you don't need to write separate docs? Does it mean all docs are in the `.plans/` directory? Is this saying your work artifacts double as documentation?

**Why it matters for public discovery:**
A reader asking "should I use this?" needs to understand the *value proposition*, not philosophical principles. These principles confuse rather than clarify the benefit.

**What you'd need to know to understand it:**
- Clearer framing: "Praxisity learns from your projects. Each time you use the framework, you generate experience. If you find yourself repeating a task, you can create a new skill to automate it next time. This is bootstrapping: the framework grows by using it to build itself."

- And for self-documenting: "Your specs, designs, and plans live in the `.plans/` directory alongside your code. They're versioned in git. This means your documentation is always in sync with your work — no separate docs folder to maintain."

**Suggestion for fix:**

Replace these principles for public consumption with:

```
2. **Bootstrapping** — Praxisity learns from your work. When you encounter a repeatable
   task, you can automate it as a new skill. The framework grows by using itself.

4. **Self-documenting** — Your specs, designs, and plans live in `.plans/` alongside
   your code, versioned in git. Documentation stays in sync with work; no separate
   docs to maintain.
```

---

## Smaller Issues

### Terminology: "DIP" Unexplained Until the Charter

**Location:** Line 24 (Workflow diagram)

The diagram references "DIPs — self-contained build instructions" but doesn't link to the Charter glossary. For someone discovering this README first, DIPs are a mystery until they read CHARTER.md.

**Minor fix:** Link to CHARTER.md or expand inline: "DIPs (Detailed Implementation Prompts — self-contained build instructions)"

---

### "Repository URL" Placeholder

**Location:** Line 78

```
git clone <repository-url>
```

This is a placeholder that should be replaced with the actual GitHub URL or a note like "Replace <repository-url> with the Praxisity repository URL from GitHub."

---

### Unclear Support Skills Purpose

**Location:** Lines 43-51

```
**Support skills** are invoked automatically when the context matches, or called
directly when needed.

| Skill | Purpose |
|-------|---------|
| `/gather` | Structured input collection across multi-part forms |
| `/skill-forge` | Create and refine skills |
| `/consult-team` | Multi-perspective agent consultation |
| `/agent-authoring` | Create new agent definitions |
```

**What's unclear:**
- "Invoked automatically when the context matches" — what context? What decides to invoke them?

- Is `/consult-team` a support skill or a workflow skill? The section above (Agent Consultation) talks about it as something you *call*, but here it's listed as support.

- `/agent-authoring` and `/skill-forge` are clearly for framework developers, not users. Should they be highlighted differently?

---

## What's Clear

1. **The tagline is strong:** "Design-first workflow framework for AI-assisted planning and execution" immediately communicates value.

2. **The workflow diagram is visually useful,** even if the supporting text is vague. Readers can see the sequence at a glance.

3. **The directory structure is well-organized** and easy to navigate.

4. **The status section is honest:** Stating pre-alpha status and that the framework is actively under development sets correct expectations.

5. **The license placeholder is appropriate** for pre-alpha.

---

## Recommendations (Priority Order)

**High Priority (affects discoverability):**
1. Define "skills" with a concrete example before using them
2. Explain agent dispatch with a workflow example
3. Make Getting Started flow explicit (5 sequential steps)

**Medium Priority (affects understanding of value):**
4. Rewrite bootstrapping and self-documenting principles for user benefit, not philosophy
5. Clarify when/why to use agents vs. doing solo work

**Low Priority (polish):**
6. Replace `<repository-url>` placeholder
7. Expand DIP acronym inline
8. Clarify which support skills are for framework developers vs. users

---

## Testing Recommendation

Run the README by 2-3 people who:
- Use Claude Code but have never heard of Praxisity
- Are NOT on the project's memory/team

Ask them to:
1. Explain what a skill is after reading this README
2. Describe when they would use `/consult-team`
3. Say what they would do after reading "Getting Started"

Their answers will reveal the actual clarity gaps.

---

*Review completed: 2026-04-17*
