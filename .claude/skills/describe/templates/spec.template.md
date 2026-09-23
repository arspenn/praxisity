# Specification: SPEC-NNN [Title]

<!--
A specification defines WHAT will be built and how you will know it is done. The HOW
comes later in a design document. It is written for two readers: the people who will
review and build from it, and the AI that will design and implement against it, so
every requirement carries an ID that later documents can cite exactly.

Each section's comment says what the section needs and gives examples. Comments are
stripped from the finished spec. Placeholder rows are illustrative: tables take as many
rows as the spec has content for. IDs are assigned as items are approved and are never
renumbered.

Two markers are allowed in place of content:
- "N/A — [reason]" when a section genuinely does not apply
- "TBD — revisit at [milestone]" when it cannot be known yet
-->

## Metadata

| Field | Value |
|-------|-------|
| Spec ID | SPEC-NNN |
| Title | [Descriptive title] |
| Status | Draft |
| Author | [Name] |
| Created | [YYYY-MM-DD] |
| Last Updated | [YYYY-MM-DD] |
| Charter Reference | [CHARTER.md](../../CHARTER.md) — [principles this spec serves] |

<!-- Status moves through: Draft → In Review → Approved → Superseded. -->

### Related Documents

<!-- Other specs, designs, or external documents this one depends on, extends,
     supersedes, or relates to, as relative links from this folder
     (e.g. [SPEC-002](002-intake-module.md), [DESIGN-001](../designs/001-intake-module.md)).
     Mark N/A for a first spec. -->

| Document | Relationship |
|----------|--------------|
| [Document name and link] | [Depends on / Extends / Supersedes / Related to] |

---

## 1. Problem Statement

<!-- What problem does this solve, for whom, and why does it matter? Write it so someone
     unfamiliar with the project understands the need. Describe the current state and its
     limits, who is affected, and the impact, quantified when possible. Connect it to the
     charter mission.

     Software: "Users wait 30+ seconds for search results because the system performs
       full-table scans; 40% abandon the search."
     Public health: "Heart failure patients discharged from Hospital X have a 25% 30-day
       readmission rate, above the 20% national average."
     Research: "Existing literature on social media and adolescent mental health relies on
       cross-sectional surveys, limiting causal inference."
     Instructional design: "New volunteers receive a two-hour lecture on intake procedures
       and 60% make a documentation error in their first week."
-->

[Describe the problem this specification addresses]

---

## 2. Goals and Objectives

<!-- The goal is the one-sentence outcome. Objectives are the specific, measurable targets
     that add up to it: "By [when], [what] will [be true], measured by [how]."

     These are project objectives: what this work achieves. They are not the learning
     objectives of a course or module. If the deliverable teaches something, the learning
     objectives become requirements ("the module shall enable learners to...") and their
     assessment becomes acceptance criteria.

     Example: "By the end of the term, the intake module is piloted with 10 volunteers,
     measured by completion of the pilot and a post-module error rate under 20%."
-->

### 2.1 Primary Goal

[One sentence describing the outcome this spec achieves]

### 2.2 Objectives

| ID | Objective | Success Metric |
|----|-----------|----------------|
| OBJ-1 | [Specific, measurable objective] | [How it will be measured] |
| OBJ-2 | [Specific, measurable objective] | [How it will be measured] |

---

## 3. Requirements

<!-- Functional requirements say what the solution must DO. Non-functional requirements say
     what qualities it must HAVE (performance, security, accessibility, compliance,
     maintainability). Each carries a priority:
       MUST   — the spec is not complete without it
       SHOULD — important; can be deferred with a stated reason
       COULD  — desirable if time allows
     Anything the solution WON'T do goes in Out of Scope, not here.
     The rationale column is what lets a reviewer judge the priority.

     Functional examples:
       Software: "The system shall return search results within 2 seconds."
       Public health: "The program shall contact each discharged patient within 48 hours."
       Instructional design: "The module shall enable learners to complete an intake form
         without reference material."
     Non-functional categories: Performance · Security · Usability/Accessibility ·
       Compliance · Maintainability. Example: "The module shall meet WCAG 2.2 AA." -->

