#!/usr/bin/env python3
"""
Generate static dashboard for Obsidian Publish.
Replicates Dataview queries as plain markdown.

Run before publishing to update dashboard.
"""

import sys
import yaml
from pathlib import Path
from datetime import datetime

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ORG_DIR = Path(__file__).parent.parent


def parse_frontmatter(filepath: Path) -> dict:
    """Extract YAML frontmatter from markdown file."""
    try:
        content = filepath.read_text(encoding='utf-8')
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return yaml.safe_load(parts[1]) or {}
    except Exception as e:
        print(f"Warning: Could not parse {filepath}: {e}", file=sys.stderr)
    return {}


def get_files_with_frontmatter(folder: Path) -> list:
    """Get all markdown files with their frontmatter."""
    files = []
    if folder.exists():
        for f in folder.glob('*.md'):
            fm = parse_frontmatter(f)
            fm['_file'] = f
            fm['_name'] = f.stem
            fm['_mtime'] = datetime.fromtimestamp(f.stat().st_mtime)
            files.append(fm)
    return files


def format_date(d) -> str:
    """Format date for display."""
    if isinstance(d, datetime):
        return d.strftime('%Y-%m-%d')
    if isinstance(d, str):
        return d[:10] if len(d) >= 10 else d
    return str(d) if d else '-'


def format_link(name: str, folder: str, title: str = None, in_table: bool = False) -> str:
    """Format as wiki-style link with optional alias.

    In tables, escape the pipe character to prevent breaking table columns.
    """
    if title:
        if in_table:
            # Escape pipe for markdown tables
            return f'[[{folder}/{name}\\|{title}]]'
        return f'[[{folder}/{name}|{title}]]'
    return f'[[{folder}/{name}]]'


