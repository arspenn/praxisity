# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

<!--
ABOUT THIS FILE

This is NOT a place to describe your codebase. It is a place for behavioral
corrections -- things the agent consistently gets wrong that you want to steer.

If the agent can discover it by reading your code, it does not belong here.
The agent already reads your package.json, directory structure, config files,
and source code. Repeating that information here wastes context tokens, biases
the agent toward mentioned patterns (even irrelevant ones), and goes stale
as your codebase evolves.

Research shows comprehensive context files increase agent costs by 20%+ with
only marginal benefit to task success (+4% developer-written, -3% LLM-generated).
Source: Gloaguen et al., 2026 - "Evaluating AGENTS.md"

WHAT BELONGS HERE:
- Mental model shifts the agent cannot infer from code
  (e.g., "this repo is a framework, not a project using the framework")
- Workflow constraints that override default behavior
  (e.g., "always run /spec before /architect")
- Behavioral corrections for repeated mistakes
  (e.g., "use Convex, not TRPC -- TRPC is legacy")
- Pointers to non-obvious files the agent wouldn't find on its own

WHAT DOES NOT BELONG HERE:
- Directory trees (the agent can ls/glob)
- Dependency lists (the agent reads package.json/requirements.txt)
- Architecture descriptions (the agent reads your code)
- Code style rules (use linters/formatters instead)
- Setup instructions (put these in README.md)
- Git workflow details (the agent knows conventional commits)

START MINIMAL. Add content only when you observe the agent consistently
getting something wrong. Remove content when new model releases fix the issue.
-->

## Project Identity

**Name:** [PROJECT_NAME]
**Type:** [software | public-health | research | other]
**Mission:** [One sentence - what does this project accomplish?]

## Current Focus

**For current tasks and session state, see `PLANNING.md`.**

PLANNING.md contains:
- Active command/task context
- Gathered state during command execution
- Completed work this session
- Next steps

This separation keeps CLAUDE.md stable while PLANNING.md handles dynamic session state.

Commands read PLANNING.md on start, update it during execution, record completion and next steps. It is archived to `.plans/archive/PLANNING-[timestamp].md` at task end or new session.

## Workflow

<!-- Keep this section. The command dependency chain is a non-obvious constraint
     that the agent cannot infer from reading individual commands. -->

Every project follows: Specify -> Design -> Breakdown -> Implement

This framework enforces that workflow through command dependencies:
- `/spec` creates specifications
- `/architect` requires specs to exist
- `/breakdown` requires designs to exist
- `/define` requires both specs and designs
- `/build` requires DIPs to exist

All tasks tracked in Todoist project: "[TODOIST_PROJECT_NAME]"

## Bootstrapping Principle

Use the system to build the system. Use the system to build the user. Use the user to build the system.

Every session generates experience. At session end, ask: **"What did we learn that should become a skill, agent, or template?"** If the answer isn't "nothing," capture it before closing. Skills codify process. Agents codify perspective. Templates codify structure. The framework grows by using it.

## Behavioral Corrections

<!-- Add entries here ONLY when you observe the agent repeatedly making the
     same mistake. Remove entries when they're no longer needed.

     Format:
     **[Short description]:** [What to do instead and why]

     Example:
     **Use Convex, not TRPC:** TRPC is legacy in this codebase. All new
     server functions should use Convex actions/queries in the /convex directory.
-->

## Non-Obvious Context

<!-- Add pointers to files or concepts the agent wouldn't discover through
     normal codebase exploration. Remove if they become obvious.

     Example:
     **data-dictionary.xlsx** - Source of truth for field names. Located in
     /docs/ but not referenced by any code. Check before creating new schemas.
-->
