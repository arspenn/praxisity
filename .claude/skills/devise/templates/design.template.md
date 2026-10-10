# Design: DESIGN-NNN [Title]

<!--
A design defines HOW the work described in a specification will be built. It translates
the spec's requirements into a structure: the parts, how they connect, what information
they handle, and the decisions that shaped them. It is written for two readers: the people
who will build and review it, and the AI that will generate implementation prompts from
it, so every element carries an ID that cites the requirement it satisfies.

Each section's comment says what the section needs and gives examples from several
fields. Comments are stripped from the finished design. Placeholder rows and blocks are
illustrative: repeat a block once per element, and IDs are assigned as items are approved
and are never renumbered.

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

## Metadata

| Field | Value |
|-------|-------|
| Design ID | DESIGN-NNN |
| Title | [Descriptive title] |
| Status | Draft |
| Author | [Name] |
| Created | [YYYY-MM-DD] |
| Last Updated | [YYYY-MM-DD] |

<!-- Status moves through: Draft → In Review → Approved → Superseded. -->

### Specification References

<!-- The spec this design implements, as a relative link from this folder, and the
     requirement IDs it addresses. -->

| Spec ID | Title | Requirements Addressed |
|---------|-------|------------------------|
| [SPEC-MMM](../specs/MMM-slug.md) | [Spec title] | [REQ-F1, REQ-F2, REQ-N1...] |

### Related Documents

<!-- Other designs, specs, or external documents this one implements, extends, depends on,
     or is an alternative to, as relative links. Mark N/A if none. -->

| Document | Relationship |
|----------|--------------|
| [Document name and link] | [Implements / Extends / Depends on / Alternative to] |

---

## 1. Overview

### 1.1 Design Summary

<!-- A few paragraphs: how does this design solve the problem the spec stated?
     Written so a stakeholder outside the field can follow it. -->

[Overall approach and the key decisions that shape it]

### 1.2 Design Principles

<!-- The rules that guided choices in this design. They apply the charter's principles to
     this piece of work; they are not a restatement of the charter.
     Software: "Favor composition over inheritance." Public health: "Community health
     workers are the primary implementers." Instructional design: "Practice before
     explanation; every concept is met in a scenario first." -->

- [Principle, and what it decided in this design]
- [Principle, and what it decided in this design]

### 1.3 Requirements Coverage

<!-- The traceability matrix: which design elements satisfy which requirements. Requirement
     IDs carry a short label in parentheses so the matrix reads without the spec open.
     Every MUST requirement in the spec appears here with at least one element, or with
     "design-wide, §7.4 Non-Functional Approach" when a non-functional requirement is met by
     the design as a whole, or with "deliberate gap, DQ-n" when the user has recorded the gap
     as an open question with a milestone. A MUST with none of those is an unfinished design. -->

| Requirement | Design Elements | Approach |
|-------------|-----------------|----------|
| REQ-F1 (short label) | COMP-1, INT-1 | [How the elements satisfy it, in a phrase] |
| REQ-N1 (short label) | design-wide, §7.4 Non-Functional Approach | [How the design as a whole meets it] |

---

## 2. Architecture

<!-- The shape of the solution before its parts. Three questions transfer across every
     field; answer them in the vocabulary of this project's field.

     2.1 Context — how does this work fit its environment? What does it connect to, who
         touches it, where are its boundaries? A diagram (ASCII or Mermaid) helps.
         Software: system context diagram. Public health: the setting and the care or
         service pathway the program sits in. Research: the conceptual framework relating
         the variables. Instructional design: the learning ecosystem — where the learner
         meets it, what comes before and after, what platform delivers it.
     2.2 Approach — what overall pattern or model organizes the solution, why it fits the
         requirements, and what trade-offs it accepts.
         Software: architecture pattern (layered, event-driven, monolith). Public health:
         logic model (inputs → activities → outputs → outcomes) and intervention model.
         Research: study design (RCT, cohort, qualitative) and why it answers the questions.
         Instructional design: instructional strategy (scenario-based, mastery, spaced,
         worked-example) and sequence.
     2.3 Key Choices — the concrete selections that realize the approach, each with a
         reason. Software: technology per layer. Public health: delivery model (setting,
         frequency, duration, delivered by whom). Research: sampling, data collection,
         analysis. Instructional design: modality, media, authoring tools, LMS, assessment
         instruments. -->

### 2.1 Context

[How the solution fits its environment and where its boundaries lie; diagram if useful]

### 2.2 Approach

**Pattern or model:** [The organizing approach]

**Rationale:** [Why it fits the requirements]

**Trade-offs:**
- Accepts: [What this approach costs]
- Gains: [What it buys]

### 2.3 Key Choices

| Concern | Choice | Rationale |
|---------|--------|-----------|
| [Layer, activity, method, or medium] | [What was chosen] | [Why] |

---

## 3. Components

<!-- The parts of the solution, one block per component, each with an ID. A component is a
     unit that can be built, reviewed, and cited on its own.
     Software: modules, services, classes. Public health: program components, materials,
     training. Research: instruments, procedures, analysis scripts. Instructional design:
     modules, lessons, activities, assessments, job aids.
     "Satisfies" cites the spec's requirement IDs; this is where the coverage matrix comes
     from. Key Design Decisions here are local to the component; decisions that shape the
     whole design go in section 6. Add one COMP block per component. -->

### COMP-1: [Component Name]

**Purpose:** [What this component does]

**Satisfies:** [REQ-F1 (short label), REQ-N1 (short label)]

