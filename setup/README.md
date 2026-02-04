# Setup: Infrastructure

> **Navigation**: This folder contains infrastructure referenced by [ONBOARDING.md](../ONBOARDING.md). See the onboarding guide for the full setup journey.

| Component | ONBOARDING Phase | Required? |
|-----------|------------------|-----------|
| [Hooks](#hooks) | Phase 3 | **Essential** |
| [Agents](#agents) | Phase 5 | Optional |
| [Skills](#skills) | Phase 5 | Optional |
| [Org Viewer](#org-viewer) | Phase 6 | Optional |
| [Obsidian](#obsidian) | Phase 6 | Optional |

---

## Hooks

### Maintenance Check (Stop Hook) - ESSENTIAL

> **ONBOARDING Phase 3** - Install this immediately after voice/project discovery.

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

### Dependencies

```bash
pip install PyYAML  # Only needed for session-start.py
```

---

## Agents

> **ONBOARDING Phase 5** (Optional) - Add these after the core system is working.

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

> **ONBOARDING Phase 5** (Optional) - Add these after the core system is working.

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

> **ONBOARDING Phase 6** (Optional) - Native document browser for your org.

A self-contained viewer for your knowledge base. Double-click to open - no configuration needed.

**Features:**
- TUI-style document browser
- Full-text search
- Graph visualization
- Live reload on file changes
- MCP integration for Claude Code

### Quick Start

**Local use:** Just run `setup/tools/org-viewer.exe` - it opens automatically.

**Remote access:** Install [Tailscale](https://tailscale.com/download) to access from other devices.

Full documentation: **[tools/README.md](tools/README.md)**

---

## Obsidian

> **ONBOARDING Phase 6** (Optional) - Add visual dashboards and graph views.

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
| [../knowledge/obsidian-workflow-patterns.md](../knowledge/obsidian-workflow-patterns.md) | Patterns and examples |

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
├── tools/
│   ├── README.md          # Org Viewer documentation
│   └── org-viewer.exe     # Native document viewer (Windows)
└── obsidian/
    └── README.md          # Obsidian integration guide
```

---

## Related

- [../ONBOARDING.md](../ONBOARDING.md) - Full setup journey (references this folder)
- [../QUICKSTART.md](../QUICKSTART.md) - 5-minute fast track
- [../CLAUDE.md](../CLAUDE.md) - System documentation
- [../samples/](../samples/) - Example completed documents
