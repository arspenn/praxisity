## Skeptic Cross-Review: Is the Fix List Over-Engineered?

**Artifact:** All SPEC-005 agent reports (critic, designer, user-advocate, project-manager, consistency-reviewer, prompt-engineer, fresh-eyes-reviewer)
**Date:** 2026-03-29
**Dispatch Mode:** Mode 3 (collaborative team)

---

## The Aggregate Finding Count

Across 7 reports (excluding my own initial skeptic report), the team produced approximately 42 distinct findings. The PM explicitly says "proceed." The question is: how many of the remaining findings actually need to be fixed before using the system?

---

## Triage: What Must Be Fixed, What Can Wait, What Is Noise

I've categorized every finding from every report into one of four buckets:

### Fix Before Use (5 findings)

These would cause real confusion or failure during the first real deployment.

| # | Source | Finding | Why it can't wait |
|---|--------|---------|-------------------|
| 1 | User Advocate | `/agents` command referenced in SKILL.md doesn't exist | A dead reference in the primary guidance document. First time something goes wrong with agent discovery, the user hits a wall with no recovery path. One-line fix. |
| 2 | Consistency Reviewer | No agent embeds "Instructions Received" in Output Format despite REQ-F8 requiring it | This is a spec-to-implementation gap. If the goal is agent-authored reports with instruction echo, the agents need to be told to do it. Without this, reports won't contain what the spec says they should. But see my note below -- the Critic's argument that this is "verification theater" weakens the case. **Verdict: fix if you keep the requirement; drop the requirement if you agree with the Critic.** Either way, the documents should be consistent. |
| 3 | Prompt Engineer | "What you ignore" sections use negative framing (elephants problem) | Affects all 8 agents on every dispatch. The Prompt Engineer's fix is clear (positive scoping instead of negation) and low-effort. This is the single highest-value prompt improvement -- it costs ~15 minutes and improves every future agent run. The PM agrees this is highest priority. |
| 4 | User Advocate | Mode 1 has no actionable guidance anywhere | The simplest entry point to the system has zero instructions on how to actually use it. One example sentence in the Tier 1 pointer or SKILL.md fixes it. |
| 5 | User Advocate | Tier 1 pointers don't explain what "invoke the consult-team skill" means | Related to #4. A new user sees jargon with no explanation. One concrete example fixes it. |

### Fix Soon but Don't Block (8 findings)

Real issues that matter for quality but won't cause failure if deferred to after the bootstrapping test.

| # | Source | Finding | Why it can wait |
|---|--------|---------|-----------------|
| 6 | Critic | Orphaned fresh-eyes-reviewer memory directory | Cleanup task. Won't interfere with normal operation. |
| 7 | Consistency Reviewer | Consistency-reviewer output format diverges from other 7 agents | Works fine as-is. Alignment improves synthesis but doesn't block individual use. |
| 8 | Prompt Engineer | Project Context boilerplate duplicated across 7 agents (~300 tokens redundant in full dispatch) | Real waste but the system functions. Fix during first prompt refinement pass. |
| 9 | Prompt Engineer | "Dispatch Mode" field undefined within agent files | Agents will guess or leave blank. Not fatal. |
| 10 | Prompt Engineer | Remove "(student)" from project-manager | Subtle bias issue. Fix during prompt refinement. |
| 11 | Critic | Review file naming convention already violated by 9 of 12 files | Historical artifacts. Future files follow the convention. Add a note about legacy files. |
| 12 | User Advocate | Add "how to check" for Mode 3 availability | Good UX improvement, doesn't block Mode 1/2 usage. |
| 13 | Consistency Reviewer | Collab-mode.md missing session report template path | Mode 3 teammates might use their own format. Fixable with one line. |

### Probably Not Worth Fixing (12 findings)

These are findings where the fix costs more than the problem, the problem is theoretical, or the finding is a documentation artifact rather than a real issue.

