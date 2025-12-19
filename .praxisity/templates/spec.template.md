# Specification: [SPEC-NNN] [Title]

<!--
ABOUT THIS TEMPLATE

This specification template is designed for dual-use:
- Humans: Clear structure for thinking through what you're building
- AI Agents: Parseable sections with explicit IDs for precise referencing

Specifications define WHAT you're building, not HOW.
The "how" comes later in design documents.

Tips:
- Be specific and measurable where possible
- Reference your CHARTER.md for alignment
- Use section IDs (e.g., REQ-1, UC-1) for traceability
- Remove these comments when complete
-->

## Metadata

| Field | Value |
|-------|-------|
| Spec ID | SPEC-NNN |
| Title | [Descriptive title] |
| Status | Draft \| In Review \| Approved \| Superseded |
| Author | [Name] |
| Created | [YYYY-MM-DD] |
| Last Updated | [YYYY-MM-DD] |
| Charter Reference | [Link to CHARTER.md or specific section] |

### Related Documents

<!-- Link to other specs, designs, or external references this spec relates to -->

| Document | Relationship |
|----------|--------------|
| [Document name/link] | [Depends on \| Extends \| Supersedes \| Related to] |

---

## 1. Problem Statement

<!--
What problem does this solve? Why does it matter?
Write this so someone unfamiliar with the project understands the need.

Good problem statements:
- Describe the current state and its limitations
- Explain who is affected and how
- Quantify the impact if possible
- Connect to charter mission/goals

Example (Software):
"Users currently wait 30+ seconds for search results because the system
performs full-table scans. This causes 40% of users to abandon searches,
directly impacting our conversion goals."

Example (Public Health):
"Heart failure patients discharged from Hospital X have a 25% 30-day
readmission rate, above the national average of 20%. Each readmission
costs approximately $15,000 and indicates gaps in care coordination."

Example (Research):
"Existing literature on social media's impact on adolescent mental health
relies primarily on cross-sectional surveys, limiting causal inference.
Longitudinal studies with objective usage data are needed."
-->

[Describe the problem this specification addresses]

---

## 2. Goals and Objectives

<!--
What does success look like? Be specific and measurable.
Goals are high-level outcomes; objectives are specific, measurable targets.

Format objectives as: "By [when/condition], [who] will be able to [do what],
resulting in [measurable outcome]."
-->

### 2.1 Primary Goal

[One sentence describing the primary outcome this spec achieves]

### 2.2 Objectives

<!-- Use OBJ-N identifiers for traceability -->

