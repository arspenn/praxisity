# Charter Skill Clarity Report

## Issues Found

1. **Gathering protocol reference (SKILL.md line 37)**
   - Quote: "Present one section at a time. Wait for the user's response before moving to the next. For each section below, follow the gathering protocol (see /gather)."
   - Unclear: What is the `/gather` protocol? Is it a skill, a tool, or embedded guidance? If it's external, what happens if it changes or doesn't exist?

2. **HTML comment guidance scope (SKILL.md line 27)**
   - Quote: "Read it — the HTML comments are your guide for what to gather in each section."
   - Unclear: Should the skill follow ALL comments in the template, or only comments within placeholder sections? The template has comments at multiple levels (section headers, examples, tips).

3. **Domain type detection order (SKILL.md line 72)**
   - Quote: "Detect the project type from CLAUDE.md or ask the user. Then prompt for the domain-specific fields..."
   - Unclear: Should the skill attempt to read CLAUDE.md first and only ask if detection fails? Or ask first if uncertain? The "or" leaves the decision logic ambiguous.

4. **File creation command vs. tool constraint (SKILL.md lines 92, 94)**
   - Quote: "Copy template: `cp ${CLAUDE_SKILL_DIR}/templates/charter.template.md CHARTER.md`" followed by "Never use Write for template-derived files."
   - Unclear: How does the skill create the file without `Write`? The instruction implies shell execution (`cp` command), but then forbids Write. This contradicts the file creation workflow.

5. **Agent consultation syntax (SKILL.md lines 131–132)**
   - Quote: "`Agent(subagent_type: "stakeholder", prompt: "Does this charter serve its intended audience?")`"
   - Unclear: Is this pseudocode, a function call, or a tool invocation? The syntax and available parameters are undefined. Is `subagent_type: "stakeholder"` a valid parameter?

6. **Domain section selection workflow (SKILL.md line 72 vs. Template lines 178–245)**
   - Quote (SKILL.md): "Detect the project type from CLAUDE.md or ask the user. Then prompt for the domain-specific fields..."
   - Quote (Template): "Remove domain sections below that don't apply to your project."
   - Unclear: Should the skill ask the user which domain section to fill, or should it auto-detect and then remove non-matching sections? The flow is not explicit.

---

## Round 2: Revised Files

1. **Undefined operation: "Load the `gather` skill" (CHARTER/SKILL.md line 25)**
   - Quote: "Load the `gather` skill so its protocol is in context before the first section is presented."
   - Unclear: What does "load" mean? Is this a tool call? The skill does not specify the operation or mechanism.

2. **Drafting default contradicted (CHARTER/SKILL.md line 32 vs. GATHER/SKILL.md line 51)**
   - Quote (Charter): "a syllabus, assignment brief, rubric, proposal, or existing plan lets you draft sections for approval instead of prompting cold."
   - Quote (Gather): "New content is drafted only when `gathering-style` is `draft-first` and prior input or loaded documents explicitly cover the topic; otherwise prompt."
   - Unclear: Does charter always draft from source material, or only when gather-style is `draft-first`? The files appear to disagree on when drafting happens.

3. **Domain Context structure mismatch (CHARTER/SKILL.md line 48 vs. Template lines 157–169)**
   - Quote (Charter): "Domain Context | One prompt, the three template questions"
   - Quote (Template): Shows five fields: Domain, Guiding Frameworks, Methods and Tools, Quality and Evaluation, Key Context
   - Unclear: When does the "Domain" field get filled? Is it one of "the three questions" or separate? The charter says "one prompt, three questions" but the template has five distinct fields.

4. **Unclear update selection mechanism (CHARTER/SKILL.md line 52)**
   - Quote: "Walk only the sections the user names plus the TBDs, presenting current content as a draft for each."
   - Unclear: How does the user "name" sections in an update? Should they say "Mission, Scope, Constraints" by name? The UI/interaction pattern is not specified.

5. **Ambiguous "kept" meaning (CHARTER/SKILL.md line 62)**
   - Quote: "Confirm you have its 'Charter established' date and the content of every section the user kept before the next step overwrites the file."
   - Unclear: Does "kept" mean sections the user chose not to modify, or sections that remain after deletions? Context suggests the former, but it is not explicit.

6. **Shell command contradicts tool constraint (CHARTER/SKILL.md line 63)**
   - Quote: "`cp` the template to `CHARTER.md`."
   - Unclear: How does a skill execute shell commands? The skill also says "use Edit for all modifications" (line 60). Should Edit be used to create the initial file, or is shell execution expected outside the tool system?

7. **Non-date derivation instruction (CHARTER/SKILL.md line 72)**
   - Quote: "New charter: established, last reviewed, and next review all derive from today and the review schedule."
   - Unclear: The "review schedule" field contains text like "quarterly" or "after major milestones", not dates. How should "next review" be derived from non-date text?

8. **Ambiguous template note (Template line 42)**
   - Quote: "[Principle — add or remove rows to match the project]"
   - Unclear: Is this a note to the skill (instruction to strip it) or placeholder text the user will see? The bracket format matches other placeholders, but the content is a meta-instruction.

---

## Summary

Round 2 identified eight issues: undefined "load" operation, conflicting draft-default between charter and gather skills, domain context structure mismatch (one prompt vs. five template fields), unclear selection mechanism for update flow, ambiguous "kept" in update context, shell command contradiction with tool workflow, non-date derivation of next review date, and mixed metadata/placeholder formatting in template. The template now defines domain context with explicit questions, and gather protocol is self-contained, but charter's integration points remain ambiguous.
