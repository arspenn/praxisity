# ADR-003: Todoist MCP for External Task Management

**Date:** 2025-12-18
**Status:** Accepted
**Deciders:** Framework Architect
**Tags:** task-management, todoist, mcp, adhd, external-accountability

## Context

The framework needs a way to manage tasks for project work. Tasks include:
- Micro-chunked implementation steps from `/breakdown`
- Charter review reminders
- Specification and design items
- Follow-up actions

Task management approaches available:
1. **Text files** (TODO.md, task lists in markdown)
2. **External tools via MCP** (Todoist, Notion, Linear, etc.)
3. **Built-in task tracking** (custom solution)
4. **No task management** (rely on user's existing system)

Requirements:
- ADHD-friendly (reminders, due dates, mobile access)
- External accountability (tasks exist outside AI conversation)
- Minimal token consumption (don't pollute context)
- Persistent across sessions
- Easy to integrate with AI workflow

## Decision

**Use Todoist via MCP (Model Context Protocol) for task management.**

Tasks are:
- Created externally in Todoist projects
- Not stored in text files within the repository
- Referenced by commands but not duplicated in conversations
- User-managed through Todoist UI, mobile app, or AI commands

Framework commands (`/breakdown`, `/charter`, etc.) will use Todoist MCP to create, update, and reference tasks.

## Rationale

**External accountability:**
Tasks in Todoist exist independent of the AI conversation. They persist across sessions, survive context window limits, and provide accountability outside the code editor. Users see tasks on mobile, get reminders, and can work without opening Claude Code.

**ADHD-appropriate design:**
Todoist provides critical ADHD support features:
- Due dates and reminders (external prompts)
- Mobile access (check tasks anywhere)
- Quick capture (add tasks from anywhere)
- Visual progress (satisfaction from checking off items)
- Priority levels (focus on what matters)

**No token consumption:**
Tasks stored externally don't consume context window tokens. A project with 200 tasks doesn't pollute every conversation. AI reads tasks when needed, not constantly.

**Micro-chunking support:**
Todoist's task structure (projects → sections → tasks → subtasks) perfectly supports the `/breakdown` command's micro-chunking. Each small task (<30min) becomes a checkbox.

**Existing ecosystem:**
Many users already use Todoist. For those who don't, it's a proven, well-designed tool. No need to reinvent task management.

**MCP integration:**
The official Todoist MCP server makes integration straightforward. Commands can create tasks, update status, and query progress without custom API code.

**Design philosophy alignment:**
External task management aligns with the framework's philosophy:
- Design-first (plan in docs, track in tasks)
- Minimal cognitive overhead (offload to external system)
- External accountability (not just text files)

## Alternatives Considered

### Alternative 1: Text File Task Lists (TODO.md)

**Description:** Store tasks in markdown files (TODO.md, tasks.md) within the repository.

**Pros:**
- Version controlled
- No external dependencies
- Simple to implement
- Works offline
- Free

**Cons:**
- No reminders or due dates
- No mobile access
- Consumes token budget (tasks in every conversation)
- No external accountability
- Manual checkbox management
- Not ADHD-friendly
- Tasks buried in text files

**Why not chosen:** Text files fail the ADHD requirement. No reminders, no mobile access, no external accountability. Tasks become stale markdown that users ignore.

### Alternative 2: GitHub Issues/Projects

**Description:** Use GitHub Issues and Projects for task management.

**Pros:**
- Integrated with repository
- Good for collaboration
- Free
- Familiar to developers
- API available

**Cons:**
- GitHub-locked (what about GitLab users?)
- Software-focused (awkward for public health/research projects)
- Heavier interface (not quick capture)
- No mobile app optimization for personal tasks
- Overkill for solo projects
- Not ADHD-optimized

**Why not chosen:** GitHub Issues are great for software collaboration but poor for personal task management. Too heavy, too software-centric, no ADHD features.

### Alternative 3: Built-In Task System

**Description:** Build custom task management into the framework.

**Pros:**
- Full control over features
- Optimized for framework workflow
- No external dependencies
- Free

**Cons:**
- Reinventing the wheel
- Months of development time
- Need mobile app, reminders, sync, etc.
- Diverts from core framework mission
- Users can't use existing task habits
- Maintenance burden

**Why not chosen:** Building task management is a massive scope creep. Todoist already exists and is excellent. Focus on framework, not reinventing productivity tools.

### Alternative 4: Multiple MCP Options (Notion, Linear, etc.)

**Description:** Support multiple task systems via different MCPs.

**Pros:**
- User choice
- Flexibility for different workflows

**Cons:**
- Complexity in command implementations
- Testing burden (test against all systems)
- Documentation burden
- Different features across systems
- Dilutes optimization for any one system

**Why not chosen:** MVP needs focus. Start with Todoist (excellent for ADHD, good MCP support). Can add alternatives post-MVP if users request.

### Alternative 5: No Task Management

**Description:** Don't provide task management. Users use whatever system they want.

**Pros:**
- Maximum flexibility
- No dependencies
- Simplest implementation

**Cons:**
- Loses ADHD-friendly design goal
- No `/breakdown` micro-chunking workflow
- Misses integration opportunity
- Forces users to manually translate designs to tasks

**Why not chosen:** Task management is core to the framework's value. The design → breakdown → tasks flow is what makes this framework useful for ADHD users.

## Consequences

### Positive Consequences

- **ADHD support:** Reminders, mobile access, due dates, quick capture
- **External accountability:** Tasks exist outside conversation
- **Token efficiency:** No task lists consuming context
- **Professional tool:** Todoist is well-designed and maintained
- **Mobile workflow:** Check tasks anywhere, not just in code editor
- **Visual progress:** Satisfaction from completing tasks
- **Proven system:** Established patterns, not experimental
- **Integration ready:** Official MCP available

### Negative Consequences

- **External dependency:** Requires Todoist account (Premium recommended: $4/month)
- **MCP requirement:** Users must configure Todoist MCP
- **Lock-in risk:** Tasks stored in Todoist (but export available)
- **Network dependency:** Need internet for task operations
- **Setup friction:** One more thing to configure

### Neutral Consequences

- **Learning curve:** Users unfamiliar with Todoist need to learn it
- **Cost:** Todoist Premium ($4/month) for best features (free tier works but limited)
- **Privacy:** Tasks stored in Todoist's cloud (some users may object)

## Implementation Notes

**MCP Configuration:**

Users add to Claude Code settings:
```json
{
  "mcpServers": {
    "todoist": {
      "command": "npx",
      "args": ["mcp-remote", "https://ai.todoist.net/mcp"]
    }
  }
}
```

**Todoist Structure:**

One Todoist project per Praxisity project with sections:
- Planning
- Specifications
- Design
- Implementation (micro-chunked from `/breakdown`)
- Delivery

**Commands Using Todoist:**

- `/new-project` - Optionally creates Todoist project
- `/charter` - Optionally creates review reminder
- `/breakdown` - Creates micro-chunked tasks from design
- `/define` - Can link DIPs to Todoist tasks

**Graceful Degradation:**

If Todoist MCP is unavailable:
- Commands detect and skip Todoist operations
- Show warning: "Todoist MCP not available. Create tasks manually."
- Core workflow still works (just without task creation)

**Documentation Needed:**

Create `.praxisity/docs/todoist-mcp-setup.md` with:
- Step-by-step MCP configuration
- Todoist account setup
- Free vs Premium comparison
- Troubleshooting

## References

- Foundation Plan: "Todoist Integration Architecture" section
- Foundation Plan: "Why Todoist (Not Text Files)"
- Todoist MCP: https://ai.todoist.net/mcp
- CLAUDE.md: Todoist Integration section
- `/breakdown` command (Week 2) - Will use Todoist MCP
- `/charter` command - Optional Todoist reminders

---

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2025-12-18 | Initial version | Framework Architect |
