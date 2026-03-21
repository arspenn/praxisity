---
description: Execute a DIP (Detailed Implementation Prompt) with step verification and git safety
tags: [execution, dip, build, git-safety]
---

# Build Command

Execute a DIP with sequential step verification, git safety, and state tracking.

## Constraints

- Follow DIP instructions precisely — do not improvise or add unrequested work
- When a step fails or is unclear, halt and ask — never guess or retry automatically
- Verify each step before proceeding to the next
- For verification: run commands automatically when possible, ask user for manual confirmation when subjective
- Keep git operations safe — no blanket adds, no secrets, scope-limited commits
- Track progress via TodoWrite throughout execution

## Pre-Flight

1. Read PLANNING.md for session context
2. Update PLANNING.md with /build as active command
3. Check PLANNING.md for previous halted `/build` execution:
   - If found: show the DIP ID, halted step number, and halt reason
   - Ask user: resume from that point, start fresh, or select a different DIP
   - User arguments override detected state
4. If no resume: check `.plans/prompts/` for available DIPs
   - If argument provided, use it as DIP path
   - Otherwise list available DIPs and prompt for selection
5. Check `git status`:
   - If working tree is dirty, warn user and list uncommitted changes
   - Require explicit approval to proceed with dirty state
6. Check if the DIP's required reading documents (spec, design, charter) are already in the current context:
   - If you created or read these documents earlier in this session, skip re-reading them
   - If this is a new session or you haven't seen them, read each document listed in the DIP's Required Reading section
   - When in doubt, read them — redundant reading is cheaper than missing context
7. Read the selected DIP file and extract:
   - Objective
   - Implementation steps (### Step N sections) with their Verify blocks
   - Acceptance criteria table
   - Scope boundaries (DO/DO NOT, files in/out of scope)
   - Commit instructions
8. Display objective and step summary to user
9. Create TodoWrite entries for each step

## Execution

For each implementation step in the DIP, in order:

1. Mark step as `in_progress` in TodoWrite
2. Show step title and instructions to user
3. Execute the step's instructions
4. Run verification:
   - If verification looks like a shell command or file check: run it, check the result
   - If verification is descriptive or subjective: present it to the user and ask "Pass or fail?"
   - If uncertain whether automatable: ask the user rather than guessing
5. On verification **pass**: mark step `completed` in TodoWrite, show progress (e.g., "Step 2/4 complete"), continue
6. On verification **fail**:
   - Stop execution immediately
   - Report: which step failed, what the verification was, what the result was
   - Ask user how to proceed (fix and retry this step, skip, or abort)
   - Update PLANNING.md with halt state (DIP ID, step number, reason)
7. On **ambiguity** in instructions: stop and ask user for clarification

## Completion

After all steps pass:

1. **Verify acceptance criteria** from the DIP's AC table
   - For each criterion: run the test or ask user for manual confirmation (same duality as step verification)
   - Report results: which passed, which failed
   - If any fail: halt and ask user how to proceed

2. **Git safety checks** before committing:
   - Never use `git add .` or `git add -A`
   - Scan staged files for sensitive patterns (.env, credentials, keys, tokens, secrets)
   - Verify all staged files are within the DIP's "Files in Scope" list
   - If any check fails: warn user, show what was flagged, require approval

3. **Show diff** to user before committing (`git diff --staged`)

4. **Commit** using the DIP's Commit Instructions section:
   - Use the conventional commit format specified in the DIP
   - Include DIP ID and REQ IDs in the commit body
   - Stage only the specific files listed

5. **Update PLANNING.md**:
   - Record DIP completion status
   - Note any deviations or decisions made during execution
   - Suggest next action

6. **Todoist** (if DIP has a Todoist Task ID and MCP is available):
   - Mark the task complete via `mcp__todoist__complete-tasks`

## Success Message

Confirm execution complete. Show:
- DIP ID and objective accomplished
- Steps completed count
- Acceptance criteria results
- Commit hash
- Suggested next action from PLANNING.md

---

## Behavior Notes

- Each run executes ONE DIP — no multi-DIP batching
- Resume: detects halted state from PLANNING.md, suggests resume point, user confirms
- Verification duality: commands run automatically, subjective checks go to user
- Git safety: warns and requires approval, never hard-blocks
- PLANNING.md: reads on start, writes on completion or halt
- TodoWrite: tracks step progress within the session
- Domain-agnostic: works for software, research, or any DIP type


ARGUMENTS: $ARGUMENTS