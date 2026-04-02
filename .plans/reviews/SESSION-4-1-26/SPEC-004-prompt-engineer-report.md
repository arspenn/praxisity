## Agent Report

**Agent:** prompt-engineer
**Artifact:** SPEC-004
**Date:** 2026-04-01
**Dispatch Mode:** Mode 2: parallel

## Instructions Received

Evaluate dual-consumption fitness: will the proposed standards work as prompt instructions that prevent bugs from recurring? Are there "don't think about elephants" problems? Are requirements clear enough as AI-consumed instructions?

## Findings

### Ambiguity: REQ-F1 says what to do but not where to say it

The spec never addresses the delivery mechanism — will rules be written into each command individually, into a shared reference, or into CLAUDE.md? The architect needs this answered.

### Ambiguity: "sequential" in REQ-F2 is insufficient for AI consumption

The bug report shows Claude parallelized pre-flight steps despite numbered lists. "Sequentially" is a description of *how*, not a constraint that actively prevents the failure mode. The fix needs explicit language: "Execute each pre-flight step one at a time. Do not begin step N+1 until step N is complete. Do not batch or parallelize pre-flight steps." The current pattern was already defeated — the fix must be stronger.

### Ambiguity: REQ-F3 "explicit stop" is vague for AI

An AI might interpret this as showing a section header and blank line. The load-bearing phrasing is: "Do not draft content for sections the user has not yet been prompted for." That prevents the actual failure mode (drafting everything then presenting for approval).

### Elephants: BUG-009 exception clause invites the exact bug it fixes

The bug report's fix description includes an exception for "prior project context" that, if carried into the standard, creates an escape hatch AI agents will use liberally. The default must be copy-then-edit with no implicit re-use detection.

### Noise: UC-2 adds no constraint value

May lead the architect to over-invest in the reference document rather than focusing on fixing existing commands.

### Clarity: REQ-F4 "complete prescribed success message" is a meta-pattern

Each command's "complete" is different. The standard should be phrased as: "each command shall emit every element listed in its own Success Message section" — a meta-instruction, not a uniform template.

### Drift: REQ-F7/F8 overlap with existing CLAUDE.md hint

Existing hint already addresses template anchoring. REQ-F7 should specify whether to replace, expand, or leave the existing note alongside a new one.

## What's Well-Engineered

- Pattern extraction into 5 behavioral standards is excellent prompt engineering thinking
- REQ-F1's `cp` then Edit prescription names exact tools — removes interpretability
- REQ-F5's "hard gate" language creates ordering dependency that's hard to skip
- AC-1's "byte-for-byte unchanged" is testable and unambiguous
- Bug report as evidence base enables architect to understand spirit, not just letter

## Self-Evaluation

- **What worked well:** Reading command files that already had numbered lists revealed the parallelization fix needs stronger language
- **What you struggled with:** Boundary between prompt engineering feedback and design feedback is fuzzy for prompt-infrastructure specs
- **Prompt improvement suggestions:** Need explicit guidance on evaluating specs that describe prompt infrastructure — "will the proposed language actually constrain the target agent's behavior?" is a specialized check
