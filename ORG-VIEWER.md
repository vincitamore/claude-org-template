# Org Viewer

A native viewer for your claude-org documents. Double-click to open - no configuration needed.

**GitHub**: https://github.com/vincitamore/org-viewer

![Dashboard](screenshots/org-viewer-dashboard.png)

## What It Does

- **Browse documents** with TUI-style interface (same aesthetic as terminal)
- **Edit documents** directly with nano-style editor
- **Search** full-text across all your org files
- **Graph view** showing document connections
- **Reminders view** with status filtering (key `5`)
- **Live reload** - changes appear instantly

### Keyboard Navigation

| Key | View |
|-----|------|
| `1` | Dashboard |
| `2` | Tasks |
| `3` | Knowledge |
| `4` | Inbox |
| `5` | Reminders |
| `6` | Graph |
| `t` | Cycle theme |
| `e` | Edit document |

### Graph View

Visualize your knowledge graph - see how documents connect through wikilinks and tags:

![Graph View](screenshots/org-viewer-graph.png)

### Tag Pages

Auto-generated tag pages group related documents by topic:

![Tag Page](screenshots/org-viewer-tag-page-example.png)

### Document Editing

Edit documents directly - press `e` or click the Edit button:

![Editor](screenshots/org-viewer-editor.png)

- **Ctrl+S** to save, **Ctrl+X** or **Escape** to exit
- **Tab** to navigate between fields
- Touch-friendly buttons for mobile
- Changes write directly to filesystem

### Themes

Six color themes - press `t` to switch:

![Themes](screenshots/org-viewer-themes.png)

## Quick Start

### Local Use (Same Machine)

Just run it:

```bash
# Windows - double-click or run from terminal
org-viewer.exe

# Specify a different org folder
org-viewer.exe C:\path\to\your\org
```

The viewer opens automatically. That's it.

**macOS/Linux:** Coming soon - Windows only for now.

---

## Remote Access (Optional)

Want to browse your org from your phone or another computer? Set up Tailscale.

### Why Tailscale?

Tailscale creates a secure private network between your devices. Your org-viewer becomes accessible from anywhere without exposing it to the public internet.

### Setup

**1. Install Tailscale** (one-time, on all devices you want to connect):

| Platform | Installation |
|----------|--------------|
| **Windows** | Download from [tailscale.com/download](https://tailscale.com/download) |
| **macOS** | `brew install tailscale` or download from website |
| **Linux** | `curl -fsSL https://tailscale.com/install.sh \| sh` |
| **iOS/Android** | App Store / Play Store |

Sign in with your preferred identity provider. All your devices on the same Tailscale account can reach each other.

**2. Run org-viewer** on your main machine (where your org lives)

**3. Access from other devices** at `http://your-machine-name:3847`

Find your Tailscale machine name with `tailscale status` or in the Tailscale app.

### Install as PWA (Mobile)

On your phone/tablet:
1. Navigate to `http://your-machine-name:3847`
2. **iOS**: Share → Add to Home Screen
3. **Android**: Menu → Install App

The PWA caches documents for offline viewing.

---

## MCP Integration

The MCP server lets Claude Code interact with your org through tools.

### Configuration

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "org-viewer": {
      "command": "node",
      "args": ["path/to/claude-org/tools/mcp/dist/index.js"],
      "env": {
        "ORG_ROOT": "path/to/your/claude-org"
      }
    }
  }
}
```

### Available Tools

**Viewer Tools:**
| Tool | Purpose |
|------|---------|
| `org_viewer_status` | Check if viewer is running |
| `org_viewer_url` | Get local or Tailscale URL |
| `org_viewer_open` | Get URL to specific document |
| `org_viewer_refresh` | Force index rebuild |
| `org_viewer_search` | Search documents |
| `org_viewer_publish` | Generate tag index pages |
| `org_viewer_tag_stats` | Get tag statistics |

**Reminder Tools:**
| Tool | Purpose |
|------|---------|
| `org_reminder_list` | List reminders by status |
| `org_reminder_create` | Create with due datetime |
| `org_reminder_update` | Update time, repeat, tags |
| `org_reminder_complete` | Mark done, move to completed/ |
| `org_reminder_dismiss` | Skip/cancel, move to completed/ |
| `org_reminder_snooze` | Delay until later time |

---

## Architecture

- **Single binary** (~8MB) - no dependencies, no installation
- **Embedded UI** - opens in its own window
- **Rust/Tauri** - native performance
- **React frontend** - TUI-style components
- **WebSocket** - live reload on file changes

---

## Troubleshooting

### Port Already in Use
```bash
# Find what's using port 3847
netstat -ano | findstr :3847

# Kill specific process
taskkill /F /PID <pid>
```

### Remote Access Not Working
1. Verify Tailscale is running on both devices
2. Check `tailscale status` shows both devices online
3. Ping your machine from the remote device
4. Check firewall isn't blocking port 3847

### Documents Not Showing
- Verify markdown files have valid YAML frontmatter
- Check the org-viewer console for parsing errors

---

## Related

- [org-viewer GitHub](https://github.com/vincitamore/org-viewer) - Source code and releases
- [Tailscale Documentation](https://tailscale.com/kb/) - Network setup help
- [ONBOARDING.md](ONBOARDING.md) - Full setup guide
