# Quick Start (5 minutes)

Want to start using the system immediately? Here's the fast track.

## 1. Open Claude Code in This Folder

```bash
cd path/to/your-claude-org
claude
```

## 2. Just Start Talking

Claude will detect that the system hasn't been set up yet and automatically enter onboarding mode. It will ask you questions about how you think, what you're working on, and how you want to collaborate. Just answer honestly.

If for some reason it doesn't auto-detect, say:

> "I want to set up this organization system. Let's start by you helping me figure out how I think and work."

## 3. What Happens

Claude will:
- Ask you questions (5-10 min of conversation)
- Draft your `context/voice.md` (your collaboration preferences)
- Map your projects in `context/projects.md`
- Install the stop hook (the system's immune system)
- Help you capture your first item
- Clean up the template scaffolding

## 4. Start Working

That's it. You now have:
- A voice.md Claude can orient to every session
- Your projects mapped with connections
- A self-maintaining system (via the stop hook)
- Something in your inbox or tasks to work on

## What Happens Next

As you work with Claude:
- Knowledge accumulates in `knowledge/`
- Tasks track in `tasks/`
- The stop hook catches things worth capturing at session end
- Your voice.md and projects.md evolve through use

The system grows with you. Start minimal, expand as needed.

---

## If You Want a Visual Browser

Run `org-viewer.exe` from the org root - a native document viewer with search, graph view, and editing. For mobile access, add [Tailscale](https://tailscale.com/download). See [ORG-VIEWER.md](ORG-VIEWER.md).

## If Something Doesn't Work

**Change it.** Rename folders, modify principles, add inbox categories, restructure whatever you want. The only load-bearing constraint is frontmatter consistency. Everything else is yours.

Or tell Claude: "Something about how we're working isn't quite right." It will help you articulate the issue and update the relevant documentation.

## Core Commands

| Need | Tell Claude |
|------|-------------|
| Quick capture | "Put this in inbox: [thing]" |
| Create task | "Create a task for: [thing]" |
| Capture knowledge | "I learned something about X - let's capture it" |
| Update docs | "voice.md doesn't feel right - let's fix it" |
| Find something | "Where did we document X?" |
| Process inbox | "Let's go through inbox and sort things" |

The system is conversational. Just tell Claude what you need.

---

## Related

- [CLAUDE.md](CLAUDE.md) - Full system documentation and living index
- [ONBOARDING.md](ONBOARDING.md) - The full onboarding playbook (Claude reads this automatically)
- [context/voice.md](context/voice.md) - Your collaboration preferences
- [setup/](setup/) - Hooks and agents to install
