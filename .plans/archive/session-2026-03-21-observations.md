# Session Observations: 2026-03-21

## Plugin Evaluation & Integration Decisions

- Evaluated superpowers (14 skills), commit-commands (3 commands), skill-creator (1 skill + 3 agents)
- Superpowers concepts absorbed into /build design rather than creating separate skills
- Superpowers plugin can be uninstalled after post-MVP skill creation is complete
- commit-commands stays as orthogonal utility

## Future Enhancements Identified

### Context-Aware Reading (All Commands)
**Observation:** When executing DIP-002, the DIP's Required Reading listed 30+ items already in context from earlier in the session. Reading them again would waste tokens and time.
**Fix applied:** Added context-aware reading to `/build` command (skip docs already in context, read fresh in new sessions).
**Remaining work:** Apply the same pattern to all other commands (`/spec`, `/architect`, `/define`, `/deliver`, `/charter`, `/breakdown`). Each command reads PLANNING.md and referenced docs — they should all skip re-reading when in context.

### Command-to-Skill Migration
**Decision:** All commands will migrate to skills with `disable-model-invocation: true` post-MVP. Benefits: template co-location, lazy loading, `allowed-tools` frontmatter, future-proofing against command deprecation.
**Priority:** After end-to-end testing validates the commands work correctly.

### Three New Standalone Skills (Post-MVP)
1. **test-driven-development** — RED-GREEN-REFACTOR enforcement (from superpowers)
2. **systematic-debugging** — 4-phase root cause investigation (from superpowers)
3. **verification-before-completion** — evidence-before-assertions gate (from superpowers)

These are auto-invocable skills for software projects, not workflow commands.

### DIP Template Improvements
- Required Reading section could have a "same-session" indicator to help agents decide whether to re-read
- Step verification format (Input/Output/Verify) maps well to the build command — no changes needed
- The DIP template's TodoWrite boilerplate is verbose — could be simplified

### /deliver Enhancements
- Multiple style variants (academic, report, memo) — add to `.praxisity/styles/` when needed
- Citation/bibliography support
- Image embedding
- Batch generation
- The test_generate.py markdown parser could become a shared utility if PDF generation is needed outside the /deliver command

### Housekeeping
- `.praxisity/templates/pandoc/` directory is deprecated (replaced by ReportLab approach) — can be removed
- `.plans/references/` directory was created for external reference docs — consider documenting this in the foundation plan

## Attribution
Key concepts in /build and /deliver were influenced by:
- **superpowers plugin** (obra/superpowers, MIT license) — executing-plans, verification-before-completion, systematic-debugging patterns
- **commit-commands plugin** (Anthropic) — git safety patterns
- **IEEE Editorial Style Manual** — visual reference for clean document formatting
- **ReportLab scoping report** — environment capabilities analysis from earlier Claude.ai session