**Responsibilities:**
- [Responsibility]
- [Responsibility]

**Dependencies:**
- [What this component needs, or N/A]

**Key Design Decisions:**
- [Local decision and rationale, or N/A]

---

## 4. Interfaces

<!-- How components connect to each other and to the outside, one block per interface, each
     with an ID. Mark the section N/A when the components do not interact.
     Software: APIs, events, data contracts. Public health: handoffs, referrals,
     communication protocols. Research: data transfer procedures, participant-facing
     interfaces. Instructional design: transitions between modules, handoffs to a facilitator
     or LMS, how assessment results flow to the learner and instructor.
     A recognition cue: does a result go anywhere, does one part unlock or trigger another,
     does a person hand something to another person? Each of those is an interface.
     The Contract is the specification of what crosses the interface: for an API, the
     endpoints and formats; for a handoff, the trigger, what is passed, from whom to whom,
     and by when. Add one INT block per interface. -->

### INT-1: [Interface Name]

**Connects:** [COMP-1] ↔ [COMP-2 or external actor]

**Type:** [API / Event / File / Protocol / Handoff / Transition]

**Satisfies:** [Requirement IDs with short labels, or N/A if purely structural]

**Contract:**
```
[What crosses the interface, in whatever form fits its type]
```

---

## 5. Data Model

<!-- The information the solution manages, one block per entity, each with an ID. Mark the
     section N/A when the design manages no persistent information.
     Software: schemas, data structures. Public health: collection forms, registries,
     tracking systems. Research: variables, datasets, codebooks. Instructional design:
     learner records, assessment results, completion tracking, content metadata.
     Distinguish information you design the storage for from information a platform
     (an LMS, an EHR, a survey tool) already stores: for the latter, name what is captured
     and where it lives instead of designing fields. Retention matters whenever the data
     is about people. Add one DATA block per entity. -->

### DATA-1: [Entity Name]

**Purpose:** [What this data represents]

**Satisfies:** [Requirement IDs with short labels, or N/A if purely structural]

**Used by:** [COMP-1, COMP-2]

**Structure:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| [field] | [type] | [Yes/No] | [What it holds] |

**Constraints:** [Rules the data must obey, or N/A]

**Retention:** [How long it is kept and how it is removed, or N/A]

---

## 6. Design Decisions

<!-- Decisions that shaped the whole design, one block per decision, each with an ID. These
     are the choices a future reader will ask "why?" about: an approach chosen over an
     obvious alternative, a constraint accepted on purpose. Add one DEC block per decision. -->

### DEC-1: [Decision Title]

**Context:** [What prompted the decision]

**Decision:** [What was decided]

**Rationale:** [Why]

**Alternatives Considered:**
- [Alternative]: [Why rejected]

**Consequences:**
- [What follows, including trade-offs accepted]

---

## 7. Implementation Considerations

<!-- Guidance for building. This section is what the implementation prompts draw on. -->

### 7.1 Implementation Order

<!-- The sequence for building the elements, driven by their dependencies. -->

| Order | Element | Depends On | Notes |
|-------|---------|------------|-------|
| 1 | [COMP-X] | None | [Start here because...] |
| 2 | [COMP-Y] | COMP-X | [Build after X because...] |

### 7.2 Risk Areas

<!-- The parts most likely to go wrong, what happens if they do, and how to reduce it. -->

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [What could go wrong] | [How to address it] |

### 7.3 Validation Strategy

<!-- How the built result will be shown to work, at each level, and which elements each level
     covers. Software: unit, integration, system tests. Public health: fidelity checks, pilot,
     outcome evaluation. Research: instrument validation, pilot, analysis checks.
     Instructional design: expert review, pilot with learners, assessment validation. -->

| Level | Approach | Covers |
|-------|----------|--------|
| [Level] | [Method] | [COMP-1, INT-1] |

### 7.4 Non-Functional Approach

<!-- How each non-functional requirement from the spec (performance, security, accessibility,
     compliance, maintainability) is met by this design. One row per REQ-N. A row here is
     what covers a non-functional MUST that no single element can satisfy on its own. -->

| Requirement | Approach |
|-------------|----------|
| REQ-N1 (short label) | [How the design meets it] |

---

## 8. Out of Scope

<!-- What this design does not cover: the spec's exclusions, inherited, plus anything the
     design deliberately leaves out. -->

**From Specification (inherited):**
- [Item from the spec's Out of Scope]

**Design-Specific Exclusions:**
- [Decision not to include something, and why]

---

## 9. Open Questions

<!-- Unresolved design questions, each Open, Resolved, or Deferred with a reason. A deliberate
     coverage gap is recorded here too: which MUST requirement, why it is not yet designed
     for, and the milestone at which it will be. Resolve or explicitly defer every question
     before implementation prompts are written. -->

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| DQ-1 | [Design question] | Open | [Answer, or reason for deferral] |

---

## 10. Glossary

<!-- Define every term in this design that a reader without project context would not know.
     Mark N/A if only common terms are used. -->

| Term | Definition |
|------|------------|
| [Term] | [Definition] |

## 11. References

- [SPEC-MMM](../specs/MMM-slug.md) — Specification title
- [Reference: description and link or path]

---

## Revision History

<!-- One row per saved revision, naming the IDs added, changed, or removed and any DIP that
     cites a removed element. IDs are never renumbered between revisions; a removed element
     keeps its block header with the ID struck through, so implementation prompts that cite
     it still resolve. -->

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | [YYYY-MM-DD] | [Name] | Initial draft |
