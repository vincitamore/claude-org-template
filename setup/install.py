#!/usr/bin/env python3
"""
Install hooks for the claude-org system.

The stop hook is essential - it's what makes the system self-maintaining.
"""

import os
import sys
import shutil
from pathlib import Path

def get_claude_dir():
    """Get the Claude configuration directory."""
    if sys.platform == "win32":
        return Path(os.environ.get("USERPROFILE", "")) / ".claude"
    return Path.home() / ".claude"

def main():
    # Find setup directory (where this script lives)
    setup_dir = Path(__file__).parent
    hooks_src = setup_dir / "hooks"

    # Target directories
    claude_dir = get_claude_dir()
    hooks_dest = claude_dir / "hooks"

    print("Claude-Org Infrastructure Installation")
    print("=" * 40)
    print()

    # Create hooks directory
    hooks_dest.mkdir(parents=True, exist_ok=True)
    print(f"Hooks directory: {hooks_dest}")

    # Copy hooks
    hooks_copied = []
    for hook_file in hooks_src.glob("*.py"):
        dest = hooks_dest / hook_file.name
        shutil.copy2(hook_file, dest)
        hooks_copied.append(hook_file.name)
        print(f"  Copied: {hook_file.name}")

    print()
    print("Installation complete.")
    print()
    print("IMPORTANT: Add to your Claude Code settings.json:")
    print()

    # Generate platform-appropriate paths
    if sys.platform == "win32":
        hook_path = str(hooks_dest / "maintenance-check.py").replace("\\", "/")
    else:
        hook_path = str(hooks_dest / "maintenance-check.py")

    print(f'''{{
  "hooks": {{
    "Stop": {{
      "command": "python \\"{hook_path}\\"",
      "timeout": 5000
    }}
  }}
}}''')
    print()
    print("Then restart Claude Code.")
    print()
    print("The stop hook is essential - it's what makes maintenance automatic.")

if __name__ == "__main__":
    main()
