---
type: knowledge
created: 2026-01-15
updated: 2026-01-20
tags: [git, workflow, patterns]
---

# Git Commit Message Patterns

## Summary

Commit messages are documentation. A good message explains *why*, not just *what*. The diff shows what changed; the message should explain the reasoning.

The commit log is the project's memory. Invest in it.

## The Pattern

**Structure:**
```
<type>: <subject line under 50 chars>

<body - the why, not the what>

<footer - references, co-authors>
```

**Types:**
| Type | Use for |
|------|---------|
| `fix:` | Bug fixes |
| `feat:` | New features |
| `refactor:` | Code changes that don't fix bugs or add features |
| `docs:` | Documentation only |
| `chore:` | Maintenance, dependencies, tooling |
| `test:` | Adding or fixing tests |
| `perf:` | Performance improvements |

**The subject line** is what appears in `git log --oneline`. Make it count. Use imperative mood: "add" not "added", "fix" not "fixed".

**The body** answers:
- Why was this change necessary?
- What problem does it solve?
- Are there side effects or trade-offs?
- What alternatives were considered?

**The footer** includes:
- Issue references (`Fixes #423`, `Closes #789`)
- Co-authors (`Co-Authored-By: Name <email>`)
- Breaking change notes

## When to Apply

Every commit. The discipline compounds - a clean history is searchable, bisectable, and tells the story of the project.

**Especially important:**
- Before merging PRs (squash if necessary to clean the story)
- When fixing bugs (future you will search for this)
- When making non-obvious changes (explain the reasoning)
- When reverting (explain why the original approach failed)

**Less critical:**
- WIP commits on feature branches (will be squashed)
- Exploratory work (will be cleaned up)

## Examples

**Bad:**
```
fixed the thing
```
No context. Which thing? Why was it broken? What does "fixed" mean?

**Also bad:**
```
Update user.py
```
The diff already shows that. What changed about user.py? Why?

**Good:**
```
fix: prevent null pointer when user has no email

The OAuth flow allows accounts without email addresses.
The profile page assumed email existed and crashed.

Added null check and fallback to username display.

Fixes #423
```
Clear type, clear subject, explains the context, references the issue.

**Good (refactor):**
```
refactor: extract validation logic to separate module

The User model was 800 lines with mixed concerns.
Validation logic now lives in validators/user.py.

No behavior change - all existing tests pass.
This enables adding new validation rules without touching the model.
```

## Anti-Patterns

**"Misc fixes"** - If you can't describe it, maybe it should be multiple commits.

**Giant commits** - If the subject line needs "and", it's probably two commits.

**Commit message in PR description only** - The PR will be squashed. The commit message is what survives.

**Relying on linked issue for context** - Issues get closed, moved, deleted. The commit should stand alone.

## Gotchas

- GitHub truncates subject lines at 72 chars in the web UI
- `git commit -m` only allows subject line; use `git commit` for body
- Rebasing rewrites history; coordinate with collaborators
- `--no-verify` skips hooks but loses safety checks

## Related

- [[git-workflow]] - Branching strategy and merge patterns
- [[code-review-patterns]] - How commits affect review quality
- [[ci-cd-patterns]] - How commit messages trigger automation
