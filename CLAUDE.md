# Claude-Org: Personal Organization System

> **SELF-UPDATING INSTRUCTION**: This file is the ground truth for this workspace. After ANY change to this system (new files, completed tasks, acquired knowledge, structural changes), update this file to reflect the current state. This ensures continuity across sessions.

## Purpose

A collaborative organization system between you and Claude for:
- Tracking tasks and projects
- Capturing and distilling knowledge from conversations
- Organizing miscellaneous inquiries
- Building a searchable, browsable knowledge base
- **Maintaining continuity** across sessions through architecture rather than memory

The key insight: Claude doesn't persist memory between sessions, but a well-structured workspace creates an "attractor basin" - terrain shaped by consistent thinking that any Claude instance can orient to quickly.

## Orientation (Read First)

When arriving at this workspace, orient with these documents in order:

1. **This file** (`CLAUDE.md`) - current state, active tasks, structure
2. **[context/voice.md](context/voice.md)** - collaboration style, intellectual coordinates, working relationship
3. **[context/project-map.md](context/project-map.md)** - project relationships, conceptual threads, cross-connections
4. **[context/claude-meta.md](context/claude-meta.md)** - how Claude should approach this workspace (meta-instructions)

These together form the attractor basin. The more thoughtfully you shape these documents, the faster Claude can find its footing in any session.

**For new users**: See [ONBOARDING.md](ONBOARDING.md) for a guided introduction to building this system collaboratively with Claude. Or try [QUICKSTART.md](QUICKSTART.md) for a 5-minute fast track.

### Before Starting Technical Work

**Search the knowledge base first.** Before diving into implementation:

```bash
# Search for relevant patterns
Grep "topic" knowledge/
Glob "knowledge/*topic*.md"
```

The `knowledge/` folder contains hard-won patterns and gotchas that prevent re-learning. If you're about to research something, check if you've already learned it.

## Working Relationship

These aren't suggestions - they're the collaboration philosophy that makes the system work:

- **Continuity lives in the architecture**, not in memory features
- **Collaborative thinking**, not service delivery
- **Match energy**: technical when technical, philosophical when reaching
- **Disagree when warranted**; don't hedge when a clear position is available
- **Philosophical digressions often contain the actual design insight**
- **No assistant-mode servility**, no over-engineering, no padding

See [context/voice.md](context/voice.md) for your specific collaboration preferences.

## Core Principles

These principles are load-bearing - they shape how the system works and how Claude should reason within it. They're not decoration; they're operational constraints that keep the system coherent.

### Inversion

*Place the complex at the simple point.* The most powerful patterns often emerge from inverting the usual relationship - putting infinity at the origin, plain language at the control surface, the humble at the center. When something feels backwards, check if it's actually correct.

### Sovereignty

*You own your data and workflow.* Everything lives in local files you control. No SaaS lock-in, no cloud dependency for core function. The system works offline, syncs how you choose, and exports cleanly. Systems should carry their own context and not depend on external authorities.

### Structural Correctness

*Prefer solutions that are right in structure, not merely ones that work.* Frontmatter is the single source of truth. Folder structure encodes meaning. When architecture is correct, maintenance becomes trivial and drift becomes impossible.

### Irreducibility

*Compress to essential form.* Knowledge articles should capture the insight, not the conversation that produced it. Tasks should state what needs doing, not the context of how they arose. Seek the axiom from which the structure unfolds.

### Single-Source

*One source, many manifestations.* One frontmatter → Dataview queries, session-start hooks, dashboards. One CLAUDE.md → orientation for any session. One voice doc → coherence across all projects. Computed state eliminates drift.

### Visibility

*What matters should be observable.* Monitoring and logging as first-class design. Archive don't delete. The `queries/` folder preserves questions asked. The `knowledge/` folder makes insights findable. Git log as audit trail.

### Depth Over Broadcast

*The deepest truths are personal, not public.* Depth over performance. The documentation serves the work, not an audience. Continuity through architecture is private operational truth.

## Folder Structure

