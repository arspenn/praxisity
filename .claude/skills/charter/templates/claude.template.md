# CLAUDE.md

<!--
This file steers Claude Code in this project. It is not a description of the project; the
agent reads the code, the charter, and the plans for that. It holds what the agent cannot
infer: the project's identity, the constitution to consult, the workflow to follow, and
corrections for things it gets wrong repeatedly. Comprehensive context files cost more and
help less (Gloaguen et al., 2026, "Evaluating AGENTS.md"), so start minimal and add a line
only when you have watched the agent make the same mistake twice.

HTML comments are stripped from the finished file.
-->

## Project Identity

**Name:** [PROJECT_NAME]
**Domain:** [From the charter's Domain Context: software, public health, research, instructional design, other]
**Mission:** [One sentence, from the charter]

## Project Constitution

@CHARTER.md

<!-- The import line above loads the charter into every session. When the agent faces a
     judgment call about scope or priorities, the charter is what it consults. -->

## Current Focus

For current tasks and session state, see `PLANNING.md`. Workflow skills read it on start, update it as they run, and record completion and next steps, so a new session picks up where the last one stopped.

## Workflow

Work follows Describe → Devise → Detail → Do (`/describe`, `/devise`, `/detail`, `/do`), with `/charter` as the entry point. Each phase cites the previous phase's artifact by ID; do not skip a phase.

## Behavioral Corrections

Add an entry here only after the agent has made the same mistake more than once. Format: a bold short name, a colon, then what to do instead and why. Keep an entry until the thing it refers to no longer exists, or until a new model release gives reason to test it: remove it, watch a few sessions, and restore it if the mistake returns. The agent cannot tell from the inside whether a correction is still doing work, so "the mistake stopped" is not evidence it can be removed.

## Non-Obvious Context

Pointers to files or facts the agent would not find by exploring the project. Remove them when they become obvious.
