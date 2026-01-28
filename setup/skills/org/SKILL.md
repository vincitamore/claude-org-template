# /org - Organization & Continuity Skill

> A skill for managing the claude-org system. Handles orientation, captures, tasks, knowledge, and maintenance.

## Installation

Copy this folder to `~/.claude/skills/org/` for global availability, or `.claude/skills/org/` for project-specific.

## Commands

### Orientation
```
/org                    # Full orientation - read CLAUDE.md, voice.md, projects.md
/org status             # Quick status - active tasks, inbox count, recent activity
```

### Capture
```
/org capture <text>     # Quick capture to inbox/
/org task <description> # Create task in tasks/
/org learn <topic>      # Start knowledge capture for topic
```

### Maintenance
```
/org maintain           # Run maintenance check manually
/org process            # Process inbox items
/org update             # Update CLAUDE.md with current state
```

---

## Skill Definition

```yaml
name: org
description: Organization & continuity system - orientation, captures, tasks, knowledge
commands:
  - name: default
    description: Full orientation
  - name: status
    description: Quick status check
  - name: capture
    description: Quick capture to inbox
    args: text
  - name: task
    description: Create task
    args: description
  - name: learn
    description: Start knowledge capture
    args: topic
  - name: maintain
    description: Run maintenance check
  - name: process
    description: Process inbox items
  - name: update
    description: Update CLAUDE.md
```

---

## Implementation Notes

The skill prompts below are templates. Customize them for your workflow.

### Key Behaviors

1. **Orientation** reads the attractor basin documents and presents current state
2. **Capture** creates files with proper frontmatter, doesn't overthink categorization
3. **Tasks** creates properly structured task files with status tracking
4. **Knowledge** guides the distillation process, not just file creation
5. **Maintenance** runs the same checklist as the stop hook

### Integration Points

- Works with the stop hook (maintenance check)
- Works with the session start hook (orientation)
- Respects frontmatter conventions
- Maintains CLAUDE.md as living index
