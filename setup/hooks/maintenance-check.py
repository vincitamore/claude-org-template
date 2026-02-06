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
- Skips if "No maintenance needed" already stated
- Handles stop_hook_active flag to prevent infinite loops
- Detects KB files at root that may need organization
- Uses proper JSON protocol for Claude Code hooks

INSTALLATION:
1. Copy this file to your hooks folder:
   - macOS/Linux: ~/.claude/hooks/maintenance-check.py
   - Windows: %USERPROFILE%\\.claude\\hooks\\maintenance-check.py

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
import re

# Customize this path to your org system location
ORG_DIR = os.path.expanduser("~/Documents/claude-org")

# Minimum transcript lines before triggering maintenance check
# Avoids nagging on quick "hello" or single-command sessions
TRIVIAL_SESSION_THRESHOLD = 15


def get_documented_cross_cutting(org_dir: str) -> set:
    """Parse knowledge/README.md to find files documented as cross-cutting."""
    readme_path = os.path.join(org_dir, "knowledge", "README.md")
    if not os.path.exists(readme_path):
        return set()

    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find "## Root Level" section and extract backtick-quoted filenames
        root_match = re.search(r'## Root Level\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
        if not root_match:
            return set()

        # Extract filenames from backticks: `filename.md`
        filenames = re.findall(r'`([^`]+\.md)`', root_match.group(1))
        return set(filenames)
    except Exception:
        return set()


def check_kb_organization(org_dir: str) -> list:
    """Check for KB files at root that might need organization.

    Excludes files documented as intentionally cross-cutting in README.md.
    """
    knowledge_dir = os.path.join(org_dir, "knowledge")
    if not os.path.exists(knowledge_dir):
        return []

    # Get files explicitly documented as cross-cutting
    documented_cross_cutting = get_documented_cross_cutting(org_dir)

    root_files = []
    for entry in os.scandir(knowledge_dir):
        if entry.is_file() and entry.name.endswith('.md'):
            if entry.name not in documented_cross_cutting and entry.name != 'README.md':
                root_files.append(entry.name.replace('.md', ''))

    return root_files


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

    # Check if Claude already stated "No maintenance needed" recently
    # Look at the last ~2000 chars of transcript for this phrase
    recent_content = content[-2000:] if len(content) > 2000 else content
    if "No maintenance needed" in recent_content:
        sys.exit(0)

    # Check if org system exists - graceful degradation
    if not os.path.exists(ORG_DIR):
        sys.exit(0)

    # Check KB organization status
    root_kb_files = check_kb_organization(ORG_DIR)
    kb_warning = ""
    if root_kb_files:
        kb_warning = f"""

**KB Organization Alert:** {len(root_kb_files)} file(s) at knowledge root:
- {', '.join(root_kb_files[:5])}{'...' if len(root_kb_files) > 5 else ''}
\u2192 Move to appropriate subfolder, OR
\u2192 If truly cross-cutting, document in knowledge/README.md under "## Root Level\""""

    # Block and prompt for maintenance evaluation
    output = {
        "decision": "block",
        "reason": f"""MAINTENANCE VIGILANCE CHECK

Before stopping, evaluate this session:

| Signal | Action if Present |
|--------|-------------------|
| New reusable insight/pattern | \u2192 knowledge/<subfolder>/<topic>.md |
| Project status changed | \u2192 Update context/current-state.md |
| New task identified | \u2192 tasks/<name>.md |
| Question worth preserving | \u2192 queries/<question>.md |
| Cross-project pattern | \u2192 Add instantiation to principle lattice |
| Feature idea / future project | \u2192 inbox/ideas/<item>.md |
| Decision needed | \u2192 inbox/decisions/<item>.md |
| Bug to investigate | \u2192 inbox/investigations/<item>.md |
| Quick unsorted capture | \u2192 inbox/captures/<item>.md |
| KB file needs organization | \u2192 Move to appropriate subfolder |

If ANY apply: perform the maintenance NOW.
If NONE apply: state "No maintenance needed" and stop.

Be aggressive about capture - lost insights are unrecoverable.{kb_warning}"""
    }

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
