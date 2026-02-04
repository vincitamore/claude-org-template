# Getting Started: Building Your System With Claude

> This isn't a form to fill out. It's a collaborative process where Claude helps you discover and articulate how you think, what you're working on, and how you want to work together.

## The Core Insight

Claude doesn't remember between sessions. But a well-structured workspace creates an "attractor basin" - terrain shaped by your thinking that any Claude instance can orient to immediately.

The goal isn't to document everything about yourself. It's to create just enough structure that Claude can find its footing quickly and collaborate at depth from the first message.

**This system works because the documentation is collaborative.** Claude helps you see patterns you might not articulate alone. You help Claude understand what matters. The result is more accurate than either could produce independently.

---

## Setup Overview

| Phase | What | Time | Required? |
|-------|------|------|-----------|
| 1 | [Voice Discovery](#phase-1-voice-discovery) | 30 min | Yes |
| 2 | [Project Mapping](#phase-2-project-mapping) | 20 min | Yes |
| 3 | [Stop Hook](#phase-3-install-the-stop-hook) | 5 min | **Essential** |
| 4 | [Capture Habit](#phase-4-the-capture-habit) | Ongoing | Yes |
| 5 | [Agents & Skills](#phase-5-agents--skills-optional) | 15 min | Optional |
| 6 | [Org Viewer](#phase-6-org-viewer-optional) | 10 min | Optional |
| 7 | [Obsidian](#phase-7-obsidian-integration-optional) | 30 min | Optional |
| 8 | [Principle Lattice](#phase-8-developing-the-principle-lattice) | Ongoing | Grows naturally |

**Minimum viable setup**: Phases 1-4. Everything else enhances but isn't required.

---

## Phase 1: Voice Discovery

Open Claude Code in this workspace and start with something like:

> "I want to set up this organization system. Let's start by you helping me figure out how I think and work. Ask me questions."

**What Claude will do:**
- Ask about your projects, interests, and work patterns
- Probe for recurring themes and concerns
- Help you notice what you care about across different domains
- Start drafting `context/voice.md` based on what emerges

**What you should do:**
- Answer honestly, not aspirationally
- Mention what frustrates you in collaborations
- Talk about recent work that felt satisfying or unsatisfying
- Let tangents happen - they often reveal important patterns

**By the end**, you'll have a first draft of [context/voice.md](context/voice.md).

### Questions Claude Might Ask

**How you think:**
- What domains do you move between? (technical, creative, philosophical, practical)
- What patterns recur across your interests?
- What do you find yourself caring about that others overlook?

**How you collaborate:**
- What communication style resonates with you?
- What behaviors from assistants/collaborators frustrate you?
- What does productive disagreement look like?

**Discovery prompts that help:**
- "What's a recent project that felt particularly satisfying? What made it work?"
- "When you look at someone else's code/writing/system, what catches your eye first?"
- "What problems keep coming back across different areas of your work?"

---

## Phase 2: Project Mapping

Next conversation (or continuing):

> "Let's map my current projects and find the threads that connect them."

**What Claude will do:**
- List what you're working on
- Look for shared concerns, technologies, patterns
- Group projects by conceptual thread
- Help you see the topology of your work

**What to share:**
- Active projects and their current state
- Past projects that still inform your thinking
- Ideas you haven't started but keep returning to
- Frustrations with how projects relate (or don't)

**By the end**, you'll have a first draft of [context/projects.md](context/projects.md).

---

## Phase 3: Install the Stop Hook

**This is the keystone.** The stop hook is what makes the system self-maintaining rather than discipline-dependent.

Without it, maintenance (capturing knowledge, updating status, creating tasks) depends on remembering to do it - which means it won't happen consistently. The hook forces evaluation at every session end.

### Quick Install

```bash
python setup/install.py
```

This copies the hook and shows you what to add to settings.json.

### Manual Install

See [setup/README.md](setup/README.md) for detailed instructions.

**What the hook does:** Before any session ends, it forces Claude to evaluate:
- New knowledge to capture?
- Project status changed?
- Tasks to create?
- Questions worth preserving?

It blocks the stop until Claude either performs maintenance or explicitly states nothing is needed.

### Verify It Works

End a session with `/stop`. You should see the maintenance checklist appear.

---

## Phase 4: The Capture Habit

Now the system is ready to use. The most important habit:

**Capture immediately, sort later.**

When something comes up:
- Quick thought → `inbox/`
- Clear task → `tasks/`
- Reusable insight → `knowledge/`

Don't overthink categorization. The `inbox/` exists so you can capture without friction. Sorting happens later, often with Claude's help.

**Practice prompts:**
- "I just learned something about X - help me capture it in knowledge/"
- "This task is getting complex - let's break it into tracked subtasks"
- "I have five things floating in my head - help me get them into inbox/"

---

## Phase 5: Agents & Skills (Optional)

Once the core system is working, you can add specialized subagents and skills.

### Agents

Focused subagents for specific types of work:

| Agent | Purpose | When to use |
|-------|---------|-------------|
| **architect** | Design with structural correctness | Planning features, refactoring decisions |
| **reviewer** | Code review + principle alignment | After writing code |
| **distiller** | Extract knowledge worth capturing | After substantive sessions |
| **explorer** | Deep codebase understanding | Before making changes |

**Installation:** See [setup/README.md#agents](setup/README.md#agents)

**Usage:**
```
Task(architect, "Design the caching layer")
Task(reviewer, "Review the auth changes")
```

### Skills

The `/org` skill provides quick commands:

```
/org              # Full orientation
/org status       # Quick status check
/org capture X    # Quick capture to inbox
/org task X       # Create task
/org maintain     # Run maintenance check manually
```

**Installation:** See [setup/README.md#skills](setup/README.md#skills)

---

## Phase 6: Org Viewer (Optional)

A native document browser for your org. Double-click to open.

**What Org Viewer adds:**
- Browse documents with TUI-style interface
- Full-text search across all files
- Graph view showing document connections
- Live reload on file changes
- MCP integration for Claude Code

**Local use:** Just run `setup/tools/org-viewer.exe` - it opens automatically.

**Remote access (optional):** Install [Tailscale](https://tailscale.com/download) to browse from your phone or other devices. Access at `http://your-machine-name:3847` and install as a PWA.

**Full guide:** [setup/tools/README.md](setup/tools/README.md)

---

## Phase 7: Obsidian Integration (Optional)

If you want visual dashboards, graph views, and publishing:

**What Obsidian adds:**
- Graph view of document connections
- Live Dataview dashboards
- Quick capture via hotkeys
- Optional publishing to the web

**Quick setup:**
1. Open this folder as an Obsidian vault
2. Install plugins: Dataview, Templater, QuickAdd
3. Enable CSS snippet for semantic checkboxes
4. Copy `templates/dashboard.md` to root

**Full guide:** [setup/obsidian/README.md](setup/obsidian/README.md)

**Publish workflow:** If using Obsidian Publish, see `scripts/publish.py` for automation.

---

## Phase 8: Developing the Principle Lattice

The principle lattice in [context/projects.md](context/projects.md) grows organically. You don't fill it in upfront - you populate it as patterns emerge.

**When to add a principle:**
- You notice yourself caring about the same thing in different contexts
- A decision feels obviously right but you can't immediately say why
- You disagree with conventional wisdom and can articulate why

**How to add:**
> "I keep noticing I care about X even when others don't. Let's articulate that as a principle and trace where it shows up."

Claude will help you find the irreducible statement and map its instantiations.

### Maintaining the Lattice

Once you have 3+ principles, review periodically:
- **Target 5-9 principles** - fewer suggests incomplete articulation, more suggests conflation
- **3-8 instantiations per principle** - fewer is just a preference, more is too broad
- **Domain coverage** - mature principles appear across multiple domains
- **Compression test** - can one principle derive another? Merge them.

---

## How to Talk to Claude

### Be Direct
❌ "Could you maybe help me with something if you don't mind?"
✅ "I need to figure out the auth architecture. Let's think through it."

### State Context Once, Reference Later
❌ Repeating the same background every session
✅ "Check voice.md - the relevant part is my preference for X"

### Invite Disagreement
❌ "Does this look okay?"
✅ "Push back if you see problems with this approach."

### Use the System
❌ Keeping tasks in your head
✅ "Create a task for this in tasks/"
✅ "This insight should go in knowledge/"

### Maintain Together
❌ Letting documentation drift
✅ "The project map is stale - let's update it"
✅ "Something about voice.md doesn't fit anymore - help me refine it"

---

## What Makes This Work

**Continuity Through Architecture** - Each session, Claude reads CLAUDE.md, voice.md, and projects.md. That's enough to resume collaboration at depth.

**Collaborative Discovery** - The documents aren't self-report. They emerged from working together, making them more accurate.

**Living Documentation** - The system evolves. When something doesn't fit, refine it. When patterns emerge, capture them.

**Forcing Functions** - The stop hook converts optional maintenance into mandatory checkpoints. Structure beats discipline.

---

## Common Questions

**"What if my voice.md feels wrong?"**
Refine it. Tell Claude: "Something about this section doesn't feel right." Work together to find better articulation.

**"How detailed should the project map be?"**
Detailed enough that Claude understands relationships without re-explanation. Not so detailed that maintenance becomes a burden.

**"What if I don't have clear principles yet?"**
Normal. The lattice builds over time. Start with the defaults (sovereignty, correctness, irreducibility) and discover your own as you work.

**"How often should I update these documents?"**
When they're wrong. If a session reveals something the documents don't capture, update them. If they still feel accurate, leave them.

---

## Quick Reference

| Resource | Purpose |
|----------|---------|
| [CLAUDE.md](CLAUDE.md) | Full system documentation |
| [QUICKSTART.md](QUICKSTART.md) | 5-minute fast track |
| [setup/README.md](setup/README.md) | Hooks, agents, skills, tools |
| [setup/tools/README.md](setup/tools/README.md) | Org Viewer documentation |
| [setup/obsidian/README.md](setup/obsidian/README.md) | Obsidian integration |
| [samples/](samples/) | Example completed documents |
| [templates/](templates/) | File templates |
| [knowledge/obsidian-workflow-patterns.md](knowledge/obsidian-workflow-patterns.md) | Obsidian patterns |

---

## First Session Success Criteria

By the end of your first real session (after setup), you should have:

- [ ] **voice.md populated** - At least 3 sections filled with concrete, specific content (not placeholders)
- [ ] **Stop hook working** - When you end with `/stop`, you see the maintenance checklist
- [ ] **One capture made** - Something in `inbox/` or a task in `tasks/`
- [ ] **One knowledge article** - Even a small one, to establish the pattern

**Signs it's working:**
- Claude references your voice.md naturally in conversation
- The maintenance prompt catches something you would have forgotten
- You find yourself thinking "I should capture this" during work

**Signs something's off:**
- Claude keeps asking about your preferences (voice.md not detailed enough)
- Sessions end without any maintenance (hook not installed or threshold too high)
- You're not sure where to put things (review CLAUDE.md folder structure)

---

## Next Steps

1. **Start Phase 1**: Open Claude Code and begin the voice.md conversation
2. **Install the hook** (Phase 3): This is non-negotiable for system health
3. **Create your first capture**: Drop something in `inbox/` to establish the habit
4. **Trust the process**: The system reveals its value over multiple sessions

The best way to understand the system is to use it. Start collaborating.
