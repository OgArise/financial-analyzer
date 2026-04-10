"""Tests for the command-line entry point."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from financial_analyzer.cli import main


def test_cli_text_output(sample_csv_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Verify the CLI returns a text report for valid input."""

    exit_code = main([str(sample_csv_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "FINANCIAL TRANSACTION SUMMARY REPORT" in captured.out


def test_cli_json_output(sample_csv_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Verify the CLI returns JSON output when requested."""

    exit_code = main([str(sample_csv_path), "--json"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert "account_summaries" in payload
