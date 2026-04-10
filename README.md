# financial-analyzer

A clean Python package for loading financial transactions from CSV, validating them, running a few useful control-style checks, and returning the result as either readable text or JSON-ready data.

This version is built to be portfolio-worthy.

It has structure. It has tests. It has linting. It has typing. It has CI.

## What it does

- Loads and validates CSV transaction data
- Summarizes total credits and debits per account
- Flags accounts where debits exceed credits by more than 20%
- Returns the top 3 largest transactions
- Produces both plain-text and JSON-ready report output

## Project structure

```text
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
│   ├── test_loader.py
│   └── test_report.py
└── data/
    └── sample_transactions.csv
```

## The Windows issue you hit

You were not inside the project directory.

That one mistake caused almost everything else:
- `pip install -e .[dev]` looked at `C:\Users\ogonn` instead of the project folder
- `pytest` searched your whole home directory and crashed on protected Windows folders
- `financial-analyzer` was not found because the package never got installed
- `source .venv/bin/activate` is a Unix command, not a PowerShell command

## Correct setup on Windows PowerShell

After unzipping the project, go into the project folder first.

```powershell
cd C:\path\to\financial-analyzer
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .[dev]
```

If PowerShell blocks activation, run this once in the same PowerShell window:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Run tests

Run pytest from the project root only:

```powershell
pytest
```

Or explicitly point to the tests folder:

```powershell
pytest tests
```

## Run the CLI

Once installed:

```powershell
financial-analyzer data\sample_transactions.csv
financial-analyzer data\sample_transactions.csv --json
```

Fallback if your shell has not picked up the script yet:

```powershell
python -m financial_analyzer.cli data\sample_transactions.csv
python -m financial_analyzer.cli data\sample_transactions.csv --json
```

## Development checks

```powershell
ruff check .
mypy .
pytest
```

## What makes the 20% threshold useful

The threshold is not a law of nature. It is a simple screening rule.

If debits exceed credits by more than 20%, that account may be under unusual cash outflow pressure. In a real finance environment, the threshold would be tuned by account type, business line, seasonality, and historical behavior. Here, it serves as a lightweight early-warning control.

## GitHub steps

Create a new repository called `financial-analyzer`, then run:

```powershell
git init
git add .
git commit -m "Initial commit: financial-analyzer"
git branch -M main
git remote add origin https://github.com/<your-username>/financial-analyzer.git
git push -u origin main
```

## Notes

Operational messages use logging.

The final report still goes to standard output from the CLI, because that is not an operational log. That is the actual product of the command.
