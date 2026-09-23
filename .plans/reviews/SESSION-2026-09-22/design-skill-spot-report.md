# Design Skill Clarity Report

1. **Shell command contradicts tool workflow (SKILL.md line 35, 78)**
   - Quote: "List `.plans/designs/` with `ls` in Bash (create it if missing)."
   - Unclear: How does a skill invoke bash? The workflow elsewhere uses Edit tools, not shell. Also, when does "create if missing" occur—before or after `ls`?

2. **Bare argument syntax unspecified (SKILL.md line 35)**
   - Quote: "If the argument is an existing design number (`DESIGN-004` or bare `004`)"
   - Unclear: What is "bare `004`"? Can the user type `/design 004` and it resolves to DESIGN-004, or is this different from `/describe`'s argument parsing?

3. **Spec reference in PLANNING.md mechanism (SKILL.md line 36)**
   - Quote: "If PLANNING.md names an active spec, offer it as the default"
   - Unclear: How and when does PLANNING.md "name" a spec? Is this set by `/describe`, by the user, or by the framework?

4. **Ambiguous field request phrasing (SKILL.md line 37)**
   - Quote: "If it does not exist, ask the field once."
   - Unclear: Does "ask the field" mean ask the user what field the project is in? This phrasing is awkward and could mean ask for a form field.

5. **Author gathering timing undefined (SKILL.md line 50)**
   - Quote: "Author defaults to `git config user.name`; if unavailable, ask here."
   - Unclear: Is Author asked during the Title prompt, or in a separate prompt? "Ask here" is vague about the pacing.

6. **Field detection for examples unspecified (SKILL.md line 53)**
   - Quote: "Show the template comment's examples for the project's field even in brief mode"
   - Unclear: How does the skill determine which of the template's four field vocabularies (Software, Public health, Research, Instructional design) to use? Read CHARTER.md, ask the user, or infer?

7. **Trigger for drafting candidates undefined (SKILL.md line 54)**
   - Quote: "Draft candidates from the spec's use cases when the user is unsure where to start."
   - Unclear: How does the skill detect that the user is "unsure"? Should it prompt, or infer from silence?

8. **Circular flow: new/revise decision vs. spec existence (SKILL.md lines 35-36)**
   - Quote: "Decide new or revise... Otherwise this is a new design... If a design for this spec already exists, say so and ask once: revise it, or create an alternative."
   - Unclear: Step 4 decides new/revise based on argument, then step 5 asks again if a design for that spec exists. Why two decision points? Should step 4 skip this for new designs?

9. **Status transitions never specified (SKILL.md vs. Template line 31)**
   - Quote (Template): "Status moves through: Draft → In Review → Approved → Superseded."
   - Unclear: The template shows four statuses, but the skill only sets Draft for new designs. Who moves a design to In Review, Approved, or Superseded? No workflow is defined.

10. **Requirements Coverage: required but pacing unspecified (SKILL.md line 21, 58)**
    - Quote: "Every MUST requirement... must be satisfied... Build the matrix from every element's Satisfies list."
    - Unclear: This section is marked "Drafted by you" (no user prompt) yet is "required." How can the user approve or edit it if it is only presented for review, not gathered?

---

## Summary

Ten clarity gaps in the design skill. Shell commands contradict the tool workflow. Bare argument syntax differs from describe without explanation. PLANNING.md's role in naming active specs is undefined. Field detection for vocabulary examples is unspecified. Author gathering timing is ambiguous. User unsureness trigger for drafting candidates lacks definition. Step 4 and 5 create a circular new/revise decision flow. Template shows four status transitions but skill never transitions them. Requirements Coverage is required yet only drafted without user input pacing. Versioning increments are specified (0.1→0.2) but status workflow is not.
