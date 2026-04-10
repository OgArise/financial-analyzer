"""Tests for report construction and serialization."""

from __future__ import annotations

from financial_analyzer.report import build_report, format_report


def test_report_formats_and_serializes(sample_transactions: list) -> None:
    """Verify report output is both readable and JSON-ready."""

    report = build_report(sample_transactions)
    formatted = format_report(report)
    payload = report.to_json()

    assert "FINANCIAL TRANSACTION SUMMARY REPORT" in formatted
    assert "ACC1001" in formatted
    assert "account_summaries" in payload
    assert "top_transactions" in payload
