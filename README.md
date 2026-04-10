# financial-analyzer

`financial-analyzer` is a Python package and CLI for loading transaction data from CSV, validating it, running lightweight control-style checks, and returning the results as either readable text or JSON-ready output.

It is designed as a small but production-minded portfolio project: structured, testable, typed, and ready to extend into API-based workflows.

---

## Features

- Load and validate financial transaction CSV files
- Summarize total credits and debits per account
- Flag accounts where debits exceed credits by more than 20%
- Identify the top 3 largest individual transactions
- Return reports as either plain text or JSON-ready data
- Run through a CLI or import as a Python package

---

## Why this project exists

This project was built to demonstrate more than basic scripting.

It shows how to structure a small Python codebase into clear modules, validate input safely, separate analysis from reporting, expose a command-line interface, and support software quality practices such as testing, linting, typing, and CI.

In short: not just code that works, but code that is meant to be read, extended, and trusted.

---

## Example usage

### CLI output

```powershell
financial-analyzer data\sample_transactions.csv
JSON output
financial-analyzer data\sample_transactions.csv --json
Module usage
from financial_analyzer.loader import load_transactions
from financial_analyzer.report import build_report, format_report

transactions = load_transactions("data/sample_transactions.csv")
report = build_report(transactions)

print(format_report(report))
print(report.to_json())
Sample output
FINANCIAL TRANSACTION SUMMARY REPORT
====================================

Total credits and debits per account
------------------------------------
ACC1001    Credits:    $4,900.00   Debits:    $2,300.00
ACC1002    Credits:    $6,300.00   Debits:    $4,400.00
ACC1003    Credits:    $2,150.00   Debits:    $1,025.00
ACC1004    Credits:   $10,000.00   Debits:    $6,650.00
Project structure
financial_analyzer/
├── pyproject.toml
├── README.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   └── financial_analyzer/
│       ├── __init__.py
│       ├── analysis.py
│       ├── cli.py
│       ├── loader.py
│       ├── models.py
│       └── report.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_analysis.py
│   ├── test_cli.py
│   ├── test_loader.py
│   └── test_report.py
└── data/
    └── sample_transactions.csv
Installation
Windows PowerShell

After unzipping or cloning the project, open PowerShell in the project root and run:

python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .[dev]
Run tests
pytest tests -q
Development checks
ruff check .
mypy src
pytest tests
Analytical rule: 20% excess debit threshold

The 20% threshold is a simple screening rule, not a universal accounting standard.

If an account’s total debits exceed total credits by more than 20%, the account is flagged for review. In a real financial environment, that threshold would usually be tuned by account type, business model, seasonality, and historical patterns. Here, it serves as a lightweight early-warning control.

Output design

Operational messages use logging.

The final report is kept separate from logging and can be rendered in two ways:

human-readable text via format_report(...)
JSON-ready structured output via to_json()

This makes the package easier to extend into APIs, scheduled jobs, or dashboard workflows.

Quality checks

This project includes:

modular package structure
docstrings on public functions
input validation and error handling
pytest-based tests
Ruff linting
mypy type checking
GitHub Actions CI
Roadmap

Planned next improvements:

configurable debit threshold from the CLI
configurable top-N transaction reporting
date and account filtering
richer JSON schema for downstream systems
FastAPI wrapper for API-based use
GitHub

To publish the project:

git init
git add .
git commit -m "Initial commit: financial-analyzer"
git branch -M main
git remote add origin https://github.com/<your-username>/financial-analyzer.git
git push -u origin main
License

MIT


---

Paste that in. Commit it. Push it.

Then we move to the next level: turning this into an API and making it *actually impressive*.
