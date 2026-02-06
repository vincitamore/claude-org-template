#!/usr/bin/env python3
"""
Session Start Hook - Auto-orientation for Claude

This hook runs when a Claude Code session starts in this workspace.
It reads frontmatter from key files to compute current state and
presents Claude with a concise orientation context.

FEATURES:
- Zero dependencies (regex-based YAML parser, no pip install needed)
- Computes state from frontmatter (1->7 pattern)
- Scans tasks, inbox (with subfolders), reminders, knowledge
- Reads project info from context/current-state.md
- Skips on resume (context already loaded)
- Extracts collaboration style from context/voice.md

INSTALLATION:
1. Copy to ~/.claude/hooks/session-start.py
2. Add to settings.json:

   {
     "hooks": {
       "SessionStart": {
         "command": "python ~/.claude/hooks/session-start.py",
         "timeout": 5000
       }
     }
   }

3. Restart Claude Code
"""

import json
import sys
import os
import re
import glob as glob_module
from datetime import datetime, timedelta

# Fix Windows console encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Customize this path to your org system location
ORG_DIR = os.path.expanduser("~/Documents/claude-org")


def parse_frontmatter(filepath: str) -> dict:
    """Parse YAML frontmatter from a markdown file using regex (no PyYAML dependency)."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return {}

    if not content.startswith('---'):
        return {}

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}

    yaml_content = parts[1].strip()
    result = {}

    for line in yaml_content.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            # Parse lists: [item1, item2]
            if value.startswith('[') and value.endswith(']'):
                inner = value[1:-1].strip()
                if inner:
                    result[key] = [v.strip().strip('"\'') for v in inner.split(',')]
                else:
                    result[key] = []
            # Parse null/empty
            elif value.lower() == 'null' or value == '':
                result[key] = None
            # Parse quoted strings
            else:
                result[key] = value.strip('"\'')

    result['_filepath'] = filepath
    result['_filename'] = os.path.basename(filepath).replace('.md', '')
    return result


def scan_tasks(org_dir: str) -> dict:
    """Scan all task folders, return dict by status category."""
    tasks_dir = os.path.join(org_dir, "tasks")
    if not os.path.exists(tasks_dir):
        return {}

    result = {
        'active': [],
        'blocked': [],
        'review': [],
        'backlog': [],
        'incubating': [],
        'paused': [],
    }

    # Scan root tasks folder
    for filepath in glob_module.glob(os.path.join(tasks_dir, "*.md")):
        if os.path.basename(filepath) == 'README.md':
            continue
        meta = parse_frontmatter(filepath)
        if meta.get('type') != 'task':
            continue
        status = meta.get('status', 'active')
        if status in result:
            result[status].append(meta)

    # Scan subfolders (review, backlog, incubating, paused)
    for subfolder in ['review', 'backlog', 'incubating', 'paused']:
        subfolder_path = os.path.join(tasks_dir, subfolder)
        if os.path.exists(subfolder_path):
            for filepath in glob_module.glob(os.path.join(subfolder_path, "*.md")):
                meta = parse_frontmatter(filepath)
                if meta.get('type') != 'task':
                    continue
                result[subfolder].append(meta)

    return result


def scan_inbox(org_dir: str) -> dict:
    """Scan inbox folder by subfolder location for pending items."""
    inbox_dir = os.path.join(org_dir, "inbox")
    if not os.path.exists(inbox_dir):
        return {}

    # Map folder names to display categories
    folder_map = {
        'emails': 'email',
        'tickets': 'ticket',
        'ideas': 'idea',
        'decisions': 'decision',
        'investigations': 'investigation',
        'captures': 'capture',
    }

    counts = {v: 0 for v in folder_map.values()}
    counts['other'] = 0

    # Scan each known subfolder
    for folder_name, category in folder_map.items():
        folder_path = os.path.join(inbox_dir, folder_name)
        if os.path.exists(folder_path):
            for filepath in glob_module.glob(os.path.join(folder_path, "*.md")):
                if os.path.basename(filepath) != 'README.md':
                    counts[category] += 1

    # Scan root inbox for any stray files
    for filepath in glob_module.glob(os.path.join(inbox_dir, "*.md")):
        if os.path.basename(filepath) != 'README.md':
            counts['other'] += 1

    return counts


def scan_reminders(org_dir: str) -> dict:
    """Scan reminders folder for due/overdue items."""
    reminders_dir = os.path.join(org_dir, "reminders")
    if not os.path.exists(reminders_dir):
        return {'overdue': [], 'due_today': [], 'due_soon': []}

    now = datetime.now()
    today = now.date()

    result = {
        'overdue': [],
        'due_today': [],
        'due_soon': [],
    }

    for filepath in glob_module.glob(os.path.join(reminders_dir, "*.md")):
        if os.path.basename(filepath) == 'README.md':
            continue

        meta = parse_frontmatter(filepath)
        if meta.get('type') != 'reminder':
            continue

        status = meta.get('status', 'pending')

        # Skip completed/dismissed
        if status in ('completed', 'dismissed'):
            continue

        # Handle snoozed reminders
        if status == 'snoozed':
            snoozed_until = meta.get('snoozed-until')
            if snoozed_until:
                try:
                    snooze_dt = datetime.fromisoformat(snoozed_until.replace('Z', '+00:00'))
                    if snooze_dt.tzinfo:
                        snooze_dt = snooze_dt.replace(tzinfo=None)
                    if snooze_dt <= now:
                        result['due_today'].append(meta)
                except Exception:
                    pass
            continue

        # Handle ongoing - skip (not time-based)
        if status == 'ongoing':
            continue

        # Parse remind-at datetime
        remind_at = meta.get('remind-at')
        if not remind_at:
            continue

        try:
            remind_dt = datetime.fromisoformat(remind_at.replace('Z', '+00:00'))
            if remind_dt.tzinfo:
                remind_dt = remind_dt.replace(tzinfo=None)
            remind_date = remind_dt.date()

            if remind_dt < now:
                result['overdue'].append(meta)
            elif remind_date == today:
                result['due_today'].append(meta)
            elif remind_dt < now + timedelta(hours=24):
                result['due_soon'].append(meta)
        except Exception:
            pass

    # Sort each list by remind-at
    def sort_key(r):
        ra = r.get('remind-at', '')
        return ra if ra else '9999'

    for key in result:
        result[key].sort(key=sort_key)

    return result


def scan_knowledge_folders(org_dir: str) -> dict:
    """Scan knowledge folder structure for organizational context."""
    knowledge_dir = os.path.join(org_dir, "knowledge")
    if not os.path.exists(knowledge_dir):
        return {}

    folders = {}
    root_files = []

    for entry in os.scandir(knowledge_dir):
        if entry.is_dir() and not entry.name.startswith('.'):
            count = len([f for f in os.listdir(entry.path) if f.endswith('.md')])
            if count > 0:
                folders[entry.name] = count
        elif entry.is_file() and entry.name.endswith('.md') and entry.name != 'README.md':
            root_files.append(entry.name.replace('.md', ''))

    return {'folders': folders, 'root_files': root_files}


def main():
    # Read stdin (hooks receive JSON input)
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    # Skip orientation on resume - context already loaded
    if data.get("source") == "resume":
        sys.exit(0)

    org_dir = ORG_DIR
    claude_md = os.path.join(org_dir, "CLAUDE.md")

    # Only inject if org system exists
    if not os.path.exists(claude_md):
        sys.exit(0)

    print('<session-context source="SessionStart hook">')
    print('## Auto-loaded Orientation')
    print('')

    # === COMPUTED STATE FROM FRONTMATTER (1->7 pattern) ===
    print('## Current State')
    print('')

    # Tasks by status
    tasks_by_status = scan_tasks(org_dir)

    print('### Active Tasks')
    active = tasks_by_status.get('active', [])
    if active:
        for t in active:
            tags = t.get('tags', [])
            tag_str = f" [{', '.join(tags)}]" if tags else ""
            print(f"- **{t['_filename']}**{tag_str} - See `tasks/{t['_filename']}.md`")
    else:
        print('_No active tasks_')
    print('')

    # Blocked tasks
    blocked = tasks_by_status.get('blocked', [])
    if blocked:
        print('### Blocked Tasks')
        for t in blocked:
            blocked_by = t.get('blocked-by', [])
            blocked_str = ', '.join(blocked_by) if blocked_by else 'unknown'
            print(f"- **{t['_filename']}** - blocked by: {blocked_str}")
        print('')

    # Review tasks
    review = tasks_by_status.get('review', [])
    if review:
        print('### Tasks Needing Review')
        for t in review:
            review_needed = t.get('review-needed', 'decision needed')
            print(f"- **{t['_filename']}** - {review_needed}")
        print('')

    # Summary of other categories
    backlog_count = len(tasks_by_status.get('backlog', []))
    incubating_count = len(tasks_by_status.get('incubating', []))
    paused_count = len(tasks_by_status.get('paused', []))
    if backlog_count or incubating_count or paused_count:
        print(f'**Other:** {backlog_count} backlog, {incubating_count} incubating, {paused_count} paused')
        print('')

    # Active Projects (from context/current-state.md)
    current_state_md = os.path.join(org_dir, "context", "current-state.md")
    if os.path.exists(current_state_md):
        with open(current_state_md, 'r', encoding='utf-8') as f:
            state_content = f.read()

        project_match = re.search(r'## Active Projects\n(.*?)(?=\n## |\Z)', state_content, re.DOTALL)
        if project_match:
            print('### Active Projects')
            print(project_match.group(1).strip())
            print('')

    # Knowledge Base (computed from folder structure)
    kb_info = scan_knowledge_folders(org_dir)
    if kb_info and kb_info.get('folders'):
        print('### Knowledge Base')
        print('See `knowledge/README.md` for full index.')
        print('')
        print('| Folder | Files |')
        print('|--------|-------|')
        for folder, count in sorted(kb_info['folders'].items()):
            print(f"| `{folder}/` | {count} |")
        if kb_info.get('root_files'):
            print(f"| *(root)* | {len(kb_info['root_files'])} |")
        print('')

    # Inbox summary (by folder)
    inbox_counts = scan_inbox(org_dir)
    total_inbox = sum(inbox_counts.values())
    if total_inbox > 0:
        print('### Inbox')
        display_map = [
            ('email', 'Pending Emails'),
            ('ticket', 'Pending Tickets'),
            ('idea', 'Ideas'),
            ('decision', 'Decisions'),
            ('investigation', 'Investigations'),
            ('capture', 'Captures'),
            ('other', 'Other'),
        ]
        for key, label in display_map:
            count = inbox_counts.get(key, 0)
            if count > 0:
                print(f"**{label}:** {count}")
        print('')

    # Due reminders alert
    reminders = scan_reminders(org_dir)
    total_due = len(reminders['overdue']) + len(reminders['due_today'])

    if total_due > 0:
        print(f'### ACTION REQUIRED: {total_due} Due Reminder(s)')
        print('')

        if reminders['overdue']:
            print('**Overdue:**')
            for r in reminders['overdue'][:5]:
                remind_at = r.get('remind-at', 'unknown')
                print(f"- [{remind_at}] **{r['_filename']}**")
            print('')

        if reminders['due_today']:
            print('**Due Today:**')
            for r in reminders['due_today'][:5]:
                remind_at = r.get('remind-at', '')
                time_part = remind_at.split('T')[1][:5] if 'T' in remind_at else ''
                print(f"- [{time_part}] **{r['_filename']}**")
            print('')

        print('Use `org_reminder_list` to see all reminders.')
        print('')

    # Collaboration style from voice.md
    voice_md = os.path.join(org_dir, "context", "voice.md")
    if os.path.exists(voice_md):
        with open(voice_md, 'r', encoding='utf-8') as f:
            content = f.read()

        match = re.search(r'## How to Collaborate\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
        if match:
            print('### Collaboration Style')
            print('')
            lines = match.group(0).split('\n')[:25]
            print('\n'.join(lines))
            print('')

    print('</session-context>')


if __name__ == "__main__":
    main()
