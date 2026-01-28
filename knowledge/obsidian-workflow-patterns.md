---
type: knowledge
created: 2026-01-27
updated: 2026-01-27
tags: [obsidian, tooling, workflow, publish]
---

# Obsidian Workflow Patterns

Patterns for optimizing Obsidian with the claude-org system.

## Essential Plugin Stack

| Plugin | Purpose |
|--------|---------|
| **Dataview** | Query frontmatter, build live dashboards |
| **Templater** | Dynamic templates with auto-dates, prompted metadata |
| **QuickAdd** | Zero-friction capture via hotkey |
| **Periodic Notes** | Daily/weekly notes as temporal spine |
| **Calendar** | Visual navigation, one-click daily note creation |
| **Homepage** | Auto-open dashboard on launch |
| **Linter** | Auto-format on save |

## Key Architectural Insight

**Computed state over manual state** (Single-Source principle)

The "Current State" section in CLAUDE.md is manually maintained and can drift from reality. Better approach:

- Make frontmatter the **single source of truth**
- Have session-start hook **compute** state by parsing frontmatter
- Obsidian (Dataview) and Claude Code (hooks) both derive from same source
- Eliminates drift, reduces maintenance burden

One source (frontmatter), multiple consumers (dashboard, session context, hooks).

## Dataview Patterns

### Inline Queries

```markdown
Active tasks: `= length(filter(dv.pages('"tasks"'), (p) => p.status == "active"))`
```

### DataviewJS for Complex Logic

```dataviewjs
const tasks = dv.pages('"tasks"')
  .where(p => p.status === "active")
  .sort(t => t.file.mtime, 'desc');
dv.table(["Task", "Tags"], tasks.map(t => [t.file.link, t.tags]));
```

### GROUP BY for Categorized Views

```dataview
TABLE rows.file.link as "Items"
FROM "knowledge"
GROUP BY domain
```

## Useful Dashboard Views

- **Weekly review**: Changes in past 7 days via `file.mtime >= date(today) - dur(7 days)`
- **By domain**: Content grouped by domain tag
- **By principle**: Content tagged with principles
- **Blocked tasks**: Tasks with `status = "blocked"` showing blockers

## Custom Checkbox Conventions

CSS snippets extend markdown task syntax for visual semantic states:

| Syntax | Meaning | Visual |
|--------|---------|--------|
| `- [ ]` | Todo (default) | Empty box |
| `- [x]` | Done (default) | Checkmark |
| `- [/]` | In Progress | Orange half-fill |
| `- [>]` | Blocked/Forwarded | Red arrow |
| `- [?]` | Needs Input | Blue question mark |
| `- [!]` | Important/Urgent | Red exclamation |
| `- [-]` | Cancelled/Won't Do | Gray strikethrough |
| `- [~]` | Partial/In Review | Purple tilde |

**When to use**:
- `[/]` for work actively underway but not complete
- `[>]` for tasks waiting on external dependency or delegated elsewhere
- `[?]` for items needing user decision or clarification
- `[!]` for high-priority items that need attention
- `[-]` for abandoned items (preserves history vs deletion)
- `[~]` for partially complete or pending review

**Example in a task file**:
```markdown
## Checklist
- [x] Research complete
- [/] Implementation in progress
- [>] Blocked by upstream API change
- [?] Need to decide on auth strategy
- [ ] Write tests
- [ ] Documentation
```

These render in both Obsidian app and Publish (CSS included in `publish.css`).

## Workflow Pattern: QuickAdd + Templater

QuickAdd handles **routing** (where does this go?)
Templater handles **content** (what's inside?)

Example flow:
1. Hotkey triggers QuickAdd
2. QuickAdd prompts: "Task or Capture?"
3. Selection routes to appropriate template
4. Templater inserts frontmatter with auto-date and prompts for tags
5. File lands in correct folder, properly formatted

**Note**: Templater folder templates only fire on Obsidian UI file creation. Files created via REST API or direct file write do not trigger Templater. For Claude-driven file creation, use the frontmatter schema documented in CLAUDE.md directly.

## Graph View Optimization

- Filter out `archive/` folder: `-path:archive`
- Color groups by tag (local only, not on Publish)
- Save preferred settings as Workspace

## Obsidian Publish Gotchas

**Dataview doesn't work**: Publish serves static HTML, no plugin execution. Solution: generate static dashboards via script (`generate-publish-dashboard.py`).

**Wikilinks in tables**: `[[path|alias]]` breaks - the pipe `|` is interpreted as table column separator. **Solution**: escape the pipe with backslash: `[[path\|alias]]`.

**Graph doesn't show tags**: Publish graph is simplified - no tag nodes, no color groups. Workaround: generate tag index pages (`generate-tag-pages.py`).

**CSS selectors differ from desktop**: Publish only uses Reading View:
- Use `.markdown-preview-view` or `.markdown-rendered` wrappers
- For custom checkboxes: `li[data-task="X"] > .task-list-item-checkbox::before`
- `.HyperMD-*` and `.cm-*` classes (editor) don't exist on Publish

## Tag Index Pages (Publish Graph Workaround)

The local Obsidian graph shows tags as connecting nodes. Publish's graph doesn't support this. Solution: generate actual markdown files for each tag that contain wikilinks to tagged documents.

**Pattern** (Single-Source instantiation):
- Source: frontmatter `tags: [sovereignty, devops]`
- Derived: `tags/sovereignty.md`, `tags/devops.md` with `[[wikilinks]]`

**Script**: `scripts/generate-tag-pages.py`
```bash
python scripts/generate-tag-pages.py  # Run before publishing
```

**What it does**:
1. Scans all .md files for `tags` in frontmatter
2. Generates `tags/<tag-name>.md` for each unique tag
3. Each tag page contains static wikilinks grouped by document type
4. Cleans up orphaned tag pages when tags are removed

**Result**: Tag pages appear as nodes in Publish graph, connecting related documents.

---

*See `setup/obsidian/README.md` for installation instructions.*
