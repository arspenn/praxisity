## Command Rewrite Pipeline Plan

**Author:** project-manager
**Date:** 2026-04-03
**Revised:** 2026-04-03 (bootstrap pivot + /new-project dropped)
**Depends on:** Sequencing analysis (Task #3/6), Q-3 resolution, Q-4 resolution

## Bootstrap Pivot

**Original plan:** `/charter` first as pattern-setter, then linear pipeline through the remaining 5.

**Revised plan:** `/describe` (renamed `/spec`) first. Once built, use `/describe` itself to write specs for the remaining skills. This follows the bootstrapping principle — use the system to build the system.

**Scope reduction:** `/new-project` dropped from SPEC-004. It's a sunset candidate — the framework will eventually be distributed as a plugin, making the repo-scaffolding command unnecessary. Its 9 bugs (BUG-001 through BUG-009) are deferred as "sunset pending distribution model decision." This also avoids a name collision with Claude Code's built-in `/init`.

**Final scope: 5 skills** — describe, charter, design, plan, do.

This changes the pipeline fundamentally:
- `/describe` is both the pattern-setter AND the tool for specifying subsequent skills
- The remaining 4 skills go through the full Praxisity workflow (specify via `/describe` -> design -> build)
- Verification of `/describe` is higher-stakes: if it doesn't work well, the whole pipeline degrades
- The "design doc covering all 6" model is replaced by per-skill specs written through the framework
- All 5 skills share the workflow structure — no structural outlier

## Pipeline Model

### Phase 1: Bootstrap `/describe` (team designs + builds directly)

This is the only skill that gets designed and built without the framework's own workflow, because the workflow doesn't exist yet.

**Design** (team activity, ~45-60 min)
- Team reviews: prototype `/spec` command + its 6 bugs + behavioral standards + skills format (Q-3) + delivery mechanism (Q-4)
- Produces: full design for the `/describe` skill
- Higher time estimate than other skills because this sets the pattern

**Build** (lead + user, ~30-60 min)
- Lead writes the actual skill file based on the design
- Team reviews the draft

**Verify** (team activity, ~20 min)
- All 6 assigned bugs addressed (BUG-017, 018, 019, 020, 021, 022)
- All REQ-F1 through F5 standards applied
- Skill file is valid for `.claude/skills/` format

### Phase 2: Bootstrap test — use `/describe` to specify the next skill

Run `/describe` to write the spec for `/charter` (or whichever is next). This is the real verification — does the rewritten skill actually work? Does it exhibit any of the old bug patterns?

If this works: the bootstrap is proven, and the remaining skills follow the same pattern.
If this fails: we fix `/describe` before proceeding. Better to find out on skill #2 than skill #6.

### Phase 3: Remaining 4 skills — specify via `/describe`, then design + build

Each remaining skill follows the Praxisity workflow:
1. `/describe` writes the skill's spec
2. Team designs the skill (informed by the spec + prototype + bugs)
3. Lead builds the skill
4. Team verifies

## Revised Pipeline Schedule

```
Session 1 (current): Design infrastructure + /describe design
  [DONE] Q-3: skills format
  [DONE] Q-4: minimal hybrid (inline mechanical + shared F3)
  [DONE] Sequencing analysis
  [IN PROGRESS] Design document — /describe section

Session 2: /describe build + bootstrap test
  Build   /describe ████████░░░░░░░░░░░░
  Verify  /describe ░░░░░░░░████░░░░░░░░
  Bootstrap test    ░░░░░░░░░░░░████████  <- run /describe to spec /charter

Session 3: /charter design + build, /design design start
  Design  /charter  ████████░░░░░░░░░░░░  <- informed by spec from bootstrap test
  Build   /charter  ░░░░░░░░████████░░░░
  Verify  /charter  ░░░░░░░░░░░░░░░░████
  /describe /design ░░░░░░░░████░░░░░░░░  <- run /describe to spec /design skill

Session 4: /design + /plan
  Design  /design   ████████░░░░░░░░░░░░
  Build   /design   ░░░░░░░░████████░░░░
  Verify  /design   ░░░░░░░░░░░░░░░░████
  Design  /plan     ░░░░░░░░████████░░░░  <- overlaps with /design build
  (spec for /plan written via /describe during gap)

Session 5: /plan build + /do
  Build   /plan     ████████░░░░░░░░░░░░
  Verify  /plan     ░░░░░░░░████░░░░░░░░
  Design  /do       ░░░░████████░░░░░░░░
  Build   /do       ░░░░░░░░░░░░████████
  Verify  /do       ░░░░░░░░░░░░░░░░████
```

Skill names: describe, charter, design, plan, do.

### Why this is better than the original pipeline

1. **Validates the tool with the tool.** If `/describe` can successfully spec the remaining skills, the rewrite worked.
2. **Each subsequent skill gets a proper spec.** Instead of one team-designed design doc section, each skill has a framework-generated specification with requirements, acceptance criteria, etc.
3. **Catches problems earlier.** The bootstrap test (Session 2) is an explicit go/no-go gate.
4. **5 sessions for 5 skills.** The extra `/describe` runs add ~15-20 min each but replace team design time, so the overall timeline is similar.
5. **No structural outlier.** All 5 skills share the workflow pattern. `/new-project` was the odd one out — dropping it makes every rewrite reinforce the same patterns.

### Risk: the bootstrap adds a dependency

In the original pipeline, all 6 command designs were independent — a bug in `/charter`'s design didn't block `/architect`'s design. In the bootstrap model, every skill after `/describe` depends on `/describe` working correctly. If `/describe` has a subtle issue that only shows up on the 3rd spec, we're reworking late.

**Mitigation:** The bootstrap test in Session 2 is the gate. Run `/describe` on a real skill (not a toy example) and have the team verify the output meets spec quality standards before proceeding.

## Revised Sequencing

1. **`/describe`** (pattern-setter, bootstrap tool) — 6 bugs, pure gathering flow
2. **`/charter`** — first bootstrap target, 7 bugs, simple gathering
3. **`/design`** (renamed `/architect`) — 5 bugs, most complex gathering (domain-aware)
4. **`/plan`** (renamed `/define`) — 5 bugs, has batch-mode question (BUG-029)
5. **`/do`** (renamed `/build`) — 7 bugs, unique execution m
**Dropped:** `/new-project` — 9 bugs deferred as "sunset pending distribution model decision"

Gathering-focused skills first, execution skill last. `/describe` leads because it's the bootstrapping tool.

### Handoff Points

| From | To | Artifact | Gate |
|------|-----|----------|------|
| /describe Design | /describe Build | Approved design | Team consensus |
| /describe Build | Bootstrap Test | Completed skill file | All 6 bugs addressed, standards applied |
| Bootstrap Test | /charter Design | Spec for /charter written by /describe | Spec quality verified by team |
| Each /describe run | Next skill Design | Spec for that skill | Team spot-check |
| Each skill Design | Build | Team-approved design | Team consensus |
| Each skill Build | Verify | Draft skill file | Lead confirms |

## Team Loading

| Phase | Lead | Designer | Prompt-Eng | Critic | Consistency | PM |
|-------|------|----------|------------|--------|-------------|-----|
| Design | Coordinates | Structure | Language | Stress-test | Cross-refs | Scope |
| Build | Writes file | Reviews | Reviews | Reviews | Reviews | Watches scope |
| Verify | Signs off | - | - | Spot-check | Leads verify | Bug checklist |

**Bottleneck risk:** The lead is the bottleneck during Build phases. The team is idle during Build except for review. This is unavoidable with a single implementer — the pipelining helps by keeping the team busy on the next Design while Build runs.

**Mitigation:** During Build, teammates can:
- Designer: pre-read the next command's prototype and bugs
- Prompt-engineer: draft language patterns for the next command's tricky sections
- Critic: review the just-completed design for anything missed
- Consistency-reviewer: update cross-reference tracking
- PM: update the pipeline status and flag any scope drift

## Scope Guardrails

Per skill, the team should check:
1. **Only assigned bugs are addressed.** No "while we're here" fixes.
2. **Standards are applied as designed in Q-4.** No per-skill variations unless justified.
3. **No new features are added.** A rewrite means the same capabilities, better behavior.
4. **Todoist references remain optional.** Don't deepen the dependency.
5. **`/new-project` is out of scope.** Sunset candidate — do not redesign, reference, or depend on it.

If a teammate proposes something outside these guardrails, I'll flag it. The user can override, but the default is "not in this spec."

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| /describe bootstrap test fails | Low | High (rework) | Session 2 gate catches this early; fix before proceeding |
| Scope creep during /design rewrite (most complex) | Medium | Medium | PM actively monitors; /design has 5 command-specific bugs, none are design questions |
| BUG-029 (/plan batch mode) stalls /plan design | Medium | Low | Make a quick decision: enforce one-per-run for now, batch mode is a future enhancement |
| Sessions run long due to Mode 3 review cycles | Medium | Low | Set session time budgets; if a skill takes >2 hours, pause and resume next session |
| Q-5 (agent prompt revision) gets pulled into scope | Low | High (doubles work) | Keep Q-5 as a separate follow-up task, not part of any skill rewrite |
| /new-project sunset re-enters scope | Low | Medium | Firm boundary — distribution model decision is a separate spec |