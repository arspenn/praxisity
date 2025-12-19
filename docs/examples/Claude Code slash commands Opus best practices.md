# Claude Code Slash Commands: Opus 4.5 Best Practices

Concise, focused commands outperform verbose ones for Claude Code, with **Opus 4.5 requiring calmer prompting language** than earlier models. Official documentation confirms a **15,000-character budget** for command descriptions loaded into context, while community consensus recommends keeping individual commands focused on single outcomes. The most significant finding: Opus 4.5's improved instruction-following means aggressive prompting patterns that worked with Sonnet 3.5 now cause "overtriggering" and over-engineering.

## Command file structure and length recommendations

Claude Code commands are Markdown files stored in `.claude/commands/` for project-scoped commands (shared via git) or `~/.claude/commands/` for personal commands. The filename becomes the slash command name—for example, `optimize.md` creates the `/optimize` command.

The official SlashCommand tool includes a **15,000-character budget** by default for loading command descriptions into Claude's context. This limit encompasses command names, arguments, and descriptions collectively, though individual command files have no explicit hard cap. Community experience suggests keeping CLAUDE.md files under **25KB** (Anthropic's own monorepo is approximately 13KB), with the practical sweet spot being under **300 lines** for instruction files.

Frontmatter support enables precise command configuration:

| Field | Purpose | Default |
|-------|---------|---------|
| `description` | Brief command explanation | First line of content |
| `argument-hint` | Expected args format (e.g., `[issue-number]`) | None |
| `allowed-tools` | Permitted tool access (e.g., `Bash(git:*)`) | Inherits from conversation |
| `model` | Override model selection | Inherits from conversation |
| `disable-model-invocation` | Prevent auto-invocation | false |

## Opus 4.5 requires calmer prompting than earlier models

The most critical distinction for Opus 4.5 command authoring involves prompting intensity. According to Anthropic's Claude 4 migration documentation, **Opus 4.5 is significantly more responsive to system prompts** than predecessors. Commands designed to overcome Sonnet 3.5's undertriggering now cause Opus 4.5 to overtrigger and over-engineer solutions.

**Replace aggressive language patterns:**
- ❌ `"CRITICAL: You MUST use this tool when..."`
- ✅ `"Use this tool when..."`
- ❌ `"ALWAYS call the search function before..."`
- ✅ `"Call the search function before..."`

Opus 4.5 exhibits a documented tendency toward **over-engineering**—creating extra files, adding unnecessary abstractions, and building flexibility that wasn't requested. Effective commands include explicit constraints:

```markdown
Avoid over-engineering. Only make changes directly requested.
Keep solutions simple and focused.
Don't add features, refactor code, or make "improvements" beyond what was asked.
```

The model is also particularly sensitive to the word "think" and its variants. When extended thinking is disabled, these terms trigger specific behavior. Community testing has identified a **thinking budget hierarchy**: `"think"` allocates less thinking time than `"think hard"`, which allocates less than `"think harder"`, which allocates less than `"ultrathink"`. Replace "think" with alternatives like "consider," "believe," or "evaluate" when you don't want to trigger extended thinking.

## Focused commands outperform verbose command libraries

Research from HumanLayer indicates that frontier LLMs can reliably follow approximately **150-200 instructions** with reasonable consistency. As instruction count increases, instruction-following quality degrades **uniformly across all instructions**—not just the newer ones. This finding argues strongly against extensive command libraries.

Developer Shrivu Shankar articulates the community anti-pattern: *"If you have a long list of complex, custom slash commands, you've created an anti-pattern. The entire point of an agent like Claude is that you can type almost whatever you want and get a useful, mergable result."*

**Effective command design principles:**
- One command should produce one clear outcome
- Use numbered steps for sequential workflows (not prose descriptions)
- Provide alternatives when prohibiting actions—don't just say "never do X"
- Test commands on edge cases before sharing with teams

The official Anthropic example demonstrates the recommended structure:

```markdown
Please analyze and fix the GitHub issue: $ARGUMENTS.

Follow these steps:
1. Use `gh issue view` to get the issue details
2. Understand the problem described in the issue
3. Search the codebase for relevant files
4. Implement the necessary changes to fix the issue
5. Write and run tests to verify the fix
6. Ensure code passes linting and type checking
7. Create a descriptive commit message
8. Push and create a PR
```

## Parameter handling and dynamic context patterns

Commands support two argument patterns. The **`$ARGUMENTS`** variable captures all arguments as a single string—useful for flexible input. Positional variables **`$1`, `$2`, `$3`** enable structured multi-parameter commands:

```markdown
---
argument-hint: [pr-number] [priority] [assignee]
---
Review PR #$1 with priority $2 and assign to $3.
```

Commands can execute bash inline to gather dynamic context using the `!` prefix:

```markdown
## Context
- Current git status: !`git status`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task
Based on the above changes, create a single git commit.
```

File references use the `@` prefix: `Review the implementation in @src/utils/helpers.js` tells Claude to read that specific file.

## Community organizational patterns from production repositories

Analysis of popular GitHub repositories (wshobson/commands with 1.2k stars, qdhenry/Claude-Command-Suite with 822 stars) reveals consistent organizational patterns:

```
.claude/commands/
├── workflows/     # Multi-step orchestration (30-90 seconds)
├── tools/         # Single-purpose utilities (5-30 seconds)
├── dev/           # Development commands
├── test/          # Testing commands
└── deploy/        # Deployment commands
```

Subdirectories create **namespaced commands**—`.claude/commands/dev/review.md` becomes `/review` with the label "(project:dev)". This enables organized command collections without name collisions.

Command lengths in production vary predictably by complexity: **short commands** (1-10 lines) for single actions like commits, **medium commands** (10-50 lines) for structured workflows like code reviews, and **long commands** (50+ lines) for comprehensive multi-phase processes like security audits or feature development.

## The explore-plan-code-commit workflow

Anthropic's recommended workflow for complex tasks uses commands strategically:

1. **Explore**: Ask Claude to read relevant files explicitly, instructing it NOT to write code yet
2. **Plan**: Request a plan using thinking triggers ("think hard about the architecture")
3. **Implement**: Ask Claude to implement with explicit verification steps
4. **Commit**: Have Claude commit changes and create a pull request

This workflow prevents Claude from jumping to implementation before understanding the problem space—a common failure mode the community has documented extensively.

## Conclusion

Opus 4.5's improved instruction-following fundamentally changes command authoring strategy. Commands that compensated for earlier model limitations now cause over-engineering and overtriggering. The winning approach: **calmer language, explicit simplicity constraints, and focused single-outcome commands**. The 15,000-character budget and 150-200 instruction attention limit provide hard constraints, but community experience suggests that fewer, well-designed commands consistently outperform extensive libraries. For complex reasoning tasks, leverage the thinking hierarchy (`think` through `ultrathink`) rather than adding more instructions.