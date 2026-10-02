## Prompt Engineer Cross-Review: Agent Report Quality

**Date:** 2026-03-29
**Scope:** All SPEC-005 agent reports in `.plans/reviews/` (excluding my own)
**Purpose:** Evaluate reports as dual-consumption artifacts -- human-readable documents AND effective input for lead review synthesis.

**Reports reviewed:**
1. `SPEC-005-designer-report.md` (designer)
2. `SPEC-005-skeptic-report.md` (skeptic)
3. `SPEC-005-user-advocate-report.md` (user-advocate)
4. `SPEC-005-project-manager-report.md` (project-manager)
5. `SPEC-005-critic-report.md` (critic)
6. `SPEC-005-consistency-reviewer-report.md` (consistency-reviewer)
7. `SPEC-005-fresh-eyes-reviewer-report.md` (fresh-eyes, round 1)
8. `SPEC-005-fresh-eyes-reviewer-report-2.md` (fresh-eyes, round 2)

---

## Part 1: Structural Consistency Across Reports

### Report metadata completeness

| Agent | Artifact field | Date | Dispatch Mode | Instructions Received |
|-------|---------------|------|---------------|----------------------|
| Designer | Yes | Yes | "Mode 3: collaborative team" | Yes (detailed) |
| Skeptic | Yes | Yes | "Mode 3: collaborative team" | No |
| User Advocate | Yes | Yes | "Mode 3 (collaborative team)" | Yes (detailed) |
| Project Manager | Yes | Yes | "Mode 3" | No |
| Critic | Yes | Yes | "Mode 3 (collaborative team)" | No |
| Consistency Reviewer | Yes (doc list) | No explicit date | No | No |
| Fresh-eyes (r1) | Yes (doc list) | Yes | No | No |
| Fresh-eyes (r2) | Yes (doc list) | Yes | No | No |

**Observations:**
- Only 2 of 8 reports include "Instructions Received" sections (designer, user-advocate). This confirms the consistency-reviewer's Issue #2: the agent Output Format templates do not instruct this, so most agents skip it.
- Dispatch Mode formatting varies: "Mode 3", "Mode 3: collaborative team", "Mode 3 (collaborative team)". For human reading this is fine. For automated parsing or consistent synthesis, it would cause friction.
- The consistency-reviewer and both fresh-eyes reports use entirely different header structures from the other 5.

### Self-evaluation section consistency

| Agent | "What worked well" | "What you struggled with" | "Prompt improvement suggestions" |
|-------|-------------------|--------------------------|--------------------------------|
| Designer | Yes | Yes | Yes |
| Skeptic | Yes | Yes | Yes |
| User Advocate | Yes | Yes | Yes |
| Project Manager | Yes | Yes | Yes |
| Critic | Yes | Yes | Yes |
| Consistency Reviewer | Different sub-headings | Different sub-headings | Yes (embedded in different heading) |
| Fresh-eyes (r1) | Different structure | Different structure | Yes (different heading) |
| Fresh-eyes (r2) | Different structure | Different structure | Yes (different heading) |

The 5 agents created in DIP-005 (designer, skeptic, user-advocate, project-manager, critic) produce consistent self-evaluation structure. The consistency-reviewer and both fresh-eyes reports diverge, confirming that the earlier reference implementation established a pattern the later agents did not follow.

---

## Part 2: Dual-Consumption Assessment

### As human-readable documents

All 8 reports are genuinely readable. Key strengths:

**The findings are specific and citation-rich.** Every report references file paths, line numbers, section names, and exact text. The critic's finding about orphaned `fresh-eyes-reviewer` memory cites the exact directory. The consistency-reviewer's Issue #3 quotes the DIP-007 format alongside the actual implementation. This is excellent -- a human reader can verify any claim without searching.

**The severity/impact taxonomies work.** The critic uses Critical/Important/Minor. The designer uses Structural/Coupling/Minor. The skeptic uses Justified/Overcomplicated/Premature/Unnecessary. The user-advocate uses Blocking/Friction/Minor. The project-manager uses Blocking/Risk/Advisory. Each taxonomy is internally consistent and intuitive within its domain. A human reader quickly calibrates what each level means for that agent's perspective.