| # | Source | Finding | Why I'm challenging it |
|---|--------|---------|----------------------|
| 14 | Critic | "Verification" claim overstated for Instructions Received | The Critic is right that self-reported instruction recording isn't true verification. But the fix is just softening language in the design doc. The design doc is a planning artifact that's already been implemented. Editing it now is polish on a document whose job is done. **If the agents are about to be used on real work, spending time wordsmithing DEC-3 is a misallocation.** |
| 15 | Critic | Skill defers to platform for agent index with no inline fallback | The Critic wants ~30 lines of agent index embedded in the skill. This directly contradicts the progressive loading principle (don't load roster details until dispatch). The README exists. The platform listing exists. Adding a redundant third source creates a synchronization problem. |
| 16 | Critic | Mode 3 fallback to Mode 2 doesn't acknowledge capability loss | True, but the skill already says "when in doubt, start with Mode 2." Adding a paragraph explaining what Mode 3 does that Mode 2 doesn't is re-explaining the decision gate that's already in the skill. The user who chose Mode 3 already understands the difference. |
| 17 | Critic | Write tool isn't path-restricted | Acknowledged in the design. Prompt-enforced, not platform-enforced. The Critic's own assessment says "low in practice." Agree -- this is a theoretical concern. |
| 18 | Critic | Session report template conflates two document types | The template has two sections. Users use the relevant one. This works fine. Splitting it into two files for "clarity" adds a file to maintain. |
| 19 | Prompt Engineer | Self-evaluation sections are open-ended and will vary | The PM explicitly says "use the agents first, then fix what the experience reveals matters." Structured self-evaluation might be better, but we have zero data on whether the current open-ended format produces useful output. Fix after bootstrapping, not before. |
| 20 | Prompt Engineer | Agent memory update instructions are underspecified | The memory system is COULD priority. The agents will either figure out `memory: project` from the frontmatter (likely, given Claude Code handles this natively) or they won't write memories (acceptable). Specifying the exact mechanism before we know if agent memory is even useful is premature. |
| 21 | Prompt Engineer | Critic's severity levels undefined | The Critic worked fine in this review without definitions. The severity levels are intuitive enough. If calibration drift appears across sessions, define them then. |
| 22 | Prompt Engineer | Stakeholder lacks audience determination guidance | The Stakeholder agent is the one I flagged as premature in my initial report (no external audience exists yet). Improving its audience detection for a context it won't encounter is doubly premature. |
| 23 | Designer | Mode 3 prompt ordering rationale not stated | The implementation is correct. Adding a comment explaining why collab-mode precedes context block is nice-to-have documentation. |
| 24 | Designer | DATA-1 schema doesn't match actual agent file sections | Design-to-implementation drift. The files are the source of truth now. Updating the design doc is polish. |
| 25 | Prompt Engineer | Consistency-reviewer format breaks cross-agent pattern | Duplicate of consistency-reviewer's own Issue #1 (finding #7 above). Already counted. |

### Documentation Cleanup Only (17 findings)

These are spec-to-DIP drift, cosmetic issues, or cross-reference fixes that matter only if someone re-implements from the planning documents. The implementation exists and works. Fixing planning docs post-implementation is archival work, not engineering.

| Source | Finding | Status |
|--------|---------|--------|
| Fresh-eyes | Spec doesn't enumerate templates as deliverables | Design does. Spec is done. |
| Fresh-eyes | "7x duplication" vs "8x" arithmetic | Cosmetic. |
| Fresh-eyes | REQ-F1 implies all frontmatter fields required, design says some optional | Implementation settled this. |
| Fresh-eyes | REQ-F3 item 5 ("what to preserve") broader than design's "report saving" | Session report template covers this adequately. |
| Fresh-eyes | REQ-F11 says skill supports 3 modes, design says Mode 1 is in COMP-4 | Intentional design split. AC-11 needs updating. |
| Fresh-eyes | No AC for REQ-F9 (COULD priority) | Intentional omission for COULD item. |
| Fresh-eyes | Template file paths not in spec | Design-level detail, correctly deferred from spec. |
| Fresh-eyes | Out-of-scope tension on Write access | Already resolved: all agents have Write, enforced by prompt. |
| Consistency Reviewer | Command pointer format differs from DIP-007 | Design INT-2 and implementation agree. DIP is stale. |
| Consistency Reviewer | DIP-006 AC-1 contradicts its own Step 1 | AC-1 wins. DIP is stale. |
| Consistency Reviewer | DIP-005 created date vs DIP-004 created date | Informational. |
| Consistency Reviewer | README agent order vs spec/design order | Cosmetic. |
| User Advocate | Template files don't say they're AI-facing | Minor. Curious users figure this out. |
| User Advocate | Review naming inconsistent in practice | Already counted under finding #11. |
| User Advocate | README doesn't explain how to use agents | Covered by finding #4 (Mode 1 guidance gap). |
| User Advocate | Decision gate complexity cliff Mode 2 to Mode 3 | This is Mode 3's inherent complexity, not a documentation problem. |
| Designer | Decision gate doesn't note Mode 3 downgrade asymmetry | One sentence could be added. Not blocking. |

---

## The Meta-Finding: Scope Creep in the Fix List

The team produced ~42 findings. My triage says **5 need fixing before use**. That's a 12% fix rate. The other 88% is either deferrable, probably not worth fixing, or documentation cleanup.

This is itself a case study in the problem the Skeptic agent exists to catch. Seven agents were told to find issues. They found issues. Each agent's findings are individually reasonable within their mandate. But aggregated, they create a 42-item backlog for a system that the PM explicitly says is ready to use.

**The collective output exhibits the exact pathology the system was designed to prevent: scope creep disguised as thoroughness.**

Patterns I see in the noise:

1. **Documentation archaeology.** Multiple agents spent significant effort comparing spec wording to design wording to DIP wording to implementation. These documents were written sequentially in a single session. Of course they drifted. The implementation is the source of truth. Fixing the planning docs is archival work with zero impact on system behavior.

2. **Agents finding each other's work.** The consistency reviewer and the fresh-eyes reviewer overlap heavily (naming conventions, format deviations). The prompt engineer and the critic both flag the Write tool restriction issue. The user advocate and the critic both note the Mode 3 fallback gap. Cross-agent redundancy is expected in parallel dispatch -- but the lead review should deduplicate before presenting to the developer.

3. **Theoretical concerns rated as Important.** The Critic rates "verification claim overstated" as Critical. But the actual impact is: a sentence in a design document overstates a capability. Nobody will die. Nobody's code will break. The design doc is a planning artifact that served its purpose.

4. **Agents manufacturing findings within their mandate.** The Stakeholder report is absent from this round, but the User Advocate found 7 issues for a system whose end-user journey literally starts with "tell the AI to dispatch an agent." Most of the UX friction findings are real but amount to "add one sentence here." That's 7 findings for 7 sentences.

5. **Prompt refinement suggestions treated as bugs.** The Prompt Engineer's 9 findings are all valid prompt quality observations. None are bugs. None prevent the system from functioning. They're the kind of improvements you make after session 5, not before session 1.

---

## Recommendation

**Do 5 things, then start using the system:**

1. Fix the dead `/agents` reference in SKILL.md (1 minute)
2. Add one example sentence to Tier 1 pointers showing how to invoke an agent (2 minutes)
3. Add one sentence to SKILL.md or Tier 1 explaining what "invoke the consult-team skill" means (1 minute)
4. Rewrite "What you ignore" to positive scoping in all 8 agents (15 minutes)
5. Decide: keep or drop the "Instructions Received" requirement. If keep, add it to agent Output Format sections. If drop, update REQ-F8 and DEC-3. (5 minutes either way)

Everything else goes on a "fix after bootstrapping" list. The bootstrapping test will reveal which of the remaining 37 findings actually matter in practice. My prediction: fewer than half will prove relevant.

**Total estimated fix time: ~25 minutes.** Not 42 items. Not a sprint. Twenty-five minutes, then use the system on real work.

---

## Self-Evaluation

- **What worked well:** Reading all 7 reports in sequence revealed the redundancy pattern clearly. Several findings appeared in 2-3 reports (naming conventions, Write tool restrictions, Mode 3 fallback). Counting and categorizing forced a severity assessment that individual reports don't provide.

- **What I struggled with:** The line between "probably not worth fixing" and "fix soon" is judgment, not fact. Finding #15 (inline agent index in skill) is where I'm least confident -- the Critic makes a reasonable argument for self-containment, and my counter-argument (synchronization cost) is also reasonable. Real usage would settle this.

- **Prompt improvement suggestions:** My prompt focuses on challenging whether individual things are necessary. For this cross-review task, I needed to challenge whether the *aggregate* is necessary -- a different skill. My prompt could add: "When reviewing collections of recommendations, assess whether the total cost of implementing all of them is proportional to the total benefit, and whether the recommendations as a group exhibit the same scope creep patterns you look for in designs."
