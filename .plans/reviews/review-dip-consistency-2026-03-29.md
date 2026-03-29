## Cross-Document Consistency Review

**Documents reviewed:**
- `/home/arspenn/Dev/praxisity/.plans/specs/005-agent-consultation-system.md`
- `/home/arspenn/Dev/praxisity/.plans/designs/004-agent-consultation-system.md`
- `/home/arspenn/Dev/praxisity/.plans/prompts/004-templates-and-extensions.md`
- `/home/arspenn/Dev/praxisity/.plans/prompts/005-agent-definition-files.md`
- `/home/arspenn/Dev/praxisity/.plans/prompts/006-consult-team-skill.md`
- `/home/arspenn/Dev/praxisity/.plans/prompts/007-tier1-command-pointers.md`

**Status:** Issues Found

---

## Issues

### Issue 1 — DESIGN-004, Section 1.3 Requirements Coverage table: Wrong DEC reference for REQ-N2

**Location:** `DESIGN-004` → Section 1.3, Requirements Coverage table, row for `REQ-N2`

**What it says:** The "Design Section" column lists `COMP-3, DEC-4`

**What it should say:** `COMP-3, DEC-5`

**The contradiction:** DEC-4 in DESIGN-004 is titled "Native Claude Code Subagent Format" and covers the rationale for using `.claude/agents/` native format (relevant to REQ-F1 and REQ-F9, not REQ-N2). DEC-5 is titled "Skills as Guidance, Not Control Flow" — that is the decision directly addressing REQ-N2 ("The consult-team skill shall be guidance and context, not control flow"). An implementer following the trace in Section 1.3 for REQ-N2 would look up DEC-4 and find irrelevant rationale.

**Why it matters for implementation:** DIP-006 cites `DEC-5` correctly in its Required Reading ("Section 6: DEC-5 - Skills as Guidance, Not Control Flow"). The cross-reference in the design itself is wrong, but the DIP happens to fix it. The error remains in the design as a false trail. If a future implementer doing independent verification follows Section 1.3, they read the wrong design decision.

---

### Issue 2 — REQ-N1 (dual-consumption) not claimed by DIP-004 or DIP-006

**Location:** `DIP-004` → Technical Requirements → Must Satisfy table; `DIP-006` → Technical Requirements → Must Satisfy table

**What is written:** Neither DIP lists REQ-N1 ("All agent files and skill content shall be optimized for dual consumption: human-readable AND effective as AI prompts") in their Must Satisfy tables. Only DIP-005 claims REQ-N1.

**What the design says:** DESIGN-004 Section 1.3, REQ-N1 row: Design Section = "All" and Approach = "All files authored for dual consumption (human-readable + AI-effective)."

**The contradiction:** The design explicitly assigns REQ-N1 to all components. DIP-004 produces three template files and DIP-006 produces the skill file — both are content that functions as AI prompt input. But if an implementer reads only their DIP's Must Satisfy table (as instructed), they see no obligation to apply dual-consumption quality to those files.

**Why it matters for implementation:** Templates and the skill file are loaded directly into agent context. The dual-consumption requirement is exactly why a template needs to be written so that a cold-reading AI agent can follow it as well as a human developer can read it. This is not caught by acceptance criteria in either DIP.

---

### Issue 3 — DIP-006 AC-6 acceptance criterion conflicts with what the DIP instructs

**Location:** `DIP-006` → Acceptance Criteria, AC-6

**What AC-6 says:** "Given the skill content, then it contains no execution sequences or control flow — only guidance and decision frameworks"

**What the DIP's implementation instructions say:** DIP-006 Step 4 (Mode 3 Dispatch Guidance) lists: "Create team... Spawn each teammate... Teammates maintain context... Teammates can message each other... Don't shut down teammates prematurely... Each teammate writes their own report... Clean up: shut down teammates, then have the lead clean up the team." This is written as a procedural sequence.

**The tension:** The spec (REQ-N2) and design (DEC-5) are clear that the skill must be guidance, not control flow. The DIP's own AC-6 restates that rule. But the DIP's Step 4 implementation instructions read as a step-by-step workflow, not as a decision framework. An implementer following Step 4 literally would produce a Mode 3 section that looks like control flow — which would then fail AC-6.

**Why it matters for implementation:** The implementer receives conflicting signals within the same document. The implementation steps drive toward a deterministic workflow; the acceptance criterion rejects that output. The implementer needs to know that Step 4 describes *what the skill should convey as context*, not the literal structure of the skill content.

---

## Recommendations (advisory, do not block approval)

- **DESIGN-004 Section 1.3:** Correct `DEC-4` to `DEC-5` in the REQ-N2 row. One-character fix, eliminates a false trail.

- **DIP-004 and DIP-006 Must Satisfy tables:** Add REQ-N1 to both. This brings the DIPs into alignment with the design's "All components" assignment and ensures implementers reading only their DIP get the reminder.

- **DIP-006 Step 4:** Add a clarifying note — something like: "The skill should convey this lifecycle as context the main agent understands, not as a step-by-step procedure. Write it so the agent knows what to think about, not what to execute." This reduces the risk of the implementer producing exactly the output AC-6 rejects.

---

## Self-Evaluation

**Most frequent inconsistency types:** Cross-reference errors (wrong ID pointing to wrong section) and requirement coverage gaps (a requirement assigned to "all" in the design but not claimed in individual DIPs). Both are the classic gap between what was decided and what was recorded.

**Unable to assess:** Technical correctness of the Claude Code platform mechanics (Agent tool parameters, TeamCreate API, experimental flag behavior). Whether the agent prompts as described will produce useful differentiated output in practice. Whether the INT-2 format for Tier 1 pointers is actually compact enough to not bloat command files.

**Document structure quality:** Cross-referencing was generally excellent. The DIPs' "Must Satisfy" and "Interfaces to Use" tables made tracing from spec requirements to implementation obligations straightforward. The design's 1.3 Requirements Coverage table is the single most valuable cross-reference artifact — it's also where the DEC-4/DEC-5 error lives. The scope boundary tables in each DIP (DO / DO NOT / Files in Scope / Files Out of Scope) are unusually precise and prevented any overlap ambiguity.

**Prompt improvement suggestions:** The DIP template should either (a) require explicit claiming of non-functional requirements in the Must Satisfy table, or (b) note which non-functional requirements apply to all DIPs by default. Currently REQ-N1 falls through because it's not component-specific — it applies everywhere but belongs to no single DIP explicitly.