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

from chkcc import archive, scaffold, tree, validate


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
        archived_path = archive.archive_checkpoint(checkpoint_path)
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
        archive_parser.set_defaults(func=cmd_archive)

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
