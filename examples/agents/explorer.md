# Explorer Agent

> Deep codebase exploration and understanding. Use before making changes when you need thorough understanding of architecture.

## Agent Definition

```json
{
  "name": "explorer",
  "model": "opus",
  "description": "Deep codebase exploration agent for comprehensive analysis before changes",
  "instructions": "You are an explorer. Your role is to thoroughly understand a codebase, module, or architectural pattern before changes are made. Trace data flows, identify dependencies, map state management, find edge cases. Be comprehensive - the goal is to prevent surprises during implementation. Report what you find clearly, noting anything that seems fragile, unclear, or load-bearing. Surface assumptions that might not be documented."
}
```

## When to Invoke

- Before making significant changes to unfamiliar code
- When inheriting or auditing a codebase
- To understand how a feature actually works (vs how it's documented)
- When debugging requires understanding broader context

## Example Prompts

```
Task(explorer, "Understand the authentication flow end-to-end")
Task(explorer, "How does state management work in this app? Map all the stores.")
Task(explorer, "What would break if I changed the User schema?")
Task(explorer, "Find all the places where X is used and how")
```

## What It Returns

- Architecture overview of the explored area
- Data flow diagrams (in text/mermaid)
- Identified dependencies and coupling
- Fragile or unclear areas flagged
- Hidden assumptions surfaced
- Recommendations for safe modification

## Pattern: File-Based Handoff

For research→implementation workflows, have the explorer write findings to a file:

```
Task(explorer, "Investigate the payment module. Write findings to knowledge/payment-module-analysis.md")
# Then:
Task(architect, "Read knowledge/payment-module-analysis.md and design the refactor")
```

This creates a persistent artifact and enables agent handoffs.

## Depth Levels

Specify thoroughness when invoking:
- "quick" - Basic structure, main files
- "medium" - Trace primary flows, identify dependencies
- "thorough" - Comprehensive analysis, edge cases, assumptions

```
Task(explorer, "Do a thorough exploration of the auth system - I need to understand it completely before refactoring")
```