### 3.1 Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-F1 | [The solution shall...] | MUST | [Why this matters] |
| REQ-F2 | [The solution shall...] | SHOULD | [Why this matters] |

### 3.2 Non-Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-N1 | [Quality the solution must have] | MUST | [Why this matters] |

---

## 4. Use Cases

<!-- How people will actually use the result. Each use case is one scenario, from trigger
     to outcome, and bridges the requirements to real-world use. Frame it in the field's
     own vocabulary:
       Software: "As a [role], I want to [action] so that [benefit]."
       Public health: "When [trigger], [actor] will [action], resulting in [outcome]."
       Research: "To answer [question], the researcher will [action] using [method]."
       Instructional design: "A [learner] in [situation] uses [the deliverable] to [do what],
         and [what the facilitator or system observes]." A scenario, not a learning objective.
     For a learning deliverable: Preconditions are what the learner already knows or has;
     Alternative Flows are remediation or edge paths.
     Add one UC block per use case. -->

### UC-1: [Use Case Title]

**Actor:** [Who performs this]

**Preconditions:**
- [What must be true before this begins]

**Flow:**
1. [Step]
2. [Step]

**Postconditions:**
- [What is true after successful completion]

**Alternative Flows:**
- [What happens if a step fails or varies, or N/A]

---

## 5. Acceptance Criteria

<!-- The tests that must pass for the spec to be done. Each is testable (a clear pass or
     fail), specific, and traced to a requirement. Every MUST requirement needs at least one.
     Format: "Given [context], when [action], then [result]."
     When a rubric exists, its rows are acceptance criteria in waiting: cite the row.

     Software: "Given 10,000 records, when a user searches, then results appear within
       2 seconds" → REQ-F1
     Instructional design: "Given a learner who has completed the module, when they are
       handed a blank intake form and a sample case, then they complete it with no more than
       one error (rubric row 3)" → REQ-F1 -->

| ID | Criterion | Validates |
|----|-----------|-----------|
| AC-1 | Given [context], when [action], then [result] | REQ-F1 |
| AC-2 | Given [context], when [action], then [result] | REQ-N1 |

---

## 6. Constraints

<!-- What limits the solution. Inherited constraints come from the charter and are cited,
     not restated at length. Spec-specific constraints are new limits this work introduces
     or discovers: a platform, a deadline, a data source, a regulation. -->

### 6.1 Inherited from Charter

- [Charter constraint that applies here]

### 6.2 Spec-Specific Constraints

- [Constraint specific to this specification]

---

## 7. Dependencies

<!-- What must exist for this spec to be buildable, and what will build on it. -->

### 7.1 Depends On

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| [Spec, system, or resource] | [Spec / External / Resource] | [Available / Pending / Blocked] | [Context] |

### 7.2 Enables

| Dependent | Relationship |
|-----------|--------------|
| [Future spec or feature] | [How it depends on this] |

---

## 8. Out of Scope

<!-- Required. Name what this spec does NOT cover: things people might reasonably expect,
     adjacent features deliberately not built, work deferred to a future spec, and anything
     the charter already excludes. This is the section that prevents scope creep. -->

The following are explicitly NOT part of this specification:

- [Excluded feature or capability]
- [Adjacent use case not addressed]

---

## 9. Open Questions

<!-- Uncertainties to resolve before or during design. Each is Open, Resolved, or Deferred
     with a reason. Resolve or explicitly defer every question before moving to design. -->

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| Q-1 | [Unresolved question] | Open | [Answer, or reason for deferral] |

---

## 10. References

<!-- Source material and external documents that inform this spec, plus the charter. -->

- [CHARTER.md](../../CHARTER.md)
- [Reference: description and link or path]

---

## Revision History

<!-- One row per saved revision. IDs are never renumbered between revisions; a removed
     item keeps its row, struck through, when a design or DIP cites it. -->

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | [YYYY-MM-DD] | [Name] | Initial draft |
