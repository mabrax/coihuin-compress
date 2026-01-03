"""Tests for chkcc prime command."""

import pytest
from argparse import Namespace
from pathlib import Path

from chkcc.cli import cmd_prime


@pytest.fixture
def checkpoint_dir(tmp_path):
    """Create checkpoint directory structure with a current checkpoint."""
    active = tmp_path / "active"
    active.mkdir()

    # Create a checkpoint file
    checkpoint = active / "chk-test.md"
    checkpoint.write_text("""---
checkpoint: chk-test
created: 2026-01-03T10:00:00Z
status: current
---

## Problem
Test problem.
""")
    return tmp_path


@pytest.fixture
def empty_checkpoint_dir(tmp_path):
    """Create checkpoint directory with no current checkpoint."""
    active = tmp_path / "active"
    active.mkdir()
    return tmp_path


def test_prime_with_current_checkpoint(checkpoint_dir, capsys):
    """Prime outputs checkpoint content when current exists."""
    args = Namespace(dir=str(checkpoint_dir), header=False)
    exit_code = cmd_prime(args)

    assert exit_code == 0
    captured = capsys.readouterr()
    assert "checkpoint: chk-test" in captured.out
    assert "Test problem." in captured.out


def test_prime_with_header(checkpoint_dir, capsys):
    """Prime prepends header when --header flag used."""
    args = Namespace(dir=str(checkpoint_dir), header=True)
    exit_code = cmd_prime(args)

    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("# Context Recovery: chk-test")


def test_prime_no_current_silent_exit(empty_checkpoint_dir, capsys):
    """Prime exits silently when no current checkpoint."""
    args = Namespace(dir=str(empty_checkpoint_dir), header=False)
    exit_code = cmd_prime(args)

    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out == ""


def test_prime_missing_dir_silent_exit(tmp_path, capsys):
    """Prime exits silently when checkpoints dir doesn't exist."""
    args = Namespace(dir=str(tmp_path / "nonexistent"), header=False)
    exit_code = cmd_prime(args)

    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out == ""
