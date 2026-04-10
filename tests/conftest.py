"""Shared pytest fixtures for financial_analyzer tests."""

from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path

import pytest

from financial_analyzer.models import Transaction


@pytest.fixture()
def sample_transactions() -> list[Transaction]:
    """Return a small in-memory transaction set for analysis and reporting tests."""

    return [
        Transaction("2026-04-01", "ACC1001", "Client payment", Decimal("2500.00"), "credit"),
        Transaction("2026-04-01", "ACC1001", "Office rent", Decimal("1200.00"), "debit"),
        Transaction("2026-04-02", "ACC1002", "Loan disbursement", Decimal("5000.00"), "credit"),
        Transaction("2026-04-02", "ACC1002", "Equipment purchase", Decimal("7000.00"), "debit"),
        Transaction("2026-04-03", "ACC1003", "Subscription income", Decimal("800.00"), "credit"),
        Transaction("2026-04-03", "ACC1003", "Software expense", Decimal("950.00"), "debit"),
    ]


@pytest.fixture()
def sample_csv_path(tmp_path: Path) -> Path:
    """Write a valid sample CSV file and return its path."""

    file_path = tmp_path / "sample_transactions.csv"
    rows = [
        ["2026-04-01", "ACC1001", "Client payment", "2500.00", "credit"],
        ["2026-04-01", "ACC1001", "Office rent", "1200.00", "debit"],
        ["2026-04-02", "ACC1002", "Loan disbursement", "5000.00", "credit"],
    ]

    with file_path.open("w", newline="", encoding="utf-8") as file_obj:
        writer = csv.writer(file_obj)
        writer.writerow(["date", "account_id", "description", "amount", "transaction_type"])
        writer.writerows(rows)

    return file_path
