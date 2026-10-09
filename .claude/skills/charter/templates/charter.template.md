# [Project Name] — Project Charter

<!--
This template produces the project's constitution: the document that guides every
decision in the project, including how AI assists. Claude reads it at the start of
each session (via CLAUDE.md), so it is written for two readers at once: the humans
who own the project and the AI that works on it. That means it must be self-contained —
a reader with no other project context should understand every term in it.

Each section's comment says what the section needs and gives examples. The comments
are stripped from the finished charter. Placeholder rows are illustrative: lists and
tables take as many rows as the project has content for.

Two markers are allowed in place of content:
- "N/A — [reason]" when a section genuinely does not apply
- "TBD — revisit at [milestone]" when it cannot be known yet (common on a first pass)

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

## Mission

<!-- One clear sentence: what does this project exist to accomplish?
     Good: "Reduce hospital readmissions for heart failure patients through AI-powered care coordination"
     Bad:  "Make healthcare better"
     Good: "Design a self-paced onboarding module that gets new volunteers field-ready in one week"
     Bad:  "Create a training course"
-->

[One sentence mission statement]

## Principles

<!-- The values that decide hard choices. Ask: "If we face a tough trade-off, what settles it?"
     Specific to this project, not generic platitudes. As many as the project needs, no fixed count.

     Praxisity suggests one principle to every project, because the framework only grows
     through use; include it if you want the sessions to practise it:
     - Bootstrapping: use the system to build the system, and to build yourself. At the end
       of each session, ask what was learned that should become a skill, agent, or template,
       and capture it before closing.

     Other examples:
     - Privacy-first: user data never leaves their device
     - Evidence-based: every intervention is backed by peer-reviewed research
     - Learner-paced: no timed assessments; mastery is demonstrated, not scheduled
     - Fail-safe: the system defaults to a safe state on any error
-->

1. [Principle, and what it means in practice]
2. [Principle, and what it means in practice]

## Scope

<!-- Clear boundaries prevent scope creep. Out of Scope is the more important half:
     list the things people might reasonably expect that this project will not deliver.
-->

### In Scope

<!-- Features, capabilities, deliverables, and audiences this project addresses.
     Examples:
     - Web-based interface for desktop and mobile browsers
     - One asynchronous module covering the intake workflow, ~90 minutes of learner time
     - Integration with existing EHR systems via FHIR API
-->

- [In-scope item]
- [In-scope item]

### Out of Scope

<!-- Examples:
     - Native mobile apps (web only for MVP)
     - Instructor-led delivery (self-paced only)
     - Diagnostic capabilities (care coordination only)
-->

- [Excluded item]
- [Excluded item]

## Stakeholders

<!-- Who is involved or affected. Fill the categories that apply; a solo project may
     list one person in two roles.
     Examples: learners in the module; nurses coordinating discharge; the instructor
     grading the deliverable; an IT department that maintains an integration.
-->

**Primary Users/Beneficiaries:**
- [Who directly uses or benefits from this project]

**Contributors:**
- [Who builds or maintains it]

**Secondary Stakeholders:**
- [Who is indirectly affected or has input]

**Advisory/Oversight:**
- [Who provides guidance or approval]

## Success Criteria

<!-- How you will know it worked. Outcomes, not just outputs. Measurable where possible.
     On a first pass it is normal not to know these yet; mark them TBD with the milestone
     at which you will.
     Examples:
     - Reduce 30-day readmission rate by 15% within 6 months
     - 80% of pilot learners pass the post-module assessment on the first attempt
     - Complete IRB approval and enroll the first participant by Q2 2026
-->

**Primary Success Metrics:**
- [Measurable outcome]

**Milestones:**
- [Time-bound achievement]

**Quality Indicators:**
- [How quality is judged]

## Constraints

<!-- What limits the work. Honest constraints make realistic plans.
     Timeline: deadlines, funding periods, term dates
     Resources: budget, team size, tooling, available hours
     Technical: platform requirements, integrations, performance
     Regulatory/Compliance: IRB, HIPAA, FERPA, GDPR, accessibility law
     Other: organizational, methodological, anything else that narrows choices
-->

**Timeline:**
- [Deadline or time constraint]

**Resources:**
- [Budget, people, or tooling limitation]

**Technical:**
- [Platform, performance, or integration constraint]

**Regulatory/Compliance:**
- [Legal, ethical, or domain-specific requirement]

**Other:**
- [Any other constraint that limits choices]

## Domain Context

<!-- The field-specific knowledge that shapes the work. Three questions transfer across
     every domain; answer them in the vocabulary of this project's field.

     1. Guiding frameworks — which theories, models, standards, or evidence base direct the work?
        Software: architecture style and why. Public health: theoretical framework, evidence base,
        theory of change. Research: research questions, theoretical framework. Instructional
        design: ID model (ADDIE, SAM, Dick & Carey...), learning theory, learner analysis.
     2. Methods and tools — how is the work delivered, and with what?
        Software: tech stack, infrastructure. Public health: intervention and delivery model,
        target population. Research: methodology, data sources, analysis plan. Instructional
        design: delivery modality, authoring tools, LMS.
     3. Quality and evaluation — how does this field judge whether the work is good?
        Software: testing, performance targets, security. Public health: evaluation approach.
        Research: contribution to the field, validity. Instructional design: evaluation model
        (Kirkpatrick...), assessment strategy, accessibility standards.
-->

**Domain:** [The field this project belongs to]

**Guiding Frameworks:**
- [Theory, model, standard, or evidence base — and how it applies here]

**Methods and Tools:**
- [How the work is delivered and what it is built with]

**Quality and Evaluation:**
- [How this field judges the work, and how this project will be judged]

**Key Context:**
- [Anything else a newcomer to this domain must know to work on this project]

---

## Glossary

<!-- Define every term in this charter that a reader without project context would not
     know: project-specific terminology, acronyms, and any concept in the principles or
     scope that carries a specific meaning here. The charter is read by AI as well as
     people, so undefined terms are a real gap, not a style issue.
     If only common terms are used, mark this section N/A.
-->

| Term | Definition |
|------|------------|
| [Term] | [Definition] |

---

## Charter Maintenance

<!-- Review schedule: quarterly, after major milestones, or when scope questions arise.
     Amendment process: how changes are made and who approves. For a solo project,
     "update via /charter" is a complete answer.
-->

**Review Schedule:** [When the charter is revisited]

**Amendment Process:** [How changes are made and approved]

---

*Charter established: [DATE]*
*Last reviewed: [DATE]*
*Next review: [DATE]*
