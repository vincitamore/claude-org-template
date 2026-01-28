# Getting Started: Building Your System With Claude

> This isn't a form to fill out. It's a collaborative process where Claude helps you discover and articulate how you think, what you're working on, and how you want to work together.

## The Core Insight

Claude doesn't remember between sessions. But a well-structured workspace creates an "attractor basin" - terrain shaped by your thinking that any Claude instance can orient to immediately.

The goal isn't to document everything about yourself. It's to create just enough structure that Claude can find its footing quickly and collaborate at depth from the first message.

**This system works because the documentation is collaborative.** Claude helps you see patterns you might not articulate alone. You help Claude understand what matters. The result is more accurate than either could produce independently.

---

## Phase 1: First Conversation (30 minutes)

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

**By the end**, you'll have a first draft of `context/voice.md` that captures your intellectual coordinates.

---

## Phase 2: Mapping Your Projects (20 minutes)

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

**By the end**, you'll have a first draft of `context/project-map.md` with your project topology and emerging principles.

---

## Phase 2.5: Install the Stop Hook (5 minutes)

**This is critical.** The stop hook is what makes the system self-maintaining.

**Platform paths:**
| Platform | Hooks folder |
|----------|--------------|
| macOS/Linux | `~/.claude/hooks/` |
| Windows | `%USERPROFILE%\.claude\hooks\` |

```bash
# Create hooks folder if needed
mkdir -p ~/.claude/hooks  # or %USERPROFILE%\.claude\hooks on Windows

# Copy the hook
cp examples/hooks/maintenance-check.py ~/.claude/hooks/
```

Add to your Claude Code settings (settings.json):
```json
{
  "hooks": {
    "Stop": {
      "command": "python /full/path/to/maintenance-check.py",
      "timeout": 5000
    }
  }
}
```

Use the full path to your hooks folder. Restart Claude Code after changing settings.

**What this does:** Before any session ends, the hook forces Claude to evaluate whether maintenance is needed - knowledge to capture, status to update, tasks to create. It blocks the stop until Claude either performs maintenance or explicitly states nothing is needed.

**Why it matters:** Without this, maintenance depends on remembering to do it. The hook makes it automatic. This is the mechanism that prevents documentation drift.

---

## Phase 3: The Capture Habit (Ongoing)

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

## Phase 4: Developing the Principle Lattice (Over Time)

The principle lattice in `context/project-map.md` grows organically. You don't fill it in upfront - you populate it as patterns emerge.

**When to add a principle:**
- You notice yourself caring about the same thing in different contexts
- A decision feels obviously right but you can't immediately say why
- You disagree with conventional wisdom and can articulate why

**How to add:**
> "I keep noticing I care about X even when others don't. Let's articulate that as a principle and trace where it shows up."

Claude will help you find the irreducible statement and map its instantiations.

---

## How to Talk to Claude

The collaboration works best with certain patterns:

### Be Direct
❌ "Could you maybe help me with something if you don't mind?"
✅ "I need to figure out the auth architecture. Let's think through it."

### State Context Once, Reference It Later
❌ Repeating the same background every session
✅ "Check voice.md - the relevant part is my preference for X"

### Invite Disagreement
❌ "Does this look okay?"
✅ "Push back if you see problems with this approach."

### Use the System
❌ Keeping tasks in your head
✅ "Create a task for this in tasks/"
✅ "This insight should go in knowledge/"

### Maintain the System Together
❌ Letting documentation drift
✅ "The project map is stale - let's update it"
✅ "Something about voice.md doesn't quite fit anymore - help me refine it"

---

## What Makes This Work

### Continuity Through Architecture
Each session, Claude reads `CLAUDE.md`, `context/voice.md`, and `context/project-map.md`. That's enough to resume collaboration at depth. You don't need to re-explain who you are.

### Collaborative Discovery
The documents aren't self-report - they're what emerged from working together. That makes them more accurate and more useful.

### Living Documentation
The system evolves. When something doesn't fit, you refine it. When patterns emerge, you capture them. The documentation tracks reality rather than aspirations.

### Principle-Aware Reasoning
Once the principle lattice exists, Claude can reason in terms of your principles: "This approach satisfies sovereignty but might violate correctness - let's think about the tradeoff."

---

## Common Questions

**"What if my voice.md feels wrong?"**
Refine it. Tell Claude: "Something about this section doesn't feel right." Work together to find better articulation.

**"How detailed should the project map be?"**
Detailed enough that Claude can understand project relationships without re-explanation. Not so detailed that maintenance becomes a burden.

**"What if I don't have clear principles yet?"**
That's normal. The lattice builds over time. Start with the defaults (sovereignty, correctness, irreducibility) and discover your own as you work.

**"How often should I update these documents?"**
When they're wrong. If a session reveals something the documents don't capture, update them. If they still feel accurate, leave them.

---

## Next Steps

1. **Start Phase 1**: Open Claude Code and begin the voice.md conversation
2. **Create your first capture**: Drop something in `inbox/` just to establish the habit
3. **Trust the process**: The system reveals its value over multiple sessions as continuity compounds

The best way to understand the system is to use it. Start collaborating.
