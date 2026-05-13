"""
Test: Perfect Match Validation
Validates that the actual monsters table in SQLite matches the expected CSV.
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import sqlite3
import csv
from pathlib import Path


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
ACTUAL_DB: Path = PROJECT_ROOT / "mini-project" / "data" / "actual" / "monsters.sqlite"
EXPECTED_CSV: Path = PROJECT_ROOT / "mini-project" / "data" / "expected" / "monsters.csv"


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_sqlite_rows(db_path: Path) -> list[tuple]:
    """
    Returns all rows from the monsters table in SQLite, ordered by id.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM monsters ORDER BY id;")
    rows = cursor.fetchall()
    conn.close()
    return rows


def load_csv_rows(csv_path: Path) -> list[tuple]:
    """
    Returns all rows from the expected CSV as tuples, skipping the header.
    """
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        return [tuple(row) for row in reader]


# ---------------------------------------------------------------------------
# Test: Perfect Match
# ---------------------------------------------------------------------------

def test_monsters_perfect_match() -> None:
    """
    Ensures the SQLite monsters table matches the expected CSV exactly.
    """
    sqlite_rows = load_sqlite_rows(ACTUAL_DB)
    csv_rows = load_csv_rows(EXPECTED_CSV)

    converted_csv: list[tuple] = []
    for row in csv_rows:
        converted_csv.append((
            int(row[0]),
            row[1],
            row[2],
            int(row[3]),
            int(row[4])
        ))

    assert sqlite_rows == converted_csv
