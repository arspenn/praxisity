# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Identity

**Name:** Praxisity Framework
**Type:** Development Framework / Tooling
**Mission:** Build a design-first workflow framework enabling consistent, structured planning and execution for multi-disciplinary projects through AI-assisted tooling — where the framework builds the user through use, and the user builds the framework through experience.

## Framework Development Context

This repository IS the Praxisity framework itself. We are building the tool, not using it. Skills and templates created here will be used by future projects. Quality and thoughtfulness in design are paramount.

We use Praxisity to build Praxisity. The `.plans/` directory contains our own specifications and designs.

## Current Focus

**For current tasks and session state, see `PLANNING.md`.**

This separation keeps CLAUDE.md stable while PLANNING.md handles dynamic session state. Skills read PLANNING.md on start, update it during execution, record completion and next steps.

## Design-First Workflow

Every Praxisity project follows: Describe -> Design -> Plan -> Do

Each phase has a corresponding skill. Refer to the available skills for specifics — they are loaded into context automatically. See CHARTER.md for the authoritative scope and principles.

## Key References

**CHARTER.md** — Project constitution. Principles, scope, and constraints that guide all decisions.
**PLANNING.md** — Dynamic session state. Current task, progress, next steps.

## Bootstrapping Principle

Use the system to build the system. Use the system to build the user. Use the user to build the system.

Every session generates experience. At session end, ask: **"What did we learn that should become a skill, agent, or template?"** If the answer isn't "nothing," capture it before closing. Skills codify process. Agents codify perspective. Templates codify structure. The framework grows by using it.

## Pacing Directive

Sub-agents and tool calls execute at machine speed. The user does not. Your primary job is to keep the user in the loop — surface decisions, summarize parallel work, and confirm direction before charging ahead. When in doubt, pause and check in. Never trade user understanding for agent velocity.

## Hints from the developer
- Just because a template or example has a certain number of items, there is no requirement for your output to contain the same number of items filled out. It might be less, it might be more, use the right amount based on the relevant material and your judgement, not the example pattern.
- When we have learned a substantial amount about a specific process during a session, consider using the /skill-forge skill to capture that experience and insight.