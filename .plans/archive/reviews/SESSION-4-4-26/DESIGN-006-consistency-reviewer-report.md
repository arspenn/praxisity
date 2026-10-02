## Cross-Document Consistency Review

**Documents reviewed:**
- `/home/arspenn/Dev/praxisity/.plans/designs/006-gather-skill.md` (DESIGN-006, primary focus)
- `/home/arspenn/Dev/praxisity/.plans/specs/006-gather-skill.md` (SPEC-006)
- `/home/arspenn/Dev/praxisity/.claude/skills/gather/SKILL.md` (prototype)
- `/home/arspenn/Dev/praxisity/.plans/designs/005-command-rewrites.md` (DESIGN-005, parent)
- `/home/arspenn/Dev/praxisity/.plans/specs/004-command-fixes-and-patterns.md` (SPEC-004, parent)

**Status:** Issues Found

**Instructions Received:**
Review DESIGN-006 for cross-document consistency across 7 focus areas: requirement ID alignment with SPEC-006, match against the SKILL.md prototype, alignment with DESIGN-005 COMP-5/DEC-2/DEC-8, correct bug IDs, no stale "shared file" references, frontmatter field accuracy, and memory file format consistency.

---

### Issues

**Issue 1 (Critical): `when_to_use` is not a supported field, but SPEC-006 and DESIGN-005 still reference it**

DESIGN-006 COMP-3 explicitly states: "`when_to_use` is NOT a supported frontmatter field (IDE diagnostic confirmed). The `description` field is what the platform uses for context matching." The SKILL.md prototype confirms this -- it uses only `name` and `description` in its frontmatter, with no `when_to_use`.

However, the following upstream documents still reference `when_to_use` as if it were the mechanism:

- **SPEC-006, REQ-G6:** "The skill shall auto-invoke via `when_to_use`..."
- **SPEC-006, AC-G7:** "...auto-invokes via platform `when_to_use` matching..."
- **SPEC-006, Section 6.1 Dependencies:** "`when_to_use` skill frontmatter auto-invocation | Platform | Available"
- **SPEC-006, QG-2:** "How does `when_to_use` auto-invocation interact with..."
- **DESIGN-005, COMP-5:** "a standalone support skill with `when_to_use` triggering"
- **DESIGN-005, INT-1:** "Platform auto-invocation via `when_to_use` context matching"
- **DESIGN-005, DATA-2:** "YAML frontmatter: `name`, `description`, `when_to_use` for auto-invocation"

**Why it matters:** An implementer reading SPEC-006 or DESIGN-005 will try to add a `when_to_use` field, which does not exist. DESIGN-006 got it right, but the upstream documents are stale. SPEC-006 REQ-G6 should reference `description`-based auto-invocation. DESIGN-005 COMP-5, INT-1, and DATA-2 should be updated to match the finding.

---

**Issue 2 (Moderate): DESIGN-005 DATA-2 is missing two SKILL.md sections**

DESIGN-005 DATA-2 (Gather Support Skill schema) lists 5 sections: The Rule, How to Gather Each Section, When Drafting is Permitted, Handling Sub-Sections, Handling Skip Requests.

Both DESIGN-006 and the SKILL.md prototype include two additional sections:
- **Preferences** (the memory-as-settings section, COMP-2 in DESIGN-006)
- **Before You Send** (the pre-send verification checklist, part of COMP-1 in DESIGN-006)

DATA-2 also says "See SPEC-006 for full requirements including REQ-G8/G9 (memory-as-settings, Phase 2)" -- the "Phase 2" label suggests it was written when memory-as-settings was deferred, but it has since been promoted to the core design in DESIGN-006.

**Why it matters:** DATA-2 is the schema definition for the gather skill within the parent design. An implementer working from DESIGN-005 would produce a skill missing two sections. DESIGN-006 supersedes DATA-2 for the gather skill, but DATA-2 should either be updated or explicitly marked as superseded.

---

**Issue 3 (Low): SPEC-006 says QG-1 is Open, DESIGN-006 says Resolved**

SPEC-006 Open Questions table, QG-1: "What specific calibration questions should be asked on first run? | **Open** | Candidates: strictness level, user experience, verbosity, show examples."

