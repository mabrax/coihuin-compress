#!/usr/bin/env python3
"""Stop hook: suggest checkpointing if meaningful work was done."""

import json
import sys
import os

# Debug log (set to None to disable)
DEBUG_LOG = "/tmp/stop-checkpoint-debug.log"

def log(msg: str):
    if DEBUG_LOG:
        with open(DEBUG_LOG, "a") as f:
            f.write(f"{msg}\n")

def analyze_transcript(transcript_path: str) -> tuple[bool, bool]:
    """
    Analyze transcript for work and checkpoint status.

    Returns:
        (has_work, already_checkpointed):
        - has_work: True if Write/Edit/NotebookEdit was used
        - already_checkpointed: True if compress skill was used after last code change
    """
    last_code_change_idx = -1
    last_checkpoint_idx = -1

    try:
        with open(transcript_path) as f:
            for idx, line in enumerate(f):
                content = line
                # Check for code changes (exclude checkpoint file operations)
                if any(tool in content for tool in ['"Write"', '"Edit"', '"NotebookEdit"']):
                    # Skip if this is a checkpoint file operation
                    if 'checkpoints/' not in content:
                        last_code_change_idx = idx
                # Check for compress skill invocation (Skill tool with coihuin-compress)
                # Must match actual skill invocation, not just path containing the name
                if '"Skill"' in content and '"coihuin-compress"' in content:
                    last_checkpoint_idx = idx
    except Exception as e:
        log(f"Error reading transcript: {e}")
        return False, False

    has_work = last_code_change_idx >= 0
    # Already checkpointed if compress skill was used after the last code change
    already_checkpointed = last_checkpoint_idx > last_code_change_idx and last_code_change_idx >= 0

    return has_work, already_checkpointed

def main():
    log("=== Stop hook invoked ===")
    data = json.load(sys.stdin)
    log(f"Input data keys: {list(data.keys())}")

    # Prevent infinite loops
    if data.get("stop_hook_active"):
        log("stop_hook_active=True, approving")
        print(json.dumps({"decision": "approve", "reason": "Already in stop hook."}))
        return

    transcript_path = data.get("transcript_path", "")
    log(f"transcript_path: {transcript_path}")

    if not transcript_path:
        log("No transcript path, approving")
        print(json.dumps({"decision": "approve", "reason": "No transcript."}))
        return

    has_work, already_checkpointed = analyze_transcript(transcript_path)
    log(f"has_work={has_work}, already_checkpointed={already_checkpointed}")

    if has_work and not already_checkpointed:
        log("Work detected, not yet checkpointed, blocking")
        print(json.dumps({
            "decision": "block",
            "reason": "Use compress skill to checkpoint before ending."
        }))
    else:
        reason = "Already checkpointed." if already_checkpointed else "No checkpoint needed."
        log(f"Approving: {reason}")
        print(json.dumps({
            "decision": "approve",
            "reason": reason
        }))

if __name__ == "__main__":
    main()
