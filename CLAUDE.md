# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Identity

**Name:** Praxisity Framework
**Type:** Development Framework / Tooling
**Mission:** Build a design-first workflow framework enabling consistent, structured planning and execution for multi-disciplinary projects through AI-assisted tooling.

## Framework Development Context

This repository IS the Praxisity framework itself. We are building the tool, not using it (yet). Commands and templates created here will be used by future projects. Quality and thoughtfulness in design are paramount.

Once core commands exist, we'll use Praxisity to build Praxisity (eating our own dog food). The `.plans/` directory contains our own specifications and designs.

## Current Focus

**For current tasks and session state, see `PLANNING.md`.**

PLANNING.md contains:
- Active command/task context
- Gathered state during command execution
- Completed work this session
- Next steps

This separation keeps CLAUDE.md stable while PLANNING.md handles dynamic session state.

Commands read PLANNING.md on start, update it during execution, record completion and next steps. It is archived to `.plans/archive/PLANNING-[timestamp].md` at task end or new session.

## Design-First Workflow

Every Praxisity project follows: Specify -> Design -> Breakdown -> Implement

This framework enforces that workflow through command dependencies:
- `/spec` creates specifications
- `/architect` requires specs to exist
- `/breakdown` requires designs to exist
- `/define` requires both specs and designs
- `/build` requires DIPs to exist

## Important Files

**praxisity-foundation-plan.md** - Source of truth for MVP scope. Reference when making decisions. Will be removed by `/new-project` for end users.

## Hints from the developer
- Just because a template or example has a certain number of items, there is no requirement for your output to contain the same number of items filled out. It might be less, it might be more, use the right ammount based on the relevant material and your judgement, not the example pattern.