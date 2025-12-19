# Design: [DESIGN-NNN] [Title]

<!--
ABOUT THIS TEMPLATE

This design template is for dual-use:
- Humans: Clear structure for thinking through HOW to build something
- AI Agents: Parseable sections with IDs for precise DIP generation

Designs define HOW you're building what the spec defined.
They translate requirements into architecture and implementation approach.

Key principle: Every design element should trace back to a spec requirement.

Tips:
- Reference spec IDs (REQ-F1, UC-1) to maintain traceability
- Use design IDs (COMP-1, INT-1) for DIP references
- Remove these comments when complete
-->

## Metadata

| Field | Value |
|-------|-------|
| Design ID | DESIGN-NNN |
| Title | [Descriptive title] |
| Status | Draft \| In Review \| Approved \| Superseded |
| Author | [Name] |
| Created | [YYYY-MM-DD] |
| Last Updated | [YYYY-MM-DD] |

### Specification References

<!-- Link to the spec(s) this design implements -->

| Spec ID | Title | Requirements Addressed |
|---------|-------|------------------------|
| [SPEC-NNN](../specs/NNN-name.md) | [Spec title] | REQ-F1, REQ-F2, REQ-N1... |

### Related Documents

| Document | Relationship |
|----------|--------------|
| [Document name/link] | [Implements \| Extends \| Depends on] |

---

## 1. Overview

<!--
High-level summary of the design approach.
Answer: "How does this design solve the problem stated in the spec?"

Keep this to 2-3 paragraphs maximum.
Should be understandable by non-technical stakeholders.
-->

### 1.1 Design Summary

[Brief description of the overall approach and key design decisions]

### 1.2 Design Principles

<!-- What principles guided this design? These complement charter principles. -->

- [Principle 1: e.g., "Favor composition over inheritance"]
- [Principle 2: e.g., "Fail fast, recover gracefully"]
- [Principle 3: e.g., "Community health workers are the primary implementers"]

### 1.3 Requirements Coverage

<!-- Quick traceability matrix - which requirements does this design address? -->

| Requirement | Design Section | Approach |
|-------------|----------------|----------|
| REQ-F1 | COMP-1, INT-1 | [Brief description] |
| REQ-F2 | COMP-2 | [Brief description] |
| REQ-N1 | Section 5 | [Brief description] |

---

## 2. Architecture

<!--
High-level structure of the solution.
This section varies by domain - use the appropriate subsection.
-->

### For Software Projects:

<!--
Describe the system architecture.
Include diagrams if helpful (can be ASCII, Mermaid, or reference external files).
-->

#### 2.1 System Context

<!-- How does this system fit into the broader environment? -->

```
[ASCII diagram or description of system context]

Example:
┌─────────┐     ┌─────────────┐     ┌──────────┐
│  User   │────▶│   System    │────▶│ Database │
└─────────┘     └─────────────┘     └──────────┘
                      │
                      ▼
               ┌─────────────┐
               │ External API│
               └─────────────┘
```

[Description of context and boundaries]

#### 2.2 Architecture Pattern

<!-- What architectural pattern is used and why? -->

**Pattern:** [e.g., Layered, Microservices, Event-driven, Monolith]

**Rationale:** [Why this pattern fits the requirements]

**Trade-offs:**
- Pros: [Benefits of this approach]
- Cons: [Drawbacks accepted]

#### 2.3 Technology Choices

| Layer/Concern | Technology | Rationale |
|---------------|------------|-----------|
| [e.g., Frontend] | [e.g., React] | [Why chosen] |
| [e.g., Backend] | [e.g., Node.js] | [Why chosen] |
| [e.g., Database] | [e.g., PostgreSQL] | [Why chosen] |
| [e.g., Auth] | [e.g., OAuth2/OIDC] | [Why chosen] |

---

### For Public Health Projects:

<!--
Describe the intervention/program architecture.
How does the intervention work? What are the components?
-->

#### 2.1 Logic Model

<!-- Visual or textual representation of the intervention theory -->

```
Inputs → Activities → Outputs → Outcomes → Impact

[Describe each stage]
```

#### 2.2 Intervention Components