**The "what earns its complexity" / "what's well-planned" / "strengths" sections are substantive, not diplomatic.** No agent fills these with filler. The skeptic's "What Earns Its Complexity" section names 7 specific things with reasons. The critic's "Strengths" section explains why the progressive loading architecture works. These sections make the reports useful for understanding what to preserve, not just what to fix.

**One human-readability weakness:** The consistency-reviewer report is 225 lines including 20 "Verified Consistencies" entries. The verified-correct items outnumber the issues 20 to 7. For a human trying to find what needs attention, the extensive "no problems here" list dilutes the signal. The verified items are useful for completeness but could be collapsed into a summary count with an expandable detail section.

### As input for lead review synthesis

This is where the reports have more significant issues.

**Problem 1: No common severity scale.** The lead reviewer synthesizing across all reports must mentally translate between 5 different severity taxonomies. The critic's "Critical" and the user-advocate's "Blocking" may or may not mean the same thing. The designer's "Structural" is a type label, not a severity level. The skeptic's "Overcomplicated" is a verdict, not a severity. A synthesis agent reading all reports simultaneously would need to infer a unified severity mapping before it could produce "areas of agreement."

**Problem for AI:** A synthesis model receiving these 8 reports as input would likely default to treating the most alarming-sounding labels as highest priority, which may not reflect actual severity. The critic's "Critical -- orphaned memory directory" sounds more urgent than the user-advocate's "Blocking -- /agents command does not exist," but the user-advocate's finding has higher practical impact for an actual user.

**Problem for humans:** A human synthesizer can calibrate across taxonomies but it requires re-reading each report's category definitions (which are implicit, not stated).

**Suggested fix:** This is a systemic issue with the agent prompt design, not with individual reports. Two approaches:
- (a) Standardize severity levels across all agents: use a single 3-level scale (Blocks progress / Degrades quality / Cosmetic) and let agents add their domain-specific label alongside it (e.g., "Blocks progress (Structural)").
- (b) Keep domain-specific taxonomies but require each agent to include a priority rank ordering of their own findings. This lets the synthesis agent compare each agent's highest-priority item without cross-taxonomy translation.

**Problem 2: Inconsistent finding structure makes automated extraction fragile.** Consider what a synthesis agent needs from each finding: (1) what the problem is, (2) where it is, (3) how severe it is, (4) what the fix is. The 5 DIP-005 agents provide this in consistent sub-headings (Location/Problem/Impact/Suggested fix or equivalent). The consistency-reviewer uses a flat list with inline structure. The fresh-eyes reports use numbered paragraphs with "Why it matters" embedded. Extracting the same four fields requires different parsing strategies for different reports.

**Problem for AI:** A synthesis agent processing all 8 reports simultaneously would need to handle three different structural patterns. This is within an LLM's capability but increases the chance of missed findings -- the model is more likely to extract all findings from well-structured reports (critic, designer) and skim the less-structured ones (consistency-reviewer, fresh-eyes).

**Problem for humans:** A human doing synthesis can handle format variation. This is primarily an AI-parsing concern.

**Suggested fix:** The consistency-reviewer's Output Format is the documented outlier (Issue #1 in its own report -- it flagged itself). Aligning it to use the same sub-heading structure as the other 7 would eliminate the largest format gap. The fresh-eyes reports are from a prototype agent that predates the roster, so they are a historical artifact, not an ongoing concern.

**Problem 3: Cross-references between reports are absent.** Multiple agents found the same issues independently. The critic flagged the "elephants" problem in agent files (Issue 5). The skeptic indirectly touches the same concern when noting agents have "overlapping mandates" and naming each other. The project-manager catalogs it as "Prompt Engineer item 1." But no report references another report's findings.

In the current mode (Mode 3 collaborative team), agents could have used SendMessage to coordinate. None did. Each report is a self-contained document with no awareness of what other agents found.

**Problem for AI:** A synthesis model must independently discover that three agents are talking about the same issue. This is detectable through semantic similarity, but explicit cross-references (e.g., "Consistent with the critic's finding on negative scope framing") would make synthesis faster and more reliable.

**Problem for humans:** Same issue -- a human synthesizer must hold all reports in working memory to notice convergence.

