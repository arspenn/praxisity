## Project Manager Review

**Artifact:** SPEC-004 — Command Rewrites: Sequencing and Dependency Analysis
**Date:** 2026-04-03
**Dispatch Mode:** Mode 3: collaborative team

## Instructions Received

Sustained teammate role through design and build. Starting task: read the spec and previous review, then produce sequencing analysis — which command first, dependency order, what can be parallelized. Guard against scope creep.

## Feasibility Assessment

### Updated Estimate

My SESSION-4-1-26 estimate of 4-7 hours was based on "targeted edits." The scope has since shifted to **full rewrites with Mode 3 agent teams**. This is substantially more work per command. Updated estimate:

- **Design phase** (this session): 2-4 hours for all 6 commands
  - Research Q-3 (command vs skill format) and Q-4 (standards delivery) feed into every rewrite
  - Each command needs a design review, not just a copy-paste of behavioral rules
- **Build phase**: 1-2 hours per command rewrite x 6 = 6-12 hours across multiple sessions
  - Each rewrite is a Mode 3 team session with review cycles
  - Not all of this is contiguous — the user can do 1-2 commands per session

**Total realistic estimate: 8-16 hours across 3-6 sessions.**

This is a significant commitment for a solo developer. The good news: the commands are small (60-102 lines each) and the patterns are well-understood. The risk is scope creep during each rewrite, not the base work.

### [Impact: Blocking] — Q-3 and Q-4 must resolve before any rewrite begins

**What's planned:** 6 full command rewrites using codified behavioral standards.
**Concern:** The team cannot start any rewrite until we know (1) whether the output is a command or a skill, and (2) how behavioral standards reach each command. These are Tasks #1 and #2 on the board. Every other design decision depends on them.
**Suggested adjustment:** These are correctly sequenced as the first design tasks. No change needed — just flagging that nothing else should start until these land.

### [Impact: Risk] — /new-project is structurally different from the other 5

**What's planned:** Rewrite all 6 commands using the same behavioral standards.
**Concern:** `/new-project` is a destructive setup command (removes files, resets git history, generates multiple files). The other 5 follow the Specify->Design->Build workflow and share a common structure: Pre-Flight -> Gather -> Generate -> Post-Save -> Success. `/new-project` has Parameter Gathering -> Execution (7 steps) -> Success. The behavioral standards (REQ-F1 through F5) don't all apply cleanly:
  - REQ-F1 (copy-then-edit): applies to Steps 2-5 (file generation)
  - REQ-F2 (pre-flight ordering): partially applies — it has a pre-flight but not the standard PLANNING.md integration
  - REQ-F3 (one-at-a-time gathering): applies to parameter gathering
  - REQ-F4 (success messages): applies
  - REQ-F5 (PLANNING.md gating): needs to be added

The 9 bugs for `/new-project` are mostly cleanup-list items (BUG-001 through BUG-006), not behavioral pattern fixes. This command's rewrite is more about completeness than behavioral correction.
**Suggested adjustment:** Sequence `/new-project` last or second-to-last. It's the least similar to the others and won't benefit from patterns established in earlier rewrites. Doing it early would distort the pattern-setting work.

### [Impact: Advisory] — /charter and /spec are the pattern-setters

**What's planned:** All 6 rewrites.
**Concern:** `/charter` and `/spec` are the purest examples of the Pre-Flight -> Gather -> Generate -> Success flow. They have the most gathering-related bugs (7 each, with REQ-F2/F3/F4 hits). Whichever gets rewritten first becomes the de facto template for the rest.
**Suggested adjustment:** `/charter` should be the first rewrite. It's the simplest gathering flow (8 sections, no traceability IDs), has the clearest bug-to-fix mapping, and its output (CHARTER.md) is referenced by `/spec`. Getting `/charter` right first means the pattern is proven before tackling the more complex commands.

### [Impact: Advisory] — /build has the most unique behavior

**What's planned:** Rewrite `/build` with same standards.
**Concern:** `/build` is the execution engine — it reads and runs DIPs. Its gathering phase is fundamentally different (it gathers from a DIP file, not from the user). REQ-F3 applies differently here (step-by-step execution, not user prompting). It also has unique features: resume from halt, git safety, TodoWrite integration, acceptance criteria verification. The 5 bugs are about execution discipline, not gathering.
**Suggested adjustment:** Sequence `/build` late (5th of 6). Its design needs the most independent thought and shouldn't be rushed by trying to fit it into the same mold as the gathering-focused commands.

## Dependency Map

