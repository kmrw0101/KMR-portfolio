"""
data_loader.py
-----------------------------------------
Data QA Automation Framework — Data Loader
-----------------------------------------

Responsibilities:
- Load CSV files into list[dict]
- Load JSON files into Python objects
- Load SQLite tables into list[dict]
- Generic loader → automatically selects CSV or JSON based on file extension
- Resolve all file paths relative to the data directory
"""


import csv
import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Any


class DataLoader:
    """
    A flexible loader for CSV, JSON, and SQLite data sources.

    Parameters
    ----------
    base_data_path : str
        The root folder where all data files live (default: "data").
    """

    def __init__(self, base_data_path: str = "data"):
        self.base_path = Path(base_data_path)

    # ---------------------------------------------------------
    # Internal helper: resolve file paths
    # ---------------------------------------------------------
    def _resolve(self, filename: str) -> Path:
        """Return the full path to a file inside the base data directory."""
        return self.base_path / filename

    # ---------------------------------------------------------
    # CSV LOADING
    # ---------------------------------------------------------
    def load_csv(self, filename: str) -> List[Dict[str, Any]]:
        """Load a CSV file and return a list of dictionary rows."""
        file_path = self._resolve(filename)

        if not file_path.exists():
            raise FileNotFoundError(f"CSV not found: {file_path}")

        with open(file_path, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    # ---------------------------------------------------------
    # JSON LOADING
    # ---------------------------------------------------------
    def load_json(self, filename: str) -> Any:
        """Load a JSON file and return parsed data."""
        file_path = self._resolve(filename)

        if not file_path.exists():
            raise FileNotFoundError(f"JSON not found: {file_path}")

        with open(file_path, mode="r", encoding="utf-8") as f:
            return json.load(f)

    # ---------------------------------------------------------
    # SQLITE LOADING
    # ---------------------------------------------------------
    def load_sqlite_table(self, db_name: str, table_name: str) -> List[Dict[str, Any]]:
        """Load an entire SQLite table into a list of dictionary rows."""
        db_path = self._resolve(db_name)

        if not db_path.exists():
            raise FileNotFoundError(f"SQLite DB not found: {db_path}")

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row

        try:
            # Check table exists
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,)
            )
            if cursor.fetchone() is None:
                raise ValueError(f"Table '{table_name}' does not exist in {db_path}")

            cursor = conn.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        finally:
            conn.close()

    # ---------------------------------------------------------
    # GENERIC LOADER
    # ---------------------------------------------------------
    def load(self, filename: str) -> Any:
        """
        Load a file based on its extension.
        CSV → list[dict]
        JSON → dict or list
        SQLite → requires load_sqlite_table() instead
        """
        ext = filename.split(".")[-1].lower()

        if ext == "csv":
            return self.load_csv(filename)
        elif ext == "json":
            return self.load_json(filename)
        elif ext == "sqlite":
            raise ValueError("Use load_sqlite_table() for SQLite tables.")
        else:
            raise ValueError(f"Unsupported file type: {ext}")