DESIGN-006 Open Questions table, QG-1: "**Resolved** | DEC-G4: two fixed questions (gathering-style, prompt-detail)"

The design resolved this question with DEC-G4 (two fixed binary questions), and the SKILL.md prototype implements exactly those two questions. But the spec still shows it as open with different candidate questions (strictness level, user experience, verbosity, show examples) that don't match the final resolution.

**Why it matters:** Minor -- the design is authoritative post-spec. But if someone returns to the spec to check what was decided, the stale "Open" status and different candidate list will be confusing.

---

### Checks That Passed

- **REQ-G1 through REQ-G9 coverage:** All 9 requirements from SPEC-006 appear in DESIGN-006's Requirements Coverage table (Section 1.3). Every COMP satisfies clause traces back correctly to the right REQs. No requirement is missing from the design.
- **Bug IDs:** DESIGN-006 references BUG-012 and BUG-018 correctly. BUG-034 is explicitly excluded in the Out of Scope section. No incorrect bug references found.
- **No stale "shared file" or `gathering-standards.md` references in DESIGN-006:** The only mention of "shared files" is in the negative ("no dependencies on shared files"), which is correct. DESIGN-005 v0.5 revision history confirms stale references were cleaned up there.
- **Memory file format:** DESIGN-006 COMP-2 memory format (frontmatter with name/description/type + gathering-style + prompt-detail) matches the SKILL.md prototype exactly, character for character.
- **DESIGN-005 DEC-2 and DEC-8 alignment:** DEC-2 (inline mechanical, skill-based judgment) and DEC-8 (memory-as-settings pattern) are fully consistent with DESIGN-006's approach. No contradictions.
- **DESIGN-006 internal consistency:** The Requirements Coverage table, COMP satisfies clauses, DEC rationales, and testing strategy all cross-reference correctly within the document.
- **Frontmatter fields in DESIGN-006:** Section 2.2 correctly identifies `name`, `description`, `user-invocable` (default true), and `disable-model-invocation` (default false) as the relevant fields. No fabricated fields.

---

### Recommendations (advisory, do not block approval)

1. **SPEC-006 should be updated** to replace `when_to_use` with `description`-based auto-invocation in REQ-G6, AC-G7, Section 6.1, and QG-2. This is upstream of DESIGN-006 and would bring the spec in line with the design's confirmed finding.

2. **SPEC-006 QG-1** should be marked Resolved with a reference to DEC-G4.

3. **DESIGN-005 DATA-2** should either be updated to include the Preferences and Before You Send sections, or annotated as "superseded by DESIGN-006 for gather skill schema."

4. **AC priority alignment (minor):** SPEC-006 AC-G6 (validates REQ-G5, SHOULD priority) and AC-G8 (validates REQ-G7, SHOULD priority) use mandatory phrasing. This is a known pattern (feedback_common_inconsistency_types #1) but unlikely to cause implementation issues here since both are behavioral expectations, not pass/fail gates.

---

## Self-Evaluation

- **Most frequent inconsistency type:** Stale field name (`when_to_use`) propagated across multiple documents after a finding in a downstream document (DESIGN-006) invalidated it. This is a "discovery flows downstream but correction doesn't propagate upstream" pattern.
- **Unable to assess:** Whether `description`-based auto-invocation actually works as DESIGN-006 claims -- this is an empirical platform behavior question, not a document consistency question.
- **Document structure quality:** Cross-referencing was straightforward. DESIGN-006 is well-structured with clear COMP-to-REQ mapping. The Open Questions table appearing in both SPEC-006 and DESIGN-006 (with status tracking) made it easy to spot the QG-1 divergence. The weakest cross-reference point was DESIGN-005 DATA-2, which is a schema definition for an artifact now fully owned by DESIGN-006.
- **Prompt improvement suggestions:** The focus areas provided in the task instructions were precise and well-targeted -- they directed attention to the exact inconsistencies that existed. For future reviews, including explicit "check for upstream propagation of downstream findings" as a standard focus area would generalize Issue 1 into a reusable check pattern.