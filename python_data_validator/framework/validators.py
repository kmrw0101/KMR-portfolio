"""
validators.py
-----------------------------------------
Data QA Automation Framework — Validators
-----------------------------------------

Responsibilities:
- Detect missing rows
- Detect extra rows
- Compare mismatched values
- Validate schema differences
- Identify null or empty values
- Identify duplicate rows
- Provide a unified validation entry point via `validate()`
"""

from typing import List, Dict, Any


class Validator:
    """
    Validation engine for comparing expected vs actual datasets.

    Parameters
    ----------
    key_field : str or None
        Optional field name used to uniquely identify rows.
        If None, full-row comparison is used.
    """

    def __init__(self, key_field: str | None = None):
        self.key_field = key_field

    # ---------------------------------------------------------
    # VALUE NORMALIZATION (NEW)
    # ---------------------------------------------------------
    # Converts numeric-looking strings into real ints/floats so
    # CSV and SQLite rows compare correctly.
    #
    # Examples:
    #   "14"  -> 14
    #   "1.0" -> 1.0
    #   "forest" stays "forest"
    # ---------------------------------------------------------

    def normalize_value(self, value):
        """Convert numeric-looking strings to numbers; leave real strings alone."""
        if isinstance(value, (int, float)):
            return value

        if isinstance(value, str):
            # Try converting to int
            try:
                return int(value)
            except ValueError:
                pass

            # Try converting to float
            try:
                return float(value)
            except ValueError:
                pass

            # Not numeric → keep as string
            return value

        return value

    def normalize_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize every value in a row."""
        return {k: self.normalize_value(v) for k, v in row.items()}

    # ---------------------------------------------------------
    # MISSING ROWS
    # ---------------------------------------------------------
    # Rows that appear in expected but not in actual.
    # ---------------------------------------------------------
    def find_missing_rows(self, expected, actual):
        if self.key_field:
            actual_keys = {row[self.key_field] for row in actual}
            return [row for row in expected if row[self.key_field] not in actual