**Suggested fix:** This is likely not worth adding to agent prompts -- it would require agents to read each other's reports before writing their own, which changes the independence guarantee. Instead, the lead review synthesis step should explicitly include a "convergence detection" pass: scan all findings for overlapping topics and group them. This is a synthesis instruction, not an agent instruction.

---

## Part 3: Individual Report Prompt Quality Notes

### Designer report -- strongest dual-consumption quality

The designer's report is the best-structured for both audiences. Every finding has a clear impact label, component references, and a concrete recommendation. The "What Composes Well" section names 5 specific architectural strengths with explanations of *why* they compose well, not just *that* they do. The "Instructions Received" section is detailed and useful for verification. The self-evaluation includes a specific, actionable prompt improvement suggestion (framework for assessing tier boundaries).

**One issue:** The Impact labels (Structural, Coupling, Minor) are type labels, not severity levels. "Structural" could mean "this is a fundamental problem" or "this is in the structural domain." The report uses it both ways. For the designer's own report this is readable; for synthesis it is ambiguous.

### Skeptic report -- the "Bottom Line" section is excellent synthesis input

The skeptic's "Bottom Line" section ("the system is about 60% well-justified and 40% premature optimization") followed by "if I could cut one thing / two things" and "what I would NOT cut" is the single most synthesis-friendly structure across all reports. A lead reviewer can read those 4 sentences and immediately understand the skeptic's position. Every other agent would benefit from a similar bottom-line summary.

**One issue:** The skeptic presents the agent count challenge as "8 agents where 4-5 would suffice" but the overlapping-mandates argument is partially contradicted by the project-manager's observation that "the agents produce structured, differentiated output" and "the prompt engineer found prompt-quality issues, the consistency reviewer found cross-reference errors, the fresh-eyes reviewer found spec-to-design semantic drift." The skeptic's theoretical argument for merging meets the PM's empirical observation that differentiation works. Neither report acknowledges the other's position. This is exactly the kind of tension a lead review should surface.

### User-advocate report -- strongest actionability

The user-advocate's findings are the most immediately actionable. The `/agents` command dead reference (Issue 1) is a concrete bug with a concrete fix. The "how do I actually dispatch an agent?" gap (Issues 2-3) is specific enough that someone could fix it in minutes. This report delivers the highest "fix per minute of reading" ratio.

**One issue:** The user-advocate may have over-indexed on new-user experience. All findings assume a user encountering the system for the first time. For a solo developer who built the system (the current user), none of the friction points are actual friction -- they know what `/agents` means, they know how to dispatch. The report would be stronger if it distinguished between "problems for the framework author" and "problems for a future user of the framework."

### Project-manager report -- the open-items catalog is high-value infrastructure

The PM's enumeration of 15 unfixed review items with categories (Fixed / Not fixed) is the most useful artifact for planning next steps. No other report attempts this. The dependency map is clean and the critical path is clearly stated.

**One issue:** The PM report is the least adversarial. Every finding is "Advisory" -- none are "Blocking" or "Risk" that would stop work. This may be appropriate (the system is functional), but it raises a calibration question: is the PM being appropriately pragmatic, or is the "(student)" label in its prompt biasing it toward over-encouragement? The PM's own self-evaluation acknowledges uncertainty about single-session delivery risk calibration, which is honest.

### Critic report -- strongest adversarial value

The critic's "verification is performative, not real" finding (Issue 2) is the most intellectually challenging finding across all reports. It traces the data flow of the "Instructions Received" verification claim and demonstrates that the mechanism cannot deliver what the spec promises. This is the kind of finding that requires understanding both the system's claims AND the platform's mechanics.

**One issue:** The critic rates 2 findings as "Critical" -- the orphaned memory directory and the performative verification. These have very different practical impacts. The orphaned directory is a simple cleanup task (5 minutes). The verification claim is a design philosophy issue that affects how the entire reporting system is documented and trusted. Using the same "Critical" label for both makes it hard for a synthesis agent to distinguish "fix this now" from "rethink this claim."

### Consistency-reviewer report -- thoroughness vs. signal density tradeoff

The 20 "Verified Consistencies" entries are valuable for audit completeness. They prove the reviewer checked specific things and found them correct. But they account for roughly 60% of the report's length while conveying the information "these 20 things are fine." The 7 actual issues (40% of length) carry 100% of the actionable content.

