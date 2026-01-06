"""Health check for coihuin-compress setup."""

import json
from pathlib import Path

from chkcc import init
from chkcc.update import (
    compute_checksum,
    determine_file_status,
    get_installed_skill_files,
    get_package_skill_files,
)


def check_directory(path: Path) -> tuple[bool, str]:
    """Check if directory exists."""
    if path.exists() and path.is_dir():
        return (True, f"✓ {path}")
    return (False, f"✗ {path} (missing)")


def check_file(path: Path) -> tuple[bool, str]:
    """Check if file exists."""
    if path.exists() and path.is_file():
        return (True, f"✓ {path}")
    return (False, f"✗ {path} (missing)")


def check_hook(project_root: Path) -> tuple[bool, str]:
    """Check if SessionStart hook is installed."""
    settings_path = project_root / ".claude" / "settings.json"

    if not settings_path.exists():
        return (False, f"✗ {settings_path} (missing)")

    try:
        settings = json.loads(settings_path.read_text())
    except json.JSONDecodeError:
        return (False, f"✗ {settings_path} (invalid JSON)")

    hooks = settings.get("hooks", {})
    session_hooks = hooks.get("SessionStart", [])

    for hook in session_hooks:
        if isinstance(hook, dict):
            # Check old direct hook format
            if "chkcc prime" in hook.get("command", ""):
                return (True, "✓ SessionStart hook installed")
            # Check new matcher-based format
            if hook.get("matcher") == "":
                for h in hook.get("hooks", []):
                    if isinstance(h, dict) and "chkcc prime" in h.get("command", ""):
                        return (True, "✓ SessionStart hook installed")

    return (False, "✗ SessionStart hook not found")


def check_stop_hook(project_root: Path) -> tuple[bool, str]:
    """Check if Stop hook is installed."""
    settings_path = project_root / ".claude" / "settings.json"

    if not settings_path.exists():
        return (False, "✗ Stop hook not found")

    try:
        settings = json.loads(settings_path.read_text())
    except json.JSONDecodeError:
        return (False, "✗ Stop hook not found")

    hooks = settings.get("hooks", {})
    stop_hooks = hooks.get("Stop", [])

    for hook in stop_hooks:
        if isinstance(hook, dict):
            # Check new matcher-based format
            if hook.get("matcher") == "":
                for h in hook.get("hooks", []):
                    if isinstance(h, dict) and "chkcc stop-hook" in h.get("command", ""):
                        return (True, "✓ Stop hook installed")
            # Check old direct hook format (stop-checkpoint.py)
            if "stop-checkpoint.py" in hook.get("command", ""):
                return (True, "✓ Stop hook installed")

    return (False, "✗ Stop hook not found")


def check_skill_files(project_root: Path) -> list[tuple[bool, str]]:
    """
    Check skill file health by comparing installed vs package files.

    Returns:
        List of check results for each file.
    """
    results = []
    skill_dir = project_root / ".claude" / "skills" / "coihuin-compress"

    # Get package and installed files
    package_files = get_package_skill_files()
    installed_files = get_installed_skill_files(skill_dir)

    # Check each file in package
    for rel_path in sorted(package_files.keys()):
        package_content = package_files[rel_path]
        status = determine_file_status(rel_path, package_content, installed_files)

        if status == "unchanged":
            results.append((True, f"✓ {rel_path} (matches)"))
        elif status == "modified":
            results.append((False, f"✗ {rel_path} (differs)"))
        elif status == "added":
            results.append((False, f"✗ {rel_path} (missing)"))

    return results


def cmd_doctor(base_dir: Path, project_root: Path, fix: bool = False) -> int:
    """Main doctor command logic. Returns 0 if healthy, 1 if issues found."""
    print("Checking coihuin-compress setup...")
    print()

    checks = []

    # Directory checks
    checks.append(check_directory(base_dir / "active"))
    checks.append(check_directory(base_dir / "archive"))

    # File checks
    checks.append(check_file(base_dir / "active" / "INDEX.md"))

    # Hook checks
    checks.append(check_hook(project_root))
    checks.append(check_stop_hook(project_root))

    all_passed = True
    for passed, msg in checks:
        print(f"  {msg}")
        if not passed:
            all_passed = False

    # Skill file checks
    skill_checks = check_skill_files(project_root)
    if skill_checks:
        print()
        print("Skill files:")
        for passed, msg in skill_checks:
            print(f"  {msg}")
            if not passed:
                all_passed = False

    print()
    if all_passed:
        print("All checks passed.")
        return 0

    if not fix:
        print("Issues found. Run 'chkcc doctor --fix' to repair.")
        return 1

    # Fix mode: repair issues
    print("Fixing issues...")
    print()

    # Fix directories and INDEX files
    created_dirs = init.create_directory_structure(base_dir)
    for d in created_dirs:
        print(f"  Created: {d}")

    created_files = init.create_index_files(base_dir)
    for f in created_files:
        print(f"  Created: {f}")

    # Fix hooks
    hook_results = init.install_hooks(project_root)
    for installed, msg in hook_results:
        if installed:
            print(f"  Installed: {msg}")

    # Fix skill files
    created_skills = init.install_skill_files(project_root)
    for f in created_skills:
        print(f"  Installed: {f}")

    if any(not passed for passed, _ in skill_checks):
        print()
        print("Run 'chkcc update' to sync skill files.")

    print()
    print("Fixed. Run 'chkcc doctor' to verify.")
    return 0
