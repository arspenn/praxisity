# Praxisity Command Evaluation: Opus 4.5 Compatibility

**Date:** December 2025  
**Scope:** Evaluate existing commands against current Claude Code best practices  
**Verdict:** Polish needed, not massive redesign

---

## Executive Summary

Your commands are **well-architected but over-specified for Opus 4.5**. The core design philosophy (guided prompting, PLANNING.md integration, template-driven output) is sound. However, the implementation style was tuned for earlier models that needed more hand-holding. Opus 4.5's improved instruction-following means your current commands may trigger over-engineering and unnecessary complexity.

**Bottom line:** You need refinement, not redesign. The architecture is correct; the prose is too aggressive.

---

## Quantitative Assessment

| Command | Estimated Lines | Character Count | Verdict |
|---------|-----------------|-----------------|---------|
| `/spec` | ~400+ | ~15,000+ | ⚠️ At/over budget |
| `/architect` | ~400+ | ~15,000+ | ⚠️ At/over budget |
| `/breakdown` | ~300+ | ~12,000+ | ✅ Within budget |
| `/define` | ~300+ | ~12,000+ | ✅ Within budget |
| `/charter` | ~460 | ~18,000+ | ⚠️ Over budget |
| `/new-project` | ~360 | ~14,000+ | ✅ Near budget |

**Budget reference:** 15,000 characters per command (official), ~300 lines practical max

---

## Issue #1: Aggressive Language Patterns (HIGH PRIORITY)

Your commands use enforcement language designed for Sonnet 3.5's undertriggering. Opus 4.5 will overtrigger on these.

### Examples Found

```markdown
# Current (too aggressive for Opus 4.5)
**If CHARTER.md does NOT exist:**
- Show error: "Spec template not found..."
- Exit command

**Validation:**
- Must select a valid spec
- Parse the selected spec file to extract...
```

### Recommended Approach

```markdown
# Calmer alternative
If CHARTER.md doesn't exist, note this and ask whether to continue.

Validation: Select a valid spec and parse its contents.
```

### Specific Patterns to Soften

| Current Pattern | Opus 4.5 Alternative |
|-----------------|---------------------|
| "MUST", "REQUIRED", "CRITICAL" | Remove or use "should" |
| Bullet-pointed error conditions | Prose descriptions |
| Explicit exit conditions | Let Claude judge context |
| Repeated safety warnings | State once, trust the model |

---

## Issue #2: Over-Specification of Steps (MEDIUM PRIORITY)

Your commands enumerate every micro-step. Opus 4.5 can infer intermediate steps from goals.

### Example: `/spec` Pre-Flight Checks

Current structure has ~100 lines just for pre-flight:
1. Read PLANNING.md
2. Check for Charter
3. Check for Spec Template  
4. Determine Next Spec Number
5. Create Specs Directory

**Opus 4.5 approach:** 
```markdown
Before creating the spec:
1. Check PLANNING.md for session context
2. Verify CHARTER.md exists (warn if not)
3. Determine next spec number from .plans/specs/
4. Read the spec template
```

Same outcome, 75% fewer tokens.

---

## Issue #3: Redundant Context (MEDIUM PRIORITY)

Each command re-explains concepts that should live in CLAUDE.md or be inferred.

### Examples of Redundant Content

- Purpose sections explaining what specs/designs are (Claude knows)
- Repeated explanations of the design-first philosophy
- Duplicate PLANNING.md integration instructions in every command
- Template location paths repeated rather than referenced

### Recommendation

Move shared concepts to CLAUDE.md (which you already have well-structured). Commands should reference, not repeat:

```markdown
# Instead of 50 lines explaining PLANNING.md integration
Follow standard PLANNING.md workflow (see CLAUDE.md).
```

---

## Issue #4: Missing Simplicity Constraints (HIGH PRIORITY)

Opus 4.5 over-engineers without explicit constraints. Your commands lack these guardrails.

### Add to Each Command

```markdown
## Constraints
- Only gather information explicitly needed for this command
- Don't add features or sections not specified in the template
- Keep interactions focused - one question or action at a time
- If uncertain, ask rather than assume
```

---

## What You're Doing Right

### Strong Patterns to Keep

1. **Frontmatter structure** - Your `description` and `tags` frontmatter is correct
2. **Template-driven output** - Referencing `.praxisity/templates/` reduces hallucination
3. **PLANNING.md state management** - Excellent for session persistence
4. **Section IDs (REQ-F1, COMP-1)** - Enables traceability, good for DIPs
5. **Pre-flight checks concept** - Just needs condensing
6. **Success message patterns** - Clear next-step guidance

### Architecture Decisions That Hold Up

- Commands in `.claude/commands/` (standard location)
- Templates separate from commands
- CLAUDE.md for stable config, PLANNING.md for dynamic state
- Git safety as a cross-cutting concern

---

## Recommended Refactoring Approach

### Phase 1: Quick Wins (Before Week 3)

1. **Add simplicity constraints** to each command header
2. **Remove aggressive language** (MUST, CRITICAL, REQUIRED)
3. **Condense pre-flight checks** to numbered lists, not subsections

Estimated effort: 1-2 hours per command

### Phase 2: Structural Optimization (Week 3-4)

1. **Extract shared patterns** to CLAUDE.md references
2. **Reduce step granularity** - let Claude infer intermediate steps
3. **Add explicit "don't over-engineer" warnings** where complexity is tempting

Estimated effort: 30 min per command

### Phase 3: Testing (Week 4)

1. Test each command with Opus 4.5 specifically
2. Note where it over-engineers or adds unrequested features
3. Add targeted constraints for those patterns

---

## Specific Command Notes

### `/spec`
- Pre-flight section is ~25% of command - condense to 10%
- "Specification Creation Flow" section is well-structured
- Domain-specific questions section is valuable, keep it
- Success message is good

### `/architect`
- Strong spec-validation logic
- Requirement coverage matrix is valuable
- Could merge similar sections (both have extensive validation flows)

### `/breakdown`
- Todoist MCP integration is unique value
- Micro-chunking rules are ADHD-informed, keep them
- Task creation loop could be simplified

### `/define`
- DIP concept is strong differentiator
- Template population logic is appropriate detail level
- TodoWrite integration is valuable

### `/charter`
- Longest command - prime candidate for condensing
- 8-section guided questionnaire is probably too granular for Opus 4.5
- Consider: fewer questions, let Claude probe deeper as needed

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Commands over budget trigger truncation | Medium | High | Condense before Week 3 |
| Opus 4.5 over-engineers outputs | High | Medium | Add simplicity constraints |
| Current commands work fine | Low | None | Test before changing |

---

## Conclusion

**Don't redesign. Refactor.**

Your command architecture is sound and reflects good context engineering principles. The issues are:

1. **Verbosity** - 20-30% reduction possible without losing function
2. **Tone** - Too aggressive for Opus 4.5's improved instruction-following
3. **Missing guardrails** - Need explicit simplicity constraints

Spend 4-6 hours before Week 3 on Phase 1 refinements. This is polish, not reconstruction.

---

*Evaluation based on December 2025 Claude Code best practices and Opus 4.5 migration documentation.*
