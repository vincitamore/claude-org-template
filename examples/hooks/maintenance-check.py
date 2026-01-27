#!/usr/bin/env python3
"""
Maintenance Check Hook - Run before session ends

CRITICAL: This hook is what makes the system self-maintaining.
Without it, maintenance depends on discipline (which fails).

This hook runs when a Claude Code session is about to stop.
It prompts Claude to evaluate whether any maintenance tasks should
be performed before ending the session. It blocks the stop (exit 1)
until Claude either performs maintenance or explicitly states
"No maintenance needed."

INSTALLATION:
1. Copy this file to ~/.claude/hooks/maintenance-check.py
2. Add to Claude Code settings (settings.json or via UI):

   {
     "hooks": {
       "Stop": {
         "command": "python ~/.claude/hooks/maintenance-check.py",
         "timeout": 5000
       }
     }
   }

3. Restart Claude Code for hooks to take effect

WHY THIS MATTERS:
- Forces maintenance evaluation at every session end
- Prevents documentation drift
- Captures knowledge that would otherwise be lost
- Keeps project status accurate
- Makes the system self-maintaining rather than discipline-dependent
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
