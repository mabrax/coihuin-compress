"""
Checkpoint lineage tree visualizer for coihuin-compress.

Displays checkpoint parent-child relationships as an ASCII tree.

This module provides library functions for tree visualization. For CLI usage,
use the chkcc command line tool.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from chkcc.validate import extract_frontmatter, parse_iso_datetime


@dataclass
class Checkpoint:
    """Represents a checkpoint with its metadata."""

    id: str
    created: datetime | None
    parent: str | None
    path: Path
    status: str = "active"  # Frontmatter status: 'current' or 'active'
    is_archived: bool = False  # True if checkpoint is in archive/ directory

    @property
    def display_status(self) -> str:
        """Get the display status for tree rendering.

        Returns:
            'archived' if in archive directory (synthetic status, not from frontmatter),
            otherwise frontmatter status ('current' or 'active')
        """
        if self.is_archived:
            return "archived"
        return self.status


def scan_checkpoints(base_dir: Path, status_filter: str = "all") -> list[Checkpoint]:
    """Scan checkpoint directories and return list of Checkpoint objects.

    Args:
        base_dir: Path to checkpoints directory (should contain active/ and archive/)
        status_filter: Filter by status - 'active', 'archive', or 'all'

    Returns:
        List of Checkpoint objects found in the directory
    """
    checkpoints = []

    # Determine which directories to scan based on filter
    # Format: (subdir_name, is_archived)
    if status_filter == "active":
        dirs_to_scan = [("active", False)]
    elif status_filter == "archive":
        dirs_to_scan = [("archive", True)]
    else:  # 'all'
        dirs_to_scan = [("active", False), ("archive", True)]

    for subdir, is_archived in dirs_to_scan:
        dir_path = base_dir / subdir
        if not dir_path.exists():
            continue

        for file_path in dir_path.glob("chk-*.md"):
            content = file_path.read_text()
            # extract_frontmatter returns (dict | None, body_str)
            frontmatter, _ = extract_frontmatter(content)

            if frontmatter is None or "checkpoint" not in frontmatter:
                continue

            # Extract status from frontmatter, default to 'active' for backward compat
            frontmatter_status = frontmatter.get("status", "active")

            # Validate status value per checkpoint-format.md spec
            if frontmatter_status not in ("current", "active"):
                import sys
                print(f"Warning: Invalid status '{frontmatter_status}' in {file_path}, defaulting to 'active'",
                      file=sys.stderr)
                frontmatter_status = "active"

            checkpoint = Checkpoint(
                id=frontmatter["checkpoint"],
                created=parse_iso_datetime(frontmatter.get("created")),
                parent=frontmatter.get("parent"),
                path=file_path,
                status=frontmatter_status,
                is_archived=is_archived,
            )
            checkpoints.append(checkpoint)

    # Validate: Only one active checkpoint should have status 'current'
    current_checkpoints = [
        cp for cp in checkpoints
        if not cp.is_archived and cp.status == "current"
    ]
    if len(current_checkpoints) > 1:
        import sys
        print(
            f"Warning: Found {len(current_checkpoints)} checkpoints with status 'current', "
            f"expected at most 1:",
            file=sys.stderr
        )
        for cp in current_checkpoints:
            print(f"  - {cp.id} ({cp.path})", file=sys.stderr)

    return checkpoints


def build_tree(checkpoints: list[Checkpoint]) -> dict[str | None, list[Checkpoint]]:
    """Build tree structure: parent_id -> list of children.

    Args:
        checkpoints: List of Checkpoint objects

    Returns:
        Dictionary mapping parent_id to list of child Checkpoints.
        Key of None represents root nodes (no parent or parent not found).
    """
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


def get_children(checkpoint_id: str, checkpoints: list[Checkpoint]) -> list[Checkpoint]:
    """Return all checkpoints that have this checkpoint_id as their parent.

    Used by archive validation to check for active children before archiving.

    Args:
        checkpoint_id: The checkpoint ID to find children for
        checkpoints: List of Checkpoint objects to search

    Returns:
        List of Checkpoints that have checkpoint_id as their parent,
        sorted by creation date (oldest first)
    """
    children = [cp for cp in checkpoints if cp.parent == checkpoint_id]
    children.sort(key=lambda c: c.created or datetime.min)
    return children


def format_date(dt: datetime | None) -> str:
    """Format datetime as YYYY-MM-DD or 'unknown'.

    Args:
        dt: datetime object or None

    Returns:
        Formatted date string or 'unknown'
    """
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
    """Render tree as ASCII art lines.

    Args:
        tree: Tree structure from build_tree()
        checkpoints_by_id: Lookup dictionary of checkpoint id -> Checkpoint
        node_id: Starting node id (None for roots)
        prefix: Current line prefix for indentation
        is_last: Whether this is the last sibling

    Returns:
        List of formatted lines representing the tree
    """
    lines = []

    if node_id is None:
        # Render all root nodes
        roots = tree.get(None, [])
        for i, root in enumerate(roots):
            is_last_root = i == len(roots) - 1

            # Root symbol and info
            root_symbol = "\u29bf"  # Root marker
            date_str = format_date(root.created)
            lines.append(f"{root_symbol} {root.id} ({date_str}) [{root.display_status}]")

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
    """Render a subtree starting from given node.

    Args:
        tree: Tree structure from build_tree()
        node: Checkpoint node to render
        prefix: Current line prefix for indentation
        is_last: Whether this is the last sibling

    Returns:
        List of formatted lines representing the subtree
    """
    lines = []

    # Choose connector
    connector = "\u2514\u2500\u2500 " if is_last else "\u251c\u2500\u2500 "

    # Choose symbol based on display status
    display_status = node.display_status
    symbol = "\u25c9" if display_status == "archived" else "\u25cb"

    # Format line
    date_str = format_date(node.created)
    lines.append(f"{prefix}{connector}{symbol} {node.id} ({date_str}) [{display_status}]")

    # Prepare prefix for children
    child_prefix = prefix + ("    " if is_last else "\u2502   ")

    # Render children
    children = tree.get(node.id, [])
    for i, child in enumerate(children):
        is_last_child = i == len(children) - 1
        lines.extend(render_subtree(tree, child, child_prefix, is_last_child))

    return lines


def show_tree(base_dir: Path, status_filter: str = "all") -> list[str]:
    """Show checkpoint tree for a directory.

    Args:
        base_dir: Path to checkpoints directory (should contain active/ and archive/)
        status_filter: Filter by status - 'active', 'archive', or 'all'

    Returns:
        List of lines representing the tree

    Raises:
        FileNotFoundError: If directory doesn't exist
        NotADirectoryError: If path is not a directory
    """
    if not base_dir.exists():
        raise FileNotFoundError(f"Directory not found: {base_dir}")

    if not base_dir.is_dir():
        raise NotADirectoryError(f"Not a directory: {base_dir}")

    # Scan checkpoints
    checkpoints = scan_checkpoints(base_dir, status_filter)

    if not checkpoints:
        if status_filter == "all":
            return ["No checkpoints found."]
        return [f"No {status_filter} checkpoints found."]

    # Build lookup
    checkpoints_by_id = {cp.id: cp for cp in checkpoints}

    # Build and render tree
    tree = build_tree(checkpoints)
    lines = render_tree(tree, checkpoints_by_id)

    return lines
