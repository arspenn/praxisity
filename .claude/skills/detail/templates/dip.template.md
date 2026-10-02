# DIP-NNN: [Task Title]

<!--
A Detailed Implementation Prompt (DIP) is a self-contained instruction set for building one
design element. It is written for two readers: whoever executes it, a person in their tools
or an agent through /do, and the person who reviews it before and after. Everything the
executor needs is either in this file or reached by an exact reference from it, so someone
with no memory of the design conversation can carry it out.

One DIP, one element, one sitting. If the steps run past about ten, or the work touches
more than one component, split it into two DIPs.

Each section's comment says what the section needs. Comments are stripped from the finished
DIP. Placeholder rows and steps are illustrative: a DIP has as many steps as the work needs.

Two markers are allowed in place of content:
- "N/A — [reason]" when a section genuinely does not apply
- "TBD — revisit at [milestone]" when it cannot be known yet

Reference conventions, identical in every Praxisity template:
- An element with an ID from another document: the ID plus a short label in parentheses,
  always in tables and Satisfies lists, and on first mention under each heading in prose:
  REQ-F1 (search latency). The label is two to four words, coined by the first document
  that cites the element and reused verbatim after that. Qualify with the document ID when
  more than one parent is in play: SPEC-003 REQ-F2. IDs from this same document are never
  labeled.
- A section: section sign, then number or name, then title: §7.4 Non-Functional Approach,
  §Scope. When the section is in another document, link the document first:
  [CHARTER.md](../../CHARTER.md) §Scope.
- Another document: a relative markdown link, from this file, whose text is the document
  ID or file name: [SPEC-005](../specs/005-agent-consultation-system.md).
- A removed item: its ID struck through, with the version, wherever it appears:
  ~~REQ-F3~~ (removed v0.2).
-->

> **For the executor, person or agent:** follow these instructions as written. Read every item
> under Required Reading before the first step and tick it. Verify each step before starting
> the next. If a verification fails or an instruction is unclear, stop and ask rather than
> improvise. When every step and criterion has passed, set Status to Done. ID key: REQ
> requirement, UC use case, AC acceptance criterion (from the spec); COMP component, INT
> interface, DATA data entity, DEC decision (from the design).

## Context

| Field | Value |
|-------|-------|
| DIP ID | DIP-NNN |
| Element | [COMP-n (short label), or "custom task"] |
| Design | [DESIGN-DDD](../designs/DDD-slug.md) |
| Specification | [SPEC-MMM](../specs/MMM-slug.md) |
| Status | Ready |
| Follows | [DIP-NNN (short label) when this is a follow-up, or N/A] |
| Author | [Name] |
| Created | [YYYY-MM-DD] |

<!-- Status: /detail sets Ready. The executor sets In Progress, then Done, or
     "Halted — Step N: [reason]" when stopped; the Status row is the durable record of a
     halt. A Ready or Halted DIP may be revised (Halted returns to Ready); an In Progress or
     Done DIP is not, and a follow-up DIP is written instead, naming it under Follows. -->

## Objective

<!-- One sentence: what exists, works, or is true when this DIP is complete. Drawn from the
     element's Purpose in the design. -->

[What must be accomplished when this DIP is complete]

## Required Reading

<!-- The exact sections the executing agent reads before starting, by ID with label, so it
     builds against the source rather than a paraphrase. Include the element, every
     requirement it satisfies, the use cases and acceptance criteria that touch it, the
     design decisions that constrain it, and the charter principles or constraints that
     apply. The DIP cites; it does not restate. -->

### From [DESIGN-DDD](../designs/DDD-slug.md)
- [ ] §3 COMP-n (short label)
- [ ] §4 INT-n (short label), or N/A
- [ ] §5 DATA-n (short label), or N/A
- [ ] §6 DEC-n (short label), or N/A

### From [SPEC-MMM](../specs/MMM-slug.md)
- [ ] §3 REQ-Fn (short label)
- [ ] §4 UC-n (short label)
- [ ] §5 AC-n (short label)

### From [CHARTER.md](../../CHARTER.md)
- [ ] §Principles: [the principle that applies, in a phrase]
- [ ] §Constraints: [the constraint that applies, in a phrase]

<!-- A block with nothing to read is a single line "N/A — [reason]" with no checkbox. -->

## Implementation Steps

