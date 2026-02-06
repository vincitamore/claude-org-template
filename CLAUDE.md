# Claude-Org: Personal Organization System

> **For Claude instances**: This is your ground truth. Start here, then read `context/voice.md` and `context/projects.md`.

> **SELF-UPDATING INSTRUCTION**: This file is the ground truth for this workspace. After ANY change to this system (new files, completed tasks, acquired knowledge, structural changes), update this file to reflect the current state. This ensures continuity across sessions.

---

## Bootstrap Check

**Read `context/voice.md` first.** If it still contains `_..._` placeholder text, this system hasn't been initialized yet. Read [ONBOARDING.md](ONBOARDING.md) and run the onboarding sequence - it will guide you through setting up the system collaboratively with the user.

If voice.md is populated with real content, onboarding is complete. Continue with normal operation below.

---

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

1. **This file** (`CLAUDE.md`) - structure, schemas, conventions, orchestration
2. **[context/current-state.md](context/current-state.md)** - dynamic state: tasks, projects, inbox, recent changes
3. **[context/voice.md](context/voice.md)** - collaboration style, intellectual coordinates, working relationship
4. **[context/projects.md](context/projects.md)** - project relationships, conceptual threads, cross-connections

These together form the attractor basin. The more thoughtfully you shape these documents, the faster Claude can find its footing in any session.

### Before Starting Technical Work

**Search the knowledge base first.** Before diving into implementation:

```bash
# Search for relevant patterns
Grep "topic" knowledge/
Glob "knowledge/*topic*.md"
```

The `knowledge/` folder contains hard-won patterns and gotchas that prevent re-learning. If you're about to research something, check if you've already learned it.

## Make It Yours

This system is scaffolding, not scripture. **If something doesn't work for you, change it.**

- Folder name doesn't make sense? Rename it.
- Principle doesn't resonate? Delete it. Add your own.
- Want different inbox categories? Make them.
- Prefer a flat structure over subfolders? Flatten it.
- Don't like the stop hook prompt? Rewrite it.

The only load-bearing constraint is **frontmatter consistency** - the YAML at the top of each file is what tools use to parse and organize documents. As long as files have valid frontmatter with `type`, `status`, `created`, and `tags`, the system works. Everything else is yours to shape.

When you change something structural, update this file so future sessions know about it.

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

These principles shape how the system works and how Claude should reason within it. They're starter principles - keep what resonates, modify what doesn't, add your own. The lattice in [context/projects.md](context/projects.md) tracks how these show up across your work.

### Inversion

*Place the complex at the simple point.* The most powerful patterns often emerge from inverting the usual relationship - putting infinity at the origin, plain language at the control surface, the humble at the center. When something feels backwards, check if it's actually correct.

### Sovereignty

*You own your data and workflow.* Everything lives in local files you control. No SaaS lock-in, no cloud dependency for core function. The system works offline, syncs how you choose, and exports cleanly.

### Structural Correctness

*Prefer solutions that are right in structure, not merely ones that work.* Frontmatter is the single source of truth. Folder structure encodes meaning. When architecture is correct, maintenance becomes trivial and drift becomes impossible.

### Irreducibility

*Compress to essential form.* Knowledge articles should capture the insight, not the conversation that produced it. Tasks should state what needs doing, not the context of how they arose. Seek the axiom from which the structure unfolds.

### Single-Source

*One source, many manifestations.* One frontmatter source drives hooks, dashboards, and session context. One CLAUDE.md drives orientation for any session. One voice doc drives coherence across all work. Computed state eliminates drift.

### Visibility

*What matters should be observable.* Archive don't delete. The `queries/` folder preserves questions asked. The `knowledge/` folder makes insights findable. Git log as audit trail. If something matters, it should be findable.

### Depth Over Broadcast

*The deepest truths are personal, not public.* Depth over performance. The documentation serves the work, not an audience. Continuity through architecture is private operational truth.

### [Your Principle]

*Add your own as patterns emerge.* When you notice yourself caring about the same thing in different contexts, or when a decision feels obviously right but you can't immediately say why - that's a principle waiting to be articulated.

## Folder Structure

