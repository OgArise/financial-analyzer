"""Tests for analytical routines."""

from __future__ import annotations

from decimal import Decimal

from financial_analyzer.analysis import find_excess_debits, summarize_by_account


def test_find_excess_debits_flags_accounts_above_threshold(sample_transactions: list) -> None:
    """Verify accounts above the 20% debit-over-credit threshold are flagged."""

    summaries = summarize_by_account(sample_transactions)
    flagged = find_excess_debits(summaries)

    flagged_account_ids = {item.account_id for item in flagged}

    assert "ACC1002" in flagged_account_ids
    assert "ACC1003" not in flagged_account_ids

    acc1002 = next(item for item in flagged if item.account_id == "ACC1002")
    assert acc1002.excess_ratio == Decimal("0.4")
