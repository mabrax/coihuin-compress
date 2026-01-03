"""Tests for chkcc doctor command."""

import json
import pytest
from pathlib import Path

from chkcc import doctor


def test_check_directory_exists(tmp_path):
    """Doctor reports existing directory as passing."""
    test_dir = tmp_path / "test"
    test_dir.mkdir()

    passed, msg = doctor.check_directory(test_dir)

    assert passed is True
    assert "✓" in msg


def test_check_directory_missing(tmp_path):
    """Doctor reports missing directory as failing."""
    passed, msg = doctor.check_directory(tmp_path / "missing")

    assert passed is False
    assert "✗" in msg
    assert "missing" in msg


def test_check_hook_installed(tmp_path):
    """Doctor detects installed hook."""
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    (claude_dir / "settings.json").write_text(
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

    passed, msg = doctor.check_hook(tmp_path)

    assert passed is True
    assert "✓" in msg


def test_check_hook_missing_file(tmp_path):
    """Doctor reports missing settings.json."""
    passed, msg = doctor.check_hook(tmp_path)

    assert passed is False
    assert "missing" in msg


def test_check_hook_not_installed(tmp_path):
    """Doctor reports when hook not in settings."""
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    (claude_dir / "settings.json").write_text(json.dumps({"hooks": {}}))

    passed, msg = doctor.check_hook(tmp_path)

    assert passed is False
    assert "not found" in msg


def test_cmd_doctor_healthy(tmp_path, capsys):
    """Doctor returns 0 when all checks pass."""
    # Setup complete structure
    base = tmp_path / "checkpoints"
    (base / "active").mkdir(parents=True)
    (base / "archive").mkdir(parents=True)
    (base / "active" / "INDEX.md").write_text("# Index")

    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    (claude_dir / "settings.json").write_text(
        json.dumps(
            {"hooks": {"SessionStart": [{"command": "chkcc prime 2>/dev/null || true"}]}}
        )
    )

    exit_code = doctor.cmd_doctor(base, tmp_path)

    assert exit_code == 0
    captured = capsys.readouterr()
    assert "All checks passed" in captured.out


def test_cmd_doctor_unhealthy(tmp_path, capsys):
    """Doctor returns 1 when checks fail."""
    base = tmp_path / "checkpoints"

    exit_code = doctor.cmd_doctor(base, tmp_path)

    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Issues found" in captured.out


def test_cmd_doctor_fix_creates_structure(tmp_path, capsys):
    """Doctor --fix creates missing directories and files."""
    base = tmp_path / "checkpoints"

    exit_code = doctor.cmd_doctor(base, tmp_path, fix=True)

    assert exit_code == 0
    assert (base / "active").is_dir()
    assert (base / "archive").is_dir()
    assert (base / "active" / "INDEX.md").exists()
    assert (base / "archive" / "INDEX.md").exists()
    captured = capsys.readouterr()
    assert "Fixing issues" in captured.out


def test_cmd_doctor_fix_installs_hook(tmp_path, capsys):
    """Doctor --fix installs missing hook."""
    base = tmp_path / "checkpoints"

    exit_code = doctor.cmd_doctor(base, tmp_path, fix=True)

    assert exit_code == 0
    settings_path = tmp_path / ".claude" / "settings.json"
    assert settings_path.exists()
    settings = json.loads(settings_path.read_text())
    assert "SessionStart" in settings["hooks"]
    captured = capsys.readouterr()
    assert "Installed hook" in captured.out


def test_cmd_doctor_fix_then_healthy(tmp_path, capsys):
    """After --fix, a second doctor run shows healthy."""
    base = tmp_path / "checkpoints"

    # First run with fix
    doctor.cmd_doctor(base, tmp_path, fix=True)
    capsys.readouterr()  # Clear output

    # Second run without fix
    exit_code = doctor.cmd_doctor(base, tmp_path, fix=False)

    assert exit_code == 0
    captured = capsys.readouterr()
    assert "All checks passed" in captured.out
