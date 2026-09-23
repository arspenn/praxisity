## Critic Review: /design skill (clone of the describe pattern)

**Artifact:** `.claude/skills/design/SKILL.md`, `templates/design.template.md`; pattern `.claude/skills/describe/SKILL.md`; protocol `.claude/skills/gather/SKILL.md`; prototype `.claude/commands/architect.md`; example output DESIGN-004
**Date:** 2026-09-22 | **Dispatch Mode:** Mode 1 (team-lead consult) | **Reviewer:** critic

## Instructions Received

Review the new /design skill against the describe pattern, with attention to pre-flight steps 4 and 5, the coverage gate and its escapes, the update flow's spec diff, global design numbering, the Specification References link, and anything wrongly dropped from the old command.

## Findings

### High — `NNN` means two different numbers in the template, and the substitution rule replaces it globally
**Location:** Template line 24 (`DESIGN-NNN`), line 40 (`[SPEC-NNN](../specs/NNN-slug.md)`), line 313 (References); Generate 4 ("replace `[bracketed placeholders]` and `NNN`").
**Problem:** The design's own number and the spec's number share one placeholder. Design and spec numbering are independent by design (SPEC-005 is implemented by DESIGN-004 in this repo, and alternatives per spec guarantee divergence), so the two numbers differ in the normal case. A literal application of the substitution rule writes the design number into the spec link.
**Impact:** Broken spec link and wrong Spec ID in the one table that ties the design to its requirements.
**Fix:** Use `MMM` for the spec number in the template, matching the commit message's `SPEC-MMM`, and say in Generate 4 that `NNN` is the design number and `MMM` the spec number.

### Medium — Bare-number arguments are ambiguous between spec and design, and this repo already has a collision
**Location:** Pre-Flight 4 ("`DESIGN-004` or bare `004`"); argument-hint.
**Problem:** The argument may name a spec to design for or a design to revise. A bare `005` is read as DESIGN-005 (which exists here, command-rewrites) when the user likely meant SPEC-005 (agent-consultation). Independent numbering makes this collision routine, not rare.
**Fix:** Bare numbers are not accepted as design IDs in this skill; require the `DESIGN-` prefix to revise. A bare number is tried as a spec number, and if both a spec and a design carry it, ask once.

### Medium — Coverage counts interfaces and data entities, but only components can declare Satisfies
**Location:** Rules bullet 4; template 1.3 example row (`COMP-1, INT-1`); Gather Coverage row ("from every element's Satisfies list"); INT and DATA blocks (no Satisfies field); 7.4 Non-Functional Approach.
**Problem:** The matrix is built from Satisfies lists, and only COMP blocks have one, so INT-1 can never appear in it despite the rule and the example. Separately, 7.4 has "one row per REQ-N" but a MUST REQ-N satisfied only there has no element and trips the gate. The template comment for 1.3 ("a gap in the design, not a detail to fill in later") also forbids the deliberate-gap escape the skill allows.
**Fix:** Add a Satisfies field to INT and DATA blocks, or restrict coverage to components and fix the example. State that 7.4 does not count toward coverage. Add the DQ escape to the 1.3 comment.

### Medium — Step 5's "revise it" answer has no path, and "a design already exists for this spec" has no detection mechanism
**Location:** Pre-Flight 5, last sentence.
**Problem:** Step 4 has already committed to "new" and taken a number by the time step 5 discovers a prior design; choosing "revise it" needs step 4's revise path (read the design, then run the update flow), which the sequential rule says is finished. Also, `ls .plans/designs/` does not reveal which spec a design implements; here DESIGN-004 and SPEC-005 share a slug by coincidence, not rule.
**Fix:** "Search `.plans/designs/` for `SPEC-MMM` to find prior designs. If the user chooses revise, drop the reserved number and continue as step 4's revise path with that design." Also add "Alternative to" to the Related Documents relationships so a sibling design can cite the first.

### Medium — Escape (c) "revise the spec" is a cancel the skill cannot perform
**Location:** Rules bullet 4; Review and Confirm.
**Problem:** /describe is `disable-model-invocation: true`, so "revise the spec" means the user leaves this run. Nothing sets PLANNING.md to `cancelled` for that exit; the same class of gap as describe's charter branch, which was fixed there.
**Fix:** "If the user chooses to revise the spec, set Status `cancelled`, stop, and tell them to run /describe then /design again."

### Medium — Spec diff leaves the fate of a component whose requirement was struck undefined
**Location:** Update flow, spec-diff sentence.
**Problem:** Three cases are unaddressed: (a) a COMP whose only Satisfies entry is now a struck REQ; (b) whether a struck MUST still counts in the matrix's "covered out of total"; (c) "changed" is undetectable from the design side, since the design holds only IDs with labels. Describe now names changed IDs in its Revision History rows, which is the signal to use.
**Fix:** "Struck spec requirements drop out of the MUST total and are struck in the matrix. Walk every element whose Satisfies cites a struck or changed ID; if nothing remains, ask whether to strike it or re-map it. Detect changes from the spec's Revision History rows dated after the design's Last Updated."

### Low — Held spec state across a long gather
**Location:** Pre-Flight 5 ("hold its requirements"); Gather Coverage row.
**Fix:** Re-read the spec's requirements tables immediately before building the coverage matrix, the same safeguard describe uses before its cp.

### Low — Struck header-only block is not a permitted generate operation
**Location:** Generate 4 vs update flow's "keeps its block header ... struck through."
**Fix:** Add "struck block: a header-only block for a removed element" to Row and block adjustment.

