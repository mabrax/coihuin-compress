"""Initialize coihuin-compress in a project."""

import json
from pathlib import Path

INDEX_TEMPLATE = """# {title} Checkpoints

| Checkpoint | Description | Last Updated |
|------------|-------------|--------------|

---

*No {status} checkpoints.*
"""

HOOK_CONFIG = {
    "type": "command",
    "command": "chkcc prime 2>/dev/null || true"
}


def create_directory_structure(base_dir: Path) -> list[str]:
    """Create checkpoints directory structure. Returns list of created paths."""
    created = []

    active_dir = base_dir / "active"
    archive_dir = base_dir / "archive"

    for dir_path in [active_dir, archive_dir]:
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
            created.append(str(dir_path))

    return created


def create_index_files(base_dir: Path) -> list[str]:
    """Create INDEX.md files. Returns list of created paths."""
    created = []

    active_index = base_dir / "active" / "INDEX.md"
    archive_index = base_dir / "archive" / "INDEX.md"

    if not active_index.exists():
        active_index.write_text(INDEX_TEMPLATE.format(title="Active", status="active"))
        created.append(str(active_index))

    if not archive_index.exists():
        archive_index.write_text(INDEX_TEMPLATE.format(title="Archived", status="archived"))
        created.append(str(archive_index))

    return created


def install_hook(project_root: Path) -> tuple[bool, str]:
    """Install SessionStart hook. Returns (installed, message)."""
    claude_dir = project_root / ".claude"
    settings_path = claude_dir / "settings.json"

    # Create .claude directory if needed
    claude_dir.mkdir(parents=True, exist_ok=True)

    # Load existing settings or create new
    if settings_path.exists():
        settings = json.loads(settings_path.read_text())
    else:
        settings = {}

    # Ensure hooks structure exists
    if "hooks" not in settings:
        settings["hooks"] = {}

    if "SessionStart" not in settings["hooks"]:
        settings["hooks"]["SessionStart"] = []

    # Check if hook already installed
    session_hooks = settings["hooks"]["SessionStart"]
    for hook in session_hooks:
        if isinstance(hook, dict) and "chkcc prime" in hook.get("command", ""):
            return (False, "Hook already installed")

    # Add the hook
    session_hooks.append(HOOK_CONFIG)

    # Write back
    settings_path.write_text(json.dumps(settings, indent=2) + "\n")

    return (True, str(settings_path))


def cmd_init(base_dir: Path, project_root: Path) -> None:
    """Main init command logic."""
    print("Initializing coihuin-compress...")
    print()

    # Create directories
    created_dirs = create_directory_structure(base_dir)
    for d in created_dirs:
        print(f"  Created: {d}")

    # Create INDEX files
    created_files = create_index_files(base_dir)
    for f in created_files:
        print(f"  Created: {f}")

    # Install hook
    installed, msg = install_hook(project_root)
    if installed:
        print(f"  Installed hook: {msg}")
    else:
        print(f"  {msg}")

    print()
    print("Done. Run 'chkcc doctor' to verify setup.")
