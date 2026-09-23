## Critic Review: /charter skill

**Artifact:** `.claude/skills/charter/SKILL.md`, `templates/charter.template.md`, `.claude/skills/gather/SKILL.md`, live output `CHARTER.md`
**Date:** 2026-09-22 | **Dispatch Mode:** Mode 1 (team-lead consult) | **Reviewer:** critic

## Instructions Received

Review the /charter skill before it is cloned as the pattern for /describe, /design, /plan, /do and packaged as a plugin. Find logical gaps, contradictions with the template and /gather, cloning and plugin fragility, and decide whether the fixed domain list must be generalized now.

## Findings

### High — PLANNING.md and CLAUDE.md contracts are assumed, never defined
**Location:** Pre-Flight 1, 2, 4; Section 7; Post-Save 1; Completion Gate.
**Problem:** Step 1 says "Create if missing" with no format. Step 2 sets "active skill" and Completion Gate sets "active artifact", fields the real PLANNING.md does not have (it uses "Last Command"). Step 4 and Section 7 read "project type" from CLAUDE.md, which only Praxisity's CLAUDE.md carries. Post-Save 1 edits CLAUDE.md, a file that governs every future session, without asking and without saying where.
**Impact:** In a fresh plugin install, step 1 invents a PLANNING.md schema, and five cloned skills will each invent a slightly different one. CLAUDE.md may not exist; if it does, the skill silently rewrites it.
**Fix:** Define the minimal PLANNING.md fields once (a bundled `planning.template.md` or a short shared reference every workflow skill cites). Make CLAUDE.md optional: "if present, use as defaults; otherwise ask." Change Post-Save 1 to "offer to add the mission to CLAUDE.md."

### High — Update flow destroys state it later tries to preserve
**Location:** Generate step 1 (`cp ... CHARTER.md`) vs step 4 ("Preserve the original 'Charter established' date").
**Problem:** In update mode the cp overwrites the existing charter before the established date is recorded anywhere. It survives only if the agent happens to remember step 3's read. Skip is also undefined in update mode: /gather says skip means "accept and move on," Generate says skipped means "N/A — [reason]." A user who says "skip, that's fine" about an existing section could have it overwritten with N/A.
**Impact:** Silent data loss on the flow the meta-review (2026-04-04) said is the more common one.
**Fix:** In update mode, record the established date and existing section content before cp. Define skip explicitly: new charter → "N/A — not provided" unless the user gives a reason; update → keep existing content unchanged.

### High — Three places override /gather's draft-for-approval rule without saying so
**Location:** Pre-Flight 3 "(r)eview ... showing current content as drafts"; Section 1 "present it as a draft for approval"; Section 9 "Present a draft glossary table." Versus /gather Preferences: `guided` → "always prompt from scratch, even when context is available."
**Problem:** /gather makes drafting conditional on the `gathering-style` memory. The charter skill drafts unconditionally in three spots. Nobody owns the decision.
**Impact:** A `guided` user gets drafts anyway, or the agent picks one rule at random per run, breaking the "consistent output across runs" quality indicator.
**Fix:** /gather owns the rule. Have it distinguish "show existing content" (always, for update flows and derived sections like Glossary) from "generate new content" (preference-gated). Charter then says only "existing CHARTER.md and CLAUDE.md content count as loaded documents for /gather's drafting rule."

### High — Cancel paths leave PLANNING.md marked "in progress"
**Location:** Pre-Flight 2 (write) precedes Pre-Flight 3 (c)ancel; Review and Confirm also offers (c)ancel.
**Problem:** No cancel path resets PLANNING.md. The skill's own ordering rule forces the write before the user can decline.
**Impact:** Next session opens with a phantom in-progress /charter. Cloned five times, this becomes a recurring stale-state bug.
**Fix:** Either move the CHARTER.md-exists check before the PLANNING.md write, or add one line: "On cancel, restore PLANNING.md to its pre-flight state."

### Medium — "Domain section removal" contradicts "never remove a section"
**Location:** Generate 3, second and fourth bullets; template Domain Context comment.
**Problem:** The two operations are reconcilable only if "section" means H2 and domain blocks are H3, which nothing says. The live CHARTER.md also removed the surviving "### For Software Projects:" heading, an operation not on the permitted list, so the list is already not being followed literally. Section 7 assumes one project type; the template comment says "remove sections that don't apply" (plural survivors possible). A dissertation with a software artifact, or Praxisity itself, spans two.
**Impact:** Ambiguity now, and this is the exact operation that will be copied into spec and design templates.
**Fix:** See next finding; generalizing the domain block removes the removal operation entirely.

