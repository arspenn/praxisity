## Agent Report

**Agent:** consistency-reviewer
**Artifact:** SPEC-004
**Date:** 2026-04-01
**Dispatch Mode:** Mode 2: parallel

## Instructions Received

Check cross-document consistency: bug IDs match bug report, requirement rationales correctly cite bugs, no contradictions with CHARTER.md, acceptance criteria align with requirements.

## Findings

### Issue 1 (Medium): REQ-N1 (MUST) has no acceptance criterion

All other MUST requirements have corresponding ACs. REQ-N1 does not. Without an AC, reviewers cannot verify "targeted edits only" compliance.

### Issue 2 (Medium): BUG-031 misattributed to REQ-F1

REQ-F1 lists BUG-031 ("Template sections silently removed instead of marked N/A") alongside BUG-009 family bugs about Write-from-scratch vs. copy-then-edit. BUG-031's actual problem is different: when a section doesn't apply, the agent removes it instead of marking N/A. This behavior persists even with `cp` + Edit. BUG-031 needs its own requirement or sub-clause.

### Issue 3 (Low): REQ-F3 cites BUG-018 and BUG-034 but omits BUG-012

BUG-012 (/charter: constraints gathered as single combined prompt) is the same pattern class and should be cited in REQ-F3's rationale for traceability.

### Issue 4 (Low): "across all 7 tested commands" is ambiguous

Bug report shows /breakdown had no bugs logged. The 46 bugs span 6 commands with bugs plus /deliver. "7 tested" vs "7 with bugs" vs "8 total" needs clarification.

### Recommendations (advisory)

1. **Acknowledge Charter tension around Todoist.** CHARTER.md Principle 2 mandates Todoist; REQ-F6 defers it. This direction change should be noted so a Charter update can be tracked.
2. **Add ACs for SHOULD requirements REQ-F6 and REQ-F7** — both are concretely testable.
3. **Clarify bug partition between OBJ-2 (pattern-class) and OBJ-3 (command-specific)** — implementer would need to re-derive which bugs fall under which objective.

## Self-Evaluation

- **What worked well:** Systematic bug ID cross-referencing caught the BUG-031 misattribution and BUG-012 omission
- **What you struggled with:** Unable to verify whether templates referenced in REQ-F1 actually exist at `.praxisity/templates/`
- **Prompt improvement suggestions:** For bug-fix specs, instruct reviewer to verify uncited bugs are accounted for, not just that cited bugs are correct