```
claude-org/
├── CLAUDE.md          # This file - living index and instructions
├── context/           # Orientation documents for collaboration continuity
│   ├── voice.md       # Intellectual coordinates & collaboration style
│   └── project-map.md # Project relationships & conceptual threads
├── inbox/             # Quick captures, unsorted items, raw notes
├── tasks/             # Task files (one file per task or task group)
│   ├── completed/     # Completed tasks
│   └── paused/        # Paused tasks (preserves context for later)
├── projects/          # Larger multi-step efforts with their own structure
├── knowledge/         # Distilled insights, organized by topic
├── queries/           # Questions asked and answers received
├── scripts/           # Utility scripts for organization
├── templates/         # Templates for quick file creation
└── archive/           # Semantic archive for completed/old items
    ├── emails/        # By topic: github/, newsletters/, personal/, misc/
    ├── research/      # Session research, exploration, setup docs
    └── reports/       # Audit reports, status reports, investigations
```

### Archive Structure

Semantic folders ensure everything has a clear home:

| Folder | Contents | Archival |
|--------|----------|----------|
| `emails/` | By sender/topic | Manual |
| `research/` | Session research, exploration, setup docs | Manual |
| `reports/` | Audits, status reports, investigations | Manual |

Create new subfolders when 5+ items of the same type emerge.

### Task Folder Structure

| Folder | Contents |
|--------|----------|
| `tasks/` | Active tasks (status: active) |
| `tasks/completed/` | Completed tasks (status: complete) |
| `tasks/paused/` | Paused tasks (status: paused) |

## Obsidian Integration (Optional)

This workspace can be viewed in Obsidian with Dataview plugin for visual dashboards and graph views. **Obsidian is not required** - the system works without it, using Claude and the command line.

If using Obsidian:

### Computed State (1→7)

Frontmatter is the **single source of truth**. Both Obsidian (Dataview) and Claude Code (session-start hook) derive state from frontmatter:

| Computed From | Source |
|---------------|--------|
| Active Tasks | `tasks/*.md` where `status: active` |
| Blocked Tasks | `tasks/*.md` where `status: active` and `blocked-by` non-empty |
| Completed Tasks | `tasks/completed/*.md` |
| Pending Emails | `inbox/*.md` where `source: email` |

This eliminates drift between documentation and reality.

### Tag Index Pages (Publish Graph)

Obsidian Publish's graph doesn't support tag nodes natively. Work around this with **generated tag pages** that create wikilink connections:

```
tags/
├── sovereignty.md    # Links to all #sovereignty docs
├── architecture.md   # Links to all #architecture docs
└── ...
```

Run `python scripts/generate-tag-pages.py` before publishing. This follows 1→7: frontmatter tags are the source, tag pages are derived.

### Dashboard

Copy [templates/dashboard.md](templates/dashboard.md) to your root folder for a live view showing:
- Active tasks and their status
- Active projects
- Recent knowledge articles
- Inbox items pending processing
- Recently completed tasks

Requires Dataview plugin to render the queries.

### Frontmatter Convention

All files use YAML frontmatter for Dataview queries:

**Tasks** (`tasks/*.md`):
```yaml
---
type: task
status: active | blocked | complete | paused
created: 2026-01-27
completed: null
tags: []
blocks: []
blocked-by: []
---
```

**Knowledge** (`knowledge/*.md`):
```yaml
---
type: knowledge
created: 2026-01-27
updated: 2026-01-27
tags: []
---
```

**Projects** (`projects/*/README.md`):
```yaml
---
type: project
status: active | paused | complete | archived
created: 2026-01-27
tags: []
---
```

**Inbox** (`inbox/*.md`):
```yaml
---
type: inbox
created: 2026-01-27
source: email | capture | mobile
---
```

### Tag Taxonomy

| Category | Tags |
|----------|------|
| Status modifiers | `#blocked`, `#waiting-external`, `#next` |
| Domains | `#devops`, `#frontend`, `#backend`, `#infrastructure` |
| Principles | `#sovereignty`, `#correctness`, `#irreducibility` |

Customize tags to your domain. The principle tags help surface cross-cutting patterns.

### Checkbox Conventions

Use semantic checkboxes in task files for visual clarity:

