#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///
"""
Checkpoint lineage tree visualizer for coihuin-compress.

Displays checkpoint parent-child relationships as an ASCII tree.

Usage:
    uv run compress-tree.py [checkpoints-dir]

Examples:
    uv run compress-tree.py                    # Uses ./checkpoints/
    uv run compress-tree.py checkpoints/       # Explicit path
    uv run compress-tree.py ~/project/chkpts/  # Custom path
"""

import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import yaml


@dataclass
class Checkpoint:
    """Represents a checkpoint with its metadata."""
    id: str
    created: datetime | None
    parent: str | None
    status: str  # 'active' or 'archived'
    path: Path


def extract_frontmatter(content: str) -> dict | None:
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    try:
        return yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None


def parse_iso_datetime(date_str: str | datetime | None) -> datetime | None:
    """Parse ISO 8601 datetime string (e.g., 2025-12-17T10:30:00Z)."""
    if date_str is None:
        return None
    if isinstance(date_str, datetime):
        return date_str
    try:
        # Handle both 'Z' and '+00:00' timezone formats
        date_str = str(date_str).replace("Z", "+00:00")
        return datetime.fromisoformat(date_str)
    except (ValueError, TypeError):
        return None


def scan_checkpoints(base_dir: Path) -> list[Checkpoint]:
    """Scan checkpoint directories and return list of Checkpoint objects."""
    checkpoints = []

    for subdir, status in [("active", "active"), ("archive", "archived")]:
        dir_path = base_dir / subdir
        if not dir_path.exists():
            continue

        for file_path in dir_path.glob("chk-*.md"):
            content = file_path.read_text()
            frontmatter = extract_frontmatter(content)

            if frontmatter is None or "checkpoint" not in frontmatter:
                continue

            checkpoint = Checkpoint(
                id=frontmatter["checkpoint"],
                created=parse_iso_datetime(frontmatter.get("created")),
                parent=frontmatter.get("parent"),
                status=status,
                path=file_path,
            )
            checkpoints.append(checkpoint)

    return checkpoints


def build_tree(checkpoints: list[Checkpoint]) -> dict[str | None, list[Checkpoint]]:
    """Build tree structure: parent_id -> list of children."""
    # Create lookup for validation
    checkpoint_ids = {cp.id for cp in checkpoints}

    tree: dict[str | None, list[Checkpoint]] = {}

    for cp in checkpoints:
        # If parent doesn't exist in our checkpoints, treat as root
        parent = cp.parent if cp.parent in checkpoint_ids else None

        if parent not in tree:
            tree[parent] = []
        tree[parent].append(cp)

    # Sort children by created date (oldest first)
    for children in tree.values():
        children.sort(key=lambda c: c.created or datetime.min)

    return tree


def format_date(dt: datetime | None) -> str:
    """Format datetime as YYYY-MM-DD or 'unknown'."""
    if dt is None:
        return "unknown"
    return dt.strftime("%Y-%m-%d")


def render_tree(
    tree: dict[str | None, list[Checkpoint]],
    checkpoints_by_id: dict[str, Checkpoint],
    node_id: str | None = None,
    prefix: str = "",
    is_last: bool = True,
) -> list[str]:
    """Render tree as ASCII art lines."""
    lines = []

    if node_id is None:
        # Render all root nodes
        roots = tree.get(None, [])
        for i, root in enumerate(roots):
            is_last_root = i == len(roots) - 1

            # Root symbol and info
            symbol = "◉" if root.status == "archived" else "○"
            root_symbol = "⦿"  # Root marker
            date_str = format_date(root.created)
            lines.append(f"{root_symbol} {root.id} ({date_str}) [{root.status}]")

            # Render children
            children = tree.get(root.id, [])
            if children:
                for j, child in enumerate(children):
                    is_last_child = j == len(children) - 1
                    lines.extend(render_subtree(tree, child, "", is_last_child))
            else:
                lines.append("    (root - no branches)")

            # Add blank line between root trees (except after last)
            if not is_last_root:
                lines.append("")

    return lines


def render_subtree(
    tree: dict[str | None, list[Checkpoint]],
    node: Checkpoint,
    prefix: str,
    is_last: bool,
) -> list[str]:
    """Render a subtree starting from given node."""
    lines = []

    # Choose connector
    connector = "└── " if is_last else "├── "

    # Choose symbol based on status
    symbol = "◉" if node.status == "archived" else "○"

    # Format line
    date_str = format_date(node.created)
    lines.append(f"{prefix}{connector}{symbol} {node.id} ({date_str}) [{node.status}]")

    # Prepare prefix for children
    child_prefix = prefix + ("    " if is_last else "│   ")

    # Render children
    children = tree.get(node.id, [])
    for i, child in enumerate(children):
        is_last_child = i == len(children) - 1
        lines.extend(render_subtree(tree, child, child_prefix, is_last_child))

    return lines


def main():
    """Main entry point."""
    # Parse arguments
    if len(sys.argv) > 1:
        base_dir = Path(sys.argv[1])
    else:
        base_dir = Path("checkpoints")

    # Validate directory
    if not base_dir.exists():
        print(f"Error: Directory not found: {base_dir}")
        sys.exit(1)

    if not base_dir.is_dir():
        print(f"Error: Not a directory: {base_dir}")
        sys.exit(1)

    # Scan checkpoints
    checkpoints = scan_checkpoints(base_dir)

    if not checkpoints:
        print("No checkpoints found.")
        sys.exit(0)

    # Build lookup
    checkpoints_by_id = {cp.id: cp for cp in checkpoints}

    # Build and render tree
    tree = build_tree(checkpoints)
    lines = render_tree(tree, checkpoints_by_id)

    # Output
    for line in lines:
        print(line)


if __name__ == "__main__":
    main()
