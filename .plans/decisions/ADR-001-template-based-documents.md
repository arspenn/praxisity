# ADR-001: Template-Based Documents Over AI Generation

**Date:** 2025-12-18
**Status:** Accepted
**Deciders:** Framework Architect
**Tags:** templates, ai-generation, user-experience, quality

## Context

When creating project artifacts (CHARTER.md, specifications, designs), we need to decide how users create these documents with AI assistance. There are two primary approaches:

1. **Templates** - Users fill in structured templates with AI help
2. **Full Generation** - AI generates complete documents from prompts

The framework must balance:
- Quality and thoughtfulness of outputs
- User engagement with the planning process
- Reduction of AI hallucination
- Ease of use
- Consistency across projects

## Decision

We will use **fillable templates** for all major project artifacts (charter, specifications, designs, DIPs) rather than full AI generation.

Templates are:
- Structured markdown with placeholder sections
- Self-documenting with HTML comments explaining each section
- Include domain-specific examples
- Filled in by users with AI assistance (not auto-generated)

## Rationale

**Promotes thoughtful engagement:**
When users fill in templates, they must think deeply about each section. The charter isn't just boilerplate - it requires real consideration of mission, principles, and scope.

**Reduces AI hallucination:**
Templates provide structure and constraints. AI helps with wording and suggestions, but doesn't fabricate entire strategies or make up technical decisions.

**Ensures completeness:**
Templates explicitly prompt for all necessary sections. Users can't forget important parts like "out of scope" or "constraints."

**Maintains consistency:**
All projects follow the same structure, making it easier to understand any Praxisity project. The charter always has the same sections in the same order.

**Enables meaningful defaults:**
Templates can show examples without prescribing solutions. Users see what good looks like without being locked into a specific approach.

**Preserves user control:**
Users make decisions; AI assists. This is critical for governance documents like the charter that shape the entire project.

## Alternatives Considered

### Alternative 1: Full AI Generation

**Description:** User provides high-level prompt (e.g., "I want to build a task manager"), AI generates complete charter, specs, designs.

**Pros:**
- Faster initial setup
- Lower cognitive load for users
- Impressive demo experience

**Cons:**
- Users don't deeply engage with content
- AI may hallucinate features, constraints, or strategies
- Less ownership of planning artifacts
- Harder to customize for specific needs
- Generic outputs that feel boilerplate
- Requires extensive review/editing anyway

**Why not chosen:** The cost of hallucination and shallow engagement outweighs the speed benefit. Planning artifacts are governance documents - they need to be thoughtfully created, not auto-generated.

### Alternative 2: Hybrid (Generate Then Edit)

**Description:** AI generates initial document, user edits to refine.

**Pros:**
- Faster than pure templates
- Provides starting point
- User still reviews content

**Cons:**
- Users often accept AI-generated content uncritically
- Editing is harder than filling blanks (decision fatigue)
- Still risk of hallucination in initial generation
- Users may not understand why certain sections exist

**Why not chosen:** Editing is cognitively harder than filling. Templates prompt thought; generation prompts acceptance. We want users to think, not just approve.

### Alternative 3: Wizards/Forms

**Description:** Interactive forms that gather input and generate structured output.

**Pros:**
- Guided experience
- Validated inputs
- Structured data collection

**Cons:**
- Rigid - hard to adapt to different project types
- Form UI disconnects from final document
- Harder to implement in markdown-based system
- Loses the "edit the document directly" workflow

**Why not chosen:** Templates provide guidance without rigidity. Users work directly with the artifact they're creating, not a separate form.

## Consequences

### Positive Consequences

- **Higher quality artifacts:** Users think deeply about their project
- **Better AI assistance:** AI helps with wording, not fabrication
- **Clearer expectations:** Templates show what information is needed
- **Easier customization:** Users can modify templates for their needs
- **Domain flexibility:** One template works for software/public health/research
- **Version control friendly:** Templates are plain markdown
- **Educational:** Users learn what makes a good charter/spec/design

### Negative Consequences

- **Slower initial setup:** Filling templates takes more time than generation
- **Requires user engagement:** Users must think, can't just accept AI output
- **More cognitive load:** Users make all decisions (though AI assists)
- **Less "magic":** Templates feel less impressive than full generation

### Neutral Consequences

- **Template maintenance:** Templates need updating as framework evolves
- **Example quality matters:** Poor examples in templates hurt user experience

## Implementation Notes

**Template Design Principles:**
1. Self-documenting with HTML comments
2. Domain-specific examples (software/public health/research)
3. Clear placeholder formatting: `[BRACKETED]`
4. Guidance marked for removal in final docs
5. Optional sections clearly marked
6. Under 300 lines (minimize length, don't exclude critical info)

**Commands Use Templates:**
- `/charter` - Uses `charter.template.md`, walks user through filling
- `/spec` - Will use `spec.template.md` (Week 2)
- `/architect` - Will use `design.template.md` (Week 2)
- `/define` - Will use `dip.template.md` (Week 2)

**AI Role:**
- Suggests wording improvements
- Provides domain-specific examples
- Asks clarifying questions
- Does NOT auto-fill entire sections

## References

- CLAUDE.md: Template Design Principles (lines 87-102)
- `.praxisity/templates/charter.template.md`
- `.praxisity/templates/claude.template.md`
- `/charter` command implementation

---

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2025-12-18 | Initial version | Framework Architect |
