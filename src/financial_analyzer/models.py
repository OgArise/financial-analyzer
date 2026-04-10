"""Data models used across loading, analysis, and reporting."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import Any, cast


@dataclass(frozen=True, slots=True)
class Transaction:
    """Represent one financial transaction from the source CSV."""

    date: str
    account_id: str
    description: str
    amount: Decimal
    transaction_type: str


@dataclass(frozen=True, slots=True)
class AccountSummary:
    """Represent total credits and debits for one account."""

    account_id: str
    total_credits: Decimal
    total_debits: Decimal


@dataclass(frozen=True, slots=True)
class ExcessDebitFlag:
    """Represent an account whose debits breached the control threshold."""

    account_id: str
    total_credits: Decimal
    total_debits: Decimal
    excess_ratio: Decimal | None
    reason: str


@dataclass(frozen=True, slots=True)
class TopTransaction:
    """Represent a ranked high-value transaction for quick review."""

    rank: int
    transaction: Transaction


@dataclass(frozen=True, slots=True)
class ReportData:
    """Represent the full report in a structured, API-friendly form."""

    account_summaries: list[AccountSummary]
    excess_debit_flags: list[ExcessDebitFlag]
    top_transactions: list[TopTransaction]

    def to_json(self) -> dict[str, Any]:
        """Return the report as a JSON-serializable dictionary."""

        return cast(dict[str, Any], _serialize_value(asdict(self)))



def _serialize_value(value: Any) -> Any:
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, list):
        return [_serialize_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _serialize_value(item) for key, item in value.items()}
    return value
