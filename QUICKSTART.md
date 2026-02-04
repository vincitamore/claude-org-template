# Quick Start (5 minutes)

Want to start using the system immediately? Here's the fast track.

## 1. Open Claude Code in This Folder

```bash
cd path/to/your-claude-org
claude
```

## 2. Start the Conversation

Say this:

> "I want to set up this organization system. Let's start quick - help me create a minimal voice.md and we can refine it later. Ask me 3-4 key questions."

Claude will ask you questions. Answer them. In 5 minutes you'll have a working `context/voice.md`.

## 3. Capture Something

Drop your first item in `inbox/`:

> "I have a task I've been meaning to do: [describe it]. Create an inbox item for it."

## 4. Start Working

That's it. You now have:
- A voice.md Claude can orient to
- Something in your inbox to process
- A working system

## What Happens Next

As you work with Claude:
- The system will suggest captures to `knowledge/`
- Tasks will accumulate in `tasks/`
- Patterns will emerge for `context/projects.md`
- Your `voice.md` will refine through use

The system grows with you. Start minimal, expand as needed.

---

## If You Want More Structure

Read [ONBOARDING.md](ONBOARDING.md) for the full guided setup process.

## If You Want a Visual Browser

Run `setup/tools/org-viewer.exe` - a native document viewer with search and graph view. For mobile access, add [Tailscale](https://tailscale.com/download). See [setup/tools/README.md](setup/tools/README.md).

## If Something Feels Off

Tell Claude: "Something about how we're working isn't quite right." It will help you articulate the issue and update the relevant documentation.

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
- [ONBOARDING.md](ONBOARDING.md) - Guided 30-60 minute setup
- [context/voice.md](context/voice.md) - Your collaboration preferences
- [setup/](setup/) - Hooks and agents to install
