## Prompt Engineer Review

**Artifact:** `.claude/skills/detail/SKILL.md` and `templates/dip.template.md` (compared against design SKILL.md and gather SKILL.md)
**Date:** 2026-10-02
**Dispatch Mode:** Mode 1 (subagent consult)

## Instructions Received

Review the new /detail skill and DIP template as prompts. Specific questions: executing-agent preamble and elephants; whether "cites, does not restate" suits an agent in a fresh session; clarity of "drafted outline, then one at a time"; conflicts in the renumber-while-Ready rule; NNN/DDD/MMM at Edit time; signal-to-noise. Under 100 lines.

## Dual-Consumption Assessment

### Drift — The cite rule will bleed into step text
**Location:** SKILL.md Rules, line 21; template Implementation Steps
**Problem for AI:** "The DIP cites; it does not restate" is a global rule. The same agent then drafts steps. In draft-first mode it will produce "Implement COMP-2 per §3" and call that a step, because the rule told it not to restate the design. The executing agent in a fresh session then has a pointer, not an instruction. Citing is the right call for Required Reading, Must Satisfy, and Interfaces, where the source is a contract. It is the wrong call for the step body, which is the only place the work is actually said.
**Problem for humans:** The reviewer cannot judge a step that says "per the design."
**Suggested fix:** Scope the rule. "Required Reading, Must Satisfy, and Interfaces cite; they do not restate. Steps state the work in full: a step the executing agent cannot carry out without opening the design is not finished." Context cost of the cites themselves is two or three file reads per execution, which is cheap compared with the drift a copied spec would carry.

### Ambiguity — Acceptance Criteria restates, contradicting the rule
**Location:** template line 165; SKILL.md line 21
**Problem for AI:** The AC table copies the Given/when/then text. That is a restatement, and the agent will either strip it to a label to obey the rule, or keep it and learn the rule is soft. Both are wrong in different runs.
**Suggested fix:** Name the exception in the rule: "Acceptance criteria are copied, so the test sits beside what it tests; the update flow re-checks them against the spec."

### Ambiguity — Token with literal suffix
**Location:** SKILL.md Generate step 4; template lines 46-47, 70, 76, 129-130
**Problem for AI:** "Replace `DDD` with the design number and slug" is applied to `[DESIGN-DDD](../designs/DDD-slug.md)`, where `DDD` appears twice with different neighbours. A literal reading yields `DESIGN-004-auth-flow` as link text or `004-auth-flow-slug.md` as the path. `MMM` has the same problem, inherited from the design skill.
**Suggested fix:** "Replace `DDD` with the design's three-digit number and `DDD-slug` with the design file name; same for `MMM` and `MMM-slug`." The `NNN` token is unambiguous: it only appears as `DIP-NNN`.

### Clarity — Pacing term is clear, draft source is not
**Location:** SKILL.md Gather, Implementation Steps row
**Problem for AI:** "Drafted outline, then one at a time" composes two gather terms correctly, and the "no unrequested drafts" rule stops the agent from drafting all steps after the outline is approved. What the row does not say is where each step's draft comes from. The design supplies titles and Output; it rarely supplies artifact paths or a runnable Verify. In draft-first mode the agent will invent paths to fill the slots.
**Suggested fix:** Add to the row: "Draft the action and Output from the design; prompt for Input paths and Verify unless source material names them."

### Elephants — Checklist escape the agent can draft itself
**Location:** SKILL.md Gather, Implementation Steps and Acceptance Criteria rows; Review and Confirm
**Problem for AI:** The gate is "every step has a Verify, every MUST has a tested AC." The escape is "name human judgment as such when nothing else works." Both rows are drafted by the agent, so "Test: human review" satisfies the gate on every row and the gate never fires. Same pattern as the design skill's deliberate gap.
**Suggested fix:** A human-judgment test must name who judges and what they look at. Have the Review outline count the human-judgment tests so the user sees how much of the gate was met that way.

### Ambiguity — "the list below"
**Location:** template line 144
**Problem for AI:** "Do not change artifacts outside the list below" is followed by two lists. The nearer reading is the first, but Out of Scope is also below.
**Suggested fix:** "Do not change any artifact not listed under Artifacts in Scope."

### Clarity — Marking bullets inside Required Reading
**Location:** template lines 72-74, 83; SKILL.md Generate marking rule
**Problem for AI:** Bullets carry "or N/A" inline, but the marking rule applies to sections, and the row rule says lines may be removed. The agent may produce `- [ ] N/A`, a checkbox the executing agent is told to read before the first step.
**Suggested fix:** "Within Required Reading, remove bullets that do not apply; mark only the charter block as a whole."