**One issue:** The consistency-reviewer's self-evaluation ends with "I am the inconsistency I was hired to find" -- a candid acknowledgment that its own Output Format diverges from the pattern it's checking others against. This is simultaneously the report's most honest moment and an indicator of a prompt engineering gap: the consistency-reviewer's prompt was written before the 7-agent pattern was established, so it could not instruct itself to follow a pattern that didn't exist yet.

### Fresh-eyes reports -- strongest evidence-based argumentation

Both fresh-eyes reports cite specific text from both documents on each side of every inconsistency. The "Why it matters" framing consistently grounds findings in implementation impact rather than abstract correctness. Round 2's correction of round 1's errors (Issues 5 and 6 were wrong, explicitly acknowledged) demonstrates calibration and intellectual honesty.

**One issue:** These reports are from a prototype agent that predates the roster. They don't follow the SPEC-005 output template. For synthesis, they are the hardest to integrate because their structure has no predictable mapping to the standard fields.

---

## Part 4: Systemic Prompt Engineering Observations

### What the reports reveal about the agent prompts

1. **The Output Format templates are working.** The 5 DIP-005 agents produce structurally consistent reports. The format guidance is effective as a prompt. This is a success.

2. **"If the work is solid, say so" is working.** Every agent includes substantive positive sections. No agent manufactures criticism. The Critical Rules guardrail is effective.

3. **"Instructions Received" is not working.** Only 2 of 8 agents include it, because the agent Output Format sections do not instruct it. The session report template defines it, but agents follow their own prompt, not the template. Fix: add "Include the instructions/context you received" to each agent's Output Format section.

4. **Self-evaluation quality varies by specificity.** Agents whose self-evaluations name specific situations ("I struggled with calibrating between bootstrapping artifact and real problem") are more useful than those with generic observations ("I could have been more systematic"). The prompt improvement suggestions are most useful when they propose a concrete addition ("a framework for assessing tier boundaries") rather than a vague direction ("more calibration guidance").

5. **Domain-specific severity labels are good for individual reports but bad for synthesis.** Each agent's taxonomy is internally calibrated. The problem is cross-agent comparison. This is a design tension with no clean resolution -- standardizing kills domain-specific nuance; keeping domain-specific kills synthesis parsability.

### Recommendation for the synthesis step

Rather than changing agent prompts to standardize findings format (which would reduce the domain-specific quality), add synthesis instructions to the lead review process:

- **Step 1: Extract** -- For each report, list findings with: topic, agent's severity label, agent's recommended fix.
- **Step 2: Deduplicate** -- Group findings that address the same underlying issue across multiple reports. Note which agents converge.
- **Step 3: Calibrate** -- For each group, assess practical impact independent of the agent's label. A critic's "Minor" and a user-advocate's "Blocking" on the same topic need to be reconciled.
- **Step 4: Synthesize** -- Present grouped findings with the unified severity and all agents' perspectives.

This keeps agent prompts optimized for their own domain while adding a synthesis layer that handles cross-domain translation.

---

## Self-Evaluation

- **What worked well:** Reading all 8 reports in sequence, comparing structure before content, revealed the systemic patterns (severity taxonomy divergence, missing Instructions Received, cross-reference absence) that would be invisible from any single report. The tabular analysis of metadata fields and self-evaluation structure made the consistency gaps concrete rather than impressionistic.

- **What I struggled with:** Separating "this report has a prompt engineering problem" from "this report's agent found different things than I expected." The skeptic's argument for fewer agents is substantive, but I kept wanting to evaluate it as a content claim rather than assessing the report's structural quality as a synthesis input. My prompt engineer role is about the prompt quality of the output, not the correctness of the findings. I drifted into content evaluation multiple times, especially on the critic's verification finding.

- **Prompt improvement suggestions:** My agent prompt should include explicit guidance on what "evaluate as synthesis input" means -- specifically, that I should assess whether findings are extractable, comparable, and groupable across reports, not whether they are correct. A checklist like "Can a synthesis agent extract: topic, location, severity, fix? Are these in consistent positions across reports?" would keep me focused on structural quality rather than content agreement.
