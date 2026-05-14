"""
conftest.py
-----------
Shared test utilities for the python_data_validator project.

This file provides helper functions and fixtures that are automatically
available to all test files in this directory. Pytest loads this file
without needing explicit imports.

Included:
- print_summary(): A helper to display a clean, readable summary of each
  validation test result so developers can quickly understand what passed,
  what failed, and why.
"""

def print_summary(test_name, result):
    """
    Print a structured, informative summary of a validation result.

    Parameters
    ----------
    test_name : str
        A descriptive name for the test being run.
    result : dict
        The dictionary returned by Validator.validate(), containing:
        - status: PASS/FAIL
        - summary: dict of counts (missing_rows, extra_rows, mismatched_values, etc.)
        - diffs: list of detailed differences (optional)
    """
    print(f"\n=== {test_name} ===")
    print(f"Status: {result['status']}")
    for key, value in result["summary"].items():
        print(f"{key}: {value}")
    print("------------------------------")
