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


def test_install_hook_fresh(tmp_path):
    """Init creates settings.json with hook."""
    installed, msg = init.install_hook(tmp_path)

    assert installed is True
    settings_path = tmp_path / ".claude" / "settings.json"
    assert settings_path.exists()

    settings = json.loads(settings_path.read_text())
    assert "SessionStart" in settings["hooks"]
    assert any(
        "chkcc prime" in h.get("command", "")
        for h in settings["hooks"]["SessionStart"]
    )


def test_install_hook_merges_existing(tmp_path):
    """Init merges hook into existing settings."""
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    settings_path = claude_dir / "settings.json"
    settings_path.write_text(
        json.dumps(
            {"hooks": {"SessionStart": [{"type": "command", "command": "echo hello"}]}}
        )
    )

    installed, msg = init.install_hook(tmp_path)

    assert installed is True
    settings = json.loads(settings_path.read_text())
    # Both hooks should exist
    assert len(settings["hooks"]["SessionStart"]) == 2


def test_install_hook_skips_duplicate(tmp_path):
    """Init doesn't add duplicate hook."""
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    settings_path = claude_dir / "settings.json"
    settings_path.write_text(
        json.dumps(
            {
                "hooks": {
                    "SessionStart": [
                        {"type": "command", "command": "chkcc prime 2>/dev/null || true"}
                    ]
                }
            }
        )
    )

    installed, msg = init.install_hook(tmp_path)

    assert installed is False
    assert "already installed" in msg