### Low — "PLANNING.md names an active spec" is not in the contract
The contract has no such field; the only place a spec appears is Next Steps. Say "if Next Steps names a spec file."

### Dropped from the old command
Nothing that should return. Domain-specific architecture questions moved into the template's 2.1–2.3 comment with four fields, an improvement. Warn-not-block became block-with-escapes, acceptable once escape (c) is fixed. Multiple designs per spec survives as "alternative alongside" but needs the relationship type above.

## Unstated Assumptions
- Every design cites exactly one spec; the Specification References table allows more, and step 4's "read the spec it references" assumes one.
- Spec and design Last Updated dates are comparable at day granularity; a same-day spec revision is invisible to the diff.
- Working directory is the project root, so `../specs/` resolves.

## Ranked Top 5
1. Split `NNN` into design `NNN` and spec `MMM` in the template and Generate 4.
2. Require the `DESIGN-` prefix to revise; treat bare numbers as spec numbers with an ask on collision.
3. Give INT and DATA a Satisfies field or restrict coverage to components; align the 1.3 comment with the DQ escape.
4. Route step 5's "revise it" and escape (c) to defined paths with PLANNING.md reset.
5. Define struck-requirement handling in the spec diff.

## Strengths
Every describe Round 2 fix carried forward: IDs on approval with "highest ever plus one," struck rows noted before the cp, Status kept, Revision History naming IDs, author gathered with Title, save withheld at Review. Showing remaining uncovered MUSTs after each component is the best pedagogical move in any of the three skills. The template's four-field examples for Architecture, Interfaces, and Validation are concrete enough to scaffold a newcomer, and the DATA retention nudge is the right place for it.

## Self-Evaluation
- **What worked well:** Checking both directories for a shared number turned the bare-number rule from hypothetical into a live collision.
- **What you struggled with:** Cannot exercise the spec diff against a real revised spec; that finding is reasoned, not observed.
- **Prompt improvement suggestions:** Add "when two documents share a placeholder token, check that substitution can tell them apart" to my checklist.

---

## Round 2 — 2026-09-23 (delta pass on the revision and the reference convention)

### Resolved
All eight named items: `MMM` for the spec in the template and Generate 4; `DESIGN-` prefix required to revise with bare numbers meaning specs; Satisfies on INT and DATA with "N/A if purely structural"; 1.3 and 7.4 comments carry design-wide and deliberate-gap; step 5 greps designs for the spec ID and routes "revise" to the update flow with "Alternative to" added; the coverage escape is now an explicit cancel naming /describe; the spec diff reads the spec's Revision History rows and asks remove-or-re-home for any element whose Satisfies empties; struck headers are a generate operation; the spec is re-read before the matrix; "Next Steps names a spec" replaces the invented field. Two small residues: the Revision History date test is "after," so a spec revised the same day as the design is missed (say "on or after, not already reflected"); and an element whose Satisfies still cites a struck requirement alongside live ones is never told to write it in the struck form.

### Convention edge cases
- **Medium — Two specs per design has a convention form but no skill path.** The Specification References table takes rows, and the convention says qualify (`SPEC-003 REQ-F2`), but step 5 selects one spec, `MMM` is one number, step 4 reads "the spec" singular, the commit message names one, and the MUST total comes from one spec. **Fix:** state the policy: one spec per design; a design that needs two is a sign to merge the specs or split the design. /plan faces the same question with a DIP citing one design.
- **Medium — Charter section references have no agreed form.** The charter has no numbered sections. The charter template's convention allows `§Scope` (name); the spec and design versions allow only "number, title." And no form combines a document link with a section, which is exactly what the spec's Charter Reference row and 6.1 Inherited need on the first /describe run. **Fix:** unify the section form as "§ plus the number if the section has one, otherwise the heading," and add a fifth form: a section in another document is the document link followed by the section, `[CHARTER.md](../../CHARTER.md) §Scope`.
- **Medium — "First mention in a section" is neither decidable nor what the template does.** "Section" granularity is undefined (H2, H3, or block). The template labels `REQ-F1 (short label)` in every COMP block's Satisfies, which is correct for blocks a DIP will excerpt but violates first-mention-per-section, and the matrix's `COMP-1, INT-1` column is bare on first mention. Row-by-row Edit cannot reliably track prior mentions across a section. **Fix:** replace the rule with two: cross-document IDs always carry the label in structured fields (Satisfies, matrix rows, table cells) and on first mention per H2 in prose; same-document IDs never need one.
- **Low-Medium — A struck design element cited by a DIP.** The header survives, so the citation resolves, but nothing tells the DIP. Describe searches designs and prompts before removing a requirement; design does not search prompts. **Fix:** search `.plans/prompts/` for the ID and name the citing DIPs in the Revision History row, giving /plan the same signal design takes from the spec.
- **Low — Convention text drifts across the three templates** (different orderings, the charter omits the removed form, the spec's `§8 Out of Scope` example). Keep one canonical block in praxisity-patterns.md and paste it verbatim. Also, References line 337 uses `[SPEC-MMM: Specification title]` while the convention says the link text is the ID alone.
- **Low — Struck header form.** The skill strikes the title, the convention strikes the ID. Pick `### ~~COMP-3: Title~~ (removed v0.2)`.

### Round 2 verdict
The skill is clean; every Round 1 finding is closed. The remaining work is in the convention, which is shared by all templates and should be settled before /plan clones it: one-spec-per-design policy, a document-plus-section form, and a decidable labeling rule.
