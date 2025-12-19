# ADR-002: Git History Reset in /new-project Command

**Date:** 2025-12-18
**Status:** Accepted
**Deciders:** Framework Architect
**Tags:** git, new-project, initialization, user-experience

## Context

When users run `/new-project` to initialize a new project from the Praxisity framework, they start with a cloned repository containing all the framework's development history. We need to decide whether to:

1. **Preserve git history** - Keep all Praxisity framework commits
2. **Reset git history** - Remove framework history and start fresh

Considerations:
- Users are creating their own project, not extending the framework
- Framework development history has no relevance to end-user projects
- Git history affects repository size and clarity
- First commit should represent the user's project, not framework development

## Decision

**The `/new-project` command will reset git history by default**, creating a fresh repository with a single initial commit:

```
chore: initialize project from Praxisity framework v1.0.0

Project: [PROJECT_NAME]
Type: [PROJECT_TYPE]
Version: [VERSION]

Generated with Praxisity - A design-first workflow framework
```

The command will:
1. Remove `.git` directory
2. Initialize fresh git repository
3. Stage all files
4. Create initial commit documenting framework version
5. Optionally configure git remote

## Rationale

**Clear project identity:**
The git log should tell the story of the user's project, not the framework's development. When someone looks at `git log`, they should see the project's evolution, not template changes and framework features.

**Professional presentation:**
If users share their repository or work in a team, a clean git history looks professional. It's their project's story from day one.

**Smaller repository:**
Framework development history is irrelevant baggage. Removing it reduces clone size and speeds up operations.

**Explicit provenance:**
The initial commit explicitly documents which framework version was used. This is better than implicit history preservation - it's clear and intentional.

**Matches user mental model:**
Users think of `/new-project` as "start my project from this framework," not "fork the framework." A fresh git history matches that mental model.

**No practical downside:**
Framework history provides no value to end users. They don't need to understand why template section X was added or refactored. They just need the current, working framework.

## Alternatives Considered

### Alternative 1: Preserve Framework History

**Description:** Keep all Praxisity framework development commits in the new project's history.

**Pros:**
- Shows framework evolution (educational?)
- Maintains full git history
- Easier implementation (no git reset needed)

**Cons:**
- Clutters user's project history with irrelevant commits
- First 50+ commits are framework development, not user's project
- Larger repository size
- Confusing to anyone reviewing the project
- User's actual project history buried under framework commits
- Implies project is a framework fork (it's not)

**Why not chosen:** Framework history has zero relevance to end-user projects. It's noise that obscures the project's actual development story.

### Alternative 2: Squash to One Commit But Keep History

**Description:** Keep git history but squash all framework commits into a single "framework baseline" commit.

**Pros:**
- Preserves git continuity
- Single commit is cleaner than full history
- User can see framework version in history

**Cons:**
- Still implies this is a fork/branch of framework
- Squashed commit contains irrelevant diff (all framework files)
- More complex than full reset
- Still larger than necessary

**Why not chosen:** Squashing is unnecessary complexity. A fresh repository is simpler, clearer, and more accurate to what's happening (starting a new project).

### Alternative 3: Give User the Choice

**Description:** Prompt user during `/new-project`: "Reset git history? (yes/no)"

**Pros:**
- User controls their setup
- Flexibility for different use cases

**Cons:**
- Adds decision fatigue to initialization
- 99% of users want reset (framework history is useless to them)
- Complicates command implementation
- Users may not understand the implications

**Why not chosen:** The right choice is obvious for 99% of cases. Making it a question implies both options are reasonable, which isn't true. Opinionated tools are better.

### Alternative 4: Preserve History But Tag Framework Baseline

**Description:** Keep history but add a tag marking where user's project starts.

**Pros:**
- Clear demarcation of "framework" vs "project" commits
- Preserves full history for reference

**Cons:**
- Still clutters history
- User has to remember to look after tag
- Doesn't solve the "irrelevant commits" problem
- More complex than reset

**Why not chosen:** Doesn't solve the core issue. Framework commits are still there, still irrelevant, still confusing.

## Consequences

### Positive Consequences

- **Clean project history:** Git log shows only the user's project evolution
- **Professional presentation:** First commit is project initialization, not framework template
- **Smaller repository:** No framework development baggage
- **Clear provenance:** Initial commit explicitly states framework version used
- **Matches user intent:** Feels like "start new project" not "fork framework"
- **Simpler mental model:** This is a new project, not a branch

### Negative Consequences

- **Cannot trace framework changes:** Users can't see how framework evolved (but why would they?)
- **Irreversible:** Once history is reset, framework commits are gone (but they're in the framework repo)
- **Slightly more complex command:** Need to handle git reset logic

### Neutral Consequences

- **Framework updates require manual merge:** Users can't `git pull` framework updates (but framework should be stable)
- **Initial commit larger:** First commit includes all framework files (but only once)

## Implementation Notes

**Command Flow:**
```bash
# Step 7 in /new-project command

# Remove old git repository
rm -rf .git

# Initialize fresh repository
git init

# Stage all files
git add .

# Create initial commit
git commit -m "chore: initialize project from Praxisity framework v1.0.0

Project: [PROJECT_NAME]
Type: [PROJECT_TYPE]
Version: [VERSION]

Generated with Praxisity - A design-first workflow framework
https://github.com/[USERNAME]/praxisity"

# Optionally set remote
# (prompt user for git remote URL)
```

**Files Affected:**
- `.claude/commands/new-project.md` - Implements git reset logic

**User Communication:**
- Documentation clearly states history is reset
- Success message shows "Fresh git repository with initial commit"
- No hidden surprises

## References

- `.claude/commands/new-project.md` - Step 7: Reset Git History
- `praxisity-foundation-plan.md` - /new-project command behavior
- Related discussion: "What is the point of preserving Git history?"

---

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2025-12-18 | Initial version | Framework Architect |
