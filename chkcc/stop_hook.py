"""Stop hook: suggest checkpointing if meaningful work was done.

This module implements a Claude Code stop hook that analyzes the session
transcript to detect if code changes were made and reminds the user to
checkpoint before ending the session.

The hook protocol:
- Reads JSON from stdin with 'transcript_path' and optional 'stop_hook_active'
- Outputs JSON with 'decision' ("block" or "approve") and 'reason'
"""

import json
import os
import sys


def _debug_log(msg: str) -> None:
    """Log debug message if CHKCC_DEBUG environment variable is set."""
    log_path = os.environ.get("CHKCC_DEBUG")
    if log_path:
        with open(log_path, "a") as f:
            f.write(f"{msg}\n")


def analyze_transcript(transcript_path: str) -> tuple[bool, bool]:
    """
    Analyze transcript for work and checkpoint status.

    Args:
        transcript_path: Path to the Claude Code transcript file.

    Returns:
        Tuple of (has_work, already_checkpointed):
        - has_work: True if Write/Edit/NotebookEdit was used on non-checkpoint files
        - already_checkpointed: True if compress skill was invoked after last code change
    """
    last_code_change_idx = -1
    last_checkpoint_idx = -1

    try:
        with open(transcript_path) as f:
            for idx, line in enumerate(f):
                # Check for code changes (exclude checkpoint file operations)
                if any(tool in line for tool in ['"Write"', '"Edit"', '"NotebookEdit"']):
                    if "checkpoints/" not in line:
                        last_code_change_idx = idx

                # Check for compress skill invocation
                if '"Skill"' in line and '"coihuin-compress"' in line:
                    last_checkpoint_idx = idx

    except (OSError, IOError) as e:
        _debug_log(f"Error reading transcript: {e}")
        return False, False

    has_work = last_code_change_idx >= 0
    already_checkpointed = (
        last_checkpoint_idx > last_code_change_idx and last_code_change_idx >= 0
    )

    return has_work, already_checkpointed


def run_hook(input_data: dict) -> dict:
    """
    Process stop hook request.

    Args:
        input_data: Dictionary from Claude Code hook protocol containing
                    'transcript_path' and optional 'stop_hook_active'.

    Returns:
        Dictionary with 'decision' ("block" or "approve") and 'reason'.
    """
    _debug_log("=== Stop hook invoked ===")
    _debug_log(f"Input data keys: {list(input_data.keys())}")

    # Prevent infinite loops
    if input_data.get("stop_hook_active"):
        _debug_log("stop_hook_active=True, approving")
        return {"decision": "approve", "reason": "Already in stop hook."}

    transcript_path = input_data.get("transcript_path", "")
    _debug_log(f"transcript_path: {transcript_path}")

    if not transcript_path:
        _debug_log("No transcript path, approving")
        return {"decision": "approve", "reason": "No transcript."}

    has_work, already_checkpointed = analyze_transcript(transcript_path)
    _debug_log(f"has_work={has_work}, already_checkpointed={already_checkpointed}")

    if has_work and not already_checkpointed:
        _debug_log("Work detected, not yet checkpointed, blocking")
        return {
            "decision": "block",
            "reason": "Use compress skill to checkpoint before ending.",
        }

    reason = "Already checkpointed." if already_checkpointed else "No checkpoint needed."
    _debug_log(f"Approving: {reason}")
    return {"decision": "approve", "reason": reason}


def main() -> int:
    """Main entry point for CLI invocation. Returns exit code."""
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        _debug_log(f"Invalid JSON input: {e}")
        print(json.dumps({"decision": "approve", "reason": "Invalid input."}))
        return 1

    result = run_hook(input_data)
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