| Component | Description | Evidence Base |
|-----------|-------------|---------------|
| [Component 1] | [What it does] | [Supporting research] |
| [Component 2] | [What it does] | [Supporting research] |

#### 2.3 Delivery Model

**Setting:** [Where intervention occurs]
**Frequency:** [How often]
**Duration:** [How long]
**Delivered by:** [Who implements]

---

### For Research Projects:

<!--
Describe the study design and methodology architecture.
-->

#### 2.1 Study Design

**Design Type:** [e.g., RCT, Cohort, Case-control, Qualitative]

**Rationale:** [Why this design answers the research questions]

#### 2.2 Conceptual Framework

<!-- How variables/concepts relate to each other -->

```
[Diagram or description of conceptual model]
```

#### 2.3 Methodological Approach

| Aspect | Approach | Justification |
|--------|----------|---------------|
| Sampling | [Strategy] | [Why appropriate] |
| Data Collection | [Methods] | [Why appropriate] |
| Analysis | [Techniques] | [Why appropriate] |

---

## 3. Components

<!--
Detailed design of individual components/modules.
Each component gets an ID (COMP-1, COMP-2) for traceability.

For software: Classes, modules, services
For public health: Program components, materials, training modules
For research: Instruments, procedures, analysis scripts
-->

### COMP-1: [Component Name]

**Purpose:** [What this component does]

**Satisfies:** [REQ-F1, REQ-F2, etc.]

**Responsibilities:**
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

**Dependencies:**
- [What this component needs]

**Key Design Decisions:**
- [Decision 1 and rationale]
- [Decision 2 and rationale]

<!--
For software, include:
- Public interface/API
- Key algorithms
- State management approach

For public health, include:
- Materials needed
- Training requirements
- Fidelity indicators

For research, include:
- Instrument details
- Validity/reliability considerations
- Scoring/coding approach
-->

---

### COMP-2: [Component Name]

**Purpose:** [What this component does]

**Satisfies:** [REQ-F3, etc.]

**Responsibilities:**
- [Responsibility 1]
- [Responsibility 2]

**Dependencies:**
- [What this component needs]

---

## 4. Interfaces

<!--
How components communicate/connect.
Each interface gets an ID (INT-1, INT-2) for traceability.

For software: APIs, events, data contracts
For public health: Handoffs, referral processes, communication protocols
For research: Data transfer procedures, participant interfaces
-->

### INT-1: [Interface Name]

**Connects:** [COMP-1] ↔ [COMP-2]

**Type:** [API \| Event \| File \| Protocol \| Handoff]

**Direction:** [Unidirectional \| Bidirectional]

<!--
For software APIs, include:
- Endpoint/method signatures
- Request/response formats
- Error handling
- Authentication requirements

For public health, include:
- Trigger conditions
- Information exchanged
- Responsible parties
- Timeline requirements

For research, include:
- Data format
- Transfer mechanism
- Security/privacy measures
-->

**Contract:**
```
[Interface specification - format depends on type]

Example for REST API:
POST /api/v1/resource
Request: { "field": "value" }
Response: { "id": "123", "status": "created" }
Errors: 400 (validation), 401 (auth), 500 (server)

Example for handoff:
Trigger: Patient discharge
From: Hospital care coordinator
To: Community health worker
Information: Discharge summary, follow-up appointments, medication list
Timeline: Within 24 hours of discharge
```

---

### INT-2: [Interface Name]

**Connects:** [Component] ↔ [External System/Actor]

**Type:** [Type]

**Contract:**
```
[Specification]
```

---

## 5. Data Model

<!--
How data/information is structured and stored.
Each entity gets an ID (DATA-1, DATA-2) for traceability.

For software: Database schemas, data structures
For public health: Data collection forms, registries, tracking systems
For research: Variables, datasets, codebooks
-->

### 5.1 Entity Overview

```
[Entity relationship diagram or description]

Example:
┌─────────┐     ┌─────────────┐     ┌──────────┐
│  User   │────▶│   Session   │────▶│ Activity │
└─────────┘     └─────────────┘     └──────────┘
     │
     ▼
┌─────────┐
│ Profile │
└─────────┘
```

### DATA-1: [Entity/Dataset Name]

**Purpose:** [What this data represents]

