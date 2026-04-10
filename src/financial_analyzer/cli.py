"""Command-line entry point for financial_analyzer."""

from __future__ import annotations

import argparse
import json
import logging
from collections.abc import Sequence

from .loader import load_transactions
from .report import build_report, format_report

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Create and return the command-line argument parser."""

    parser = argparse.ArgumentParser(description="Analyze financial transactions from a CSV file.")
    parser.add_argument("csv_path", help="Path to the transactions CSV file.")
    parser.add_argument("--json", action="store_true", help="Output the report as JSON.")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging.")
    return parser


def configure_logging(verbose: bool = False) -> None:
    """Configure logging for operational visibility without mixing it into report output."""

    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s:%(name)s:%(message)s")


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI workflow and return an exit code."""

    parser = build_parser()
    args = parser.parse_args(argv)
    configure_logging(verbose=args.verbose)

    try:
        transactions = load_transactions(args.csv_path)
        report = build_report(transactions)

        if args.json:
            print(json.dumps(report.to_json(), indent=2))
        else:
            print(format_report(report))

        logger.info("Analysis completed successfully")
        return 0
    except Exception:
        logger.exception("Analysis failed")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
