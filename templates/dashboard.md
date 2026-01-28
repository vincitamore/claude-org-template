---
type: dashboard
---

# Dashboard

> Live view of system health. Requires Obsidian with Dataview plugin.

## Active Tasks

```dataview
TABLE status, tags, created
FROM "tasks"
WHERE status = "active"
SORT created DESC
```

## Blocked Tasks

```dataview
TABLE status, blocked-by, tags
FROM "tasks"
WHERE status = "active" AND blocked-by
SORT created DESC
```

## Inbox (Pending Sort)

```dataview
TABLE source, created
FROM "inbox"
SORT created DESC
LIMIT 10
```

## Recent Knowledge

```dataview
TABLE updated, tags
FROM "knowledge"
SORT updated DESC
LIMIT 5
```

## Recently Completed

```dataview
TABLE completed, tags
FROM "tasks/completed"
SORT completed DESC
LIMIT 5
```

---

*Counts update automatically via Dataview. If queries show errors, ensure Dataview plugin is installed.*
