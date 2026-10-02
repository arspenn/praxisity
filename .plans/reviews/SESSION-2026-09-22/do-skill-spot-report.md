# Do Skill Clarity Review

## Issues Found

1. **Step ordering contradiction** (lines 26–28): "Step 2 lands first so that an interrupted run still leaves PLANNING.md accurate, and steps 3 and 4 decide whether this is a fresh run or a resume" contradicts "Run these steps in order and finish each before starting the next." It is unclear whether steps are reordered or executed sequentially.

2. **Undefined task-tracking tool** (line 42): "Create one entry per step in your task-tracking tool" — what tool? Where does it live? How is it accessed? No prior definition or reference.

3. **Resume point recording format** (lines 36, 51): Line 51 says "record `DIP-NNN at step N` in PLANNING.md's Next Steps" but line 36 says resume "from the step PLANNING.md's Next Steps last recorded." The exact format and content of this record is not specified. Is it a prose string or structured data?

4. **Deviation recording mechanism** (lines 52, 64, 75): "Record the deviation" and "skip with a recorded deviation" appear three times, but the skill never specifies how deviations are captured or stored during execution. Only at line 75 is the destination stated: "commit body."

5. **Verify form detection** (line 50): "Run the step's Verify in whichever form it takes. For a human judgment, name what the judge should look at." But the skill provides no method to detect whether a Verify is a command, an observable check, or human judgment if the DIP text is ambiguous.

6. **TBD criteria matching** (line 61): "Mark rows that read 'TBD' or 'tested in the DIP for COMP-n' as deferred." The phrase "tested in the DIP for COMP-n" does not appear in dip.template.md and the match criteria (substring, exact string) is undefined.

7. **Resume status clearing** (line 55): "Resume from a halt within the same run by clearing the Halted status back to `In Progress`" but the pre-flight section (lines 35–36) offers restart as an alternative. The instructions do not specify whether restart clears Status to Ready or In Progress.

8. **Blocked scope detection timing** (line 53): "If completing the step would change something outside Artifacts in Scope, do not make the change." It is unclear whether this is checked before step execution, after Verify, or during step completion.

9. **Completion gate next-element rule** (line 79): "Next Steps naming the DIP and its outcome... and the next element to detail per the design's §7.1 Implementation Order." But if a run halts, line 91 offers to fix or revise; it does not mention naming the next element. When is the next element recorded?

10. **Secret pattern override mechanism** (line 72): "Scan the changed content for secret patterns" and refuse staging without "the user's explicit override." The mechanics of override (a keyword, a confirmation prompt format) are not specified.

## Summary

Step ordering contradicts itself. Task-tracking tool, deviation recording, and resume status branching are undefined. Verify form detection assumes the DIP text is unambiguous; TBD criterion matching relies on an undefined phrase. Completion gate behavior differs between halted and done outcomes. Override mechanism for secret patterns is unexplained.