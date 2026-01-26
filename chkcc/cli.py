"""
CLI entry point for the chkcc checkpoint compression tool.

Provides command-line interface for managing checkpoint lifecycle:
- tree: visualize checkpoint lineage
- validate: check checkpoint format
- scaffold: create new checkpoints or deltas
- archive: move completed checkpoints to archive
"""

import argparse
import sys
from pathlib import Path

from chkcc import archive, current, doctor, init, scaffold, status, tree, update, validate


def cmd_tree(args: argparse.Namespace) -> int:
    """Handle 'tree' subcommand."""
    try:
        base_dir = Path(args.dir).expanduser().resolve()
        lines = tree.show_tree(base_dir, args.status)
        for line in lines:
            print(line)
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except NotADirectoryError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_status(args: argparse.Namespace) -> int:
    """Handle 'status' subcommand."""
    try:
        base_dir = Path(args.dir).expanduser().resolve()
        status.cmd_status(base_dir, args.all)
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except NotADirectoryError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_validate(args: argparse.Namespace) -> int:
    """Handle 'validate' subcommand."""
    try:
        file_path = Path(args.file).expanduser().resolve()
        result = validate.validate_file(file_path)

        # Determine file type for display
        if file_path.name == "INDEX.md":
            file_type = "INDEX"
        else:
            file_type = "checkpoint"

        validate.print_result(result, file_type, str(file_path))

        # Exit with status 0 if valid, 1 if invalid
        return 0 if result.valid else 1
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_scaffold_checkpoint(args: argparse.Namespace) -> int:
    """Handle 'scaffold checkpoint' subcommand."""
    try:
        output_dir = Path(args.dir).expanduser().resolve()
        created_path = scaffold.scaffold_checkpoint(
            args.name,
            parent=args.parent,
            anchor=args.anchor,
            output_dir=output_dir,
            set_current=args.current,
        )
        print(f"Created checkpoint: {created_path}")
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except FileExistsError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_scaffold_delta(args: argparse.Namespace) -> int:
    """Handle 'scaffold delta' subcommand."""
    try:
        checkpoint_path = Path(args.file).expanduser().resolve()
        scaffold.scaffold_delta(checkpoint_path)
        print(f"Added delta to: {checkpoint_path}")
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_archive(args: argparse.Namespace) -> int:
    """Handle 'archive' subcommand."""
    try:
        checkpoint_path = Path(args.file).expanduser().resolve()
        archived_path = archive.archive_checkpoint(checkpoint_path, force=args.force)
        print(f"Archived checkpoint: {archived_path}")
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except (PermissionError, OSError) as e:
        print(f"Error: Unable to archive checkpoint: {e}", file=sys.stderr)
        return 1


def cmd_current(args: argparse.Namespace) -> int:
    """Handle 'current' subcommand."""
    try:
        base_dir = Path(args.dir).expanduser().resolve()

        # Resolve checkpoint path if provided
        checkpoint_path = None
        if args.checkpoint:
            # If just a filename, resolve relative to active/ directory
            checkpoint_input = Path(args.checkpoint)
            if not checkpoint_input.is_absolute():
                # Check if it's just a filename or a relative path
                if checkpoint_input.parent == Path("."):
                    # Just a filename - look in active/ directory
                    checkpoint_path = base_dir / "active" / checkpoint_input
                    # Add .md extension if not present
                    if not checkpoint_path.suffix:
                        checkpoint_path = checkpoint_path.with_suffix(".md")
                else:
                    # Relative path - resolve from current directory
                    checkpoint_path = checkpoint_input.expanduser().resolve()
            else:
                checkpoint_path = checkpoint_input.expanduser().resolve()

        current.cmd_current(base_dir, checkpoint_path, args.clear)
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except (PermissionError, OSError) as e:
        print(f"Error: Unable to update checkpoint: {e}", file=sys.stderr)
        return 1


def cmd_prime(args: argparse.Namespace) -> int:
    """Handle 'prime' subcommand."""
    base_dir = Path(args.dir).expanduser().resolve()

    checkpoint = current.get_current(base_dir)
    if checkpoint is None:
        return 0  # Silent exit, no error

    content = checkpoint.path.read_text(encoding='utf-8')
    print(content, end='')  # Avoid extra newline if content already ends with one
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    """Handle 'init' subcommand."""
    base_dir = Path(args.dir).expanduser().resolve()
    project_root = Path(args.project).expanduser().resolve()
    init.cmd_init(base_dir, project_root)
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    """Handle 'doctor' subcommand."""
    base_dir = Path(args.dir).expanduser().resolve()
    project_root = Path(args.project).expanduser().resolve()
    return doctor.cmd_doctor(base_dir, project_root, fix=args.fix)


def cmd_update(args: argparse.Namespace) -> int:
    """Handle 'update' subcommand."""
    skill_dir = Path(args.project).expanduser().resolve() / ".claude" / "skills" / "coihuin-compress"
    return update.cmd_update(skill_dir, force=args.force, dry_run=args.dry_run)


