"""
data_loader.py
Centralized data loading utilities for the Data QA Automation Framework.
Handles CSVs, SQLite tables, and JSON payloads.
"""

import csv
import json
import sqlite3
from pathlib import Path


class DataLoader:
    def __init__(self, base_data_path="data"):
        self.base_path = Path(base_data_path)

    # -----------------------------
    # CSV LOADING
    # -----------------------------
    def load_csv(self, filename):
        """Load a CSV file and return a list of dict rows."""
        file_path = self.base_path / filename

        if not file_path.exists():
            raise FileNotFoundError(f"CSV not found: {file_path}")

        with open(file_path, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    # -----------------------------
    # JSON LOADING
    # -----------------------------
    def load_json(self, filename):
        """Load a JSON file and return parsed data."""
        file_path = self.base_path / filename

        if not file_path.exists():
            raise FileNotFoundError(f"JSON not found: {file_path}")

        with open(file_path, mode="r", encoding="utf-8") as f:
            return json.load(f)

    # -----------------------------
    # SQLITE LOADING
    # -----------------------------
    def load_sqlite_table(self, db_name, table_name):
        """Load an entire SQLite table into a list of dict rows."""
        db_path = self.base_path / db_name

        if not db_path.exists():
            raise FileNotFoundError(f"SQLite DB not found: {db_path}")

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row

        try:
            cursor = conn.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