```
claude-org/
├── CLAUDE.md          # This file - living index and instructions
├── context/           # Orientation documents for collaboration continuity
│   ├── current-state.md  # Dynamic state (tasks, projects, inbox, changes)
│   ├── voice.md       # Intellectual coordinates & collaboration style
│   └── projects.md    # Project relationships & conceptual threads
├── inbox/             # Incoming items by type
│   ├── emails/        # Email staging area
│   ├── tickets/       # Work tickets, support requests
│   ├── ideas/         # Feature ideas, future projects (percolating)
│   ├── decisions/     # Architecture/design decisions pending input
│   ├── investigations/# Bugs to research, things to verify
│   └── captures/      # Quick unsorted captures (triage promptly)
├── tasks/             # Task files (see tasks/README.md for full model)
│   ├── completed/     # Completed tasks
│   └── paused/        # Paused tasks (preserves context for later)
├── reminders/         # Time-based reminders (see reminders/README.md)
│   └── completed/     # Completed and dismissed reminders
├── projects/          # Larger multi-step efforts with their own structure
├── knowledge/         # Distilled insights, organized by topic
├── queries/           # Questions asked and answers received (optional)
├── scripts/           # Utility scripts for organization
├── templates/         # Templates for quick file creation
└── archive/           # Semantic archive for completed/old items
    ├── emails/        # By topic: github/, newsletters/, personal/, misc/
    ├── tickets/       # Resolved tickets
    ├── research/      # Session research, exploration, setup docs
    └── reports/       # Audit reports, status reports, investigations
```

### Inbox Structure

Semantic subfolders for incoming items. Use the specific folder when the type is clear, or `captures/` as a catch-all for quick unsorted captures.

| Folder | Contents | Source | Routing |
|--------|----------|--------|---------|
| `inbox/emails/` | Email staging | Email integrations | Archive after triage |
| `inbox/tickets/` | Work tickets | Ticketing systems | Archive after resolution |
| `inbox/ideas/` | Feature ideas, future projects | Session captures | Percolate until ready for task or archive |
| `inbox/decisions/` | Pending architecture/design decisions | Session captures | Resolve then archive to research/ |
| `inbox/investigations/` | Bugs to research, things to verify | Session captures | Resolve then create task or archive |
| `inbox/captures/` | Quick unsorted captures | Anything | Triage promptly into above folders |

Process inbox items regularly - move to tasks, knowledge, or archive.

### Task Folder Structure

See `tasks/README.md` for full status model (starter 4-status or full 7-status).

| Folder | Contents |
|--------|----------|
| `tasks/` | Active and blocked tasks |
| `tasks/completed/` | Completed tasks (status: complete) |
| `tasks/paused/` | Paused tasks (status: paused) |

Additional folders for full model: `tasks/review/`, `tasks/backlog/`, `tasks/incubating/`

### Archive Structure

Semantic folders ensure everything has a clear home:

| Folder | Contents |
|--------|----------|
| `emails/` | By sender/topic subfolder |
| `tickets/` | Resolved work tickets |
| `research/` | Session research, exploration, setup docs |
| `reports/` | Audits, status reports, investigations |

Create new subfolders when 5+ items of the same type emerge.

## Viewing Your Org

### Org Viewer (Recommended)

A native document browser bundled with this system. Run `org-viewer.exe` from the org root - no configuration needed.

**Features:** TUI-style interface, full-text search, graph view, document editing, code editor, live reload, reminders view.

**Keyboard shortcuts:** `1`-`6` for views, `t` for theme, `e` to edit.