<!-- The work, in order, each step small enough to verify on its own, written in full in the
     executor's terms (never "implement COMP-2 per §3"). Every step has an Input (what you
     start from, with locations), an Output (what exists afterward), and a Verify: the
     step's criterion for done, as a command, an observable check, or a named human judgment
     (who looks at what). Input and Output may fold into the step text when they would only
     restate the title. The executor tracks each step as it goes.
     Software: "Create the migration file"; verify: "migration runs clean on an empty DB".
     Instructional design: "Build the practice scenario screen in the authoring tool";
     verify: "scenario launches from the module menu and the three branches resolve".
     Research: "Write the cleaning script"; verify: "row count after cleaning matches the
     expected N and no nulls remain in key fields". -->

### Step 1: [Action]

[What to do]

**Input:** [What you start from]
**Output:** [What exists after this step]
**Verify:** [How to confirm it worked]

### Step 2: [Action]

[What to do]

**Input:** [What you start from]
**Output:** [What exists after this step]
**Verify:** [How to confirm it worked]

## Must Satisfy

<!-- One row per requirement the element satisfies, with its priority from the spec and the
     approach this DIP takes, drawn from the design's coverage matrix and the element's
     Satisfies list. Every MUST row has a tested criterion under Acceptance Criteria. -->

| Requirement | Priority | How This DIP Satisfies It |
|-------------|----------|---------------------------|
| REQ-Fn (short label) | MUST | [Approach] |

## Interfaces and Data Touched

<!-- Interfaces this element implements or consumes and data entities it creates, modifies,
     or reads, each with its contract or structure reference in the design. N/A if none. -->

| Element | Role | Reference |
|---------|------|-----------|
| INT-n (short label) | [Implement / Consume] | [DESIGN-DDD](../designs/DDD-slug.md) §4 |
| DATA-n (short label) | [Create / Modify / Read] | [DESIGN-DDD](../designs/DDD-slug.md) §5 |

## Scope Boundaries

<!-- The executor does exactly what is listed and nothing adjacent. DO comes from the
     element's responsibilities; DO NOT from the design's and spec's Out of Scope plus the
     neighbouring elements this DIP must leave alone. Artifacts are files, documents, media,
     or packages: anything the work creates or changes. When several elements live in one
     file (an authoring-tool project, a slide deck), an artifact is a named location inside
     it: "module.story, Scene 3". -->

### DO
- [Action that is part of this task]

### DO NOT
- [Action that is not part of this task]
- Do not change anything outside Artifacts in Scope; this DIP's Status row and PLANNING.md are bookkeeping, not scope

### Artifacts in Scope
```
[path/to/artifact]
[path/to/directory/]
[file, named location inside it]
```

### Artifacts Out of Scope
```
[path/to/protected/artifact]
```

## Acceptance Criteria

<!-- The spec's acceptance criteria this DIP must make pass, cited by ID; the executor has
     read them under Required Reading. What this DIP adds is the Test: how this piece of work
     demonstrates each criterion here, as a command, an observable check, or a human
     judgment naming who looks at what. Every MUST requirement under Must Satisfy has at
     least one. If the spec's own criterion is TBD, say so with its milestone; if it can only
     be tested once a sibling element exists, write "tested in the DIP for COMP-n" so that
     DIP picks it up when it is detailed. -->

| Criterion | Validates | Test |
|-----------|-----------|------|
| AC-n (short label) | REQ-Fn (short label) | [Command, check, or who judges what] |

### Verification

<!-- Commands or checks that confirm the whole DIP, run after the last step. For work with no
     runnable tests, describe the manual check and who performs it. -->

```
[command or check]
```

## Safety Checklist

<!-- The executor confirms each before finishing. The first three apply to any work; the
     last two only under version control and are removed otherwise. Bookkeeping edits
     (this DIP's Status row, PLANNING.md) are not scope violations. -->

- [ ] No secrets, keys, or credentials in the changes
- [ ] Only artifacts in scope were changed, plus this DIP's Status row and PLANNING.md
- [ ] Verification passed
- [ ] Each artifact staged by name; no `git add .` or `git add -A`
- [ ] No unrelated changes in the commit

## Commit Instructions

<!-- Conventional commit. Type: feat, fix, refactor, docs, content, test. Scope: the element
     or area. N/A if the project is not under version control. -->

```
git add [artifacts in scope, by name]
git commit -m "[type]([scope]): [description]

Implements DIP-NNN: [task title]
Satisfies: REQ-Fn, REQ-Fn"
```

## Notes

<!-- Anything else the executing agent should know: known pitfalls, environment setup, a
     decision deferred to execution time, or N/A. -->

[Additional guidance, or N/A]

---

## Revision History

<!-- One row per saved revision while the DIP is Ready or Halted. -->

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | [YYYY-MM-DD] | [Name] | Initial draft |