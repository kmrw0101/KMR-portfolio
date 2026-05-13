"""
Test: Dataset Discovery
Validates that the dataset discovery function correctly identifies the monsters
dataset and groups actual and expected files under the proper dataset name.
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from pathlib import Path

from mini_project.app.validate_app import discover_datasets, ACTUAL_DIR, EXPECTED_DIR


# ---------------------------------------------------------------------------
# Test: Dataset Discovery for Monsters
# ---------------------------------------------------------------------------
# This test verifies that:
#   - monsters.sqlite and monsters_bad.sqlite are discovered in the actual/ folder
#   - monsters.csv is discovered in the expected/ folder
#   - all three files are grouped under the dataset name "monsters"
#   - the returned structure matches the expected dictionary format
#
# This test uses real files from the project, which keeps things simple and
# ensures the discovery logic works in the real environment.
# ---------------------------------------------------------------------------

def test_dataset_discovery_monsters():
    datasets = discover_datasets()

    # Ensure the monsters dataset exists
    assert "monsters" in datasets

    monsters_info = datasets["monsters"]

    # Validate actual files
    actual_files = [p.name for p in monsters_info["actual"]]
    assert "monsters.sqlite" in actual_files
    assert "monsters_bad.sqlite" in actual_files

    # Validate expected files
    expected_files = [p.name for p in monsters_info["expected"]]
    assert "monsters.csv" in expected_files

    # Ensure the directories being scanned are correct
    assert ACTUAL_DIR.exists()
    assert EXPECTED_DIR.exists()

    # Ensure the structure matches the expected format
    assert isinstance(monsters_info["actual"], list)
    assert isinstance(monsters_info["expected"], list)
    assert all(isinstance(p, Path) for p in monsters_info["actual"])
    assert all(isinstance(p, Path) for p in monsters_info["expected"])
