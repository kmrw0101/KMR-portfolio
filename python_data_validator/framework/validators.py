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
    # VALUE NORMALIZATION
    # ---------------------------------------------------------

    def normalize_value(self, value):
        """Convert numeric-looking strings to numbers; leave real strings alone."""
        if isinstance(value, (int, float)):
            return value

        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                pass

            try:
                return float(value)
            except ValueError:
                pass

            return value

        return value

    def normalize_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize every value in a row."""
        return {k: self.normalize_value(v) for k, v in row.items()}

    # ---------------------------------------------------------
    # MISSING ROWS
    # ---------------------------------------------------------

    def find_missing_rows(self, expected, actual):
        if self.key_field:
            actual_keys = {row[self.key_field] for row in actual}
            return [row for row in expected if row[self.key_field] not in actual_keys]
        else:
            actual_set = {tuple(sorted(row.items())) for row in actual}
            return [
                row for row in expected
                if tuple(sorted(row.items())) not in actual_set
            ]

    # ---------------------------------------------------------
    # EXTRA ROWS
    # ---------------------------------------------------------

    def find_extra_rows(self, expected, actual):
        if self.key_field:
            expected_keys = {row[self.key_field] for row in expected}
            return [row for row in actual if row[self.key_field] not in expected_keys]
        else:
            expected_set = {tuple(sorted(row.items())) for row in expected}
            return [
                row for row in actual
                if tuple(sorted(row.items())) not in expected_set
            ]

    # ---------------------------------------------------------
    # MISMATCHED VALUES
    # ---------------------------------------------------------

    def find_mismatched_values(self, expected, actual):
        if not self.key_field:
            return []

        expected_map = {row[self.key_field]: row for row in expected}
        actual_map = {row[self.key_field]: row for row in actual}

        mismatches = []

        for key, exp_row in expected_map.items():
            if key not in actual_map:
                continue

            act_row = actual_map[key]

            for field in exp_row:
                exp_val = exp_row[field]
                act_val = act_row.get(field)

                if exp_val != act_val:
                    mismatches.append({
                        "key": key,
                        "field": field,
                        "expected": exp_val,
                        "actual": act_val
                    })

        return mismatches

    # ---------------------------------------------------------
    # SCHEMA VALIDATION
    # ---------------------------------------------------------

    def validate_schema(self, expected, actual):
        if not expected or not actual:
            return {"missing_columns": [], "extra_columns": []}

        expected_cols = set(expected[0].keys())
        actual_cols = set(actual[0].keys())

        return {
            "missing_columns": sorted(expected_cols - actual_cols),
            "extra_columns": sorted(actual_cols - expected_cols),
        }

    # ---------------------------------------------------------
    # NULL CHECKS
    # ---------------------------------------------------------

    def check_nulls(self, rows):
        nulls = []
        for idx, row in enumerate(rows):
            for field, value in row.items():
                if value in (None, "", "NULL", "null"):
                    nulls.append({
                        "row_index": idx,
                        "field": field,
                        "value": value
                    })
        return nulls

    # ---------------------------------------------------------
    # DUPLICATE CHECKS
    # ---------------------------------------------------------

    def check_duplicates(self, rows):
        seen = set()
        duplicates = []

        for row in rows:
            if self.key_field:
                key = row[self.key_field]
            else:
                key = tuple(sorted(row.items()))

            if key in seen:
                duplicates.append(row)
            else:
                seen.add(key)

        return duplicates

    # ---------------------------------------------------------
    # MAIN VALIDATION ENTRY POINT
    # ---------------------------------------------------------

    def validate(self, expected, actual):
        """
        Run all validation checks and return a fully structured result.

        Returns
        -------
        dict with:
            - status: PASS or FAIL
            - summary: dict of counts for every check type
            - differences: list of detailed issue descriptions
        """

        # Normalize values BEFORE comparing
        expected = [self.normalize_row(r) for r in expected]
        actual = [self.normalize_row(r) for r in actual]

        # Run all checks
        missing_rows = self.find_missing_rows(expected, actual)
        extra_rows = self.find_extra_rows(expected, actual)
        mismatched_values = self.find_mismatched_values(expected, actual)
        schema_diffs = self.validate_schema(expected, actual)
        nulls = self.check_nulls(actual)
        duplicates = self.check_duplicates(actual)

        # Build summary (always include all categories)
        summary = {
            "missing_rows": len(missing_rows),
            "extra_rows": len(extra_rows),
            "mismatched_values": len(mismatched_values),
            "missing_columns": len(schema_diffs["missing_columns"]),
            "extra_columns": len(schema_diffs["extra_columns"]),
            "nulls": len(nulls),
            "duplicates": len(duplicates),
        }

        # Build unified differences list
        differences = []

        for row in missing_rows:
            differences.append({"type": "missing_row", "row": row})

        for row in extra_rows:
            differences.append({"type": "extra_row", "row": row})

        for mismatch in mismatched_values:
            differences.append({"type": "mismatched_value", "detail": mismatch})

        for col in schema_diffs["missing_columns"]:
            differences.append({"type": "missing_column", "column": col})

        for col in schema_diffs["extra_columns"]:
            differences.append({"type": "extra_column", "column": col})

        for item in nulls:
            differences.append({"type": "null_value", "detail": item})

        for row in duplicates:
            differences.append({"type": "duplicate_row", "row": row})

        # Final PASS/FAIL
        status = "PASS" if not differences else "FAIL"

        return {
            "status": status,
            "summary": summary,
            "differences": differences
        }
