# Setup: Infrastructure

This folder contains infrastructure for the organization system. These aren't examples - they're the forcing functions that make the system work.

**Install the hooks first.** The stop hook is what makes the system self-maintaining rather than discipline-dependent.

---

## Hooks

### Maintenance Check (Stop Hook) - ESSENTIAL

**Install this immediately.** Without it, maintenance (capturing knowledge, updating status, creating tasks) depends on remembering to do it - which means it won't happen consistently.

The hook forces evaluation at the end of every session, blocking the stop until maintenance is addressed or explicitly declined. This is the mechanism that prevents documentation drift.

| Hook | File | Purpose |
|------|------|---------|
| **Maintenance Check** | [hooks/maintenance-check.py](hooks/maintenance-check.py) | Force maintenance evaluation before stopping |
| Session Start | [hooks/session-start.py](hooks/session-start.py) | Auto-orient Claude with current state |

### Quick Install

Run the installation script:

```bash
python setup/install.py
```

Or install manually:

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

**Dependencies:**
```bash
pip install PyYAML  # Only needed for session-start.py
```

---

## Agents

Specialized subagent configurations for focused work.

| Agent | File | Purpose |
|-------|------|---------|
| Architect | [agents/architect.md](agents/architect.md) | Design with structural correctness |
| Reviewer | [agents/reviewer.md](agents/reviewer.md) | Code review + principle alignment |
| Distiller | [agents/distiller.md](agents/distiller.md) | Knowledge extraction |
| Explorer | [agents/explorer.md](agents/explorer.md) | Deep codebase understanding |

### Installation

1. Create `~/.claude/agents/`
2. Create JSON files from the agent definitions

Example `~/.claude/agents/architect.json`:
```json
{
  "name": "architect",
  "model": "opus",
  "description": "Software architect for structural correctness",
  "instructions": "[content from agents/architect.md]"
}
```

### Usage

```
Task(architect, "Design the caching layer")
Task(reviewer, "Review the changes I made")
Task(distiller, "What should be captured?")
```

---

## Skills

The `/org` skill provides quick commands for the organization system.

| Skill | File | Purpose |
|-------|------|---------|
| org | [skills/org/](skills/org/) | Organization & continuity commands |

### Installation

Copy to `~/.claude/skills/`:

```bash
# macOS/Linux
cp -r setup/skills/org ~/.claude/skills/

# Windows
xcopy setup\skills\org %USERPROFILE%\.claude\skills\org /E /I
```

---

## Related

- [../CLAUDE.md](../CLAUDE.md) - System documentation
- [../ONBOARDING.md](../ONBOARDING.md) - Guided setup process
- [../samples/](../samples/) - Reference examples of completed documents
