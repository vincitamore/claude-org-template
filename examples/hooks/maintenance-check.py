#!/usr/bin/env python3
"""
Maintenance Check Hook - Run before session ends

This hook runs when a Claude Code session is about to stop.
It prompts Claude to check whether any maintenance tasks should
be performed before ending the session.

Install: Copy to ~/.claude/hooks/ and configure as Stop hook in settings.json
"""

import sys

# Output the maintenance checklist - Claude will evaluate
CHECKLIST = """
MAINTENANCE VIGILANCE CHECK

Before stopping, evaluate this session:

| Signal | Action if Present |
|--------|-------------------|
| New reusable insight/pattern | → knowledge/<topic>.md |
| Project status changed | → Update CLAUDE.md, project-map.md |
| New task identified | → tasks/<name>.md |
| Question worth preserving | → queries/<question>.md |
| Cross-project pattern | → Add instantiation to principle lattice |
| Something to revisit | → inbox/<item>.md |

If ANY apply: perform the maintenance NOW.
If NONE apply: state "No maintenance needed" and stop.

Be aggressive about capture - lost insights are unrecoverable.
"""

if __name__ == '__main__':
    print(CHECKLIST)
    # Exit with error to prevent stop until Claude addresses this
    sys.exit(1)
