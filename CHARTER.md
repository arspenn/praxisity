# Project Charter

## Mission

Build a design-first workflow framework enabling consistent, structured planning and execution for multi-disciplinary projects through AI-assisted tooling — where the framework builds the user through use, and the user builds the framework through experience.

## Principles

1. **Design before implementation** — Specification and design precede building
2. **Bootstrapping** — Use the system to build the system. Use the system to build the user. Use the user to build the system. Every session generates experience that becomes skills, agents, or templates.
3. **Minimal cognitive overhead** — One thing at a time. Structured workflows, micro-chunked tasks, and progressive loading reduce the mental burden at each step.
4. **Self-documenting** — The work IS the documentation. Specs, designs, and plans are git-versioned artifacts that serve as both the process record and the project knowledge base.
5. **Safety-first** — Git safety controls prevent accidental commits. As integrations expand, apply the lethal trifecta model: minimize private data access, sanitize untrusted content, control exfiltration vectors. Start read-only, add capabilities deliberately.
6. **Dual-use design** — All templates, skills, and outputs optimized for both human understanding and AI agent consumption. Files are both prompt output and prompt input.
7. **Reliability** — Operations are referenced, reviewed, reproducible, and rigorous. Claims about platform capabilities are verified empirically. Standards are tested before they're trusted.

## Scope

### In Scope

- Skills-driven workflow: /describe → /design → /plan → /do (with /charter as the entry point)
- Support skills for cross-cutting concerns (/gather, /consult-team, /agent-authoring)
- Agent consultation system (9-agent roster, Mode 1/2/3 dispatch)
- Document templates bundled with skills (charter, spec, design, DIP)
- Git safety controls
- Multi-disciplinary support (software, public health, research)
- Self-bootstrapping capability
- Memory-as-settings for per-project configuration

### Out of Scope

- Collaboration/multi-user features (post-MVP)
- Task management service integration (future — Obsidian vault system under consideration)
- `/deliver` pipeline (deferred — separate Python-based process, needs own spec)
- `/breakdown` task decomposition (deferred — depends on task management decision)
- `/new-project` scaffolding (sunset candidate — pending framework distribution model)
- Proactive agent capabilities (heartbeat, scheduled actions)
- External platform integrations beyond Claude Code (Slack, email, calendar)
- Analytics and metrics (post-MVP)

## Stakeholders

**Primary Users/Beneficiaries:**
- Solo practitioners (developers, researchers, students) needing structured workflows for complex projects

**Contributors:**
- Andrew Robert Spenn (creator)
- Future open-source contributors

**Secondary Stakeholders:**
- N/A — solo project currently

**Advisory/Oversight:**
- N/A — solo project currently

## Success Criteria

**Primary Success Metrics:**
- Successfully self-bootstrap: use Praxisity skills to build Praxisity skills
- End-to-end workflow validated: /charter → /describe → /design → /plan → /do
- Agent consultation system produces measurably better design decisions than solo work

**Milestones:**
- All 5 workflow skills rewritten and validated (SPEC-004)
- /gather support skill tested empirically across multiple sessions
- Charter v2 complete (this session)
- Framework used to specify and build its own remaining skills (bootstrapping proven)

**Quality Indicators:**
- Skills produce consistent output across repeated runs (template determinism)
- Agent reviews catch issues that solo work misses (consultation value)
- Behavioral standards hold — no recurrence of v0.5.0 pattern-class bugs

## Constraints

**Timeline:**
- No hard deadline — quality over speed
- MVP when the 5 workflow skills and bootstrapping are validated

**Resources:**
- Solo developer
- Claude Code Max subscription ($200/mo — supports Mode 3 teams, sustained sessions)

**Technical:**
- Claude Code platform (skills, agents, hooks, memory system)
- Platform capabilities must be empirically verified before relying on them

**Regulatory/Compliance:**
- N/A — no regulatory constraints currently

**Other:**
- Mode 3 team UX is a current limitation — teammate messages flood the terminal, limiting effective team size

## Domain Context

**Tech Stack:**
- Claude Code skills platform (markdown-based prompt engineering)
- Claude Code agent SDK (subagents, teams, memory)
- Git for version control and safety
- Python for /deliver pipeline (deferred)

**Architecture Approach:**
- Skills-based: self-contained skill directories with bundled templates
- Two skill types: workflow (user-invoked) and support (auto-invokable)
- Inline mechanical standards + skill-based judgment standards
- Memory-as-settings for per-project configuration
- Agent consultation for multi-perspective review (9-agent roster)

**Quality Standards:**
- All skills reviewed by specialist agents before deployment
- Platform capabilities verified empirically (reference_skill_platform_capabilities.md)
- Consistency reviewer catches cross-document drift
- Bootstrapping: the framework tests itself by building itself

---

## Charter Maintenance

**Review Schedule:** After each major milestone (skill completion, new integration) or when scope questions arise

**Amendment Process:** Update via /charter skill. Changes reviewed by agent consultation before committing.

---

*Charter established: December 2025*
*Last reviewed: April 2026*
*Next review: After SPEC-004 skill rewrites complete*
