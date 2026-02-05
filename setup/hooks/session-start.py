#!/usr/bin/env python3
"""
Session Start Hook - Auto-orientation for Claude

This hook runs when a Claude Code session starts in this workspace.
It reads frontmatter from key files to compute current state and
presents Claude with a concise orientation context.

Install: Copy to ~/.claude/hooks/ and configure in settings.json
"""

import os
import sys
import yaml
from pathlib import Path
from datetime import datetime

def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown file."""
    if not content.startswith('---'):
        return {}
    try:
        end = content.index('---', 3)
        return yaml.safe_load(content[3:end]) or {}
    except:
        return {}

def get_active_tasks(tasks_dir: Path) -> list:
    """Get active tasks from tasks/*.md files."""
    tasks = []
    if not tasks_dir.exists():
        return tasks

    for f in tasks_dir.glob('*.md'):
        if f.name.startswith('.'):
            continue
        content = f.read_text(encoding='utf-8')
        fm = parse_frontmatter(content)
        if fm.get('status') == 'active':
            # Get first heading as title
            lines = content.split('\n')
            title = f.stem
            for line in lines:
                if line.startswith('# '):
                    title = line[2:].strip()
                    break
            tasks.append({
                'name': f.stem,
                'title': title,
                'tags': fm.get('tags', []),
                'blocked_by': fm.get('blocked-by', [])
            })
    return tasks

def get_inbox_count(inbox_dir: Path) -> dict:
    """Count inbox items by source."""
    counts = {'email': 0, 'capture': 0, 'other': 0}
    if not inbox_dir.exists():
        return counts

    for f in inbox_dir.glob('*.md'):
        content = f.read_text(encoding='utf-8')
        fm = parse_frontmatter(content)
        source = fm.get('source', 'other')
        if source in counts:
            counts[source] += 1
        else:
            counts['other'] += 1
    return counts

def get_due_reminders(reminders_dir: Path) -> dict:
    """Get due and overdue reminders."""
    result = {'overdue': [], 'due_today': [], 'upcoming': []}
    if not reminders_dir.exists():
        return result

    now = datetime.now()
    today = now.date()

    for f in reminders_dir.glob('*.md'):
        if f.name.startswith('.') or f.name == 'README.md':
            continue
        content = f.read_text(encoding='utf-8')
        fm = parse_frontmatter(content)

        # Only check pending, snoozed, ongoing reminders
        status = fm.get('status', '')
        if status not in ['pending', 'snoozed', 'ongoing']:
            continue

        remind_at = fm.get('remind-at')
        if not remind_at:
            continue

        # Parse the remind-at datetime
        try:
            if isinstance(remind_at, str):
                if 'T' in remind_at:
                    due_dt = datetime.fromisoformat(remind_at.replace('Z', '+00:00'))
                else:
                    due_dt = datetime.fromisoformat(remind_at)
            elif isinstance(remind_at, datetime):
                due_dt = remind_at
            else:
                continue
        except:
            continue

        # Get title from first heading or filename
        lines = content.split('\n')
        title = f.stem
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break

        reminder_info = {
            'name': f.stem,
            'title': title,
            'remind_at': due_dt.strftime('%H:%M') if due_dt.date() == today else due_dt.strftime('%Y-%m-%d %H:%M'),
            'path': f'reminders/{f.name}'
        }

        if due_dt < now:
            result['overdue'].append(reminder_info)
        elif due_dt.date() == today:
            result['due_today'].append(reminder_info)
        elif (due_dt.date() - today).days <= 1:
            result['upcoming'].append(reminder_info)

    return result

def main():
    workspace = Path(os.environ.get('CLAUDE_WORKSPACE', '.')).resolve()

    # Gather state
    tasks = get_active_tasks(workspace / 'tasks')
    inbox = get_inbox_count(workspace / 'inbox')
    reminders = get_due_reminders(workspace / 'reminders')

    # Build orientation output
    output = []
    output.append("## Auto-loaded Orientation\n")

    # Active tasks summary
    if tasks:
        output.append("### Active Tasks")
        for t in tasks:
            tags = f" [{', '.join(t['tags'])}]" if t['tags'] else ""
            blocked = " [BLOCKED]" if t['blocked_by'] else ""
            output.append(f"- **{t['name']}**{tags}{blocked} - See `tasks/{t['name']}.md`")
        output.append("")

    # Inbox summary
    total_inbox = sum(inbox.values())
    if total_inbox > 0:
        output.append("### Inbox Items Pending Sort")
        if inbox['email'] > 0:
            output.append(f"**Pending Emails:** {inbox['email']}")
        if inbox['capture'] > 0:
            output.append(f"**Pending Captures:** {inbox['capture']}")
        if inbox['other'] > 0:
            output.append(f"**Other:** {inbox['other']}")
        output.append("")

    # Due reminders - alert section
    total_due = len(reminders['overdue']) + len(reminders['due_today'])
    if total_due > 0:
        output.append(f"### ACTION REQUIRED: {total_due} Due Reminder(s)\n")

        if reminders['overdue']:
            output.append("**Overdue:**")
            for r in reminders['overdue']:
                output.append(f"- [{r['remind_at']}] **{r['title']}**")

        if reminders['due_today']:
            output.append("\n**Due Today:**")
            for r in reminders['due_today']:
                output.append(f"- [{r['remind_at']}] **{r['title']}**")

        output.append("\nUse `org_reminder_list` to see all reminders.\n")

    # Collaboration reminder from voice.md
    voice_file = workspace / 'context' / 'voice.md'
    if voice_file.exists():
        content = voice_file.read_text(encoding='utf-8')
        # Extract "How to Collaborate" section if it exists
        if '## How to Collaborate' in content:
            start = content.index('## How to Collaborate')
            end = content.find('\n## ', start + 1)
            if end == -1:
                end = len(content)
            section = content[start:end].strip()
            output.append("### Collaboration Style\n")
            output.append(section)

    if output:
        print('\n'.join(output))

if __name__ == '__main__':
    main()
