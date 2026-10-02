# Detail Skill Clarity Review

## Issues Found

1. **Step ordering contradiction** (SKILL.md line 31): "Step 2 lands first so that an interrupted run still leaves PLANNING.md accurate" contradicts the introduction "Run these steps in order and finish each before starting the next." It is unclear whether steps should be reordered or completed sequentially.

2. **Undefined invocation mechanism** (SKILL.md line 35): "Invoke the `gather` skill with the Skill tool so its protocol is in context before the first section is presented." The phrase "the Skill tool" is not defined, and "so its protocol is in context" is vague about the purpose or mechanism.

3. **Element attributes undefined** (SKILL.md lines 52–54): "Element's Purpose," "Responsibilities," "Dependencies," "Satisfies list," and "coverage matrix" are referenced as source material but never defined or located within design documents. An executing agent reading this cold cannot identify what these sections are or where to find them.

4. **Ambiguous phrasing** (SKILL.md line 51): "Author defaults to `git config user.name`; if unavailable, ask alongside." The phrase "ask alongside" is incomplete—ask alongside what prompt or action?

5. **Undefined term** (SKILL.md line 37): "Custom DIP" is introduced without definition. Does it follow the same template and structure as a normal DIP, or is its format different?

6. **Template abbreviations unexplained** (dip.template.md lines 70–83): COMP, INT, DATA, DEC, REQ, UC, AC are used without definition. An executing agent cannot map these to sections of the design or spec without external knowledge.

7. **Spec reference path unclear** (SKILL.md line 37 and dip.template.md line 47): Step 5 says "read the spec it references" and the template lists `[SPEC-MMM]`, but how does an executing agent discover which spec the design links to? The reference path is not specified.

8. **Artifact scope format ambiguous** (dip.template.md lines 146–150): "Artifacts in Scope" uses code blocks with paths, but does not specify whether paths are mandatory, how to handle generated vs. checked-in files, or the path format (relative, absolute, glob patterns).

9. **Verification failure escalation undefined** (dip.template.md line 38): "If a verification fails... stop and ask rather than improvise." Ask whom? An AI executing this document has no recipient defined.

10. **Test column scope unclear** (dip.template.md line 162): The Acceptance Criteria table's "Test" column shows `[Command or check]` but does not distinguish manual judgment from automated tests or state whether all criteria must have runnable tests.

## Summary

The skill assumes executing agents know where design attributes (Purpose, Responsibilities, Dependencies) live, what design/spec abbreviations mean (COMP, REQ, UC), and how to locate linked specs. Template paths and artifact scope formats are ambiguous. Verification failure and test validation flows lack clear escalation or acceptance rules for agents with no project memory.
