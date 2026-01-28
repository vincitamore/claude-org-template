#!/usr/bin/env python3
"""
Maintenance Check Hook - Run before session ends

CRITICAL: This hook is what makes the system self-maintaining.
Without it, maintenance depends on discipline (which fails).

This hook runs when a Claude Code session is about to stop.
It prompts Claude to evaluate whether any maintenance tasks should
be performed before ending the session. It blocks the stop until
Claude either performs maintenance or explicitly states
"No maintenance needed."

FEATURES:
- Skips trivial sessions (< 15 lines) to avoid unnecessary nagging
- Skips if org system doesn't exist (graceful degradation)
- Handles stop_hook_active flag to prevent infinite loops
- Uses proper JSON protocol for Claude Code hooks

INSTALLATION:
1. Copy this file to your hooks folder:
   - macOS/Linux: ~/.claude/hooks/maintenance-check.py
   - Windows: %USERPROFILE%\.claude\hooks\maintenance-check.py

2. Add to Claude Code settings.json:

   {
     "hooks": {
       "Stop": {
         "command": "python ~/.claude/hooks/maintenance-check.py",
         "timeout": 5000
       }
     }
   }

   On Windows, use the full path:
   "command": "python C:/Users/YourName/.claude/hooks/maintenance-check.py"

3. Restart Claude Code for hooks to take effect

WHY THIS MATTERS:
- Forces maintenance evaluation at every substantive session end
- Prevents documentation drift
- Captures knowledge that would otherwise be lost
- Keeps project status accurate
- Makes the system self-maintaining rather than discipline-dependent
"""

import json
import sys
import os

# Customize this path to your org system location
ORG_DIR = os.path.expanduser("~/Documents/claude-org")

# Minimum transcript lines before triggering maintenance check
# Avoids nagging on quick "hello" or single-command sessions
TRIVIAL_SESSION_THRESHOLD = 15

MAINTENANCE_CHECKLIST = """MAINTENANCE VIGILANCE CHECK

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

Be aggressive about capture - lost insights are unrecoverable."""


def main():
    # Read hook input from stdin
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        # No valid input, allow stop
        sys.exit(0)

    # If already continuing from stop hook, don't block again
    # This prevents infinite loops
    if data.get("stop_hook_active"):
        sys.exit(0)

    # Check transcript length - don't nag on trivial sessions
    transcript_path = data.get("transcript_path")
    if not transcript_path or not os.path.exists(transcript_path):
        sys.exit(0)

    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            content = f.read()
            line_count = content.count('\n')
    except Exception:
        sys.exit(0)

    if line_count < TRIVIAL_SESSION_THRESHOLD:
        sys.exit(0)

    # Check if org system exists - graceful degradation
    if not os.path.exists(ORG_DIR):
        sys.exit(0)

    # Block and prompt for maintenance evaluation
    output = {
        "decision": "block",
        "reason": MAINTENANCE_CHECKLIST
    }

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
