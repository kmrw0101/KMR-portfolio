"""
Test: Unified Dataset Validation
--------------------------------
This test performs a full end‑to‑end validation of a dataset by:

- Loading expected CSV data
- Loading actual SQLite data
- Running the Validator to compare both datasets
- Producing a single PASS/FAIL result
- Listing all differences when the datasets do not match

This version also prints a detailed, developer‑friendly summary using
print_summary() from conftest.py so that test output is easier to read.
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import framework
print("Using framework package from:", framework.__file__)

from pathlib import Path
from framework.data_loader import DataLoader
from framework.validators import Validator
from framework.config import (
    BASE_DATA_PATH,
    DEFAULT_ACTUAL_DB,
    DEFAULT_EXPECTED_CSV,
    DEFAULT_TABLE_NAME,
)


# ---------------------------------------------------------------------------
# Notes: What this test covers
# ---------------------------------------------------------------------------
"""
1. Ensures the expected and actual files exist
2. Loads both datasets using the DataLoader
3. Runs the Validator to compare them
4. Confirms the result structure is correct
5. Prints differences if the result is FAIL
6. Prints a readable summary for developers
7. Asserts that the configured dataset should PASS when expected and actual match
"""


# ---------------------------------------------------------------------------
# Test: Unified Dataset Validation
# ---------------------------------------------------------------------------

def test_dataset_validation():
    """
    Runs a full end‑to‑end validation of the configured dataset.
    """

    # -----------------------------
    # Resolve file paths
    # -----------------------------
    loader = DataLoader(BASE_DATA_PATH)

    actual_path = loader.base_path / DEFAULT_ACTUAL_DB
    expected_path = loader.base_path / DEFAULT_EXPECTED_CSV

    # -----------------------------
    # Ensure files exist
    # -----------------------------
    assert actual_path.exists(), f"Missing actual DB: {actual_path}"
    assert expected_path.exists(), f"Missing expected CSV: {expected_path}"

    # -----------------------------
    # Load datasets
    # -----------------------------
    expected = loader.load_csv(DEFAULT_EXPECTED_CSV)
    actual = loader.load_sqlite_table(DEFAULT_ACTUAL_DB, DEFAULT_TABLE_NAME)

    # -----------------------------
    # Run validation
    # -----------------------------
    validator = Validator()
    result = validator.validate(expected, actual)

    # -----------------------------
    # Developer-friendly summary
    # -----------------------------
    print_summary("Unified Dataset Validation", result)

    # -----------------------------
    # If FAIL → print differences
    # -----------------------------
    if result["status"] == "FAIL":
        print("\nDifferences found:")
        for diff in result["differences"]:
            print(f"- {diff}")

    # -----------------------------
    # Perfect dataset should PASS
    # -----------------------------
    assert result["status"] == "PASS"