def generate_dashboard() -> str:
    """Generate the full dashboard content."""
    lines = [
        '---',
        'type: dashboard',
        f'generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
        '---',
        '',
        '# Dashboard',
        '',
        '> *Auto-generated for Obsidian Publish. Updates when `generate-publish-dashboard.py` runs.*',
        '',
    ]

    # === Active Tasks ===
    tasks = get_files_with_frontmatter(ORG_DIR / 'tasks')
    completed_folder_tasks = get_files_with_frontmatter(ORG_DIR / 'tasks' / 'completed')
    all_tasks = tasks + completed_folder_tasks
    active_tasks = [t for t in tasks if t.get('status') == 'active']
    active_tasks.sort(key=lambda t: t['_mtime'], reverse=True)

    lines.extend([
        '## Active Tasks',
        '',
        '| Task | Status | Updated |',
        '|------|--------|---------|',
    ])
    for t in active_tasks:
        title = t.get('title') or t['_name'].replace('-', ' ').title()
        link = format_link(t['_name'], 'tasks', title, in_table=True)
        status = t.get('status', '-')
        updated = format_date(t['_mtime'])
        lines.append(f'| {link} | {status} | {updated} |')
    if not active_tasks:
        lines.append('| *No active tasks* | - | - |')
    lines.append('')

    # === Blocked Tasks ===
    blocked_tasks = [t for t in tasks if t.get('status') == 'blocked']

    lines.extend([
        '## Blocked Tasks',
        '',
        '| Task | Blocked By |',
        '|------|------------|',
    ])
    for t in blocked_tasks:
        title = t.get('title') or t['_name'].replace('-', ' ').title()
        link = format_link(t['_name'], 'tasks', title, in_table=True)
        blocked_by = ', '.join(t.get('blocked-by', [])) or '-'
        lines.append(f'| {link} | {blocked_by} |')
    if not blocked_tasks:
        lines.append('| *No blocked tasks* | - |')
    lines.append('')

    # === Active Projects ===
    projects = []
    projects_dir = ORG_DIR / 'projects'
    if projects_dir.exists():
        for pdir in projects_dir.iterdir():
            if pdir.is_dir():
                readme = pdir / 'README.md'
                if readme.exists():
                    fm = parse_frontmatter(readme)
                    fm['_name'] = pdir.name
                    fm['_file'] = readme
                    projects.append(fm)

    active_projects = [p for p in projects if p.get('status') == 'active']

    lines.extend([
        '## Active Projects',
        '',
        '| Project | Status | Tags |',
        '|---------|--------|------|',
    ])
    for p in active_projects:
        title = p.get('title') or p['_name'].replace('-', ' ').title()
        link = f'[[projects/{p["_name"]}/README\\|{title}]]'
        status = p.get('status', '-')
        tags = ', '.join(p.get('tags', [])) or '-'
        lines.append(f'| {link} | {status} | {tags} |')
    if not active_projects:
        lines.append('| *No active projects* | - | - |')
    lines.append('')

    # === Recent Knowledge ===
    knowledge = get_files_with_frontmatter(ORG_DIR / 'knowledge')
    for k in knowledge:
        updated = k.get('updated')
        if updated:
            try:
                k['_sort_date'] = datetime.strptime(str(updated)[:10], '%Y-%m-%d')
            except:
                k['_sort_date'] = k['_mtime']
        else:
            k['_sort_date'] = k['_mtime']
    knowledge.sort(key=lambda k: k['_sort_date'], reverse=True)

    lines.extend([
        '## Recent Knowledge',
        '',
        '| Topic | Updated | Tags |',
        '|-------|---------|------|',
    ])
    for k in knowledge[:10]:
        title = k.get('title') or k['_name'].replace('-', ' ').title()
        link = format_link(k['_name'], 'knowledge', title, in_table=True)
        updated = format_date(k.get('updated') or k['_mtime'])
        tags = ', '.join(k.get('tags', [])) or '-'
        lines.append(f'| {link} | {updated} | {tags} |')
    lines.append('')

    # === Inbox ===
    inbox = get_files_with_frontmatter(ORG_DIR / 'inbox')
    for i in inbox:
        created = i.get('created')
        if created:
            i['_sort_created'] = str(created)[:10]
        else:
            i['_sort_created'] = ''
    inbox.sort(key=lambda i: i['_sort_created'], reverse=True)

    lines.extend([
        '## Inbox (Unprocessed)',
        '',
    ])
    if inbox:
        for i in inbox:
            title = i.get('title') or i['_name'].replace('-', ' ').title()
            link = format_link(i['_name'], 'inbox', title)
            lines.append(f'- {link}')
    else:
        lines.append('*Inbox empty*')
    lines.append('')

    # === Recently Completed ===
    completed_tasks = [t for t in all_tasks if t.get('status') == 'complete']
    for t in completed_tasks:
        comp = t.get('completed')
        if comp:
            try:
                t['_comp_date'] = datetime.strptime(str(comp)[:10], '%Y-%m-%d')
            except:
                t['_comp_date'] = datetime.min
        else:
            t['_comp_date'] = datetime.min
    completed_tasks.sort(key=lambda t: t['_comp_date'], reverse=True)

    lines.extend([
        '## Recently Completed',
        '',
        '| Task | Completed |',
        '|------|-----------|',
    ])
    for t in completed_tasks[:5]:
        title = t.get('title') or t['_name'].replace('-', ' ').title()
        if 'completed' in str(t['_file'].parent):
            link = format_link(t['_name'], 'tasks/completed', title, in_table=True)
        else:
            link = format_link(t['_name'], 'tasks', title, in_table=True)
        completed = format_date(t.get('completed'))
        lines.append(f'| {link} | {completed} |')
    if not completed_tasks:
        lines.append('| *No completed tasks* | - |')
    lines.append('')

    # === Footer ===
    lines.extend([
        '---',
        f'*Last generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}*',
    ])

    return '\n'.join(lines)


def main():
    dashboard_content = generate_dashboard()
    output_path = ORG_DIR / 'publish-dashboard.md'
    output_path.write_text(dashboard_content, encoding='utf-8')
    print(f"Generated: {output_path}")


if __name__ == '__main__':
    main()
