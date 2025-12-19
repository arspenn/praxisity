# ADR-004: Framework Directory Structure (.praxisity/ namespace)

**Date:** 2025-12-18
**Status:** Accepted
**Deciders:** Framework Architect
**Tags:** directory-structure, namespacing, organization, separation-of-concerns

## Context

The framework provides resources (templates, safety logic, documentation) that users need when running commands. We need to decide where to store these framework resources in relation to user project files.

Options for organizing framework resources:
1. **Dedicated framework directory** (e.g., `.praxisity/`)
2. **Mixed with project files** (templates in `templates/`, safety in `lib/`, etc.)
3. **Hidden dotfiles** (`.praxisity-templates`, `.praxisity-safety`, etc.)
4. **Single file** (all resources in one large file)

Considerations:
- Clear ownership (framework vs. project resources)
- Namespace collision prevention
- Ease of framework updates
- Discoverability for users
- Git ignore patterns
- Cross-platform compatibility

## Decision

**Use a dedicated `.praxisity/` directory to namespace all framework resources.**

Structure:
```
.praxisity/
├── templates/          # Document templates
│   ├── claude.template.md
│   ├── charter.template.md
│   ├── spec.template.md
│   ├── design.template.md
│   ├── dip.template.md
│   ├── adr.template.md
│   ├── readme.template.md
│   └── pandoc/         # LaTeX templates for PDF generation
└── safety/             # Git safety validation logic
```

This directory:
- Contains only framework-provided resources
- Is preserved by `/new-project` command
- Uses `.` prefix to indicate "framework infrastructure"
- Has clear subdirectories for different resource types

## Rationale

**Clear ownership:**
`.praxisity/` clearly belongs to the framework. `templates/` (without the prefix) would be ambiguous - user templates or framework templates? `.praxisity/templates/` is unambiguous.

**Namespace collision prevention:**
User projects might naturally create `templates/`, `safety/`, or `lib/` directories for their own use. `.praxisity/` won't conflict because the prefix is framework-specific.

**Easier framework updates:**
If we need to update templates or add new framework resources, we know exactly where they live. No need to hunt through project files or worry about overwriting user content.

**Conceptual separation:**
Framework resources are infrastructure, not project content. The `.` prefix (like `.git`, `.github`) signals "system directory, not main content."

**Subdirectory organization:**
Within `.praxisity/`, subdirectories (`templates/`, `safety/`) provide clear categorization. Easy to find the charter template: `.praxisity/templates/charter.template.md`.

**Git-friendly:**
Users can choose to ignore `.praxisity/` in their own projects if they want to manage it separately, though we don't recommend it. The clear boundary makes this possible.

**Discoverable but not intrusive:**
The `.` prefix keeps it out of the main workspace visually (many editors hide dotfiles by default) but it's easily accessible when needed. Run `ls -la` and you see it.

## Alternatives Considered

### Alternative 1: Mix Framework Files with Project Files

**Description:** Put templates in `templates/`, safety in `lib/` or `scripts/`, etc.

**Pros:**
- Flatter structure
- No dotfile prefix
- More "visible"

**Cons:**
- Namespace collisions (user might want `templates/` for their own use)
- Unclear ownership (which templates are framework, which are user?)
- Harder to update framework (need to identify framework files)
- Conceptual mixing (framework infrastructure mixed with project content)

**Why not chosen:** Creates ambiguity. Is `templates/charter.template.md` a framework resource or a user-created template? Mixing ownership is asking for confusion.

### Alternative 2: Multiple Hidden Dotfiles

**Description:** Use separate dotfiles/directories: `.praxisity-templates/`, `.praxisity-safety/`, etc.

**Pros:**
- Clear framework ownership (`.praxisity-` prefix)
- Each resource type isolated

**Cons:**
- Clutters root directory with multiple dotfiles
- Harder to understand "what is framework"
- More paths for commands to reference
- Scattered organization

**Why not chosen:** Multiple dotfiles are harder to manage than one directory with subdirectories. `.praxisity/` is a single conceptual unit.

### Alternative 3: Single File (All Resources Bundled)

