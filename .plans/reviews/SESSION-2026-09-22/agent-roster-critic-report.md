## Critic Review

**Artifact:** agent-authoring skill (SKILL.md, references/roster.md, references/platform-reference.md, templates/roster/*.md), CLAUDE.md Non-Obvious Context, .gitignore, consult-team pointer
**Date:** 2026-10-08
**Dispatch Mode:** Mode 3 (team dispatch, one-shot review task)

## Instructions Received

Review step 8b of the consolidation: roster moved to `templates/roster/` as single source, `.claude/agents/` gitignored as an installed copy, SKILL.md rebuilt with Install and Author flows. Focus: fresh-install behaviour, overwrite handling, whether `/agents` suffices, fresh-clone assumptions, the four `/agent-authoring` pointers, Praxisity-specific Checklist content, Write-not-cp and the roster-promotion offer, `category`, and the wholesale `.claude/agents/` ignore. Under 90 lines.

## Findings

### Important — Overwrite loses local customizations silently
**Location:** SKILL.md, Install step 2: "For an agent that already exists, ask whether to overwrite it; its memory ... is untouched either way."
**Problem:** The question cannot tell an untouched installed copy from one the project has edited, or from a project-authored agent that happens to share a name. Step 1 only "marks" existence.
**Impact:** A user who tuned critic.md for their project and answers "yes" loses the edits with no signal; CLAUDE.md warns this repo, not other projects.
**Fix:** In step 1, run `diff -q` between each existing file and its roster file; report "identical" or "differs locally" in the overwrite question. Offer "skip" as the default when it differs.

### Important — Every roster file violates the skill's own "define every taxonomy level" rule
**Location:** SKILL.md Writing the Body ("findings in the agent's own taxonomy with each level defined") and Principles ("define every taxonomy level, because undefined ones drift"); Author step 3 ("each defined"). Roster: critic `Critical | Important | Minor`, designer `Structural | Coupling | Minor`, stakeholder `Misses Audience | Weakened | Minor`, project-manager `Blocking | Risk | Advisory`, user-advocate `Blocking | Friction | Minor`, prompt-engineer `Ambiguity | Noise | Elephants | Drift | Clarity`: none defined.
**Impact:** Author step 2 sends a new author to a roster file "as the structural reference" that contradicts step 3's requirement; the drift the principle warns about is already live across eight agents.
**Fix:** Add a one-line definition per level in each roster file's Output Format (e.g. Critical: the artifact fails its purpose; Important: a real failure in some path; Minor: cosmetic or edge). Or drop the principle; keeping both is the contradiction.

### Important — Roster promotion only works inside the framework repo
**Location:** SKILL.md Author step 5 "Offer to add it to the roster templates as well"; roster.md "when a pattern recurs across projects, it belongs in the roster file".
**Problem:** In a plugin install, `${CLAUDE_SKILL_DIR}/templates/roster/` is the plugin cache, overwritten at update and outside the user's version control. The offer is actionable only in `~/Dev/praxisity`.
**Impact:** A user in an unrelated project accepts the offer, the file lands in the cache, and vanishes at the next plugin update; the skill reported success.
**Fix:** Condition the offer on being in the Praxisity source repo (`.claude-plugin/plugin.json` with `"name": "praxisity"` present). Elsewhere, say "note it for a contribution to the framework" and stop.

### Important — Author flow writes into a gitignored directory in this repo without warning
**Location:** SKILL.md Author step 4 "Write the file to `.claude/agents/[name].md`"; `.gitignore` line 8 ignores `.claude/agents/` wholesale. `.claude/settings.local.json` shows a prior `fresh-eyes-reviewer` lived there, so repo-local authored agents are a real case.
**Impact:** In this repo, an authored agent the user declines to promote (step 5) is unversioned, absent from a fresh clone, and has no "single source". Other projects are fine: the charter's gitignore template does not ignore `.claude/agents/`.
**Fix:** Either ignore the nine installed files by name instead of the directory, or add to Author step 4: "In the Praxisity source repo, write to `templates/roster/` and then install; `.claude/agents/` is not versioned there." The second keeps the single-source rule honest.

### Important — Default install set omits the agents the workflow skills recommend
**Location:** SKILL.md Install step 2: default "critic, prompt-engineer, user-advocate, and spot (the four used to review every skill in this framework)". describe/SKILL.md:100 recommends critic or skeptic; design/SKILL.md:106 recommends designer or skeptic.
**Impact:** A user who follows the describe pointer, installs the default, then returns to /design finds neither designer nor skeptic installed and runs the skill again. The default is tuned to reviewing skills, which non-framework projects never do.
**Fix:** Default to all nine (nine 100-line files cost nothing until dispatched), or default to what the pointers name: critic, skeptic, designer, stakeholder. Move the "four used for skills" note to roster.md, where it already lives.

### Important — Two Checklists are skill-review checklists presented as unconditional
**Location:** user-advocate Checklist lead-in "Check each before writing up"; items on brief mode, template examples per section, success messages naming skills, update flows replaying sections. critic Checklist lead-in "Run through them before writing up"; items "does the thing ... exist in the repo", "verify against the project's capabilities reference".
**Impact:** Installed into a public-health program or a course module, user-advocate is told to check twelve skill-authoring patterns against a protocol document, priming it to review every artifact as an interactive skill. critic hunts for a capabilities reference that exists only here, and assumes a repo.
**Fix:** Scope the lead-ins: "When the artifact is an interactive skill or workflow, also check:". Keep the portable items (jargon, scope statable without paths, executor may be human; optional references must resolve) unscoped. Change "the project's capabilities reference" to "any capabilities reference the project keeps; if none, mark the claim unverified". prompt-engineer and consistency-reviewer are already scoped; leave them.

### Important — "Run /agents" is asserted, not shown; my own dispatch is counter-evidence
**Location:** SKILL.md Install step 5; platform-reference Dispatch ("loaded at startup or via `/agents`"; team dispatch "scans fresh").
**Problem:** The file at `.claude/agents/critic.md` has the Checklist section; the definition I am running under is the pre-pass version (Specify → Design → Breakdown → Implement, no Checklist). Either I was spawned before the reinstall, or the fresh-scan claim does not hold for team dispatch. The `/agents` claim rests on a memory note, and no live run in this session confirms it.
**Fix:** Add this to the live-test list in PLANNING.md: reinstall, run `/agents`, dispatch standalone, confirm the Checklist is present in the agent's Instructions Received. Until then, step 5 should read "run `/agents`, or start a new session if the agent does not appear".

### Minor — Fresh project with no .gitignore leaves agent memory unignored
**Location:** Install step 4 "If `.gitignore` exists and does not exclude ...".
**Fix:** "If `.gitignore` is absent or lacks the line, offer to add it, creating the file if needed." The skill's own words say memory "may hold personal details".

### Minor — platform-reference overclaims `category`
**Location:** platform-reference line 42 "Used by Praxisity's consult-team skill for dispatch grouping". consult-team never reads it. No validation failure is in evidence: the prior installed files carried the field and dispatched.
**Fix:** "Documentation only; consult-team does not read it." Or drop the field and keep category in roster.md's table.

### Minor — Counts and stale descriptions
consult-team line 38 "all 8" vs nine. README line 50 "Create new agent definitions" omits Install; README line 54 "includes a roster" reads as bundled while plugin.json ships agentless. Fold into step 9.

### Minor — Flow selection and reference file unstated
SKILL.md never says which flow runs: add "Install when invoked bare or from another skill's pointer; Author when the user describes a new perspective." Author step 2 "read one roster file" can land on spot (17 lines, no sections); name critic.

## Unstated assumptions
- Bare `/agent-authoring` resolves in a plugin install; PLANNING.md verified `/praxisity:charter`, not the bare form. All four pointers use it, as do every other cross-skill pointer, so this is a framework-wide bet, not this pass's.
- A fresh clone of this repo starts agentless and memoryless; CLAUDE.md's Non-Obvious Context explains the copy but not "run /agent-authoring first". PLANNING.md line 40 still says reviewers "hold checklists in agent memory", which a clone lacks; the harvested Checklist sections are the actual fix and should be cited there.
- Line 8 "Both end with the agents registered" asserts an outcome only the user's `/agents` run produces.

## Ranked top 5
1. Overwrite without diff (silent data loss in other projects).
2. Taxonomy levels undefined in eight roster files, contradicting the skill's own rule.
3. Roster promotion offer and "belongs in the roster" only valid in the framework repo.
4. Author flow writes to gitignored `.claude/agents/` here with no warning.
5. Default install set contradicts the describe and design pointers.

## Strengths
The install-not-bundle rationale is stated once, correctly, and traced to a documented constraint. The Checklist harvest turns gitignored memory into versioned baseline, which is the right answer to the fresh-clone problem. Project Context is now identical across the roster and names the real workflow. Author step 4's Write-not-cp choice is correct and its reason is given. The "do not name other agents in boundaries" rule is a genuine priming fix.

## Self-Evaluation
- **What worked well:** Reading my own loaded definition against the on-disk file produced the only live evidence in the review.
- **What you struggled with:** I cannot run `/agents` or `cp`, so install-flow claims are reasoned, not executed.
- **Prompt improvement suggestions:** Add to the Checklist: "When a skill offers to write into its own `${CLAUDE_SKILL_DIR}`, ask where that resolves in a plugin install."