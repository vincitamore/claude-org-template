<p align="center">
  <img src="claude-org-logo.png" alt="Claude-Org Logo" width="200">
</p>

# Claude-Org: Personal Organization System Template

A collaborative organization system for working with Claude Code. Not just a folder structure - a framework for maintaining continuity across sessions through architecture rather than memory.

## The Core Insight

Claude doesn't remember between sessions. But a well-structured workspace creates an "attractor basin" - terrain shaped by consistent thinking that any Claude instance can orient to immediately.

**This system works because the documentation is collaborative.** Claude helps you discover patterns you might not articulate alone. You help Claude understand what matters. The result is more accurate than either could produce independently.

## What's Included

```
├── CLAUDE.md              # Living index - ground truth for the workspace
├── ONBOARDING.md          # Guided collaborative setup process
├── QUICKSTART.md          # 5-minute fast track
├── context/
│   ├── voice.md           # Template: your thinking patterns & collaboration preferences
│   ├── project-map.md     # Template: project relationships & principle lattice
│   └── claude-meta.md     # Meta-instructions for Claude's role as collaborator
├── examples/
│   ├── hooks/             # Session-start, maintenance-check scripts
│   └── agents/            # Architect, reviewer, distiller, explorer definitions
├── templates/             # Task, knowledge, inbox file templates
├── inbox/                 # Quick captures, unsorted items
├── tasks/                 # Active task tracking
├── knowledge/             # Distilled insights
└── archive/               # Completed/old items
```

## Getting Started

### Quick Start (5 minutes)
See `QUICKSTART.md` - open Claude Code and start collaborating immediately.

### Full Onboarding (30-60 minutes)
See `ONBOARDING.md` - guided process for discovering your voice and mapping your projects.

## Core Principles

These aren't decoration - they're operational constraints that make the system work:

- **Sovereignty (⊕)**: You own your data. Everything local, no SaaS dependency.
- **Structural Correctness (≡)**: Architecture that prevents invalid states.
- **Irreducibility (Σ→1)**: Compress to essential form. Capture insights, not conversations.
- **Single-Source (1→7)**: One source of truth, many derived views.
- **Visibility (∮)**: What matters should be observable. Archive don't delete.

## The Collaborative Relationship

This system treats Claude as a **collaborative thinker**, not a service provider:

- Claude helps discover and articulate your patterns
- Claude actively maintains system health
- Claude pushes back when something seems wrong
- Claude suggests captures and refinements
- You refine together, not fill in forms

See `context/claude-meta.md` for the full philosophy.

## Requirements

- [Claude Code](https://github.com/anthropics/claude-code) CLI
- Optional: [Obsidian](https://obsidian.md) with Dataview plugin for visualization

## Customization

The structure is load-bearing; the content is yours to shape:

1. Work with Claude to develop your `context/voice.md`
2. Map your projects in `context/project-map.md`
3. Add domain-specific knowledge as you work
4. Install and customize hooks from `examples/hooks/`
5. Configure agents from `examples/agents/`
6. Develop your own principles as patterns emerge

## License

MIT - Fork it, make it yours.

---

*Built through collaborative practice, not prescription.*
