# Setup: Infrastructure

> **Navigation**: This folder contains infrastructure referenced by [ONBOARDING.md](../ONBOARDING.md). The onboarding playbook handles installation during setup - this document is the reference for manual installation or later modifications.

| Component | Required? | Notes |
|-----------|-----------|-------|
| [Hooks](#hooks) | **Essential** | Stop hook is the system's immune system |
| [Agents](#agents) | Optional | Specialized subagents for focused work |
| [Skills](#skills) | Optional | Quick commands for system management |
| [Org Viewer](#org-viewer) | Recommended | Bundled native document browser |
| [Obsidian](#obsidian) | Alternative | If you prefer Obsidian over Org Viewer |

---

## Hooks

### Maintenance Check (Stop Hook) - ESSENTIAL

The stop hook is the keystone mechanism. Without it, maintenance depends on remembering to do it - which means it won't happen consistently. The hook forces evaluation at every session end, blocking the stop until maintenance is addressed or explicitly declined.

| Hook | File | Purpose |
|------|------|---------|
| **Maintenance Check** | [hooks/maintenance-check.py](hooks/maintenance-check.py) | Force maintenance evaluation before stopping |
| Session Start | [hooks/session-start.py](hooks/session-start.py) | Auto-orient Claude with current state |

### Quick Install

```bash
python setup/install.py
```

This copies hooks and shows you the settings.json configuration.

### Manual Install

**1. Create hooks folder:**
```bash
# macOS/Linux
mkdir -p ~/.claude/hooks

# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\hooks"
```

**2. Copy hooks:**
```bash
# macOS/Linux
cp setup/hooks/*.py ~/.claude/hooks/

# Windows (PowerShell)
Copy-Item setup\hooks\*.py "$env:USERPROFILE\.claude\hooks\"
```

**3. Configure in Claude Code settings.json:**

Find settings.json:
- macOS/Linux: `~/.claude/settings.json`
- Windows: `%USERPROFILE%\.claude\settings.json`

Add:
```json
{
  "hooks": {
    "Stop": {
      "command": "python ~/.claude/hooks/maintenance-check.py",
      "timeout": 5000
    }
  }
}
```

Use the full path appropriate for your OS.

**4. Restart Claude Code** after changing settings.

**5. Verify:** End a session with `/stop`. You should see the maintenance checklist.

---

## Agents

Specialized subagent configurations for focused work:

| Agent | File | Purpose | When to use |
|-------|------|---------|-------------|
| Architect | [agents/architect.md](agents/architect.md) | Design with structural correctness | Planning features, refactoring |
| Reviewer | [agents/reviewer.md](agents/reviewer.md) | Code review + principle alignment | After writing code |
| Distiller | [agents/distiller.md](agents/distiller.md) | Knowledge extraction | After substantive sessions |
| Explorer | [agents/explorer.md](agents/explorer.md) | Deep codebase understanding | Before making changes |

### Installation

1. Create `~/.claude/agents/` (or `%USERPROFILE%\.claude\agents\` on Windows)
2. Create JSON files from the agent definitions

Example `~/.claude/agents/architect.json`:
```json
{
  "name": "architect",
  "model": "opus",
  "description": "Software architect for structural correctness",
  "instructions": "[paste content from agents/architect.md]"
}
```

### Usage

```
Task(architect, "Design the caching layer")
Task(reviewer, "Review the changes I made")
Task(distiller, "What should be captured from this session?")
Task(explorer, "Understand the authentication flow")
```

---

## Skills

The `/org` skill provides quick commands for the organization system:

| Command | Purpose |
|---------|---------|
| `/org` | Full orientation |
| `/org status` | Quick status check |
| `/org capture <text>` | Quick capture to inbox |
| `/org task <desc>` | Create task |
| `/org maintain` | Run maintenance check manually |
| `/org process` | Process inbox items |

### Installation

```bash
# macOS/Linux
cp -r setup/skills/org ~/.claude/skills/

# Windows (PowerShell)
xcopy setup\skills\org %USERPROFILE%\.claude\skills\org /E /I
```

### Files

| File | Purpose |
|------|---------|
| [skills/org/SKILL.md](skills/org/SKILL.md) | Skill definition and commands |
| [skills/org/prompt.md](skills/org/prompt.md) | Full skill prompt |

---

## Org Viewer

A native document browser bundled with this system. Run `org-viewer.exe` from the org root - no configuration needed.

**Features:**
- TUI-style document browser
- Full-text search
- Graph visualization
- Document editing
- Code editor with syntax highlighting
- Live reload on file changes
- Reminders view

### Quick Start

**Local use:** Run `org-viewer.exe` from the org root - it opens automatically.

**Remote access:** Install [Tailscale](https://tailscale.com/download) to access from other devices.

**Customize:** Source on [GitHub](https://github.com/vincitamore/org-viewer) if you want to change the aesthetics and rebuild.

Full documentation: **[ORG-VIEWER.md](../ORG-VIEWER.md)**

---

## Obsidian

> **Alternative to Org Viewer.** If you prefer Obsidian's ecosystem (Dataview, graph views, publishing), this workspace works as an Obsidian vault.

Full Obsidian integration guide: **[obsidian/README.md](obsidian/README.md)**

Quick overview:
- CSS snippets for semantic checkboxes
- Plugin recommendations (Dataview, Templater, QuickAdd)
- Publish workflow scripts
- Gotchas and workarounds

### Key Files

| File | Purpose |
|------|---------|
| [obsidian/README.md](obsidian/README.md) | Complete integration guide |
| [../.obsidian/snippets/checkboxes.css](../.obsidian/snippets/checkboxes.css) | Semantic checkbox styling |
| [../scripts/publish.py](../scripts/publish.py) | Automated publish workflow |
| [../scripts/generate-tag-pages.py](../scripts/generate-tag-pages.py) | Tag index generation |

---

## File Map

```
setup/
├── README.md              # This file - infrastructure index
├── install.py             # Quick installation script
├── hooks/
│   ├── maintenance-check.py   # Stop hook (essential)
│   └── session-start.py       # Auto-orientation (optional)
├── agents/
│   ├── architect.md       # Design agent
│   ├── reviewer.md        # Code review agent
│   ├── distiller.md       # Knowledge extraction agent
│   └── explorer.md        # Codebase exploration agent
├── skills/
│   └── org/
│       ├── SKILL.md       # Skill definition
│       └── prompt.md      # Full skill prompt
└── obsidian/
    └── README.md          # Obsidian integration guide
```

---

## Related

- [../ONBOARDING.md](../ONBOARDING.md) - Onboarding playbook (references this folder)
- [../QUICKSTART.md](../QUICKSTART.md) - 5-minute fast track
- [../CLAUDE.md](../CLAUDE.md) - System documentation
- [../samples/](../samples/) - Example completed documents
