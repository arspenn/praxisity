# Describe Skill Clarity Report

1. **Undefined frontmatter metadata (SKILL.md line 5)**
   - Quote: "argument-hint: '[title, or an existing SPEC-NNN to revise]'"
   - Unclear: What is "argument-hint" and how does it define the skill's input mechanism?

2. **Undefined skill invocation (SKILL.md line 32)**
   - Quote: "Invoke the `gather` skill with the Skill tool so its protocol is in context before the first section is presented."
   - Unclear: How does one "invoke" a skill with a tool? What is the syntax or specific tool call?

3. **Implicit argument passing mechanism (SKILL.md line 33)**
   - Quote: "If the argument names an existing spec by ID or title... Otherwise this is a new spec... use the argument as the working title if one was given."
   - Unclear: What is "the argument" and how is it passed to the skill? Via CLI string? Is the mechanism the same as the charter skill?

4. **Directory listing operation undefined (SKILL.md line 33)**
   - Quote: "list `.plans/specs/` (create it if missing), take the next number"
   - Unclear: Is "list" a tool call (Glob) or shell command? When does "create it if missing" occur—before or after listing?

5. **Automatic drafting contradicts gather protocol (SKILL.md line 51)**
   - Quote: "With source material, draft each one; approval is fast."
   - Unclear: Does describe always draft requirements when source material exists, or only when gather-style is `draft-first`? This contradicts gather/SKILL.md which makes drafting conditional.

6. **Shell command contradicts tool workflow (SKILL.md line 72)**
   - Quote: "`cp` the template to `.plans/specs/NNN-[slug].md` with `cp` in Bash (NNN zero-padded to three digits)."
   - Unclear: How does a skill invoke bash? Line 69 says "use Edit" not shell. This contradicts the tool-based workflow.

7. **ID sequencing order ambiguous (SKILL.md line 79)**
   - Quote: "number OBJ, REQ-F, REQ-N, UC, AC, and Q sequentially in the order gathered"
   - Unclear: For checklist sections (Non-Functional Requirement categories), what is "the order gathered"? Do unchecked categories skipped by the user leave gaps, or are they renumbered?

8. **Versioning scheme unspecified (SKILL.md line 81)**
   - Quote: "append a Revision History row with the next minor version"
   - Unclear: What increment pattern should follow v0.1? Is it v0.2, v1.0, or per semantic versioning rules not stated here?

9. **Missing interaction for template field (SKILL.md vs. Template line 28)**
   - Quote (Template): "Charter Reference | [CHARTER.md](../../CHARTER.md) — [principles this spec serves]"
   - Unclear: SKILL.md never instructs gathering "principles this spec serves," yet template has a placeholder for it. Who fills this field and when?

10. **Domain vocabulary detection unspecified (SKILL.md line 53 vs. Template lines 113–118)**
    - Quote (SKILL.md): "Frame each in the field's vocabulary per the template comment."
    - Quote (Template): Shows four vocabularies (Software, Public health, Research, Instructional design).
    - Unclear: How does the skill detect the project's domain or know which vocabulary to use? No logic is specified.

---

## Summary

Ten clarity gaps found. Frontmatter metadata "argument-hint" and skill invocation syntax are undefined. The "argument" passing mechanism is unclear. Directory listing and bash invocation operations contradict tool-based workflow. Automatic requirement drafting conflicts with conditional gather protocol. ID sequencing and versioning schemes lack specification. Template placeholder for "principles this spec serves" is never gathered. Domain vocabulary selection is unspecified despite template showing four options.
