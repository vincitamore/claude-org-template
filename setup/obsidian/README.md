# Obsidian Integration

> **ONBOARDING Phase 6** (Optional) - Add visual dashboards, graph views, and publishing after the core system is working.

This folder contains configuration and guidance for integrating claude-org with Obsidian.

## Why Obsidian?

Obsidian is optional but powerful for this system:
- **Graph view** visualizes connections between documents
- **Dataview plugin** creates live dashboards from frontmatter
- **Templates** speed up capture
- **Publish** shares your knowledge base (if desired)

The system works without Obsidian using Claude and the command line.

---

## Quick Setup

### 1. Install Obsidian

Download from [obsidian.md](https://obsidian.md) and open this folder as a vault.

### 2. Install Community Plugins

Go to Settings → Community Plugins → Browse and install:

| Plugin | Purpose | Priority |
|--------|---------|----------|
| **Dataview** | Query frontmatter, build dashboards | Essential |
| **Templater** | Dynamic templates with auto-dates | Essential |
| **QuickAdd** | Zero-friction capture via hotkey | Recommended |
| **Calendar** | Visual navigation, daily notes | Recommended |
| **Homepage** | Auto-open dashboard on launch | Optional |
| **Linter** | Auto-format files consistently | Optional |
| **Local REST API** | Enable script automation | For Publish |

### 3. Enable CSS Snippets

1. Settings → Appearance → CSS Snippets
2. Click the folder icon to open snippets folder
3. Copy `.obsidian/snippets/checkboxes.css` to your snippets folder (already there if you cloned)
4. Enable the snippet in settings

This gives you semantic checkboxes:
- `- [/]` In Progress (orange)
- `- [>]` Blocked (red)
- `- [?]` Needs Input (blue)
- `- [!]` Urgent (red)
- `- [-]` Cancelled (gray strikethrough)
- `- [~]` In Review (purple)

### 4. Copy Dashboard Template

Copy `templates/dashboard.md` to your root folder. It contains Dataview queries that show:
- Active tasks
- Blocked tasks
- Active projects
- Recent knowledge
- Inbox items

---

## Plugin Configuration

### Dataview

Settings → Dataview:
- Enable JavaScript queries: ON
- Enable inline queries: ON

### Templater

Settings → Templater:
- Template folder location: `templates`
- Trigger on file creation: ON

### QuickAdd (Optional)

Create capture commands:
1. Settings → QuickAdd → Add Choice → Capture
2. Name: "Quick Capture"
3. File: `inbox/{{DATE}}-capture.md`
4. Template: `templates/inbox.md`

Assign hotkey (e.g., Ctrl+Shift+C) for instant capture.

---

## Obsidian Publish (Optional)

If you want to publish your knowledge base:

### The Problem

Dataview queries don't run on Publish - it's static HTML. Tag nodes don't appear in the Publish graph.

### The Solution

Run `scripts/publish.py` before publishing:

```bash
python scripts/publish.py
```

This script:
1. **Generates tag index pages** (`tags/*.md`) - creates actual files for each tag with wikilinks, making tags appear in the Publish graph
2. **Generates static dashboard** (`publish-dashboard.md`) - renders Dataview queries as plain markdown
3. **Lints files** (optional) - auto-formats via Obsidian Linter
4. **Refreshes Dataview** - updates cached queries
5. **Opens Publish dialog** - ready to review and publish

### Setup for Publish Script

1. Install **Obsidian Local REST API** plugin
2. Copy the API key from plugin settings
3. Create `scripts/.publish-config.json`:
   ```json
   {
     "rest_api_key": "your-api-key-here"
   }
   ```
   Or set environment variable: `OBSIDIAN_REST_API_KEY`

4. Run the workflow:
   ```bash
   python scripts/publish.py           # Full workflow
   python scripts/publish.py --no-lint # Skip linting
   python scripts/publish.py --dry-run # Preview only
   ```

### Publish CSS

For checkboxes to render correctly on Publish, include the CSS in your publish settings or create a `publish.css` file with the contents of `.obsidian/snippets/checkboxes.css`.

---

## Computed State Architecture

The key insight: **frontmatter is the single source of truth**.

Both Obsidian (Dataview) and Claude Code (session-start hook) derive state from frontmatter:

| What | Source | Consumers |
|------|--------|-----------|
| Active Tasks | `tasks/*.md` where `status: active` | Dashboard, session hook |
| Blocked Tasks | `blocked-by` field non-empty | Dashboard, session hook |
| Project Status | `projects/*/README.md` frontmatter | Dashboard, CLAUDE.md |
| Tag Graph | `tags` field in frontmatter | Tag pages, graph view |

This eliminates drift between documentation and reality. Update frontmatter, everything else follows.

---

## Gotchas

### Wikilinks in Tables

The pipe character `|` breaks tables. Escape it:
```markdown
| Column |
|--------|
| [[file\|Display Name]] |  <!-- Note the backslash -->
```

### Graph Colors (Local Only)

Obsidian's graph color groups don't work on Publish. The local graph can color by tag/folder; Publish shows all nodes the same color.

### Templater Doesn't Trigger on Script-Created Files

Files created via Claude or scripts don't trigger Templater. Use the frontmatter schema from CLAUDE.md directly when creating files programmatically.

### YAML Files Don't Render

If you symlink a folder with YAML files (like a knowledge base from another tool), Obsidian won't render them. Generate markdown equivalents.

---

## File Organization

```
.obsidian/
├── snippets/
│   └── checkboxes.css     # Semantic checkbox styling
├── app.json               # App settings
├── appearance.json        # Theme settings
├── core-plugins.json      # Core plugin toggles
└── workspace.json         # Window layout

scripts/
├── generate-tag-pages.py      # Tag → wikilink index pages
├── generate-publish-dashboard.py  # Dataview → static markdown
└── publish.py                 # Full publish workflow

templates/
├── task.md       # New task with frontmatter
├── knowledge.md  # New knowledge article
├── inbox.md      # Quick capture
└── dashboard.md  # Dataview dashboard (copy to root)
```

---

## Further Reading

- [Dataview Documentation](https://blacksmithgu.github.io/obsidian-dataview/)
- [Templater Documentation](https://silentvoid13.github.io/Templater/)
- [Obsidian Publish](https://obsidian.md/publish)
- `knowledge/obsidian-workflow-patterns.md` - detailed patterns and examples