**Description:** Put all framework resources in one file (e.g., `.praxisity.json` or `.praxisity.md`).

**Pros:**
- Minimal filesystem footprint
- Easy to version as single file

**Cons:**
- Huge file (thousands of lines)
- Hard to edit individual templates
- Complex parsing needed
- Poor git diffs (entire file changes)
- Unnatural for markdown templates

**Why not chosen:** Templates are markdown documents, not JSON data. They need to be separate files for editing and version control.

### Alternative 4: Framework Subdirectory (no dot prefix)

**Description:** Use `praxisity/` instead of `.praxisity/`.

**Pros:**
- More visible (no dot prefix)
- Same organization as `.praxisity/`

**Cons:**
- Not clearly "system infrastructure"
- Clutters main workspace visually
- Name collision if user wants a `praxisity/` directory for their own use
- Doesn't follow convention (`.git`, `.github`, `.vscode`)

**Why not chosen:** The `.` prefix is meaningful. It signals "framework infrastructure" like `.git` signals "version control infrastructure."

### Alternative 5: Claude Code-Specific Location

**Description:** Use `.claude/praxisity/` or put resources in `.claude/`.

**Pros:**
- Groups with Claude Code configuration
- Clear it's for AI tooling

**Cons:**
- `.claude/` is for commands, not data
- Conflates commands with resources
- Harder to reference (deeper path)
- Less clear separation

**Why not chosen:** `.claude/commands/` is for command implementations. Resources are separate concerns and deserve their own namespace.

## Consequences

### Positive Consequences

- **Clear ownership:** Framework resources obviously belong to framework
- **No collisions:** Won't conflict with user-created directories
- **Easy updates:** Framework updates know exactly where to put new resources
- **Conceptual clarity:** Infrastructure separated from project content
- **Subdirectory organization:** `templates/`, `safety/` are clearly categorized
- **Git-friendly:** Clear boundary for version control decisions
- **Convention-following:** Like `.git`, `.github`, `.vscode`
- **Discoverable:** `ls -la` shows it; most editors allow access

### Negative Consequences

- **Hidden by default:** Some tools hide dotfiles (but `ls -la` shows it)
- **One more directory:** Adds to project structure (minimal impact)
- **Unusual for some users:** Not everyone knows dotfile conventions

### Neutral Consequences

- **Framework-specific:** Other tools won't recognize `.praxisity/` (that's fine - it's ours)
- **Subdirectory depth:** `.praxisity/templates/` is three levels deep (acceptable)

## Implementation Notes

**Directory Structure:**
```
.praxisity/
├── templates/
│   ├── claude.template.md       # CLAUDE.md for new projects
│   ├── charter.template.md      # CHARTER.md for projects
│   ├── spec.template.md         # Specification template (Week 2)
│   ├── design.template.md       # Design document template (Week 2)
│   ├── dip.template.md          # DIP template (Week 2)
│   ├── adr.template.md          # ADR template
│   ├── readme.template.md       # README.md for new projects
│   └── pandoc/                  # LaTeX templates (Week 3)
│       ├── academic.latex
│       ├── report.latex
│       └── memo.latex
└── safety/                      # Git safety scripts (Week 3)
    └── (to be designed)
```

**Preserved by /new-project:**

The `/new-project` command explicitly preserves `.praxisity/`:
```
Preserves:
- .claude/commands/ (framework commands)
- .praxisity/        (framework resources)
```

**Command References:**

Commands reference templates with full path:
```bash
# Read charter template
cat .praxisity/templates/charter.template.md

# Read CLAUDE.md template
cat .praxisity/templates/claude.template.md
```

**Future Additions:**

Can add more subdirectories as needed:
- `.praxisity/docs/` - Framework documentation
- `.praxisity/scripts/` - Helper scripts
- `.praxisity/config/` - Framework configuration

## References

- Foundation Plan: "Directory Structure" section
- `.claude/commands/new-project.md` - Preserves .praxisity/
- CLAUDE.md: Framework Structure section
- All templates in `.praxisity/templates/`

---

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2025-12-18 | Initial version | Framework Architect |
