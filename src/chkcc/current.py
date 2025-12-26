"""
Current checkpoint management for coihuin-compress.

Provides functionality to mark a single checkpoint as the "current" focus.
Only ONE checkpoint can be current at a time. Status is stored in frontmatter
as `status: current` or `status: active`.
"""

import os
import re
import stat
import tempfile
from pathlib import Path

from chkcc.tree import Checkpoint, scan_checkpoints


def get_current(base_dir: Path) -> Checkpoint | None:
    """Find the checkpoint with status: current.

    Args:
        base_dir: Base checkpoints directory (parent of active/)

    Returns:
        The current Checkpoint, or None if no checkpoint is current.
    """
    checkpoints = scan_checkpoints(base_dir, status_filter="active")

    for cp in checkpoints:
        if cp.status == "current":
            return cp

    return None


def update_frontmatter_status(checkpoint_path: Path, new_status: str) -> None:
    """Update the status field in a checkpoint's frontmatter.

    Args:
        checkpoint_path: Path to the checkpoint file
        new_status: New status value ('current' or 'active')

    This function reads the file, updates/adds the status field in the
    YAML frontmatter, and writes it back atomically.

    If status field exists, update it.
    If status field doesn't exist and new_status is 'current', add it.
    If status field doesn't exist and new_status is 'active', don't add it (default).
    """
    # Validate new_status
    if new_status not in ("current", "active"):
        raise ValueError(f"Invalid status '{new_status}', must be 'current' or 'active'")

    content = checkpoint_path.read_text(encoding='utf-8')

    # Match frontmatter: starts with ---, ends with ---
    # Use re.DOTALL so . matches newlines
    frontmatter_pattern = r"^---\n(.*?)---\n"
    match = re.match(frontmatter_pattern, content, re.DOTALL)

    if not match:
        raise ValueError(f"Invalid frontmatter format in: {checkpoint_path}")

    frontmatter_text = match.group(1)
    # Extract body - everything after the closing ---\n
    # This preserves any blank lines between frontmatter and content
    body = content[match.end():]

    # Update or add status field
    frontmatter_lines = frontmatter_text.rstrip("\n").split("\n")
    new_frontmatter_lines = []
    status_found = False

    for line in frontmatter_lines:
        if line.startswith("status:"):
            new_frontmatter_lines.append(f"status: {new_status}")
            status_found = True
        else:
            new_frontmatter_lines.append(line)

    # Only add status field if setting to current (non-default)
    if not status_found and new_status == "current":
        new_frontmatter_lines.append(f"status: {new_status}")

    new_frontmatter = "\n".join(new_frontmatter_lines)
    new_content = f"---\n{new_frontmatter}\n---\n{body}"

    # Atomic write - write to temp file then rename
    tmp_fd, tmp_path = tempfile.mkstemp(
        dir=checkpoint_path.parent,
        suffix=".tmp",
        prefix=checkpoint_path.stem,
    )
    try:
        with os.fdopen(tmp_fd, 'w', encoding='utf-8') as f:
            f.write(new_content)
        # Preserve original file permissions
        original_mode = os.stat(checkpoint_path).st_mode
        os.chmod(tmp_path, stat.S_IMODE(original_mode))
        # Atomic rename (on POSIX systems)
        os.replace(tmp_path, checkpoint_path)
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def clear_current(base_dir: Path) -> Checkpoint | None:
    """Clear the current checkpoint by setting it to active.

    Args:
        base_dir: Base checkpoints directory

    Returns:
        The checkpoint that was cleared, or None if no current existed.
    """
    current = get_current(base_dir)

    if current is None:
        return None

    update_frontmatter_status(current.path, "active")
    return current


def set_current(checkpoint_path: Path, base_dir: Path) -> None:
    """Set a checkpoint as current, clearing any existing current first.

    Args:
        checkpoint_path: Path to checkpoint to make current
        base_dir: Base checkpoints directory

    Raises:
        ValueError: If checkpoint is not in active/ directory
        FileNotFoundError: If checkpoint file doesn't exist

    Steps:
    1. Validate checkpoint exists and is in active/ directory
    2. Clear any existing current checkpoint
    3. Set the new checkpoint as current
    """
    # Validate checkpoint exists
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint file not found: {checkpoint_path}")

    # Validate checkpoint is in active/ directory
    active_dir = base_dir / "active"
    try:
        checkpoint_path.relative_to(active_dir)
    except ValueError:
        raise ValueError(
            f"Checkpoint must be in active/ directory. "
            f"Got: {checkpoint_path}, expected under: {active_dir}"
        )

    # Clear any existing current checkpoint
    clear_current(base_dir)

    # Set the new checkpoint as current
    update_frontmatter_status(checkpoint_path, "current")


def cmd_current(
    base_dir: Path, checkpoint_path: Path | None = None, clear: bool = False
) -> None:
    """Main current command logic.

    Args:
        base_dir: Base checkpoints directory
        checkpoint_path: Path to checkpoint to set as current (optional)
        clear: If True, clear current without setting new one

    Behavior:
    - No args: Show current checkpoint or "No current checkpoint"
    - checkpoint_path: Set that checkpoint as current
    - clear=True: Clear current, show confirmation
    """
    if clear:
        # Clear current checkpoint
        cleared = clear_current(base_dir)
        if cleared:
            print(f"Cleared current: {cleared.id}")
        else:
            print("No current checkpoint to clear")
        return

    if checkpoint_path is not None:
        # Set checkpoint as current
        set_current(checkpoint_path, base_dir)
        print(f"Set current: {checkpoint_path.stem}")
        return

    # Show current checkpoint
    current = get_current(base_dir)
    if current:
        print(f"Current: {current.id}")
        print(f"  Path: {current.path}")
    else:
        print("No current checkpoint")
