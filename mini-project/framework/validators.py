"""
validators.py
Core validation utilities for the Data QA Automation Framework.
Provides row‑level and dataset‑level comparison functions for detecting
missing records, extra records, mismatched values, schema differences,
nulls, duplicates, and other data quality issues.
"""

class Validator:
    def __init__(self, key_field=None):
        """
        key_field: Optional field name used to uniquely identify rows.
        If None, full-row comparison is used.
        """
        self.key_field = key_field

    # ---------------------------------------------------------
    # Find missing rows (in expected but not in actual)
    # ---------------------------------------------------------
    def find_missing_rows(self, expected, actual):
        if self.key_field:
            actual_keys = {row[self.key_field] for row in actual}
            return [row for row in expected if row[self.key_field] not in actual_keys]
        else:
            return [row for row in expected if row not in actual]

    # ---------------------------------------------------------
    # Find extra rows (in actual but not in expected)
    # ---------------------------------------------------------
    def find_extra_rows(self, expected, actual):
        if self.key_field:
            expected_keys = {row[self.key_field] for row in expected}
            return [row for row in actual if row[self.key_field] not in expected_keys]
        else:
            return [row for row in actual if row not in expected]

    # ---------------------------------------------------------
    # Find mismatched values for matching keys
    # ---------------------------------------------------------
    def find_mismatched_values(self, expected, actual):
        if not self.key_field:
            return []  # cannot compare values without a key

        # Build lookup tables
        expected_map = {row[self.key_field]: row for row in expected}
        actual_map = {row[self.key_field]: row for row in actual}

        mismatches = []

        for key, exp_row in expected_map.items():
            if key not in actual_map:
                continue  # handled by missing rows

            act_row = actual_map[key]

            # Compare each field
            for field in exp_row:
                if field not in act_row:
                    mismatches.append({
                        "key": key,
                        "field": field,
                        "expected": exp_row[field],
                        "actual": None
                    })
                elif exp_row[field] != act_row[field]:
                    mismatches.append({
                        "key": key,
                        "field": field,
                        "expected": exp_row[field],
                        "actual": act_row[field]
                    })

        return mismatches

    # ---------------------------------------------------------
    # Validate schema differences
    # ---------------------------------------------------------
    def validate_schema(self, expected, actual):
        if not expected or not actual:
            return {"missing_columns": [], "extra_columns": []}

        expected_cols = set(expected[0].keys())
        actual_cols = set(actual[0].keys())

        return {
            "missing_columns": sorted(list(expected_cols - actual_cols)),
            "extra_columns": sorted(list(actual_cols - expected_cols)),
        }

    # ---------------------------------------------------------
    # Check for null or empty values
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
    # Check for duplicate rows
    # ---------------------------------------------------------
    def check_duplicates(self, rows):
        seen = set()
        duplicates = []

        for row in rows:
            if self.key_field:
                key = row[self.key_field]
            else:
                key = tuple(sorted(row.items()))  # full-row uniqueness

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
        Run all validation checks and return a structured result object.
        """
        result = {
            "missing_rows": self.find_missing_rows(expected, actual),
            "extra_rows": self.find_extra_rows(expected, actual),
            "mismatched_values": self.find_mismatched_values(expected, actual),
            "schema_differences": self.validate_schema(expected, actual),
            "nulls": self.check_nulls(actual),
            "duplicates": self.check_duplicates(actual),
        }

        # Determine pass/fail
        result["passed"] = (
            not result["missing_rows"]
            and not result["extra_rows"]
            and not result["mismatched_values"]
            and not result["schema_differences"]["missing_columns"]
            and not result["schema_differences"]["extra_columns"]
            and not result["nulls"]
            and not result["duplicates"]
        )

        return result