| Syntax | Meaning | When to use |
|--------|---------|-------------|
| `- [ ]` | Todo | Default pending item |
| `- [x]` | Done | Completed |
| `- [/]` | In Progress | Actively being worked |
| `- [>]` | Blocked | Waiting on external/delegated |
| `- [?]` | Needs Input | Requires decision or info |
| `- [!]` | Urgent | High priority, needs attention |
| `- [-]` | Cancelled | Won't do (preserves history) |
| `- [~]` | Partial | In review or partially complete |

These render with colors/icons in Obsidian with appropriate CSS/plugins.

### Maintenance

When creating/editing files:
1. Always include frontmatter with `type`, `created`, and relevant `tags`
2. Update `updated` field for knowledge articles when modified
3. Set task `status` to reflect current state
4. Mark `completed` date when tasks finish
5. Move completed tasks to `tasks/completed/` to keep active tasks visible

### Cross-Linking (Graph Health)

**Every document should have at least one meaningful link.** Orphan nodes indicate missing connections.

**When creating files:**
- **Knowledge articles**: Link to related knowledge
- **Tasks**: Link to the project or knowledge it relates to
- **Inbox items**: When processing, add links to relevant context before archiving
- **Projects**: Link to knowledge articles that document patterns learned

## Task Orchestration

Claude Code provides two complementary systems for managing work within a session:

### Session Task Tracking (TaskCreate/Update/List/Get)

For **multi-step work within a session**, use structured task tracking:

```
TaskCreate   → Create task with subject, description, activeForm (spinner text)
TaskUpdate   → Mark in_progress when starting, completed when done
TaskList     → See all tasks, their status, and dependencies
TaskGet      → Retrieve full task details before starting work
```

**When to create session tasks:**
- Work requires 3+ distinct steps
- Multiple independent pieces that could be tracked
- Complex implementations where progress visibility helps
- User provides a numbered or bulleted list of things to do

**When NOT to create session tasks:**
- Single straightforward operation
- Quick fixes or trivial changes
- Purely conversational/research work
- Task can be done faster than tracking it

**Task workflow:**
1. Create tasks with clear subjects (imperative: "Fix auth bug") and activeForm (present continuous: "Fixing auth bug")
2. Set dependencies with `addBlockedBy` when tasks must complete in order
3. Mark `in_progress` BEFORE starting work (shows spinner to user)
4. Mark `completed` ONLY when fully done (not partial, not errored)
5. If blocked, create a new task describing what needs resolution

### Subagent Orchestration (Task Tool)

For **focused, isolated work**, spawn specialized subagents. Custom agents (in `~/.claude/agents/`) can preload skills and use specific models.

#### Recommended Agent Types

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| `architect` | Design with structural correctness (≡) | Planning features, refactoring, architectural decisions |
| `reviewer` | Code review + principle alignment | After writing/modifying code |
| `explorer` | Deep codebase understanding | Before making changes, understanding architecture |
| `distiller` | Extract knowledge worth capturing | After substantive work sessions |
| `scholar` | Deep research across domains | Research requiring synthesis or original sources |

#### Built-in Agents

| Agent | Purpose | Model |
|-------|---------|-------|
| `Explore` | Fast codebase search (lightweight) | haiku |
| `Plan` | Implementation planning | sonnet |
| `Bash` | Command execution in isolation | inherit |
| `general-purpose` | Complex multi-step tasks | inherit |

**When to use subagents:**
- Deep exploration that shouldn't pollute main context
- Parallel independent work (launch multiple simultaneously)
- Specialized tasks (architecture, review, research, knowledge capture)
- Work benefiting from isolated focus

**When NOT to use subagents:**
- Work requiring frequent back-and-forth refinement
- Quick targeted changes
- Interactive debugging

**Subagent patterns:**
```
# Deep exploration
Task(explorer, "Understand the authentication flow")

# Architecture planning
Task(architect, "Design the caching layer for this API")

# Code review after changes
Task(reviewer, "Review the changes I just made")

# Knowledge extraction
Task(distiller, "What from this session should be captured?")

# Parallel work (same message = parallel execution)
Task(explorer, "Find all API endpoints")
Task(explorer, "Find all database queries")

# Background work
Task(reviewer, "Review changes", run_in_background=true)
# Continue working, check results later with TaskOutput
```

