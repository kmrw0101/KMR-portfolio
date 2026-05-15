import sys
from pathlib import Path

from framework.data_loader import DataLoader
from framework.validators import Validator

# Load your data
loader = DataLoader(base_data_path="data")
expected = loader.load("expected/monsters.csv")
actual = loader.load_sqlite_table("actual/monsters.sqlite", "monsters")

# Run validation
validator = Validator(key_field="id")  # or whatever your key is
result = validator.validate(expected, actual)

# Pretty print
print("\n=== Validation Results ===")
print(f"Status: {result['status']}\n")

print("Summary:")
for k, v in result["summary"].items():
    print(f"  {k}: {v}")

print("\nDifferences:")
if not result["differences"]:
    print("  None")
else:
    for diff in result["differences"]:
        print(f"  - {diff}")
