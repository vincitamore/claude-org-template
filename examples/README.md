# Examples: Hooks and Agents

This folder contains example implementations of hooks and agent definitions that extend the organization system.

## Hooks

Hooks are scripts that run at specific points in a Claude Code session.

### ⚠️ The Stop Hook is Essential

**Install `maintenance-check.py` first.** This hook is what makes the system self-maintaining.

Without it, maintenance (capturing knowledge, updating status, creating tasks) depends on discipline - which means it won't happen consistently. The stop hook forces evaluation at the end of every session, blocking the stop until maintenance is addressed.

This is the difference between a system that drifts and one that stays accurate.

### Available Examples

| Hook | File | Purpose | Priority |
|------|------|---------|----------|
| **Maintenance Check** | `hooks/maintenance-check.py` | Force maintenance evaluation before stopping | **ESSENTIAL** |
| Session Start | `hooks/session-start.py` | Auto-orient Claude with current state | Helpful |

### Installation

**Dependencies:**
```bash
pip install PyYAML  # Only needed for session-start.py
```

**Platform paths:**
| Platform | Hooks folder |
|----------|--------------|
| macOS/Linux | `~/.claude/hooks/` |
| Windows | `%USERPROFILE%\.claude\hooks\` |
| Windows (git bash) | `~/.claude/hooks/` |

**Steps:**
1. Create hooks folder if it doesn't exist
2. Copy hook files to hooks folder
3. Configure in Claude Code settings (settings.json or via UI):

```json
{
  "hooks": {
    "SessionStart": {
      "command": "python path/to/session-start.py",
      "timeout": 5000
    },
    "Stop": {
      "command": "python path/to/maintenance-check.py",
      "timeout": 5000
    }
  }
}
```

Replace `path/to/` with your actual hooks folder path.

### Customization

Edit the Python files to:
- Add workspace-specific context
- Integrate with your tooling (MCPs, etc.)
- Adjust what state gets computed and presented

---

## Agents

Agents are specialized subagent configurations that Claude can spawn for focused work.

### Available Examples

| Agent | File | Purpose |
|-------|------|---------|
| Architect | `agents/architect.md` | Design with structural correctness |
| Reviewer | `agents/reviewer.md` | Code review + principle alignment |
| Distiller | `agents/distiller.md` | Knowledge extraction |
| Explorer | `agents/explorer.md` | Deep codebase understanding |

### Installation

1. Create `~/.claude/agents/` if it doesn't exist
2. For each agent, create a JSON file with the definition from the example

Example `~/.claude/agents/architect.json`:
```json
{
  "name": "architect",
  "model": "opus",
  "description": "Software architect for designing implementations with structural correctness",
  "instructions": "You are an architect focused on structural correctness..."
}
```

### Usage

Once installed, invoke agents with the Task tool:

```
Task(architect, "Design the caching layer for this API")
Task(reviewer, "Review the changes I just made")
Task(distiller, "What from this session should be captured?")
Task(explorer, "Understand the authentication flow")
```

### Customization

Adapt the agent instructions to:
- Reference your specific principles
- Include domain-specific guidance
- Integrate with your knowledge base
- Match your collaboration preferences

---

## Creating Your Own

### Custom Hooks

Hooks can be any executable. They receive workspace context via environment variables:
- `CLAUDE_WORKSPACE` - Path to current workspace

Output is passed to Claude as context. Exit code 0 means success; non-zero can be used to block actions (like the maintenance check blocking stop).

### Custom Agents

Agent definitions support:
- `name` - How to invoke it
- `model` - Which model to use (opus, sonnet, haiku)
- `description` - Shown in agent listings
- `instructions` - System prompt for the agent
- `skills` - Skills to preload (optional)

Design agents for specific tasks where isolated focus helps. The general pattern:
1. Give it a clear purpose
2. Tell it what principles to apply
3. Specify what output format you expect

---

## Philosophy

Hooks and agents extend Claude's capabilities while maintaining the collaborative relationship:

- **Hooks** automate system maintenance so neither of you has to remember
- **Agents** provide focused expertise without polluting main conversation context
- **Both** should embody the principles (≡, ⊕, Σ→1) rather than just execute commands

When creating custom hooks/agents, ask: "Does this help maintain the system's health and the collaboration's quality?"
