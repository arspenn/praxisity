## Meta-Review: /charter Skill First Live Run

**Date:** 2026-04-04
**Artifact:** /charter skill (SKILL.md + template)
**Purpose:** What did we learn about the skill as a process, not the charter as output? What patterns carry forward to /describe, /design, /plan, /do?

---

## What Worked

### 1. Pre-Flight sequential execution held
Steps ran in order. PLANNING.md was updated as step 2 before anything else. The explicit "do not begin step N+1 until step N completes" language appears to work. **Carry forward:** Use identical REQ-F2 language in all skills.

### 2. One-at-a-time gathering worked conversationally
We went section by section with pauses. The user had control over each section, could approve/edit/skip. Sub-categories (constraints, stakeholders, domain context) were prompted individually. **BUT:** see "What Didn't Work #4" — we don't know if /gather auto-invoked or if the lead agent just followed the skill's inline instructions.

### 3. Template copy-then-edit was clean
`cp` from `${CLAUDE_SKILL_DIR}/templates/` to destination, Edit operations applied. Template verified unchanged after generation. The permitted operations list worked — placeholders substituted, domain sections removed, comments stripped, content populated.

### 4. `${CLAUDE_SKILL_DIR}` resolved correctly
The platform expanded it to the full path in the loaded skill content. **VERIFIED.** Carry forward to all skills.

### 5. Completion Gate worked
PLANNING.md was updated before the success message displayed. The structural separation (Post-Save → Completion Gate → Success Message) enforced the ordering.

### 6. Review-and-update flow was natural
Presenting current content as drafts for each section worked well for the update use case. The user could approve sections that were fine and focus time on sections that needed changes.

---

## What Didn't Work / Needed Mid-Run Fixes

### 1. Glossary section missing from template
The charter output used project-specific terms (lethal trifecta, DIP, dispatch modes, etc.) that an AI reading it as governance wouldn't understand. We had to add a Glossary section mid-process. **Root cause:** The template didn't have a glossary section. **Fix applied:** Glossary added to template with dual-use HTML comment guidance. **Carry forward:** Consider whether OTHER templates (spec, design, DIP) need glossary sections too. The dual-use principle applies to all output documents, not just charters.

### 2. Principles count was too rigid
Template said "3-5" but we wrote 7. The skill echoed "3-5." **Root cause:** Template example counts anchor behavior (ISSUE-001 — this is the exact problem we identified). **Fix applied:** Changed to "the number should match what the project needs." **Carry forward:** Audit ALL template comments for fixed counts or ranges that could anchor output.

### 3. Date handling didn't distinguish new vs update
Skill said "Charter established = today" — but on an update, the established date should be preserved. **Root cause:** Skill was written for the new-charter flow; update flow was an afterthought. **Fix applied:** Date handling now branches on new vs update. **Carry forward:** Every skill that produces dated output needs explicit new vs update date handling.

### 4. /gather auto-invocation not tested
We don't know if the /gather skill auto-invoked during the charter gathering phase. The gathering protocol was followed, but that could be because: (a) /gather loaded automatically, or (b) the charter skill's inline "follow the gathering protocol (see /gather)" instruction was sufficient, or (c) the lead agent already knew the protocol from this session's context. **QG-2 remains open.** **Carry forward:** Need a clean test — run /charter in a fresh session where the agent has NOT been discussing the gathering protocol. If it still gathers one-at-a-time, /gather auto-invocation works. If it batches, we need explicit fallback references.

### 5. Review-and-update flow was underspecified
The skill said "offer (r)eview and update, (s)tart fresh, or (c)ancel" but didn't describe what the review-and-update flow LOOKS like — do you read the existing charter and present each section's current content as a draft? That's what happened, and it worked well, but the skill didn't instruct it. **Fix applied:** Step 3 now explicitly says "read it and walk through each section showing current content as drafts." **Carry forward:** All skills with an update mode need explicit update-flow instructions, not just "offer update."

### 6. Terms in governance documents need definitions
The charter referenced "lethal trifecta," "9-agent roster," "Mode 1/2/3," "DIP," "SPEC-004" without definitions. The spot reviewer flagged these as governance failures — an AI reading the charter can't act on terms it doesn't understand. **Fix applied:** Glossary section. Definitions are conceptual, not implementation-anchored. **Carry forward:** This is a dual-use principle enforcement issue. Any output document that will be loaded as AI context must define its terms or link to definitions. This applies to specs, designs, and potentially DIPs.

---

## Patterns for Other Skills

### Pattern 1: Live testing reveals what reviews don't
Three separate agent reviews (consistency-reviewer, prompt-engineer, spot) didn't catch the missing glossary, the date handling issue, or the underspecified update flow. Running the skill live did. **Implication:** Each skill must be live-tested before it's considered validated. Reviews are necessary but not sufficient.

### Pattern 2: Template updates propagate to two places (until sunset)
During migration, templates exist in both `.praxisity/templates/` and `.claude/skills/[name]/templates/`. Changes must be applied to both. This is a maintenance burden that goes away as templates are sunset. **Implication:** Sunset `.praxisity/` copies as soon as each skill is validated, not all at once.

### Pattern 3: The update flow is as important as the new-creation flow
The first run of /charter was an update, not a creation. The skill was designed primarily for creation. **Implication:** Every skill should be designed for both new and update flows from the start. The update flow presents existing content as drafts; the new flow prompts from scratch.

### Pattern 4: Governance documents must be self-contained
The dual-use principle means any document that will be loaded as AI context needs to define all its terms. This isn't just a charter concern — it applies to any document that CLAUDE.md, PLANNING.md, or skills point to as a reference. **Implication:** Consider glossary sections in specs and designs that introduce project-specific terminology.

### Pattern 5: Don't anchor to implementation evidence in output
We caught ourselves referencing "v0.5.0 bug report" and specific bug IDs in the charter glossary. The user corrected this — definitions should be conceptual. **Implication:** All skill gathering flows should guide the user toward conceptual descriptions, not implementation anchors. The evidence lives in specs and bug reports; governance documents state principles.

### Pattern 6: Memory-as-settings was not tested
REQ-G8/G9 (gather preferences) was not exercised during this run. The /gather skill's calibration flow didn't fire — either because /gather didn't auto-invoke, or because the session context made calibration unnecessary. **Implication:** Need a fresh-project test where no gather preferences exist in memory.

---

## Open Items from This Run

| Item | Status | Next Step |
|------|--------|-----------|
| QG-2: /gather auto-invocation | Still open | Test in fresh session |
| Memory-as-settings calibration | Not tested | Test in fresh project |
| Glossary in other templates | Not yet assessed | Audit spec, design, DIP templates during their skill builds |
| Template count anchoring | Charter fixed | Audit other templates for fixed-count guidance |
| `.praxisity/templates/charter.template.md` sunset | Ready | Delete after this session's commits are stable |