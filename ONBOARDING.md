# Onboarding Playbook

> **This document is for Claude, not the user.** When you detect that this system hasn't been initialized yet (voice.md still has placeholder text), read this document and run the onboarding sequence below. The user's job is to answer your questions. Your job is to run a great onboarding, synthesize their answers into the right files, and clean up when done.

---

## Detection

You're in onboarding mode if ANY of these are true:
- `context/voice.md` contains `_..._` placeholder text
- `context/projects.md` contains `_..._` placeholder text
- `context/current-state.md` still says `_None yet_`

If all three documents are populated with real content, onboarding is complete. Skip this document entirely.

---

## The Goal

By the end of onboarding, the user should have:
- A populated `context/voice.md` that lets any future Claude instance collaborate at depth immediately
- A populated `context/projects.md` with their actual projects and emerging principles
- An initialized `context/current-state.md` reflecting their real state
- The stop hook installed (the system's immune system)
- At least one real item in `inbox/` or `tasks/` to establish the capture habit
- Org Viewer running (optional but encouraged - it's bundled and zero-config)

**What success feels like to the user:** "This Claude already gets how I think."

---

## Phase 1: Voice Discovery (20-30 min)

### Opening

Start with something like:

> "Let's set up this organization system. The most important part is helping me understand how you think and work, so I can be useful from the first message of every future session. I'm going to ask you some questions - there are no wrong answers. Just be honest, not aspirational."

### Questions to Ask

Ask these conversationally, not as a survey. Follow threads. Let tangents happen - they often reveal the most important patterns. You don't need to ask all of them; stop when you have enough signal to draft voice.md.

**How they think:**

- "What domains or fields do you move between in your work and interests?"
  - *The range here matters. Someone might say "I'm a frontend developer" or "I move between embedded systems, theology, and small business operations" or "I do DevOps by day and compose music by night." Both narrow and wide are valid. You're listening for the cross-domain connections they make naturally.*

- "When you're solving a problem, what's your instinct? Do you reach for the abstract model first, or the concrete thing that works?"
  - *Examples: some people prototype immediately and clean up later. Others need to understand the whole system before touching anything. Some oscillate depending on stakes. There's no right answer but it deeply affects how you should collaborate with them.*

- "What do you find yourself caring about that other people in your field tend to overlook?"
  - *This often surfaces their latent principles. Someone who says "I care way too much about error messages" is telling you about communication clarity and user empathy. Someone who says "I can't stop thinking about naming" is telling you about conceptual precision. Listen for the values under the preference.*

- "What patterns keep showing up across different areas of your work?"
  - *Examples: "I always end up building the documentation system," "I keep automating myself out of jobs," "I notice I restructure things before I extend them," "Everything I build eventually needs a CLI."*

**How they collaborate:**

- "What communication style works for you? Do you want me to be terse and direct, or more exploratory and discursive?"
  - *Examples: "Give me the code, skip the explanation" is valid. So is "I want to think out loud together." Some want both depending on context - terse for execution, exploratory for design. Get specific - "direct" means different things to different people.*

- "What behaviors from AI assistants (or human collaborators) frustrate you?"
  - *This is gold. Common frustrations: over-explaining things they already know, asking permission for every little thing, hedging when a clear answer exists, adding features nobody asked for, sycophantic agreement, refusing to disagree. But listen for their specific ones - they'll be unique and highly informative.*

- "When we disagree about an approach, how do you want me to handle it?"
  - *Some people want hard pushback. Others want alternatives presented and let them choose. Some want "just do what I say and flag concerns once." This shapes every future interaction.*

**What they're working on:**

- "What are you actively working on right now? Don't worry about being organized - just dump."
  - *Let them ramble. You'll organize it later in projects.md.*

- "What's a project or piece of work you're proud of? What made it work?"
  - *Surfaces values, quality standards, and what "done well" means to them.*

- "What's something you keep meaning to do but haven't started?"
  - *Great first inbox item or task candidate.*

### Synthesizing voice.md

Once you have enough signal (usually 10-15 minutes of conversation), tell the user:

> "I have a good picture now. Let me draft your voice.md - this is the document future Claude instances will read to understand how to work with you. I'll show you what I've got and you can tell me what's off."

Write `context/voice.md` with real content. Key principles:
- **Be specific, not generic.** "Direct communication" is generic. "Terse when executing, exploratory when designing" is specific.
- **Reflect what they said, not what sounds good.** If they said "I hate when AI adds emoji" - put that in.
- **Include the surprising things.** The unusual preferences are the most valuable for differentiation.
- **Areas of depth vs. active learning is critical.** This prevents future Claude instances from over-explaining things they're expert in, or assuming knowledge they don't have.

Show them the draft. Ask: "What's off? What's missing? What did I get wrong?" Iterate until it feels right to them.

### Important

**Don't over-polish on the first pass.** voice.md will evolve through use. A good-enough voice.md today is better than a perfect one that takes an hour. Tell them: "This will evolve. When something feels wrong in a future session, just say so and we'll fix it."

---

## Phase 2: Project Mapping (15-20 min)

### Opening

> "Now let's map what you're working on. This helps future sessions understand not just individual projects, but how they connect. What are you actively building or maintaining?"

### What to Listen For

- **Project clusters**: projects that share technology, purpose, or philosophy
- **Recurring themes**: the same concern showing up in different contexts
- **Maturity spectrum**: what's research vs. building vs. mature vs. done
- **Tech stack**: what they're using and what they're learning

### Synthesizing projects.md

Write `context/projects.md` with:
1. **Conceptual threads** grouping related projects with the ASCII diagram format
2. **Their tech stack** as a reference table
3. **Project maturity spectrum** showing where things stand
4. **Principle lattice** - see below

### The Principle Lattice

The template comes with seven starter principles. Present them like this:

> "The system includes some starter principles that have proven useful across different workflows. Let me walk through them - keep what resonates, modify what doesn't, and definitely add your own. These are starting points, not requirements. The goal is to end up with principles that actually describe how YOU think."

The starter principles:
- **Inversion** - Place the complex at the simple point
- **Sovereignty** - You own your data and workflow
- **Structural Correctness** - Architecture that prevents invalid states
- **Irreducibility** - Compress to essential form
- **Single-Source** - One source, many derived views
- **Visibility** - What matters should be observable
- **Depth Over Broadcast** - The deepest truths are personal, not public

For each one, briefly explain what it means in practice, then ask: "Does this show up in how you think or work?" If yes, help them find their own instantiations (where this principle appears in their work). If it doesn't click, leave it with empty instantiations or remove it.

**Also ask:** "Is there a principle you live by that isn't on this list? Something you keep coming back to that shapes your decisions?"

Often there is. Examples that have come up for others:
- "Reversibility" - prefer changes that can be undone
- "Automation over manual" - if I do it twice, script it
- "Explicit over implicit" - no magic, readable configuration
- "Worse is better" - simple and working beats complex and theoretical
- "Composability" - small tools that combine over monoliths

Help them articulate new principles in the same format: one-sentence statement + instantiations across their domains.

**Target**: 4-9 principles with 2-5 instantiations each. This will grow over time - don't force completeness. A lattice with 4 honest principles is better than 8 borrowed ones.

### Initialize current-state.md

Update `context/current-state.md` with:
- Any tasks that emerged from the conversation
- Their projects with current status
- Reset the inbox counts to reflect reality

---

## Phase 3: Install the Stop Hook (5 min)

### Why This Matters

Tell the user directly:

> "There's one piece of infrastructure that makes the whole system self-maintaining: the stop hook. It runs at the end of every session and forces a quick check - did we learn anything worth capturing? Did any task statuses change? Without it, maintenance depends on remembering, which means it won't happen consistently. With it, the system maintains itself."

### Installation

```bash
python setup/install.py
```

Or walk them through manual installation from `setup/README.md`.

### Verify

Have them test it:

> "Try ending this session with /stop - you should see the maintenance checklist appear. That means the system's immune system is working."

If they want to continue after testing, that's fine - the hook will fire again at the real end.

---

## Phase 4: First Capture (5 min)

### Establish the Habit

During the conversation, things will have come up - tasks they mentioned, ideas that surfaced, things they want to explore. Create at least one real item:

- A task in `tasks/` for something concrete they need to do
- An idea in `inbox/ideas/` for something percolating
- A knowledge article in `knowledge/` if any reusable insight emerged

Tell them:

> "The most important habit is: capture immediately, sort later. When something comes up - a task, an idea, a thing to investigate - drop it in inbox/ and move on. The inbox exists so you never lose a thought to 'I'll remember that later.' There are subfolders if you want to be specific (ideas/, decisions/, investigations/) but captures/ works as a catch-all too."

---

## Phase 5: Org Viewer (Optional, 2 min)

### Quick Introduction

> "There's a document viewer bundled with this system - org-viewer.exe. It gives you a visual way to browse your documents, search across everything, see the knowledge graph, and edit files. Want to try it?"

If yes: run `org-viewer.exe` from the org root. It opens automatically.

Mention:
- Keyboard shortcuts (1-6 for views, `t` for theme, `e` to edit)
- Remote access is possible via Tailscale if they want to browse from their phone
- Full docs in `ORG-VIEWER.md`
- Source on GitHub if they want to customize the aesthetics and rebuild: https://github.com/vincitamore/org-viewer

Don't push hard. Some people prefer the command line or other tools. That's fine.

---

## Phase 6: Cleanup

### Remove Scaffolding

Once onboarding is complete, these files are dead weight. Delete them:

```
ONBOARDING.md          ← this file (you've run it, it's done)
QUICKSTART.md          ← superseded by completed setup
CONTRIBUTING.md        ← only relevant for contributing to the template repo itself
samples/               ← entire folder (examples served their purpose during onboarding)
claude-org-logo.png    ← template branding
.github/               ← template repo config
```

### Obsidian Decision

Ask the user:

> "The system comes with optional Obsidian integration (visual dashboards, graph views, publishing). Do you use Obsidian or are you interested in trying it?"

**If no (most people):** Delete the Obsidian-specific files:
```
.obsidian/                              ← vault configuration
setup/obsidian/                         ← Obsidian setup guide
knowledge/obsidian-workflow-patterns.md  ← Obsidian-specific knowledge
publish.css                             ← Obsidian Publish CSS
scripts/publish.py                      ← Obsidian Publish workflow
scripts/generate-tag-pages.py           ← org-viewer handles this natively
scripts/generate-publish-dashboard.py   ← Obsidian Publish specific
templates/dashboard.md                  ← Obsidian Dataview specific
```

**If yes:** Keep those files. Move `knowledge/obsidian-workflow-patterns.md` into their knowledge structure appropriately. Point them to `setup/obsidian/README.md` for configuration.

### README.md Decision

Ask the user:

> "The README.md is the GitHub template's landing page. Want me to delete it, or replace it with a brief personal README for your org?"

Most people will want to delete it or replace it with something minimal.

### Update CLAUDE.md

Remove the setup checkpoint at the top (the checkbox section about verifying the stop hook). Remove the "For new users: See ONBOARDING.md" line from the Orientation section. CLAUDE.md should now be a clean operational reference, not a setup guide.

### Final Message

> "Setup is complete. Your system is live. A few things to know:
>
> - **If something doesn't work for you, change it.** Rename folders, add inbox categories, modify principles, restructure whatever you want. This is your system. The only load-bearing constraint is frontmatter consistency so the tools can parse your files. Everything else is yours to shape.
> - **The stop hook keeps things maintained.** Every time you end a session, it'll prompt for captures. Trust the process.
> - **voice.md and projects.md evolve.** When they feel wrong, just say 'something about voice.md isn't right' and we'll fix it together.
> - **Capture aggressively, sort lazily.** inbox/ exists so you never lose a thought."

---

## Timing Guide

| Phase | Time | Required? |
|-------|------|-----------|
| Voice Discovery | 20-30 min | Yes |
| Project Mapping | 15-20 min | Yes |
| Stop Hook | 5 min | **Essential** |
| First Capture | 5 min | Yes |
| Org Viewer | 2 min | Optional |
| Cleanup | 5 min | Yes |

**Total: ~50-65 minutes** for a fully initialized, cleaned-up system.

---

## Anti-Patterns to Avoid

- **Don't turn it into a survey.** This is a conversation, not a form. Follow threads, let tangents happen.
- **Don't over-explain the system.** They'll learn it by using it. Explain only what's immediately relevant.
- **Don't skip cleanup.** Template artifacts left behind confuse future sessions and create noise.
- **Don't force the principles.** Better to have 3 genuine ones than 7 borrowed ones.
- **Don't make voice.md too long.** Dense and specific beats comprehensive and vague. 40-80 lines is ideal.
- **Don't forget to test the stop hook.** It's the single most important piece of infrastructure.
- **Don't be precious about the template.** If the user wants to rename `knowledge/` to `notes/` or merge `inbox/` into a single flat folder, help them do it. The system serves them, not the other way around.
