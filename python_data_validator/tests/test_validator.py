"""
--> This file contains pytest tests for the validator. It is not used by the main application. Use if using pytest.
Test: Unified Dataset Validation
--------------------------------
This test performs a full end‑to‑end validation of a dataset by:

- Loading expected CSV data
- Loading actual SQLite data
- Running the Validator to compare both datasets
- Producing a single PASS/FAIL result
- Listing all differences when the datasets do not match
- Printing a developer‑friendly summary using print_summary() from conftest.py

This test verifies the entire workflow:
file loading → validation → reporting.
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

from python_data_validator.framework.data_loader import DataLoader
from python_data_validator.framework.validators import Validator
from python_data_validator.framework.config import (
    BASE_DATA_PATH,
    DEFAULT_ACTUAL_DB,
    DEFAULT_EXPECTED_CSV,
    DEFAULT_TABLE_NAME,
)

# NOTE:
# print_summary is NOT imported.
# Pytest automatically loads it from conftest.py.


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
    # Developer‑friendly summary
    # (print_summary comes from conftest.py)
    # -----------------------------
    print_summary("Unified Dataset Validation", result)

    # -----------------------------
    # If FAIL → print differences
    # -----------------------------
    if result["status"] == "FAIL":
        print("\nDifferences found:")
        for diff in result.get("differences", []):
            print(f"- {diff}")

    # -----------------------------
    # Perfect dataset should PASS
    # -----------------------------
    assert result["status"] == "PASS"
