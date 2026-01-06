"""Update skill files from package to project installation."""

import hashlib
from importlib import resources
from importlib.resources import abc as resources_abc
from pathlib import Path


def compute_checksum(content: bytes) -> str:
    """Compute SHA256 checksum of content."""
    return hashlib.sha256(content).hexdigest()


def get_package_skill_files() -> dict[str, bytes]:
    """Return dict of {relative_path: content} for all skill files in package."""
    result: dict[str, bytes] = {}

    # Use importlib.resources to access package data
    package_path = resources.files("chkcc").joinpath("data", "skill")

    def traverse(base: resources_abc.Traversable, prefix: str = "") -> None:
        """Recursively traverse the package resources."""
        for item in base.iterdir():
            rel_path = str(Path(prefix) / item.name) if prefix else item.name
            if item.is_file():
                result[rel_path] = item.read_bytes()
            elif item.is_dir():
                traverse(item, rel_path)

    traverse(package_path)
    return result


def get_installed_skill_files(skill_dir: Path) -> dict[str, bytes]:
    """Return dict of {relative_path: content} for installed skill files."""
    result: dict[str, bytes] = {}

    if not skill_dir.exists():
        return result

    for file_path in skill_dir.rglob("*"):
        if file_path.is_file():
            rel_path = str(file_path.relative_to(skill_dir))
            result[rel_path] = file_path.read_bytes()

    return result


def determine_file_status(
    rel_path: str,
    package_content: bytes,
    installed_files: dict[str, bytes],
) -> str:
    """
    Determine the status of a file.

    Returns one of: 'unchanged', 'modified', 'added'

    Note: Without tracking original checksums at install time, we cannot
    distinguish "package updated" from "local modified". We conservatively
    treat any difference as "modified" to avoid overwriting user changes.
    """
    if rel_path not in installed_files:
        return "added"

    installed_content = installed_files[rel_path]
    package_checksum = compute_checksum(package_content)
    installed_checksum = compute_checksum(installed_content)

    if package_checksum == installed_checksum:
        return "unchanged"

    # Files differ - treat as locally modified (conservative approach)
    return "modified"


def cmd_update(skill_dir: Path, force: bool = False, dry_run: bool = False) -> int:
    """
    Update skill files from package to installation.

    Args:
        skill_dir: Path to installed skill directory (.claude/skills/coihuin-compress/)
        force: If True, overwrite local modifications
        dry_run: If True, only preview changes without applying

    Returns:
        0 on success, 1 if errors occurred
    """
    # Validate project was initialized
    if not skill_dir.exists():
        print("Error: skill directory not found. Run 'chkcc init' first.")
        return 1

    print("Checking skill files...")

    # Get package and installed files
    package_files = get_package_skill_files()
    installed_files = get_installed_skill_files(skill_dir)

    # Track statistics
    stats = {
        "unchanged": 0,
        "updated": 0,
        "modified": 0,
        "added": 0,
    }

    # Track files to update
    files_to_update: list[tuple[str, bytes]] = []  # (rel_path, content)

    # Check each package file
    for rel_path in sorted(package_files.keys()):
        package_content = package_files[rel_path]
        status = determine_file_status(rel_path, package_content, installed_files)

        if status == "unchanged":
            print(f"  \u2713 {rel_path} (unchanged)")
            stats["unchanged"] += 1

        elif status == "added":
            print(f"  + {rel_path} (added)")
            stats["added"] += 1
            files_to_update.append((rel_path, package_content))

        elif status == "modified":
            if force:
                print(f"  \u2713 {rel_path} (updated, --force)")
                stats["updated"] += 1
                files_to_update.append((rel_path, package_content))
            else:
                print(f"  \u26a0 {rel_path} (modified locally, skipped)")
                stats["modified"] += 1

    print()

    # Apply updates unless dry_run
    if not dry_run and files_to_update:
        for rel_path, content in files_to_update:
            target_path = skill_dir / rel_path
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_bytes(content)

    # Print summary
    action_verb = "Would update" if dry_run else "Updated"
    parts = []
    if stats["updated"] > 0:
        parts.append(f"updated {stats['updated']}")
    if stats["added"] > 0:
        parts.append(f"added {stats['added']}")
    if stats["modified"] > 0:
        parts.append(f"skipped {stats['modified']} modified")

    if parts:
        print(f"{action_verb} {', '.join(parts)}.")
    else:
        print("All files up to date.")

    if stats["modified"] > 0 and not force:
        print("Use --force to overwrite local modifications.")

    if dry_run:
        print("(dry run - no changes made)")

    return 0
