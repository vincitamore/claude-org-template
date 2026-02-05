---
type: index
created: {{date}}
---
# Reminders

Time-based reminder system with due dates, snoozing, and repeating support.

## Status Taxonomy

| Status | Meaning | Folder |
|--------|---------|--------|
| `pending` | Due in future, not yet triggered | `reminders/` |
| `snoozed` | Temporarily delayed | `reminders/` |
| `ongoing` | Recurring reminder, active | `reminders/` |
| `completed` | Marked done | `reminders/completed/` |
| `dismissed` | Skipped/cancelled | `reminders/completed/` |

## Frontmatter Schema

```yaml
---
type: reminder
status: pending | snoozed | ongoing | completed | dismissed
created: 2026-02-05
remind-at: 2026-02-06T09:00    # ISO datetime with time component
repeat: null | daily | weekly | monthly | custom
repeat-until: null              # ISO date for repeat end
snoozed-until: null             # ISO datetime for snooze end
completed: null                 # date when completed
tags: []
---
```

## Working with Reminders

### Creating Reminders

Using MCP tools:
```
org_reminder_create(title="Call dentist", remindAt="2026-02-06T09:00")
org_reminder_create(title="Weekly review", remindAt="2026-02-07T10:00", repeat="weekly")
```

Or create manually with the template at `templates/reminder.md`.

### Snoozing

```
org_reminder_snooze(path="reminders/call-dentist.md", until="2026-02-06T14:00")
```

### Completing/Dismissing

```
org_reminder_complete(path="reminders/call-dentist.md")
org_reminder_dismiss(path="reminders/old-reminder.md")
```

## Session Integration

Due and overdue reminders appear at session start with "ACTION REQUIRED" alert.

## Org Viewer

Access reminders in org-viewer with keyboard shortcut `5`. Filter by status:
- pending, snoozed, ongoing, completed, dismissed

Reminders appear as red/salmon nodes in the graph view, making time-sensitive items visually distinct.
