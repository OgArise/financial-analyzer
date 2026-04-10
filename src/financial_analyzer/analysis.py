"""Analytical routines for financial transaction screening."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from decimal import Decimal

from .models import AccountSummary, ExcessDebitFlag, TopTransaction, Transaction


def summarize_by_account(transactions: Iterable[Transaction]) -> list[AccountSummary]:
    """Aggregate credits and debits per account for monitoring and reconciliation."""

    totals: dict[str, dict[str, Decimal]] = defaultdict(
        lambda: {"credit": Decimal("0"), "debit": Decimal("0")}
    )

    for transaction in transactions:
        totals[transaction.account_id][transaction.transaction_type] += transaction.amount

    return [
        AccountSummary(
            account_id=account_id,
            total_credits=amounts["credit"],
            total_debits=amounts["debit"],
        )
        for account_id, amounts in sorted(totals.items())
    ]


def find_excess_debits(
    account_summaries: Iterable[AccountSummary], threshold: Decimal = Decimal("0.20")
) -> list[ExcessDebitFlag]:
    """Flag accounts where debits exceed credits by more than 20%.

    This serves as a simple early-warning control for unusual cash outflow pressure.
    """

    flagged_accounts: list[ExcessDebitFlag] = []

    for summary in account_summaries:
        credits = summary.total_credits
        debits = summary.total_debits

        if credits == 0:
            if debits > 0:
                flagged_accounts.append(
                    ExcessDebitFlag(
                        account_id=summary.account_id,
                        total_credits=credits,
                        total_debits=debits,
                        excess_ratio=None,
                        reason="Debits exist with no offsetting credits.",
                    )
                )
            continue

        excess_ratio = (debits - credits) / credits
        if excess_ratio > threshold:
            flagged_accounts.append(
                ExcessDebitFlag(
                    account_id=summary.account_id,
                    total_credits=credits,
                    total_debits=debits,
                    excess_ratio=excess_ratio,
                    reason=f"Debits exceed credits by more than {threshold * Decimal('100'):.0f}%.",
                )
            )

    return flagged_accounts


def get_top_transactions(
    transactions: Iterable[Transaction], top_n: int = 3
) -> list[TopTransaction]:
    """Return the largest individual transactions because high-value items deserve first review."""

    ranked = sorted(transactions, key=lambda item: item.amount, reverse=True)[:top_n]
    return [TopTransaction(rank=index, transaction=tx) for index, tx in enumerate(ranked, start=1)]