**Used by:** [COMP-1, COMP-2, etc.]

**Schema/Structure:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| [field_name] | [type] | [Yes/No] | [What it stores] |
| [field_name] | [type] | [Yes/No] | [What it stores] |

**Constraints:**
- [Constraint 1: e.g., "email must be unique"]
- [Constraint 2: e.g., "age must be 18+"]

**Retention:** [How long data is kept, deletion policy]

---

### DATA-2: [Entity/Dataset Name]

**Purpose:** [What this data represents]

**Schema/Structure:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| [field_name] | [type] | [Yes/No] | [What it stores] |

---

## 6. Design Decisions

<!--
Key decisions made during design and their rationale.
Each decision gets an ID (DEC-1, DEC-2) for reference.
These are smaller than ADRs but important to document.
-->

### DEC-1: [Decision Title]

**Context:** [What situation prompted this decision]

**Decision:** [What was decided]

**Rationale:** [Why this choice was made]

**Alternatives Considered:**
- [Alternative 1]: [Why rejected]
- [Alternative 2]: [Why rejected]

**Consequences:**
- [Positive consequence]
- [Trade-off accepted]

---

### DEC-2: [Decision Title]

**Context:** [Situation]

**Decision:** [Choice made]

**Rationale:** [Reasoning]

---

## 7. Implementation Considerations

<!--
Guidance for implementing this design.
This section feeds directly into DIPs.
-->

### 7.1 Implementation Order

<!-- Suggested sequence for building components -->

| Order | Component | Dependencies | Notes |
|-------|-----------|--------------|-------|
| 1 | [COMP-X] | None | [Start here because...] |
| 2 | [COMP-Y] | COMP-X | [Build after X because...] |
| 3 | [INT-1] | COMP-X, COMP-Y | [Connect X and Y] |

### 7.2 Risk Areas

<!-- What parts of this design are risky or complex? -->

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk 1] | [What could go wrong] | [How to address] |
| [Risk 2] | [What could go wrong] | [How to address] |

### 7.3 Testing Strategy

<!-- How should this design be validated? -->

| Level | Approach | Covers |
|-------|----------|--------|
| Unit | [Testing approach] | [COMP-1, COMP-2] |
| Integration | [Testing approach] | [INT-1, INT-2] |
| System | [Testing approach] | [End-to-end flows] |

### 7.4 Security Considerations

<!-- Security aspects relevant to this design -->

- [Security consideration 1]
- [Security consideration 2]
- [Data privacy requirements]

### 7.5 Performance Considerations

<!-- Performance aspects relevant to this design -->

- [Performance target 1]
- [Scalability consideration]
- [Resource constraints]

---

## 8. Out of Scope

<!--
What this design explicitly does NOT cover.
Inherit from spec and add design-specific exclusions.
-->

**From Specification (inherited):**
- [Item from spec's out of scope]

**Design-Specific Exclusions:**
- [Design decision not to include X]
- [Future enhancement Y not addressed]

---

## 9. Open Questions

<!--
Unresolved design questions.
Aim to resolve before implementation begins.
-->

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| DQ-1 | [Design question] | Open \| Resolved | [Answer if resolved] |
| DQ-2 | [Design question] | Open \| Resolved | [Answer if resolved] |

---

## 10. Appendices

### A. Glossary

<!-- Domain-specific terms used in this design -->

| Term | Definition |
|------|------------|
| [Term] | [Definition] |

### B. References

- [SPEC-NNN: Specification title](../specs/NNN-name.md)
- [External reference 1]
- [External reference 2]

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | [YYYY-MM-DD] | [Name] | Initial draft |

---

<!--
NEXT STEPS AFTER DESIGN APPROVAL:

1. Break down into tasks: /breakdown
   - Creates Todoist tasks referencing COMP-N, INT-N sections

2. Generate DIPs: /define
   - Each DIP references:
     - Spec sections (REQ-F1, UC-1, AC-1)
     - Design sections (COMP-1, INT-1, DEC-1)

3. Implement: /build
   - Execute DIPs with git safety

The section IDs (COMP-N, INT-N, DATA-N, DEC-N) enable precise
task scoping and DIP generation.
-->
