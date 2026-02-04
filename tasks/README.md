---
type: index
created: 2026-02-03
---
# Tasks

Task management with semantic status tracking. Frontmatter is the single source of truth.

## Status Models

This system supports two task models. Start with **Starter** and upgrade when you need finer distinctions.

### Starter Model (4 Statuses)

| Status | Meaning | Folder |
|--------|---------|--------|
| `active` | Current focus | `tasks/` |
| `blocked` | Waiting on something | `tasks/` |
| `paused` | Deliberately shelved | `tasks/paused/` |
| `complete` | Done | `tasks/completed/` |

Good for: Most users starting out. Handles 80% of task management needs.

### Full Model (7 Statuses)

| Status | Meaning | Folder |
|--------|---------|--------|
| `active` | Current focus, can proceed | `tasks/` |
| `blocked` | Has external dependency | `tasks/` |
| `review` | Needs decision/input to proceed | `tasks/review/` |
| `backlog` | Committed work, not prioritized | `tasks/backlog/` |
| `incubating` | Speculative, exploring viability | `tasks/incubating/` |
| `paused` | Deliberately shelved, will resume | `tasks/paused/` |
| `complete` | Done | `tasks/completed/` |

**Key distinctions** (why 7 > 4):
- **blocked vs review**: `blocked` = waiting on *external* thing; `review` = needs *our* decision
- **backlog vs incubating**: `backlog` = will do; `incubating` = *might* do
- **paused vs backlog**: `paused` = was active, stepped away; `backlog` = never started

**When to upgrade**: When you find yourself wanting to distinguish "I can't proceed because I'm waiting on someone" from "I can't proceed because I need to make a decision."

## State Machine (Full Model)

```
┌─────────────┐
│ incubating  │──── validated ───→┌─────────┐
│ (exploring) │                   │ backlog │
└──────┬──────┘                   │ (queue) │
       │                          └────┬────┘
       │ rejected                      │ prioritized
       ▼                               ▼
┌─────────────┐               ┌────────────┐
│  (deleted)  │               │   active   │◄────────┐
└─────────────┘               │ (working)  │         │
                              └─────┬──────┘         │
                    ┌───────────────┼───────────────┐│
                    │               │               ││
              needs decision   has blocker    step away
                    │               │               ││
                    ▼               ▼               ▼│
              ┌──────────┐   ┌─────────┐     ┌────────┐
              │  review  │   │ blocked │     │ paused │
              │(deciding)│   │(waiting)│     │(shelved)│
              └────┬─────┘   └────┬────┘     └───┬────┘
                   │              │              │
                   └──────────────┴──────────────┘
                              │ resolved
                              ▼
                        ┌──────────┐
                        │ complete │
                        │  (done)  │
                        └──────────┘
```

## Frontmatter Schema

### Starter Model

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

### Full Model (adds these)

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

## Folder Structure

### Starter

```
tasks/
├── README.md       # This file
├── *.md            # active, blocked
├── paused/         # Deliberately shelved
└── completed/      # Done
```

### Full (create folders as needed)

```
tasks/
├── README.md       # This file
├── *.md            # active, blocked
├── review/         # Needs decision/input
├── backlog/        # Committed but not prioritized
├── incubating/     # Speculative, exploring
├── paused/         # Deliberately shelved
└── completed/      # Done
```

## Working with Tasks

### Creating Tasks

Use templates (copy `templates/task.md`) or create manually with frontmatter.

If using MCP tools:
```
org_task_create(title, description, tags)
```

### Status Transitions

| From | To | Trigger |
|------|-----|---------|
| active | blocked | External dependency identified |
| active | paused | Deliberately stepping away |
| active | complete | Work finished |
| blocked | active | Blocker resolved |
| paused | active | Resuming work |

Full model adds:
| From | To | Trigger |
|------|-----|---------|
| incubating | backlog | Validated as worth doing |
| backlog | active | Prioritized for current work |
| active | review | Decision needed |
| review | active | Decision made |

## Related

- [[CLAUDE.md]] - System overview and frontmatter reference
- [[templates/task.md]] - Task file template