def main() -> None:
    """Main entry point for the CLI."""
    try:
        parser = argparse.ArgumentParser(
            prog="chkcc",
            description="Checkpoint compression CLI for managing work sessions",
        )

        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # tree command
        tree_parser = subparsers.add_parser(
            "tree",
            help="Show checkpoint lineage tree",
        )
        tree_parser.add_argument(
            "dir",
            nargs="?",
            default="./checkpoints",
            help="Checkpoints directory (default: ./checkpoints)",
        )
        tree_parser.add_argument(
            "-s", "--status",
            choices=["active", "archive", "all"],
            default="all",
            help="Filter by status (default: all)",
        )
        tree_parser.set_defaults(func=cmd_tree)

        # status command
        status_parser = subparsers.add_parser(
            "status",
            help="Show checkpoint status summaries with context and next actions",
        )
        status_parser.add_argument(
            "dir",
            nargs="?",
            default="./checkpoints",
            help="Checkpoints directory (default: ./checkpoints)",
        )
        status_parser.add_argument(
            "-a", "--all",
            action="store_true",
            help="Include archived checkpoints",
        )
        status_parser.set_defaults(func=cmd_status)

        # validate command
        validate_parser = subparsers.add_parser(
            "validate",
            help="Validate checkpoint or INDEX file format",
        )
        validate_parser.add_argument(
            "file",
            help="Path to checkpoint or INDEX file",
        )
        validate_parser.set_defaults(func=cmd_validate)

        # scaffold command
        scaffold_parser = subparsers.add_parser(
            "scaffold",
            help="Create checkpoint or delta templates",
        )
        scaffold_subparsers = scaffold_parser.add_subparsers(
            dest="scaffold_command",
            help="Scaffold subcommands",
        )

        # scaffold checkpoint command
        scaffold_checkpoint_parser = scaffold_subparsers.add_parser(
            "checkpoint",
            help="Create new checkpoint",
        )
        scaffold_checkpoint_parser.add_argument(
            "name",
            help="Checkpoint name (will be prefixed with 'chk-' if needed; no path separators)",
        )
        scaffold_checkpoint_parser.add_argument(
            "--parent",
            default=None,
            help="Parent checkpoint ID for branching",
        )
        scaffold_checkpoint_parser.add_argument(
            "--anchor",
            default=None,
            help="Anchor reference (branch, commit, PR, etc.)",
        )
        scaffold_checkpoint_parser.add_argument(
            "--current",
            action="store_true",
            help="Set this checkpoint as current (status: current)",
        )
        scaffold_checkpoint_parser.add_argument(
            "--dir",
            default="./checkpoints/active",
            help="Output directory (default: ./checkpoints/active)",
        )
        scaffold_checkpoint_parser.set_defaults(func=cmd_scaffold_checkpoint)

        # scaffold delta command
        scaffold_delta_parser = scaffold_subparsers.add_parser(
            "delta",
            help="Append delta to existing checkpoint",
        )
        scaffold_delta_parser.add_argument(
            "file",
            help="Path to checkpoint file",
        )
        scaffold_delta_parser.set_defaults(func=cmd_scaffold_delta)

        # archive command
        archive_parser = subparsers.add_parser(
            "archive",
            help="Archive completed checkpoint",
        )
        archive_parser.add_argument(
            "file",
            help="Path to checkpoint file",
        )
        archive_parser.add_argument(
            "-f", "--force",
            action="store_true",
            help="Force archive even if checkpoint has active children",
        )
        archive_parser.set_defaults(func=cmd_archive)

        # current command
        current_parser = subparsers.add_parser(
            "current",
            help="Show or set the current checkpoint",
        )
        current_parser.add_argument(
            "checkpoint",
            nargs="?",
            default=None,
            help="Checkpoint to set as current (filename or path)",
        )
        current_parser.add_argument(
            "-c", "--clear",
            action="store_true",
            help="Clear current checkpoint marker",
        )
        current_parser.add_argument(
            "--dir",
            default="./checkpoints",
            help="Checkpoints directory (default: ./checkpoints)",
        )
        current_parser.set_defaults(func=cmd_current)

        # prime command
        prime_parser = subparsers.add_parser(
            "prime",
            help="Dump current checkpoint content to stdout",
        )
        prime_parser.add_argument(
            "--dir",
            default="./checkpoints",
            help="Checkpoints directory (default: ./checkpoints)",
        )
        prime_parser.set_defaults(func=cmd_prime)

        # init command
        init_parser = subparsers.add_parser(
            "init",
            help="Initialize coihuin-compress in current project",
        )
        init_parser.add_argument(
            "--dir",
            default="./checkpoints",
            help="Checkpoints directory (default: ./checkpoints)",
        )
        init_parser.add_argument(
            "--project",
            default=".",
            help="Project root directory (default: current directory)",
        )
        init_parser.set_defaults(func=cmd_init)

        # doctor command
        doctor_parser = subparsers.add_parser(
            "doctor",
            help="Check coihuin-compress setup health",
        )
        doctor_parser.add_argument(
            "--dir",
            default="./checkpoints",
            help="Checkpoints directory (default: ./checkpoints)",
        )
        doctor_parser.add_argument(
            "--project",
            default=".",
            help="Project root directory (default: current directory)",
        )
        doctor_parser.add_argument(
            "--fix",
            action="store_true",
            help="Automatically fix any issues found",
        )
        doctor_parser.set_defaults(func=cmd_doctor)

        # update command
        update_parser = subparsers.add_parser(
            "update",
            help="Update skill files from package",
        )
        update_parser.add_argument(
            "--project",
            default=".",
            help="Project root directory (default: current directory)",
        )
        update_parser.add_argument(
            "-f", "--force",
            action="store_true",
            help="Overwrite locally modified files",
        )
        update_parser.add_argument(
            "-n", "--dry-run",
            action="store_true",
            help="Show what would change without writing",
        )
        update_parser.set_defaults(func=cmd_update)

        # Parse arguments
        args = parser.parse_args()

        # If no command specified, print help
        if not hasattr(args, "func"):
            parser.print_help()
            sys.exit(0)

        # Handle empty scaffold subcommand
        if hasattr(args, "command") and args.command == "scaffold" and not hasattr(args, "func"):
            scaffold_parser.print_help()
            sys.exit(1)

        # Execute the command function
        exit_code = args.func(args)
        sys.exit(exit_code)

    except KeyboardInterrupt:
        print("\nOperation cancelled.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
