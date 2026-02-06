# Org Viewer

A native viewer for your claude-org documents. Double-click to open - no configuration needed.

**GitHub**: https://github.com/vincitamore/org-viewer

![Dashboard](screenshots/org-viewer-dashboard.png)

## What It Does

- **Browse documents** with TUI-style interface (same aesthetic as terminal)
- **Edit documents** directly with nano-style editor
- **Code editor** with syntax highlighting for 12+ languages (key `7`)
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
| `7` | Code |
| `t` | Cycle theme |
| `e` | Edit document |

### Code Editor

Browse and edit project source code with syntax highlighting:

![Code Editor](screenshots/org-viewer-code.png)

- **12+ language packs**: TypeScript, Rust, Python, JSON, CSS, HTML, and more
- **Project file browser** with type badges and file sizes
- **Theme-aware syntax highlighting** — matches your active terminal theme
- **Inline editing**: `e` to edit, `Ctrl+S` to save, `Ctrl+B` to toggle sidebar

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

**2. Generate TLS certificates** for your Tailscale hostname:

```bash
# Find your machine's Tailscale hostname
tailscale status

# Generate certs (replace with your actual hostname)
tailscale cert your-machine.your-tailnet.ts.net
```

This creates `your-machine.your-tailnet.ts.net.crt` and `.key` files in the current directory.

**3. Set environment variables** before launching org-viewer:

```bash
# Windows (cmd)
set ORG_VIEWER_TLS_CERT=C:\path\to\your-machine.your-tailnet.ts.net.crt
set ORG_VIEWER_TLS_KEY=C:\path\to\your-machine.your-tailnet.ts.net.key

# PowerShell
$env:ORG_VIEWER_TLS_CERT = "C:\path\to\your-machine.your-tailnet.ts.net.crt"
$env:ORG_VIEWER_TLS_KEY = "C:\path\to\your-machine.your-tailnet.ts.net.key"
```

**4. Run org-viewer** on your main machine (where your org lives)

**5. Access from other devices** at `https://your-machine.your-tailnet.ts.net:3848`

> **Without TLS certs**: The viewer still works locally at `http://localhost:3847`, but remote browsers may block mixed content over plain HTTP. TLS is recommended for Tailscale access.

### Install as PWA (Mobile)

On your phone/tablet:
1. Navigate to `https://your-machine.your-tailnet.ts.net:3848`
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

- **Single binary** (~17MB) - no dependencies, no installation
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
3. Verify TLS env vars are set: `ORG_VIEWER_TLS_CERT` and `ORG_VIEWER_TLS_KEY`
4. Check the log file (`%TEMP%\org-viewer.log`) for TLS errors
5. Regenerate certs if expired: `tailscale cert your-machine.your-tailnet.ts.net`
6. Ping your machine from the remote device
7. Check firewall isn't blocking ports 3847 (HTTP) and 3848 (HTTPS)

### Documents Not Showing
- Verify markdown files have valid YAML frontmatter
- Check the org-viewer console for parsing errors

---

## Related

- [org-viewer GitHub](https://github.com/vincitamore/org-viewer) - Source code and releases
- [Tailscale Documentation](https://tailscale.com/kb/) - Network setup help
- [ONBOARDING.md](ONBOARDING.md) - Full setup guide
