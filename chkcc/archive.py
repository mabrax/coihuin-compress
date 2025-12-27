"""
Archive checkpoint functionality for coihuin-compress.

This module provides functionality for archiving completed checkpoints,
moving them from the active directory to the archive directory and
updating the INDEX.md file accordingly.
"""

import re
import shutil
from pathlib import Path

from chkcc.tree import Checkpoint, get_children, scan_checkpoints
from chkcc.validate import extract_frontmatter


def get_active_children(checkpoint_id: str, base_dir: Path) -> list[Checkpoint]:
    """Find all active (non-archived) children of a checkpoint.

    Args:
        checkpoint_id: The checkpoint ID to find children for
        base_dir: Base checkpoints directory (parent of active/ and archive/)

    Returns:
        List of Checkpoint objects that are children and in active/ directory
    """
    # Scan only active checkpoints for better performance
    checkpoints = scan_checkpoints(base_dir, status_filter="active")

    # Get children using helper from tree.py
    # All returned checkpoints are already non-archived
    return get_children(checkpoint_id, checkpoints)


def has_completion_section(content: str) -> bool:
    """Check if checkpoint content has a ## Completion section."""
    for line in content.split("\n"):
        if line.startswith("## Completion"):
            return True
    return False


def remove_table_row(content: str, checkpoint_name: str) -> str:
    """Remove a checkpoint row from the INDEX.md table.

    Args:
        content: The INDEX.md content
        checkpoint_name: Name of checkpoint to remove (e.g., 'chk-foo')

    Returns:
        Updated content with the row removed
    """
    lines = content.split("\n")
    result_lines = []

    for line in lines:
        # Check if this line is the table row for our checkpoint
        if line.strip().startswith(f"| {checkpoint_name} |"):
            continue  # Skip this row
        result_lines.append(line)

    return "\n".join(result_lines)


def remove_summary_section(content: str, checkpoint_name: str) -> str:
    """Remove a checkpoint summary section (## chk-xxx) from INDEX.md.

    Args:
        content: The INDEX.md content
        checkpoint_name: Name of checkpoint to remove (e.g., 'chk-foo')

    Returns:
        Updated content with the section removed
    """
    lines = content.split("\n")
    result_lines = []
    in_target_section = False

    for line in lines:
        # Check if we're entering the target section
        if line.startswith("## ") and line[3:].strip() == checkpoint_name:
            in_target_section = True
            continue

        # Check if we're leaving the section (hit another ## header or end)
        if in_target_section:
            if line.startswith("## ") or line.startswith("# "):
                in_target_section = False
                result_lines.append(line)
                continue
            # Skip lines while in target section
            continue

        result_lines.append(line)

    return "\n".join(result_lines)


def count_table_rows(content: str) -> int:
    """Count the number of data rows in the INDEX.md table.

    Args:
        content: The INDEX.md content

    Returns:
        Number of checkpoint rows (excluding header and separator)
    """
    count = 0
    in_table = False

    for line in content.split("\n"):
        stripped = line.strip()
        # Detect table start
        if "| Checkpoint | Description | Last Updated |" in stripped:
            in_table = True
            continue
        # Skip separator row
        if in_table and stripped.startswith("|") and "---" in stripped:
            continue
        # Count data rows
        if in_table and stripped.startswith("|") and stripped.endswith("|"):
            count += 1
        # End of table
        elif in_table and stripped and not stripped.startswith("|"):
            break

    return count


def add_empty_state_message(content: str) -> str:
    """Add the empty state message after the table if no checkpoints remain.

    Args:
        content: The INDEX.md content

    Returns:
        Updated content with empty state message
    """
    lines = content.split("\n")
    result_lines = []
    table_separator_found = False

    for i, line in enumerate(lines):
        result_lines.append(line)
        # Look for the table separator line (|---|---|---|)
        if line.strip().startswith("|") and "---" in line.strip():
            table_separator_found = True
            # Add empty state message after the separator
            result_lines.append("")
            result_lines.append("*No active checkpoints.*")

    return "\n".join(result_lines)


def update_index(index_path: Path, checkpoint_name: str) -> None:
    """Update INDEX.md to remove a checkpoint entry.

    Args:
        index_path: Path to INDEX.md file
        checkpoint_name: Name of checkpoint to remove

    Raises:
        FileNotFoundError: If INDEX.md doesn't exist
    """
    if not index_path.exists():
        raise FileNotFoundError(f"INDEX.md not found: {index_path}")

    content = index_path.read_text()

    # Remove the table row
    content = remove_table_row(content, checkpoint_name)

    # Remove the summary section
    content = remove_summary_section(content, checkpoint_name)

    # Check if table is now empty and add empty state message
    if count_table_rows(content) == 0:
        # Check if empty message already exists
        if "*No active checkpoints.*" not in content:
            content = add_empty_state_message(content)

    # Clean up extra blank lines
    content = re.sub(r"\n{3,}", "\n\n", content)

    # Ensure file ends with single newline
    content = content.rstrip() + "\n"

    index_path.write_text(content)


def archive_checkpoint(checkpoint_path: Path, force: bool = False) -> Path:
    """Archive a completed checkpoint.

    Moves a checkpoint from the active directory to the archive directory
    and updates INDEX.md to remove its entry.

    Args:
        checkpoint_path: Path to the checkpoint file in active/ directory
        force: If True, skip validation for active children

    Returns:
        Path to the archived checkpoint file

    Raises:
        FileNotFoundError: If checkpoint file doesn't exist
        ValueError: If checkpoint lacks ## Completion section
        ValueError: If checkpoint is not in an active/ directory
        ValueError: If checkpoint has active children (unless force=True)
    """
    # Validate checkpoint exists
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")

    # Validate checkpoint is in active/ directory
    if checkpoint_path.parent.name != "active":
        raise ValueError(
            f"Checkpoint must be in an 'active/' directory, "
            f"found: {checkpoint_path.parent.name}/"
        )

    # Read and validate checkpoint has Completion section
    content = checkpoint_path.read_text()
    if not has_completion_section(content):
        raise ValueError(
            f"Checkpoint lacks required '## Completion' section. "
            f"Add a Completion section before archiving."
        )

    # Check for active children (unless force=True)
    if not force:
        # Extract checkpoint ID from frontmatter
        frontmatter, _ = extract_frontmatter(content)
        checkpoint_id = frontmatter.get("checkpoint") if frontmatter else None

        if checkpoint_id:
            # Determine base_dir from checkpoint_path
            # checkpoint_path is in active/, base_dir is parent of active/
            base_dir = checkpoint_path.parent.parent

            active_children = get_active_children(checkpoint_id, base_dir)
            if active_children:
                child_names = "\n".join([f"  - {cp.id} ({cp.display_status})" for cp in active_children])
                raise ValueError(
                    f"Cannot archive '{checkpoint_id}': has active children\n"
                    f"{child_names}\n"
                    f"Archive children first, or use --force to override."
                )

    # Determine archive path (sibling to active/)
    active_dir = checkpoint_path.parent
    checkpoints_dir = active_dir.parent
    archive_dir = checkpoints_dir / "archive"
    archive_path = archive_dir / checkpoint_path.name

    # Create archive directory if it doesn't exist
    archive_dir.mkdir(parents=True, exist_ok=True)

    # Move the file
    shutil.move(str(checkpoint_path), str(archive_path))

    # Update INDEX.md
    index_path = active_dir / "INDEX.md"
    if index_path.exists():
        # Extract checkpoint name from filename (chk-foo.md -> chk-foo)
        checkpoint_name = checkpoint_path.stem
        update_index(index_path, checkpoint_name)

    return archive_path