**Remote access:** Install [Tailscale](https://tailscale.com/download) to browse from your phone or other devices.

**Full docs:** [ORG-VIEWER.md](ORG-VIEWER.md) | **Source:** [GitHub](https://github.com/vincitamore/org-viewer)

### Obsidian (Alternative)

If you prefer Obsidian, this workspace can be opened as an Obsidian vault. See `setup/obsidian/README.md` for plugin recommendations and configuration. Obsidian adds Dataview dashboards, graph views with color groups, and optional web publishing.

## Frontmatter Convention

All files use YAML frontmatter as the single source of truth. See `tasks/README.md` for full task model documentation.

**Tasks** (`tasks/*.md`) - Starter Model:
```yaml
---
type: task
status: active | blocked | paused | complete
created: 2026-01-27
completed: null
tags: []
blocked-by: []
---
```

**Tasks** - Full Model (adds review, backlog, incubating statuses):
```yaml
---
type: task
status: active | blocked | review | backlog | incubating | paused | complete
created: 2026-01-27
completed: null
tags: []
blocked-by: []           # for blocked status
review-needed: ""        # for review status - what decision?
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

**Inbox** (`inbox/**/*.md`):
```yaml
---
type: inbox
created: 2026-01-27
source: email | capture | mobile | ticket
---
```

**Reminders** (`reminders/**/*.md`):
```yaml
---
type: reminder
status: pending | snoozed | ongoing | completed | dismissed
created: 2026-02-05
remind-at: 2026-02-06T09:00    # ISO datetime with time
repeat: null | daily | weekly | monthly | custom
repeat-until: null              # ISO date for repeat end
snoozed-until: null             # ISO datetime for snooze
completed: null
tags: []
---
```

**Reminder Status Semantics:**
| Status | Meaning | Folder |
|--------|---------|--------|
| `pending` | Due in future, not yet triggered | `reminders/` |
| `snoozed` | Temporarily delayed | `reminders/` |
| `ongoing` | Recurring reminder, active | `reminders/` |
| `completed` | Marked done | `reminders/completed/` |
| `dismissed` | Skipped/cancelled | `reminders/completed/` |

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

### Session Task Tracking (TodoWrite)

For **multi-step work within a session**, use structured task tracking:

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

### Subagent Orchestration (Task Tool)

For **focused, isolated work**, spawn specialized subagents. Custom agents (in `~/.claude/agents/`) can preload skills and use specific models.

#### Recommended Agent Types

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| `architect` | Design with structural correctness | Planning features, refactoring, architectural decisions |
| `reviewer` | Code review + principle alignment | After writing/modifying code |
| `explorer` | Deep codebase understanding | Before making changes, understanding architecture |
| `distiller` | Extract knowledge worth capturing | After substantive work sessions |

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

# Parallel work (same message = parallel execution)
Task(explorer, "Find all API endpoints")
Task(explorer, "Find all database queries")
```

### File-Based Handoffs (Critical for Dependent Workflows)

**Subagents spawn fresh** - they cannot see previous agents' outputs. For research->synthesis workflows, use explicit file bridges:

```
# WRONG - synthesis agent sees nothing
Task(scholar, "Research X")  → returns to main context
Task(architect, "Synthesize the research above")  → fails

# RIGHT - file bridge
Task(scholar, "Research X. Write to knowledge/x-research.md")
Task(architect, "Read knowledge/x-research.md, synthesize to knowledge/x-synthesis.md")
```

## Workflow

### Adding Items

- **Quick capture**: Drop a file in `inbox/captures/` immediately - sort later
- **Clear task**: Create `tasks/task-name.md` with frontmatter
- **Feature idea**: Add to `inbox/ideas/`
- **Decision needed**: Add to `inbox/decisions/`
- **Bug to investigate**: Add to `inbox/investigations/`
- **Research question**: Add to `queries/`
- **Knowledge**: After conversations with reusable insights, distill to `knowledge/`

### Processing

- Review `inbox/` periodically, move items to appropriate locations
- When tasks complete, move to `tasks/completed/` (preserves history together)
- Extract reusable insights from completed work into `knowledge/`
- Periodically archive old completed tasks to `archive/` if desired

### Maintenance

- Update this file after any structural change
- Update `context/projects.md` when project statuses change
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

See [setup/hooks/maintenance-check.py](setup/hooks/maintenance-check.py) for the full implementation. Copy it to `~/.claude/hooks/` and configure in settings.json.

### Session Start Hook
Automatically read orientation files, compute current state from frontmatter, present context to Claude. Helpful but not critical - Claude can orient manually.

See [setup/README.md](setup/README.md) for full implementations and installation instructions.

## Current State

**Dynamic state lives in [context/current-state.md](context/current-state.md)** - tasks, projects, inbox counts, recently completed. Update that file (not this one) when task/project state changes.

Quick reference: Check `tasks/*.md` for live task state.

### Context Documents

- [context/current-state.md](context/current-state.md) - Dynamic state (tasks, projects, inbox, recent changes)
- [context/voice.md](context/voice.md) - Collaboration style, intellectual coordinates, working relationship
- [context/projects.md](context/projects.md) - Project topology, conceptual threads, cross-connections

---

*Last updated: 2026-02-06*