### Medium — Fixed domain list is duplicated in skill and template; generalize now, not later
**Location:** SKILL.md Section 7 (four hard-coded lists); template lines 181–244.
**Problem:** Adding an ISD domain means editing two files plus the removal logic. PLANNING.md's scratch pad already says "keep domain sections generic during the rebuild."
**Impact:** Deferring means cloning the hard-coded pattern into four more skills first, then fixing five.
**Fix:** Replace the four H3 blocks with one generic Domain Context block (Domain, Guiding frameworks or standards, Methods or approach, Quality or evaluation approach, Key context). Move the per-domain field prompts into the section's HTML comment as guidance the agent reads when it detects the domain. Adding ISD becomes one comment paragraph, multi-domain projects just work, and the removal operation disappears. Alternative if the per-domain structure must stay literal: `templates/domains/*.md` fragments inserted by Edit.

### Medium — SKILL.md duplicates the template's structure (two sources of truth)
**Location:** Charter Flow sections 2–8 restate every heading and sub-category the template already defines; the lists disagree (template comment lists Budget, Organizational, Domain as constraint categories; skill lists Timeline, Resources, Technical, Regulatory, Other).
**Problem:** Pre-Flight 5 already says "the HTML comments are your guide for what to gather." The 40-line restatement is drift waiting to happen, and anyone cloning this for /describe will restate the spec template too.
**Impact:** Every template edit needs a mirrored skill edit, times five.
**Fix:** Replace sections 2–8 with "gather in template order; the template comment defines each section." Keep only the charter-specific rules: Mission is required, Glossary is derived last from gathered content, domain detection. This also matches current model guidance toward lean prompts with rationale.

### Medium — "Task management service" does not exist
**Location:** Post-Save 2.
**Problem:** ADR-003 (2025-12-18) chose Todoist MCP; CHARTER.md Out of Scope now says task management integration is future work. Nothing in the repo implements it.
**Impact:** In a plugin install, "if available" sends the agent hunting through MCP servers. Dead instruction contradicting the charter.
**Fix:** Delete the line. If a reminder is wanted, put "next review: <date>" in PLANNING.md next steps.

### Medium — `${CLAUDE_SKILL_DIR}` is unverified inside plugins, and appears three times
**Location:** Pre-Flight 5, Generate 1, Generate 5.
**Problem:** Verified 2026-04-04 for a repo-local skill only. If it fails to resolve in a plugin, the skill halts at step 5 after PLANNING.md was already dirtied (see cancel finding).
**Fix:** Verify during work-plan step 8 before cloning. State the template path once ("Template: `${CLAUDE_SKILL_DIR}/templates/charter.template.md`") and refer to it, so a switch to `${CLAUDE_PLUGIN_ROOT}` is one edit per skill.

### Low — Git commit is "optional" without saying who decides
**Location:** Post-Save 3. CHARTER principle 5 says git safety controls prevent accidental commits.
**Fix:** "Offer to commit; never commit without an explicit yes. Skip if the project is not a git repo."

### Low — Agent Consultation block is unreachable and plugin-fragile
**Location:** Final section. Not referenced by any flow step; `subagent_type: "stakeholder"` may be namespaced `plugin:stakeholder` after packaging.
**Fix:** Fold into the success message next steps or drop; do not clone it.

### Low — Frontmatter note for cloning
This skill is interactive and must not use `context: fork` (a forked context cannot converse with the user). State this in the skill-forge pattern so it is not applied by default to the clones.

## Unstated Assumptions

- Working directory is the project root; CHARTER.md, PLANNING.md, CLAUDE.md live there.
- Bash is available for `cp`, and the "byte-for-byte unchanged" check has some unspecified mechanism.
- Exactly one project domain; the domain is detectable from a "Type:" line in CLAUDE.md.
- /gather auto-invokes from its description and its calibration questions fire somewhere in the flow (the skill never says when; meta-review QG-2 still open).
- The gather-preferences memory format (`type:` at top level) matches the platform's format (`metadata: type:`). The existing file uses the former.
- The user is the sole approver; the Amendment Process gathered in Section 8 is never enforced by the skill.
- "The dual-use design principle" (Section 9) is understood outside Praxisity. The template comment defines it, so this holds, but the phrasing reads as a universal.
- A git repository exists.

## Top 5, Ranked

1. **Define the PLANNING.md and CLAUDE.md contract once** before cloning; make CLAUDE.md optional and never auto-edited.
2. **Fix the update flow**: capture existing state before cp, define skip per mode, add a cancel reset.
3. **Give /gather sole ownership of draft-vs-prompt**, with an "existing content is always shown" rule.
4. **Generalize Domain Context now**: one generic block, per-domain prompts in the comment, removal operation deleted.
5. **Collapse SKILL.md sections 2–8** to "follow the template" plus charter-specific rules; delete the task-management line.

