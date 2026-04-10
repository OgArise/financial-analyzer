"""Tests for CSV loading and validation."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from financial_analyzer.loader import load_transactions


def test_load_transactions_valid_csv(sample_csv_path: Path) -> None:
    """Verify valid CSV input loads into transaction objects."""

    transactions = load_transactions(sample_csv_path)

    assert len(transactions) == 3
    assert transactions[0].account_id == "ACC1001"
    assert transactions[1].transaction_type == "debit"


def test_load_transactions_rejects_bad_date(tmp_path: Path) -> None:
    """Verify bad date values are rejected with a helpful validation error."""

    file_path = tmp_path / "bad_date.csv"

    with file_path.open("w", newline="", encoding="utf-8") as file_obj:
        writer = csv.writer(file_obj)
        writer.writerow(["date", "account_id", "description", "amount", "transaction_type"])
        writer.writerow(["2026/04/01", "ACC1001", "Client payment", "2500.00", "credit"])

    with pytest.raises(ValueError, match="Invalid date format"):
        load_transactions(file_path)


def test_load_transactions_rejects_missing_column(tmp_path: Path) -> None:
    """Verify missing required columns are caught before row processing starts."""

    file_path = tmp_path / "missing_column.csv"

    with file_path.open("w", newline="", encoding="utf-8") as file_obj:
        writer = csv.writer(file_obj)
        writer.writerow(["date", "account_id", "description", "amount"])
        writer.writerow(["2026-04-01", "ACC1001", "Client payment", "2500.00"])

    with pytest.raises(ValueError, match="missing required columns"):
        load_transactions(file_path)
