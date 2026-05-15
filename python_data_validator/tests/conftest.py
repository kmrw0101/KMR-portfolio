"""
conftest.py
-----------
Shared test utilities for the python_data_validator project.

Pytest automatically loads this file for all tests in this directory.
Anything defined here (like helper functions or fixtures) becomes
available to tests *without* needing an import.

Included:
- print_summary(): Prints a clean, readable summary of a validation result.
"""

def print_summary(test_name, result):
    """
    Print a structured summary of a validation result.

    Parameters
    ----------
    test_name : str
        A descriptive label for the test being run.

    result : dict
        The dictionary returned by Validator.validate(), expected to contain:
            - "status": PASS or FAIL
            - "summary": dict of numeric counts
            - "differences": list of mismatch descriptions
    """

    print(f"\n=== {test_name} ===")
    print(f"Status: {result.get('status', 'UNKNOWN')}")

    # Summary counts
    summary = result.get("summary", {})
    if summary:
        print("\nSummary:")
        for key, value in summary.items():
            print(f"- {key}: {value}")
    else:
        print("\nSummary: (none provided)")

    # Differences
    diffs = result.get("differences", [])
    if diffs:
        print("\nDifferences:")
        for diff in diffs:
            print(f"- {diff}")
    else:
        print("\nDifferences: None")

    print("------------------------------\n")
