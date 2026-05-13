# Mini Project: Monster Data Validation

## Overview

This is a **SQL portfolio project** demonstrating data validation, ETL testing, and QA automation.

The project compares actual data outputs (from a simulated data pipeline) against a golden truth CSV file to identify discrepancies and validate data quality.

## Project Structure
mini-project/
├── framework/                 # Core validation framework
│   ├── data_loader.py         # Load data from SQLite & CSV
│   ├── validators.py          # Validation & comparison logic
│   ├── api_client.py          # (Reserved for future API integration)
│   ├── config.py              # (Reserved for configuration)
│   └── init.py            # Package initialization
│
├── tests/                     # Test suites
│   ├── test_monsters_perfect.py   # Tests for GOOD data
│   ├── test_monsters_diffs.py     # Tests for BAD data (should find diffs)
│   └── init.py            # Package initialization
│
├── data/                      # Test datasets
│   ├── actual/                # Data output from pipeline
│   │   ├── monsters.sqlite        # ✓ GOOD (pipeline succeeded)
│   │   └── monsters_bad.sqlite    # ✗ BAD (pipeline broken)
│   │
│   └── expected/              # Golden truth (answer key)
│       └── monsters.csv           # Reference data
│
├── basic_python_exercises.py  # Python practice exercises
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
## Framework Components

### DataLoader (`framework/data_loader.py`)

Handles loading data from multiple sources:
- SQLite databases  
- CSV files  
- Data transformation and normalization  

### Validators (`framework/validators.py`)

Core validation logic:
- Row-level comparisons  
- Column-level validation  
- Difference detection and reporting  
- Data type checking  

## Test Suites

### `test_monsters_perfect.py`

Validates the GOOD dataset:
- Loads `monsters.sqlite` (successful pipeline output)
- Compares against `monsters.csv` (golden truth)
- **Expected outcome:** All tests pass ✓

### `test_monsters_diffs.py`

Validates the BAD dataset:
- Loads `monsters_bad.sqlite` (broken pipeline output)
- Compares against `monsters.csv` (golden truth)
- Identifies and logs all discrepancies
- **Expected outcome:** Tests find differences ⚠️

## Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test suite
pytest tests/test_monsters_perfect.py
pytest tests/test_monsters_diffs.py

# Run with verbose output
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=framework
