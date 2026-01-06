"""Tests for chkcc init command."""

import json
import pytest
from pathlib import Path

from chkcc import init


def test_create_directory_structure(tmp_path):
    """Init creates active and archive directories."""
    base = tmp_path / "checkpoints"
    created = init.create_directory_structure(base)

    assert (base / "active").is_dir()
    assert (base / "archive").is_dir()
    assert len(created) == 2


def test_create_directory_structure_idempotent(tmp_path):
    """Init skips existing directories."""
    base = tmp_path / "checkpoints"
    (base / "active").mkdir(parents=True)

    created = init.create_directory_structure(base)

    assert len(created) == 1  # Only archive created
    assert "archive" in created[0]


def test_create_index_files(tmp_path):
    """Init creates INDEX.md files."""
    base = tmp_path / "checkpoints"
    (base / "active").mkdir(parents=True)
    (base / "archive").mkdir(parents=True)

    created = init.create_index_files(base)

    assert (base / "active" / "INDEX.md").exists()
    assert (base / "archive" / "INDEX.md").exists()
    assert "Active" in (base / "active" / "INDEX.md").read_text()
    assert "Archived" in (base / "archive" / "INDEX.md").read_text()


def test_install_hooks_fresh(tmp_path):
    """Init creates settings.json with hooks."""
    results = init.install_hooks(tmp_path)

    # Both SessionStart and Stop hooks should be installed
    assert len(results) == 2
    assert results[0][0] is True  # SessionStart installed
    assert results[1][0] is True  # Stop installed

    settings_path = tmp_path / ".claude" / "settings.json"
    assert settings_path.exists()

    settings = json.loads(settings_path.read_text())
    assert "SessionStart" in settings["hooks"]
    assert "Stop" in settings["hooks"]

    # Check matcher-based format for SessionStart
    session_hooks = settings["hooks"]["SessionStart"]
    assert any(
        hook.get("matcher") == "" and
        any("chkcc prime" in h.get("command", "") for h in hook.get("hooks", []))
        for hook in session_hooks
    )


def test_install_hooks_merges_existing(tmp_path):
    """Init merges hooks into existing settings."""
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    settings_path = claude_dir / "settings.json"
    settings_path.write_text(
        json.dumps(
            {"hooks": {"SessionStart": [{"type": "command", "command": "echo hello"}]}}
        )
    )

    results = init.install_hooks(tmp_path)

    assert results[0][0] is True  # SessionStart installed
    settings = json.loads(settings_path.read_text())
    # Both old hook and new matcher-based hook should exist
    assert len(settings["hooks"]["SessionStart"]) == 2


def test_install_hooks_skips_duplicate(tmp_path):
    """Init doesn't add duplicate hooks when matcher-based format already present."""
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    settings_path = claude_dir / "settings.json"
    settings_path.write_text(
        json.dumps(
            {
                "hooks": {
                    "SessionStart": [
                        {
                            "matcher": "",
                            "hooks": [{"type": "command", "command": "chkcc prime 2>/dev/null || true"}]
                        }
                    ],
                    "Stop": [
                        {
                            "matcher": "",
                            "hooks": [{"type": "command", "command": "chkcc stop-hook"}]
                        }
                    ]
                }
            }
        )
    )

    results = init.install_hooks(tmp_path)

    assert results[0][0] is False  # SessionStart already installed
    assert results[1][0] is False  # Stop already installed
    assert "already installed" in results[0][1]
    assert "already installed" in results[1][1]


def test_install_hooks_detects_old_stop_format(tmp_path):
    """Init detects old stop-checkpoint.py format and skips duplicate."""
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    settings_path = claude_dir / "settings.json"
    settings_path.write_text(
        json.dumps(
            {
                "hooks": {
                    "Stop": [
                        {"type": "command", "command": "python3 /path/to/stop-checkpoint.py"}
                    ]
                }
            }
        )
    )

    results = init.install_hooks(tmp_path)

    # SessionStart should be installed (new)
    assert results[0][0] is True
    # Stop should be skipped (old format detected)
    assert results[1][0] is False
    assert "already installed" in results[1][1]
