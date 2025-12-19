# ADR-005: PLANNING.md for State Persistence and Session Recovery

**Date:** 2025-12-19
**Status:** Accepted
**Deciders:** Framework User, Framework Architect
**Tags:** state-management, context-persistence, session-recovery, planning

## Context

Claude Code commands gather significant information from users through guided questionnaires (spec details, design decisions, requirements, etc.). This information needs to be:
1. Retained during command execution to generate outputs
2. Available for session recovery if context window closes/compacts
3. Traceable for audit and debugging purposes

Initial command designs used a "Store as: `VARIABLE_NAME`" pattern, treating Claude's context window as implicit storage. This has limitations:
- Context window can close accidentally (terminal crash, user closes window)
- Auto-compaction can lose gathered information
- No persistence between sessions
- No audit trail of what was gathered
- CLAUDE.md becomes cluttered with dynamic state if we try to persist there

Previous framework versions (Bootstrap) used a PLANNING.md file successfully for similar purposes.

## Decision

**Use a root-level `PLANNING.md` file for active session state, with automatic archival to `.plans/archive/`.**

**File location:** `PLANNING.md` (root directory, visible and accessible)

**Archive location:** `.plans/archive/PLANNING-[YYYY-MM-DD-HHMMSS].md`

**Archival triggers:**
1. End of a task/command completion
2. Start of a new user session (detected by new conversation)
3. Explicit user request

**Philosophy:**
- Records and trails, not polished outputs
- Trains of thought for both user and agent
- Duplication is acceptable (storage cheap, compute expensive)
- Don't over-invest in formatting or "living document" maintenance
- Capture efficiently, not prettily

## Rationale

**Context persistence:**
Unlike conversation context which can be lost, PLANNING.md survives terminal crashes, accidental closes, and auto-compaction. A new session can read it and resume.

**Reduces CLAUDE.md churn:**
CLAUDE.md should contain stable framework guidance and project identity. Dynamic state (current task, gathered parameters, recent decisions) belongs in PLANNING.md. This keeps CLAUDE.md predictable.

**Explicit state vs. implicit memory:**
"Store as: `VARIABLE_NAME`" relies on Claude remembering things in context. Writing to PLANNING.md makes state explicit and verifiable. If something seems wrong, both user and agent can check the file.

**Audit trail:**
Archived PLANNING files create a history of framework usage. Useful for:
- Debugging ("what did I tell Claude last session?")
- Learning patterns ("how did I approach similar specs before?")
- Future features (analytics, pattern detection)

**Token cost trade-off:**
Reading PLANNING.md consumes tokens, but it's a worthwhile trade-off for reliability. A lost context window wastes far more tokens (re-gathering all information) than reading a state file.

**Cheap storage, expensive compute:**
Archiving every session creates files, but storage is cheap. Re-running entire questionnaires because state was lost is expensive (user time + API tokens).

## Alternatives Considered

### Alternative 1: Keep State in Context Only

**Description:** Rely on Claude's context window to remember gathered information.

**Pros:**
- No file I/O
- Simpler implementation
- No cleanup needed

**Cons:**
- Lost on context close/compaction
- No persistence between sessions
- No audit trail
- No way to verify what Claude "knows"

**Why not chosen:** Too fragile. Context loss wastes significant user time and tokens.

### Alternative 2: Store State in CLAUDE.md

**Description:** Add a "Current State" section to CLAUDE.md that updates dynamically.

**Pros:**
- Single file for Claude to reference
- Already being read by Claude

**Cons:**
- Clutters CLAUDE.md with dynamic state
- Frequent edits to a governance document
- Harder to parse stable config vs. transient state
- Mixing concerns (identity/guidance vs. session state)

**Why not chosen:** CLAUDE.md should be stable. Dynamic state deserves its own file.

### Alternative 3: Hidden State File (.planning or .state.json)

**Description:** Use a dotfile for state, keeping it hidden from normal view.

**Pros:**
- Less visible clutter
- Could use structured format (JSON)

**Cons:**
- Hidden from user (harder to debug)
- JSON less human-readable than markdown
- Dotfile convention implies "system" not "working document"

**Why not chosen:** PLANNING.md should be visible and human-readable. It's a working document, not system infrastructure.

### Alternative 4: Per-Command Temp Files

**Description:** Each command creates its own temp file (e.g., `.spec-session.md`), cleaned up after.

**Pros:**
- Isolated per command
- No single file growing large

**Cons:**
- Multiple files to track
- Cross-command context lost
- More complex archival
- No unified view of session state

**Why not chosen:** Unified PLANNING.md provides full session context. Commands often build on each other (spec → architect → breakdown).

## Consequences

### Positive Consequences

- **Session recovery:** New conversations can resume from PLANNING.md
- **Explicit state:** Both user and agent can verify gathered information
- **Audit trail:** Archived files track framework usage history
- **Stable CLAUDE.md:** Dynamic state doesn't clutter guidance document
- **Debugging:** "What did I tell Claude?" is answerable
- **Reliability:** State survives context loss

### Negative Consequences

- **Token cost:** Reading PLANNING.md uses tokens (acceptable trade-off)
- **File management:** Need to archive periodically (automated by commands)
- **Storage growth:** Archives accumulate (cheap, can prune later)

### Neutral Consequences

- **Visible in project:** PLANNING.md is visible in root (intentional - it's a working document)
- **Duplication:** Some content duplicated between PLANNING.md and final outputs (acceptable per philosophy)

## Implementation Notes

**PLANNING.md Structure:**
```markdown
# Planning

## Session Context
- **Started:** [timestamp]
- **Current Task:** [description]
- **Active Command:** [/spec, /architect, etc.]

## Active Artifacts
- **Spec:** SPEC-003 User Authentication
- **Design:** (none yet)

## Gathered State
[Command-specific state, e.g., for /spec:]
### Spec Parameters
- Title: User Authentication
- Problem: Users cannot securely...
- Requirements:
  - REQ-F1: System shall...

## Decisions Made
- [timestamp] Chose OAuth2 over session auth
- [timestamp] Selected PostgreSQL

## Next Steps
- [ ] Review generated spec
- [ ] Run /architect to create design
```

**Command Integration:**
1. **On command start:** Read PLANNING.md, check for prior state
2. **During execution:** Update PLANNING.md as information gathered
3. **On command end:** Update with results, suggest next steps
4. **On new session:** Archive existing PLANNING.md, start fresh

**Archival:**
```bash
# Archive pattern
mv PLANNING.md .plans/archive/PLANNING-2025-12-19-143022.md

# Create fresh PLANNING.md
[command initializes new file]
```

**`.plans/archive/` directory:**
- Created automatically when first archive occurs
- Can be .gitignored if user prefers (suggested, not enforced)
- Retained indefinitely (cheap storage)

## References

- Bootstrap Framework: PLANNING.md predecessor concept
- ADR-004: Framework Directory Structure (archive location in .plans/)
- CLAUDE.md: Should reference PLANNING.md for dynamic state

---

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2025-12-19 | Initial version | Framework Architect |
