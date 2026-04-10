"""CSV loading, validation, and parsing logic."""

from __future__ import annotations

import csv
import logging
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

from .models import Transaction

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {"date", "account_id", "description", "amount", "transaction_type"}
VALID_TRANSACTION_TYPES = {"credit", "debit"}


def parse_date(value: str) -> str:
    """Validate a date string using the expected YYYY-MM-DD format."""

    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(f"Invalid date format: {value!r}. Expected YYYY-MM-DD.") from exc
    return value


def parse_amount(value: str) -> Decimal:
    """Convert a raw string amount into Decimal for accurate financial arithmetic."""

    try:
        return Decimal(value)
    except (InvalidOperation, TypeError) as exc:
        raise ValueError(f"Invalid amount: {value!r}") from exc


def normalize_transaction_type(value: str) -> str:
    """Normalize and validate a transaction type as either credit or debit."""

    cleaned = value.strip().lower()
    if cleaned not in VALID_TRANSACTION_TYPES:
        raise ValueError(f"Invalid transaction_type: {value!r}. Expected 'credit' or 'debit'.")
    return cleaned


def load_transactions(file_path: str | Path) -> list[Transaction]:
    """Load transactions from CSV after validating columns and row-level quality rules."""

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    logger.info("Loading transactions from %s", path)

    transactions: list[Transaction] = []
    with path.open("r", newline="", encoding="utf-8-sig") as file_obj:
        reader = csv.DictReader(file_obj)
        if reader.fieldnames is None:
            raise ValueError("CSV file is empty or missing a header row.")

        missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing_columns:
            raise ValueError(f"CSV is missing required columns: {sorted(missing_columns)}")

        for line_number, row in enumerate(reader, start=2):
            transactions.append(_parse_row(row, line_number))

    logger.info("Loaded %d transactions", len(transactions))
    return transactions


def _parse_row(row: dict[str, str | None], line_number: int) -> Transaction:
    try:
        transaction = Transaction(
            date=parse_date((row.get("date") or "").strip()),
            account_id=(row.get("account_id") or "").strip(),
            description=(row.get("description") or "").strip(),
            amount=parse_amount((row.get("amount") or "").strip()),
            transaction_type=normalize_transaction_type(
                (row.get("transaction_type") or "").strip()
            ),
        )
    except ValueError as exc:
        raise ValueError(f"Row {line_number}: {exc}") from exc

    if not transaction.account_id:
        raise ValueError(f"Row {line_number}: account_id is blank")
    if not transaction.description:
        raise ValueError(f"Row {line_number}: description is blank")
    if transaction.amount < 0:
        raise ValueError(
            f"Row {line_number}: amount must be non-negative; "
            "use transaction_type to indicate direction"
        )

    return transaction
