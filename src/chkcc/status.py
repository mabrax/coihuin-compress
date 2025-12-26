"""
Status command for displaying checkpoint summaries with context and next actions.

Answers "What am I working on and what's next?" with a content-focused view
that complements the tree command's structure-focused view.
"""

import re
from pathlib import Path

from chkcc.tree import Checkpoint, format_date, scan_checkpoints


def extract_problem_summary(content: str) -> str:
    """Extract first line of ## Problem section.

    Returns the first non-empty line after '## Problem' heading.
    Returns empty string if section not found.

    Args:
        content: Full markdown content of checkpoint file

    Returns:
        First non-empty line of Problem section, or empty string
    """
    # Match ## Problem heading (with optional whitespace)
    pattern = r"^##\s+Problem\s*$"
    lines = content.split("\n")

    in_problem_section = False
    for line in lines:
        if in_problem_section:
            # Skip empty lines until we find content
            stripped = line.strip()
            if stripped:
                # Stop at next heading
                if stripped.startswith("#"):
                    return ""
                return stripped
        elif re.match(pattern, line, re.IGNORECASE):
            in_problem_section = True

    return ""


def extract_next_action(content: str) -> str | None:
    """Extract first uncompleted item from ### Next Actions section.

    Returns first uncompleted list item (- or * prefixed, with [ ] or no checkbox)
    after '### Next Actions'. If all items are completed ([x]), returns None.
    Returns None if section not found or empty.

    Args:
        content: Full markdown content of checkpoint file

    Returns:
        First uncompleted list item text (without prefix/checkbox), or None
    """
    # Match ### Next Actions heading (with optional whitespace)
    pattern = r"^###\s+Next\s+Actions\s*$"
    lines = content.split("\n")

    in_next_actions = False
    for line in lines:
        if in_next_actions:
            stripped = line.strip()
            # Stop at next heading
            if stripped.startswith("#"):
                return None
            # Look for list items (- or *)
            list_match = re.match(r"^[-*]\s+(.+)$", stripped)
            if list_match:
                item_text = list_match.group(1)
                # Skip completed items (marked with [x] or [X])
                if re.match(r"^\[[xX]\]", item_text):
                    continue
                # Remove uncompleted checkbox if present: [ ]
                item_text = re.sub(r"^\[ \]\s*", "", item_text)
                return item_text.strip()
        elif re.match(pattern, line, re.IGNORECASE):
            in_next_actions = True

    return None


def format_status_entry(
    checkpoint: Checkpoint, problem: str, next_action: str | None
) -> str:
    """Format a single checkpoint status entry.

    Output format:
    chk-name [current] (2025-12-20)
      -> Problem summary here
      >> Next action item

    If no next_action, show:
      >> (none)

    Args:
        checkpoint: Checkpoint object with metadata
        problem: Problem summary text
        next_action: Next action item text, or None

    Returns:
        Formatted multi-line status entry string
    """
    date_str = format_date(checkpoint.created)
    status_str = checkpoint.display_status

    lines = [
        f"{checkpoint.id} [{status_str}] ({date_str})",
        f"  -> {problem if problem else '(no problem summary)'}",
        f"  >> {next_action if next_action else '(none)'}",
    ]

    return "\n".join(lines)


def cmd_status(base_dir: Path, show_all: bool = False) -> None:
    """Display checkpoint status summaries.

    Args:
        base_dir: Base checkpoints directory (parent of active/ and archive/)
        show_all: If True, include archived checkpoints. Default False.

    Logic:
    1. Call scan_checkpoints() from tree.py
    2. Filter to active-only unless show_all=True
    3. Sort: current first, then by date (newest first)
    4. For each: read file, extract problem/next, format and print
    5. If no checkpoints found, print appropriate message
    """
    # Determine filter based on show_all flag
    status_filter = "all" if show_all else "active"

    # Scan checkpoints
    checkpoints = scan_checkpoints(base_dir, status_filter)

    if not checkpoints:
        if show_all:
            print("No checkpoints found.")
        else:
            print("No active checkpoints found.")
        return

    # Sort: current first, then by date (newest first)
    def sort_key(cp: Checkpoint) -> tuple[int, float]:
        # Only active (non-archived) checkpoints with status='current' get priority
        status_priority = 0 if (not cp.is_archived and cp.status == "current") else 1
        timestamp = cp.created.timestamp() if cp.created else 0
        return (status_priority, -timestamp)

    checkpoints.sort(key=sort_key)

    # Collect entries, handling read errors
    entries = []
    for cp in checkpoints:
        try:
            content = cp.path.read_text()
        except (OSError, UnicodeDecodeError) as e:
            import sys
            print(f"Warning: Could not read {cp.path}: {e}", file=sys.stderr)
            continue

        problem = extract_problem_summary(content)
        next_action = extract_next_action(content)
        entry = format_status_entry(cp, problem, next_action)
        entries.append(entry)

    # Print with blank lines between
    print("\n\n".join(entries))