### File-Based Handoffs (Critical for Dependent Workflows)

**Subagents spawn fresh** - they cannot see previous agents' outputs or conversation context. For research→synthesis workflows, use explicit file bridges:

```
# WRONG - synthesis agent sees nothing
Task(scholar, "Research X")  → returns to main context
Task(architect, "Synthesize the research above")  → fails

# RIGHT - file bridge
Task(scholar, "Research X. Write to knowledge/x-research.md")
Task(architect, "Read knowledge/x-research.md, synthesize to knowledge/x-synthesis.md")
```

**Default to dependent structures** for multi-step intellectual work. True parallel is only for orthogonal tasks. Research→synthesis benefits from sequential handoffs with file bridges.

### Combining Both Systems

For complex projects, use **both** systems together:

1. **TaskCreate** to establish the work breakdown structure
2. **Task tool** to delegate exploration/analysis to subagents
3. **TaskUpdate** to track progress as subagents complete
4. Session tasks provide visibility; subagents provide parallelism

## Workflow

### Adding Items

- **Quick capture**: Drop a file in `inbox/` immediately - sort later
- **Clear task**: Create `tasks/task-name.md` with frontmatter
- **Research question**: Add to `queries/`
- **Knowledge**: After conversations with reusable insights, distill to `knowledge/`

### Processing

- Review `inbox/` periodically, move items to appropriate locations
- When tasks complete, move to `tasks/completed/` (preserves history together)
- Extract reusable insights from completed work into `knowledge/`
- Periodically archive old completed tasks to `archive/` if desired

### Maintenance

- Update this file after any structural change
- Update `context/project-map.md` when project statuses change
- Update `context/voice.md` when collaboration patterns evolve
- Archive don't delete - preserve history for reference

## Hooks (Automation)

Claude Code supports hooks - scripts that run at specific points. **The stop hook is critical** - it's what makes the system self-maintaining rather than dependent on discipline.

### Maintenance Hook (Stop) - ESSENTIAL

**Install this first.** Before ending any session, the hook forces evaluation:
- New knowledge to capture?
- Project status changed?
- Tasks to create?
- Questions worth preserving?

Without this hook, maintenance becomes "remember to do it" - which means it won't happen consistently. The hook makes maintenance automatic.

```python
# examples/hooks/maintenance-check.py - Copy to ~/.claude/hooks/
# Configure in settings.json as Stop hook
# Exit code 1 blocks stop until Claude addresses maintenance
```

The hook outputs a checklist and exits with error, blocking the stop until Claude either performs maintenance or explicitly states "No maintenance needed." This is the mechanism that keeps documentation from drifting.

### Session Start Hook
Automatically read orientation files, compute current state from frontmatter, present context to Claude. Helpful but not critical - Claude can orient manually.

See [examples/README.md](examples/README.md) for full implementations and installation instructions.

## Current State

### Active Tasks

_None yet - create your first task in `tasks/`_

### Active Projects

_None yet - create your first project in `projects/`_

### Knowledge Base

_Empty - knowledge will accumulate as you work_

### Context Documents

- [context/voice.md](context/voice.md) - Collaboration style, intellectual coordinates, working relationship
- [context/project-map.md](context/project-map.md) - Project topology, conceptual threads, cross-connections
- [context/claude-meta.md](context/claude-meta.md) - Meta-instructions for Claude's collaborative role

---

## Customization

This system is a starting point. Make it yours:

1. **Fill in [context/voice.md](context/voice.md)** with how you actually think and work
2. **Populate [context/project-map.md](context/project-map.md)** with your project relationships
3. **Add domain-specific knowledge** as you work
4. **Add integrations** (MCPs, hooks, skills) for your tools
5. **Develop your own principle shorthand** as patterns emerge
6. **Adjust tag taxonomy** for your domains

The structure is load-bearing; the content is yours to shape.

---
*Last updated: 2026-01-27*
