---
type: knowledge
created: 2026-01-15
updated: 2026-01-20
tags: [git, workflow, patterns]
---

# Git Commit Message Patterns

## Summary

Commit messages are documentation. A good message explains *why*, not just *what*. The diff shows what changed; the message should explain the reasoning.

## The Pattern

**Structure:**
```
<type>: <subject line under 50 chars>

<body - the why, not the what>

<footer - references, co-authors>
```

**Types:**
- `fix:` - Bug fixes
- `feat:` - New features
- `refactor:` - Code changes that don't fix bugs or add features
- `docs:` - Documentation only
- `chore:` - Maintenance, dependencies, tooling

**The subject line** is what appears in `git log --oneline`. Make it count.

**The body** answers: "Why was this change necessary? What problem does it solve? Are there side effects?"

## When to Apply

Every commit. The discipline compounds - a clean history is searchable, bisectable, and tells the story of the project.

Especially important:
- Before merging PRs (squash if necessary to clean the story)
- When fixing bugs (future you will search for this)
- When making non-obvious changes (explain the reasoning)

## Examples

**Bad:**
```
fixed the thing
```

**Good:**
```
fix: prevent null pointer when user has no email

The OAuth flow allows accounts without email addresses.
The profile page assumed email existed and crashed.

Added null check and fallback to username display.

Fixes #423
```

## Related

- [[git-workflow]] - broader branching strategy
- [[code-review-patterns]] - how commits affect review