```
Q-3 (command vs skill) ──┐
                         ├──> All 6 rewrites
Q-4 (standards delivery) ┘

/charter ──> /spec ──> /architect ──> /define ──> /build
   │            │           │            │          │
   │            │           │            │          └── Unique: execution engine
   │            │           │            └── Depends on design output format
   │            │           └── Depends on spec output format
   │            └── References charter, sets traceability pattern
   └── Pattern-setter, simplest flow

/new-project ──> (independent, do last)
```

### Critical Path

1. **Q-3 + Q-4** (blocking research/design decisions)
2. **`/charter`** — pattern-setter, simplest, proves the behavioral standards work
3. **`/spec`** — adds traceability IDs, references charter, second validation of patterns
4. **`/architect`** — most complex gathering (domain-aware sections), adds requirement coverage
5. **`/define`** — depends on design output format, has batch-mode question (BUG-029)
6. **`/build`** — unique execution model, needs independent design
7. **`/new-project`** — structurally different, mostly cleanup bugs, do last

### What Can Be Parallelized

Within the design phase, very little. Each command rewrite informs the next. The dependency chain is real — `/spec` references `/charter` output, `/architect` references `/spec` output, etc.

However: **design and implementation can overlap**. Once `/charter`'s design is approved, its implementation can begin while `/spec`'s design is being developed. This pipelining is the main parallelization opportunity.

Within a single command rewrite, the Mode 3 team already provides internal parallelism (5 perspectives reviewing simultaneously).

## Bug Distribution Per Command

| Command | Bugs | Pattern-Class | Command-Specific |
|---------|------|--------------|-----------------|
| /new-project | 9 | 3 (BUG-007,008,009) | 6 (BUG-001-006) |
| /charter | 7 | 3 (BUG-012,014,016) | 4 (BUG-010,011,013,015) |
| /spec | 6 | 4 (BUG-017,018,020,021) | 2 (BUG-019,022) |
| /architect | 5 | 0 | 5 (BUG-023-027) |
| /define | 5 | 2 (BUG-031,032) | 3 (BUG-028-030) |
| /build | 5+2 | 4 (BUG-034,036,037,042,043) | 2 (BUG-033,035) |

Pattern-class bugs (REQ-F1 through F5) are addressed by the behavioral standards themselves — once the standards are codified and applied, these bugs are fixed by construction. Command-specific bugs require individual attention during each rewrite.

## Scope Creep Risks

1. **Agent prompt revision (Q-5)** is listed as "open" in the spec. This is a separate workstream. If it gets folded into the command rewrites, it doubles the scope. Keep it separate — the agent prompts can be updated after the commands are stable.

2. **Command rename (describe/design/do)** is noted in PLANNING.md as "deferred to implementation." This is fine as long as it stays deferred per-command and doesn't become a batch rename exercise.

3. **BUG-029 (batch mode for /define)** is a design question, not just a bug fix. The existing command says "each run creates a NEW DIP" but users naturally want batch creation. This needs a design decision, not just a rewrite. Flag it during `/define` design.

4. **Todoist references** appear in `/new-project`, `/charter`, `/spec`, `/architect`, and `/define`. The charter still mandates Todoist but SPEC-004 defers `/breakdown`. The rewrites need to handle Todoist as optional without deepening the dependency. This is already implicit in the spec but should be explicit in each rewrite.

## What's Well-Planned

- **Bug disposition table is complete.** 35 bugs + 1 issue in scope, cleanly categorized. No ambiguity about what each rewrite must address.
- **Full rewrite approach is correct.** These 60-102 line prompt files are small enough to rewrite cleanly. Patching would leave inconsistent voice and structure.
- **Mode 3 teams are appropriate.** Each command rewrite benefits from multiple perspectives catching cross-cutting issues in real time.
- **Scope exclusions are clean.** `/deliver` and `/breakdown` are properly excluded with rationale. No loose ends.
- **The spec-to-design-to-build pipeline is the natural rewrite order.** The dependency chain matches the workflow the commands themselves implement.

## Self-Evaluation

- **What worked well:** Reading all 6 command files to understand structural differences between `/new-project`+`/build` and the other four. This drove the sequencing recommendation rather than just going alphabetically or by bug count.
- **What I struggled with:** Estimating Mode 3 team rewrite time. Each session involves 5+ agents reviewing and iterating — the calendar time is hard to predict because it depends on how many review cycles each command needs.
- **Prompt improvement suggestions:** My prompt could include guidance on estimating collaborative team work vs. solo work. The multiplier for Mode 3 sessions is non-obvious.