"""
Checkpoint and delta scaffold generator for coihuin-compress.

This module provides functions to generate checkpoint and delta markdown
templates, enabling quick creation of properly structured checkpoint files.
"""

from datetime import datetime, timezone
from pathlib import Path


def get_timestamp() -> str:
    """Get current UTC timestamp in ISO 8601 format.

    Returns:
        ISO 8601 formatted timestamp (e.g., 2025-12-22T15:30:00Z)
    """
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get_checkpoint_template(
    name: str,
    parent: str | None = None,
    anchor: str | None = None,
) -> str:
    """Generate a checkpoint markdown template.

    Args:
        name: Name for the checkpoint (used in frontmatter)
        parent: Optional parent checkpoint name for branching
        anchor: Optional anchor reference (e.g., branch name, commit, PR)

    Returns:
        Markdown string with checkpoint template including HTML guidance comments
    """
    timestamp = get_timestamp()

    # Build frontmatter
    frontmatter_lines = [
        "---",
        f"checkpoint: {name}",
        f"created: {timestamp}",
    ]
    if anchor:
        frontmatter_lines.append(f"anchor: {anchor}")
    if parent:
        frontmatter_lines.append(f"parent: {parent}")
    frontmatter_lines.append("---")
    frontmatter = "\n".join(frontmatter_lines)

    template = f"""{frontmatter}

## Problem
<!-- 1-2 sentences. What are we solving? Must stand alone without context. -->

## Session Intent
<!-- User's goal. Include constraints and requirements. -->

## Essential Information

### Decisions
<!-- Format: - **Decision**: Rationale (why chosen, what rejected) -->

### Technical Context
<!-- Stack, environment, key dependencies relevant to the work. -->

### Breadcrumbs
<!-- Minimal references for reconstruction. -->
| Type | Reference | Hint |
|------|-----------|------|

### Play-By-Play
<!-- Major actions. Format: - Phase -> Action -> Outcome -->

### Artifact Trail
<!-- Files touched. -->
| File | Status | Key Change |
|------|--------|------------|

### Current State
<!-- Concrete: what exists NOW. Not "good progress" - specific. -->

### Next Actions
<!-- Specific enough to execute without clarification. -->

## User Rules
<!-- Constraints the agent must follow. Optional. -->
"""
    return template


def get_delta_template() -> str:
    """Generate a delta markdown template to append to existing checkpoint.

    Returns:
        Markdown string with delta template including HTML guidance comments
    """
    timestamp = get_timestamp()

    template = f"""

---

## Delta: {timestamp}

### What Changed
<!-- One sentence: what was accomplished this session? -->

### Artifacts
<!-- Files created/modified/deleted. -->
| File | Action | Description |
|------|--------|-------------|

### Status Transitions
<!-- Optional: track phase/task changes. -->
| Item | Before | After |
|------|--------|-------|
"""
    return template


def normalize_checkpoint_name(name: str) -> str:
    """Normalize checkpoint name to ensure chk- prefix.

    Args:
        name: Raw checkpoint name

    Returns:
        Name with chk- prefix if not already present

    Raises:
        ValueError: If name contains path separators or invalid characters
    """
    # Validate no path traversal attempts
    if "/" in name or "\\" in name or ".." in name:
        raise ValueError(f"Checkpoint name cannot contain path separators: {name}")

    if not name.startswith("chk-"):
        return f"chk-{name}"
    return name


def scaffold_checkpoint(
    name: str,
    parent: str | None = None,
    anchor: str | None = None,
    *,
    output_dir: Path,
) -> Path:
    """Create a new checkpoint file from template.

    Args:
        name: Name for the checkpoint
        parent: Optional parent checkpoint name for branching
        anchor: Optional anchor reference (e.g., branch name, commit, PR)
        output_dir: Directory where checkpoint file will be created

    Returns:
        Path to the created checkpoint file

    Raises:
        FileExistsError: If checkpoint file already exists
        FileNotFoundError: If output_dir doesn't exist or parent doesn't exist
        ValueError: If name contains invalid characters
    """
    if not output_dir.exists():
        raise FileNotFoundError(f"Output directory not found: {output_dir}")

    # Normalize the name to ensure chk- prefix
    normalized_name = normalize_checkpoint_name(name)
    filename = f"{normalized_name}.md"
    file_path = output_dir / filename

    if file_path.exists():
        raise FileExistsError(f"Checkpoint already exists: {file_path}")

    # Normalize and validate parent if specified
    normalized_parent = None
    if parent:
        normalized_parent = normalize_checkpoint_name(parent)
        parent_path = output_dir / f"{normalized_parent}.md"
        if not parent_path.exists():
            raise FileNotFoundError(f"Parent checkpoint not found: {parent_path}")

    # Generate template content
    template = get_checkpoint_template(normalized_name, normalized_parent, anchor)

    # Write the file with explicit encoding
    file_path.write_text(template, encoding="utf-8")

    return file_path


def scaffold_delta(checkpoint_path: Path) -> None:
    """Append a delta section to an existing checkpoint file.

    Updates the `last_delta` field in frontmatter and appends the delta template.

    Args:
        checkpoint_path: Path to the existing checkpoint file

    Raises:
        FileNotFoundError: If checkpoint file doesn't exist
        ValueError: If checkpoint file doesn't have valid frontmatter
    """
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")

    # Read existing content with explicit encoding
    existing_content = checkpoint_path.read_text(encoding="utf-8")

    # Validate frontmatter exists
    if not existing_content.startswith("---"):
        raise ValueError(f"Invalid checkpoint format (missing frontmatter): {checkpoint_path}")

    # Find end of frontmatter
    end_marker = existing_content.find("\n---", 3)
    if end_marker == -1:
        raise ValueError(f"Invalid checkpoint format (unclosed frontmatter): {checkpoint_path}")

    # Extract frontmatter and body
    frontmatter = existing_content[4:end_marker]  # Skip opening "---\n"
    body = existing_content[end_marker + 4:]  # Skip "\n---"

    # Update or add last_delta in frontmatter
    timestamp = get_timestamp()
    lines = frontmatter.split("\n")
    updated_lines = []
    found_last_delta = False

    for line in lines:
        if line.startswith("last_delta:"):
            updated_lines.append(f"last_delta: {timestamp}")
            found_last_delta = True
        else:
            updated_lines.append(line)

    if not found_last_delta:
        updated_lines.append(f"last_delta: {timestamp}")

    # Reconstruct content with updated frontmatter
    new_frontmatter = "\n".join(updated_lines)
    updated_content = f"---\n{new_frontmatter}\n---{body}"

    # Generate delta template
    delta = get_delta_template()

    # Append delta to content
    new_content = updated_content.rstrip("\n") + "\n" + delta

    # Write back with explicit encoding
    checkpoint_path.write_text(new_content, encoding="utf-8")
