"""Report assembly and formatting utilities."""

from __future__ import annotations

from collections.abc import Iterable
from decimal import Decimal

from .analysis import find_excess_debits, get_top_transactions, summarize_by_account
from .models import ReportData, Transaction


def build_report(transactions: Iterable[Transaction]) -> ReportData:
    """Build a structured report object from a collection of validated transactions."""

    transaction_list = list(transactions)
    account_summaries = summarize_by_account(transaction_list)
    return ReportData(
        account_summaries=account_summaries,
        excess_debit_flags=find_excess_debits(account_summaries),
        top_transactions=get_top_transactions(transaction_list),
    )


def format_report(report: ReportData) -> str:
    """Return the full report as a plain-text string for console output or downstream delivery."""

    lines: list[str] = [
        "FINANCIAL TRANSACTION SUMMARY REPORT",
        "=" * 40,
        "",
        "Total credits and debits per account",
        "-" * 40,
    ]

    for summary in report.account_summaries:
        lines.append(
            f"{summary.account_id:<10} Credits: {_format_money(summary.total_credits):>12}   "
            f"Debits: {_format_money(summary.total_debits):>12}"
        )

    lines.extend(
        [
            "",
            "Accounts where debits exceed credits by more than 20%",
            "-" * 40,
        ]
    )

    if not report.excess_debit_flags:
        lines.append("None")
    else:
        for flag in report.excess_debit_flags:
            excess_text = (
                "no credits recorded"
                if flag.excess_ratio is None
                else f"{(flag.excess_ratio * Decimal('100')):.2f}%"
            )
            lines.append(
                f"{flag.account_id:<10} Credits: {_format_money(flag.total_credits):>12}   "
                f"Debits: {_format_money(flag.total_debits):>12}   Excess: {excess_text}"
            )

    lines.extend(["", "Top 3 largest individual transactions", "-" * 40])

    if not report.top_transactions:
        lines.append("No transactions found.")
    else:
        for item in report.top_transactions:
            tx = item.transaction
            lines.append(
                f"{item.rank}. {tx.date} | {tx.account_id} | {tx.transaction_type.upper():<6} | "
                f"{_format_money(tx.amount):>12} | {tx.description}"
            )

    return "\n".join(lines)


def _format_money(value: Decimal) -> str:
    return f"${value:,.2f}"