| ID | Objective | Success Metric |
|----|-----------|----------------|
| OBJ-1 | [Specific, measurable objective] | [How you'll measure it] |
| OBJ-2 | [Specific, measurable objective] | [How you'll measure it] |
| OBJ-3 | [Specific, measurable objective] | [How you'll measure it] |

---

## 3. Requirements

<!--
Requirements define what the solution MUST do (functional) and
what qualities it MUST have (non-functional).

Use MoSCoW prioritization:
- MUST: Non-negotiable for this spec to be considered complete
- SHOULD: Important but not critical; can be deferred if necessary
- COULD: Desirable if time/resources permit
- WON'T: Explicitly excluded (moved to Out of Scope)

Use REQ-N identifiers for traceability in DIPs and testing.
-->

### 3.1 Functional Requirements

<!-- What the solution must DO -->

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-F1 | [The system shall...] | MUST | [Why this matters] |
| REQ-F2 | [The system shall...] | MUST | [Why this matters] |
| REQ-F3 | [The system shall...] | SHOULD | [Why this matters] |
| REQ-F4 | [The system shall...] | COULD | [Why this matters] |

### 3.2 Non-Functional Requirements

<!-- Qualities the solution must HAVE: performance, security, usability, etc. -->

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| REQ-N1 | [Performance/quality requirement] | MUST | [Why this matters] |
| REQ-N2 | [Security/compliance requirement] | MUST | [Why this matters] |
| REQ-N3 | [Usability/accessibility requirement] | SHOULD | [Why this matters] |

---

## 4. User Stories / Use Cases

<!--
Describe how users/stakeholders will interact with the solution.
These bridge requirements to real-world usage.

For Software: User stories in standard format
For Public Health: Intervention scenarios or patient journeys
For Research: Data collection scenarios or analysis workflows

Use UC-N identifiers for traceability.
-->

### UC-1: [Use Case Title]

<!--
Software format:
"As a [role], I want to [action] so that [benefit]."

Public Health format:
"When [trigger], [actor] will [action], resulting in [outcome]."

Research format:
"To answer [question], researcher will [action] using [method]."
-->

**Actor:** [Who performs this]

**Preconditions:**
- [What must be true before this use case begins]

**Flow:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Postconditions:**
- [What is true after successful completion]

**Alternative Flows:**
- [What happens if step N fails or varies]

---

### UC-2: [Use Case Title]

**Actor:** [Who performs this]

**Preconditions:**
- [What must be true before this use case begins]

**Flow:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Postconditions:**
- [What is true after successful completion]

---

## 5. Acceptance Criteria

<!--
How do we know this spec is successfully implemented?
These are the tests that must pass for the spec to be "done."

Write criteria that are:
- Testable (can definitively say pass/fail)
- Specific (no ambiguity)
- Traced to requirements (reference REQ-N)

Format: "Given [context], when [action], then [expected result]."
-->

| ID | Criterion | Validates |
|----|-----------|-----------|
| AC-1 | Given [context], when [action], then [result] | REQ-F1 |
| AC-2 | Given [context], when [action], then [result] | REQ-F2 |
| AC-3 | Given [context], when [action], then [result] | REQ-N1 |

---

## 6. Constraints

<!--
What limits the solution? Pull relevant constraints from CHARTER.md
and add any spec-specific constraints.

Categories:
- Technical: Platform, integration, performance limits
- Timeline: Deadlines affecting this spec
- Resources: Budget, team, tools available
- Regulatory: Compliance requirements
- Dependencies: External systems, other specs
-->

### 6.1 Inherited from Charter

<!-- Reference specific charter constraints that apply -->

- [Constraint from CHARTER.md]
- [Constraint from CHARTER.md]

### 6.2 Spec-Specific Constraints

- [Constraint specific to this specification]
- [Constraint specific to this specification]

---

## 7. Dependencies

<!--
What must exist or happen for this spec to be implementable?
What does this spec enable?
-->

### 7.1 Depends On

<!-- Things that must exist before this spec can be implemented -->

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| [Spec/system/resource] | [Spec \| External \| Resource] | [Available \| Pending \| Blocked] | [Additional context] |

### 7.2 Enables

<!-- Things that depend on this spec being complete -->

| Dependent | Relationship |
|-----------|--------------|
| [Spec/feature] | [How it depends on this] |

---

## 8. Out of Scope

<!--
CRITICAL SECTION: Explicitly state what this spec does NOT cover.
This prevents scope creep and sets clear boundaries.

Include things that:
- Users might reasonably expect but won't be delivered
- Will be addressed in future specs
- Are explicitly excluded by charter
- Are adjacent features you're intentionally not building
-->

The following are explicitly NOT part of this specification:

- [Feature/capability explicitly excluded]
- [Feature/capability explicitly excluded]
- [Adjacent use case not addressed]
- [Future enhancement not included]

---

## 9. Open Questions

<!--
What needs to be resolved before or during implementation?
Track questions and their resolutions.

Questions should be resolved before moving to design phase,
or explicitly deferred with rationale.
-->

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| Q-1 | [Unresolved question] | Open \| Resolved \| Deferred | [Answer or reason for deferral] |
| Q-2 | [Unresolved question] | Open \| Resolved \| Deferred | [Answer or reason for deferral] |

---

## 10. References

<!--
External documents, research, or resources that inform this spec.
-->

- [Reference 1: Description and link]
- [Reference 2: Description and link]
- [CHARTER.md](../CHARTER.md)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | [YYYY-MM-DD] | [Name] | Initial draft |

---

<!--
NEXT STEPS AFTER SPEC APPROVAL:

1. Create design document: /architect
   - Design document will reference this spec's requirements and use cases

2. Break down into tasks: /breakdown
   - Tasks will be created in Todoist referencing spec sections

3. Generate DIPs: /define
   - Each DIP will link to specific REQ-N, UC-N, and AC-N from this spec

The section IDs (REQ-N, UC-N, AC-N, etc.) enable precise traceability
from spec through design to implementation.
-->
