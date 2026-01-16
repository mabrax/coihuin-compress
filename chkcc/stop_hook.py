"""Stop hook: spawn headless Claude to summarize session.

This module implements a Claude Code stop hook that spawns a headless
Claude instance to run /summary on the session. Fire-and-forget approach:
the hook approves immediately while the summary runs in background.

The hook protocol:
- Reads JSON from stdin with 'session_id', 'transcript_path', etc.
- Outputs JSON with 'decision' ("approve") - never blocks
- Spawns: claude -p "/summary" --resume <session_id> --allowedTools "Read,Write,Skill"
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def _debug_log(msg: str) -> None:
    """Log debug message if CHKCC_DEBUG environment variable is set."""
    log_path = os.environ.get("CHKCC_DEBUG")
    if log_path:
        with open(log_path, "a") as f:
            f.write(f"{msg}\n")


def _find_project_root(transcript_path: str) -> Path | None:
    """
    Find project root from transcript path.

    Transcript paths look like: ~/.claude/projects/<hash>/transcript.jsonl
    We need to find the actual project directory.
    """
    # The transcript is in ~/.claude/projects/<hash>/
    # The hash directory contains a .project file with the actual path
    transcript = Path(transcript_path).expanduser()
    if not transcript.exists():
        return None

    project_meta = transcript.parent / ".project"
    if project_meta.exists():
        try:
            # .project file contains the actual project path
            project_path = project_meta.read_text().strip()
            return Path(project_path)
        except (OSError, IOError):
            pass

    # Fallback: use current working directory
    return Path.cwd()


def _ensure_summaries_dir(project_root: Path) -> Path:
    """Ensure checkpoints/summaries directory exists."""
    summaries_dir = project_root / "checkpoints" / "summaries"
    summaries_dir.mkdir(parents=True, exist_ok=True)
    return summaries_dir


def _update_state(summaries_dir: Path, session_id: str) -> None:
    """Update state.json with new summary entry."""
    state_file = summaries_dir / "state.json"

    # Load existing state or create new
    state = {"summaries": []}
    if state_file.exists():
        try:
            state = json.loads(state_file.read_text())
        except (json.JSONDecodeError, OSError):
            pass

    # Add new entry
    entry = {
        "session_id": session_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
    }
    state["summaries"].append(entry)

    # Write back
    state_file.write_text(json.dumps(state, indent=2) + "\n")


def _spawn_summary(session_id: str, project_root: Path) -> None:
    """Spawn headless Claude to run /summary in background."""
    summaries_dir = _ensure_summaries_dir(project_root)

    # Update state before spawning
    _update_state(summaries_dir, session_id)

    # Output file for this summary
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    output_file = summaries_dir / f"summary-{timestamp}.md"

    # Spawn headless Claude in background
    # Use --resume with explicit session ID for deterministic behavior
    cmd = (
        f'claude -p "/summary" --resume "{session_id}" --allowedTools "Read,Write,Skill" '
        f'> "{output_file}" 2>&1 &'
    )

    _debug_log(f"Spawning: {cmd}")

    subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,  # Detach from parent
        cwd=str(project_root),
    )


def run_hook(input_data: dict) -> dict:
    """
    Process stop hook request.

    Args:
        input_data: Dictionary from Claude Code hook protocol containing
                    'session_id', 'transcript_path', etc.

    Returns:
        Dictionary with 'decision' ("approve") - always approves.
    """
    _debug_log("=== Stop hook invoked ===")
    _debug_log(f"Input data: {json.dumps(input_data, indent=2)}")

    # Loop prevention: don't spawn if we're already in a stop hook
    if input_data.get("stop_hook_active"):
        _debug_log("Stop hook already active, skipping")
        return {"decision": "approve", "reason": "Stop hook already active."}

    session_id = input_data.get("session_id", "unknown")
    transcript_path = input_data.get("transcript_path", "")

    # Find project root
    project_root = None
    if transcript_path:
        project_root = _find_project_root(transcript_path)

    if project_root is None:
        project_root = Path.cwd()

    _debug_log(f"Project root: {project_root}")

    # Check if checkpoints directory exists (coihuin-compress is set up)
    checkpoints_dir = project_root / "checkpoints"
    if not checkpoints_dir.exists():
        _debug_log("No checkpoints directory, skipping summary")
        return {"decision": "approve", "reason": "No checkpoints directory."}

    # Spawn summary in background
    try:
        _spawn_summary(session_id, project_root)
        _debug_log("Summary spawned successfully")
    except Exception as e:
        _debug_log(f"Failed to spawn summary: {e}")

    # Always approve - fire and forget
    return {"decision": "approve", "reason": "Summary spawned."}


def main() -> int:
    """Main entry point for CLI invocation. Returns exit code."""
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        _debug_log(f"Invalid JSON input: {e}")
        print(json.dumps({"decision": "approve", "reason": "Invalid input."}))
        return 0

    result = run_hook(input_data)
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
