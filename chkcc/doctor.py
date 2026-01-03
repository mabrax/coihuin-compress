"""Health check for coihuin-compress setup."""

import json
from pathlib import Path


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
        if isinstance(hook, dict) and "chkcc prime" in hook.get("command", ""):
            return (True, "✓ SessionStart hook installed")

    return (False, "✗ SessionStart hook not found")


def cmd_doctor(base_dir: Path, project_root: Path) -> int:
    """Main doctor command logic. Returns 0 if healthy, 1 if issues found."""
    print("Checking coihuin-compress setup...")
    print()

    checks = []

    # Directory checks
    checks.append(check_directory(base_dir / "active"))
    checks.append(check_directory(base_dir / "archive"))

    # File checks
    checks.append(check_file(base_dir / "active" / "INDEX.md"))

    # Hook check
    checks.append(check_hook(project_root))

    all_passed = True
    for passed, msg in checks:
        print(f"  {msg}")
        if not passed:
            all_passed = False

    print()
    if all_passed:
        print("All checks passed.")
        return 0
    else:
        print("Issues found. Run 'chkcc init' to fix.")
        return 1
