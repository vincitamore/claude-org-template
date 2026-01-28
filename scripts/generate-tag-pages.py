#!/usr/bin/env python3
"""
Generate tag index pages from frontmatter tags.

Follows the Single-Source pattern: frontmatter tags are the source of truth,
tag pages are derived/computed state for graph connectivity on Publish.

Run before publishing: python scripts/generate-tag-pages.py
"""

import os
import re
import yaml
from pathlib import Path
from collections import defaultdict
from datetime import date

# Configuration
VAULT_ROOT = Path(__file__).parent.parent
TAGS_DIR = VAULT_ROOT / "tags"
EXCLUDED_DIRS = {".obsidian", "node_modules", ".git", "tags", "setup"}


def extract_frontmatter(filepath: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    try:
        content = filepath.read_text(encoding="utf-8")
        if not content.startswith("---"):
            return {}

        end_match = re.search(r"\n---\s*\n", content[3:])
        if not end_match:
            return {}

        yaml_content = content[3:end_match.start() + 3]
        return yaml.safe_load(yaml_content) or {}
    except Exception:
        return {}


def get_tags_from_frontmatter(frontmatter: dict) -> list[str]:
    """Extract tags from frontmatter, handling various formats."""
    tags = frontmatter.get("tags", [])

    if isinstance(tags, str):
        # Handle comma-separated or space-separated
        tags = [t.strip() for t in re.split(r"[,\s]+", tags) if t.strip()]
    elif isinstance(tags, list):
        tags = [str(t).strip() for t in tags if t]
    else:
        tags = []

    # Normalize: remove # prefix if present, lowercase
    return [t.lstrip("#").lower() for t in tags if t]


def scan_vault() -> dict[str, list[dict]]:
    """Scan vault and build tag -> documents mapping."""
    tag_docs = defaultdict(list)

    for root, dirs, files in os.walk(VAULT_ROOT):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for filename in files:
            if not filename.endswith(".md"):
                continue

            filepath = Path(root) / filename
            rel_path = filepath.relative_to(VAULT_ROOT)

            # Skip certain files
            if rel_path.name in ("CLAUDE.md", "README.md", "ONBOARDING.md", "QUICKSTART.md", "CONTRIBUTING.md"):
                continue

            frontmatter = extract_frontmatter(filepath)
            tags = get_tags_from_frontmatter(frontmatter)

            if tags:
                doc_info = {
                    "path": rel_path,
                    "name": filepath.stem,
                    "type": frontmatter.get("type", "unknown"),
                    "title": extract_title(filepath) or filepath.stem,
                }

                for tag in tags:
                    tag_docs[tag].append(doc_info)

    return tag_docs


def extract_title(filepath: Path) -> str | None:
    """Extract first H1 heading as title."""
    try:
        content = filepath.read_text(encoding="utf-8")
        match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        return match.group(1).strip() if match else None
    except Exception:
        return None


def generate_tag_page(tag: str, docs: list[dict]) -> str:
    """Generate markdown content for a tag index page."""
    # Sort docs by type, then name
    type_order = {"knowledge": 0, "project": 1, "task": 2, "inbox": 3, "unknown": 9}
    docs_sorted = sorted(docs, key=lambda d: (type_order.get(d["type"], 5), d["name"]))

    # Group by type
    by_type = defaultdict(list)
    for doc in docs_sorted:
        by_type[doc["type"]].append(doc)

    lines = [
        "---",
        "type: tag-index",
        f"tag: {tag}",
        f"generated: {date.today().isoformat()}",
        "publish: true",
        "---",
        "",
        f"# {tag.replace('-', ' ').title()}",
        "",
        f"**{len(docs)} documents** with this tag.",
        "",
    ]

    # Add sections by type
    type_labels = {
        "knowledge": "Knowledge",
        "project": "Projects",
        "task": "Tasks",
        "inbox": "Inbox",
        "unknown": "Other",
    }

    for doc_type in ["knowledge", "project", "task", "inbox", "unknown"]:
        type_docs = by_type.get(doc_type, [])
        if type_docs:
            lines.append(f"## {type_labels.get(doc_type, doc_type.title())}")
            lines.append("")
            for doc in type_docs:
                # Use the filename without extension for the wikilink
                link_name = doc["path"].stem
                lines.append(f"- [[{link_name}]]")
            lines.append("")

    lines.append("---")
    lines.append(f"*Auto-generated from frontmatter tags. Last updated: {date.today().isoformat()}*")

    return "\n".join(lines)


def main():
    """Main entry point."""
    print(f"Scanning vault: {VAULT_ROOT}")

    # Ensure tags directory exists
    TAGS_DIR.mkdir(exist_ok=True)

    # Scan vault for tags
    tag_docs = scan_vault()

    if not tag_docs:
        print("No tags found in vault.")
        return

    print(f"Found {len(tag_docs)} unique tags across {sum(len(docs) for docs in tag_docs.values())} tag usages")

    # Generate tag pages
    generated = 0
    for tag, docs in sorted(tag_docs.items()):
        tag_file = TAGS_DIR / f"{tag}.md"
        content = generate_tag_page(tag, docs)

        # Only write if content changed
        if tag_file.exists():
            existing = tag_file.read_text(encoding="utf-8")
            # Compare without the generated date line
            if existing.split("\n")[5:] == content.split("\n")[5:]:
                continue

        tag_file.write_text(content, encoding="utf-8")
        generated += 1
        print(f"  Generated: tags/{tag}.md ({len(docs)} docs)")

    # Clean up orphaned tag pages (tags no longer used)
    for tag_file in TAGS_DIR.glob("*.md"):
        tag_name = tag_file.stem
        if tag_name not in tag_docs:
            tag_file.unlink()
            print(f"  Removed orphan: tags/{tag_name}.md")

    print(f"\nDone. Generated/updated {generated} tag pages.")
    print(f"Tag pages are in: {TAGS_DIR}")


if __name__ == "__main__":
    main()
