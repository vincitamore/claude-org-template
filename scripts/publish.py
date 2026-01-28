#!/usr/bin/env python3
"""
Automated Publish Workflow

Runs all pre-publish steps and opens the Publish dialog in Obsidian.

Steps:
1. Generate tag index pages (for graph connectivity)
2. Generate static publish dashboard (Dataview doesn't run on Publish)
3. Optionally lint all files
4. Refresh Dataview caches
5. Open Publish dialog in Obsidian

Usage:
  python publish.py           # Run full workflow
  python publish.py --no-lint # Skip linting
  python publish.py --dry-run # Show what would be done

Requirements:
  - Obsidian must be running with the vault open
  - Obsidian Local REST API plugin must be installed and configured
  - Set OBSIDIAN_REST_API_KEY environment variable or configure in .publish-config.json
"""

import argparse
import json
import subprocess
import sys
import urllib.request
import urllib.error
import ssl
from pathlib import Path

# Configuration
SCRIPTS_DIR = Path(__file__).parent
VAULT_DIR = SCRIPTS_DIR.parent
CONFIG_FILE = SCRIPTS_DIR / ".publish-config.json"
REST_API_URL = "https://127.0.0.1:27124"
REST_API_TIMEOUT = 10


def load_config() -> dict:
    """Load configuration from file."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}


def get_api_key() -> str | None:
    """Get REST API key from config or environment."""
    import os
    api_key = os.environ.get("OBSIDIAN_REST_API_KEY")
    if api_key:
        return api_key
    config = load_config()
    return config.get("rest_api_key")


def check_api_available() -> bool:
    """Check if Obsidian REST API is available."""
    api_key = get_api_key()
    if not api_key:
        return False

    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(
            f"{REST_API_URL}/",
            headers={"Authorization": f"Bearer {api_key}"}
        )

        with urllib.request.urlopen(req, timeout=REST_API_TIMEOUT, context=ctx) as response:
            data = json.loads(response.read().decode())
            return data.get("status") == "OK" and data.get("authenticated", False)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return False


def execute_command(command_id: str) -> bool:
    """Execute an Obsidian command via REST API."""
    api_key = get_api_key()
    if not api_key:
        return False

    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        url = f"{REST_API_URL}/commands/{command_id}/"
        req = urllib.request.Request(
            url,
            data=b"",  # POST requires data
            headers={"Authorization": f"Bearer {api_key}"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=REST_API_TIMEOUT, context=ctx) as response:
            return response.status in (200, 204)
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"  [WARN] Command execution failed: {e}")
        return False


def run_script(script_name: str, dry_run: bool = False) -> bool:
    """Run a Python script in the scripts directory."""
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        print(f"  [SKIP] Script not found: {script_name}")
        return False

    if dry_run:
        print(f"  [DRY] Would run: {script_name}")
        return True

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(VAULT_DIR),
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            # Print condensed output
            lines = result.stdout.strip().split('\n')
            for line in lines[-3:]:  # Last 3 lines
                print(f"    {line}")
            return True
        else:
            print(f"  [FAIL] {script_name}")
            print(f"    {result.stderr}")
            return False
    except Exception as e:
        print(f"  [FAIL] {script_name}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Automated Publish Workflow")
    parser.add_argument("--no-lint", action="store_true", help="Skip linting step")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--no-dialog", action="store_true", help="Don't open Publish dialog")
    args = parser.parse_args()

    print("=" * 50)
    print("Publish Workflow")
    print("=" * 50)

    # Check API availability
    api_available = check_api_available()
    if not api_available:
        print("\n[WARN] Obsidian REST API not available.")
        print("       Obsidian must be open for command execution.")
        print("       Install 'Obsidian Local REST API' plugin and configure API key.")
        if not args.dry_run:
            response = input("\nContinue with scripts only? [y/N] ")
            if response.lower() != 'y':
                sys.exit(1)

    # Step 1: Generate tag pages
    print("\n[1/5] Generating tag index pages...")
    run_script("generate-tag-pages.py", args.dry_run)

    # Step 2: Generate publish dashboard
    print("\n[2/5] Generating publish dashboard...")
    run_script("generate-publish-dashboard.py", args.dry_run)

    # Step 3: Lint (optional)
    if not args.no_lint and api_available:
        print("\n[3/5] Linting all files...")
        if args.dry_run:
            print("  [DRY] Would execute: obsidian-linter:lint-all-files")
        else:
            if execute_command("obsidian-linter:lint-all-files"):
                print("  [OK] Linter executed")
            else:
                print("  [SKIP] Linter not available")
    else:
        print("\n[3/5] Linting... SKIPPED")

    # Step 4: Refresh Dataview
    if api_available:
        print("\n[4/5] Refreshing Dataview...")
        if args.dry_run:
            print("  [DRY] Would execute: dataview:dataview-force-refresh-views")
        else:
            if execute_command("dataview:dataview-force-refresh-views"):
                print("  [OK] Dataview refreshed")
            else:
                print("  [SKIP] Dataview not available")
    else:
        print("\n[4/5] Refreshing Dataview... SKIPPED (API not available)")

    # Step 5: Open Publish dialog
    if not args.no_dialog and api_available:
        print("\n[5/5] Opening Publish dialog...")
        if args.dry_run:
            print("  [DRY] Would execute: publish:view-changes")
        else:
            if execute_command("publish:view-changes"):
                print("  [OK] Publish dialog opened")
                print("\n" + "=" * 50)
                print("Ready to publish! Review changes in Obsidian and click Publish.")
                print("=" * 50)
            else:
                print("  [FAIL] Could not open Publish dialog")
    else:
        print("\n[5/5] Opening Publish dialog... SKIPPED")

    print("\nDone!")


if __name__ == "__main__":
    main()
