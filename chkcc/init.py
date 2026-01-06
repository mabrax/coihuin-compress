"""Initialize coihuin-compress in a project."""

import json
from importlib import resources
from importlib.resources import abc as resources_abc
from pathlib import Path

INDEX_TEMPLATE = """# {title} Checkpoints

| Checkpoint | Description | Last Updated |
|------------|-------------|--------------|

---

*No {status} checkpoints.*
"""


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


def install_skill_files(project_root: Path) -> list[str]:
    """
    Copy all files from package chkcc/data/skill/ to .claude/skills/coihuin-compress/.

    Returns:
        List of created file paths.
    """
    created = []
    skills_dir = project_root / ".claude" / "skills" / "coihuin-compress"

    # Use importlib.resources to access package data
    package_path = resources.files("chkcc").joinpath("data", "skill")

    def traverse(base: resources_abc.Traversable, prefix: str = "") -> None:
        """Recursively traverse and copy package resources."""
        for item in base.iterdir():
            rel_path = str(Path(prefix) / item.name) if prefix else item.name

            if item.is_file():
                target_path = skills_dir / rel_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_bytes(item.read_bytes())
                created.append(str(target_path))
            elif item.is_dir():
                traverse(item, rel_path)

    traverse(package_path)
    return created


def install_hooks(project_root: Path) -> list[tuple[bool, str]]:
    """
    Install SessionStart and Stop hooks.

    Returns:
        List of (installed, message) tuples for each hook type.
    """
    results = []
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

    # Install SessionStart hook
    if "SessionStart" not in settings["hooks"]:
        settings["hooks"]["SessionStart"] = []

    session_hooks = settings["hooks"]["SessionStart"]
    session_installed = False

    # Check if SessionStart hook already installed
    for hook_entry in session_hooks:
        if isinstance(hook_entry, dict) and hook_entry.get("matcher") == "":
            for h in hook_entry.get("hooks", []):
                if isinstance(h, dict) and "chkcc prime" in h.get("command", ""):
                    session_installed = True
                    break

    if not session_installed:
        # Add matcher-based SessionStart hook
        session_hooks.append({
            "matcher": "",
            "hooks": [{"type": "command", "command": "chkcc prime 2>/dev/null || true"}]
        })
        results.append((True, "SessionStart hook installed"))
    else:
        results.append((False, "SessionStart hook already installed"))

    # Install Stop hook
    if "Stop" not in settings["hooks"]:
        settings["hooks"]["Stop"] = []

    stop_hooks = settings["hooks"]["Stop"]
    stop_installed = False

    # Check if Stop hook already installed (new or old format)
    for hook_entry in stop_hooks:
        if isinstance(hook_entry, dict):
            # New matcher-based format
            if hook_entry.get("matcher") == "":
                for h in hook_entry.get("hooks", []):
                    if isinstance(h, dict) and "chkcc stop-hook" in h.get("command", ""):
                        stop_installed = True
                        break
            # Old direct hook format (stop-checkpoint.py)
            if "stop-checkpoint.py" in hook_entry.get("command", ""):
                stop_installed = True

    if not stop_installed:
        # Add matcher-based Stop hook
        stop_hooks.append({
            "matcher": "",
            "hooks": [{"type": "command", "command": "chkcc stop-hook"}]
        })
        results.append((True, "Stop hook installed"))
    else:
        results.append((False, "Stop hook already installed"))

    # Write back settings
    settings_path.write_text(json.dumps(settings, indent=2) + "\n")

    return results


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

    # Install skill files
    created_skills = install_skill_files(project_root)
    for f in created_skills:
        print(f"  Installed: {f}")

    # Install hooks
    hook_results = install_hooks(project_root)
    for installed, msg in hook_results:
        if installed:
            print(f"  Installed hook: {msg}")
        else:
            print(f"  {msg}")

    print()
    print("Done. Run 'chkcc doctor' to verify setup.")
