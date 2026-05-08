from pathlib import Path
import csv
import sqlite3

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent / "data"
ACTUAL_DIR = DATA_DIR / "actual"
EXPECTED_FILE = DATA_DIR / "expected" / "monsters.csv"
BAD_DB = ACTUAL_DIR / "monsters_bad.sqlite"


def read_expected_rows():
    with EXPECTED_FILE.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_bad_database_exists():
    assert BAD_DB.exists(), f"Missing bad database: {BAD_DB}"


def test_expected_csv_exists():
    assert EXPECTED_FILE.exists(), f"Missing expected CSV: {EXPECTED_FILE}"


def test_expected_csv_loads():
    rows = read_expected_rows()
    assert rows, "Expected CSV should contain at least one row"


def test_bad_database_connects():
    with sqlite3.connect(BAD_DB) as conn:
        conn.execute("PRAGMA schema_version")
