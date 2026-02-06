<!-- If you're Claude, read CLAUDE.md instead - that's your ground truth -->

<p align="center">
  <img src="claude-org-logo.png" alt="Claude-Org Logo" width="200">
</p>

# Claude-Org: Personal Organization System Template

A collaborative organization system for working with Claude Code. Not just a folder structure - a framework for maintaining continuity across sessions through architecture rather than memory.

## The Core Insight

Claude doesn't remember between sessions. But a well-structured workspace creates an "attractor basin" - terrain shaped by consistent thinking that any Claude instance can orient to immediately.

**This system works because the documentation is collaborative.** Claude helps you discover patterns you might not articulate alone. You help Claude understand what matters. The result is more accurate than either could produce independently.

## Getting Started

### Just Open Claude Code

```bash
cd path/to/your-claude-org
claude
```

Claude will automatically detect that the system hasn't been set up and walk you through the onboarding process. It will ask you questions, help you articulate how you think and work, map your projects, install the maintenance hook, and clean up the template scaffolding when done.

**Total setup time:** ~50-65 minutes for a fully initialized system.

Or see [QUICKSTART.md](QUICKSTART.md) for the 5-minute fast track.

## What's Included

```
├── CLAUDE.md              # Living index - ground truth for the workspace
├── ONBOARDING.md          # Onboarding playbook (Claude reads this automatically)
├── QUICKSTART.md          # 5-minute fast track
├── context/
│   ├── voice.md           # Template: your thinking patterns & collaboration preferences
│   ├── projects.md        # Template: project relationships & principle lattice
│   └── current-state.md   # Dynamic state tracking
├── setup/
│   ├── hooks/             # Session-start, maintenance-check scripts
│   ├── agents/            # Architect, reviewer, distiller, explorer definitions
│   ├── skills/            # Organization skill definitions
│   └── obsidian/          # Optional Obsidian integration guide
├── samples/               # Example completed documents (deleted after onboarding)
├── templates/             # Task, knowledge, inbox, reminder file templates
├── inbox/                 # Incoming items (emails, tickets, ideas, decisions, investigations, captures)
├── tasks/                 # Active task tracking
├── reminders/             # Time-based reminders
├── knowledge/             # Distilled insights
├── projects/              # Larger multi-step efforts
└── archive/               # Completed/old items
```

## Make It Yours

The structure is load-bearing; the content is yours to shape. If something doesn't work for you, change it. Rename folders, modify principles, add inbox categories, restructure whatever you want. The only constraint is frontmatter consistency so the tools can parse your files.

1. Work with Claude to develop your [context/voice.md](context/voice.md)
2. Map your projects in [context/projects.md](context/projects.md)
3. Add domain-specific knowledge as you work
4. Install and customize hooks from [setup/hooks/](setup/hooks/)
5. Configure agents from [setup/agents/](setup/agents/)
6. Develop your own principles as patterns emerge

## Org Viewer

A native document browser for your org. Double-click `org-viewer.exe` to open.

Features: TUI-style interface, **document editing**, **code editor** with syntax highlighting, full-text search, graph view, live reload. For remote access from other devices, add [Tailscale](https://tailscale.com/download).

See [ORG-VIEWER.md](ORG-VIEWER.md) | [GitHub](https://github.com/vincitamore/org-viewer)

## Core Principles

Starter principles included - keep what resonates, add your own:

- **Inversion**: Place the complex at the simple point.
- **Sovereignty**: You own your data. Everything local, no SaaS dependency.
- **Structural Correctness**: Architecture that prevents invalid states.
- **Irreducibility**: Compress to essential form. Capture insights, not conversations.
- **Single-Source**: One source of truth, many derived views.
- **Visibility**: What matters should be observable. Archive don't delete.
- **Depth Over Broadcast**: The deepest truths are personal, not public.

## Requirements

- [Claude Code](https://github.com/anthropics/claude-code) CLI
- Optional: [Tailscale](https://tailscale.com/download) for remote access to Org Viewer
- Optional: [Obsidian](https://obsidian.md) with Dataview plugin (alternative to Org Viewer)

## Related Documentation

- [CLAUDE.md](CLAUDE.md) - The living index and ground truth for your workspace
- [ONBOARDING.md](ONBOARDING.md) - The onboarding playbook
- [setup/README.md](setup/README.md) - Hooks, agents, tools, and infrastructure
- [ORG-VIEWER.md](ORG-VIEWER.md) - Org Viewer documentation
- [samples/](samples/) - Example completed documents for reference
- [templates/](templates/) - File templates for tasks, knowledge, inbox items

## License

MIT - Fork it, make it yours.

---

*Built through collaborative practice, not prescription.*