### Noise — Pre-Flight step 5
**Location:** SKILL.md line 37
**Problem for both:** One paragraph carries six branches (argument given, default from PLANNING.md, ask, no element, custom DIP, existing Ready DIP). Each is clear alone; together they are the hardest lines in the skill to execute in order.
**Suggested fix:** Split into 5a to 5d by branch. No content change.

## Answers to the Specific Questions

- **Preamble:** does its job with no elephants. The four sentences name the behaviours wanted; "rather than improvise" is the only negative and it is short. One gap: it does not say who ticks the checkboxes. Add "mark each as read" or drop the boxes.
- **Renumbering while Ready:** no conflict. The reason given (nothing outside the DIP cites a step) holds, the no-revise-after-In-Progress rule keeps /do's step tracking safe, and the rule is explicitly the opposite of the design skill's ID rule, with the why stated. Only Revision History rows that name step numbers go stale, which is acceptable for history.
- **Signal-to-noise:** good for 100 lines. The Rules block repeats three items from the template header (one element, markers, cite rule). That duplication is tolerable because the header is stripped from the output, but it is the place drift will start.

## What's Well-Engineered

- The frontmatter description says what the artifact is and who executes it, so the skill picker has a real signal.
- The gather load is an explicit Skill tool call, not a reference.
- Update flow checks the design's and spec's Revision History and surfaces struck IDs, so a stale DIP is caught before the user is asked what changed.
- The success message's first next step ("read it as the agent with no memory of this conversation") is the best single test of a DIP and costs one line.
- The commit template puts the DIP ID and satisfied requirements in the message body, giving git history a traceability line for free.

## Self-Evaluation

- **What worked well:** Reading the DIP as its downstream reader, a fresh /do session, surfaced the cite-rule bleed and the escape-drafting gate, which a read as a document would miss.
- **What you struggled with:** /do does not exist, so claims about step tracking and Status handling are inferences from comments in the template.
- **Prompt improvement suggestions:** My agent prompt should say that when the artifact under review is itself a prompt for a third agent, review from that agent's seat first and the author's seat second.

## Round 2 (2026-10-02, delta pass on the revision)

**Resolved (7 of 8):**
- Cite rule bleed: the rule is now scoped to the four reference sections, and step bodies and Scope Boundaries are named as written in full. The template step comment carries the same contrast. Done.
- Token ambiguity: "`DDD` alone is the design number and `DDD-slug` is the design's filename stem" is unambiguous at Edit time. `DESIGN-DDD` and `../designs/DDD-slug.md` each resolve to one reading. One nit: "alone" could be read as "not prefixed" and `DESIGN-DDD` is prefixed. "`DDD` not followed by `-slug`" closes it, but no agent is likely to stumble here.
- Step draft source: the row now says what is drafted from the design and what is prompted, with the reason. Done.
- Gate escape: human judgment must name who looks at what, the Review outline names the judge, and the three exits are shown at the gate rather than drafted into rows. Done.
- "the list below": now "outside Artifacts in Scope". Done.
- N/A bullets in Required Reading: a block with nothing to read is one N/A line, no checkbox, stated in both files. Done.
- Pre-Flight step 5: split into 5a to 5e. Done.
- Preamble: "and tick it" settles who ticks. The ID key is two lines a human executor will use and an agent will not mind.

**Decided the other way: cite-only Acceptance Criteria.** The table now carries AC-n, the REQ it validates, and the Test. Judgment: an executor can act on this. The Test column is required to be a command, a check, or a named judgment, so it is runnable as written; the criterion text is one lookup away in a file the executor was already told to read and tick; and the Verification block below gives the whole-DIP check regardless. The drift argument is sound. Two conditions make it hold:
1. Every AC-n in the table must also appear under Required Reading, or the executor is testing against a criterion it was never told to read. The Gather row for Required Reading covers this in principle; have the Review outline confirm it.
2. A Test must not say "as the criterion states". The rule already forbids this form for steps; the AC comment says "how this piece of work demonstrates each criterion here", which is enough.

**New, minor:**
- Template line 154, "Do not change anything outside Artifacts in Scope", now contradicts the Safety Checklist's exception for the Status row and PLANNING.md. An agent obeying DO NOT literally will not update Status. Add the same exception to the DO NOT line, or let /do own that edit and say so.
- Template line 54, "Status is set by /do", while Generate step 5 has /detail set Ready. Say "/do moves Status" instead.
- Template line 226, Revision History "while the DIP is Ready", should read "Ready or Halted" to match the new rule.

No remaining issue blocks use. The skill reads consistently from the executor's seat.