## Strengths

Sequential pre-flight, copy-then-edit with template verification, the completion gate ordering, and the new-vs-update date branching all held in the live run and are worth keeping as the pattern. The template's example guidance is concrete and domain-varied, and the glossary section correctly enforces self-containment.

## Self-Evaluation

- **What worked well:** Reading the live CHARTER.md against the permitted-operations list exposed a real deviation (heading removal) that reading the skill alone would not have.
- **What you struggled with:** I cannot test plugin path resolution or /gather auto-invocation; those findings are risk flags, not confirmed failures.
- **Prompt improvement suggestions:** My persona should tell me to read the artifact's most recent live output alongside the artifact when reviewing a process; that comparison was the highest-yield step here.

---

## Round 2 — 2026-09-22 (delta pass on the rewrite)

### Resolved
- **PLANNING.md / CLAUDE.md contract:** step 1 defines the minimal schema; CLAUDE.md is optional in pre-flight 5 and offer-only in Post-Save 1. One loose end: Completion Gate says "CHARTER.md listed as an artifact" but the step-1 schema has no artifacts field. Put it under Next Steps or add the field.
- **Cancel paths:** both set Status `cancelled` and stop; the pre-flight rationale now explains why step 2 writes first. Resolved.
- **Drafting and skip ownership:** gather step 2 separates "existing or derived content, always drafted" from "new content, preference-gated"; skip has two markers and an explicit update-mode meaning in both files. Charter's Mission row ("Draft from CLAUDE.md or source material") should add "per gather's drafting rule" so a `guided` user is not drafted at anyway. Otherwise resolved.
- **Domain Context, skill/template duplication, task-management line, single template path, git offer-only, agent block, `context: fork`:** all resolved as recommended. The ISD prompts are in the template comment.

### Partly resolved
- **Update-flow state across the cp.** Generate step 1 asks the agent to "confirm you have" the established date and kept content. That is a memory check, not a safeguard: a long gather plus context compaction can drop it. **Fix:** "Immediately before the cp, re-read CHARTER.md" costs one Read and removes the dependence on recall.

### New gaps introduced by the rewrite
- **Medium — Template drift breaks "keep existing content unchanged."** The rewrite changed the template's shape (Domain Context is now four generic fields; the old charter has Tech Stack, Architecture Approach, Quality Standards). In update mode the skill walks only named sections and TBDs, and skip keeps content "unchanged," but an unchanged old-shape section cannot be substituted into the new placeholders. The very next run, updating Praxisity's own charter in work-plan step 9, hits this. **Fix:** in update mode, any section whose template structure differs from the existing charter is walked regardless, with the old content shown as a draft mapped into the new fields.
- **Medium — "Claude reads it every session via CLAUDE.md" over-claims.** The skill description, intro, and success message all assert this, but Post-Save 1 only offers a pointer line, and a pointer is not a load. If the user declines the offer, the claim is false outright. **Fix:** offer the `@CHARTER.md` import line instead (CLAUDE.md imports are documented; verify and record in the platform reference), and condition the success-message claim on the user having accepted.
- **Low-Medium — Pre-flight 3 "Load the gather skill" names no mechanism.** Invoking a skill from inside a skill in the main conversation is not in the verified-capabilities table. Test it during work-plan step 8; if it does not work, the fallback is the description-based auto-invocation that QG-2 never confirmed.
- **Low — Start-fresh dates undefined.** Option (s) is neither "new" nor "update" for Generate step 5. State whether the established date is preserved.
- **Low — Project name has no home.** Pre-flight 5 gathers it when CLAUDE.md is absent, but the template has no field for it; it only feeds the optional CLAUDE.md creation. Either add `# [Project Name] — Charter` to the template or gather it only when the CLAUDE.md offer is accepted.
- **Low — Glossary not re-derived in update mode.** Changed sections can introduce new terms; the update flow never revisits the glossary unless the user names it. Add "always re-derive the glossary" to the update flow.
- **Low — Next review "derives from the review schedule"** fails for event-based schedules like "after each milestone." Allow a triggering event in place of a date, as the live charter already does.

### Round 2 verdict
The four high findings are closed or reduced to a one-line fix. The two medium items above (template-drift in update mode, the CLAUDE.md load claim) are the ones to settle before this becomes the clone pattern, because both would be copied verbatim into /describe, /design, and /plan.
