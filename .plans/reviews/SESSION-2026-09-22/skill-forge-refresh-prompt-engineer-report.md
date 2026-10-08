## Prompt Engineer Review

**Artifact:** `.claude/skills/skill-forge/SKILL.md` and `references/praxisity-patterns.md`, read as the prompt an agent holds while writing `/decide`
**Date:** 2026-10-08 · **Dispatch Mode:** Mode 2 (parallel with consistency-patterns)

## Instructions Received
Evaluate both files as prompts for the next skill author: skeleton followability without the five skills open, contradictions with current authoring guidance, noise and restatement, instructions-vs-documentation drift, one-owner-per-fact violations in the patterns file, and unverified platform claims stated as fact.

## Findings

### HIGH — Verification wording reads as "tested" (SKILL.md Frontmatter, Plugin Packaging)
"Fields verified against the Claude Code documentation" tells the agent these fields work. None of the new ones has run here, and `when_to_use` was rejected by an IDE diagnostic on 2026-04-04. The `$ARGUMENTS` line says "verify in a plugin," but it is unverified in a repo-local skill too, and the Skill-tool invocation of `gather` (skeleton Pre-Flight step 3) is unverified anywhere.
**Rewrite:** replace the table intro with "Field list taken from the documentation on 2026-09-22 (2.1.280). Tested in this repo: `${CLAUDE_SKILL_DIR}`, `disable-model-invocation` loading. Documented only: everything else, and `when_to_use` was rejected by an IDE diagnostic under an earlier version." Change the `$ARGUMENTS` sentence to "documented; not yet observed working in a skill here or in a plugin." Add "skill-to-skill invocation via the Skill tool is also untested" to the plugin test list.

### HIGH — Reasons are referenced, not stated, so the skeleton needs the five skills open (patterns Generate, Completion Gate; SKILL.md Template Bundling)
"The copy-then-edit paragraph with its reason" and "'a hard gate' with its reason" name a reason that appears in neither file. The agent writing `/decide` either opens `describe` or invents one. Same for "the closed list of permitted Edit operations": the four operations are scattered across Markers (marking), Template Conventions (row and block adjustment, comment stripping), and nowhere (placeholder substitution).
**Rewrite:** in SKILL.md Template Bundling step 2 add "because Write regenerates the file from memory and drifts: renamed headers, dropped sections, half-stripped comments, renumbered IDs." In the skeleton's Generate entry name the four: "placeholder substitution, comment stripping, marking, row and block adjustment." In Completion Gate write "a hard gate because the next session reads PLANNING.md before anything else."

### MEDIUM — Patterns file is a second or third owner of three shared facts (patterns §Gather Terms, §Reference Conventions, §Status Lifecycle of a DIP)
Gather Terms restates gather's four definitions in different words ("Drafted by you" vs gather's "Drafted") and imports a describe-only rule (empty sub-table is N/A). Reference Conventions reformats the template header block into a table, a third format of a block that drifted across three templates the day it was adopted; anyone copying from the table instead of a template produces a fourth variant. The DIP status lifecycle is `/detail` and `/do` internals that only matter when editing those two skills, which the editor will have open.
**Rewrite:** Gather Terms becomes two lines: "The Pacing column uses gather's four terms verbatim, read from gather's The Rule section; compounds are allowed, each part following its own term." Reference Conventions keeps the prose intro and the cite rule, drops the table, and says "copy the block verbatim from an existing template header." DIP lifecycle becomes one line: "DIP Status strings are owned by `/detail` (Ready) and `/do` (all others); trace every string when touching either."

### MEDIUM — Praxisity-specific review ritual lives in the general skill and is restated in the reference (SKILL.md Testing step 1; patterns §Agent Consultation)
Both name the same four agents, Mode 2, two rounds. "Mode 2" is consult-team vocabulary that a non-Praxisity project loading skill-forge will not have. The patterns section also opens with the elephant "do not carry an Agent Consultation section; it was unreachable."
**Rewrite:** SKILL.md step 1: "Review before testing: dispatch reviewers in parallel (see consult-team if installed); a Praxisity reference names which." Patterns: open with "Consultation lives in the success message's next steps" and keep the reviewer list there only.

### LOW — Residual restatement and anchors
- SKILL.md line 26 restates the three loading levels just listed. Cut.
- Patterns §Two Skill Types re-explains `disable-model-invocation` and `context: fork`, both already in the SKILL.md table that is always loaded alongside. Keep only the two phase shapes and the support-skill list.
- Skeleton Frontmatter's support-skill parenthetical is noise inside a workflow-skill skeleton, and "one sentence" is contradicted by describe's two-sentence description. Cut both.
- "Five to seven bullets" is an item-count anchor CLAUDE.md warns against. Write "one bullet per rule, each with its reason."
- SKILL.md Before You Start step 3, "a skill for the Praxisity framework," is ambiguous outside this repo: a skill shipped in Praxisity, or any skill in a project that uses it? Say "a skill that will ship in the Praxisity plugin or follow its workflow conventions (template, PLANNING.md contract)."
- The maintainer HTML comment the skeleton propagates addresses the maintainer but loads into every run of every skill. A YAML `#` comment in frontmatter would not load into the body (unverified that the parser keeps the file valid; test once).
- Naming's history of "plan" and "define" is documentation. Reduce to the check it implies: "test the verb against Claude Code's own mode and command names and against the field's stage vocabulary."

## What's Well-Engineered
"One owner per fact" and "trace every state string" are stated with their failure modes, which is what makes them actionable. The patterns file's opening rule (the skill is newer, fix this file) handles its own drift. Pre-Flight's "every branch that stops sets Status to cancelled" and the PLANNING.md contract's "nothing survives the next skill's step 2" close two gaps the review series found. The closing `/decide` section correctly disables the parent and gate rules instead of leaving the author to infer it. SKILL.md's body is still instructions; only Plugin Packaging reads as documentation, and its final sentence turns it back into a test list.

## Self-Evaluation
Reading the patterns file as the `/decide` author surfaced the missing-reason gaps that a skill-by-skill reading would not. Blind spot: I did not open `/do` or `/detail` to confirm the DIP lifecycle paragraph is accurate; I judged only whether it belongs here. Prompt improvement: my persona should say to read a reference file from the seat of the author who will clone from it, not from the seat of the reviewer who already knows the originals.